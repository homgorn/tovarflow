"""Print the current state of the knowledge base and research DB.

Usage:
    python tools/status.py
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count(db: Path, table: str) -> int | str:
    if not db.exists():
        return "missing"
    conn = sqlite3.connect(db)
    try:
        return conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
    except sqlite3.Error:
        return "no table"
    finally:
        conn.close()


def main() -> int:
    q = ROOT / "data" / "qparser.sqlite"
    r = ROOT / "data" / "research.sqlite"
    print("Q-Parser corpus")
    for table in ("sources", "chunks", "endpoints", "formats", "plans", "claims", "edges"):
        print(f"  {table:10} {count(q, table)}")
    print("Research")
    for table in ("tracks", "records", "marketplaces", "assets", "adrs", "edges"):
        print(f"  {table:12} {count(r, table)}")
    wiki = list((ROOT / "wiki").rglob("*.md"))
    print(f"Wiki pages       {len(wiki)}")
    graph = ROOT / "data" / "knowledge.graph.json"
    if graph.exists():
        g = json.loads(graph.read_text(encoding="utf-8"))
        print(f"Knowledge graph  {len(g['nodes'])} nodes / {len(g['edges'])} edges")
    reports = sorted((ROOT / "docs" / "research").rglob("REPORT.md"))
    print("Research reports")
    for report in reports:
        print(f"  {report.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
