---
id: "knowledge-graph"
title: "Knowledge graph"
tags:
  - graph
  - index
sources: []
confidence: "measured"
updated: "2026-11-27"
---

# Knowledge graph

**Nodes:** 435 · **Edges:** 477 · Generated: 2026-11-27

Merged from the Q-Parser corpus graph and the research graph. JSON and GraphML are in `data/`.

## Node types

| Type | Count |
|---|---|
| `page` | 128 |
| `format` | 72 |
| `platform` | 71 |
| `marketplace` | 68 |
| `concept` | 18 |
| `endpoint` | 16 |
| `claim` | 15 |
| `asset` | 14 |
| `research_track` | 10 |
| `limit` | 7 |
| `adr` | 6 |
| `plan` | 4 |
| `entity` | 3 |
| `layer` | 3 |

## Edge types

| Relation | Count |
|---|---|
| `CONTAINS` | 102 |
| `DOCUMENTS` | 92 |
| `EXPORTS_TO` | 72 |
| `IN_CATEGORY` | 72 |
| `IN_LAYER` | 68 |
| `OPERATES_ON` | 20 |
| `HAS_CLAIM` | 15 |
| `EVIDENCED_BY` | 15 |
| `REUSED_IN` | 14 |
| `LIMITS` | 4 |
| `INCLUDES` | 3 |

## Files

- `data/knowledge.graph.json` — machine-readable.
- `data/knowledge.graphml` — Gephi / yEd.
- `data/qparser.graph.json` — corpus only.
- `data/research.graph.json` — research only.

## Query examples

```bash
python -c "import json; g=json.load(open('data/knowledge.graph.json')); print([n for n in g['nodes'] if n['type']=='marketplace'][:5])"
```
