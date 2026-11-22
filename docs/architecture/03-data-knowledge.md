# Data and knowledge layer

> Status: implemented for the Q-Parser corpus; the research tracks will add more atoms.

## 1. Storage tiers

| Tier | Store | Content | Lifetime |
|---|---|---|---|
| Raw | `docs/research/qparser/raw/` | Verbatim HTML per URL | Immutable |
| Clean | `docs/research/qparser/pages/` | Markdown + source frontmatter | Regenerated from raw |
| Structured | `docs/research/qparser/extracted/` | endpoints, formats, plans, claims, stats | Regenerated |
| Query | `data/qparser.sqlite` | sources, chunks, FTS5, entities, edges | Rebuildable |
| Graph | `data/qparser.graph.json`, `.graphml` | nodes and edges with provenance | Rebuildable |
| Wiki | `wiki/` | LLM-readable pages with backlinks and indexes | Rebuildable |
| Runtime | PostgreSQL 16 | tenants, catalogue, listings, orders, proposals | System of record |
| Objects | S3-compatible | raw payloads, images, exports, evidence | Immutable per hash |

The rule: **the SQLite corpus is a research artefact, not the runtime database**. The runtime
system of record is PostgreSQL. This keeps research reproducible without putting 4 MB marketplace
schemas into the hot path.

## 2. Provenance contract

Every durable claim has:

```yaml
subject: q-parser-api
predicate: concurrency_limit
object: parsings
value: 100
unit: jobs
source_url: https://q-parser.ru/howto/api
observed_at: 2026-11-22
confidence: measured   # measured | reported | inferred | unverified
```

Rules:

1. A fact without a source URL is `unverified`, not `verified`.
2. `measured` means we observed it directly at the source on `observed_at`.
3. `reported` means a third party said it and we have not reproduced it.
4. `inferred` means we derived it; the derivation must be written in `note`.
5. Numbers are stored as text plus `unit`; comparisons are done by typed views, not string sort.
6. If a source disappears, the claim stays with its last observation and a `stale` flag.

## 3. Atomised wiki contract

Adopted from `C:\susa ai\china auto\wiki\SCHEMA.md`. One file = one idea.

| Layer | Holds | Example |
|---|---|---|
| `concept` | A durable domain or market fact | `concept.pricing.landed-cost` |
| `source` | A data source, site or dataset | `source.qparser.api` |
| `finding` | A conclusion from research | `finding.ozon.moderation-gate` |
| `question` | Something unresolved + the test that resolves it | `question.wb.rate-limits` |

Frontmatter:

```yaml
id: finding.ozon.moderation-gate
title: Ozon publishes cards only after moderation
layer: finding
status: verified              # draft | verified | contested | refuted
confidence: 0.85              # 0..1, honest probability
summary: One sentence an LLM can load alone.
tags: [ozon, moderation, connectors]
sources: [https://docs.ozon.ru/...]
depends_on: [concept.listing.state-machine]
see_also: [finding.wb.card-quarantine]
origin: research-ru-marketplaces
reviewed: 2026-11-22
resolves_when: null            # required only for questions
```

Status semantics:

- `draft` — plausible, unchecked. Never use as a premise.
- `verified` — observed directly, source URL present.
- `contested` — sources disagree; the disagreement is the finding.
- `refuted` — was believed, is wrong. **Keep the file**; say what disproved it.
- `unverified` — no source; cannot be used in a spec.

## 4. Graph schema

Node types:

`tenant`, `storefront`, `supplier`, `source`, `parse_run`, `product`, `variant`, `offer`,
`listing`, `channel`, `account`, `category`, `attribute`, `price_observation`, `order`,
`proposal`, `policy_decision`, `execution`, `verification`, `claim`, `page`, `endpoint`,
`format`, `plan`, `platform`, `concept`, `competitor`.

Edge types:

`SUPPLIES`, `PARSED_FROM`, `VARIANT_OF`, `OFFER_OF`, `PUBLISHED_AS`, `ON_CHANNEL`,
`MAPPED_TO`, `PRICED_BY`, `EVIDENCED_BY`, `DOCUMENTS`, `EXPORTS_TO`, `SUPPORTS`,
`REQUIRES`, `LIMITS`, `IN_CATEGORY`, `COMPETES_WITH`, `DEPENDS_ON`, `CONTRADICTS`,
`RESOLVED_BY`.

Every edge carries `confidence` and `source_id` (or `source_url`). The graph is queryable as JSON
and viewable in Gephi/yEd via GraphML.

## 5. Retrieval

Three complementary indexes:

1. **FTS5** over 826 chunks with the source path and heading. Query:
   `python tools/query_kb.py "webhook signature"`.
2. **Graph traversal** for relationship questions:
   "which formats target Shopify", "which claims depend on the API page".
3. **Vector** (optional, later) for semantic recall. `pgvector` in runtime; a JSONL or `sqlite-vec`
   index for research. Not a substitute for FTS when the exact term matters.

Chunk size is ~1400 characters, split at headings and paragraphs. Every chunk keeps its heading
and URL, so a retrieval result can always be traced to a page.

## 6. Wiki generation

`tools/build_knowledge.py` generates:

- `wiki/index.md` — hub.
- `wiki/topics/api.md` — 16 endpoints with request/response fields.
- `wiki/topics/formats.md` + `wiki/topics/formats/*.md` — 72 format contracts.
- `wiki/topics/pricing.md`, `limits-and-quotas.md`, `webhooks.md`, `modifiers.md`, `ai.md`,
  `storage.md`, `catalog.md`, `automata.md`.
- `wiki/indexes/by-endpoint.md`, `by-format.md`, `by-platform.md`, `by-marketplace.md`,
  `claims.md`, `sources.md`.

Every page has `id`, `title`, `tags`, `sources`, `confidence`, `updated`. Links use
`[[wikilinks]]`, so the folder opens directly in Obsidian.

## 7. Rebuild pipeline

```bash
python tools/fetch_corpus.py            # incremental; --force for full refetch
python tools/extract_qparser.py         # pages/endpoints/formats/plans/claims
python tools/build_knowledge.py         # SQLite + FTS5 + graph + wiki
python tools/verify_coverage.py         # manifest + coverage report
python tools/query_kb.py "webhook"      # query
```

Gates:

- `verify_coverage.py` exits non-zero if any canonical URL is missing.
- `build_knowledge.py` fails if a claim has no source.
- A schema-drift check compares the live API heading set with `extracted/endpoints.json`.

## 8. Research ingestion

Each research track writes:

```text
docs/research/<track>/
  REPORT.md      narrative, decisions, gaps
  data.json      machine-readable records with source_url + observed_at + confidence
  atoms/         optional: one concept/finding/question per file
```

The platform database will load `data.json` into a `research_records` table, and the graph builder
will add `finding` nodes and `EVIDENCED_BY` edges. This is how a competitor price becomes a
queryable fact instead of a paragraph nobody re-checks.

## 9. Deletion and versioning

- Raw captures and claims are never deleted.
- A refuted finding stays, with `status: refuted`.
- A superseded spec gets a new version; the old one stays for audit.
- Deleting a file requires explicit double confirmation from the owner. This rule applies to every
  agent, script and human working in this repository.
