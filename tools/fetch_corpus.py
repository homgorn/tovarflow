"""Fetch the canonical Q-Parser documentation corpus.

Usage:
    python tools/fetch_corpus.py            # incremental fetch
    python tools/fetch_corpus.py --force    # refetch everything
    python tools/fetch_corpus.py --only format/ymlformat
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

sys.path.insert(0, str(Path(__file__).parent))
from corpus_urls import inventory  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "docs" / "research" / "qparser" / "raw"
PAGES_DIR = ROOT / "docs" / "research" / "qparser" / "pages"
META_DIR = ROOT / "docs" / "research" / "qparser"
MANIFEST = META_DIR / "manifest.jsonl"
COVERAGE = META_DIR / "coverage.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 q-parser-research/1.0",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.6",
}

DROPPED_TAGS = ["script", "style", "noscript", "svg", "form", "button"]
BOILERPLATE_MARKERS = (
    "Навигация по базе знаний",
    "Все права защищены",
)


def slug_for(path: str) -> str:
    slug = path.strip("/").replace("/", "__") or "root"
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", slug)


def clean_markdown(text: str) -> str:
    text = text.replace("\u00a0", " ")
    # drop site-wide navigation tail if it survived extraction
    for marker in BOILERPLATE_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def extract(html: str, path: str = "") -> tuple[str, str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.get_text(" ", strip=True) if title_tag else (soup.title.get_text(strip=True) if soup.title else "")

    prose = soup.select_one("main div.prose.max-w-none")
    if path.startswith("/howto") and prose is not None and len(prose.get_text(" ", strip=True)) >= 300:
        article = prose
    else:
        # Landing, pricing and FAQ pages keep their content outside <main>.
        article = soup.body
    if article is None:
        return title, "", []

    for tag in article.find_all(DROPPED_TAGS):
        tag.decompose()
    for tag in article.find_all(["header", "nav", "footer", "aside"]):
        tag.decompose()
    for tag in article.select(".page-title, .bg-\\[\\#444f60\\]"):
        tag.decompose()

    links = sorted({a["href"] for a in article.find_all("a", href=True) if a["href"].startswith("/")})
    md = markdownify(str(article), heading_style="ATX", bullets="-", strip=DROPPED_TAGS)
    return title, clean_markdown(md), links


def fetch_one(session: requests.Session, url: str, force: bool) -> dict:
    path = url.replace("https://q-parser.ru", "") or "/"
    slug = slug_for(path)
    raw_path = RAW_DIR / f"{slug}.html"
    md_path = PAGES_DIR / f"{slug}.md"
    record = {
        "url": url,
        "path": path,
        "slug": slug,
        "fetched_at": None,
        "http_status": None,
        "bytes": 0,
        "sha256": None,
        "title": None,
        "md_chars": 0,
        "cached": False,
        "error": None,
    }

    if raw_path.exists() and md_path.exists() and not force:
        record["cached"] = True
        record["bytes"] = raw_path.stat().st_size
        record["md_chars"] = md_path.stat().st_size
        return record

    last_error = None
    for attempt in range(1, 5):
        try:
            resp = session.get(url, headers=HEADERS, timeout=45)
            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                raise RuntimeError(f"retryable status {resp.status_code}")
            resp.raise_for_status()
            resp.encoding = "utf-8"
            html = resp.content.decode("utf-8", errors="replace")
            title, md, links = extract(html, path)
            stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
            digest = hashlib.sha256(html.encode("utf-8")).hexdigest()
            frontmatter = (
                "---\n"
                f"url: {url}\n"
                f"path: {path}\n"
                f"title: {json.dumps(title, ensure_ascii=False)}\n"
                f"fetched_at: {stamp}\n"
                f"http_status: {resp.status_code}\n"
                f"sha256: {digest}\n"
                f"links: {json.dumps(links, ensure_ascii=False)}\n"
                "---\n\n"
            )
            raw_path.write_text(html, encoding="utf-8")
            md_path.write_text(frontmatter + md, encoding="utf-8")
            record.update(
                fetched_at=stamp,
                http_status=resp.status_code,
                bytes=len(html.encode("utf-8")),
                sha256=digest,
                title=title,
                md_chars=len(md),
            )
            return record
        except Exception as exc:  # noqa: BLE001 - recorded per URL
            last_error = str(exc)
            time.sleep(min(30, (2 ** attempt) + random.random()))
    record["error"] = last_error
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only", default=None)
    parser.add_argument("--delay", type=float, default=0.9)
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    urls = inventory()
    if args.only:
        urls = [u for u in urls if args.only in u["url"]]

    session = requests.Session()
    existing: dict[str, dict] = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            if line.strip():
                prev = json.loads(line)
                existing[prev["url"]] = prev

    records = []
    ok = 0
    for i, item in enumerate(urls, 1):
        rec = fetch_one(session, item["url"], args.force)
        rec["kind"] = item["kind"]
        rec["section"] = item["section"]
        records.append(rec)
        status = rec["http_status"] or "ERR"
        flag = "cache" if rec["cached"] else status
        print(f"[{i:03}/{len(urls):03}] {flag} {rec['path']} ({rec['md_chars']} chars)")
        if rec["http_status"] == 200 or rec["cached"]:
            ok += 1
        if not rec["cached"]:
            time.sleep(args.delay)

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for rec in records:
        rec["run_at"] = stamp
        existing[rec["url"]] = rec

    ordered = [existing[u["url"]] for u in inventory() if u["url"] in existing]
    with MANIFEST.open("w", encoding="utf-8") as fh:
        for rec in ordered:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    with COVERAGE.open("w", encoding="utf-8") as fh:
        fh.write("url,http_status,md_chars,error,cached\n")
        for rec in ordered:
            err = (rec["error"] or "").replace('"', "'")
            fh.write(f'"{rec["url"]}",{rec["http_status"] or ""},{rec["md_chars"]},"{err}",{rec["cached"]}\n')

    print(f"\nFetched/verified {ok}/{len(records)} pages; manifest: {MANIFEST}")
    return 0 if ok == len(records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
