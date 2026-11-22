# Global Marketplace API Comparison Report

**Generated:** 2026-11-22  
**Scope:** 16 marketplaces, prioritized by integration complexity and regional coverage  
**Confidence scale:** 10 = directly verified from official docs; 7 = official docs + community corroboration; 5 = partial/indirect; 3 = inferred from SDKs/third-party wrappers; 1 = login-walled or unavailable

---

## Executive Summary

| Tier | Platform | Region | Integration Difficulty | Key Blocker |
|------|----------|--------|------------------------|-------------|
| **1 (Easy)** | Google Merchant Center | Global | ★☆☆☆☆ | None — feed-based, service-account auth |
| **1 (Easy)** | Bol.com | NL/BE | ★★☆☆☆ | Client-credentials OAuth2; async writes via process-status polling |
| **1 (Easy)** | Kaufland | DE/AT/CZ/SK/PL | ★★☆☆☆ | HMAC-signed REST; 30 feeds/day CSV limit; playground sync lag |
| **2 (Medium)** | Walmart Marketplace | US/CA/MX | ★★★☆☆ | OAuth2 (15-min tokens); dual feed+API paths; dynamic sandbox only |
| **2 (Medium)** | Zalando (zDirect) | EU | ★★★☆☆ | Partner-only onboarding; per-API rate limits; 2-hr JWT tokens |
| **2 (Medium)** | Allegro | PL/CZ/SK/HU | ★★★☆☆ | OAuth2 + custom media types; 9k req/min global; sandbox separate |
| **2 (Medium)** | TikTok Shop | Global (SEA/US/EU) | ★★★☆☆ | Multi-market OAuth domains; sandbox QPH=1000; compliance review (3+ wks) |
| **2 (Medium)** | Meta Commerce | US (beta) | ★★★☆☆ | Closed beta; system-user tokens; App Review required for prod |
| **3 (Hard)** | Amazon SP-API | Global | ★★★★☆ | LWA OAuth + RDT for PII; per-operation token-bucket; sandbox ≠ prod limits |
| **3 (Hard)** | eBay Sell APIs | Global | ★★★★☆ | Dual Inventory+Feed APIs; 2M/day Inventory limit; LMS vs Seller Hub feeds |
| **3 (Hard)** | Mercado Libre | LatAm | ★★★★☆ | 6-hr access tokens; per-Client-ID limits; scroll-based pagination |
| **3 (Hard)** | Shopee Open Platform | SEA/TW/BR | ★★★★☆ | HMAC-SHA256 signing per call; per-shop token fragmentation; sandbox v2 only |
| **3 (Hard)** | Lazada Open Platform | SEA | ★★★★☆ | Per-region endpoints; HMAC signing; 3 auth policies; 10k/day test quota |
| **3 (Hard)** | Cdiscount (Octopia) | FR/BE/ES/IT | ★★★★☆ | Login-walled docs; SOAP deprecated; OAuth2 + API key; rate limit 100/min |
| **4 (Very Hard)** | Rakuten RMS | JP | ★★★★★ | ESA auth (serviceSecret+licenseKey 90-day expiry); docs login-walled; no public sandbox |
| **4 (Very Hard)** | Etsy Open API v3 | Global | ★★★★☆ | Dual auth (x-api-key + OAuth2); 100-listing batch limits; Commercial Access gated |

---

## Detailed Comparison Table

| Platform | Auth | API Style | Product Import | Price Write | Stock Write | Order Read | Returns | Rate Limits | Sandbox | Docs URL | Confidence |
|----------|------|-----------|----------------|-------------|-------------|------------|---------|-------------|---------|----------|------------|
| **Amazon SP-API** | LWA OAuth2 (public) / Self-auth (private); RDT for PII | REST + JSON; Swagger/OpenAPI per API | Feeds API (async) + Listings Items API (sync) | Feeds API / Listings Items PATCH | Feeds API / Inventory API | Orders API v0/v2026 | Returns API (beta) | Token-bucket per op/account/app; x-amzn-RateLimit-Limit header | Static + Dynamic + AI local; 5 req/s, burst 15 | https://developer-docs.amazon.com/sp-api/ | 9 |
| **eBay Sell APIs** | OAuth2 (Auth Code + Client Credentials); scopes per API | REST + JSON; Inventory API (sync) + Feed API (async LMS/Seller Hub) | Inventory API (offers) + Feed API (bulk) | Inventory API bulk_update_price_quantity / Feed ReviseInventoryStatus | Inventory API bulk_update_price_quantity / Feed ReviseInventoryStatus | Fulfillment API (orders) + Feed OrderReport | Post-Order API (returns/cases) | Per-API daily limits (Inventory 2M/day, Feed 100k/day, Fulfillment 100k/day) | Full sandbox env (separate keys); 5k calls/day default | https://developer.ebay.com/ | 9 |
| **Etsy Open API v3** | x-api-key (keystring:secret) + OAuth2 (Auth Code + PKCE) | REST + JSON; OpenAPI 3.0 spec | createDraftListing + updateListingInventory (per-listing) | PUT /listings/{id}/inventory (price in offerings) | PUT /listings/{id}/inventory (quantity in offerings) | Receipts API (transactions_r scope) | Shop Return Policy API | Undocumented global limits; batch endpoints 100 IDs max | Seller App = own shop only; Personal App + Commercial Access request | https://developers.etsy.com/ | 8 |
| **Walmart Marketplace** | OAuth2 Client Credentials (15-min tokens); delegated access for SPs | REST + JSON; Feeds (async) + Items/Inventory/Orders (sync) | Feeds API (Items feed) + Item Management API | Feeds Price feed / Items API price update | Feeds Inventory feed / Inventory API | Orders API (acknowledge, ship, cancel) | Returns/Refunds API | Token bucket; x-current-token-count + X-Next-Replenishment-Time headers | Dynamic sandbox (custom test data); 30 req/hr per feed type | https://developer.walmart.com/ | 9 |
| **TikTok Shop** | OAuth2 (Auth Code) per market; app_key/app_secret signing | REST + JSON; Global Product API for cross-border | Product API (create/edit) + Global Product API | Product API update_price / Global Product API | Product API update_inventory / Global Product API | Order API (list/get/ack/ship) | Return & Refund API | Sandbox QPH=1000; Production per-endpoint limits (undocumented) | Seller Center Dev Shops (Core/Full Function); 180-day expiry | https://partner.tiktokshop.com/ | 8 |
| **Allegro** | OAuth2 (Auth Code + Client Credentials); custom media types vnd.allegro.public.v1+json | REST + JSON; versioned via Accept header | Offers API (create from product) + Product API | Offers API price update | Offers API stock update | Order Events API (polling) + Checkout Forms | Limited returns via order events | 9,000 req/min per Client ID; Leaky Bucket per user; 429 on excess | Separate sandbox (allegrosandbox.pl); same limits as prod | https://developer.allegro.pl/ | 9 |
| **Kaufland** | HMAC-SHA256 (Client Key + Secret Key); no OAuth | REST + JSON; OpenAPI 3.0 (Swagger) | Product Data API (EAN-based) + CSV import-files (async) | Product Data PATCH /units price | Product Data PATCH /units quantity | Orders API (list/get) + Order Units | Order Units refund/cancel endpoints | Deep pagination >1M offset: 200/min; undocumented general limits | Playground env (sellerapi-playground.kaufland.com); 2-week sync lag | https://sellerapi.kaufland.com/ | 9 |
| **Bol.com** | OAuth2 Client Credentials (299-sec JWT); no user consent | REST + JSON; versioned APIs (Offers v11, Orders v10, etc.) | Offers API (EAN-based) | Offers API v11 price update | Offers API v11 stock update | Orders & Shipments API v10 | Returns API v10 | Per-endpoint; published at api.bol.com/retailer/public/ratelimits; X-RateLimit headers | Demo env (/retailer-demo/ prefix); fixed sample data only | https://developers.bol.com/ | 9 |
| **Cdiscount (Octopia)** | OAuth2 + API Key (login-walled); legacy SOAP deprecated | REST + JSON (Octopia unified); CSV feeds | Product Integration API (POST packages) + CSV | Product Integration API price fields | Product Integration API stock fields | Orders API (via Octopia) | Returns via Octopia | 100 req/min (observed); token 1hr | Not publicly documented; Octopia portal required | https://dev.cdiscount.com/ / https://developer.octopia-io.net/ | 5 |
| **Zalando (zDirect)** | OAuth2 Client Credentials (2-hr JWT); no refresh token | REST + JSON; GraphQL for PSR; per-Merchant-ID scoping | Product Submissions API (async) + Product Attributes | Prices API (write-only; 30 req/min, 8k updates/min) | Stocks API (60 req/min, 2k updates/min) | Orders API (7 sub-limits; 40-2000 req/min) | Order lines transitions | Per-API limits (see row); 429 + Retry-After + X-Rate-Limit | Sandbox base URL (api-sandbox.merchants.zalando.com); app must be in sandbox mode | https://developers.merchants.zalando.com/ | 9 |
| **Mercado Libre** | OAuth2 Auth Code (6-hr access + refresh); PKCE recommended | REST + JSON; scroll-based search pagination | Items API (create/update) | PUT /items/{id} price | PUT /items/{id} available_quantity | Orders API (search/get) + Shipments | Claims/Returns API | Per-Client-ID per-endpoint (hundreds/hr); 429 with backoff guidance | Test users via developers portal; no separate sandbox env | https://developers.mercadolibre.com/ | 8 |
| **Shopee Open Platform** | OAuth2 Auth Code (365-day max auth); HMAC-SHA256 signing per call | REST + JSON; partner_id + sign + timestamp on every request | Product API (global + shop SKU) | Product API update_price | Product API update_stock | Order API (list/get/split/cancel) | Order cancellation + returns | Undocumented; per-app/per-shop fragmentation after refresh | Sandbox v2 (openplatform.sandbox.test-stable.shopee.sg); test accounts via Console | https://open.shopee.com/ | 7 |
| **Lazada Open Platform** | OAuth2 Auth Code (3 policies); HMAC-SHA256 signing; per-region endpoints | REST + JSON; SDKs provided (Java/PHP/Python/.NET/Ruby) | Product API (create/update) + Global Product | Product API price update | Product API stock update | Order API (get/set status/ship) | Returns API | 10k/day (Testing); 10M/day (Online); QPS global per-API shared; E1002 backend limit | No public sandbox; Testing status = 10k/day on prod-like env | https://open.lazada.com/ | 7 |
| **Rakuten RMS** | ESA: serviceSecret (no expiry) + licenseKey (90-day expiry for PII APIs) | REST + JSON (+ some XML); specs login-walled (RMS portal) | ItemAPI 2.0/2.1 + CabinetAPI (images) | ItemAPI price update | InventoryAPI 2.1 (bulk 400 max) | RakutenPayOrderAPI (searchOrder+getOrder) | InquiryManagementAPI | Undocumented; no public rate limit specs | None public; specs 403 from external; RMS Service Square for partners | https://webservice.rms.rakuten.co.jp/ (login-walled) | 3 |
| **Google Merchant Center** | OAuth2 (3rd-party) or Service Account (own); no API keys | REST + JSON (Merchant API v1beta); resource names not IDs | ProductInputs API (insert/update) + DataSources | ProductInputs price attribute | ProductInputs availability attribute | Not applicable (ads platform) | Not applicable | Quotas via accounts.limits.get; per-account product limits | No sandbox; test via Merchant Center demo account | https://developers.google.com/merchant/api/ | 10 |
| **Meta Commerce** | System User access tokens (Page token); App Review required for prod | Graph API (REST + JSON); cursor pagination | Catalog Batch API + Product Feeds (scheduled CSV/TSV/XML) | Catalog Batch API price update | Catalog Batch API availability update | Order Management API (commerce_orders) | Promotions/Offers API | Standard Graph API rate limits (undocumented for Commerce) | Test Commerce Accounts (US only); Staging mode in Commerce Manager | https://developers.facebook.com/docs/commerce-platform/ | 6 |

---

## Common Abstraction Patterns

### 1. **Auth Abstraction Layer**
```
Interface: TokenProvider
  - getAccessToken(scopes[]) -> Promise<Token>
  - refresh() -> Promise<Token>
Implementations:
  - OAuth2AuthCode (Amazon, eBay, Etsy, TikTok, Mercado Libre, Shopee, Lazada, Zalando, Meta)
  - OAuth2ClientCredentials (Walmart, Bol.com, Google Service Account, Zalando)
  - HMACSigned (Kaufland, Allegro custom, Shopee, Lazada)
  - ESASigned (Rakuten)
  - DualKey (Etsy: x-api-key + OAuth2)
```

### 2. **Product Sync Patterns**
| Pattern | Platforms | Notes |
|---------|-----------|-------|
| **Feed-first (async)** | Amazon, eBay, Walmart, Cdiscount, Meta | Batch CSV/JSON; status polling via process-status/feed-status |
| **API-first (sync)** | Bol.com, Kaufland, Zalando (Prices/Stocks), Allegro, TikTok | REST endpoints; immediate validation; webhook for async confirmation |
| **Hybrid** | Amazon (both), eBay (Inventory+Feed), Walmart (both) | Feeds for bulk onboarding; API for real-time price/stock |
| **EAN/GTIN-centric** | Bol.com, Kaufland, Zalando, Google | Catalog lookup by GTIN; offer attached to existing product |
| **SKU-centric** | Amazon, eBay, TikTok, Shopee, Lazada, Mercado Libre | Seller owns SKU; product created per listing |

### 3. **Order Import Patterns**
| Pattern | Platforms | Notes |
|---------|-----------|-------|
| **Polling + Acknowledge** | Amazon, Walmart, Bol.com, Zalando, Allegro, TikTok, Lazada | GET orders → ACK → Ship → Track |
| **Webhook/Push + Polling fallback** | eBay (notifications), Shopee (push), TikTok (webhooks), Lazada (Push) | Reduce polling; verify via GET |
| **Feed-based download** | eBay (Feed API OrderReport), Cdiscount | Async report generation; download file |
| **Scroll/Cursor pagination** | Mercado Libre (scroll_id), Meta (cursor), Zalando (cursor) | No offset/limit; consume scroll before expiry |

### 4. **Rate Limit Handling**
- **Token Bucket** (Amazon, Walmart, Kaufland, Zalando): read `x-current-token-count` / `X-RateLimit-Remaining`; backoff on 429
- **Fixed Window** (eBay daily, Lazada daily, Bol.com per-endpoint): track locally; schedule bursts
- **Leaky Bucket** (Allegro per-user): expect latency increase before 429
- **Undocumented** (Mercado Libre, Shopee, TikTok prod, Rakuten): exponential backoff + jitter; monitor 429 rate

### 5. **Sandbox Strategy**
| Type | Platforms |
|------|-----------|
| **Full separate env** | Amazon (3 regions), eBay, Walmart (Dynamic), Allegro, TikTok (Dev Shops), Zalando, Shopee v2 |
| **Demo/fixed data** | Bol.com (/retailer-demo/), Google (test Merchant Center), Meta (Test Commerce US only) |
| **Prod-like limited quota** | Lazada (Testing status 10k/day), Kaufland (Playground, 2-week sync) |
| **None / Login-walled** | Rakuten, Cdiscount (Octopia portal) |

---

## Recommended First Three Global Connectors

### 1. **Google Merchant Center** (Tier 1 — Foundation)
**Rationale:**
- **Zero integration friction**: Service-account auth (no user consent), feed-based REST, no sandbox needed
- **Universal catalog backbone**: GTIN-centric model maps to Bol.com, Kaufland, Zalando, Amazon (ASIN↔GTIN), eBay (ePID)
- **Free, unlimited scale**: No rate limits on product writes (quotas are account-level product counts, not API calls)
- **Strategic value**: Powers Google Shopping, free listings, Performance Max, local inventory ads — revenue driver for every merchant
- **Confidence**: 10/10 (official docs fully public, client libs in 3 languages)

**Implementation effort:** ~2 weeks for full product + inventory sync with DataSource management

---

### 2. **Bol.com** (Tier 1 — European Beachhead)
**Rationale:**
- **Clean OAuth2 Client Credentials**: 299-sec JWT, no redirect flows, token caching trivial
- **Explicit async contract**: Every write returns `process-status` — predictable polling pattern reusable for Walmart, Amazon Feeds, Zalando
- **Published rate limits**: Machine-readable at `api.bol.com/retailer/public/ratelimits` — no guessing
- **NL/BE focus**: High GMV density; single VAT regime; English docs; seller onboarding self-serve
- **Confidence**: 9/10 (all docs public, Postman collections, active community)

**Implementation effort:** ~3 weeks (Offers v11 + Orders v10 + Returns v10 + ProcessStatus polling)

---

### 3. **Walmart Marketplace** (Tier 2 — US Scale)
**Rationale:**
- **Largest US marketplace after Amazon**: 150M+ monthly visitors; seller-friendly onboarding
- **Dual path mirrors real-world needs**: Feeds for bulk catalog onboarding; Items/Inventory/Orders APIs for real-time ops
- **Dynamic sandbox with simulation APIs**: Create test orders, simulate carrier delivery, test returns — end-to-end CI/CD possible
- **Delegated access model**: Solution Provider keys enable multi-seller SaaS from day one
- **Confidence**: 9/10 (comprehensive docs, Python/Java samples, active partner program)

**Blockers to watch:**
- 15-min token expiry → requires robust token cache with proactive refresh
- Feed throttling: 30 req/hr per feed type in sandbox (prod higher but per-account)
- Category mapping: Walmart taxonomy ≠ Google/GS1; requires mapping table maintenance

**Implementation effort:** ~5 weeks (Feeds + Items + Inventory + Orders + Returns + sandbox CI)

---

## Hardest Blockers Across All Platforms

| Blocker | Affected Platforms | Mitigation |
|---------|-------------------|------------|
| **Login-walled / partner-gated docs** | Rakuten RMS, Cdiscount (Octopia), Zalando (partner-only onboarding) | Require seller to share PDF specs; build against Saras/BluePrism connector schemas; apply for partner access early |
| **Short-lived tokens + no refresh** | Zalando (2-hr JWT, no refresh), Walmart (15-min), Google (1-hr) | Centralized token service with proactive renewal (T-5min); cache by (client_id, scopes) |
| **Per-call HMAC signing** | Shopee, Lazada, Kaufland, Allegro (custom) | Shared signing middleware; timestamp sync (NTP); request-id idempotency keys |
| **Token fragmentation per shop** | Shopee (post-refresh per shop_id), TikTok (per-shop tokens), Lazada (per-seller) | Token store keyed by (app, shop_id); refresh workflow per shop; monitor auth expiry webhooks |
| **Undocumented rate limits** | Mercado Libre, Shopee, TikTok prod, Rakuten, Cdiscount | Conservative defaults (50% of observed); exponential backoff + jitter; 429 telemetry dashboard |
| **Separate sandbox = separate code paths** | Amazon (3 regions), eBay, Allegro, Lazada, TikTok | Abstract base URL + credentials per environment; integration tests against each |
| **Category/attribute mapping divergence** | All platforms | Maintain canonical product model → per-platform transformers; use GTIN as anchor; invest in PIM |
| **Async write confirmation polling** | Amazon Feeds, eBay Feeds, Walmart Feeds, Bol.com, Zalando Product Submissions | Generic `ProcessStatusPoller` with webhook fallback; configurable timeout/interval per platform |
| **Compliance / App Review gates** | TikTok (3+ weeks), Meta (closed beta), Amazon (Appstore listing), Zalando (partner contract) | Start legal/compliance review in parallel with dev; use sandbox for dev; budget calendar time |

---

## Next Steps

1. **Week 1-2**: Implement Google Merchant Center connector (service account + ProductInputs + DataSources)
2. **Week 3-5**: Implement Bol.com connector (Offers v11 + Orders v10 + ProcessStatus polling framework)
3. **Week 6-10**: Implement Walmart connector (Feeds + Items/Inventory/Orders + Dynamic Sandbox CI)
4. **Parallel**: Apply for TikTok Shop Partner Center (3+ week compliance), Zalando Partner Program, Amazon SP-API Appstore
5. **Architecture**: Build `TokenProvider`, `ProcessStatusPoller`, `RateLimitHandler`, `CategoryMapper` as shared libraries before platform-specific code

---

*All facts marked with confidence scores. "Measured" = directly from official docs with URL/date. "Reported" = from official docs but login-walled or partner-gated. "Inferred" = from SDKs, third-party wrappers, or community sources.*