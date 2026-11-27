"""Answer-First / AEO gate for generated wiki pages and optional HTML.

Usage:
    python tools/aeo_lint.py
    python tools/aeo_lint.py --html path/to/product.html
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
PAGES = ["index.md", "topics/api.md", "topics/pricing.md",
         "topics/limits-and-quotas.md", "topics/aeo.md"]

FACT = re.compile(r"(?:\d+(?:[.,]\d+)?|₽|\$|USD|RUB|CNY|20\d\d-\d\d-\d\d|\bAPI\b|\bSKU\b)")


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def check_markdown(path: Path) -> tuple[bool, list[str]]:
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    h1 = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    problems = []
    if h1 is None:
        return False, ["no H1"]
    lead = " ".join(lines[h1 + 1:h1 + 8])
    lead = re.sub(r"^#{2,6}\s+", " ", lead).strip()[:300]
    facts = FACT.findall(lead)
    if len(facts) < 3:
        problems.append(f"answer-first has {len(facts)} facts in first 300 chars (need >=3)")
    over = [len(p) for p in re.split(r"\n\s*\n", text)
            if len(p) > 2000 and not (p.lstrip().startswith("|") and "---" in p)]
    if over:
        problems.append(f"{len(over)} blocks over 2000 chars without a heading")
    if "|" not in text:
        problems.append("no table")
    if not re.search(r"https?://", text):
        problems.append("no source link")
    return not problems, problems


def check_html(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    problems = []
    if not re.search(r"<h1[^>]*>", text, re.I):
        problems.append("no H1 in HTML")
    body = text.lower().find("<body")
    visible = text[body:] if body != -1 else text
    visible = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", visible, flags=re.S | re.I)
    head = re.sub(r"<[^>]+>", " ", visible)
    head = re.sub(r"\s+", " ", head).strip()[:300]
    if len(FACT.findall(head)) < 3:
        problems.append("first 300 chars have fewer than 3 facts")
    if not re.search(r"<table", text, re.I):
        problems.append("no <table>")
    if not re.search(r"<dl", text, re.I):
        problems.append("no <dl>")
    if not re.search(r"https?://", text):
        problems.append("no primary source link")
    return not problems, problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default=None)
    args = parser.parse_args()

    failed = 0
    for rel in PAGES:
        path = WIKI / rel
        if not path.exists():
            print(f"FAIL {rel}: missing")
            failed += 1
            continue
        ok, problems = check_markdown(path)
        print(("PASS " if ok else "FAIL ") + rel + (" — " + "; ".join(problems) if problems else ""))
        failed += 0 if ok else 1
    if args.html:
        ok, problems = check_html(Path(args.html))
        print(("PASS " if ok else "FAIL ") + args.html + (" — " + "; ".join(problems) if problems else ""))
        failed += 0 if ok else 1
    print(f"\nAEO lint: {len(PAGES) + (1 if args.html else 0) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
