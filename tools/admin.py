"""Operator console prototype for TovarFlow.

Server-rendered HTML (no JS required) reading the local canonical catalogue:
dashboard, attribute mapping review, and a price-proposal approval queue.

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
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "catalog.sqlite"
FEED_REPORT = ROOT / "data" / "feeds" / "yandex.report.json"

SCHEMA = """
CREATE TABLE IF NOT EXISTS attribute_mapping (
  source_key TEXT PRIMARY KEY, canonical_key TEXT, reviewer TEXT, reviewed_at TEXT
);
CREATE TABLE IF NOT EXISTS proposal (
  id TEXT PRIMARY KEY, kind TEXT, ref_id TEXT, status TEXT, actor TEXT,
  reason TEXT, created_at TEXT, decided_at TEXT
);
CREATE TABLE IF NOT EXISTS approval_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT, proposal_id TEXT, action TEXT, actor TEXT,
  policy_decision TEXT, idempotency_key TEXT UNIQUE, created_at TEXT
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    return conn


def summary(conn: sqlite3.Connection) -> dict:
    counts = {}
    for table in ("ingest_run", "product", "variant", "offer", "media", "attribute",
                  "raw_good", "price_decision", "proposal", "attribute_mapping"):
        try:
            counts[table] = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        except sqlite3.Error:
            counts[table] = 0
    runs = conn.execute(
        "SELECT domain,parse_id,status,goods_total,goods_written,unknown_publish,created_at "
        "FROM ingest_run ORDER BY created_at DESC"
    ).fetchall()
    feed = {}
    if FEED_REPORT.exists():
        try:
            feed = json.loads(FEED_REPORT.read_text(encoding="utf-8"))
        except ValueError:
            feed = {}
    return {"counts": counts, "runs": runs, "feed": feed}


def ensure_proposals(conn: sqlite3.Connection) -> None:
    stamp = now()
    rows = conn.execute(
        "SELECT offer_id,price_minor,is_complete,can_publish FROM price_decision"
    ).fetchall()
    for offer_id, price, complete, can_publish in rows:
        conn.execute(
            "INSERT OR IGNORE INTO proposal(id,kind,ref_id,status,created_at) VALUES(?,?,?,?,?)",
            (f"prop_{offer_id}", "PRICE", offer_id, "PENDING", stamp),
        )
    conn.commit()


def mapping_stats(conn: sqlite3.Connection) -> list[dict]:
    counts: dict[str, int] = {}
    for (raw,) in conn.execute("SELECT attributes_raw FROM product"):
        try:
            attrs = json.loads(raw or "{}")
        except ValueError:
            attrs = {}
        for key in attrs:
            counts[str(key)] = counts.get(str(key), 0) + 1
    mapped = {k: (c, r) for k, c, r in conn.execute(
        "SELECT source_key,canonical_key,reviewed_at FROM attribute_mapping")}
    out = []
    for key in sorted(counts):
        canonical, reviewed = mapped.get(key, ("", ""))
        out.append({"key": key, "count": counts[key], "canonical": canonical,
                    "reviewed": reviewed})
    return out


def proposals(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT p.id,p.status,p.actor,p.reason,p.created_at,p.decided_at,"
        "d.price_minor,d.is_complete,d.can_publish,d.explanation "
        "FROM proposal p LEFT JOIN price_decision d ON d.offer_id=p.ref_id "
        "ORDER BY CASE p.status WHEN 'PENDING' THEN 0 ELSE 1 END, p.id LIMIT 60"
    ).fetchall()
    return [{"id": r[0], "status": r[1], "actor": r[2], "reason": r[3],
             "created": r[4], "decided": r[5], "price": r[6], "complete": r[7],
             "can_publish": r[8], "explanation": r[9]} for r in rows]


def head(title: str, active: str) -> str:
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title>
<style>
:root{{color-scheme:light;--bg:#f5f6f8;--card:#fff;--ink:#151a22;--muted:#5b6474;--line:#dfe3ea;--accent:#1d5fd8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
.wrap{{max-width:1050px;margin:0 auto;padding:22px 16px 60px}}h1{{font-size:26px;margin:0 0 12px}}h2{{font-size:19px;margin:28px 0 10px}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:9px;padding:14px 16px;font-size:16px}}
table{{width:100%;border-collapse:collapse;background:var(--card);font-size:14px}}th,td{{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}}
th{{background:#eef2f8}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:12px}}.num{{font-size:24px;font-weight:700}}
.ok{{color:#147a4b;font-weight:650}}.bad{{color:#b42318;font-weight:650}}code{{background:#eef2f8;padding:1px 4px;border-radius:3px}}
nav a{{margin-right:14px;color:var(--accent)}}footer{{margin-top:32px;color:var(--muted);font-size:13px}}
input{{padding:5px 7px;border:1px solid var(--line);border-radius:5px}}button{{background:var(--accent);color:#fff;border:0;border-radius:5px;padding:6px 12px;cursor:pointer}}
button.reject{{background:#b42318}}
</style></head><body><div class="wrap">
<nav><a href="/">Дашборд</a><a href="/mapping">Маппинг</a><a href="/proposals">Предложения</a><a href="/feed">YML</a><a href="https://github.com/homgorn/tovarflow">GitHub</a></nav>
<h1>{escape(title)}</h1>"""


def tail() -> str:
    return f"<footer>Обновлено {escape(now())} · прототип по specs/007 · без JavaScript и секретов в HTML</footer></div></body></html>"


def page_dashboard() -> str:
    conn = connect()
    s = summary(conn)
    c = s["counts"]
    feed = s["feed"]
    rows = "".join(
        f"<tr><td>{escape(str(r[0]))}</td><td><code>{escape(str(r[1]))}</code></td>"
        f"<td>{escape(str(r[2]))}</td><td>{r[3] or 0}</td><td>{r[4] or 0}</td>"
        f"<td>{r[5] or 0}</td><td>{escape(str(r[6] or ''))}</td></tr>"
        for r in s["runs"]
    ) or "<tr><td colspan='7'>Нет запусков</td></tr>"
    parts = [head("TovarFlow — операторский дашборд", "dashboard")]
    parts.append(
        f'<p class="lead">В каталоге {c["product"]} продуктов, {c["offer"]} офферов и '
        f'{c["price_decision"]} ценовых решений; в очереди {c["proposal"]} предложений; '
        f'YML-фид {"валиден" if feed.get("valid") else "НЕ валиден"} на '
        f'{feed.get("offers", 0)} офферов.</p>'
    )
    parts.append('<div class="cards">')
    for value, label in ((c["product"], "продуктов"), (c["offer"], "офферов"),
                         (c["proposal"], "предложений"),
                         (feed.get("fallback_vendors", 0), "подстановок vendor")):
        parts.append(f'<div class="card"><div class="num">{value}</div>{label}</div>')
    parts.append("</div><h2>Запуски парсинга</h2>")
    parts.append("<table><thead><tr><th>Домен</th><th>Parse id</th><th>Статус</th><th>Обработано</th>"
                 "<th>Записано</th><th>Неизвестный publish</th><th>Дата</th></tr></thead><tbody>"
                 + rows + "</tbody></table>")
    parts.append('<h2>Очередь ценовых предложений</h2>')
    pend = conn.execute("SELECT count(*) FROM proposal WHERE status='PENDING'").fetchone()[0]
    parts.append(f'<p>Ожидают решения: <strong>{pend}</strong>. '
                 '<a href="/proposals">Открыть очередь →</a></p>')
    parts.append('<h2>Маппинг атрибутов</h2>')
    mapped = conn.execute("SELECT count(*) FROM attribute_mapping").fetchone()[0]
    parts.append(f'<p>Подтверждено соответствий: <strong>{mapped}</strong>. '
                 '<a href="/mapping">Открыть словарь →</a></p>')
    parts.append(tail())
    conn.close()
    return "".join(parts)


def page_mapping(message: str = "") -> str:
    conn = connect()
    stats = mapping_stats(conn)
    rows = "".join(
        f"<tr><td><code>{escape(s['key'])}</code></td><td>{s['count']}</td>"
        f"<td>{escape(s['canonical'] or '—')}</td><td>{escape(s['reviewed'] or '—')}</td>"
        f"<td><form method='post' action='/mapping'>"
        f"<input type='hidden' name='source_key' value='{escape(s['key'], quote=True)}'>"
        "<input name='canonical_key' placeholder='color / size / material' required>"
        "<input name='reviewer' value='operator' required>"
        "<button type='submit'>Подтвердить</button></form></td></tr>"
        for s in stats
    ) or "<tr><td colspan='5'>Ключей атрибутов нет</td></tr>"
    conn.close()
    return "".join([
        head("TovarFlow — маппинг атрибутов", "mapping"),
        f'<p class="lead">В каталоге {len(stats)} уникальных ключей атрибутов. Подтверждённые '
        'соответствия пишутся в словарь и больше не попадают в отчёт качества. '
        'Источник: данные поставщика, измерено на живом парсинге npopt.ru.</p>',
        ("<p class='ok'>" + escape(message) + "</p>") if message else "",
        "<table><thead><tr><th>Ключ поставщика</th><th>Товаров</th><th>Канонический ключ</th>"
        "<th>Проверен</th><th>Действие</th></tr></thead><tbody>" + rows + "</tbody></table>",
        tail(),
    ])


def page_proposals(message: str = "") -> str:
    conn = connect()
    ensure_proposals(conn)
    items = proposals(conn)
    rows = "".join(
        f"<tr><td><code>{escape(p['id'])}</code></td><td>{escape(str(p['status']))}</td>"
        f"<td>{p['price'] / 100 if p['price'] is not None else '—'}</td>"
        f"<td>{'полная' if p['complete'] else 'неполная'}</td>"
        f"<td>{escape(str(p['actor'] or '—'))}</td>"
        f"<td><form method='post' action='/proposals'>"
        f"<input type='hidden' name='proposal_id' value='{escape(p['id'], quote=True)}'>"
        "<input type='hidden' name='actor' value='operator'>"
        "<button name='action' value='approve' type='submit'>Одобрить</button> "
        "<button class='reject' name='action' value='reject' type='submit'>Отклонить</button>"
        "</form></td></tr>"
        for p in items
    ) or "<tr><td colspan='6'>Предложений нет</td></tr>"
    conn.close()
    return "".join([
        head("TovarFlow — ценовые предложения", "proposals"),
        f'<p class="lead">В очереди {len(items)} ценовых предложений. Каждое решение пишется '
        'в append-only журнал с idempotency-ключом; одобренное предложение получает '
        'политику ALLOW и может уйти в исполнение коннектора.</p>',
        ("<p class='ok'>" + escape(message) + "</p>") if message else "",
        "<table><thead><tr><th>ID</th><th>Статус</th><th>Цена, ₽</th><th>Проверка</th>"
        "<th>Кто решил</th><th>Решение</th></tr></thead><tbody>" + rows + "</tbody></table>",
        tail(),
    ])


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str | bytes, ctype: str = "text/html; charset=utf-8", code: int = 200) -> None:
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        parsed = parse_qs(raw, keep_blank_values=True)
        return {k: v[0] for k, v in parsed.items()}

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/feed" and FEED_REPORT.exists():
            return self._send(FEED_REPORT.read_bytes(), "application/json; charset=utf-8")
        if self.path == "/mapping":
            return self._send(page_mapping())
        if self.path == "/proposals":
            return self._send(page_proposals())
        if self.path == "/":
            return self._send(page_dashboard())
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        form = self._form()
        conn = connect()
        if self.path == "/mapping":
            key = form.get("source_key", "").strip()
            canonical = form.get("canonical_key", "").strip()
            reviewer = form.get("reviewer", "operator").strip()
            if key and canonical:
                conn.execute(
                    "INSERT INTO attribute_mapping(source_key,canonical_key,reviewer,reviewed_at) "
                    "VALUES(?,?,?,?) ON CONFLICT(source_key) DO UPDATE SET "
                    "canonical_key=excluded.canonical_key,reviewer=excluded.reviewer,"
                    "reviewed_at=excluded.reviewed_at",
                    (key, canonical, reviewer, now()),
                )
                conn.commit()
            return self._redirect("/mapping")
        if self.path == "/proposals":
            pid = form.get("proposal_id", "").strip()
            action = form.get("action", "").strip()
            actor = form.get("actor", "operator").strip()
            decision = "ALLOW" if action == "approve" else "DENY"
            status = "APPROVED" if action == "approve" else "REJECTED"
            idem = f"approval:{pid}:{decision}"
            if pid and action in ("approve", "reject"):
                cur = conn.execute(
                    "INSERT OR IGNORE INTO approval_event(proposal_id,action,actor,"
                    "policy_decision,idempotency_key,created_at) VALUES(?,?,?,?,?,?)",
                    (pid, action, actor, decision, idem, now()),
                )
                if cur.rowcount:
                    conn.execute(
                        "UPDATE proposal SET status=?,actor=?,reason=?,decided_at=? "
                        "WHERE id=? AND status='PENDING'",
                        (status, actor, f"policy {decision}", now(), pid),
                    )
                conn.commit()
            return self._redirect("/proposals")
        self.send_error(404)

    def log_message(self, fmt, *args) -> None:
        pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8878)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Admin console on http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
