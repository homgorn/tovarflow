"""Verify that a stored raw payload replays to the same canonical hash.

Usage:
    python tools/replay.py --domain demo-home.ru
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="demo-home.ru")
    args = parser.parse_args()

    report_path = ROOT / "data" / "ingest" / f"{args.domain.replace('.', '-')}.report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    conn = sqlite3.connect(ROOT / "data" / "catalog.sqlite")
    rows = conn.execute(
        "SELECT payload FROM raw_good WHERE ingest_run_id=? ORDER BY position", (report["run_id"],)
    ).fetchall()
    conn.close()

    hashes = []
    for (payload,) in rows:
        good = json.loads(payload)
        canonical = {
            "title": good.get("title") or "",
            "description": good.get("description") or "",
            "data": good.get("data") or {},
        }
        hashes.append(hashlib.sha256(json.dumps(canonical, ensure_ascii=False, sort_keys=True)
                                     .encode("utf-8")).hexdigest())
    replay_hash = hashlib.sha256("".join(hashes).encode("utf-8")).hexdigest()
    ok = replay_hash == report["canonical_hash"] and len(rows) == report["goods_written"]
    print(f"raw goods: {len(rows)} / {report['goods_written']}")
    print(f"stored hash: {report['canonical_hash']}")
    print(f"replay  hash: {replay_hash}")
    print("REPLAY PASS" if ok else "REPLAY FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
