# Roadmap

> Outcome-based horizons, not a promise of dates. Effort is in focused dev-weeks for one
> senior engineer plus agents. A horizon closes only when its exit criteria are verified.

## How this roadmap is organised

Three layers, deliberately separate:

1. **Roadmap** (this file) — why and in what order. Horizons with exit criteria.
2. **Backlog** (`docs/backlog/tickets.md`) — executable tracer-bullet tickets with dependencies.
3. **Specs** (`specs/`) — what "done" means for each feature, with acceptance criteria.

A TODO list alone turns into an unprioritised pile. A roadmap alone turns into a slide. The
backlog is where work actually moves, and a ticket cannot start without a spec.

## H0 — Foundation (now, mostly done)

Scope:

- Full Q-Parser corpus: 128 canonical pages, 442k characters, 100% coverage.
- Structured extraction: 16 endpoints, 72 formats, 4 plans, 15 sourced claims.
- SQLite + FTS5, knowledge graph (334 nodes / 293 edges), LLM wiki with indexes.
- Layered architecture: RU / CN / global / CIS, supply vs sales separation.
- Inherited-assets registry from `wb china`, `alibaba ali temu`, `china auto`, `goofish`,
  `niche-radar`.
- Deep research tracks launched: competitors, RU marketplaces, CN marketplaces, global
  marketplaces, platforms, demand.

Exit criteria:

- `tools/verify_coverage.py` reports 0 missing.
- Every claim has `source_url` + `observed_at`.
- Architecture docs and constitution exist.
- Research reports have `REPORT.md` + `data.json` + confidence labels.

## H1 — Ingest and normalise (4–6 weeks)

Scope:

- Q-Parser client with polling, retries, pagination, raw capture, fixtures.
- Ingest one real domain end to end: categories → parse → goods → canonical products.
- Canonical model: product, variant, offer, media, attributes, category.
- Attribute mapping v1 (the `data` map is the hard part).
- Margin ledger v1: purchase + delivery + commission + returns + acquiring + tax.
- Storefront MVP on Medusa v2 + Next.js: catalogue, product page, search, cart.
- YML feed with a validator.

Exit criteria:

- Same parse id replays to the same canonical output (hash-stable).
- 1,000 products ingested, 0 broken images, 0 lost variants.
- A price can be explained line by line from the margin ledger.
- Storefront page has primary content in raw HTML (crawler test).
- YML passes the target validator.

## H2 — RU sales loop (6–8 weeks)

Scope:

- Ozon Seller adapter at L2: price and stock write, verified by re-read.
- Wildberries adapter at L2: category-scoped tokens, rate limits, quarantine warning.
- Yandex Market feed-first publishing.
- Listing state machine and moderation queue.
- Order import and tracking push for one channel.
- Reconciliation: parsed vs published vs rejected vs sold.
- Admin MVP: Medusa Admin extended for catalogue/orders + a Next.js/Refine operator console for
  proposals, listings and reconciliation (research `docs/research/admin/`).

Exit criteria:

- 100 listings published to a real account; 0 duplicate cards.
- Price write is idempotent: same key → one HTTP request.
- Every price change is verified; mismatches open an incident.
- Daily reconciliation report has zero unexplained deltas.
- A rollback procedure is tested on a price batch.

## H3 — Storefront engine (4–6 weeks)

Scope:

- Multi-storefront: domain, locale, currency, theme, catalogue filter.
- SEO/AEO: SSR/ISR, schema.org, sitemap, `llms.txt`, `.md` twins.
- Search and facets (Postgres FTS + `pg_trgm`, optional vector).
- Payments and delivery for RU.
- Content pages, legal pages, returns policy.
- Performance budget: LCP < 2.5 s on mobile, CLS < 0.1.
- Answer-First/AEO templates, spec table, `<dl>` facts, primary-source links and `aeo_lint` gate.
- WordPress sync v1: separate installs managed by MainWP, WooCommerce REST v3 (`wc/v3`) with
  Application Passwords, batches ≤100, outbox + Action Scheduler, media via `/wp/v2/media`.
  **Do not use Multisite for independent WooCommerce shops** (`switch_to_blog()` cache corruption,
  network-activated WC overhead, single DB = SPOF). MCP is an AI-admin tool, not a bulk sync bus.

Exit criteria:

- 10k SKU storefront passes the performance budget.
- 100% of product pages have valid structured data.
- Crawler test passes: no primary content requires JavaScript.
- A second storefront can be created without code changes.

## H4 — China supply and cross-border (6–8 weeks)

Scope:

- 1688 sourcing through a partner/agent API, not a direct seller API.
- Landed cost: purchase + domestic CN delivery + export + international + duty + VAT.
- Translation pipeline RU ↔ CN with a glossary and human review queue.
- Ozon Global / WB China as sales channels.
- Product certification/document checklist per category.

Exit criteria:

- Landed cost is complete for a sample of 100 SKUs, with unknown components explicit.
- A translated card passes a native-speaker review sample.
- Cross-border listing is published and tracked on one channel.
- No content is published without a rights/attribution record.

## H5 — Global channels (8–12 weeks)

Scope:

- eBay and Etsy adapters at L2/L3 are re-evaluated after Google Merchant/Bol/Walmart.
- Google Merchant Center feed and ProductInputs API (first global channel).
- Bol.com and Walmart adapters at L2, then Kaufland/Allegro.
- Amazon SP-API at L1/L2 (feeds, price, stock), then orders.
- TikTok Shop / Zalando evaluation and, if approved, one pilot.
- Multi-currency, tax and settlement.
- Localised storefronts (EN first).
- WordPress fleet scale: 100–1000 sites, per-site workers, system cron instead of WP-Cron,
  Redis object cache and CDN purge; MainWP for bulk updates/backups.

Exit criteria:

- One global channel publishes and receives a real order.
- Multi-currency price ledger reconciles to settlement.
- Channel-specific category/attribute validation catches errors before submission.
- Connector contract tests run in CI against fixtures and sandbox.

## H6 — SaaS and ready-made storefronts (8–12 weeks)

Scope:

- Tenant onboarding, roles, billing, usage limits.
- Storefront templates and a theme editor.
- Per-tenant channel accounts and credentials.
- Client-facing catalogue and moderation console.
- White-label domain and email.

Exit criteria:

- A second tenant is onboarded without engineering work.
- Tenant isolation is tested (no cross-tenant reads, object paths, or search results).
- Billing reconciles to usage.
- A storefront can be handed over with its own domain and data export.

## H7 — Demand and growth (ongoing, starts in H1)

Scope:

- Niche Radar sidecar: Wordstat/Bukvarix, B/R/A/G/C/P metrics, niches, hypotheses.
- Marketplace demand signals: search suggestions, out-of-stock, sales ranks.
- Keyword graph linked to categories and products.
- SEO/AEO playbook and content pipeline.
- Paid-channel experiments with a measured CAC gate.

Exit criteria:

- Every new storefront starts from a demand brief, not a hunch.
- A niche has a scored demand, competition and unit-economics gate.
- Content production is traceable to a keyword and a product.

## H8 — Scale and certification (ongoing)

Scope:

- 1M SKU catalogue, partitioned tables, async indexing.
- Connector certification suites (L5).
- Observability, SLOs, incident runbooks.
- Cost control: AI points, scraping, storage, egress.
- Security: secrets, RLS, audit, threat model.
- WordPress hardening: block `/wp-json/batch/v1` until WP ≥ 7.0.3 is confirmed (CVE-2026-63030),
  least-privilege sync users, per-site secret rotation.

Exit criteria:

- p95 catalogue read < 300 ms at 1M SKU.
- Every live connector has a passing certification suite.
- A failed price sync is detected within 5 minutes and rolled back.
- Cost per 1k SKU is known and budgeted.

## What is deliberately out of order

- No global connectors before the RU loop is proven; the failure modes are the same, but the
  account/legal setup is not.
- No SaaS before a single storefront works; multi-tenancy multiplies every bug.
- No automatic supplier identity merge; it is a one-way door.
- No browser automation in autonomous paths; it is brittle and legally risky.
