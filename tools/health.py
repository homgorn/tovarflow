"""Fast automated health check for the whole foundation.

Usage:
    python tools/health.py            # quick gates
    python tools/health.py --full     # also run the API smoke test and canonical replay
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHECKS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (" — " + detail if detail else ""))


def check_db(path: Path, table: str) -> None:
    if not path.exists():
        record(f"db:{path.name}", False, "missing")
        return
    conn = sqlite3.connect(path)
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        count = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        record(f"db:{path.name}", integrity == "ok" and count > 0,
               f"{table}={count}, integrity={integrity}")
    except sqlite3.Error as exc:
        record(f"db:{path.name}", False, str(exc))
    finally:
        conn.close()


def check_fts() -> None:
    conn = sqlite3.connect(DATA / "qparser.sqlite")
    try:
        rows = conn.execute(
            "SELECT count(*) FROM chunks_fts WHERE chunks_fts MATCH '\"webhook\"'"
        ).fetchone()[0]
        record("fts:webhook", rows > 0, f"{rows} chunks")
    except sqlite3.Error as exc:
        record("fts:webhook", False, str(exc))
    finally:
        conn.close()


def check_graph() -> None:
    path = DATA / "knowledge.graph.json"
    if not path.exists():
        record("graph", False, "missing")
        return
    graph = json.loads(path.read_text(encoding="utf-8"))
    record("graph", len(graph["nodes"]) > 100 and len(graph["edges"]) > 100,
           f"{len(graph['nodes'])} nodes / {len(graph['edges'])} edges")


def check_coverage() -> None:
    path = ROOT / "docs" / "research" / "qparser" / "COVERAGE.md"
    if not path.exists():
        record("corpus coverage", False, "missing report")
        return
    text = path.read_text(encoding="utf-8")
    ok = "| Missing | 0 |" in text and "| Present and HTTP 200 | 128 |" in text
    record("corpus coverage", ok, "128/128 expected" if ok else "stale report")


def run_script(name: str, script: str, *args: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / "tools" / script), *args],
                            cwd=ROOT, capture_output=True, text=True, timeout=180)
    tail = (result.stdout or result.stderr).strip().splitlines()[-1:] or [""]
    record(name, result.returncode == 0, tail[0][:160])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    check_coverage()
    check_db(DATA / "qparser.sqlite", "sources")
    check_db(DATA / "research.sqlite", "records")
    check_db(DATA / "catalog.sqlite", "product")
    check_fts()
    check_graph()
    run_script("aeo-lint", "aeo_lint.py")
    if args.full:
        run_script("mock-smoke", "smoke_mock.py")
        if (DATA / "ingest" / "demo-home-ru.report.json").exists():
            run_script("canonical-replay", "replay.py", "--domain", "demo-home.ru")
        run_script("ozon-contract", "contract_ozon.py")

    failed = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"\nhealth: {len(CHECKS) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
