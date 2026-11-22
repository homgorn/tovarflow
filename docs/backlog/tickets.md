# Backlog — tracer-bullet tickets

> A ticket is a vertical slice that ends in something observable, not a layer of plumbing.
> No ticket starts without a spec. Dependencies are explicit; parallel work is allowed only
> when the dependency graph allows it.
>
> Status: `done`, `ready`, `blocked`, `in-progress`.

## Foundation

### T01 — Corpus and coverage gate — `done`
Outcome: 128 canonical Q-Parser pages fetched, cleaned, hashed, and verified.
Acceptance: `tools/verify_coverage.py` reports 0 missing; manifest has HTTP status, SHA-256,
title and timestamp for every URL.
Evidence: `docs/research/qparser/COVERAGE.md`.

### T02 — Knowledge base and graph — `done`
Outcome: SQLite + FTS5, 826 chunks, 16 endpoints, 72 formats, 4 plans, 15 claims, graph
334 nodes / 293 edges, wiki with indexes.
Acceptance: `python tools/query_kb.py "webhook"` returns sourced chunks; `data/qparser.graph.json`
loads; wiki index links resolve.

### T03 — Architecture and constitution — `done`
Outcome: layer model (RU/CN/global/CIS), supply vs sales, adapter contract, domain model,
data/knowledge contract, roadmap, inherited-assets registry.
Acceptance: `docs/architecture/*.md`, `specs/000-constitution/constitution.md`,
`docs/research/inherited/ASSETS.md` exist and cross-link.

### T04 — Deep research ingestion — `ready`
Outcome: competitor, RU, CN, global, platform and demand reports loaded into the research DB and
graph.
Depends on: research subagents.
Acceptance: every `data.json` validates; every price/fact has `source_url` + `observed_at`;
`docs/research/<track>/REPORT.md` has a gaps section.

## H1 — Ingest and normalise

### T10 — Q-Parser API client — `ready`
Outcome: a typed client with auth, retries, pagination, polling and error mapping.
Depends on: T03.
Scope: 16 methods; only `catalog`, `website`, `categories`, `parser`, `parser/:id`,
`parser/:id/goods`, `format`, `export`, `export/:id` are needed for the first slice.
Acceptance: contract tests against recorded fixtures; 429/5xx backoff; `unprocessable` mapped;
no secret in logs; `idempotency` documented for every call.
Spec: `specs/001-catalog-ingestion/spec.md`.

### T11 — Ingest one domain end to end — `ready`
Outcome: categories → parse → goods → raw blobs → canonical products for one real domain.
Depends on: T10, T20.
Acceptance: 1,000 goods ingested; 0 lost pages; parse id replay produces the same output hash;
raw payload reference stored for every good.
Spec: `specs/001-catalog-ingestion/spec.md`.

### T12 — Canonical model and migrations — `ready`
Outcome: Postgres schema for product/variant/offer/media/attribute/category, tenant-scoped.
Depends on: T03.
Acceptance: migrations apply on a clean DB; RLS test passes; money is minor units + currency;
unknowns are NULL; `product_identity_match` candidates only.
Spec: `specs/002-normalization/spec.md`.

### T13 — Attribute mapping v1 — `ready`
Outcome: Q-Parser `data` keys → canonical attributes with a versioned dictionary.
Depends on: T11, T12.
Acceptance: top 100 `data` keys mapped; unmapped keys are recorded, never dropped; mapping
coverage report; a new key does not break ingestion.
Spec: `specs/002-normalization/spec.md`.

### T14 — Margin ledger v1 — `ready`
Outcome: a price is explained by purchase, delivery, duty, commission, returns, acquiring, tax
and target margin.
Depends on: T12.
Acceptance: a price can be recomputed from stored inputs; unknown components make the result
`incomplete`; a floor price is enforced by policy.
Spec: `specs/002-normalization/spec.md`.

### T15 — Media pipeline — `ready`
Outcome: images downloaded, hashed, resized, converted to WebP/AVIF, stored in S3, served via CDN.
Depends on: T12.
Acceptance: 0 broken images; dedupe by hash; original preserved; variant URLs stable; EXIF stripped.
Spec: `specs/002-normalization/spec.md`.

### T16 — Storefront MVP — `ready`
Outcome: catalogue, category page, product page, search, cart on the chosen platform.
Depends on: platform decision (T04), T12, T15.
Acceptance: 1,000 products render; LCP < 2.5 s on mobile; primary content in raw HTML; schema.org
Product; sitemap; `llms.txt` and `.md` twins.
Spec: `specs/003-storefront/spec.md`.

### T17 — YML feed and validator — `ready`
Outcome: a valid YML feed for Yandex Market and a validator in CI.
Depends on: T12, T14.
Acceptance: feed validates against the target schema; categories map; 0 missing required fields;
a broken product fails the build, not the marketplace.
Spec: `specs/004-marketplace-connectors/spec.md`.

## H2 — RU sales loop

### T20 — Adapter kernel — `ready`
Outcome: capability profile loader, rate limiter, idempotency store, raw capture, error taxonomy,
verification hook.
Depends on: T03.
Acceptance: two adapters can share the kernel without branching on platform; a repeated write
with the same key sends one HTTP request; raw payload is stored before mapping.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T21 — Ozon adapter L2 — `ready`
Outcome: read products, write price and stock, verify by re-read.
Depends on: T20, T14.
Acceptance: sandbox/fixtures; 20 methods covered by contract tests; price write idempotent;
verification mismatch opens an incident; auth expiry maps to `AuthError`.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T22 — Wildberries adapter L2 — `ready`
Outcome: category-scoped tokens, price and stock write, quarantine warning.
Depends on: T20, T14.
Acceptance: missing token → `EntitlementError` before HTTP; price drop > 3x produces a warning;
rate limiter respects stats limits; contract tests from the 13 local specs.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T23 — Listing state machine and moderation queue — `ready`
Outcome: draft → validated → submitted → moderation → live / rejected / paused.
Depends on: T21, T22.
Acceptance: every transition is an event; rejected cards carry a reason; operator can retry after
a fix; no silent overwrite of a live listing.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T24 — Order import and tracking push — `ready`
Outcome: orders from one channel normalised, acknowledged, shipped with tracking.
Depends on: T21 or T22.
Acceptance: order idempotency; status transitions match the channel; tracking push verified;
return reason codes stored.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T25 — Reconciliation — `ready`
Outcome: daily parsed vs published vs rejected vs sold vs settled report.
Depends on: T21–T24.
Acceptance: every delta has a reason code; unexplained deltas alert; report is reproducible.
Spec: `specs/005-ops/spec.md`.

## H4–H6

### T30 — China landed cost — `ready`
Outcome: purchase + CN delivery + export + international + duty + VAT + certification, with
unknowns explicit.
Depends on: T14, CN research.
Acceptance: 100 SKU sample complete; unknown components flagged; a rule change creates a new
version.
Spec: `specs/002-normalization/spec.md`.

### T31 — Translation pipeline — `ready`
Outcome: RU ↔ CN product content with glossary, review queue and versioning.
Depends on: T12.
Acceptance: no machine translation published without review; glossary terms enforced; original
preserved; per-locale content hash.
Spec: `specs/002-normalization/spec.md`.

### T32 — eBay adapter L2/L3 — `ready`
Outcome: OAuth2, listing publish, price/stock, orders.
Depends on: T20, global research.
Acceptance: sandbox listing created; price verified; order imported; contract tests.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T33 — Etsy adapter L2/L3 — `ready`
Outcome: OAuth2, listing publish, price/stock, orders.
Depends on: T20, global research.
Acceptance: app review checklist; listing published to a test shop; taxonomy mapping.
Spec: `specs/004-marketplace-connectors/spec.md`.

### T40 — Multi-tenant isolation — `ready`
Outcome: tenant_id on every table, RLS, tenant-scoped object paths and search.
Depends on: T12.
Acceptance: cross-tenant read test fails; object path traversal test fails; a second tenant can be
created without code changes.
Spec: `specs/003-storefront/spec.md`.

### T41 — Billing and plans — `ready`
Outcome: subscription, usage metering (SKU, channels, AI points), invoices.
Depends on: T40.
Acceptance: usage reconciles to invoice; limits enforced before the job, not after.
Spec: `specs/005-ops/spec.md`.

### T50 — Demand sidecar — `ready`
Outcome: Niche Radar integrated as a read-only demand service.
Depends on: demand research.
Acceptance: Wordstat/Bukvarix CSV import; B/R/A/G/C/P metrics; niche scoring; MCP read-only;
every hypothesis has evidence.
Spec: `specs/003-storefront/spec.md` (growth section).

## Ticket rules

1. A ticket without a spec is `blocked`, not `ready`.
2. A ticket is `done` only after an independent verifier exercises the real path.
3. No ticket may delete data, drop a table, or overwrite a source file without double human
   confirmation.
4. Every ticket ends with an evidence artefact: a test, a report, a screenshot, or a reconciliation
   output. "It works on my machine" is not evidence.
