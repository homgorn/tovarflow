# Spec 006 — WordPress / WooCommerce synchronisation

**Status:** draft for approval · **Date:** 2026-11-27 · **Depends on:** spec 002, ADR-0006,
research `docs/research/wordpress/`.

## 1. Direct answer

Use **separate WordPress installs managed by MainWP**, not Multisite. Bulk sync goes through
**WooCommerce REST API v3 (`wc/v3`)** with Application Passwords and batches of ≤100 items, backed
by an outbox and Action Scheduler on the WordPress side. Real-time price/stock uses WooCommerce
webhooks with a scheduled REST pull as reconciliation. Media uses `/wp/v2/media`. MCP is for
AI-assisted administration, **not** for system-to-system bulk sync.

Confidence: 8/10. The Multisite cache issue (core ticket #14992) and the batch RCE
(CVE-2026-63030) are the two hard constraints.

## 2. User scenarios

### US1 — Publish a product to one site (P0)
Given a canonical product with a right record, when I publish it to a registered WP site, then a
WooCommerce product is created/updated by SKU, with categories, attributes, variations and media.

### US2 — Change price and stock (P0)
Given a verified price change, when the outbox emits it, then `wc/v3` batch update is applied within
5 minutes, and a scheduled pull verifies the stored value within 15 minutes.

### US3 — Publish to many sites (P1)
Given 100 registered sites, when a product is published, then fan-out respects a per-site
concurrency limit, retries on 429/5xx, records per-site results and never writes directly to MySQL.

### US4 — Recover from site downtime (P1)
Given a WordPress site that is offline, when the outbox has pending jobs, then jobs stay queued and
resume when the site returns; no product is partially published without a recorded result.

## 3. Functional requirements

- **FR-001** Site registry: `wp_site(id, tenant_id, url, auth_ref, status, plugin_versions, health_at)`.
- **FR-002** Auth: dedicated sync user per site, Application Password or OAuth1 consumer key in a
  secret manager; least privilege (`manage_woocommerce`, `edit_products`, `upload_files`).
- **FR-003** Bulk: `POST /wp-json/wc/v3/products/batch`, ≤100 items, partial success recorded per item.
- **FR-004** Idempotency: stable SKU and a client-side idempotency key; WP does not provide one natively.
- **FR-005** Media: upload via `/wp/v2/media`, then link `featured_media` / `images[]`.
- **FR-006** Webhooks: `X-WC-Webhook-Signature` HMAC verified before ingest.
- **FR-007** Reconciliation: scheduled REST pull every 15 minutes compares price, stock and status.
- **FR-008** No direct MySQL writes; no XML-RPC; no network-activated WooCommerce on Multisite.
- **FR-009** Block `/wp-json/batch/v1` at the edge until all managed sites are on WP ≥ 7.0.3.
- **FR-010** Fleet control: MainWP child on each site, health checks and bulk updates.
- **FR-011** WP-Cron is disabled; system cron drives Action Scheduler.
- **FR-012** Every write emits an event with site id, trace id and result.

## 4. Non-functional requirements

- **NFR-001** 10 sites / 10k SKU: 5 parallel requests per site, ≤50 req/s aggregate.
- **NFR-002** 100 sites / 100k SKU: outbox + Action Scheduler, 10 runners/site, batch size 50.
- **NFR-003** 1000 sites / 1M SKU: per-site workers, 20 runners/site, Redis object cache, CDN purge.
- **NFR-004** A failed batch never silently succeeds; per-item errors are stored.

## 5. Data model

```text
wp_site(id, tenant_id, url, auth_ref, status, wc_version, wp_version, health_at)
wp_sync_job(id, tenant_id, site_id, kind, payload_ref, status, attempts, idempotency_key,
            created_at, finished_at, error)
wp_sync_result(id, job_id, external_id, result, error)
wp_webhook_event(id, site_id, signature_ok, payload_ref, received_at, processed_at)
```

## 6. Canonical → WooCommerce mapping

SKU ← `product.external_article`; GTIN → `_gtin` meta; name, description, short_description;
status; type simple/variable; categories via `/wc/v3/products/categories`; attributes via
`/wc/v3/products/attributes`; variations via `/products/<id>/variations/batch`; price as string
minor units converted to major; `stock_quantity` with `manage_stock: true`; images via media ids.

## 7. Acceptance scenarios

```gherkin
Scenario: batch with one bad item
  Given a batch of 100 products with one invalid category
  When WooCommerce returns partial success
  Then 99 results are recorded as published
  And the failed item gets a reason code and a retry job

Scenario: no direct database write
  Given a sync job
  When it executes
  Then only HTTPS REST calls are made
  And no wp_* table is touched directly

Scenario: site is offline
  Given a site with status=unhealthy
  When a publish job is queued
  Then the job stays pending
  And it resumes when health check passes
```

## 8. Out of scope

- Multisite for independent WooCommerce shops.
- MCP as a sync transport.
- Direct MySQL writes except a one-time migration under maintenance mode.
- Theme editing and content design.

## 9. Open questions

- Which managed-WordPress provider will host the fleet, and does it allow Application Passwords?
- Do we need WPGraphQL Smart Cache for read-heavy storefronts, or is REST + CDN enough?
- Which plugin set is mandatory on every site (MainWP Child, Action Scheduler High Volume, security)?
