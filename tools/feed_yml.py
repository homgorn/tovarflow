"""Generate and validate a Yandex Market YML feed from the canonical catalogue.

Usage:
    python tools/feed_yml.py
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "catalog.sqlite"
OUT = ROOT / "data" / "feeds"


def cat_id(title: str) -> str:
    return hashlib.sha1(title.encode("utf-8")).hexdigest()[:10]


def money(minor: int | None) -> str:
    return f"{minor / 100:.2f}" if minor is not None else "0.00"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT p.domain,p.url,p.title,p.description,p.brand,p.short_description,p.category_title,"
        "p.attributes_raw,o.quantity,o.publish,pd.price_minor,pd.is_complete,pd.can_publish,"
        "(SELECT m.url FROM media m WHERE m.product_id=p.id ORDER BY m.position LIMIT 1) AS picture "
        "FROM product p JOIN variant v ON v.product_id=p.id "
        "JOIN offer o ON o.variant_id=v.id "
        "JOIN price_decision pd ON pd.offer_id=o.id"
    ).fetchall()
    vendor_map = {}
    catalog_file = ROOT / "data" / "catalog_sites.json"
    if catalog_file.exists():
        try:
            catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
            vendor_map = {s.get("domain"): s.get("title") for s in catalog.get("sites", [])}
        except (ValueError, TypeError):
            vendor_map = {}
    categories = sorted({r[6] or "Разное" for r in rows})
    errors = []
    offers = []
    fallback_vendors = 0
    for r in rows:
        domain, url, title, description, brand, short, category, attrs_raw, quantity, publish, price, complete, can_publish, picture = r
        vendor = brand or vendor_map.get(domain) or "TovarFlow"
        if not brand:
            fallback_vendors += 1
        article = url.rsplit("/", 1)[-1] if url else ""
        attrs = json.loads(attrs_raw or "{}")
        problems = []
        if not title:
            problems.append("missing name")
        if not url:
            problems.append("missing url")
        if not complete:
            problems.append("incomplete price")
        if not can_publish:
            problems.append("below floor")
        if price is None or price <= 0:
            problems.append("missing price")
        if not picture:
            problems.append("missing picture")
        if problems:
            errors.append({"article": article, "problems": problems})
            continue
        params = "".join(
            f'<param name="{escape(str(k))}">{escape(str(v))}</param>' for k, v in attrs.items()
        )
        offers.append(f"""<offer id="{escape(article)}" available="{'true' if publish is True and (quantity or 0) > 0 else 'false'}">
  <name>{escape(title)}</name>
  <url>{escape(url)}</url>
  <price>{money(price)}</price>
  <currencyId>RUB</currencyId>
  <categoryId>{cat_id(category)}</categoryId>
  <picture>{escape(picture or '')}</picture>
  <vendor>{escape(vendor)}</vendor>
  <model>{escape(article)}</model>
  <vendorCode>{escape(article)}</vendorCode>
  <description>{escape(description or short or title)}</description>
  {params}
</offer>""")

    cats_xml = "".join(f'<category id="{cat_id(c)}">{escape(c)}</category>' for c in categories)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    yml = f"""<?xml version="1.0" encoding="UTF-8"?>
<yml_catalog date="{date}">
  <shop>
    <name>TovarFlow</name>
    <company>TovarFlow</company>
    <url>https://tovarflow.ru</url>
    <currencies><currency id="RUB" rate="1"/></currencies>
    <categories>{cats_xml}</categories>
    <offers>{''.join(offers)}</offers>
  </shop>
</yml_catalog>
"""
    feed_path = OUT / "yandex.yml"
    feed_path.write_text(yml, encoding="utf-8")

    parse_errors = []
    try:
        root = ET.fromstring(yml)
        actual = len(root.findall("./shop/offers/offer"))
        if actual != len(offers):
            parse_errors.append(f"parsed {actual} offers, expected {len(offers)}")
    except ET.ParseError as exc:
        parse_errors.append(str(exc))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "offers": len(offers), "categories": len(categories),
        "fallback_vendors": fallback_vendors,
        "validation_errors": errors, "parse_errors": parse_errors,
        "feed": str(feed_path.relative_to(ROOT)).replace("\\", "/"),
        "valid": not errors and not parse_errors,
    }
    report_path = OUT / "yandex.report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    conn.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
