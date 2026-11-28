"""Local emulator of the Ozon Seller endpoints used by the L2 adapter.

This is a test fixture, not a marketplace. It implements the same method names as the official
OpenAPI schema: import/prices, info/prices, stocks, product/list.

Usage:
    python tools/mock_ozon.py --port 8890
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PRICES: dict[str, str] = {}
STOCKS: dict[str, int] = {}
IDEMPOTENCY: dict[str, dict] = {}
WRITES = 0
RATELIMIT_HITS: dict[str, int] = {}


class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        return (self.headers.get("Client-Id") == "test-client"
                and self.headers.get("Api-Key") == "test-key")

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def do_POST(self) -> None:  # noqa: N802
        global WRITES
        if not self._authorized():
            return self._json(401, {"error": {"code": "unauthorized", "message": "missing headers"}})
        path = self.path.rstrip("/")
        body = self._body()

        if path == "/v1/product/list":
            return self._json(200, {"result": {"items": list(PRICES.keys())}})

        if path == "/v1/product/import/prices":
            idem = self.headers.get("X-Idempotency-Key", "")
            if idem and idem in IDEMPOTENCY:
                return self._json(200, IDEMPOTENCY[idem])
            first = (body.get("prices") or [{}])[0]
            offer_id = first.get("offer_id", "")
            if offer_id == "RATELIMIT-1":
                hits = RATELIMIT_HITS.get(offer_id, 0) + 1
                RATELIMIT_HITS[offer_id] = hits
                if hits == 1:
                    self.send_response(429)
                    self.send_header("Retry-After", "0")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            PRICES[offer_id] = str(first.get("price", "0"))
            WRITES += 1
            result = {"result": {"updated": 1, "offer_id": offer_id}}
            if idem:
                IDEMPOTENCY[idem] = result
            return self._json(200, result)

        if path == "/v5/product/info/prices":
            ids = ((body.get("filter") or {}).get("offer_id") or [])
            prices = [{"offer_id": o, "price": PRICES.get(o, "0")} for o in ids]
            return self._json(200, {"result": {"prices": prices}})

        if path == "/v2/products/stocks":
            for item in body.get("stocks") or []:
                STOCKS[str(item.get("offer_id"))] = int(item.get("amount", 0))
            return self._json(200, {"result": {"updated": len(body.get("stocks") or [])}})

        return self._json(404, {"error": {"code": "not_found", "message": path}})

    def log_message(self, fmt, *args) -> None:
        pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8890)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Mock Ozon Seller on http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
