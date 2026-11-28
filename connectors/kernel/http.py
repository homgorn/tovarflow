"""HTTP transport with rate limiting, retries, raw capture and idempotency.

Nothing here knows an Ozon or WB endpoint. Adapters pass method/path/body and get back a
normalised dict; HTTP exceptions are mapped to the kernel error taxonomy.
"""

from __future__ import annotations

import hashlib
import json
import random
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from .errors import AuthError, EntitlementError, ModerationError, RateLimitError, TransientError, ValidationError

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw_responses"
IDEM_DB = ROOT / "data" / "connectors.sqlite"


class RateLimiter:
    def __init__(self, per_scope: dict[str, float] | None = None):
        self.per_scope = per_scope or {}
        self.last: dict[str, float] = {}

    def wait(self, scope: str) -> None:
        interval = self.per_scope.get(scope, 0.0)
        if not interval:
            return
        elapsed = time.time() - self.last.get(scope, 0.0)
        if elapsed < interval:
            time.sleep(interval - elapsed)
        self.last[scope] = time.time()


class HttpAdapter:
    def __init__(self, base_url: str, headers: dict[str, str], limiter: RateLimiter | None = None,
                 timeout: int = 30, retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.headers = headers
        self.limiter = limiter or RateLimiter()
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        IDEM_DB.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(IDEM_DB)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS idempotency ("
            "key TEXT PRIMARY KEY, response TEXT, created_at TEXT)"
        )
        conn.commit()
        conn.close()

    def _idem_get(self, key: str) -> dict | None:
        conn = sqlite3.connect(IDEM_DB)
        row = conn.execute("SELECT response FROM idempotency WHERE key=?", (key,)).fetchone()
        conn.close()
        return json.loads(row[0]) if row else None

    def _idem_put(self, key: str, response: dict) -> None:
        conn = sqlite3.connect(IDEM_DB)
        conn.execute(
            "INSERT OR IGNORE INTO idempotency(key,response,created_at) VALUES(?,?,?)",
            (key, json.dumps(response, ensure_ascii=False),
             datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )
        conn.commit()
        conn.close()

    def _capture(self, method: str, path: str, text: str) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
        safe = "".join(c if c.isalnum() else "-" for c in path)[:80]
        target = RAW_DIR / f"{stamp}_{method.lower()}_{safe}_{digest}.json"
        target.write_text(text, encoding="utf-8")
        return str(target.relative_to(ROOT)).replace("\\", "/")

    def request(self, method: str, path: str, *, body: dict | None = None,
                scope: str = "default", idempotency_key: str | None = None) -> dict:
        if idempotency_key:
            cached = self._idem_get(idempotency_key)
            if cached is not None:
                return cached
        headers = dict(self.headers)
        if idempotency_key:
            headers["X-Idempotency-Key"] = idempotency_key
        url = f"{self.base_url}{path}"
        last: Exception = TransientError("no attempt made")
        for attempt in range(1, self.retries + 1):
            self.limiter.wait(scope)
            try:
                resp = self.session.request(method, url, json=body, headers=headers,
                                            timeout=self.timeout)
            except requests.RequestException as exc:
                last = TransientError(type(exc).__name__)
                time.sleep(min(20, 2 ** attempt + random.random()))
                continue
            self._capture(method, path, resp.text)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else min(
                    20, 2 ** attempt + random.random())
                last = RateLimitError(f"HTTP 429 on {path}")
                time.sleep(delay)
                continue
            if 500 <= resp.status_code < 600:
                last = TransientError(f"HTTP {resp.status_code} on {path}")
                time.sleep(min(20, 2 ** attempt + random.random()))
                continue
            if resp.status_code in (401, 403):
                raise AuthError(f"HTTP {resp.status_code} on {path}")
            if resp.status_code == 404:
                from .errors import MarketplaceError
                raise MarketplaceError(f"not_found: {path}")
            if resp.status_code >= 400:
                raise ValidationError(f"HTTP {resp.status_code}: {resp.text[:200]}")
            result = resp.json() if resp.content else {}
            if idempotency_key:
                self._idem_put(idempotency_key, result)
            return result
        raise last
