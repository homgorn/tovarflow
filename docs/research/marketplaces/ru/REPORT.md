# RU Marketplace Capability Matrix
## Sales Channel API Research for Supplier Catalogue Publishing & Sync

**Generated:** 2026-11-22  
**Scope:** Ozon Seller API, Wildberries, Yandex Market Partner API, Megamarket, Avito, Kaspi.kz (CIS)  
**Sources:** Local OpenAPI specs (Ozon: 482 paths, WB: 290 ops across 13 domains), official docs, developer portals  
**Confidence scale:** measured (from spec), reported (official docs), inferred (community/third-party)

---

## 1. Ozon Seller API

### 1.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | API Key + Client-Id headers | measured (OpenAPI) |
| Headers | `Client-Id: <string>`, `Api-Key: <string>` | measured |
| Token location | Seller Cabinet → Settings → API | reported (docs.ozon.ru) |
| Expiry | Unlimited (revocable) | reported |
| Scopes | Granular per-method groups (read/write) | measured (spec tags) |

### 1.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST (POST for all mutating + listing ops) | measured |
| Base URL | `https://api-seller.ozon.ru` | reported |
| Versioning | URL path `/v1/`, `/v2/`, `/v3/`, `/v4/`, `/v5/`, `/v6/` | measured |
| Format | JSON request/response | measured |
| Pagination | Cursor-based (`cursor` + `limit`) | measured |

### 1.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | API-only (`/v3/product/import`, `/v1/product/import-by-sku`) | measured |
| Feed support | No native feed; CSV/Excel only in UI | reported |
| Required attributes | Category-specific via `/v1/description-category/tree` + `/v1/description-category/attribute` | measured |
| Category mapping | Hierarchical tree; `type_id` required; attributes validated pre-import (FR-026) | measured |
| Media | `/v1/product/pictures/import` (up to 3600 px, JPEG/PNG/WebP, ≤20 MB) | measured |
| Moderation | Async; status via `/v1/product/import/info`; rejection codes documented | measured |
| Variants | SKU-based (offer_id + product_id); size/color via characteristics | measured |

### 1.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `/v1/product/import/prices` (bulk), `/v5/product/info/prices` (read) | measured |
| Frequency | Near real-time; no hard throttle documented | reported |
| Validation | Min/max price rules per category; auto-reject if <3× cost (WB pattern, inferred for Ozon) | inferred |
| Idempotency | `offer_id` + `price` as key; no explicit idem key in spec | measured |

### 1.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v2/products/stocks` (FBS/rFBS), `/v1/product/info/stocks-by-warehouse/fbo\|fbs` (read) | measured |
| Warehouse types | FBO (Ozon), FBS (seller), rFBS (regional) | measured |
| Granularity | Per SKU per warehouse; `present`, `reserved` fields | measured |
| Sync latency | Seconds | reported |

### 1.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v3/posting/fbo/list`, `/v3/posting/fbs/list`, `/v4/posting/fbs/list`, `/v2/order/create` | measured |
| Models | FBO (Ozon fulfillment), FBS (seller fulfillment), rFBS, FBP | measured |
| Status flow | `awaiting_packaging` → `awaiting_deliver` → `delivering` → `delivered` | measured |
| Webhooks | Notifications API (`/v1/notification/*`) for order events | measured |

### 1.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v1/returns/list`, `/v1/returns/company/fbs/info`, `/v1/return/giveout/*` | measured |
| Flow | Buyer initiates → seller confirms/rejects → giveout barcode → utilization | measured |
| Automation | Partial via API; some statuses UI-only | reported |

### 1.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| General | ~50–100 req/min (unofficial) | reported |
| Finance | ≤31-day window; auto-split required (FR-025) | measured (spec) |
| Premium/Analytics | Separate quotas | reported |

### 1.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Availability | No public sandbox; test on production with test products | reported |
| CI strategy | Contract tests on fixtures (FR-029, FR-030) | measured (spec) |

### 1.10 Regional/Legal Constraints
- Russian entity required (IP/OOO)
- Certificate/GOST for regulated categories (cosmetics, children's goods, electronics)
- `product/certificate/*` endpoints for binding certs
- Data localization (152-FZ)

### 1.11 Docs URL
https://docs.ozon.ru/api/seller/

---

## 2. Wildberries (WB)

### 2.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | JWT Bearer token per API domain | measured |
| Header | `Authorization: <token>` | measured |
| Token source | Seller Cabinet → Settings → API (12 token scopes) | reported |
| Expiry | Long-lived; refresh via UI | reported |
| Scopes | 13 domains × read/write (Content, Marketplace, Statistics, Advert, Discounts, Supplies, Finance, etc.) | measured |

### 2.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST (mixed GET/POST/PUT/PATCH/DELETE) | measured |
| Base URLs | 13 subdomains (see domain table) | measured |
| Versioning | Path `/v1/`, `/v2/`, `/v3/`, `/content/v2/`, `/content/v3/` | measured |
| Format | JSON | measured |
| Pagination | `limit`/`offset` or `page`/`size` | measured |

### 2.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | API-only (`/content/v2/cards/upload`, `/content/v2/cards/update`) | measured |
| Feed support | Excel upload in UI only | reported |
| Required attributes | Subject-based (`/content/v2/object/charcs/{subjectId}`); characteristics dict per subject | measured |
| Category mapping | Subject tree (`/content/v2/object/parent/all`, `/content/v2/object/all`) | measured |
| Media | `/content/v3/media/file` + `/content/v3/media/save` (max 50 MB, JPEG/PNG) | measured |
| Moderation | Async; `/content/v2/cards/error/list` for rejections; quarantine if price anomaly | measured |
| Variants | `nmID` (nomenclature) + `size` + `characteristics` | measured |

### 2.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/api/v2/upload/task` (prices), `/api/v2/upload/task/club-discount`, `/api/v3/stocks/{warehouseId}` (discounts-prices-api) | measured |
| Validation | Quarantine if price < ⅓ of reference (US2 acceptance) | measured (spec) |
| Frequency | Buffer/task model; async processing | measured |

### 2.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `PUT/DELETE /api/v3/stocks/{warehouseId}` (marketplace-api) | measured |
| Warehouses | `/api/v3/warehouses` (list); FBO/FBS warehouses | measured |
| Granularity | Per `nmID` + `size` + `warehouseId` | measured |

### 2.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/api/v3/orders/new`, `/api/v3/orders`, `/api/v3/dbw/orders/new`, `/api/v3/dbs/orders/new` | measured |
| Models | FBS (seller), FBW (WB fulfillment), DBS (direct), Click&Collect | measured |
| Status flow | `new` → `confirm` → `assemble` → `deliver` / `cancel` | measured |
| Stickers | `/api/v3/orders/stickers` (PDF) | measured |

### 2.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/api/v1/claims` (list), `PATCH /api/v1/claim` (returns-api) | measured |
| Flow | Claim → seller decision → refund/replace | measured |

### 2.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| Stats API | 1 req/min (hard) (FR-027) | measured |
| Content API | ~100–200 req/min (unofficial) | reported |
| Marketplace API | ~200 req/min (unofficial) | reported |
| 429 handling | `Retry-After` header; 3 consecutive → account pause (FR-024) | measured |

### 2.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Availability | No public sandbox | reported |
| Test approach | Test tokens on staging products | inferred |

### 2.10 Regional/Legal Constraints
- Russian entity or KZ/BY/ARM/KG entity for cross-border
- Mandatory certification (TR CU) for regulated categories
- Labeling (Честный ЗНАК) via `/api/v3/orders/{id}/meta/sgtin|uin|imei|gtin|expiration`
- Data localization

### 2.11 Docs URL
https://dev.wildberries.ru/

---

## 3. Yandex Market Partner API

### 3.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | API-Key header (preferred) + OAuth 2.0 (legacy) | reported |
| Header | `Api-Key: <token>` | measured |
| Token source | Partner Cabinet → Settings → API Keys | reported |
| Expiry | Unlimited (API-Key); 1 year (OAuth) | reported |
| Scopes | Granular: `all-methods`, `inventory-and-order-processing`, `pricing`, `offers-and-cards-management`, `promotion` + `:read-only` variants | measured |

### 3.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST + Webhooks | reported |
| Base URL | `https://api.partner.market.yandex.ru` | reported |
| Versioning | `/v1/`, `/v2/` | reported |
| Format | JSON | reported |
| Pagination | `pageToken` + `limit` (max 100) | reported |

### 3.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | API (`/v2/businesses/{businessId}/offer-mappings`) + Feed (YML/CSV via FTP/HTTP) | reported |
| Feed support | Yes — YML (Yandex Market Language) primary; scheduled fetch | reported |
| Required attributes | Category-specific via `/v2/categories/tree`; GTIN/EAN mandatory for most | reported |
| Category mapping | `categoryId` from tree; `mapping` endpoint for auto-match | reported |
| Media | Up to 50 images; max 10 MB; JPEG/PNG; HTTPS URLs | reported |
| Moderation | Async; status via offer-mapping `state`; rejection reasons in response | reported |
| Variants | `offerId` + `color`/`size`/`vendorCode` | reported |

### 3.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v2/businesses/{businessId}/offer-prices/updates` (bulk) | reported |
| Feed | YML price element | reported |
| Frequency | Near real-time via API; feed refresh per schedule | reported |

### 3.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v2/businesses/{businessId}/offer-stocks/updates` | reported |
| Granularity | Per offer per warehouse (`warehouseId`) | reported |
| Models | FBS (seller), FBY (Yandex fulfillment) | reported |

### 3.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v1/businesses/{businessId}/orders` (filter by status/date) | reported |
| Webhooks | Order create/update, status change, chat, returns, reviews | reported |
| Models | FBS, FBY, DBS, Express | reported |

### 3.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | `/v1/businesses/{businessId}/returns` | reported |
| Flow | Buyer request → seller accept/reject → refund | reported |

### 3.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| Campaigns list | 1,000 req/hour | reported |
| General | Not publicly documented; 429 with `Retry-After` | inferred |

### 3.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Availability | Test environment (`api.partner.market.yandex.ru` with test token) | reported |

### 3.10 Regional/Legal Constraints
- Russian entity or CIS entity with Russian tax registration
- Mandatory GTIN for most categories
- Data localization (152-FZ)
- YML feed must be HTTPS-accessible

### 3.11 Docs URL
https://yandex.ru/dev/market/partner-api/doc/ru/

---

## 4. Megamarket (СберМегамаркет)

### 4.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | API Token (single per cabinet) + Basic Auth for webhooks | reported |
| Header | `Authorization: Bearer <token>` (merchant→MM); Basic Auth (MM→merchant) | reported |
| Token source | Seller Cabinet → Settings → API Integration → Generate Token | reported |
| Expiry | Unlimited (revocable) | reported |
| Environments | Separate tokens for test/production | reported |

### 4.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST (POST only for merchant endpoints) + Webhooks (MM→merchant) | reported |
| Base URL | Merchant-hosted HTTPS endpoint (MM calls merchant) | reported |
| Format | JSON | reported |
| SSL | Valid CA-signed cert required; no self-signed | reported |

### 4.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | Feed-based (YML/CSV/JSON via FTP/HTTP) + API for stock/price | reported |
| Feed support | Primary method; scheduled pull by MM | reported |
| Required attributes | Category-specific; GTIN/EAN; brand; model | reported |
| Category mapping | MM category tree (provided in cabinet) | reported |
| Media | URLs in feed; max 20 MB; JPEG/PNG | reported |
| Moderation | Async; status in cabinet | reported |

### 4.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | API: `/prices/update` (merchant-hosted); Feed: price element | reported |
| Frequency | Feed: per schedule; API: on-demand | reported |

### 4.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | API: `/stocks/update` (merchant-hosted); Feed: stock element | reported |
| Models | FBS, FBO, DBS, C&C, P&C | reported |

### 4.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Webhooks (MM→merchant) | `order/new`, `order/cancel`, `order/confirm`, `order/packing`, `order/reject`, `order/shipping`, `sticker/print`, `order/search`, `order/get` | reported |
| Merchant→MM API | Not documented (callback model) | inferred |

### 4.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Webhooks | `return/new`, `return/confirm`, `return/cancel` (per wiki) | reported |

### 4.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| Not documented | Likely IP-based on merchant endpoint | inferred |

### 4.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Availability | Test token + test environment | reported |

### 4.10 Regional/Legal Constraints
- Russian entity (Sber ecosystem)
- SSL cert from trusted CA
- Data localization
- Integration requires personal manager approval for API activation

### 4.11 Docs URL
https://partner-wiki.megamarket.ru/merchant-api/ (auth required)  
https://openapi.megamarket.ru/ (403 public)

---

## 5. Avito

### 5.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | OAuth 2.0 Client Credentials (app-specific) + Authorization Code (user data) | reported |
| Token endpoint | `https://api.avito.ru/token` | reported |
| Header | `Authorization: Bearer <access_token>` | reported |
| Expiry | 24 hours (access token); refresh via client_credentials | reported |
| Scopes | Per-API (Ads, Chat, Delivery, Autoload, Balance, etc.) | reported |

### 5.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST (OpenAPI 3.0) | reported |
| Base URL | `https://api.avito.ru` | reported |
| Domains | 51 separate APIs (Ads, Chat, Delivery, Autoload, Stats, etc.) | reported |
| Format | JSON | reported |

### 5.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | API (`/ads` endpoints) + Autoload API (bulk) | reported |
| Feed support | Autoload = feed-based (XML/JSON) | reported |
| Required attributes | Category-specific via `/categories/list` | reported |
| Category mapping | Category tree with parameters | reported |
| Media | Upload via `/media` endpoints; max 50 MB | reported |
| Moderation | Async; status in ad object | reported |

### 5.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `PATCH /ads/{id}/price` | reported |

### 5.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `PATCH /ads/{id}/quantity` | reported |

### 5.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | Avito Delivery API: `/orders`, `/orders/{id}/status` | reported |
| Models | Avito Delivery (C2C/B2C), Pickup points | reported |

### 5.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoints | Delivery API returns flow | reported |

### 5.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| Not publicly documented | Per-app quotas; 429 with Retry-After | inferred |

### 5.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Availability | Pre-production environment | reported |

### 5.10 Regional/Legal Constraints
- Russian entity or verified individual
- Category restrictions (no weapons, pharma, etc.)
- Avito Delivery requires separate contract
- Data localization

### 5.11 Docs URL
https://www.avito.ru/developers  
https://developers.avito.ru/api-catalog

---

## 6. Kaspi.kz (CIS — Kazakhstan)

### 6.1 Authentication
| Attribute | Value | Source |
|-----------|-------|--------|
| Model | X-Auth-Token header (seller-generated) | reported |
| Header | `X-Auth-Token: <token>` | measured (guide.kaspi.kz) |
| Token source | Seller Cabinet → Settings → API Token | reported |
| Expiry | Unlimited (revocable) | reported |
| Format | JSON API (vnd.api+json) | reported |

### 6.2 API Style
| Attribute | Value | Source |
|-----------|-------|--------|
| Protocol | REST (JSON API spec) | reported |
| Base URL | `https://kaspi.kz/shop/api/v2/` | reported |
| Versioning | Path `/v2/` | reported |
| Format | `application/vnd.api+json` | reported |
| Pagination | `page[number]` + `page[size]` (max 100) | reported |

### 6.3 Product Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Method | API (`POST /products`) | reported |
| Feed support | Not documented | inferred |
| Required attributes | Category-specific; GTIN/EAN; brand | reported |
| Category mapping | Category tree via API | reported |
| Media | Image URLs in product create/update | reported |
| Moderation | Async; status in product object | reported |

### 6.4 Price Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `PATCH /products/{id}` (price field) | reported |

### 6.5 Stock Update
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `PATCH /products/{id}` (stock/quantity field) | reported |

### 6.6 Order Import
| Aspect | Detail | Source |
|--------|--------|--------|
| Endpoint | `GET /orders` with filters (`filter[orders][state]`, `filter[orders][creationDate]`) | measured (guide.kaspi.kz) |
| Includes | `include[orders]=user` | measured |
| Models | Pickup, Delivery | reported |

### 6.7 Returns
| Aspect | Detail | Source |
|--------|--------|--------|
| Not documented | Likely via order status transitions | inferred |

### 6.8 Rate Limits
| Scope | Limit | Source |
|-------|-------|--------|
| Not documented | Page size max 100; likely per-token quotas | inferred |

### 6.9 Sandbox
| Aspect | Detail | Source |
|--------|--------|--------|
| Not documented | No public sandbox | inferred |

### 6.10 Regional/Legal Constraints
- Kazakhstan entity (IP/TOO) or CIS with local tax registration
- Kaspi Bank account required
- Contract with Kaspi.kz Marketplace
- Kazakh/Russian language support
- Data residency in Kazakhstan

### 6.11 Docs URL
https://guide.kaspi.kz/partner/ru/shop/api/general/q3193  
https://kaspi.kz/merchantcabinet/support/pages/viewpage.action?pageId=917615 (Confluence, auth required)

---

## Comparison Table

| Capability | Ozon | Wildberries | Yandex Market | Megamarket | Avito | Kaspi.kz |
|------------|------|-------------|---------------|------------|-------|----------|
| **Auth** | Client-Id + Api-Key | JWT per domain | API-Key (OAuth legacy) | Bearer token + Basic | OAuth2 Client Cred | X-Auth-Token |
| **API Style** | REST (POST-heavy) | REST (13 subdomains) | REST + Webhooks | Webhook-first (merchant-hosted) | REST (51 APIs) | JSON API (REST) |
| **Product Import** | API only | API only | API + YML Feed | Feed (YML) + API | API + Autoload Feed | API |
| **Category Mapping** | Tree + attributes | Subject + charcs | Category tree + mapping | MM category tree | Category tree | Category tree |
| **Media** | API upload (3600px) | API upload (50MB) | URLs in feed/API | URLs in feed | Media API | URLs in product |
| **Moderation** | Async + status API | Async + error list | Async + state | Async (cabinet) | Async (ad status) | Async |
| **Price Write** | `/v1/product/import/prices` | `/api/v2/upload/task` | `/v2/.../offer-prices/updates` | Feed + `/prices/update` | `PATCH /ads/{id}/price` | `PATCH /products/{id}` |
| **Stock Write** | `/v2/products/stocks` | `PUT /api/v3/stocks/{wh}` | `/v2/.../offer-stocks/updates` | Feed + `/stocks/update` | `PATCH /ads/{id}/qty` | `PATCH /products/{id}` |
| **Order Read** | Posting APIs (FBO/FBS) | Orders APIs (FBS/FBW/DBS) | `/v1/.../orders` + webhooks | Webhooks (`order/new`) | Delivery API `/orders` | `GET /orders` |
| **Returns** | Returns API | Claims API | Returns API | Webhooks | Delivery API | Not documented |
| **Rate Limits** | ~50-100/min (unofficial) | Stats 1/min; others ~100-200/min | 1000/h (campaigns) | Not documented | Per-app quotas | Not documented |
| **Sandbox** | No (fixtures only) | No | Test env + token | Test token + env | Pre-prod env | No |
| **Official Docs** | docs.ozon.ru | dev.wildberries.ru | yandex.ru/dev/market | partner-wiki.megamarket.ru | developers.avito.ru | guide.kaspi.kz |
| **Legal Entity** | RU | RU/CIS | RU/CIS | RU | RU | KZ/CIS |
| **Certification** | GOST/TR CU via API | TR CU + ЧЗ via API | GTIN mandatory | GTIN/EAN | Category-dependent | GTIN/EAN |
| **Confidence** | High (OpenAPI) | High (OpenAPI) | High (official) | Medium (wiki + 3rd party) | High (OpenAPI catalog) | Medium (guide + 3rd party) |

---

## Read vs Write Coverage Matrix

| Operation | Ozon | WB | Yandex | Megamarket | Avito | Kaspi |
|-----------|------|-----|--------|------------|-------|-------|
| **Product Read** | ✅ `/v3/product/list` | ✅ `/content/v2/get/cards/list` | ✅ `/v2/.../offer-mappings` | ❌ (Feed only) | ✅ `/ads/{id}` | ✅ `GET /products` |
| **Product Write** | ✅ `/v3/product/import` | ✅ `/content/v2/cards/upload` | ✅ `/v2/.../offer-mappings` | ❌ (Feed only) | ✅ `POST /ads` | ✅ `POST /products` |
| **Price Read** | ✅ `/v5/product/info/prices` | ✅ `/api/v2/list/goods/filter` | ✅ `/v2/.../offer-prices` | ❌ (Feed only) | ✅ `/ads/{id}` | ✅ `GET /products` |
| **Price Write** | ✅ `/v1/product/import/prices` | ✅ `/api/v2/upload/task` | ✅ `/v2/.../offer-prices/updates` | ✅ API + Feed | ✅ `PATCH /ads/{id}/price` | ✅ `PATCH /products/{id}` |
| **Stock Read** | ✅ `/v1/product/info/stocks...` | ✅ `/api/v3/stocks/{wh}` | ✅ `/v2/.../offer-stocks` | ❌ (Feed only) | ✅ `/ads/{id}` | ✅ `GET /products` |
| **Stock Write** | ✅ `/v2/products/stocks` | ✅ `PUT /api/v3/stocks/{wh}` | ✅ `/v2/.../offer-stocks/updates` | ✅ API + Feed | ✅ `PATCH /ads/{id}/qty` | ✅ `PATCH /products/{id}` |
| **Order Read** | ✅ Posting APIs | ✅ Orders APIs | ✅ `/v1/.../orders` | ✅ Webhook `order/new` | ✅ `/orders` | ✅ `GET /orders` |
| **Order Write** | ✅ Status transitions | ✅ Confirm/assemble/cancel | ✅ Status via API | ✅ Webhook `order/confirm` | ✅ Delivery status | ❓ |
| **Returns Read** | ✅ `/v1/returns/list` | ✅ `/api/v1/claims` | ✅ `/v1/.../returns` | ✅ Webhook `return/new` | ✅ Delivery API | ❓ |
| **Returns Write** | ✅ Giveout/barcode | ✅ `PATCH /api/v1/claim` | ✅ Accept/reject | ✅ Webhook `return/confirm` | ✅ Delivery API | ❓ |
| **Finance Read** | ✅ `/v1/finance/*` | ✅ `/api/v1/supplier/sales` | ✅ Reports API | ❓ | ✅ Balance API | ❓ |
| **Analytics** | ✅ Premium API | ✅ Statistics API | ✅ Reports | ❓ | ✅ Stats API | ❓ |

---

## Blockers & Hard Constraints

### Universal Blockers
1. **Account required for all write operations** — No anonymous/sandbox write access on any platform
2. **Legal entity + contract** — Must sign marketplace agreement before API tokens issued
3. **Certification/GOST/TR CU** — Mandatory for regulated categories (cosmetics, kids, electronics, food, pharma)
4. **Data localization (152-FZ)** — Personal data must stay in Russia (Kaspi: Kazakhstan residency)
5. **GTIN/EAN mandatory** — Yandex Market, Kaspi, Megamarket require valid barcodes for most categories

### Platform-Specific Blockers

| Platform | Blocker | Severity |
|----------|---------|----------|
| **Ozon** | No public sandbox; write tests require production account | High |
| **Ozon** | Finance API window ≤31 days; auto-split needed | Medium |
| **Ozon** | Premium Plus required for feedback answer; Premium for chat | Medium |
| **WB** | 12 separate token scopes; wrong token → EntitlementError | High |
| **WB** | Stats API hard limit 1 req/min (FR-027) | High |
| **WB** | Price quarantine if <⅓ reference price (auto-block) | High |
| **WB** | No sandbox; frequent API changes (versioning) | Medium |
| **Yandex** | YML feed must be HTTPS-accessible; scheduled pull | Medium |
| **Yandex** | GTIN mandatory for most categories | High |
| **Megamarket** | Merchant must host HTTPS endpoint with valid CA cert | High |
| **Megamarket** | API activation requires personal manager approval | High |
| **Megamarket** | No public OpenAPI spec; docs behind auth | Medium |
| **Avito** | Separate app registration per scope; review process | Medium |
| **Avito** | Avito Delivery requires separate contract | Medium |
| **Avito** | 51 APIs — complexity explosion | Medium |
| **Kaspi** | Kazakhstan entity + Kaspi Bank account mandatory | High |
| **Kaspi** | JSON API format (vnd.api+json) — non-standard tooling | Medium |
| **Kaspi** | No public sandbox; docs in Confluence (auth) | High |
| **Kaspi** | Returns/order write not well documented | Medium |

---

## Observed At
All local specs: 2026-11-02 (MARKETPLACE_APIS.md, endpoint indexes, spec.md)  
Web docs accessed: 2026-11-22  
Confidence reflects: measured (from OpenAPI), reported (official docs), inferred (community/third-party)