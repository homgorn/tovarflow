"""Query the local Q-Parser knowledge base.

Usage:
    python tools/query_kb.py "webhook signature"
    python tools/query_kb.py "лимит парсингов" --limit 5
    python tools/query_kb.py --sql "select path,title from sources limit 5"
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "qparser.sqlite"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default=None)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--sql", default=None)
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    if args.sql:
        for row in conn.execute(args.sql):
            print(" | ".join(str(x) for x in row))
        return 0
    if not args.query:
        parser.error("provide a query or --sql")

    # FTS5 treats punctuation as syntax; quote each token to keep it literal.
    tokens = [t for t in "".join(c if c.isalnum() or c.isspace() else " " for c in args.query).split() if t]
    match = " OR ".join(f'"{t}"' for t in tokens)
    rows = conn.execute(
        "SELECT path, heading, snippet(chunks_fts, 0, '[', ']', ' … ', 18) "
        "FROM chunks_fts WHERE chunks_fts MATCH ? LIMIT ?",
        (match, args.limit),
    ).fetchall()
    for path, heading, snippet in rows:
        print(f"\n{path}  § {heading}\n  {snippet}")
    if not rows:
        print("no matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
