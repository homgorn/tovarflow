"""Mock Q-Parser API for local development and contract tests.

It implements the documented surface closely enough to build the ingestion client without a paid
account: auth, catalogue, website options, categories, parse progress, goods pagination, formats,
exports and stop/resume.

Usage:
    python tools/mock_qparser.py --port 8765
    python tools/mock_qparser.py --port 8765 --no-auth

This is a test fixture, not a production service. It stores everything in memory.
"""

from __future__ import annotations

import argparse
import json
import random
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DOMAINS = [
    {"domain": "demo-home.ru", "title": "Demo Home", "categories": ["Кухня", "Текстиль"]},
    {"domain": "demo-tech.ru", "title": "Demo Tech", "categories": ["Аксессуары", "Аудио"]},
    {"domain": "demo-kids.ru", "title": "Demo Kids", "categories": ["Игрушки", "Одежда"]},
]

FORMATS = [
    {"id": "csv", "title": "CSV", "options": {}},
    {"id": "yml", "title": "YML (Яндекс.Маркет)", "options": {
        "split": {"title": "Разделять свойства", "type": "select",
                  "values": [{"key": "0", "label": "Нет"}, {"key": "1", "label": "Да"}]}}},
    {"id": "json", "title": "JSON", "options": {}},
]

STATE_LOCK = threading.Lock()
PARSES: dict[str, dict] = {}
EXPORTS: dict[str, dict] = {}
CATEGORY_JOBS: dict[str, dict] = {}


def now_ms() -> int:
    return int(time.time() * 1000)


def make_goods(domain: str, count: int, seed: int) -> list[dict]:
    rng = random.Random(f"{domain}:{seed}")
    goods = []
    for i in range(count):
        price = rng.randint(500, 15000)
        goods.append({
            "title": f"Товар {i + 1} — {domain}",
            "article": f"ART-{i + 1:05d}",
            "url": f"https://{domain}/product/{i + 1}",
            "price": price,
            "old_price": price + rng.choice([0, 0, 300, 700]),
            "currency": "RUB",
            "brand": rng.choice(["Nord", "Delta", "Sfera", "Lumen"]),
            "quantity": rng.choice([0, 1, 5, 10, 50]),
            "publish": rng.choice([True, True, False, None]),
            "images": [f"https://picsum.photos/seed/{domain}-{i}/800/800"],
            "file_links": [],
            "video_links": [],
            "category_title": "Кухня" if i % 2 == 0 else "Текстиль",
            "category_url": f"https://{domain}/category/{'kitchen' if i % 2 == 0 else 'textile'}",
            "description": f"Описание товара {i + 1}. Тестовые данные для разработки.",
            "short_description": f"Короткое описание {i + 1}",
            "data": {
                "Цвет": rng.choice(["белый", "чёрный", "серый"]),
                "Материал": rng.choice(["хлопок", "керамика", "金属"]),
                "Размер": rng.choice(["S", "M", "L"]),
            },
        })
    return goods


def progress_parse(parse_id: str, total: int) -> None:
    for i in range(1, total + 1):
        time.sleep(0.05)
        with STATE_LOCK:
            job = PARSES.get(parse_id)
            if not job or job["status"] in ("canceled", "error"):
                return
            job["goods_processed"] = i
            job["categories_processed"] = job["categories_total"] if i == total else min(
                job["categories_total"], 1 + (i * job["categories_total"] // total))
    with STATE_LOCK:
        job = PARSES.get(parse_id)
        if job:
            job["status"] = "completed"
            job["finished"] = now_ms()


class Handler(BaseHTTPRequestHandler):
    server_version = "MockQParser/1.0"

    def log_message(self, fmt, *args):  # keep the smoke output readable
        if getattr(self.server, "verbose", False):
            super().log_message(fmt, *args)

    def _json(self, code: int, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code: int, error_code: str, message: str) -> None:
        self._json(code, {"error": {"code": error_code, "message": message}})

    def _authorized(self) -> bool:
        if getattr(self.server, "no_auth", False):
            return True
        auth = self.headers.get("Authorization", "")
        key = self.headers.get("X-Api-Key", "")
        return auth.startswith("Bearer ") or bool(key)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_GET(self) -> None:  # noqa: N802
        if not self._authorized():
            return self._error(401, "unauthorized", "missing API key")
        parsed = urlparse(self.path)
        path, query = parsed.path, parse_qs(parsed.query)

        if path == "/api/v1/me":
            return self._json(200, {"email": "demo@example.com", "tariff_id": "pro",
                                    "tariff_until": now_ms() + 30 * 86400_000,
                                    "balance": 0, "ai_points": 10000})

        if path == "/api/v1/catalog":
            q = (query.get("q", [""])[0] or "").lower()
            free = query.get("free", ["0"])[0] == "1"
            limit = min(int(query.get("limit", ["100"])[0]), 1000)
            offset = int(query.get("offset", ["0"])[0])
            items = [d for d in DOMAINS if not q or q in d["domain"].lower() or q in d["title"].lower()]
            if free:
                items = items[:1]
            page = items[offset:offset + limit]
            return self._json(200, {
                "total": len(items), "limit": limit, "offset": offset,
                "list": [{"domain": d["domain"], "title": d["title"],
                          "slug": d["domain"].replace(".", "-"), "private": False,
                          "free_until": None,
                          "categories": [{"title": c, "slug": c.lower()} for c in d["categories"]],
                          "cities": [{"title": "Москва", "slug": "moscow"}]} for d in page],
            })

        if path.startswith("/api/v1/website/"):
            domain = path.rsplit("/", 1)[-1]
            return self._json(200, {"domain": domain, "protocol": "https",
                                    "auth_required": False, "manual_categories": False,
                                    "options": {}})

        if path == "/api/v1/credentials":
            return self._json(200, {"credentials": []})

        if path.startswith("/api/v1/categories/"):
            job_id = path.rsplit("/", 1)[-1]
            job = CATEGORY_JOBS.get(job_id)
            if not job:
                return self._error(404, "not_found", "category job not found")
            return self._json(200, job)

        if path == "/api/v1/parser/list":
            limit = min(int(query.get("limit", ["100"])[0]), 1000)
            offset = int(query.get("offset", ["0"])[0])
            items = sorted(PARSES.values(), key=lambda x: x["created"], reverse=True)
            return self._json(200, {"total": len(items), "limit": limit, "offset": offset,
                                    "list": items[offset:offset + limit]})

        if path.startswith("/api/v1/parser/"):
            parts = path.strip("/").split("/")
            parse_id = parts[3]
            job = PARSES.get(parse_id)
            if not job:
                return self._error(404, "not_found", "parse not found")
            if len(parts) == 5 and parts[4] == "goods":
                if job.get("archive"):
                    return self._error(422, "unprocessable", "archived parse has no goods")
                limit = min(int(query.get("limit", ["100"])[0]), 1000)
                offset = int(query.get("offset", ["0"])[0])
                goods = job["_goods"]
                return self._json(200, {"total": len(goods), "limit": limit, "offset": offset,
                                        "goods": goods[offset:offset + limit]})
            return self._json(200, {k: v for k, v in job.items() if not k.startswith("_")})

        if path == "/api/v1/format":
            return self._json(200, {"formats": FORMATS})

        if path.startswith("/api/v1/export/"):
            export_id = path.rsplit("/", 1)[-1]
            job = EXPORTS.get(export_id)
            if not job:
                return self._error(404, "not_found", "export not found")
            return self._json(200, job)

        return self._error(404, "not_found", "unknown endpoint")

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized():
            return self._error(401, "unauthorized", "missing API key")
        path = urlparse(self.path).path
        body = self._body()

        if path == "/api/v1/credentials":
            return self._json(201, {"id": str(uuid.uuid4()), "login": body.get("login"),
                                    "domain": body.get("domain")})

        if path == "/api/v1/categories":
            job_id = str(uuid.uuid4())
            CATEGORY_JOBS[job_id] = {"id": job_id, "status": "completed", "updated": now_ms(),
                                     "categories": [{"title": c, "url": f"https://{body.get('domain')}/c/{c}"}
                                                    for c in ["Кухня", "Текстиль", "Аксессуары"]]}
            return self._json(201, {"id": job_id, "status": "completed"})

        if path == "/api/v1/parser":
            domain = body.get("domain", "demo-home.ru")
            trial = bool(body.get("trial"))
            total = 50 if trial else 100
            parse_id = f"id{random.randint(1000000, 9999999)}"
            job = {"id": parse_id, "status": "running", "domain": domain,
                   "goods_processed": 0, "goods_limited": total if trial else None,
                   "categories_total": 2, "categories_processed": 0,
                   "created": now_ms(), "finished": None, "archive": False, "error": None,
                   "_goods": make_goods(domain, total, random.randint(1, 10000))}
            PARSES[parse_id] = job
            threading.Thread(target=progress_parse, args=(parse_id, total), daemon=True).start()
            return self._json(201, {"id": parse_id})

        if path.startswith("/api/v1/parser/") and path.endswith("/stop"):
            parse_id = path.strip("/").split("/")[3]
            job = PARSES.get(parse_id)
            if not job:
                return self._error(404, "not_found", "parse not found")
            if job["status"] in ("completed", "canceled", "error"):
                return self._error(422, "unprocessable", "cannot stop")
            job["status"] = "canceled"
            job["finished"] = now_ms()
            return self._json(200, {k: v for k, v in job.items() if not k.startswith("_")})

        if path.startswith("/api/v1/parser/") and path.endswith("/resume"):
            parse_id = path.strip("/").split("/")[3]
            job = PARSES.get(parse_id)
            if not job or job["status"] != "canceled" or job.get("archive"):
                return self._error(422, "unprocessable", "cannot resume")
            job["status"] = "running"
            job["finished"] = None
            threading.Thread(target=progress_parse, args=(parse_id, len(job["_goods"])),
                             daemon=True).start()
            return self._json(200, {k: v for k, v in job.items() if not k.startswith("_")})

        if path == "/api/v1/export":
            parser_id = body.get("parser_id")
            if parser_id not in PARSES:
                return self._error(422, "unprocessable", "unknown parser_id")
            export_id = str(uuid.uuid4())
            EXPORTS[export_id] = {
                "id": export_id, "status": "completed", "parser_id": parser_id,
                "format": body.get("format", "csv"), "goods_exported": len(PARSES[parser_id]["_goods"]),
                "created": now_ms(), "finished": now_ms(), "error": None,
                "message": None,
                "files": [f"https://s3.example.test/{export_id}/export.csv"],
                "links": [], "progress": None,
            }
            return self._json(201, {"id": export_id})

        return self._error(404, "not_found", "unknown endpoint")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-auth", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.no_auth = args.no_auth
    server.verbose = args.verbose
    print(f"Mock Q-Parser on http://127.0.0.1:{args.port}/api/v1 (auth={'off' if args.no_auth else 'on'})")
    print("Endpoints: me, catalog, website, categories, parser, parser/:id/goods, format, export")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
