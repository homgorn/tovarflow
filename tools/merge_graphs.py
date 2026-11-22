"""Merge the corpus graph and the research graph into one knowledge graph.

Usage:
    python tools/merge_graphs.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
WIKI = ROOT / "wiki"

SOURCES = ["qparser.graph.json", "research.graph.json"]


def load(path: Path) -> dict:
    if not path.exists():
        return {"nodes": [], "edges": []}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    nodes: dict[str, dict] = {}
    edges: dict[tuple[str, str, str], dict] = {}

    for name in SOURCES:
        graph = load(DATA / name)
        for node in graph.get("nodes", []):
            nid = node.get("id")
            if not nid:
                continue
            nodes.setdefault(nid, node)
        for edge in graph.get("edges", []):
            key = (edge.get("source"), edge.get("relation"), edge.get("target"))
            if all(key):
                edges.setdefault(key, edge)

    merged = {"nodes": list(nodes.values()), "edges": list(edges.values())}
    (DATA / "knowledge.graph.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="type" for="node" attr.name="type" attr.type="string"/>',
        '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
        '  <key id="relation" for="edge" attr.name="relation" attr.type="string"/>',
        '  <graph id="knowledge" edgedefault="directed">',
    ]
    for n in merged["nodes"]:
        lines.append(
            f'    <node id="{escape(str(n["id"]))}"><data key="type">{escape(str(n.get("type", "")))}</data>'
            f'<data key="label">{escape(str(n.get("label", "")))}</data></node>'
        )
    for i, e in enumerate(merged["edges"]):
        lines.append(
            f'    <edge id="e{i}" source="{escape(str(e["source"]))}" target="{escape(str(e["target"]))}">'
            f'<data key="relation">{escape(str(e.get("relation", "")))}</data></edge>'
        )
    lines += ["  </graph>", "</graphml>"]
    (DATA / "knowledge.graphml").write_text("\n".join(lines), encoding="utf-8")

    type_counts = Counter(n.get("type", "unknown") for n in merged["nodes"])
    rel_counts = Counter(e.get("relation", "unknown") for e in merged["edges"])

    page = [
        "# Knowledge graph",
        "",
        f"**Nodes:** {len(merged['nodes'])} · **Edges:** {len(merged['edges'])} · "
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "Merged from the Q-Parser corpus graph and the research graph. JSON and GraphML are in `data/`.",
        "",
        "## Node types",
        "",
        "| Type | Count |",
        "|---|---|",
    ]
    for ntype, count in type_counts.most_common():
        page.append(f"| `{ntype}` | {count} |")
    page += ["", "## Edge types", "", "| Relation | Count |", "|---|---|"]
    for rel, count in rel_counts.most_common():
        page.append(f"| `{rel}` | {count} |")
    page += [
        "",
        "## Files",
        "",
        "- `data/knowledge.graph.json` — machine-readable.",
        "- `data/knowledge.graphml` — Gephi / yEd.",
        "- `data/qparser.graph.json` — corpus only.",
        "- `data/research.graph.json` — research only.",
        "",
        "## Query examples",
        "",
        "```bash",
        "python -c \"import json; g=json.load(open('data/knowledge.graph.json')); "
        "print([n for n in g['nodes'] if n['type']=='marketplace'][:5])\"",
        "```",
    ]
    (WIKI / "indexes" / "knowledge-graph.md").write_text(
        "---\nid: \"knowledge-graph\"\ntitle: \"Knowledge graph\"\ntags:\n  - graph\n  - index\n"
        "sources: []\nconfidence: \"measured\"\nupdated: \"" + datetime.now(timezone.utc).date().isoformat()
        + "\"\n---\n\n" + "\n".join(page) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "nodes": len(merged["nodes"]),
        "edges": len(merged["edges"]),
        "node_types": dict(type_counts),
        "edge_types": dict(rel_counts),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
