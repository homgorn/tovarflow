"""Dump the full Q-Parser site catalogue through GET /api/v1/catalog.

The API documentation does not contain a static domain list; this endpoint returns it. Requires
QPARSER_API_KEY in .env, or --mock for the local emulator.

Usage:
    python tools/catalog_dump.py --mock
    python tools/catalog_dump.py            # live, needs the key
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"


def start_mock() -> tuple[ThreadingHTTPServer, str]:
    from mock_qparser import Handler
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.no_auth = True
    server.verbose = False
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/api/v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--q", default=None, help="search by name, description or domain")
    parser.add_argument("--free-only", action="store_true")
    args = parser.parse_args()

    server = None
    if args.mock:
        os.environ["USE_MOCK"] = "1"
        server, url = start_mock()
        os.environ["QPARSER_MOCK_URL"] = url

    from qparser_client import QParserClient
    client = QParserClient()
    rows, offset, total = [], 0, None
    while True:
        page = client.catalog(q=args.q, free=True if args.free_only else None,
                              limit=1000, offset=offset)
        total = int(page.get("total", 0))
        batch = page.get("list", [])
        rows.extend(batch)
        offset += len(batch)
        if offset >= total or not batch:
            break

    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {"generated_at": stamp, "total": total, "sites": rows}
    (OUT / "catalog_sites.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    with (OUT / "catalog_sites.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["domain", "title", "slug", "private", "free_until",
                         "categories", "cities"])
        for s in rows:
            writer.writerow([
                s.get("domain"), s.get("title"), s.get("slug"), s.get("private"),
                s.get("free_until"),
                "|".join(c.get("title", "") for c in s.get("categories") or []),
                "|".join(c.get("title", "") for c in s.get("cities") or []),
            ])
    if server:
        server.shutdown()
        server.server_close()
    print(f"{len(rows)}/{total} sites written to data/catalog_sites.json and .csv")
    for s in rows[:5]:
        print(" -", s.get("domain"), "|", s.get("title"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
