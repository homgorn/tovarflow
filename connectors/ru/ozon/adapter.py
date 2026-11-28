"""Ozon Seller adapter — L2 slice: price write with idempotency and read-back verification.

Endpoint names are taken from the official Ozon OpenAPI schema stored locally under
`H:/susa ai 500/wb china/` and from docs/research/marketplaces/ru/data.json (measured 2026-11-27).
No write happens outside the kernel's idempotency cache.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "connectors"))

from config import get  # noqa: E402
from connectors.kernel import EntitlementError, HttpAdapter, RateLimiter, ValidationError, load  # noqa: E402

PROFILE_PATH = Path(__file__).with_name("profile.json")


def money_to_minor(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(round(float(value) * 100))
    text = str(value).replace(" ", "").replace(",", ".")
    try:
        return int(round(float(text) * 100))
    except ValueError:
        return None


class OzonAdapter:
    def __init__(self, base_url: str | None = None, client_id: str | None = None,
                 api_key: str | None = None):
        self.profile = load(PROFILE_PATH)
        self.base_url = base_url or get("OZON_API_URL") or self.profile.api["base_url"]
        self.client_id = client_id or get("OZON_CLIENT_ID") or "test-client"
        self.api_key = api_key or get("OZON_API_KEY") or "test-key"
        self.http = HttpAdapter(
            base_url=self.base_url,
            headers={"Client-Id": self.client_id, "Api-Key": self.api_key,
                     "Content-Type": "application/json"},
            limiter=RateLimiter({"price_write": 0.2, "price_read": 0.2, "default": 0.1}),
        )

    def profile_summary(self) -> dict:
        return {"id": self.profile.id, "layer": self.profile.layer,
                "role": self.profile.role, "capabilities": self.profile.capabilities,
                "maturity": self.profile.maturity}

    def health(self) -> dict:
        if not self.profile.supports("order_read"):
            raise EntitlementError("products listing is not enabled for this profile")
        return self.http.request("POST", self.profile.endpoints["products"],
                                 body={"limit": 1, "offset": 0}, scope="default")

    def validate(self, offer_id: str, price_minor: int, currency: str = "RUB") -> list[str]:
        problems = []
        if not offer_id:
            problems.append("missing offer_id")
        if price_minor is None or price_minor <= 0:
            problems.append("price must be positive")
        if currency != self.profile.content["currency"]:
            problems.append(f"currency {currency} != {self.profile.content['currency']}")
        return problems

    def update_price(self, offer_id: str, price_minor: int, idempotency_key: str,
                     currency: str = "RUB", ctx: dict | None = None) -> dict:
        problems = self.validate(offer_id, price_minor, currency)
        if problems:
            raise ValidationError("; ".join(problems))
        if not self.profile.supports("price_write"):
            raise EntitlementError("price_write is not enabled for this profile")
        body = {"prices": [{"offer_id": offer_id,
                            "price": f"{price_minor / 100:.2f}",
                            "currency_code": currency}]}
        return self.http.request(
            "POST", self.profile.endpoints["price_write"], body=body,
            scope="price_write", idempotency_key=idempotency_key,
        )

    def verify_price(self, offer_id: str) -> int | None:
        body = {"filter": {"offer_id": [offer_id], "visibility": "ALL"}}
        result = self.http.request("POST", self.profile.endpoints["price_read"],
                                   body=body, scope="price_read")
        prices = (result.get("result") or {}).get("prices") or []
        if not prices:
            return None
        return money_to_minor(prices[0].get("price"))

    def update_stock(self, offer_id: str, stock: int, warehouse_id: int,
                     idempotency_key: str) -> dict:
        body = {"stocks": [{"offer_id": offer_id, "warehouse_id": warehouse_id,
                            "amount": stock}]}
        return self.http.request("POST", self.profile.endpoints["stock_write"], body=body,
                                 scope="default", idempotency_key=idempotency_key)
