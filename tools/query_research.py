"""Query the research knowledge base.

Usage:
    python tools/query_research.py "WB token scope"
    python tools/query_research.py --sql "select name,layer,role,status from marketplaces limit 10"
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "research.sqlite"


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

    tokens = [t for t in "".join(c if c.isalnum() or c.isspace() else " " for c in args.query).split() if t]
    match = " OR ".join(f'"{t}"' for t in tokens)
    rows = conn.execute(
        "SELECT track, heading, snippet(report_fts, 0, '[', ']', ' … ', 18) "
        "FROM report_fts WHERE report_fts MATCH ? LIMIT ?",
        (match, args.limit),
    ).fetchall()
    for track, heading, snippet in rows:
        print(f"\n[{track}] § {heading}\n  {snippet}")
    if not rows:
        print("no matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
