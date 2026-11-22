"""Turn the fetched Q-Parser corpus into structured JSON.

Outputs (docs/research/qparser/extracted/):
    pages.json      - one record per page: title, section, kind, links, headings
    endpoints.json  - REST API contract derived from /howto/api
    formats.json    - export formats, their category and documented settings
    plans.json      - tariff plans and limits from /tariffs
    claims.json     - atomic, sourced claims used by the wiki and specs
    stats.json      - corpus coverage counters
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "research" / "qparser" / "pages"
OUT = ROOT / "docs" / "research" / "qparser" / "extracted"

FORMAT_CATEGORY = {
    "csvformat": "file", "xlsformat": "file", "jsonformat": "file",
    "xmlformat": "file", "ymlformat": "file",
    "facebookcsvformat": "social", "facebookxmlfeedformat": "social",
    "googlemerchantformat": "social", "showcaseformat": "social",
    "vkalbumsformat": "social", "vkformat": "social",
    "okalbumsformat": "social", "okformat": "social",
    "stospformat": "sp", "ok24format": "sp", "pokupki63format": "sp",
    "mikaiformat": "sp", "serpokformat": "sp", "superpuperformat": "sp",
    "tom70format": "sp", "amadyformat": "sp", "zaprosto24format": "sp",
    "kupivspformat": "sp", "materinstvoshopformat": "sp",
    "pokupkiprostoformat": "sp", "samarskieroditeliformat": "sp",
    "spkostromaformat": "sp", "spprotonformat": "sp", "supermamkiformat": "sp",
    "megamarketymlformat": "marketplace", "kaspixmlformat": "marketplace",
    "promuaymlformat": "marketplace", "rozetkaymlformat": "marketplace",
    "epicentrkymlformat": "marketplace",
    "commercemlformat": "commerce", "moyskladformat": "commerce",
    "advantshopv1format": "cms", "advantshopv2format": "cms",
    "alltradesformat": "cms", "botobotformat": "cms", "cmss3format": "cms",
    "cscartformat": "cms", "diskauntscsvformat": "cms", "eshoperformat": "cms",
    "hostcmsformat": "cms", "insalescsvformat": "cms", "insalesxlsformat": "cms",
    "joomlaformat": "cms", "joomshoppingformat": "cms", "lpmotorformat": "cms",
    "mogutaformat": "cms", "okaycmsformat": "cms",
    "opencartcsvliteformat": "cms", "opencartcsvpriceproformat": "cms",
    "opencartexportimportformat": "cms", "openmallformat": "cms",
    "osclassadimporterformat": "cms", "phpshopformat": "cms",
    "prestashopformat": "cms", "prestashopmagiconestoremanagerformat": "cms",
    "readyscriptformat": "cms", "shopifyformat": "cms", "simplacmsformat": "cms",
    "storelandformat": "cms", "tildacsvformat": "cms", "tildaymlformat": "cms",
    "uralcmscsvformat": "cms", "ushopymlformat": "cms",
    "webasystshopscriptformat": "cms", "wixformat": "cms",
    "woocommerceformat": "cms", "bitrixcsvformat": "cms",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[end + 5:]


def load_pages() -> list[dict]:
    out = []
    for path in sorted(PAGES.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        headings = re.findall(r"^(#{1,4})\s+(.+)$", body, flags=re.M)
        out.append({
            "slug": path.stem,
            "path": meta.get("path"),
            "url": meta.get("url"),
            "title": meta.get("title"),
            "fetched_at": meta.get("fetched_at"),
            "sha256": meta.get("sha256"),
            "http_status": meta.get("http_status"),
            "chars": len(body),
            "headings": [{"level": len(h), "text": t.strip()} for h, t in headings],
            "body": body,
        })
    return out


def parse_endpoints(api_body: str, source_url: str) -> list[dict]:
    pattern = re.compile(r"^### (GET|POST|PUT|DELETE|PATCH) (\S+)\s*$", re.M)
    matches = list(pattern.finditer(api_body))
    endpoints = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(api_body)
        section = api_body[start:end]
        # cut related-material tail
        section = section.split("## Связанные материалы")[0]
        method, path = m.group(1), m.group(2)
        summary = ""
        for line in section.splitlines():
            line = line.strip()
            if line and not line.startswith("**") and not line.startswith("-"):
                summary = line
                break
        request_block, response_block = "", ""
        req = re.search(r"\*\*Запрос:\*\*(.*?)(?=\*\*Ответ|\Z)", section, re.S | re.I)
        if req:
            request_block = req.group(1).strip()
        resp = re.search(r"\*\*Ответ\*\*(?:\s*\([^)]*\))?:(.*)", section, re.S)
        if resp:
            response_block = resp.group(1).strip()

        def fields(block: str) -> list[dict]:
            items = []
            for line in block.splitlines():
                line = line.strip()
                if not line.startswith("- "):
                    continue
                text = line[2:]
                codes = re.findall(r"`([^`]+)`", text)
                name = codes[0] if codes else text.split("—")[0].strip()
                desc = text.split("—", 1)[1].strip() if "—" in text else ""
                items.append({"name": name, "description": desc})
            return items

        endpoints.append({
            "method": method,
            "path": path,
            "summary": summary,
            "request": request_block,
            "response": response_block,
            "request_fields": fields(request_block),
            "response_fields": fields(response_block),
            "source_url": source_url,
            "confidence": "measured",
        })
    return endpoints


def parse_formats(pages: list[dict]) -> list[dict]:
    formats = []
    for page in pages:
        if not page["path"] or not page["path"].startswith("/howto/format/"):
            continue
        slug = page["path"].rsplit("/", 1)[-1]
        if slug == "format":
            continue
        title = page["title"] or slug
        target = re.sub(r"^Как выгрузить товары (в|на|для)\s*", "", title, flags=re.I)
        target = re.sub(r"\?$", "", target).strip()
        settings = []
        for h in page["headings"]:
            if h["level"] >= 3 and re.search(r"настройк|формат|характеристик|тег|поле", h["text"], re.I):
                settings.append(h["text"])
        bolds = re.findall(r"\*\*([^*]{2,80})\*\*", page["body"])
        formats.append({
            "slug": slug,
            "title": title,
            "target": target,
            "category": FORMAT_CATEGORY.get(slug, "other"),
            "settings_headings": settings,
            "bold_terms": sorted(set(bolds))[:40],
            "source_url": page["url"],
            "confidence": "measured",
        })
    return sorted(formats, key=lambda f: (f["category"], f["slug"]))


def parse_plans(tariff_body: str, source_url: str) -> list[dict]:
    def to_int(value: str | None) -> int | None:
        if not value:
            return None
        digits = re.sub(r"\D", "", value)
        return int(digits) if digits else None

    plans = []
    known = ["Пробная версия", "Day", "Lite", "Pro"]
    positions = []
    for name in known:
        m = re.search(rf"^{re.escape(name)}\s*$", tariff_body, re.M)
        if m:
            positions.append((m.start(), name))
    positions.sort()
    for i, (start, name) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(tariff_body)
        block = tariff_body[start:end]
        price = re.search(r"([\d\s]+)\s*₽\s*/\s*(день|мес)", block)
        parallel = re.search(r"(\d+)\s+параллельн", block)
        aip = re.search(r"([\d\s]+)\s*AI Points", block)
        plans.append({
            "name": name,
            "price_rub": to_int(price.group(1)) if price else 0,
            "period": price.group(2) if price else ("trial" if name == "Пробная версия" else None),
            "parallel_downloads": to_int(parallel.group(1)) if parallel else None,
            "ai_points": to_int(aip.group(1)) if aip else None,
            "features": [l.strip()[2:] for l in block.splitlines() if l.strip().startswith("- ")][:12],
            "source_url": source_url,
            "confidence": "measured",
        })
    return plans


def build_claims(pages: list[dict], endpoints: list[dict], plans: list[dict]) -> list[dict]:
    api = next((p for p in pages if p["path"] == "/howto/api"), None)
    tariffs = next((p for p in pages if p["path"] == "/tariffs"), None)
    webhooks = next((p for p in pages if p["path"] == "/howto/automata/webhooks"), None)
    claims = []

    def add(subject, predicate, obj, value, unit, source, confidence="measured", note=""):
        claims.append({
            "subject": subject, "predicate": predicate, "object": obj,
            "value": value, "unit": unit, "source_url": source,
            "confidence": confidence, "note": note,
            "observed_at": datetime.now(timezone.utc).date().isoformat(),
        })

    if api:
        add("q-parser-api", "base_url", "base", "https://q-parser.ru/api/v1", "url", api["url"])
        add("q-parser-api", "auth", "header", "Authorization: Bearer | X-Api-Key", "header", api["url"])
        add("q-parser-api", "endpoint_count", "count", len(endpoints), "endpoints", api["url"])
        body = api["body"]
        for m in re.finditer(r"не больше\s*(\d+)\s*незавершенн\w*\s*(парсингов|выгрузок)", body, re.I):
            add("q-parser-api", "concurrency_limit", m.group(2), int(m.group(1)), "jobs", api["url"])
        for m in re.finditer(r"максимум\s*(\d+)", body, re.I):
            add("q-parser-api", "page_size_max", "pagination", int(m.group(1)), "records", api["url"])
        if "50 товаров" in body:
            add("q-parser-api", "trial_limit", "trial", 50, "goods", api["url"])
    if tariffs:
        for plan in plans:
            add("q-parser-plan", "price", plan["name"], plan["price_rub"], f"RUB/{plan['period']}", tariffs["url"])
    if webhooks:
        add("q-parser-webhooks", "signature", "headers", "X-QParser-Signature: sha256=HMAC-SHA256(timestamp.body)", "scheme", webhooks["url"])
        add("q-parser-webhooks", "retry_schedule", "seconds", "1,5,10,30,60", "schedule", webhooks["url"])
        add("q-parser-webhooks", "max_addresses", "per_automation", 5, "webhooks", webhooks["url"])
    return claims


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pages = load_pages()
    api = next((p for p in pages if p["path"] == "/howto/api"), None)
    tariffs = next((p for p in pages if p["path"] == "/tariffs"), None)
    endpoints = parse_endpoints(api["body"], api["url"]) if api else []
    formats = parse_formats(pages)
    plans = parse_plans(tariffs["body"], tariffs["url"]) if tariffs else []
    claims = build_claims(pages, endpoints, plans)

    for name, payload in [
        ("pages", [{k: v for k, v in p.items() if k != "body"} for p in pages]),
        ("endpoints", endpoints),
        ("formats", formats),
        ("plans", plans),
        ("claims", claims),
    ]:
        (OUT / f"{name}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    stats = {
        "pages": len(pages),
        "pages_ok": sum(1 for p in pages if p.get("http_status") == "200"),
        "total_chars": sum(p["chars"] for p in pages),
        "endpoints": len(endpoints),
        "formats": len(formats),
        "formats_by_category": {c: sum(1 for f in formats if f["category"] == c) for c in sorted({f["category"] for f in formats})},
        "plans": len(plans),
        "claims": len(claims),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
