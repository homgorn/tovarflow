"""Contract tests for the Ozon Seller L2 adapter against the local emulator.

Usage:
    python tools/contract_ozon.py
"""

from __future__ import annotations

import json
import sys
import threading
import uuid
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mock_ozon import Handler, PRICES, WRITES  # noqa: E402
from connectors.ru.ozon.adapter import OzonAdapter  # noqa: E402
from connectors.kernel import AuthError, ValidationError  # noqa: E402


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    adapter = OzonAdapter(base_url=base, client_id="test-client", api_key="test-key")
    results: list[dict] = []

    def check(name: str, condition: bool, detail: str) -> None:
        results.append({"check": name, "passed": bool(condition), "detail": detail})
        print(("PASS " if condition else "FAIL ") + name + " — " + detail)

    p = adapter.profile_summary()
    check("profile", p["id"] == "ru.ozon.seller" and p["capabilities"]["price_write"], json.dumps(p))

    health = adapter.health()
    check("health", "result" in health, "POST /v1/product/list returned result")

    offer = f"SKU-{uuid.uuid4().hex[:8]}"
    key = f"contract-{offer}"
    first = adapter.update_price(offer, 123456, key)
    observed = adapter.verify_price(offer)
    check("price write + read-back", observed == 123456,
          f"wrote 123456 minor, read {observed}, response={first}")

    writes_before = WRITES
    adapter.update_price(offer, 999999, key)  # same key, different price
    observed_again = adapter.verify_price(offer)
    check("idempotent replay", observed_again == 123456 and WRITES == writes_before,
          f"price stayed {observed_again}, writes {writes_before} -> {WRITES}")

    problems = adapter.validate("X", -1)
    check("local validation", bool(problems), "; ".join(problems))

    try:
        adapter.update_price("INVALID", -5, "bad-key")
        check("validation blocks HTTP", False, "no ValidationError")
    except ValidationError:
        check("validation blocks HTTP", True, "ValidationError raised before HTTP")

    bad = OzonAdapter(base_url=base, client_id="wrong", api_key="wrong")
    try:
        bad.health()
        check("auth error", False, "401 did not map to AuthError")
    except AuthError:
        check("auth error", True, "401 mapped to AuthError")

    rate_offer = "RATELIMIT-1"
    rate_key = f"rate-{uuid.uuid4().hex[:6]}"
    adapter.update_price(rate_offer, 50000, rate_key)
    rate_observed = adapter.verify_price(rate_offer)
    check("429 retry", rate_observed == 50000, f"after one 429, price read {rate_observed}")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "endpoint_evidence": "H:/susa ai 500/wb china/ozon-seller-api-openapi.json (482 paths)",
        "results": results,
        "passed": sum(1 for r in results if r["passed"]),
        "total": len(results),
        "confidence": "measured",
    }
    out = ROOT / "data" / "ozon_contract_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    server.shutdown()
    server.server_close()
    print(f"\n{report['passed']}/{report['total']} contract checks passed; report: {out.relative_to(ROOT)}")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
