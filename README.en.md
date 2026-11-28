# TovarFlow

A catalogue-to-channel platform built on [Q-Parser](https://q-parser.ru). It ingests supplier
catalogues, normalises them into a canonical product model, prices them with a margin ledger,
publishes them to owned storefronts and marketplace channels, and syncs price, stock, orders and
returns.

The first market is RU (Ozon, Wildberries, Yandex Market). China and global channels are separate
layers, designed but not built. The storefront platform is **Medusa v2 + Next.js** (ADR-0006).

**Site:** https://tovarflow.rvcdax.workers.dev/ · **Russian README:** [README.md](README.md)

## Status

| Layer | State |
|---|---|
| Q-Parser corpus | 128/128 pages, 442k characters, 100% coverage |
| Structured extraction | 16 endpoints, 72 formats, 4 plans, 15 sourced claims |
| Knowledge base | SQLite + FTS5 (826 chunks), graph 434 nodes / 477 edges, LLM wiki |
| Research | competitors, RU, CN, global, platforms, demand, WordPress, admin complete |
| AEO | Answer-First contract, chunk/table/citation rules, `aeo_lint` gate |
| First slice | 100 goods ingested, canonical replay verified, margin ledger, valid YML feed |
| Site | RU + EN static site on Cloudflare Workers with `llms.txt`, sitemap, `.md` twins |
| Admin | hybrid decision: Medusa Admin + Next.js/Refine |
| Code | foundation tools and prototype; production services not started |

## Where to put the Q-Parser API key

```bash
copy .env.example .env
```

Set `QPARSER_API_KEY` in `.env` to the value from `https://q-parser.ru/my/profile`. `.env` is
gitignored; the client sends the key only in `Authorization: Bearer` and never logs it. Without a
key, use `--mock` or `USE_MOCK=1` — a local emulator covers the same API.

## Quick start

```bash
python tools/fetch_corpus.py            # incremental
python tools/extract_qparser.py
python tools/build_knowledge.py
python tools/verify_coverage.py
python tools/build_research_db.py
python tools/query_kb.py "webhook signature"
python tools/query_research.py "WB token"
python tools/mock_qparser.py --port 8765
python tools/smoke_mock.py
python tools/catalog_dump.py --mock        # full site catalogue to JSON/CSV
python tools/ingest.py --domain demo-home.ru --mock --limit 100
python tools/margin.py
python tools/feed_yml.py
python tools/replay.py --domain demo-home.ru
python tools/aeo_lint.py --html site/index.html
python tools/health.py --full
python tools/admin.py --port 8878           # operator dashboard prototype
python tools/test_admin.py --port 8878      # smoke: mapping + approval idempotency
python tools/executor.py                    # execute approved proposals, verify by read-back
```

Requirements: Python 3.12, `requests`, `beautifulsoup4`, `markdownify`.

## Product thesis

Q-Parser is a supply source, not a sales channel. It has no direct Ozon/WB/Amazon connectors. The
gap between "parsed" and "sold" is normalisation, pricing, category mapping and channel APIs. That
gap is the product.

Three layers are deliberately separate:

1. **Supply** — Q-Parser, 1688, supplier feeds. Raw capture, no storefront knowledge.
2. **Catalog Hub** — canonical products, variants, offers, margin ledger, media, identity candidates.
3. **Channels** — RU/CN/global adapters, each a capability profile plus a thin adapter. Every write
   goes through Proposal → Policy → Execution → Verification.

## Key decisions

- **Medusa v2** (MIT) + Next.js, Cloud Pro for the MVP, self-host at scale.
- **RU first**, because the Q-Parser catalogue and the Ozon/WB specs are RU-centric.
- **China is supply-first**; Ozon Global / WB China are blocked until a Chinese entity exists.
- **Global first** is Google Merchant Center, then Bol.com/Walmart, not Amazon.
- **WordPress:** separate installs + MainWP, not Multisite for independent WooCommerce shops;
  `wc/v3` REST with Application Passwords and an outbox; MCP is for AI admin, not bulk sync.
- **Admin:** hybrid Medusa Admin (commerce) + Next.js/Refine (platform operations), shared RLS.
- **AEO:** Answer-First lead in the first 150–300 characters, fact-dense tables, primary sources,
  consistent entity fields, raw-HTML gate.
- **No auto-merge** of supplier products; identity matches are candidates.
- **No publish without a content right.**
- **No deletion without double human confirmation.**

## Roadmap

See [ROADMAP.md](ROADMAP.md). Next milestone: ingest a live domain with a real key, ship the
Medusa + Next.js storefront MVP with AEO templates, then Ozon/WB L2 and WordPress sync v1.
