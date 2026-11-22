"""Verify corpus coverage and rebuild the manifest from the fetched files.

Usage:
    python tools/verify_coverage.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from corpus_urls import inventory  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "docs" / "research" / "qparser" / "raw"
PAGES = ROOT / "docs" / "research" / "qparser" / "pages"
META = ROOT / "docs" / "research" / "qparser"
MANIFEST = META / "manifest.jsonl"
COVERAGE = META / "coverage.csv"
REPORT = META / "COVERAGE.md"


def slug_for(path: str) -> str:
    import re
    slug = path.strip("/").replace("/", "__") or "root"
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", slug)


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta


def main() -> int:
    rows = []
    missing = []
    thin = []
    for item in inventory():
        path = item["path"]
        slug = slug_for(path)
        md_path = PAGES / f"{slug}.md"
        raw_path = RAW / f"{slug}.html"
        if not md_path.exists():
            missing.append(path)
            continue
        text = md_path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        body = text.split("\n---\n", 1)[-1]
        raw_bytes = raw_path.read_bytes() if raw_path.exists() else b""
        rec = {
            "url": item["url"],
            "path": path,
            "slug": slug,
            "section": item["section"],
            "kind": item["kind"],
            "title": meta.get("title"),
            "fetched_at": meta.get("fetched_at"),
            "http_status": meta.get("http_status"),
            "bytes": len(raw_bytes),
            "sha256": hashlib.sha256(raw_bytes).hexdigest() if raw_bytes else meta.get("sha256"),
            "md_chars": len(body),
            "cached": False,
            "error": None,
        }
        rows.append(rec)
        if rec["http_status"] != "200":
            thin.append((path, rec["http_status"], rec["md_chars"]))
        elif rec["md_chars"] < 200:
            thin.append((path, "thin", rec["md_chars"]))

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with MANIFEST.open("w", encoding="utf-8") as fh:
        for rec in rows:
            rec["run_at"] = stamp
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    with COVERAGE.open("w", encoding="utf-8") as fh:
        fh.write("url,http_status,md_chars,error\n")
        for rec in rows:
            fh.write(f'"{rec["url"]}",{rec["http_status"]},{rec["md_chars"]},""\n')

    total_chars = sum(r["md_chars"] for r in rows)
    report = [
        "# Corpus coverage — Q-Parser",
        "",
        f"Generated: {stamp}",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Canonical URLs in inventory | {len(inventory())} |",
        f"| Present and HTTP 200 | {sum(1 for r in rows if r['http_status'] == '200')} |",
        f"| Missing | {len(missing)} |",
        f"| Thin / non-200 | {len(thin)} |",
        f"| Total extracted characters | {total_chars:,} |",
        "",
        "## Missing",
        "",
    ]
    report += [f"- `{p}`" for p in missing] or ["- none"]
    report += ["", "## Thin / non-200 pages", ""]
    report += [f"- `{p}` — status `{s}`, {c} chars" for p, s, c in thin] or ["- none"]
    report += [
        "",
        "## Method",
        "",
        "- Canonical documentation URLs only. The sitemap's `/catalog/<city>/<category>` permutations are excluded by design.",
        "- Each page is stored twice: raw HTML (`raw/`) and cleaned Markdown (`pages/`) with source frontmatter.",
        "- The manifest records HTTP status, byte size, SHA-256, title and fetch timestamp for every URL.",
        "",
        "## Rebuild",
        "",
        "```bash",
        "python tools/fetch_corpus.py            # incremental",
        "python tools/fetch_corpus.py --force    # full refetch",
        "python tools/extract_qparser.py",
        "python tools/build_knowledge.py",
        "python tools/verify_coverage.py",
        "```",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "inventory": len(inventory()),
        "present": len(rows),
        "ok": sum(1 for r in rows if r["http_status"] == "200"),
        "missing": missing,
        "thin": thin,
        "chars": total_chars,
    }, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
