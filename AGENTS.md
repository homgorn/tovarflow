# AGENTS.md — operating rules for this repository

> Read this before touching anything. It applies to every agent, subagent, script and human.

## 1. What this project is

A catalogue-to-channel platform. It ingests supplier catalogues through Q-Parser, normalises them,
prices them with a margin ledger, publishes them to owned storefronts (Medusa v2 + Next.js) and to
marketplace channels (RU / CN / global), and syncs price, stock, orders and returns.

Start with:

- `ROADMAP.md` — horizons and exit criteria.
- `docs/architecture/00-overview.md` — boundaries.
- `docs/architecture/01-marketplace-layers.md` — RU/CN/global layers.
- `specs/000-constitution/constitution.md` — non-negotiable principles.
- `docs/backlog/tickets.md` — what to build next.

## 2. Hard rules

1. **Nothing is deleted without double confirmation from the owner.** Not a file, not a table, not
   a row of research. A refuted finding stays, marked `refuted`. A superseded spec gets a version.
2. **No secrets in the repository.** API keys, tokens and passwords live in a secret manager or an
   environment variable, never in a file that can be committed.
3. **No fabrication.** If a fact is not verified, write `unverified` and say what you tried. A
   number without a source is not a fact.
4. **Spec before code.** No implementation without a spec in `specs/`. A prototype is labelled as
   a prototype.
5. **External systems behind an adapter.** No Q-Parser, Ozon, WB or Amazon vocabulary in the core.
6. **All writes follow Proposal → Policy → Execution → Verification.** No direct marketplace write.
7. **No browser automation in autonomous paths.** Manual/supervised only, with an ADR.
8. **License discipline.** MIT/Apache-2.0/BSD may be used. GPL/AGPL/unlicensed require an ADR and
   legal review.
9. **Content rights before publishing.** No product or image without a `content_right` record.
10. **Tenant isolation from day one.** Every domain table has `tenant_id`; RLS is on.
11. **Work in chunks, driven by the todo list.** Read the backlog before starting; take one
    vertical slice at a time; close a todo only with an evidence artefact (test, report, feed,
    deployed URL). Report progress per chunk, not only at the end.

## 3. Evidence rules

Every durable claim carries:

```yaml
source_url: https://...
observed_at: 2026-11-22
confidence: measured | reported | inferred | unverified
```

- `measured` — read directly at the source today.
- `reported` — a third party said it; not reproduced.
- `inferred` — derived; the derivation is written down.
- `unverified` — no source; cannot be used as a premise.

Long reports are derivative. The retrieval surface is the atomised wiki: one `concept`, `source`,
`finding` or `question` per file, with `id`, `status`, `confidence`, `summary`, `tags`, `sources`,
`reviewed`. A `question` also has `resolves_when`.

## 4. Repository map

```text
ROADMAP.md                     horizons and exit criteria
docs/
  architecture/                overview, layers, domain model, data/knowledge
  adr/                         accepted decisions
  backlog/                     tracer-bullet tickets
  roadmap/                     world marketplaces coverage
  research/
    qparser/                   raw corpus, pages, extracted JSON, coverage
    competitors/               REPORT.md + data.json
    marketplaces/ru|c|global/  REPORT.md + data.json
    platforms/                 REPORT.md + data.json
    demand/                    REPORT.md + data.json
    inherited/                 reusable assets registry
  legal/                       rights, ToS, compliance (to be added)
specs/
  000-constitution/            the highest authority
  001-catalog-ingestion/       Q-Parser ingestion contract
  002-normalization/           canonical model, identity, pricing, media
  003-storefront/              Medusa v2 + Next.js behaviour
  004-marketplace-connectors/  RU/CN/global adapter contract
  005-ops/                     observability, reconciliation, backups
wiki/                          generated LLM wiki + indexes
data/
  qparser.sqlite               corpus + FTS5
  qparser.graph.json/.graphml  graph
  research.sqlite              research records + marketplaces + assets + FTS5
  research.graph.json          research graph
  inherited_assets.json        asset registry seed
tools/                         fetch, extract, build, query, verify
```

## 5. Commands

```bash
python tools/fetch_corpus.py            # incremental corpus fetch
python tools/fetch_corpus.py --force    # full refetch
python tools/extract_qparser.py         # structured extraction
python tools/build_knowledge.py         # SQLite + FTS5 + graph + wiki
python tools/verify_coverage.py         # coverage gate
python tools/query_kb.py "webhook"      # query the corpus
python tools/build_research_db.py       # research DB + graph + wiki
python tools/query_research.py "WB token"
python tools/mock_qparser.py --port 8765 # local Q-Parser API emulator
python tools/smoke_mock.py               # contract smoke test
python tools/merge_graphs.py             # combined knowledge graph
python tools/status.py                   # current counts
```

Create `.env` from `.env.example` and paste the key from `https://q-parser.ru/my/profile` into
`QPARSER_API_KEY`. `.env` is gitignored. Never send a key in chat. For local development use
`USE_MOCK=1` or `--mock` — no key and no paid plan needed.

```bash
python tools/qparser_client.py --domain demo-home.ru --mock
python tools/ingest.py --domain demo-home.ru --mock --limit 100
python tools/replay.py --domain demo-home.ru
python tools/aeo_lint.py
python tools/health.py --full
```

A change is not done until the relevant gate passes and the wiki is regenerated.

## 6. Research rules

- Official documentation and pricing pages first. A blog listicle is not a primary source.
- Every price cell has `source_url` and `observed_at`.
- A blocked page is marked `not verified`, never guessed.
- Separate `supply` from `sales` when researching a marketplace.
- For RU/CN/global, record entity requirements and ToS blockers before API details.
- Prefer atomised findings over a 30-page report; the report is the narrative, the atoms are the
  knowledge.

## 7. Definition of done

- The spec's acceptance criteria pass.
- A verifier exercises the real path, not a mock.
- Evidence is stored (test, report, screenshot, reconciliation output).
- The wiki and graph are updated.
- No rule above is violated, even if all tests pass.

## 8. Current state (2026-11-27)

Done: corpus 128/128, 16 endpoints, 72 formats, 4 plans, SQLite + FTS5, graph, wiki; architecture,
constitution, seven ADRs, roadmap, backlog; nine research tracks (competitors, RU, CN, global,
platforms, demand, WordPress, admin, inherited assets), synthesis, inherited-assets registry;
Answer-First/AEO contract and lint; Q-Parser client, mock API emulator and first vertical slice
(100 goods ingested, canonical replay verified).

Next: live Q-Parser key for a real domain; Medusa v2 + Next.js storefront MVP with AEO templates;
margin ledger; Ozon/WB adapters at L2; Google Merchant feed; WordPress sync v1.
