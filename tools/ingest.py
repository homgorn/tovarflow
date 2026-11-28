"""First vertical slice: ingest one Q-Parser domain into a canonical local catalogue.

This is a local prototype using SQLite (Postgres is the production system of record). It proves
the contract end to end: catalog -> website -> categories -> parse -> goods -> canonical product.

Usage:
    python tools/ingest.py --domain demo-home.ru --mock
    python tools/ingest.py --domain my-supplier.ru --limit 500   # needs QPARSER_API_KEY in .env
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import redact  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "catalog.sqlite"
REPORT_DIR = ROOT / "data" / "ingest"

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS ingest_run (
  id TEXT PRIMARY KEY, domain TEXT NOT NULL, parse_id TEXT, status TEXT,
  goods_total INTEGER, goods_written INTEGER, unknown_publish INTEGER,
  unmapped_keys TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS product (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL DEFAULT 'default', domain TEXT,
  url TEXT, external_article TEXT, title TEXT, brand TEXT, description TEXT,
  short_description TEXT, category_title TEXT, category_url TEXT,
  attributes_raw TEXT, content_hash TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS variant (
  id TEXT PRIMARY KEY, product_id TEXT NOT NULL, sku TEXT, title TEXT
);
CREATE TABLE IF NOT EXISTS offer (
  id TEXT PRIMARY KEY, variant_id TEXT NOT NULL, url TEXT, price_minor INTEGER,
  old_price_minor INTEGER, currency TEXT, quantity INTEGER, publish INTEGER
);
CREATE TABLE IF NOT EXISTS media (
  id TEXT PRIMARY KEY, product_id TEXT NOT NULL, url TEXT, kind TEXT, position INTEGER, sha256 TEXT
);
CREATE TABLE IF NOT EXISTS attribute (
  id TEXT PRIMARY KEY, product_id TEXT NOT NULL, key TEXT, value TEXT
);
CREATE TABLE IF NOT EXISTS raw_good (
  id TEXT PRIMARY KEY, ingest_run_id TEXT NOT NULL, payload TEXT, sha256 TEXT,
  position INTEGER
);
CREATE VIRTUAL TABLE IF NOT EXISTS product_fts USING fts5(
  title, description, brand, sku, tokenize='unicode61'
);
"""

KNOWN_KEYS = {"Цвет": "color", "Материал": "material", "Размер": "size",
              "Color": "color", "Material": "material", "Size": "size",
              "颜色": "color", "材质": "material", "尺寸": "size"}


def uid(*parts: str) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:24]


def to_minor(value) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(round(float(value) * 100))
    text = str(value).replace(" ", "").replace(",", ".")
    try:
        return int(round(float(text) * 100))
    except ValueError:
        return None


def start_mock() -> tuple[ThreadingHTTPServer, str]:
    from mock_qparser import Handler
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.no_auth = True
    server.verbose = False
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    return server, f"http://127.0.0.1:{port}/api/v1"


def init_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(raw_good)")}
    if "position" not in columns:
        conn.execute("ALTER TABLE raw_good ADD COLUMN position INTEGER")
    return conn


def upsert(conn: sqlite3.Connection, table: str, columns: list[str], values: tuple) -> None:
    placeholders = ",".join("?" for _ in columns)
    updates = ",".join(f"{c}=excluded.{c}" for c in columns if c != "id")
    conn.execute(
        f"INSERT INTO {table}({','.join(columns)}) VALUES({placeholders}) "
        f"ON CONFLICT(id) DO UPDATE SET {updates}", values,
    )


def normalise(good: dict, domain: str, run_id: str, conn: sqlite3.Connection,
              unmapped: set[str], position: int = 0) -> tuple[str, str]:
    external = good.get("article") or good.get("url") or uid(domain, json.dumps(good, sort_keys=True))
    product_id = uid("product", domain, external)
    payload = json.dumps(good, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    upsert(conn, "raw_good", ["id", "ingest_run_id", "payload", "sha256", "position"],
           (uid("raw", run_id, digest), run_id, payload, digest, position))

    title = good.get("title") or ""
    description = good.get("description") or ""
    attrs_raw = good.get("data") or {}
    content_hash = hashlib.sha256(
        json.dumps({"title": title, "description": description, "data": attrs_raw},
                   ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()

    upsert(conn, "product", [
        "id", "domain", "url", "external_article", "title", "brand", "description",
        "short_description", "category_title", "category_url", "attributes_raw",
        "content_hash", "created_at",
    ], (
        product_id, domain, good.get("url"), good.get("article"), title, good.get("brand"),
        description, good.get("short_description"), good.get("category_title"),
        good.get("category_url"), json.dumps(attrs_raw, ensure_ascii=False, sort_keys=True),
        content_hash, datetime.now(timezone.utc).isoformat(timespec="seconds"),
    ))

    variant_id = uid("variant", product_id, external)
    upsert(conn, "variant", ["id", "product_id", "sku", "title"],
           (variant_id, product_id, good.get("article"), title[:120]))
    upsert(conn, "offer", [
        "id", "variant_id", "url", "price_minor", "old_price_minor", "currency",
        "quantity", "publish",
    ], (
        uid("offer", variant_id, good.get("url")), variant_id, good.get("url"),
        to_minor(good.get("price")), to_minor(good.get("old_price")), good.get("currency"),
        good.get("quantity"), good.get("publish"),
    ))

    for i, image in enumerate(good.get("images") or []):
        if not image:
            continue
        upsert(conn, "media", ["id", "product_id", "url", "kind", "position", "sha256"],
               (uid("media", product_id, image), product_id, image, "image", i,
                hashlib.sha256(image.encode("utf-8")).hexdigest()[:16]))

    for key, value in attrs_raw.items():
        canonical = KNOWN_KEYS.get(str(key))
        if canonical:
            upsert(conn, "attribute", ["id", "product_id", "key", "value"],
                   (uid("attr", product_id, canonical), product_id, canonical, str(value)))
        else:
            unmapped.add(str(key))

    # Stable FTS rowid derived from the deterministic product id. Re-upserting replaces the row.
    rowid = int(product_id[:12], 16)
    conn.execute("DELETE FROM product_fts WHERE rowid=?", (rowid,))
    conn.execute("INSERT INTO product_fts(rowid,title,description,brand,sku) VALUES(?,?,?,?,?)",
                 (rowid, title, description, good.get("brand") or "", str(good.get("article") or "")))
    return product_id, content_hash


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=os.environ.get("INGEST_DOMAIN", "demo-home.ru"))
    parser.add_argument("--limit", type=int, default=int(os.environ.get("INGEST_LIMIT", "1000")))
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--parse-id", default=None,
                        help="continue an existing parse instead of starting a new one")
    args = parser.parse_args()

    mock_server = None
    if args.mock:
        os.environ["USE_MOCK"] = "1"
        mock_server, url = start_mock()
        os.environ["QPARSER_MOCK_URL"] = url
    else:
        url = None

    from qparser_client import QParserClient
    client = QParserClient()
    print(f"mode={'mock' if client.use_mock else 'live'} key={redact(client.api_key)}")

    catalog = client.catalog(q=args.domain)
    found = [s for s in catalog["list"] if s["domain"] == args.domain]
    if not found:
        print(f"domain not found in catalogue: {args.domain}")
        return 2
    site = client.website(args.domain)
    print("site options:", site.get("options"))

    if args.parse_id:
        parse_id = args.parse_id
        print("reusing parse:", parse_id)
    else:
        cat_job = client.start_categories(args.domain)
        for _ in range(30):
            categories = client.categories(cat_job["id"])
            if categories["status"] in ("completed", "error"):
                break
            time.sleep(0.5)
        if categories["status"] != "completed":
            print("categories failed:", categories)
            return 2
        chosen = categories.get("categories") or []
        print("categories:", len(chosen))
        parse_id = client.start_parser(args.domain, categories=chosen[:5])
    deadline = time.time() + 900
    status: dict = {}
    while time.time() < deadline:
        status = client.parser(parse_id)
        if status["status"] in ("completed", "error", "canceled"):
            break
        time.sleep(min(10, 1 + int(time.time() % 5)))
    if status.get("status") != "completed":
        print("parse failed:", status)
        return 2
    print("parse:", parse_id, "goods:", status["goods_processed"])

    conn = init_db()
    run_id = uid("run", args.domain, parse_id)
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO ingest_run(id,domain,parse_id,status,created_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(id) DO UPDATE SET status=excluded.status",
        (run_id, args.domain, parse_id, "running", created),
    )

    unmapped: set[str] = set()
    written = 0
    unknown_publish = 0
    hashes: list[str] = []
    for i, good in enumerate(client.iter_goods(parse_id, page_size=1000)):
        if i >= args.limit:
            break
        if good.get("publish") is None:
            unknown_publish += 1
        _, digest = normalise(good, args.domain, run_id, conn, unmapped, i)
        hashes.append(digest)
        written += 1
        if i % 200 == 0:
            conn.commit()
    conn.commit()

    summary_hash = hashlib.sha256("".join(hashes).encode("utf-8")).hexdigest()
    conn.execute(
        "UPDATE ingest_run SET status='completed',goods_total=?,goods_written=?,"
        "unknown_publish=?,unmapped_keys=? WHERE id=?",
        (status["goods_processed"], written, unknown_publish,
         json.dumps(sorted(unmapped), ensure_ascii=False), run_id),
    )
    conn.commit()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "domain": args.domain, "parse_id": parse_id, "run_id": run_id,
        "goods_processed": status["goods_processed"], "goods_written": written,
        "unknown_publish": unknown_publish, "unmapped_keys": sorted(unmapped),
        "canonical_hash": summary_hash, "generated_at": created,
        "storage": str(DB_PATH.relative_to(ROOT)).replace("\\", "/"),
    }
    report_path = REPORT_DIR / f"{args.domain.replace('.', '-')}.report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
              for t in ("product", "variant", "offer", "media", "attribute", "raw_good")}
    conn.close()
    if mock_server:
        mock_server.shutdown()
        mock_server.server_close()

    print("written:", written, "unknown publish:", unknown_publish)
    print("unmapped keys:", sorted(unmapped))
    print("canonical hash:", summary_hash[:16])
    print("counts:", counts)
    print("report:", report_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
