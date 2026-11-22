"""Smoke test for tools/mock_qparser.py.

Usage:
    python tools/smoke_mock.py
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from mock_qparser import Handler

BASE = "http://127.0.0.1:8877/api/v1"
HEADERS = {"Authorization": "Bearer test", "Content-Type": "application/json"}


def call(method: str, path: str, body: dict | None = None, auth: bool = True):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers=HEADERS if auth else {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", 8877), Handler)
    server.no_auth = False
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    checks = []

    def ok(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, condition, detail))
        print(("PASS " if condition else "FAIL ") + name + (" — " + detail if detail else ""))

    try:
        status, me = call("GET", "/me")
        ok("auth + /me", status == 200 and me["email"] == "demo@example.com")

        try:
            call("GET", "/me", auth=False)
            ok("missing auth rejected", False)
        except urllib.error.HTTPError as exc:
            ok("missing auth rejected", exc.code == 401)

        _, catalog = call("GET", "/catalog?q=demo")
        ok("catalog", catalog["total"] == 3, f"total={catalog['total']}")

        _, site = call("GET", "/website/demo-home.ru")
        ok("website options", site["domain"] == "demo-home.ru")

        _, cats = call("POST", "/categories", {"domain": "demo-home.ru"})
        ok("categories start", cats["status"] == "completed")
        _, cat = call("GET", f"/categories/{cats['id']}")
        ok("categories result", len(cat["categories"]) == 3)

        _, started = call("POST", "/parser", {"domain": "demo-home.ru"})
        parse_id = started["id"]
        deadline = time.time() + 20
        job = {}
        while time.time() < deadline:
            _, job = call("GET", f"/parser/{parse_id}")
            if job["status"] == "completed":
                break
            time.sleep(0.2)
        ok("parse completed", job.get("status") == "completed", f"status={job.get('status')}")
        ok("progress", job.get("goods_processed") == 100, f"processed={job.get('goods_processed')}")

        _, goods = call("GET", f"/parser/{parse_id}/goods?limit=10&offset=0")
        ok("goods page", goods["total"] == 100 and len(goods["goods"]) == 10)
        ok("goods fields", "data" in goods["goods"][0] and "price" in goods["goods"][0])

        _, formats = call("GET", "/format")
        ok("formats", any(f["id"] == "yml" for f in formats["formats"]))

        _, export = call("POST", "/export", {"parser_id": parse_id, "format": "yml"})
        _, export_job = call("GET", f"/export/{export['id']}")
        ok("export completed", export_job["status"] == "completed" and export_job["files"])

        _, trial = call("POST", "/parser", {"domain": "demo-home.ru", "trial": True})
        time.sleep(0.5)
        _, trial_job = call("GET", f"/parser/{trial['id']}")
        _, trial_goods = call("GET", f"/parser/{trial['id']}/goods?limit=10")
        ok("trial cap", trial_job["goods_limited"] == 50 and trial_goods["total"] == 50,
           f"limited={trial_job['goods_limited']} total={trial_goods['total']}")

        _, long_job = call("POST", "/parser", {"domain": "demo-home.ru"})
        time.sleep(0.3)
        _, stopped = call("POST", f"/parser/{long_job['id']}/stop")
        ok("stop", stopped["status"] == "canceled")
        _, resumed = call("POST", f"/parser/{long_job['id']}/resume")
        ok("resume", resumed["status"] in ("running", "completed"))
    finally:
        server.shutdown()
        server.server_close()

    failed = [c for c in checks if not c[1]]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
