# ADR 0006 — Storefront platform: Medusa v2

**Status:** accepted · **Date:** 2026-11-22 · **Confidence:** 8/10

## Context

We need a storefront/commerce core that can:

- hold a 10k–1M SKU supplier catalogue with variants and supplier-specific offers;
- run multiple storefronts (brands, locales, regions) from one catalogue;
- be extended with Q-Parser ingestion, a margin ledger and RU/CN/global marketplace connectors;
- avoid per-order or GMV fees that break unit economics at scale;
- become multi-tenant later without a rewrite.

Eleven candidates were scored against eight weighted criteria. The full matrix, TCO scenarios and
sources are in `docs/research/platforms/REPORT.md` and `docs/research/platforms/data.json`.

Top scores: custom Next.js + Postgres 85 (but 3–5 senior engineers, $50k+/mo), Medusa v2 81,
Vendure 77, Saleor 74, Shopify Plus 72, 1C-Bitrix 71, Advantshop/InSales 65, WooCommerce 59,
Tilda 37.

## Decision

Use **Medusa v2** (MIT core) with a **Next.js** storefront.

Deployment path:

1. Medusa Cloud Pro ($299/mo) for the MVP, to avoid ops work.
2. Self-host on Kubernetes/managed Postgres/Redis when the catalogue or GMV justifies it
   (estimated $600–800/mo at 100k SKU).

Architecture:

- Medusa is the commerce core: products, variants, prices, stock, carts, orders, regions, sales
  channels.
- A separate **Catalog Hub** service owns ingestion, normalisation, supplier offers, the margin
  ledger and marketplace connectors. It synchronises into Medusa through the Admin API and
  workflows.
- Multi-tenancy is added from day one as a thin scoping layer (`tenant_id` → store/sales channel),
  not deferred. The research estimates 4–6 weeks for this, versus Vendure's native channels.
- Custom Medusa modules: `qparser`, `supplier-offer`, `margin`, `marketplace-listing`,
  `marketplace-sync`.

## Why not the others

| Candidate | Reason rejected |
|---|---|
| Vendure | Native multi-tenant is attractive, but the core is GPLv3 and paid plans start at €599/mo; smaller ecosystem. Reopen if SaaS becomes phase 1. |
| Saleor | Strong GraphQL core, but Cloud is $1,599+/mo with GMV overage; heavier ops. |
| Shopify Plus | Best ecosystem and RU payments, but $2,300+/mo plus GMV fees, limited catalogue control and content-rights risk. Wrong architecture for a catalogue platform. |
| 1C-Bitrix | Native 1C and RU payments, but legacy PHP stack and weak API-first posture. |
| Advantshop / InSales | Fast launch and native marketplace sync, but not multi-tenant and limited catalogue scale. |
| WooCommerce | Cheap, but PHP/WordPress ops at 100k+ SKU and a weak multi-store model. |
| Custom Next.js + Postgres | Theoretical maximum (85), but 3–5 senior engineers and $50k+/mo; premature. |
| Tilda | Not an ecommerce platform. |

## Consequences

Positive:

- MIT core, no GMV fee, full data ownership.
- TypeScript/Node/Postgres/Next.js — one language across the core and storefront.
- Workflows and modules fit the Proposal → Policy → Execution → Verification path.
- Cloud Pro removes infra work for the MVP; self-host is a documented exit.

Negative:

- Multi-tenancy is not native; the scoping layer is our code and must be tested hard.
- Medusa's admin is product-centric; supplier offers and margin need custom admin UI.
- Medusa's catalogue model must be mapped to our canonical model, not the other way around.
- A future Medusa major version may require migration work; pin the version and test upgrades.

## Reopen conditions

- Multi-tenant SaaS is required in month 1 → Vendure (native channels).
- The team has no TypeScript/Node experience → Shopify Plus or 1C-Bitrix.
- 1C integration is a hard blocker → 1C-Bitrix.
- Native Ozon/WB/Yandex two-way sync is non-negotiable before MVP → InSales/Advantshop.
