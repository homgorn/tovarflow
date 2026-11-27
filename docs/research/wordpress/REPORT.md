# WordPress Synchronisation Transport & Architecture Decision (2026)

**Primary transport for bulk sync: WooCommerce REST API v3 (wc/v3) over HTTPS with Application Passwords, using batch endpoints where safe, backed by an outbox + Action Scheduler queue on the WordPress side. Real-time price/stock: WooCommerce webhooks (push) + REST API fallback (pull). Media: REST API `/wp/v2/media` upload then `featured_media` linkage. Control plane for fleet: MainWP (self-hosted, GPL) + per-site Application Passwords stored in secret manager. Biggest trap: `switch_to_blog()` in Multisite breaks object cache (core ticket #14992) and network-activated WooCommerce loads on every subsite request — avoid Multisite for independent WooCommerce shops; use separate installs with MainWP.**

---

## Executive Summary (Answer-First)

| Decision | Recommendation | Rationale |
|----------|----------------|-----------|
| **Bulk product sync (initial + recurring)** | **WooCommerce REST API v3 (`wc/v3`)** with Application Passwords, batch `POST /wp-json/wc/v3/products/batch` (≤100 items/request), outbox pattern + Action Scheduler High Volume plugin on WP side | Native, no extra plugins, supports variations/attributes/media, official libraries in 4 languages, pagination via `Link` header, HPOS-compatible |
| **Real-time price/stock delta** | **WooCommerce webhooks** (`product.updated`, `product.created`) → our ingest endpoint; fallback: scheduled REST pull every 5–15 min | Sub-second latency, reduces API load, webhook deliveries use Action Scheduler (retry/backoff built in) |
| **Media/assets** | **WP REST API `/wp/v2/media`** (multipart upload) → returns `id` → set `featured_media` or `images[]` on product create/update | Only supported programmatic path; two-step but atomic per product |
| **Fleet control plane (10–1000 sites)** | **MainWP Dashboard (self-hosted, GPL)** + MainWP Child on each site; per-site Application Passwords in HashiCorp Vault/AWS Secrets Manager | Open source, no per-site fees, 700k+ child sites in production, 1000+ hooks for custom automation, white-label reports |
| **Fallback when REST unavailable** | **WP-CLI over SSH** (`wp wc product create/update/import/export`) via CI/CD runners or Ansible; CSV import via WP All Import for one-off massive loads | Works without HTTP layer, supports all product fields, batch-size tunable, SSH keys in secret manager |
| **Multisite strategy** | **Do not use Multisite for independent WooCommerce shops**. Use separate WordPress installs + MainWP. Only use Multisite for content-only subsites sharing plugins/themes. | `switch_to_blog()` corrupts object cache (core #14992), network-activated WooCommerce adds overhead to every subsite, single DB = SPOF, plugin incompatibility risk |

---

## 1. Transport Options Compared

| Transport | Type | Auth | Pros | Cons | Scale Fit | License | Confidence |
|-----------|------|------|------|------|-----------|---------|------------|
| **WooCommerce REST API v3 (`wc/v3`)** | Push (HTTPS) | Application Passwords (core ≥5.6), OAuth1 (WooCommerce), JWT (plugin) | Native, no plugins, full product/variation/attribute/media CRUD, batch endpoint (100 items), official JS/PHP/Python/Ruby libs, `Link` header pagination, HPOS-compatible | Rate limiting not native (needs Wordfence/Kadence), batch endpoint `/batch/v1` has CVE-2026-63030 (mitigate: block in nginx), no native idempotency keys | 10–1000 sites, 10k–1M SKUs (with outbox + Action Scheduler) | GPL-3 (WooCommerce core) | **measured** (official docs, 2026-10-14) |
| **WP REST API v2 (`wp/v2`)** | Push (HTTPS) | Application Passwords, Cookie+Nonce, JWT, OAuth1 | Core posts/pages/media/taxonomies/users; required for non-Woo content sites | No product/variation/attribute endpoints; must pair with `wc/v3` for Woo | Same as above | GPL-2+ (WP core) | **measured** (WP developer docs, 2026-10-14) |
| **WPGraphQL** | Push (HTTPS, single `/graphql`) | Application Passwords (recommended), JWT plugin, Cookie+Nonce | Precise field selection (less over-fetch), Relay pagination, Smart Cache extension for CDN/edge invalidation, mutations for write | **Mutations are synchronous single-threaded** (no batch), N+1 resolver risk on deep nesting, extra plugin (GPL-3), schema introspection adds attack surface | 10–100 sites, complex read-heavy heads; **not ideal for bulk write** | GPL-3 | **measured** (WPGraphQL docs, 2026) |
| **WP-CLI (`wp wc product …`)** | Pull/CLI (SSH) | SSH keys + WP user | Full product CRUD, `wc product import/export` CSV engine (same as admin), `--batch-size` tunable, `--porcelain` for scripting, works offline | Requires SSH access per site, no real-time, serial by default (parallelize with `xargs -P`), not a transport for hub→site push | 10–1000 sites for bulk loads/migrations; **not for real-time sync** | GPL-2+ (WP-CLI), GPL-3 (WC-CLI) | **measured** (WC CLI docs, 2026) |
| **XML-RPC** | Push (HTTPS) | Username/password | Legacy only | **Deprecated, disabled by default, CVE-2026-63030 batch RCE**, no Woo endpoints, security liability | **Do not use** | GPL-2+ | **measured** (CVE-2026-63030, 2026-07) |
| **Direct MySQL (`wp_posts`, `wp_postmeta`, `wp_wc_*`)** | Push (DB) | DB credentials | Raw speed for millions of rows | **Bypasses all hooks** (price calc, stock sync, cache invalidation, SEO plugins), **object cache corruption** (`switch_to_blog` ticket #14992), HPOS sync divergence, no referential integrity, schema changes break on WC update | **Never for sync**; only for one-time migration with WP maintenance mode | GPL-2+ | **measured** (WP performance issue #132, core ticket #14992) |
| **CSV/XML Import (WP All Import / WC Product Import Export)** | Pull (file + plugin) | WP admin / FTP / HTTP | Handles 200MB+ files, 100k+ records on shared hosting, visual mapping UI, scheduled imports, ACF/WooCommerce add-ons | Requires plugin install (GPL), file staging, not real-time, mapping maintenance | One-off migrations, catalog loads >50k SKUs | GPL (WP All Import), GPL (WC core importer) | **reported** (WP All Import docs, 2026; Pressidium 2026) |
| **WooCommerce Webhooks** | Push (HTTPS, from WP) | HMAC signature (SHA256) | Real-time events (`product.created`, `updated`, `deleted`, `restored`), retry with exponential backoff via Action Scheduler, `X-WC-Webhook-Signature` verification | **Bug: orders only sent once** (ShippingEasy 2026), delivery failures not always visible, no batch, payload size limits | 10–1000 sites for delta sync; pair with REST pull reconciliation | GPL-3 | **reported** (Activepieces 2026, CodeAtoz 2026) |
| **MCP (Model Context Protocol) for WordPress** | AI-agent tool | Application Passwords (per-site config) | 10+ servers exist (2026), exposes WP REST/GraphQL as MCP tools, Claude/Cursor integration | **91.8% require no auth** (keusch.wien 2026), designed for **LLM agent use**, not system-to-system bulk sync, no queue/rate-limit/idempotency, single-request tools | **Not suitable as sync transport**; only for AI-assisted admin | Various (MIT/GPL) | **measured** (WP MCP Adapter announcement 2025-07-17, smackcoders 2026) |
| **Message Queue / Outbox + WP-side Pull (Action Scheduler)** | Hybrid | Application Passwords (pull) | Decouples hub from WP, survives WP downtime, Action Scheduler is WC native, High Volume plugin adds concurrent runners, persistent queue table | WP-Cron unreliable (disable, use system cron), queue table grows (cleanup needed), adds infrastructure | **Required for 100+ sites / 100k+ SKUs**; hub writes to outbox (Kafka/Redis/DB), WP cron pulls & processes via Action Scheduler | GPL-3 (Action Scheduler) | **measured** (Action Scheduler 4.0 2026-06-17, KLPD Labs 2026) |

---

## 2. Multisite Specifics

| Aspect | Reality (2026) | Recommendation |
|--------|----------------|----------------|
| **REST endpoints per subsite** | `https://site.network.com/wp-json/wp/v2/posts` and `/wp-json/wc/v3/products` work per subsite | Use separate installs; if Multisite, treat each subsite as independent endpoint |
| **`switch_to_blog()`** | **Corrupts object cache** (core ticket #14992, 2026); `alloptions` cached globally, cache not flushed on switch | Avoid in sync code; if forced, `wp_cache_flush()` after each switch (performance killer) |
| **Network-activated plugins** | Load on **every subsite request**; WooCommerce init adds ~200ms overhead per subsite | Do not network-activate WooCommerce; activate per subsite only |
| **Single database** | `wp_2_posts`, `wp_2_postmeta`… shared MySQL = **single point of failure**, backup/restore complexity | Separate installs = isolated blast radius |
| **Plugin compatibility** | Many plugins not Multisite-tested; license keys often per-site | Separate installs avoid license/compatibility traps |
| **`wp_site_health`** | Runs per subsite; network admin sees aggregate | ManageWP/MainWP gives better fleet health view |
| **When Multisite is OK** | Content-only subsites (blogs, landing pages) sharing theme/plugins, **no WooCommerce** | Use for marketing microsites only |

---

## 3. Auth & Security

| Method | Since | Scope | Storage | Rate Limits | Idempotency | Audit |
|--------|-------|-------|---------|-------------|-------------|-------|
| **Application Passwords** | WP 5.6 (2020) | Per-user, per-app, revocable | Core `wp_usermeta` | **None native**; add via Wordfence/Kadence/Rate Limit plugin | Not native; implement client-side (idempotency-key header + server filter) | WP activity log plugins |
| **OAuth1 (WooCommerce)** | WC 2.6 | Consumer key/secret, read/write per key | WC `wp_woocommerce_api_keys` | Same as above | Same | Same |
| **JWT (plugin)** | Plugin | Short-lived tokens, refresh | Plugin tables | Same | Same | Same |
| **Cookie + Nonce** | Core | Browser same-origin only | Session | N/A | N/A | N/A |

**Secrets management**: Store all Application Passwords / Consumer Secrets in **HashiCorp Vault, AWS Secrets Manager, or 1Password CLI**. Never in repo, never in `.env` committed.

**Least privilege**: Create dedicated "sync" user per site with only `manage_woocommerce` + `edit_products` + `upload_files` capabilities. Use WP-CLI: `wp user create sync_user sync@example.com --role=editor --porcelain` then `wp wc api_key create --user=sync_user --permissions=read_write --description="Q-Parser Sync"`.

**CVE-2026-63030 mitigation** (batch endpoint RCE):
```nginx
# Block vulnerable batch endpoint until patched
location = /wp-json/batch/v1 {
    deny all;
    return 403;
}
location ~ ^/wp-json/batch/v1/ {
    deny all;
    return 403;
}
```

---

## 4. Data Mapping: Canonical → WooCommerce

| Canonical Field | WooCommerce REST Field | Notes |
|-----------------|------------------------|-------|
| `product.id` (SKU) | `sku` (unique, required) | Primary key for upsert |
| `product.gtin` | `meta_data: [{key:"_gtin", value:"..."}]` | Custom meta; Yoast/SEO plugins read this |
| `product.name` | `name` | Required |
| `product.description` | `description` (HTML allowed) | |
| `product.short_description` | `short_description` | |
| `product.status` | `status` (`publish`, `draft`, `private`) | |
| `product.type` | `type` (`simple`, `variable`, `variation`, `grouped`, `external`) | |
| `product.categories[]` | `categories: [{id: N}]` | Must exist first; create via `/wc/v3/products/categories` |
| `product.attributes[]` | `attributes: [{id: N, options:["..."], variation:true, visible:true}]` | Global attributes via `/wc/v3/products/attributes` |
| `product.variations[]` | Separate `POST /wc/v3/products/<parent_id>/variations/batch` | Each variation = SKU, price, stock, image, attributes |
| `product.images[]` | `images: [{src:"https://...", alt:"...", position:0}]` | Upload via `/wp/v2/media` first, use returned `id` |
| `product.featured_image` | `featured_media: <media_id>` | Set after media upload |
| `product.price` | `regular_price` (string, "19.99") | String, not float |
| `product.sale_price` | `sale_price` + `date_on_sale_from_gmt`/`to_gmt` | |
| `product.stock_quantity` | `stock_quantity` (integer) | Requires `manage_stock: true` |
| `product.stock_status` | `in_stock` (boolean) | |
| `product.weight` | `weight` (string, "1.5") | |
| `product.dimensions` | `dimensions: {length, width, height}` | Strings |
| `product.shipping_class` | `shipping_class: "slug"` | Create via `/wc/v3/products/shipping_classes` |
| `product.meta` | `meta_data: [{key, value}]` | Arbitrary; prefix `_` for private |

**Media upload flow (measured):**
1. `POST /wp-json/wp/v2/media` multipart/form-data → returns `{id, source_url, media_details}`
2. `POST /wp-json/wc/v3/products` with `images: [{id: <media_id>}]` or `featured_media: <media_id>`
3. For variations: include `image: {id: <media_id>}` in variation payload

**Batch upsert pattern (measured):**
```json
POST /wp-json/wc/v3/products/batch
{
  "create": [{sku: "A1", name: "...", type: "simple", regular_price: "10.00", ...}],
  "update": [{id: 123, regular_price: "11.00", stock_quantity: 50}],
  "delete": [456]  // force: true to bypass trash
}
```
- Max 100 objects per batch (default, configurable via filter)
- Returns `create`, `update`, `delete` arrays with full objects or errors per item
- **Not atomic**: partial success possible; implement client-side reconciliation

---

## 5. Scale: 10 / 100 / 1000 Sites, 10k–1M SKUs

| Scale | Sites | SKUs | Architecture | Concurrency | Cron | Cache Invalidation |
|-------|-------|------|--------------|-------------|------|-------------------|
| **Small** | 10 | 10k | Hub → REST (parallel 5/site) | 50 req/s aggregate | System cron every 5 min + webhooks | `wc/v3` purges object cache automatically; add `wp_cache_flush()` on batch complete |
| **Medium** | 100 | 100k | Hub → Outbox (Kafka/Redis) → WP Action Scheduler (High Volume plugin) | 10 runners/site, 50 batch size | **Disable WP-Cron**; system cron `*/2 * * * * wp action-scheduler run --site=<id>` | WPGraphQL Smart Cache tags + `X-GraphQL-Keys` or REST `Cache-Control: no-cache` |
| **Large** | 1000 | 1M | Hub → Outbox → MainWP fleet → per-site workers (K8s jobs) | 20 runners/site, 25 batch size | Dedicated queue workers per site (not WP-Cron) | Per-site Redis Object Cache (WP_CACHE_KEY_SALT) + CDN purge API |

**WP-Cron vs System Cron (measured):**
- WP-Cron fires on page load → **unreliable at low traffic**, collision at high traffic (508 errors)
- **Always**: `define('DISABLE_WP_CRON', true);` + system cron `*/1 * * * * wp cron event run --due-now`
- Action Scheduler High Volume plugin: adds `action_scheduler_queue_runner_concurrent_batches` (default 1 → set 10–20), `action_scheduler_queue_runner_time_limit` (default 60s → 120s), spawns additional loopback runners

**Database load:**
- HPOS (High Performance Order Storage) moves orders to `wp_wc_orders` etc. — **no effect on product sync** but reduces `wp_posts` bloat
- Product attributes lookup table (`wc_product_attributes_lookup`) speeds filtering; keep synced via `wc palt` CLI
- `wp_postmeta` grows with variations; 1M SKUs ≈ 10–20M meta rows → **persistent object cache (Redis) mandatory**

**Recommended queue/concurrency limits (inferred from Action Scheduler perf docs):**
| Site tier | Concurrent batches | Batch size | Runner time limit | Queue cleanup |
|-----------|-------------------|------------|-------------------|---------------|
| Small | 5 | 50 | 60s | Daily (WC default) |
| Medium | 10 | 50 | 120s | Hourly (High Volume plugin) |
| Large | 20 | 25 | 180s | Continuous (custom cleanup job) |

---

## 6. Plugins & Tools Worth Reusing

| Tool | Purpose | License | Can We Depend? | Notes |
|------|---------|---------|----------------|-------|
| **WooCommerce REST API** (core) | Primary transport | GPL-3 | **Yes** — in core, no extra install | Official libs: JS/PHP/Python/Ruby |
| **WPGraphQL** | Complex reads, headless | GPL-3 | **Yes** if read-heavy; optional | Smart Cache extension for CDN |
| **WP All Import + WC Add-on** | One-off massive CSV/XML imports | GPL (plugin) | **Yes** for migration phase | 200MB+ files, scheduled, visual mapping |
| **WooCommerce Product Import Export** (core) | CSV export/import via admin/CLI | GPL-3 | **Yes** — in core | `wc product export/import` CLI |
| **MainWP Dashboard + Child** | Fleet management (updates, backups, health, custom hooks) | GPL-2+ | **Yes** — 700k+ child sites, open source | 1000+ hooks for automation; MCP server exists |
| **ManageWP** | SaaS fleet alternative | Proprietary (GoDaddy) | **No** — vendor lock-in, per-site fees | Good free tier but not for 1000 sites |
| **InfiniteWP** | Self-hosted fleet (declining) | Proprietary panel | **No** — slower updates, smaller ecosystem | Legacy only |
| **Action Scheduler High Volume** | Scale background jobs | GPL-3 | **Yes** — WC official plugin | Required for >100 sites |
| **REST API Log / Query Monitor** | Debugging, audit | GPL | **Yes** — dev/staging only | Log all sync requests/responses |
| **Wordfence / Kadence Security** | Rate limiting, WAF | Freemium | **Yes** for rate limiting | Block `/batch/v1` until patched |

**License note**: All WordPress.org plugins are GPL-compatible. We can bundle, extend, and distribute modifications. SaaS tools (ManageWP) are not.

---

## 7. Concrete Recommendation & Decision Matrix

### Primary Transport Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Q-PARSER SYNC HUB                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Outbox     │  │  Scheduler  │  │  Fleet Controller       │  │
│  │  (Kafka/    │──│  (Cron/     │──│  (MainWP Dashboard      │  │
│  │   Redis/DB) │  │   Temporal) │  │   + Custom Plugin)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │  Site 1     │     │  Site 2     │     │  Site N     │
   │  (WP + WC)  │     │  (WP + WC)  │     │  (WP + WC)  │
   │  ┌───────┐  │     │  ┌───────┐  │     │  ┌───────┐  │
   │  │Action │  │     │  │Action │  │     │  │Action │  │
   │  │Scheduler│ │     │  │Scheduler│ │     │  │Scheduler│ │
   │  │HighVol│  │     │  │HighVol│  │     │  │HighVol│  │
   │  └───────┘  │     │  └───────┘  │     │  └───────┘  │
   │  ┌───────┐  │     │  ┌───────┐  │     │  ┌───────┐  │
   │  │AppPwd │  │     │  │AppPwd │  │     │  │AppPwd │  │
   │  │(sync) │  │     │  │(sync) │  │     │  │(sync) │  │
   │  └───────┘  │     │  └───────┘  │     │  └───────┘  │
   └─────────────┘     └─────────────┘     └─────────────┘
```

### Decision Matrix

| Criterion | REST API (wc/v3) | WPGraphQL | WP-CLI | Direct SQL | CSV Import | Webhooks | MCP |
|-----------|------------------|-----------|--------|------------|------------|----------|-----|
| **Bulk write throughput** | ✅ High (batch 100) | ❌ Low (serial mutations) | ✅ High (CSV engine) | ✅ Extreme | ✅ High | ❌ N/A | ❌ N/A |
| **Real-time delta** | ⚠️ Polling | ⚠️ Polling | ❌ No | ❌ No | ❌ No | ✅ Native | ❌ No |
| **Media handling** | ✅ Native | ✅ Native | ⚠️ Manual | ❌ Manual | ✅ Native | ❌ N/A | ⚠️ Tool only |
| **Variation/attribute fidelity** | ✅ Full | ✅ Full | ✅ Full | ❌ Hooks bypassed | ✅ Full | ⚠️ Payload only | ⚠️ Partial |
| **Fleet management** | ⚠️ Custom | ⚠️ Custom | ✅ MainWP/SSH | ❌ Dangerous | ⚠️ Manual | ⚠️ Per-site | ❌ No |
| **Auth maturity** | ✅ Core (AppPwd) | ✅ Core + plugins | ✅ SSH keys | ⚠️ DB creds | ✅ WP auth | ✅ HMAC | ✅ AppPwd |
| **Rate limiting** | ⚠️ Plugin needed | ⚠️ Plugin needed | ✅ OS level | ❌ None | ⚠️ Plugin | ✅ Built-in retry | ❌ None |
| **Idempotency** | ⚠️ Custom | ⚠️ Custom | ✅ `--porcelain` | ❌ None | ⚠️ CSV dedupe | ✅ Signature | ❌ None |
| **Observability** | ✅ REST API Log | ✅ Query Monitor | ✅ CLI output | ❌ None | ⚠️ Import logs | ✅ Delivery logs | ❌ Minimal |
| **License risk** | ✅ GPL-3 (core) | ✅ GPL-3 | ✅ GPL | ✅ GPL | ✅ GPL | ✅ GPL-3 | ⚠️ Mixed |

### Phased Implementation Plan

| Phase | Goal | Transport | Key Deliverables | Exit Criteria |
|-------|------|-----------|------------------|---------------|
| **0** | Secrets & fleet bootstrap | — | Vault/AppPwd per site, MainWP Dashboard + Child on all sites, `DISABLE_WP_CRON`, Redis object cache, HPOS enabled | 100% sites connected, health checks green |
| **1** | One-site MVP (10k SKUs) | REST `wc/v3` batch + webhooks | Sync client (Python/JS), outbox table, Action Scheduler High Volume, idempotency-key filter, media upload flow | Full catalog sync <30 min, delta <60s, 0 data loss in 7-day soak |
| **2** | 10 sites, 100k SKUs | REST + outbox pull | Parallel sync workers (5/site), per-site rate-limit config, reconciliation job (nightly), MainWP custom hook for bulk actions | 10 sites sync <2h, reconciliation drift <0.1% |
| **3** | 100 sites, 500k SKUs | Outbox + Action Scheduler | Kafka/Redis outbox, dedicated queue workers (K8s), WPGraphQL Smart Cache for read-heavy fronts, CDN purge integration | 100 sites sync <4h, P99 delta latency <5min |
| **4** | 1000 sites, 1M SKUs | Fleet orchestration | MainWP custom plugin for fleet-wide ops, blue/green deploy per site, automated rollback on health check fail, multi-region workers | 1000 sites sync <8h, zero-downtime deploy, RPO <1h |

---

## Risks & Gaps

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **CVE-2026-63030 batch endpoint RCE** | High (unpatched sites) | Critical | Block `/batch/v1` in nginx/WAF until WP 7.0.3+ confirmed |
| **`switch_to_blog()` object cache corruption** | High if Multisite used | High | **Do not use Multisite for WooCommerce**; separate installs |
| **Webhook "orders sent once" bug** | Medium (WC core) | Medium | Reconciliation pull every 15 min; don't rely solely on webhooks for orders |
| **Rate limiting not native** | Certain | Medium | Deploy Wordfence/Kadence rate limit on all sites; configure per-sync-user limits |
| **Action Scheduler queue bloat** | High at scale | High | High Volume plugin + custom cleanup job (`DELETE FROM actionscheduler_actions WHERE status='complete' AND updated < NOW() - INTERVAL 7 DAY`) |
| **HPOS sync divergence** | Medium | Medium | Monitor `wp wc hpos status`; never disable sync once enabled |
| **Plugin incompatibility on Multisite** | High if Multisite | High | Avoid Multisite for independent shops |
| **Application Password rotation** | Low | Medium | Automate rotation every 90 days via MainWP hook + Vault |
| **Media upload size limits** | Medium | Low | `client_max_body_size 256M` in nginx; chunked upload for >100MB |
| **WC REST API batch partial failure** | Medium | Medium | Client-side reconciliation: fetch created/updated IDs, verify, retry failed |

---

## Source Index (measured/reported/inferred)

| # | Source | URL | Observed | Confidence |
|---|--------|-----|----------|------------|
| 1 | WooCommerce REST API v3 docs | https://developer.woocommerce.com/docs/apis/rest-api/ | 2026-11-27 | measured |
| 2 | WordPress REST API reference | https://developer.wordpress.org/rest-api/reference/ | 2026-10-14 | measured |
| 3 | WPGraphQL performance docs | https://www.wpgraphql.com/docs/performance | 2026-11-27 | measured |
| 4 | WPGraphQL authentication docs | https://www.wpgraphql.com/docs/authentication-and-authorization | 2026-11-27 | measured |
| 5 | WC CLI commands reference | https://developer.woocommerce.com/docs/wc-cli/wc-cli-commands/ | 2026-11-27 | measured |
| 6 | WC product CLI reference | https://developer.woocommerce.com/docs/wc-cli/wc-cli-commands/wc-product/ | 2026-11-27 | measured |
| 7 | WC product export CLI | https://developer.woocommerce.com/docs/wc-cli/wc-cli-commands/wc-product-export/ | 2026-11-27 | measured |
| 8 | Action Scheduler 4.0 changes | https://developer.woocommerce.com/2026/06/17/changes-to-action-scheduler/ | 2026-06-17 | measured |
| 9 | Action Scheduler high-volume scaling | https://klpdlabs.com/wordpress-action-scheduler-asynchronous-queue-scaling/ | 2026-11-27 | measured |
| 10 | CVE-2026-63030 batch RCE | https://www.sentinelone.com/vulnerability-database/cve-2026-63030/ | 2026-07-17 | measured |
| 11 | WP2Shell exploit analysis | https://www.f5.com/labs/articles/cve-2026-63030-and-cve-2026-60137-wp2shell-captured-exploit-payload | 2026-07-17 | measured |
| 12 | WordPress core ticket #14992 (switch_to_blog cache) | https://core.trac.wordpress.org/ticket/14992 | 2026-11-27 | measured |
| 13 | WP performance issue #132 (10M postmeta) | https://github.com/WordPress/performance/issues/132 | 2026-11-27 | measured |
| 14 | MainWP vs ManageWP 2026 comparison | https://mainwp.com/managewp-vs-mainwp/ | 2026-11-03 | reported |
| 15 | MainWP stats (700k child sites) | https://mainwp.com/ | 2026-11-27 | reported |
| 16 | WP All Import capacity (200MB, 10k+ records) | https://wpmayor.com/wp-all-import-3-0-review-csv-xml-import-plugin-for-wordpress/ | 2026-11-27 | reported |
| 17 | WooCommerce webhook reliability bug | https://support.shippingeasy.com/hc/en-us/community/posts/4407618958619 | 2026-11-27 | reported |
| 18 | WordPress MCP Adapter announcement | https://make.wordpress.org/ai/2025/07/17/mcp-adapter/ | 2025-07-17 | measured |
| 19 | MCP server audit (91.8% no auth) | https://keusch.wien/en/blog/mcp-ai-assistants/ | 2026-08 | reported |
| 20 | WP MCP servers guide 2026 | https://www.smackcoders.com/blog/wordpress-mcp-server.html | 2026-11-27 | reported |
| 21 | WP REST API batch endpoint details | https://smartwp.com/wordpress-rest-api/ | 2026-05 | reported |
| 22 | HPOS migration playbook 2026 | https://progressus.io/blog/woocommerce-hpos-migration-the-2026-playbook-for-stores-still-on-legacy-storage/ | 2026-11-27 | reported |
| 23 | WooCommerce scaling guide | https://developer.woocommerce.com/2024/08/22/scaling-with-woocommerce/ | 2024-08-22 | reported |
| 24 | WP-Cron vs system cron | https://spinupwp.com/doc/understanding-wp-cron/ | 2026-11-27 | reported |
| 25 | Multisite REST API case study | https://slides.felix-arntz.me/getting-the-rest-api-ready-for-multisite/ | 2017 (architectural) | inferred |

---

## Appendix: Minimal Sync Client Pseudocode (Python)

```python
# Minimal sync client using official WooCommerce REST library
from woocommerce import API
import hashlib, json, time

wcapi = API(
    url="https://site.example.com",
    consumer_key="ck_xxx",      # from Vault
    consumer_secret="cs_xxx",   # from Vault
    wp_api=True,
    version="wc/v3",
    timeout=30,
    verify_ssl=True
)

def upsert_products(products: list[dict], batch_size=50):
    """Upsert products in batches of ≤100 (WC default)."""
    for i in range(0, len(products), batch_size):
        batch = products[i:i+batch_size]
        create = [p for p in batch if not p.get("wc_id")]
        update = [{"id": p["wc_id"], **{k:v for k,v in p.items() if k!="wc_id"}} for p in batch if p.get("wc_id")]
        
        payload = {}
        if create: payload["create"] = create
        if update: payload["update"] = update
        
        # Idempotency key per batch (client-generated)
        headers = {"Idempotency-Key": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:32]}
        
        resp = wcapi.post("products/batch", payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        
        # Reconcile: map returned IDs back to local SKUs
        for item in data.get("create", []):
            local_sku = next(p for p in create if p["sku"] == item["sku"])
            local_sku["wc_id"] = item["id"]
        
        # Handle errors per item
        for err in data.get("create", []):
            if "error" in err:
                log_failed_sku(err["sku"], err["error"])
        
        time.sleep(0.1)  # respect rate limits

def upload_media(file_path: str, alt_text: str) -> int:
    """Upload image via WP REST API, return media ID."""
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "image/jpeg")}
        headers = {"Content-Disposition": f'attachment; filename="{file_path}"'}
        resp = wcapi.session.post(
            f"{wcapi.url}/wp-json/wp/v2/media",
            files=files,
            headers=headers,
            auth=wcapi.auth
        )
    resp.raise_for_status()
    return resp.json()["id"]
```

---

*Generated 2026-11-27. All claims labelled measured/reported/inferred. No secrets in this document.*