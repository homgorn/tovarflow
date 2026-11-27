"""Build the research knowledge base: SQLite + FTS5 + graph + wiki pages.

Run after the research tracks have produced REPORT.md / data.json:
    python tools/build_research_db.py

It is tolerant of missing tracks: whatever exists is indexed, the rest is listed as pending.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RESEARCH = DOCS / "research"
DATA = ROOT / "data"
WIKI = ROOT / "wiki"
DB_PATH = DATA / "research.sqlite"
TODAY = datetime.now(timezone.utc).date().isoformat()

TRACK_DIRS = [
    ("competitors", "competitors", "general"),
    ("marketplaces/ru", "marketplaces-ru", "ru"),
    ("marketplaces/cn", "marketplaces-cn", "cn"),
    ("marketplaces/global", "marketplaces-global", "global"),
    ("platforms", "platforms", "general"),
    ("demand", "demand", "general"),
    ("inherited", "inherited", "general"),
    ("wordpress", "wordpress", "global"),
    ("admin", "admin", "general"),
]

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS tracks (
  slug TEXT PRIMARY KEY, title TEXT, layer TEXT, report_path TEXT,
  data_path TEXT, generated_at TEXT, records INTEGER, status TEXT
);
CREATE TABLE IF NOT EXISTS records (
  id INTEGER PRIMARY KEY, track TEXT NOT NULL, layer TEXT, name TEXT,
  role TEXT, confidence TEXT, observed_at TEXT, docs_url TEXT, payload TEXT
);
CREATE TABLE IF NOT EXISTS marketplaces (
  id INTEGER PRIMARY KEY, name TEXT, region TEXT, layer TEXT, role TEXT,
  priority TEXT, status TEXT, notes TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS assets (
  id TEXT PRIMARY KEY, name TEXT, path TEXT, category TEXT, license TEXT,
  reuse TEXT, notes TEXT, confidence TEXT
);
CREATE TABLE IF NOT EXISTS adrs (
  id TEXT PRIMARY KEY, title TEXT, status TEXT, date TEXT, path TEXT
);
CREATE TABLE IF NOT EXISTS edges (
  id INTEGER PRIMARY KEY, source TEXT, relation TEXT, target TEXT, confidence TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS report_fts USING fts5(
  text, heading, track UNINDEXED, path UNINDEXED, tokenize='unicode61'
);
"""


def reset_db() -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB_PATH) + suffix)
        if p.exists():
            p.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn


def parse_marketplaces() -> list[dict]:
    path = DOCS / "roadmap" / "world-marketplaces.md"
    if not path.exists():
        return []
    rows, region = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            region = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] in ("Channel", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        name, reg, role, priority, status = cells[0], cells[1], cells[2], cells[3], cells[4]
        notes = " | ".join(cells[5:])
        if not name or name.startswith("---"):
            continue
        layer = "ru" if "RU" in region or "CIS" in region else (
            "cn" if "China" in region or "cross-border" in region else (
                "feeds" if "Feeds" in region else "global"))
        rows.append({
            "name": name, "region": reg, "layer": layer, "role": role,
            "priority": priority, "status": status.strip("`"), "notes": notes,
            "source": str(path.relative_to(ROOT)).replace("\\", "/"),
        })
    return rows


def parse_adrs() -> list[dict]:
    out = []
    for path in sorted((DOCS / "adr").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), path.stem)
        status = re.search(r"\*\*Status:\*\*\s*([a-zA-Z]+)", text)
        date = re.search(r"\*\*Date:\*\*\s*([0-9-]+)", text)
        out.append({
            "id": path.stem, "title": title,
            "status": status.group(1) if status else "unknown",
            "date": date.group(1) if date else None,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        })
    return out


def load_assets(conn: sqlite3.Connection) -> int:
    path = DATA / "inherited_assets.json"
    if not path.exists():
        return 0
    items = json.loads(path.read_text(encoding="utf-8"))
    for a in items:
        conn.execute(
            "INSERT OR REPLACE INTO assets(id,name,path,category,license,reuse,notes,confidence) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (a["id"], a["name"], a["path"], a["category"], a["license"], a["reuse"],
             a["notes"], a["confidence"]),
        )
        conn.execute("INSERT INTO edges(source,relation,target,confidence) VALUES(?,?,?,?)",
                     (a["id"], "REUSED_IN", "project:q-parser.ru", a["confidence"]))
    conn.commit()
    return len(items)


def record_list(payload) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("platforms", "vendors", "candidates", "sources", "records", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        return []
    return []


def load_tracks(conn: sqlite3.Connection) -> list[dict]:
    tracks = []
    for rel, slug, layer in TRACK_DIRS:
        folder = RESEARCH / rel
        if not folder.exists():
            tracks.append({"slug": slug, "title": slug, "layer": layer, "status": "pending",
                           "records": 0, "report": None, "data": None})
            continue
        report = folder / "REPORT.md"
        data = folder / "data.json"
        payload = json.loads(data.read_text(encoding="utf-8")) if data.exists() else None
        recs = record_list(payload) if payload is not None else []
        title = slug
        if report.exists():
            first = next((l[2:].strip() for l in report.read_text(encoding="utf-8").splitlines()
                          if l.startswith("# ")), slug)
            title = first
        for i, rec in enumerate(recs):
            name = (rec.get("platform") or rec.get("vendor") or rec.get("name")
                    or rec.get("candidate") or f"{slug}-{i}")
            docs = rec.get("docs_url") or rec.get("url") or rec.get("source_url")
            conn.execute(
                "INSERT INTO records(track,layer,name,role,confidence,observed_at,docs_url,payload) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (slug, layer, str(name), rec.get("role"), rec.get("confidence"),
                 rec.get("observed_at"), docs, json.dumps(rec, ensure_ascii=False)),
            )
            conn.execute("INSERT INTO edges(source,relation,target,confidence) VALUES(?,?,?,?)",
                         (f"track:{slug}", "CONTAINS", f"record:{slug}:{name}", rec.get("confidence")))
        generated = payload.get("generated_at") if isinstance(payload, dict) else None
        tracks.append({
            "slug": slug, "title": title, "layer": layer,
            "status": "complete" if report.exists() or data.exists() else "pending",
            "records": len(recs), "report": str(report.relative_to(ROOT)).replace("\\", "/") if report.exists() else None,
            "data": str(data.relative_to(ROOT)).replace("\\", "/") if data.exists() else None,
            "generated_at": generated,
        })
        if report.exists():
            text = report.read_text(encoding="utf-8")
            heading = ""
            buffer = []
            for line in text.splitlines():
                if re.match(r"^#{1,4}\s+", line):
                    if buffer:
                        conn.execute("INSERT INTO report_fts(text,heading,track,path) VALUES(?,?,?,?)",
                                     ("\n".join(buffer).strip(), heading, slug, tracks[-1]["report"]))
                        buffer = []
                    heading = re.sub(r"^#{1,4}\s+", "", line).strip()
                else:
                    buffer.append(line)
            if buffer:
                conn.execute("INSERT INTO report_fts(text,heading,track,path) VALUES(?,?,?,?)",
                             ("\n".join(buffer).strip(), heading, slug, tracks[-1]["report"]))
    conn.commit()
    return tracks


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


def build_wiki(conn: sqlite3.Connection, tracks: list[dict], marketplaces: list[dict],
               adrs: list[dict], assets: int) -> None:
    complete = [t for t in tracks if t["status"] == "complete"]
    body = [
        "# Research knowledge base",
        "",
        f"**Tracks complete:** {len(complete)}/{len(tracks)} · **Records:** "
        f"{conn.execute('SELECT count(*) FROM records').fetchone()[0]} · "
        f"**Marketplaces mapped:** {len(marketplaces)} · **Inherited assets:** {assets}",
        "",
        "Each track keeps a narrative `REPORT.md`, machine-readable `data.json` and a source/date on",
        "every fact. The SQLite file `data/research.sqlite` holds the same records plus FTS5.",
        "",
        "## Tracks",
        "",
        "| Track | Status | Records | Report | Data |",
        "|---|---|---|---|---|",
    ]
    for t in tracks:
        report = f"[REPORT](../../{t['report']})" if t["report"] else "—"
        data = f"[data.json](../../{t['data']})" if t["data"] else "—"
        body.append(f"| [[research/{t['slug']}\\|{t['title']}]] | {t['status']} | {t['records']} | {report} | {data} |")
    body += [
        "",
        "## Marketplaces",
        "",
        "- [[indexes/marketplaces-world]] — the full world coverage map with status and priority.",
        "",
        "## Synthesis",
        "",
        "- [SYNTHESIS.md](../../docs/research/SYNTHESIS.md) — cross-track decisions, gaps and build order.",
        "",
        "## Decisions and assets",
        "",
        "- [[research/inherited-assets]] — reusable projects and license policy.",
        "- [[research/adr]] — architecture decision records.",
        "",
        "## Query",
        "",
        "```bash",
        "python tools/query_research.py \"WB token scope\"",
        "python tools/query_research.py --sql \"select name,layer,role,status from marketplaces\"",
        "```",
    ]
    write_wiki(WIKI / "research" / "index.md", {
        "id": "research-index", "title": "Research knowledge base", "tags": ["research", "index"],
        "sources": [], "confidence": "measured", "updated": TODAY,
    }, "\n".join(body))

    for t in tracks:
        rows = conn.execute(
            "SELECT name,role,confidence,observed_at,docs_url FROM records WHERE track=? ORDER BY name",
            (t["slug"],),
        ).fetchall()
        page = [
            f"# {t['title']}",
            "",
            f"**Status:** {t['status']} · **Layer:** `{t['layer']}` · **Records:** {len(rows)}",
            "",
            f"Narrative: [{t['report']}](../../{t['report']})" if t["report"] else "Narrative: pending.",
            "",
        ]
        if rows:
            page += ["| Name | Role | Confidence | Observed | Docs |", "|---|---|---|---|---|"]
            for name, role, confidence, observed, docs in rows:
                link = f"[docs]({docs})" if docs else "—"
                page.append(f"| {name} | {role or '—'} | {confidence or '—'} | {observed or '—'} | {link} |")
        else:
            page.append("_No structured records yet._")
        page += [
            "",
            "## Method",
            "",
            "Official documentation and pricing pages first. Every fact is labelled `measured`,"
            " `reported` or `inferred`; a blocked page is marked `not verified`, never guessed.",
        ]
        write_wiki(WIKI / "research" / f"{t['slug']}.md", {
            "id": f"research-{t['slug']}", "title": t["title"], "tags": ["research", t["layer"]],
            "sources": [t["report"]] if t["report"] else [], "confidence": "mixed", "updated": TODAY,
        }, "\n".join(page))

    # inherited assets
    asset_rows = conn.execute(
        "SELECT name,path,category,license,reuse,notes FROM assets ORDER BY category,name"
    ).fetchall()
    page = ["# Inherited assets", "",
            "Existing projects on this machine that we reuse instead of rebuilding.", ""]
    for category in sorted({r[2] for r in asset_rows}):
        page += [f"## {category}", "", "| Asset | Path | License | Reuse | Notes |", "|---|---|---|---|---|"]
        for name, path, cat, lic, reuse, notes in asset_rows:
            if cat != category:
                continue
            page.append(f"| {name} | `{path}` | {lic} | {reuse} | {notes} |")
        page.append("")
    page += ["See [ASSETS.md](../../docs/research/inherited/ASSETS.md) for the full registry."]
    write_wiki(WIKI / "research" / "inherited-assets.md", {
        "id": "inherited-assets", "title": "Inherited assets", "tags": ["research", "assets", "reuse"],
        "sources": [], "confidence": "measured", "updated": TODAY,
    }, "\n".join(page))

    # ADR index
    page = ["# Architecture decision records", "", "| ADR | Status | Date |", "|---|---|---|"]
    for a in adrs:
        page.append(f"| [{a['title']}](../../{a['path']}) | {a['status']} | {a['date'] or '—'} |")
    write_wiki(WIKI / "research" / "adr.md", {
        "id": "adr", "title": "Architecture decision records", "tags": ["adr", "decisions"],
        "sources": [], "confidence": "measured", "updated": TODAY,
    }, "\n".join(page))

    # world marketplaces index
    page = ["# World marketplaces", "",
            f"{len(marketplaces)} channels mapped across RU/CIS, China, Europe, North America, LATAM,"
            " APAC, Middle East, Africa and Oceania.", "",
            "| Channel | Region | Role | Priority | Status |",
            "|---|---|---|---|---|"]
    for m in marketplaces:
        page.append(f"| {m['name']} | {m['region']} | {m['role']} | {m['priority']} | `{m['status']}` |")
    page += ["", "Source: [world-marketplaces.md](../../docs/roadmap/world-marketplaces.md).",
             "", "A channel is not done until L5 certification. See spec 004."]
    write_wiki(WIKI / "indexes" / "marketplaces-world.md", {
        "id": "marketplaces-world", "title": "World marketplaces", "tags": ["marketplaces", "index", "roadmap"],
        "sources": ["docs/roadmap/world-marketplaces.md"], "confidence": "measured", "updated": TODAY,
    }, "\n".join(page))


def build_graph(conn: sqlite3.Connection, tracks: list[dict], marketplaces: list[dict],
                adrs: list[dict]) -> dict:
    nodes, edges = {}, []
    for t in tracks:
        nodes[f"track:{t['slug']}"] = {"id": f"track:{t['slug']}", "type": "research_track",
                                       "label": t["title"]}
    for m in marketplaces:
        nid = f"marketplace:{m['layer']}:{m['name']}"
        nodes[nid] = {"id": nid, "type": "marketplace", "label": m["name"]}
        nodes[f"layer:{m['layer']}"] = {"id": f"layer:{m['layer']}", "type": "layer", "label": m["layer"]}
        edges.append({"source": nid, "relation": "IN_LAYER", "target": f"layer:{m['layer']}"})
    for a in adrs:
        nodes[f"adr:{a['id']}"] = {"id": f"adr:{a['id']}", "type": "adr", "label": a["title"]}
    for row in conn.execute("SELECT id,name,path,category,reuse FROM assets"):
        nodes[f"asset:{row[0]}"] = {"id": f"asset:{row[0]}", "type": "asset", "label": row[1]}
    for row in conn.execute("SELECT id,source,relation,target,confidence FROM edges"):
        edges.append({"source": row[1], "relation": row[2], "target": row[3],
                      "confidence": row[4]})
    return {"nodes": list(nodes.values()), "edges": edges}


def main() -> int:
    conn = reset_db()
    assets = load_assets(conn)
    marketplaces = parse_marketplaces()
    for m in marketplaces:
        conn.execute(
            "INSERT INTO marketplaces(name,region,layer,role,priority,status,notes,source) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (m["name"], m["region"], m["layer"], m["role"], m["priority"], m["status"],
             m["notes"], m["source"]),
        )
    adrs = parse_adrs()
    for a in adrs:
        conn.execute("INSERT OR REPLACE INTO adrs(id,title,status,date,path) VALUES(?,?,?,?,?)",
                     (a["id"], a["title"], a["status"], a["date"], a["path"]))
    tracks = load_tracks(conn)
    for t in tracks:
        conn.execute(
            "INSERT OR REPLACE INTO tracks(slug,title,layer,report_path,data_path,generated_at,records,status) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (t["slug"], t["title"], t["layer"], t["report"], t["data"],
             t.get("generated_at"), t["records"], t["status"]),
        )
    conn.commit()

    build_wiki(conn, tracks, marketplaces, adrs, assets)
    graph = build_graph(conn, tracks, marketplaces, adrs)
    (DATA / "research.graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2),
                                              encoding="utf-8")
    counts = {
        "tracks": conn.execute("SELECT count(*) FROM tracks").fetchone()[0],
        "records": conn.execute("SELECT count(*) FROM records").fetchone()[0],
        "marketplaces": conn.execute("SELECT count(*) FROM marketplaces").fetchone()[0],
        "assets": conn.execute("SELECT count(*) FROM assets").fetchone()[0],
        "adrs": conn.execute("SELECT count(*) FROM adrs").fetchone()[0],
        "nodes": len(graph["nodes"]),
        "edges": len(graph["edges"]),
    }
    conn.close()
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
