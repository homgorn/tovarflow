"""Margin ledger v1: explain every price instead of guessing a markup.

Reads canonical offers from data/catalog.sqlite, applies versioned margin rules from .env,
and writes price_decision rows with a full explanation. Unknown components are NULL and
make is_complete=false; an incomplete price cannot be published.

Usage:
    python tools/margin.py
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import get  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "catalog.sqlite"
VERSION = "margin.v1"
TABLE = """
CREATE TABLE IF NOT EXISTS price_decision (
  id TEXT PRIMARY KEY, product_id TEXT, offer_id TEXT, currency TEXT,
  purchase_minor INTEGER, delivery_minor INTEGER, duty_minor INTEGER,
  commission_rate REAL, return_rate REAL, acquiring_rate REAL, tax_rate REAL,
  target_margin REAL, floor_minor INTEGER, price_minor INTEGER,
  is_complete INTEGER, can_publish INTEGER, explanation TEXT,
  version TEXT, created_at TEXT
);
"""


def minor_from_env(name: str) -> int | None:
    """Values with a _MINOR suffix are already in minor units (kopecks), not major units."""
    raw = get(name)
    if raw is None or raw == "":
        return None
    try:
        return int(round(float(raw)))
    except ValueError:
        return None


def rate_from_env(name: str) -> float | None:
    raw = get(name)
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def compute(purchase: int | None, delivery: int | None, duty: int | None,
            commission: float | None, returns: float | None, acquiring: float | None,
            tax: float | None, margin: float | None, floor: int | None) -> dict:
    missing = [name for name, value in (
        ("purchase", purchase), ("delivery", delivery), ("duty", duty),
        ("commission", commission), ("returns", returns), ("acquiring", acquiring),
        ("tax", tax), ("margin", margin), ("floor", floor),
    ) if value is None]
    if missing:
        return {"price_minor": None, "is_complete": False, "can_publish": False,
                "missing": missing}
    denominator = 1.0 - commission - returns - acquiring - tax - margin
    if denominator <= 0.05:
        return {"price_minor": None, "is_complete": False, "can_publish": False,
                "missing": ["invalid_denominator"]}
    landed = purchase + delivery + duty
    price = int(round(landed / denominator))
    floor_price = max(price, floor)
    return {"price_minor": floor_price, "is_complete": True,
            "can_publish": floor_price >= floor, "missing": [], "landed_minor": landed,
            "denominator": round(denominator, 4)}


def main() -> int:
    conn = sqlite3.connect(DB)
    conn.executescript(TABLE)
    delivery = minor_from_env("MARGIN_DELIVERY_MINOR")
    duty = minor_from_env("MARGIN_DUTY_MINOR")
    commission = rate_from_env("MARGIN_COMMISSION")
    returns = rate_from_env("MARGIN_RETURNS")
    acquiring = rate_from_env("MARGIN_ACQUIRING")
    tax = rate_from_env("MARGIN_TAX")
    margin = rate_from_env("MARGIN_TARGET")
    floor = minor_from_env("MARGIN_FLOOR_MINOR")

    offers = conn.execute(
        "SELECT o.id,o.variant_id,o.price_minor,o.currency,v.product_id "
        "FROM offer o JOIN variant v ON v.id=o.variant_id"
    ).fetchall()
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    complete = 0
    for offer_id, variant_id, purchase, currency, product_id in offers:
        result = compute(purchase, delivery, duty, commission, returns, acquiring, tax, margin, floor)
        explanation = {
            "formula": "price = (purchase + delivery + duty) / (1 - commission - returns - acquiring - tax - margin)",
            "purchase_minor": purchase, "delivery_minor": delivery, "duty_minor": duty,
            "commission": commission, "returns": returns, "acquiring": acquiring,
            "tax": tax, "target_margin": margin, "floor_minor": floor,
            "missing": result["missing"], "version": VERSION,
        }
        conn.execute(
            "INSERT INTO price_decision(id,product_id,offer_id,currency,purchase_minor,"
            "delivery_minor,duty_minor,commission_rate,return_rate,acquiring_rate,tax_rate,"
            "target_margin,floor_minor,price_minor,is_complete,can_publish,explanation,version,created_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(id) DO UPDATE SET price_minor=excluded.price_minor,"
            "is_complete=excluded.is_complete,can_publish=excluded.can_publish,"
            "explanation=excluded.explanation",
            (f"pd_{offer_id}", product_id, offer_id, currency, purchase, delivery, duty,
             commission, returns, acquiring, tax, margin, floor, result["price_minor"],
             int(result["is_complete"]), int(result["can_publish"]),
             json.dumps(explanation, ensure_ascii=False, sort_keys=True), VERSION, created),
        )
        complete += int(result["is_complete"])
    conn.commit()
    total = conn.execute("SELECT count(*) FROM price_decision").fetchone()[0]
    sample = conn.execute(
        "SELECT explanation FROM price_decision WHERE is_complete=1 LIMIT 1"
    ).fetchone()
    conn.close()
    print(json.dumps({
        "decisions": total, "complete": complete, "version": VERSION,
        "sample_explanation": json.loads(sample[0]) if sample else None,
    }, ensure_ascii=False, indent=2))
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
