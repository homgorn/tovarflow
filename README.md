# Q-Parser → Storefront → Marketplaces

A catalogue-to-channel platform built on top of [Q-Parser](https://q-parser.ru). It ingests
supplier catalogues, normalises them into a canonical product model, prices them with a margin
ledger, publishes them to owned storefronts and marketplace channels, and syncs price, stock,
orders and returns.

The first market is RU (Ozon, Wildberries, Yandex Market). China and global channels are separate
layers, designed but not built. The storefront platform is **Medusa v2 + Next.js** (ADR-0006).

## Status

| Layer | State |
|---|---|
| Q-Parser corpus | 128/128 pages, 442k chars, 100% coverage |
| Structured extraction | 16 endpoints, 72 formats, 4 plans, 15 sourced claims |
| Knowledge base | SQLite + FTS5 (826 chunks), graph 334 nodes / 293 edges, LLM wiki |
| Research | competitors, RU, CN, global, platforms, demand complete; synthesis written |
| Architecture | layers, domain model, adapter contract, write path, data/knowledge |
| Specs | constitution + 5 specs + 6 ADRs |
| Code | not started; this repository is the foundation |

## Quick start

```bash
python tools/fetch_corpus.py            # incremental
python tools/extract_qparser.py
python tools/build_knowledge.py
python tools/verify_coverage.py
python tools/build_research_db.py
python tools/query_kb.py "webhook signature"
python tools/query_research.py "WB token"
```

Requirements: Python 3.12, `requests`, `beautifulsoup4`, `markdownify`.

## What is inside

```text
docs/architecture/     system boundaries, RU/CN/global layers, domain model, knowledge layer
docs/research/         corpus, competitors, marketplaces, platforms, demand, inherited assets
docs/adr/              decisions (layers, supply vs sales, write path, knowledge, rights, Medusa)
docs/backlog/          tracer-bullet tickets with dependencies
specs/                 constitution + ingestion, normalisation, storefront, connectors, ops
wiki/                  generated LLM wiki with indexes and backlinks
data/                  SQLite databases, graph JSON/GraphML, asset registry
tools/                 fetch, extract, build, query, verify
ROADMAP.md             horizons and exit criteria
AGENTS.md              operating rules for agents and humans
```

## The product thesis

Q-Parser is a supply source, not a sales channel. It has no direct Ozon/WB/Amazon connectors. The
gap between "parsed" and "sold" is normalisation, pricing, category mapping and channel APIs. That
gap is the product.

Three layers are deliberately separate:

1. **Supply** — Q-Parser, 1688, supplier feeds. Raw capture, no storefront knowledge.
2. **Catalog Hub** — canonical products, variants, offers, margin, media, identity candidates.
3. **Channels** — RU/CN/global adapters, each a capability profile plus a thin adapter. All writes
   go through Proposal → Policy → Execution → Verification.

## Key decisions

- **Medusa v2** (MIT) + Next.js, Cloud Pro for the MVP, self-host at scale.
- **RU first**, because the Q-Parser catalogue and the Ozon/WB specs are RU-centric.
- **China is supply-first**; Ozon Global / WB China are blocked until a Chinese entity exists.
- **Global first** is Google Merchant Center, then Bol.com/Walmart, not Amazon.
- **No auto-merge** of supplier products; identity matches are candidates.
- **No publish without a content right.**
- **No deletion without double human confirmation.**

## Roadmap

See [ROADMAP.md](ROADMAP.md). Next milestone: ingest one real domain end to end, build the margin
ledger, and ship a Medusa + Next.js storefront MVP with a valid YML feed.

## License

Proprietary. Reused open-source dependencies must be MIT/Apache-2.0/BSD; GPL/AGPL requires an ADR.
