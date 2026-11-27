"""Build the Q-Parser knowledge base: SQLite + FTS5 + graph + LLM wiki.

Run after tools/fetch_corpus.py and tools/extract_qparser.py:
    python tools/build_knowledge.py
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "docs" / "research" / "qparser" / "extracted"
PAGES = ROOT / "docs" / "research" / "qparser" / "pages"
DATA = ROOT / "data"
WIKI = ROOT / "wiki"
DB_PATH = DATA / "qparser.sqlite"
TODAY = datetime.now(timezone.utc).date().isoformat()

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY,
  url TEXT UNIQUE NOT NULL,
  path TEXT NOT NULL,
  title TEXT,
  section TEXT,
  kind TEXT,
  http_status TEXT,
  fetched_at TEXT,
  sha256 TEXT,
  chars INTEGER,
  md_path TEXT
);

CREATE TABLE IF NOT EXISTS pages (
  id INTEGER PRIMARY KEY,
  source_id INTEGER NOT NULL REFERENCES sources(id),
  body TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY,
  source_id INTEGER NOT NULL REFERENCES sources(id),
  ord INTEGER NOT NULL,
  heading TEXT,
  text TEXT NOT NULL,
  chars INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS endpoints (
  id INTEGER PRIMARY KEY,
  method TEXT NOT NULL,
  path TEXT NOT NULL,
  summary TEXT,
  request TEXT,
  response TEXT,
  source_id INTEGER REFERENCES sources(id),
  UNIQUE(method, path)
);

CREATE TABLE IF NOT EXISTS endpoint_fields (
  id INTEGER PRIMARY KEY,
  endpoint_id INTEGER NOT NULL REFERENCES endpoints(id),
  direction TEXT NOT NULL CHECK (direction IN ('request','response')),
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS formats (
  id INTEGER PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT,
  target TEXT,
  category TEXT,
  source_id INTEGER REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS format_terms (
  id INTEGER PRIMARY KEY,
  format_id INTEGER NOT NULL REFERENCES formats(id),
  term TEXT NOT NULL,
  kind TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  price_rub INTEGER,
  period TEXT,
  parallel_downloads INTEGER,
  ai_points INTEGER,
  source_id INTEGER REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS plan_features (
  id INTEGER PRIMARY KEY,
  plan_id INTEGER NOT NULL REFERENCES plans(id),
  feature TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claims (
  id INTEGER PRIMARY KEY,
  subject TEXT NOT NULL,
  predicate TEXT NOT NULL,
  object TEXT,
  value TEXT,
  unit TEXT,
  source_id INTEGER REFERENCES sources(id),
  confidence TEXT,
  observed_at TEXT,
  note TEXT
);

CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  label TEXT NOT NULL,
  source_id INTEGER
);

CREATE TABLE IF NOT EXISTS edges (
  id INTEGER PRIMARY KEY,
  source TEXT NOT NULL,
  relation TEXT NOT NULL,
  target TEXT NOT NULL,
  confidence TEXT,
  source_id INTEGER
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  text, heading, url UNINDEXED, path UNINDEXED, tokenize='unicode61'
);
"""


def load(name: str):
    return json.loads((EXTRACTED / f"{name}.json").read_text(encoding="utf-8"))


def chunk_body(body: str, max_chars: int = 1400) -> list[dict]:
    sections: list[tuple[str, str]] = []
    current_heading = ""
    buffer: list[str] = []
    for line in body.splitlines():
        if re.match(r"^#{2,4}\s+", line):
            if buffer:
                sections.append((current_heading, "\n".join(buffer).strip()))
                buffer = []
            current_heading = re.sub(r"^#{2,4}\s+", "", line).strip()
        else:
            buffer.append(line)
    if buffer:
        sections.append((current_heading, "\n".join(buffer).strip()))

    chunks = []
    for heading, text in sections:
        if not text:
            continue
        if len(text) <= max_chars:
            chunks.append({"heading": heading, "text": text})
            continue
        paragraph: list[str] = []
        size = 0
        for para in text.split("\n\n"):
            if size + len(para) > max_chars and paragraph:
                chunks.append({"heading": heading, "text": "\n\n".join(paragraph)})
                paragraph, size = [], 0
            paragraph.append(para)
            size += len(para) + 2
        if paragraph:
            chunks.append({"heading": heading, "text": "\n\n".join(paragraph)})
    return chunks


def yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {v}" for v in values) if values else "  - (none)"


def write_wiki(path: Path, front: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = ["---"]
    for key, value in front.items():
        if isinstance(value, list):
            fm.append(f"{key}:")
            fm.append(yaml_list(value))
        else:
            fm.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    fm.append("---")
    path.write_text("\n".join(fm) + "\n\n" + body.strip() + "\n", encoding="utf-8")


def build_db() -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        candidate = Path(str(DB_PATH) + suffix)
        if candidate.exists():
            candidate.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    sources = load("pages")
    for src in sources:
        cur = conn.execute(
            "INSERT INTO sources(url,path,title,section,kind,http_status,fetched_at,sha256,chars,md_path) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (src["url"], src["path"], src["title"], src.get("section"), src.get("kind"),
             src.get("http_status"), src.get("fetched_at"), src.get("sha256"), src["chars"],
             str(PAGES / f"{src['slug']}.md")),
        )
        sid = cur.lastrowid
        body = (PAGES / f"{src['slug']}.md").read_text(encoding="utf-8").split("\n---\n", 1)[-1]
        conn.execute("INSERT INTO pages(source_id,body) VALUES(?,?)", (sid, body))
        for i, chunk in enumerate(chunk_body(body)):
            conn.execute(
                "INSERT INTO chunks(source_id,ord,heading,text,chars) VALUES(?,?,?,?,?)",
                (sid, i, chunk["heading"], chunk["text"], len(chunk["text"])),
            )
            conn.execute(
                "INSERT INTO chunks_fts(text,heading,url,path) VALUES(?,?,?,?)",
                (chunk["text"], chunk["heading"], src["url"], src["path"]),
            )

    def source_id(path: str) -> int | None:
        row = conn.execute("SELECT id FROM sources WHERE path=?", (path,)).fetchone()
        return row[0] if row else None

    api_sid = source_id("/howto/api")
    for ep in load("endpoints"):
        cur = conn.execute(
            "INSERT INTO endpoints(method,path,summary,request,response,source_id) VALUES(?,?,?,?,?,?)",
            (ep["method"], ep["path"], ep["summary"], ep["request"], ep["response"], api_sid),
        )
        for direction, fields in (("request", ep["request_fields"]), ("response", ep["response_fields"])):
            for field in fields:
                conn.execute(
                    "INSERT INTO endpoint_fields(endpoint_id,direction,name,description) VALUES(?,?,?,?)",
                    (cur.lastrowid, direction, field["name"], field["description"]),
                )

    for f in load("formats"):
        sid = source_id(f["source_url"].replace("https://q-parser.ru", ""))
        cur = conn.execute(
            "INSERT INTO formats(slug,title,target,category,source_id) VALUES(?,?,?,?,?)",
            (f["slug"], f["title"], f["target"], f["category"], sid),
        )
        for term in f["bold_terms"]:
            conn.execute("INSERT INTO format_terms(format_id,term,kind) VALUES(?,?,?)",
                         (cur.lastrowid, term, "setting"))

    plan_sid = source_id("/tariffs")
    for p in load("plans"):
        cur = conn.execute(
            "INSERT INTO plans(name,price_rub,period,parallel_downloads,ai_points,source_id) VALUES(?,?,?,?,?,?)",
            (p["name"], p["price_rub"], p["period"], p["parallel_downloads"], p["ai_points"], plan_sid),
        )
        for feature in p["features"]:
            conn.execute("INSERT INTO plan_features(plan_id,feature) VALUES(?,?)", (cur.lastrowid, feature))

    for c in load("claims"):
        sid = source_id(c["source_url"].replace("https://q-parser.ru", ""))
        conn.execute(
            "INSERT INTO claims(subject,predicate,object,value,unit,source_id,confidence,observed_at,note) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (c["subject"], c["predicate"], c["object"], str(c["value"]), c["unit"], sid,
             c["confidence"], c["observed_at"], c.get("note", "")),
        )

    conn.commit()
    return conn


def build_graph(conn: sqlite3.Connection) -> dict:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def node(nid: str, ntype: str, label: str, source_id: int | None = None):
        nodes.setdefault(nid, {"id": nid, "type": ntype, "label": label, "source_id": source_id})

    def edge(src: str, rel: str, dst: str, confidence="measured", source_id=None):
        edges.append({"source": src, "target": dst, "relation": rel,
                      "confidence": confidence, "source_id": source_id})

    for sid, path, title in conn.execute("SELECT id,path,title FROM sources"):
        node(f"page:{path}", "page", title or path, sid)

    for eid, method, path, summary in conn.execute("SELECT id,method,path,summary FROM endpoints"):
        nid = f"endpoint:{method} {path}"
        node(nid, "endpoint", f"{method} {path}", api_sid(conn))
        edge(f"page:/howto/api", "DOCUMENTS", nid)
        parts = [p for p in path.split("/") if p and p not in ("api", "v1")]
        for part in parts[:3]:
            if ":" in part:
                continue
            cid = f"concept:{part}"
            node(cid, "concept", part)
            edge(nid, "OPERATES_ON", cid)

    for fid, slug, title, target, category in conn.execute(
        "SELECT id,slug,title,target,category FROM formats"
    ):
        nid = f"format:{slug}"
        node(nid, "format", title, None)
        edge(f"page:/howto/format/{slug}", "DOCUMENTS", nid)
        if target:
            tid = f"platform:{target.lower()}"
            node(tid, "platform", target)
            edge(nid, "EXPORTS_TO", tid)
        cid = f"category:{category}"
        node(cid, "concept", category)
        edge(nid, "IN_CATEGORY", cid)

    for pid, name, price, period, parallel, aip in conn.execute(
        "SELECT id,name,price_rub,period,parallel_downloads,ai_points FROM plans"
    ):
        nid = f"plan:{name}"
        node(nid, "plan", f"{name} ({price} RUB/{period})", None)
        edge("page:/tariffs", "DOCUMENTS", nid)
        if parallel is not None:
            lid = f"limit:parallel_downloads={parallel}"
            node(lid, "limit", f"{parallel} parallel downloads")
            edge(nid, "LIMITS", lid)
        if aip is not None:
            aid = f"limit:ai_points={aip}"
            node(aid, "limit", f"{aip} AI Points")
            edge(nid, "INCLUDES", aid)

    for cid, subject, predicate, obj, value, unit, confidence, src in conn.execute(
        "SELECT id,subject,predicate,object,value,unit,confidence,source_id FROM claims"
    ):
        nid = f"claim:{cid}"
        node(nid, "claim", f"{subject} {predicate} {obj}", src)
        node(f"entity:{subject}", "entity", subject)
        edge(f"entity:{subject}", "HAS_CLAIM", nid, confidence, src)
        if src:
            row = conn.execute("SELECT path FROM sources WHERE id=?", (src,)).fetchone()
            if row:
                edge(nid, "EVIDENCED_BY", f"page:{row[0]}", confidence, src)

    for edge_item in edges:
        conn.execute(
            "INSERT INTO edges(source,relation,target,confidence,source_id) VALUES(?,?,?,?,?)",
            (edge_item["source"], edge_item["relation"], edge_item["target"],
             edge_item["confidence"], edge_item["source_id"]),
        )
    conn.commit()
    return {"nodes": list(nodes.values()), "edges": edges}


def api_sid(conn: sqlite3.Connection) -> int | None:
    row = conn.execute("SELECT id FROM sources WHERE path='/howto/api'").fetchone()
    return row[0] if row else None


def write_graphml(graph: dict) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="type" for="node" attr.name="type" attr.type="string"/>',
        '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
        '  <key id="relation" for="edge" attr.name="relation" attr.type="string"/>',
        '  <graph id="qparser" edgedefault="directed">',
    ]
    for n in graph["nodes"]:
        lines.append(f'    <node id="{escape(n["id"])}"><data key="type">{escape(n["type"])}</data>'
                     f'<data key="label">{escape(n["label"])}</data></node>')
    for i, e in enumerate(graph["edges"]):
        lines.append(f'    <edge id="e{i}" source="{escape(e["source"])}" target="{escape(e["target"])}">'
                     f'<data key="relation">{escape(e["relation"])}</data></edge>')
    lines += ["  </graph>", "</graphml>"]
    (DATA / "qparser.graphml").write_text("\n".join(lines), encoding="utf-8")


def build_wiki(conn: sqlite3.Connection) -> None:
    pages = conn.execute("SELECT id,url,path,title,section,kind,chars FROM sources ORDER BY path").fetchall()
    endpoints = conn.execute("SELECT method,path,summary,request,response FROM endpoints ORDER BY path").fetchall()
    formats = conn.execute("SELECT slug,title,target,category FROM formats ORDER BY category,slug").fetchall()
    plans = conn.execute("SELECT name,price_rub,period,parallel_downloads,ai_points FROM plans").fetchall()
    claims = conn.execute(
        "SELECT c.subject,c.predicate,c.object,c.value,c.unit,c.confidence,s.url "
        "FROM claims c LEFT JOIN sources s ON s.id=c.source_id ORDER BY c.id"
    ).fetchall()

    # ---------- index ----------
    body = [
        "# Q-Parser Knowledge Base",
        "",
        "128 страниц документации Q-Parser, 16 REST-эндпоинтов, 72 формата выгрузки и 4 тарифа. "
        "Корпус собран 22.11.2026: 0 пропусков, 442 579 символов; каждый факт имеет URL-источник и дату.",
        "",
        "| Артефакт | Значение | Источник |",
        "|---|---|---|",
        "| API-эндпоинты | 16 | https://q-parser.ru/howto/api |",
        "| Форматы выгрузки | 72 | https://q-parser.ru/howto/format |",
        "| Тарифы | 4 | https://q-parser.ru/tariffs |",
        "",
        f"**Corpus:** {len(pages)} pages · **API endpoints:** {len(endpoints)} · "
        f"**Export formats:** {len(formats)} · **Tariff plans:** {len(plans)} · **Claims:** {len(claims)}",
        "",
        "This wiki is generated from the fetched corpus. Every page has a source URL and a SHA-256",
        "in `docs/research/qparser/manifest.jsonl`. Facts are labelled `measured`, `reported` or `inferred`.",
        "",
        "## Start here",
        "",
        "- [[topics/api]] — the complete REST contract (16 methods).",
        "- [[topics/limits-and-quotas]] — concurrency, pagination, trial limits.",
        "- [[topics/formats]] — all 72 export formats by category.",
        "- [[topics/pricing]] — Day / Lite / Pro / Trial.",
        "- [[topics/webhooks]] — signed automation callbacks.",
        "- [[topics/modifiers]] — product and image transforms before export.",
        "- [[topics/ai]] — AI editing, image generation, watermark removal, AI Points.",
        "- [[topics/storage]] — FTP/SFTP/S3 delivery.",
        "",
        "## Indexes",
        "",
        "- [[indexes/by-endpoint]]",
        "- [[indexes/by-format]]",
        "- [[indexes/by-platform]]",
        "- [[indexes/by-marketplace]]",
        "- [[indexes/claims]]",
        "- [[indexes/sources]]",
        "",
        "## Machine-readable artefacts",
        "",
        "- `data/qparser.sqlite` — sources, pages, chunks, endpoints, formats, plans, claims, edges + FTS5.",
        "- `data/qparser.graph.json` — nodes and edges with provenance.",
        "- `data/qparser.graphml` — the same graph for Gephi / yEd.",
        "- `docs/research/qparser/extracted/` — raw structured JSON.",
        "",
        "## Research tracks",
        "",
        "- [[research/index]] — all research tracks, records and gaps.",
        "- [[research/inherited-assets]] — reusable projects and license policy.",
        "- [[indexes/marketplaces-world]] — world coverage map with status and priority.",
        "- [[research/adr]] — architecture decisions.",
        "- [[topics/aeo]] — Answer-First contract for AI search ranking.",
        "",
        "## Research tracks (raw)",
        "",
        "- `docs/research/competitors/` — direct and adjacent competitors.",
        "- `docs/research/marketplaces/` — RU / CN / global sales channels.",
        "- `docs/research/platforms/` — storefront platform comparison.",
        "- `docs/research/demand/` — demand, keyword and niche research.",
    ]
    write_wiki(WIKI / "index.md", {
        "id": "index", "title": "Q-Parser Knowledge Base", "tags": ["qparser", "index"],
        "sources": ["https://q-parser.ru/howto/api"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(body))

    # ---------- API topic ----------
    api_body = [
        "# Q-Parser REST API",
        "",
        "16 REST-методов по адресу https://q-parser.ru/api/v1. Авторизация через `Authorization: Bearer` "
        "или `X-Api-Key`, ошибки `{error:{code,message}}`, даты в unix ms; лимит 1000 записей на страницу.",
        "",
        "Base URL `https://q-parser.ru/api/v1`. Auth: `Authorization: Bearer <key>` or `X-Api-Key: <key>`.",
        "Errors: `{ \"error\": { \"code\": \"...\", \"message\": \"...\" } }`; dates are unix milliseconds.",
        "Source: [[sources]] · `https://q-parser.ru/howto/api`.",
        "",
        "| # | Method | Path | Purpose |",
        "|---|---|---|---|",
    ]
    for i, (method, path, summary, _, _) in enumerate(endpoints, 1):
        api_body.append(f"| {i} | `{method}` | `{path}` | {summary.replace('|', '/')} |")
    api_body.append("")
    for method, path, summary, request, response in endpoints:
        api_body += [f"## {method} {path}", "", summary, ""]
        if request:
            api_body += ["#### Request", "", request, ""]
        if response:
            api_body += ["#### Response", "", response, ""]
    write_wiki(WIKI / "topics" / "api.md", {
        "id": "api", "title": "Q-Parser REST API", "tags": ["qparser", "api", "rest"],
        "sources": ["https://q-parser.ru/howto/api"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(api_body))

    # ---------- formats ----------
    fmt_body = [
        "# Export formats",
        "",
        f"{len(formats)} formats are documented. A format is a contract: target platform, file shape,",
        "settings, and field mapping. The storefront pipeline must treat each format as a versioned adapter.",
        "",
        "| Category | Count | What it is for |",
        "|---|---|---|",
        "| file | 5 | Universal CSV / XLS / JSON / XML / YML |",
        "| cms | 36 | Direct import into a shop engine |",
        "| social | 8 | VK, OK, Facebook, Google Merchant, showcase |",
        "| marketplace | 5 | YML/XML feeds for marketplaces |",
        "| sp | 16 | Group-buying platforms |",
        "| commerce | 2 | CommerceML / MoySklad |",
        "",
        "## File formats",
        "",
    ]
    for category in ["file", "marketplace", "commerce", "cms", "social", "sp", "other"]:
        rows = [f for f in formats if f[3] == category]
        if not rows:
            continue
        fmt_body += [f"### {category}", "", "| Format | Target | Source |", "|---|---|---|"]
        for slug, title, target, cat in rows:
            fmt_body.append(f"| [[topics/formats/{slug}\\|{title}]] | {target} | {cat} |")
        fmt_body.append("")
    write_wiki(WIKI / "topics" / "formats.md", {
        "id": "formats", "title": "Export formats", "tags": ["qparser", "formats", "export"],
        "sources": ["https://q-parser.ru/howto/format"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(fmt_body))

    for slug, title, target, category in formats:
        source_path = f"/howto/format/{slug}"
        row = conn.execute("SELECT body FROM pages WHERE source_id=(SELECT id FROM sources WHERE path=?)",
                           (source_path,)).fetchone()
        raw = row[0] if row else ""
        # drop the generated frontmatter and the trailing nav if present
        raw = raw.split("Навигация по базе знаний")[0].strip()
        terms = [r[0] for r in conn.execute(
            "SELECT term FROM format_terms WHERE format_id=(SELECT id FROM formats WHERE slug=?)", (slug,))]
        page_body = [
            f"# {title}",
            "",
            f"**Category:** `{category}` · **Target:** {target}",
            f"**Source:** https://q-parser.ru{source_path}",
            "",
            raw,
            "",
            "## Extracted settings",
            "",
        ]
        page_body += [f"- {t}" for t in terms] or ["- (no bold settings detected)"]
        page_body += [
            "",
            "## Pipeline note",
            "",
            "Treat this as an adapter contract, not as a file dump. Required fields, enum values and",
            "media rules must be validated against the target platform before publishing.",
        ]
        write_wiki(WIKI / "topics" / "formats" / f"{slug}.md", {
            "id": f"format-{slug}", "title": title, "tags": ["qparser", "format", category],
            "sources": [f"https://q-parser.ru{source_path}"], "confidence": "measured", "updated": TODAY,
        }, "\n".join(page_body))

    # ---------- pricing ----------
    price_body = [
        "# Pricing and limits",
        "",
        "Четыре тарифа Q-Parser: Trial 0 ₽, Day 295 ₽/сутки, Lite 995 ₽/мес, Pro 2495 ₽/мес. "
        "Параллельных загрузок 1 / 3 / 10 / 20; AI Points 10 / 100 / 10 000. Данные измерены 22.11.2026.",
        "",
        "Source: https://q-parser.ru/tariffs (measured 2026-11-22).",
        "",
        "| Plan | Price | Parallel downloads | AI Points |",
        "|---|---|---|---|",
    ]
    for name, price, period, parallel, aip in plans:
        price_body.append(f"| {name} | {price} ₽/{period} | {parallel} | {aip if aip is not None else '—'} |")
    price_body += [
        "",
        "## What is included in every plan",
        "",
        "- Parsing of the whole site catalogue (no per-site limit).",
        "- Export to every supported file format and social network.",
        "- Parsing and export continue even if the plan expires mid-run.",
        "- Already parsed goods remain exportable after the plan expires.",
        "",
        "## Trial",
        "",
        "- Free sites can be parsed without a plan.",
        "- Paid sites: trial parsing is limited to 50 goods.",
        "- One parallel download.",
        "",
        "## AI Points",
        "",
        "- Included AIP do not roll over; purchased AIP do.",
        "- AI editing pauses for 12 hours if the balance hits zero, then cancels.",
        "- AIP can go negative; the debt is deducted on the next top-up.",
    ]
    write_wiki(WIKI / "topics" / "pricing.md", {
        "id": "pricing", "title": "Pricing and limits", "tags": ["qparser", "pricing", "limits"],
        "sources": ["https://q-parser.ru/tariffs"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(price_body))

    # ---------- limits ----------
    limit_body = [
        "# Limits and quotas",
        "",
        "Источник: https://q-parser.ru/howto/api. Измерено 22.11.2026.",
        "",
        "These are hard constraints the ingestion pipeline must respect. Values are measured from the API page.",
        "",
        "| Constraint | Value | Consequence |",
        "|---|---|---|",
        "| Concurrent unfinished parsings | 100 | `POST /parser` returns `unprocessable` above it |",
        "| Concurrent unfinished exports | 100 | `POST /export` returns `unprocessable` above it |",
        "| Page size (`/catalog`, `/parser/list`, `/goods`) | max 1000 | paginate, do not assume one page |",
        "| Trial parsing | 50 goods | cannot be used for a full catalogue |",
        "| Parallel downloads per plan | 1 / 3 / 10 / 20 | planner must cap jobs per tenant |",
        "| Webhook addresses per automation | 5 | shard by event type if more are needed |",
        "| Webhook response timeout | 10 s | acknowledge fast, process asynchronously |",
        "| Webhook retries | 1, 5, 10, 30, 60 s | deduplicate with `X-QParser-Delivery` |",
        "",
        "## Missing webhook for parser completion",
        "",
        "The API documents webhooks only for `automata.finished`. A one-off `POST /parser` has no callback.",
        "Therefore the ingestion service must poll `GET /parser/:id` with exponential backoff and persist",
        "`status`, `goods_processed`, `categories_processed` and `error` on every poll.",
        "",
        "## Archive behaviour",
        "",
        "Archived parsings have no goods (`GET /parser/:id/goods` returns `unprocessable`).",
        "Archive state must be recorded at ingest time, otherwise a re-export silently loses the catalogue.",
    ]
    write_wiki(WIKI / "topics" / "limits-and-quotas.md", {
        "id": "limits-and-quotas", "title": "Limits and quotas", "tags": ["qparser", "limits", "api"],
        "sources": ["https://q-parser.ru/howto/api"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(limit_body))

    # ---------- webhooks ----------
    wh = conn.execute("SELECT body FROM pages WHERE source_id=(SELECT id FROM sources WHERE path='/howto/automata/webhooks')").fetchone()
    write_wiki(WIKI / "topics" / "webhooks.md", {
        "id": "webhooks", "title": "Automation webhooks", "tags": ["qparser", "webhooks", "hmac"],
        "sources": ["https://q-parser.ru/howto/automata/webhooks"], "confidence": "measured", "updated": TODAY,
    }, "# Automation webhooks\n\n" + (wh[0] if wh else ""))

    # ---------- modifiers / ai / storage ----------
    for topic, path, title, tags in [
        ("modifiers", "/howto/mods", "Product and image modifiers", ["qparser", "mods", "pipeline"]),
        ("ai", "/howto/ai", "AI capabilities", ["qparser", "ai"]),
        ("storage", "/howto/filestorage", "File storage delivery", ["qparser", "storage", "s3", "ftp"]),
        ("catalog", "/catalog", "Site catalogue", ["qparser", "catalog"]),
        ("automata", "/howto/automata", "Scheduled parsing and export", ["qparser", "automata", "schedule"]),
    ]:
        row = conn.execute("SELECT body FROM pages WHERE source_id=(SELECT id FROM sources WHERE path=?)", (path,)).fetchone()
        write_wiki(WIKI / "topics" / f"{topic}.md", {
            "id": topic, "title": title, "tags": tags,
            "sources": [f"https://q-parser.ru{path}"], "confidence": "measured", "updated": TODAY,
        }, f"# {title}\n\n" + (row[0] if row else ""))

    aeo_source = ROOT / "docs" / "architecture" / "04-answer-first-aeo.md"
    if aeo_source.exists():
        write_wiki(WIKI / "topics" / "aeo.md", {
            "id": "aeo", "title": "Answer-First / AEO", "tags": ["aeo", "seo", "content"],
            "sources": ["docs/architecture/04-answer-first-aeo.md"],
            "confidence": "mixed", "updated": TODAY,
        }, aeo_source.read_text(encoding="utf-8"))

    # ---------- indexes ----------
    idx = ["# By endpoint", "", "| Method | Path | Purpose |", "|---|---|---|"]
    for method, path, summary, _, _ in endpoints:
        idx.append(f"| `{method}` | `{path}` | {summary.replace('|', '/')} |")
    write_wiki(WIKI / "indexes" / "by-endpoint.md", {
        "id": "by-endpoint", "title": "Index: by endpoint", "tags": ["index", "api"],
        "sources": ["https://q-parser.ru/howto/api"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))

    idx = ["# By format", "", "| Format | Category | Target |", "|---|---|---|"]
    for slug, title, target, category in formats:
        idx.append(f"| [[topics/formats/{slug}\\|{title}]] | {category} | {target} |")
    write_wiki(WIKI / "indexes" / "by-format.md", {
        "id": "by-format", "title": "Index: by format", "tags": ["index", "format"],
        "sources": ["https://q-parser.ru/howto/format"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))

    platforms: dict[str, list[str]] = {}
    for slug, title, target, category in formats:
        platforms.setdefault(target, []).append(f"[[topics/formats/{slug}\\|{title}]]")
    idx = ["# By platform", ""]
    for target, links in sorted(platforms.items()):
        idx += [f"## {target}", "", *[f"- {l}" for l in links], ""]
    write_wiki(WIKI / "indexes" / "by-platform.md", {
        "id": "by-platform", "title": "Index: by platform", "tags": ["index", "platform"],
        "sources": ["https://q-parser.ru/howto/format"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))

    marketplaces = [f for f in formats if f[3] in ("marketplace", "social")]
    idx = ["# By marketplace / channel", "", "| Channel | Format |", "|---|---|"]
    for slug, title, target, category in marketplaces:
        idx.append(f"| {target} | [[topics/formats/{slug}\\|{title}]] |")
    write_wiki(WIKI / "indexes" / "by-marketplace.md", {
        "id": "by-marketplace", "title": "Index: by marketplace", "tags": ["index", "marketplace"],
        "sources": ["https://q-parser.ru/howto/format"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))

    idx = ["# Claims", "", "| Subject | Predicate | Object | Value | Confidence | Source |", "|---|---|---|---|---|---|"]
    for subject, predicate, obj, value, unit, confidence, url in claims:
        idx.append(f"| {subject} | {predicate} | {obj} | {value} {unit or ''} | {confidence} | {url} |")
    write_wiki(WIKI / "indexes" / "claims.md", {
        "id": "claims", "title": "Index: claims", "tags": ["index", "claims", "evidence"],
        "sources": ["https://q-parser.ru/howto/api"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))

    idx = ["# Sources", "", "| Path | Title | HTTP | Chars |", "|---|---|---|---|"]
    for _, url, path, title, section, kind, chars in pages:
        idx.append(f"| `{path}` | {title} | {url} | {chars} |")
    write_wiki(WIKI / "indexes" / "sources.md", {
        "id": "sources", "title": "Index: sources", "tags": ["index", "sources", "provenance"],
        "sources": ["https://q-parser.ru"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(idx))


def main() -> int:
    conn = build_db()
    graph = build_graph(conn)
    (DATA / "qparser.graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    write_graphml(graph)
    build_wiki(conn)

    counts = {
        "sources": conn.execute("SELECT count(*) FROM sources").fetchone()[0],
        "chunks": conn.execute("SELECT count(*) FROM chunks").fetchone()[0],
        "endpoints": conn.execute("SELECT count(*) FROM endpoints").fetchone()[0],
        "formats": conn.execute("SELECT count(*) FROM formats").fetchone()[0],
        "plans": conn.execute("SELECT count(*) FROM plans").fetchone()[0],
        "claims": conn.execute("SELECT count(*) FROM claims").fetchone()[0],
        "nodes": len(graph["nodes"]),
        "edges": len(graph["edges"]),
    }
    conn.close()
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
