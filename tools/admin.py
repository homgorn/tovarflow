"""Minimal operator console prototype for TovarFlow.

Server-rendered HTML (no JS required) that reads the local canonical catalogue and feed report.
This is the first slice of the admin decision from specs/007: facts first, tables, provenance.

Usage:
    python tools/admin.py --port 8878
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "catalog.sqlite"
FEED_REPORT = ROOT / "data" / "feeds" / "yandex.report.json"
WIKI_INDEX = ROOT / "wiki" / "index.md"


def summary() -> dict:
    conn = sqlite3.connect(DB)
    counts = {}
    for table in ("ingest_run", "product", "variant", "offer", "media", "attribute",
                  "raw_good", "price_decision"):
        try:
            counts[table] = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        except sqlite3.Error:
            counts[table] = 0
    runs = conn.execute(
        "SELECT domain,parse_id,status,goods_total,goods_written,unknown_publish,created_at "
        "FROM ingest_run ORDER BY created_at DESC"
    ).fetchall()
    quality = conn.execute(
        "SELECT domain,unmapped_keys FROM ingest_run WHERE unmapped_keys IS NOT NULL"
    ).fetchall()
    conn.close()
    feed = {}
    if FEED_REPORT.exists():
        try:
            feed = json.loads(FEED_REPORT.read_text(encoding="utf-8"))
        except ValueError:
            feed = {}
    return {"counts": counts, "runs": runs, "quality": quality, "feed": feed}


def render_page() -> str:
    s = summary()
    c = s["counts"]
    feed = s["feed"]
    rows = "".join(
        f"<tr><td>{escape(str(r[0]))}</td><td><code>{escape(str(r[1]))}</code></td>"
        f"<td>{escape(str(r[2]))}</td><td>{r[3] or 0}</td><td>{r[4] or 0}</td>"
        f"<td>{r[5] or 0}</td><td>{escape(str(r[6] or ''))}</td></tr>"
        for r in s["runs"]
    ) or "<tr><td colspan='7'>Нет запусков</td></tr>"
    quality_rows = "".join(
        f"<tr><td>{escape(str(d))}</td><td><code>{escape(str(k or '[]'))}</code></td></tr>"
        for d, k in s["quality"]
    ) or "<tr><td colspan='2'>Несоответствий нет</td></tr>"
    feed_valid = feed.get("valid", False)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TovarFlow Admin</title>
<style>
:root{{color-scheme:light;--bg:#f5f6f8;--card:#fff;--ink:#151a22;--muted:#5b6474;--line:#dfe3ea;--accent:#1d5fd8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
.wrap{{max-width:1000px;margin:0 auto;padding:22px 16px 60px}}h1{{font-size:26px;margin:0 0 12px}}h2{{font-size:19px;margin:28px 0 10px}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:9px;padding:14px 16px;font-size:16px}}
table{{width:100%;border-collapse:collapse;background:var(--card);font-size:14px}}th,td{{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}}
th{{background:#eef2f8}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:12px}}.num{{font-size:24px;font-weight:700}}
.ok{{color:#147a4b;font-weight:650}}.bad{{color:#b42318;font-weight:650}}code{{background:#eef2f8;padding:1px 4px;border-radius:3px}}
nav a{{margin-right:14px;color:var(--accent)}}footer{{margin-top:32px;color:var(--muted);font-size:13px}}
</style></head><body><div class="wrap">
<nav><a href="/">Дашборд</a><a href="/feed">YML</a><a href="https://github.com/homgorn/tovarflow">GitHub</a></nav>
<h1>TovarFlow — операторский дашборд</h1>
<p class="lead">В каталоге {c['product']} продуктов, {c['offer']} офферов и {c['price_decision']} ценовых решений; YML-фид {'валиден' if feed_valid else 'НЕ валиден'} на {feed.get('offers', 0)} офферов. Все данные приходят из локального канонического каталога и отчёта фида, а не из папок с выгрузками.</p>
<div class="cards">
<div class="card"><div class="num">{c['product']}</div>продуктов</div>
<div class="card"><div class="num">{c['offer']}</div>офферов</div>
<div class="card"><div class="num">{c['media']}</div>медиа</div>
<div class="card"><div class="num">{c['raw_good']}</div>сырых товаров</div>
<div class="card"><div class="num">{feed.get('fallback_vendors', 0)}</div>подстановок vendor</div>
</div>
<h2>Запуски парсинга</h2>
<table><thead><tr><th>Домен</th><th>Parse id</th><th>Статус</th><th>Обработано</th><th>Записано</th><th>Неизвестный publish</th><th>Дата</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Качество данных</h2>
<table><thead><tr><th>Домен</th><th>Нераспознанные ключи атрибутов</th></tr></thead><tbody>{quality_rows}</tbody></table>
<h2>Фид</h2>
<p>Офферов: <strong>{feed.get('offers', 0)}</strong> · категорий: <strong>{feed.get('categories', 0)}</strong> · ошибок валидации: <strong class="{'ok' if not feed.get('validation_errors') else 'bad'}">{len(feed.get('validation_errors') or [])}</strong> · статус: <strong class="{'ok' if feed_valid else 'bad'}">{feed.get('valid')}</strong></p>
<h2>Что дальше</h2>
<table><thead><tr><th>Экран</th><th>Действие</th></tr></thead><tbody>
<tr><td>Источники и парсинг</td><td>перезапуск, просмотр raw, сравнение с прошлым запуском</td></tr>
<tr><td>Маппинг атрибутов</td><td>разобрать нераспознанные ключи и подтвердить словарь</td></tr>
<tr><td>Цены</td><td>симуляция маржи до публикации, approval ниже floor</td></tr>
<tr><td>Листинги</td><td>очередь модерации mapper/канал, состояние карточки</td></tr>
<tr><td>Сверка</td><td>parsed → published → rejected → sold</td></tr>
</tbody></table>
<footer>Обновлено {escape(now)} · прототип по specs/007 · без JavaScript, без секретов в HTML</footer>
</div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/feed" and FEED_REPORT.exists():
            body = FEED_REPORT.read_bytes()
            ctype = "application/json; charset=utf-8"
        elif self.path == "/":
            body = render_page().encode("utf-8")
            ctype = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args) -> None:
        pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8878)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Admin prototype on http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
