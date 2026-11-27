# Spec 003 — Storefront

**Status:** draft, platform decided: Medusa v2 · **Date:** 2026-11-22 · **Depends on:** specs 001–002,
ADR-0006.

## 1. Why

The storefront is the first owned sales channel. It must prove the catalogue, the price and the
media before a marketplace connector is worth building. It also becomes the template that can later
be sold or hosted for a client.

The platform is decided: **Medusa v2** (MIT) with a Next.js storefront. This spec states behaviour
that must hold on that platform; ADR-0006 records the choice, the alternatives and the reopen
conditions. A separate Catalog Hub owns ingestion, supplier offers and the margin ledger; Medusa
owns products, variants, carts, orders, regions and sales channels.

## 2. User scenarios

### US1 — Browse and buy (P0)
As a customer, I want to find a product, understand it, and buy it without friction.

Acceptance:
1. Home, category, search, product and cart pages render on mobile and desktop.
2. A product page shows title, price, availability, media, attributes and delivery estimate.
3. Search returns relevant results for a misspelled query (trigram fallback).
4. Cart persists across sessions; checkout has a single-page summary.
5. A failed payment returns a recoverable error, not a dead end.

### US2 — Find us in search and AI answers (P0)
As the business, I want every product page to be readable by crawlers and AI answer engines.

Acceptance:
1. Primary content is present in the raw HTML response, without JavaScript execution.
2. Every product page has schema.org `Product` with offers, price, currency, availability and images.
3. `sitemap.xml`, `robots.txt`, canonical URLs and hreflang are correct.
4. `llms.txt` and a `.md` twin exist for key pages.
5. Core Web Vitals: LCP < 2.5 s, CLS < 0.1, INP < 200 ms on a mid-range mobile.
6. No duplicate content across filter/sort URLs; faceted navigation has canonical rules.

### US3 — Operate multiple storefronts (P1)
As an operator, I want a second storefront with its own domain, locale and catalogue, without
forking the code.

Acceptance:
1. A storefront has `domain`, `locale`, `currency`, `theme`, `catalogue_filter`.
2. Products and media are shared; visibility is a rule, not a copy.
3. A new storefront is created from a template and a config, not a branch.
4. Tenant isolation is preserved.

### US4 — Keep content fresh (P1)
As an operator, I want price/stock/content changes to appear without a deploy.

Acceptance:
1. A price change is visible within 60 seconds.
2. An out-of-stock product shows an explicit state and does not accept an order.
3. A removed product returns 410, not a 200 empty page.
4. Image changes use a new content hash, so CDN caches invalidate.

### US5 — Start from demand (P0 for growth)
As an operator, I want a storefront to start from a demand brief, not a hunch.

Acceptance:
1. A brief contains keywords, demand trend, competition, seasonality and a unit-economics gate.
2. The brief is linked to categories and products.
3. A storefront without a brief is allowed only as an experiment, marked as such.

## 2A. Answer-First / AEO contract

Every product, category and documentation page follows `docs/architecture/04-answer-first-aeo.md`:

1. A direct factual answer in the first **150–300 characters** under the H1: name, SKU, brand,
   price, currency, availability, units, delivery, warranty.
2. Chunks of 200–500 tokens (~800–2000 characters), split at headings; our corpus chunker uses
   ~1400 characters.
3. High fact density: exact numbers with units and sources; unknown is written as unknown, not zero.
4. A specification `<table>`, a price-explanation table and a `<dl>` of short facts.
5. At least one `primary` source link to a manufacturer, register or official rule.
6. Entity consistency: SKU, GTIN, brand and canonical URL come from the canonical catalogue, never
   retyped per channel; NAP agrees with Google Business Profile / OpenStreetMap where applicable.
7. All of the above is present in **raw HTML without JavaScript**.

`tools/aeo_lint.py` is the gate. The ranking mechanics are confidence 7/10; the specific citation
uplift was supplied by the owner and is not independently measured here.

## 3. Functional requirements

- **FR-001** Server-rendered catalogue; JavaScript enhances, never gates content.
- **FR-002** Product URL is stable and human-readable; a slug change preserves a redirect.
- **FR-003** Search supports RU morphology and typo tolerance (at minimum trigram).
- **FR-004** Facets are indexed, not client-side filtered from a full dump.
- **FR-005** Price is rendered from the margin ledger, never from the raw supplier price.
- **FR-006** Availability is tri-state; unknown is not "in stock".
- **FR-007** Checkout supports the local payment and delivery methods of the target market.
- **FR-008** Every page has a canonical URL and a locale.
- **FR-009** Structured data is generated from the same DTO as the page, not duplicated.
- **FR-010** A crawler-view test runs in CI and fails if primary content is absent.
- **FR-011** A second storefront is config-only.
- **FR-012** Content rights are recorded per product and per image; a product without a right is
  not published.

## 4. Non-functional requirements

- **NFR-001** 10k SKU catalogue, p95 category page < 300 ms at the edge cache, < 800 ms on origin.
- **NFR-002** Lighthouse mobile performance >= 90 for product and category pages.
- **NFR-003** Accessibility: WCAG 2.2 AA for checkout and product pages.
- **NFR-004** Uptime 99.9% for the storefront; a read-only catalogue during checkout outages.
- **NFR-005** SEO: 0 orphan product pages; 0 pages with missing title/description.

## 5. Platform decision

The decision is recorded in **ADR-0006: Medusa v2** (MIT) with a Next.js storefront. The matrix
compared Medusa, Vendure, Saleor, Shopify, WooCommerce, BigCommerce, Bitrix, InSales, Advantshop,
Tilda and a custom Next.js + Postgres build.

Weights: catalogue scale (15), multi-store/tenant (15), API-first (15), marketplace ecosystem (15),
TCO at 10k/100k/1M SKU (10), SEO/performance (10), RU payments/delivery (10), ops fit (10).

Medusa scored 81/100; Vendure 77; Saleor 74; Shopify Plus 72; 1C-Bitrix 71. The custom build scored
85 but was rejected on TCO (3–5 senior engineers, $50k+/mo) and time to market.

## 6. Data model (platform-independent)

```text
storefront(id, tenant_id, domain, locale, currency, theme, catalogue_filter, status)
storefront_page(id, storefront_id, type, slug, title, content, seo JSONB)
navigation(id, storefront_id, parent_id, label, url, position)
product_visibility(storefront_id, product_id, visible, position)
cart(id, tenant_id, storefront_id, customer_id, currency, status)
cart_line(id, cart_id, variant_id, qty, price_minor)
order(id, tenant_id, storefront_id, customer_id, status, totals JSONB, payment_status)
```

## 7. Acceptance scenarios

```gherkin
Scenario: a crawler sees the product
  Given a product page
  When I fetch it with a crawler user-agent and no JavaScript
  Then the title, price, availability and description are in the HTML
  And the structured data is valid

Scenario: a second storefront without a fork
  Given an existing tenant with a catalogue
  When I create a storefront with a new domain and locale
  Then products are visible by rule
  And no product data is duplicated
  And the first storefront is unchanged

Scenario: unknown stock is not sellable
  Given a variant with unknown stock
  When a customer opens the product page
  Then the buy button is disabled
  And the availability text says "unknown", not "in stock"

Scenario: a price change is fast
  Given a live product
  When the margin ledger changes the price
  Then the storefront shows the new price within 60 seconds
  And the old price is not cached indefinitely
```

## 8. Out of scope for the first storefront

- Customer accounts, loyalty, subscriptions.
- Multi-warehouse split shipments.
- Marketplace checkout inside the storefront.
- A theme marketplace.

## 9. Open questions

- Which platform wins the weighted matrix? (research track `platforms`)
- Which payment provider and delivery integrator are available for the first market?
- Is a marketplace "showcase" (Ozon/WB) a channel or a storefront variant? (Recommendation:
  channel, because orders and moderation are marketplace-owned.)
- How much content is generated vs supplied? (Rights gate first.)

## 10. Test plan

- Crawler-view test on 100 product pages.
- Lighthouse CI on mobile.
- Structured-data validation.
- Faceted navigation canonicalisation test.
- Checkout happy path and payment failure.
- Multi-store isolation test.
- 10k SKU load test with cache cold/warm.
