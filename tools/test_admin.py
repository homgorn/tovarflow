"""Smoke test for the operator console (assumes tools/admin.py is running).

Usage:
    python tools/admin.py --port 8880   # in another shell
    python tools/test_admin.py --port 8880
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import urllib.parse
import urllib.request

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def post(base: str, path: str, data: dict) -> None:
    body = urllib.parse.urlencode(data).encode("utf-8")
    urllib.request.urlopen(urllib.request.Request(base + path, data=body, method="POST"), timeout=10).read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8880)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"

    dashboard = urllib.request.urlopen(base + "/", timeout=10).read().decode("utf-8")
    assert "операторский дашборд" in dashboard

    mapping = urllib.request.urlopen(base + "/mapping", timeout=10).read().decode("utf-8")
    keys = re.findall(r"<code>([^<]+)</code>", mapping)
    assert keys, "no attribute keys found"
    post(base, "/mapping", {"source_key": keys[0], "canonical_key": "color", "reviewer": "smoke"})

    proposals = urllib.request.urlopen(base + "/proposals", timeout=10).read().decode("utf-8")
    ids = re.findall(r"<code>(prop_[^<]+)</code>", proposals)
    assert ids, "no proposals found"
    target = ids[0]
    post(base, "/proposals", {"proposal_id": target, "action": "approve", "actor": "smoke"})
    post(base, "/proposals", {"proposal_id": target, "action": "approve", "actor": "smoke-again"})

    conn = sqlite3.connect(ROOT / "data" / "catalog.sqlite")
    events = conn.execute(
        "SELECT count(*) FROM approval_event WHERE idempotency_key=?",
        (f"approval:{target}:ALLOW",),
    ).fetchone()[0]
    status = conn.execute("SELECT status FROM proposal WHERE id=?", (target,)).fetchone()[0]
    mapping_rows = conn.execute("SELECT count(*) FROM attribute_mapping").fetchone()[0]
    conn.close()
    ok = events == 1 and status == "APPROVED" and mapping_rows >= 1
    print(f"admin-smoke: events={events}, status={status}, mapping_rows={mapping_rows}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
