"""Typed Q-Parser API client.

The key is read from .env / environment by tools/config.py; it is sent only in the Authorization
header and is never logged. This client implements the 16 documented endpoints; the first slice
uses 9 of them.

Usage:
    python tools/qparser_client.py --domain demo-home.ru --mock
    python tools/qparser_client.py --domain my-supplier.ru   # needs QPARSER_API_KEY in .env
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import qparser_config, redact  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_responses"


class QParserError(Exception):
    code = "unknown"


class AuthError(QParserError):
    code = "unauthorized"


class ValidationError(QParserError):
    code = "bad_request"


class RateLimitError(QParserError):
    code = "rate_limited"


class TransientError(QParserError):
    code = "internal"


class UnprocessableError(QParserError):
    code = "unprocessable"


ERROR_MAP = {
    "unauthorized": AuthError,
    "bad_request": ValidationError,
    "forbidden": AuthError,
    "not_found": QParserError,
    "unprocessable": UnprocessableError,
    "internal": TransientError,
}


class QParserClient:
    def __init__(self, capture_raw: bool = True, timeout: int = 45, retries: int = 4):
        cfg = qparser_config()
        self.base_url = cfg["base_url"].rstrip("/")
        self.api_key = cfg["api_key"]
        self.use_mock = cfg["use_mock"]
        self.capture_raw = capture_raw
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "qparser-catalog-client/0.1",
        })
        if capture_raw:
            RAW_DIR.mkdir(parents=True, exist_ok=True)

    def _store_raw(self, method: str, path: str, payload: str) -> str | None:
        if not self.capture_raw:
            return None
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        safe = re.sub(r"[^A-Za-z0-9_-]+", "-", path).strip("-")[:120] or "root"
        name = f"{stamp}_{method.lower()}_{safe}_{digest}.json"
        target = RAW_DIR / name
        target.write_text(payload, encoding="utf-8")
        return str(target.relative_to(ROOT)).replace("\\", "/")

    def request(self, method: str, path: str, *, params: dict | None = None,
                body: dict | None = None) -> Any:
        url = f"{self.base_url}{path}"
        last: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.request(
                    method, url, params=params,
                    json=body if body is not None else None,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                last = TransientError(f"network failure: {type(exc).__name__}")
                time.sleep(min(30, 2 ** attempt + random.random()))
                continue

            self._store_raw(method, path + (("?" + requests.compat.urlencode(params)) if params else ""),
                            response.text)

            if response.status_code == 429 or 500 <= response.status_code < 600:
                retry_after = response.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else min(
                    30, 2 ** attempt + random.random())
                last = RateLimitError(f"HTTP {response.status_code} on {path}")
                time.sleep(delay)
                continue

            if response.status_code >= 400:
                try:
                    err = response.json().get("error", {})
                    code, message = err.get("code", "unknown"), err.get("message", response.text[:200])
                except ValueError:
                    code, message = "unknown", response.text[:200]
                raise ERROR_MAP.get(code, QParserError)(f"{code}: {message}")

            return response.json() if response.content else {}

        raise last or TransientError(f"exhausted retries on {path}")

    # ---------------- API methods ----------------
    def me(self) -> dict:
        return self.request("GET", "/me")

    def catalog(self, q: str | None = None, free: bool | None = None,
                limit: int = 100, offset: int = 0) -> dict:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            params["q"] = q
        if free:
            params["free"] = 1
        return self.request("GET", "/catalog", params=params)

    def website(self, domain: str) -> dict:
        return self.request("GET", f"/website/{domain}")

    def credentials(self, domain: str | None = None) -> dict:
        return self.request("GET", "/credentials", params={"domain": domain} if domain else None)

    def add_credentials(self, domain: str, login: str, password: str) -> dict:
        return self.request("POST", "/credentials", body={"domain": domain, "login": login,
                                                           "password": password})

    def start_categories(self, domain: str, credentials_id: str | None = None,
                         options: dict | None = None) -> dict:
        body: dict[str, Any] = {"domain": domain}
        if credentials_id:
            body["credentials_id"] = credentials_id
        if options:
            body["options"] = options
        return self.request("POST", "/categories", body=body)

    def categories(self, job_id: str) -> dict:
        return self.request("GET", f"/categories/{job_id}")

    def start_parser(self, domain: str, categories: list[dict] | None = None,
                     credentials_id: str | None = None, options: dict | None = None,
                     trial: bool = False) -> str:
        body: dict[str, Any] = {"domain": domain}
        if categories:
            body["categories"] = categories
        if credentials_id:
            body["credentials_id"] = credentials_id
        if options:
            body["options"] = options
        if trial:
            body["trial"] = True
        return self.request("POST", "/parser", body=body)["id"]

    def parser(self, parse_id: str) -> dict:
        return self.request("GET", f"/parser/{parse_id}")

    def parser_list(self, limit: int = 100, offset: int = 0) -> dict:
        return self.request("GET", "/parser/list", params={"limit": limit, "offset": offset})

    def stop(self, parse_id: str) -> dict:
        return self.request("POST", f"/parser/{parse_id}/stop")

    def resume(self, parse_id: str) -> dict:
        return self.request("POST", f"/parser/{parse_id}/resume")

    def goods(self, parse_id: str, limit: int = 1000, offset: int = 0) -> dict:
        return self.request("GET", f"/parser/{parse_id}/goods",
                            params={"limit": min(limit, 1000), "offset": offset})

    def iter_goods(self, parse_id: str, page_size: int = 1000) -> Iterator[dict]:
        offset = 0
        total = None
        while True:
            page = self.goods(parse_id, limit=page_size, offset=offset)
            if total is None:
                total = int(page.get("total", 0))
            batch = page.get("goods", [])
            yield from batch
            offset += len(batch)
            if offset >= total or not batch:
                break

    def formats(self) -> dict:
        return self.request("GET", "/format")

    def start_export(self, parser_id: str, fmt: str, options: dict | None = None) -> str:
        body = {"parser_id": parser_id, "format": fmt}
        if options:
            body["options"] = options
        return self.request("POST", "/export", body=body)["id"]

    def export(self, export_id: str) -> dict:
        return self.request("GET", f"/export/{export_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="demo-home.ru")
    parser.add_argument("--mock", action="store_true", help="force USE_MOCK=1")
    parser.add_argument("--trial", action="store_true")
    args = parser.parse_args()
    if args.mock:
        import os
        os.environ["USE_MOCK"] = "1"
    client = QParserClient()
    print(f"mode={'mock' if client.use_mock else 'live'} base={client.base_url} "
          f"key={redact(client.api_key)}")
    me = client.me()
    print("me:", me.get("email"), "tariff:", me.get("tariff_id"))
    print("catalog total:", client.catalog(q=args.domain)["total"])
    print("site:", client.website(args.domain))
    parse_id = client.start_parser(args.domain, trial=args.trial)
    print("parse:", parse_id)
    for _ in range(60):
        status = client.parser(parse_id)
        if status["status"] in ("completed", "error", "canceled"):
            break
        time.sleep(0.25)
    print("status:", status["status"], "goods:", status["goods_processed"])
    goods = list(client.iter_goods(parse_id, page_size=10))
    print("goods fetched:", len(goods), "first:", goods[0]["article"] if goods else None)
    return 0 if status["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
