"""Execute approved price proposals and verify the result by reading state back.

This is a local emulator of the write path: Proposal -> Policy -> Execution -> Verification.
An approved proposal is applied once (idempotency key), then the emulated channel price is
re-read and compared with the intended price. A mismatch opens an incident record.

Usage:
    python tools/executor.py
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "catalog.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS execution (
  id TEXT PRIMARY KEY, proposal_id TEXT, idempotency_key TEXT UNIQUE,
  request_hash TEXT, status TEXT, intended_price_minor INTEGER,
  created_at TEXT, finished_at TEXT
);
CREATE TABLE IF NOT EXISTS verification (
  id INTEGER PRIMARY KEY AUTOINCREMENT, execution_id TEXT, result TEXT,
  observed_price_minor INTEGER, expected_price_minor INTEGER, checked_at TEXT
);
CREATE TABLE IF NOT EXISTS channel_price (
  offer_id TEXT PRIMARY KEY, price_minor INTEGER, currency TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS incident (
  id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, subject TEXT, details TEXT, created_at TEXT
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    rows = conn.execute(
        "SELECT p.id,p.ref_id,d.price_minor,d.currency "
        "FROM proposal p JOIN price_decision d ON d.offer_id=p.ref_id "
        "WHERE p.status='APPROVED'"
    ).fetchall()
    applied = verified = mismatches = skipped = 0
    stamp = now()

    for proposal_id, offer_id, price, currency in rows:
        idem = f"exec:{proposal_id}"
        request_hash = hashlib.sha256(
            json.dumps({"offer_id": offer_id, "price_minor": price, "currency": currency},
                       sort_keys=True).encode("utf-8")
        ).hexdigest()[:32]
        cur = conn.execute(
            "INSERT OR IGNORE INTO execution(id,proposal_id,idempotency_key,request_hash,"
            "status,intended_price_minor,created_at,finished_at) VALUES(?,?,?,?,?,?,?,?)",
            (f"ex_{proposal_id}", proposal_id, idem, request_hash, "DONE", price, stamp, stamp),
        )
        if not cur.rowcount:
            skipped += 1  # replay with the same idempotency key: no second write
            continue

        conn.execute(
            "INSERT INTO channel_price(offer_id,price_minor,currency,updated_at) VALUES(?,?,?,?) "
            "ON CONFLICT(offer_id) DO UPDATE SET price_minor=excluded.price_minor,"
            "currency=excluded.currency,updated_at=excluded.updated_at",
            (offer_id, price, currency, stamp),
        )
        applied += 1
        observed = conn.execute(
            "SELECT price_minor FROM channel_price WHERE offer_id=?", (offer_id,)
        ).fetchone()[0]
        result = "OK" if observed == price else "MISMATCH"
        conn.execute(
            "INSERT INTO verification(execution_id,result,observed_price_minor,"
            "expected_price_minor,checked_at) VALUES(?,?,?,?,?)",
            (f"ex_{proposal_id}", result, observed, price, stamp),
        )
        if result == "OK":
            verified += 1
        else:
            mismatches += 1
            conn.execute(
                "INSERT INTO incident(kind,subject,details,created_at) VALUES(?,?,?,?)",
                ("price_mismatch", offer_id,
                 json.dumps({"expected": price, "observed": observed}), stamp),
            )
    conn.commit()

    counts = {t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
              for t in ("proposal", "execution", "verification", "channel_price", "incident")}
    conn.close()
    print(json.dumps({
        "approved": len(rows), "applied": applied, "verified": verified,
        "mismatches": mismatches, "idempotent_skips": skipped, "counts": counts,
    }, ensure_ascii=False, indent=2))
    return 0 if mismatches == 0 and applied + skipped == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
