# Marketplace layers: RU, CN, global, CIS

> Status: proposed, 2026-11-22. Platform details marked `research` are being verified by the
> parallel research tracks. Do not treat an unverified cell as a contract.

## 1. Why separate layers

RU, Chinese and global channels differ in almost every dimension that matters to an integration:

| Dimension | RU | CN | Global |
|---|---|---|---|
| Entity required | RU/EAEU seller | Chinese business licence for domestic platforms | Local entity or marketplace Global programme |
| Auth | Client-Id + Api-Key, JWT tokens | OAuth / app review / partner agreements | OAuth2, LWA, app review |
| Content language | Russian | Chinese | English + local language |
| Currency / tax | RUB, VAT | CNY, export VAT, customs | Local currency, VAT/GST/sales tax |
| Fulfilment | FBO / FBS / DBS | Domestic or cross-border consolidation | FBA / 3PL / dropship |
| Demand signals | Wordstat, marketplace analytics | 1688/Taobao search, Douyin | Google, Amazon, TikTok |
| Legal | 152-FZ, labelling, certification | Export licences, product safety | GDPR, DSA, product compliance |

Trying to model these as one `Marketplace` table with nullable columns produces a table where
half the fields are always empty and nobody knows which half. The layer model keeps the shared
kernel small and makes each region's rules explicit.

## 2. Layer model

```text
connectors/
  kernel/            adapter port, capability profile, errors, rate limiter, idempotency
  ru/                Ozon, Wildberries, Yandex Market, Megamarket, Avito, Kaspi
  cn/                1688, Taobao, Tmall, Pinduoduo, JD, Douyin, Alibaba.com, AliExpress,
                     Temu, Ozon Global, WB China, Xianyu
  global/            Amazon, eBay, Etsy, Walmart, TikTok Shop, Allegro, Kaufland, Bol,
                     Cdiscount, Zalando, Mercado Libre, Shopee, Lazada, Rakuten
  profiles/          JSON capability profiles, one file per channel
```

A connector is **not** a folder of HTTP calls. It is a profile plus a thin adapter that implements
the kernel port. The kernel owns retries, rate limits, idempotency, raw capture and error mapping.

## 3. Role: supply vs sales

This distinction is more important than geography:

| Role | What it means | Examples |
|---|---|---|
| `supply` | We read a catalogue and/or place purchase orders | Q-Parser, 1688, Taobao, Alibaba.com, supplier CSV |
| `sales` | We publish listings and receive orders | Ozon, WB, Yandex Market, eBay, Etsy, Amazon |
| `both` | Same platform used for sourcing and selling | AliExpress (affiliate + seller), Amazon (retail + SP-API) |

A `supply` adapter produces `SourceProduct` and `PurchaseOrder`. A `sales` adapter consumes
`ListingDraft` and produces `OrderDTO`. They must not share a port: the payloads and failure
modes are different.

## 4. RU layer

| Channel | Role | API status | Evidence | Confidence | Notes |
|---|---|---|---|---|---|
| Ozon Seller | sales | official REST, 482 paths | local OpenAPI 4.25 MB | measured | Client-Id + Api-Key; no write sandbox; moderation; Premium for some reads |
| Wildberries | sales | official REST, 13 specs | local 13 YAML specs | measured | 12–13 category-scoped JWT tokens; Stats 1 req/min; 3 consecutive 429 pauses account |
| Yandex Market | sales | Partner API | official docs | measured | Api-Key with granular scopes; `pageToken`, limit max 100; feed + API |
| Megamarket | sales | feed / API | official docs | research | YML/XML first |
| Avito | sales | API | official docs | research | Classifieds model, not classic marketplace |
| Kaspi.kz | sales (CIS) | API | official docs | research | Kazakhstan entity/payment specifics; no write sandbox |

## 5. CN layer

| Channel | Role | Public API for a foreign entity | Evidence | Confidence | Notes |
|---|---|---|---|---|---|
| 1688 | supply | yes for a foreign developer account; procurement needs a CN receiving entity | inherited research | reported | `alibaba.product.get`, wholesale search; domestic CN logistics only |
| Taobao / Tmall | supply | affiliate API only (Taobao Union Overseas); no seller API | inherited research | reported | Foreign corp OK; `adzone_id`; 3-day cookie; affiliate, not sourcing |
| Pinduoduo | supply | no public API | inherited research | reported | Merchant platform is for own stores only |
| JD.com | supply / sales | requires Chinese entity | official docs | research | POP API |
| Douyin | sales | requires Chinese entity | official docs | research | Domestic CN only |
| Alibaba.com | supply | B2B API / RFQ | official docs | research | Export-oriented; Russia blocked for affiliate |
| AliExpress | sales / affiliate | seller API + affiliate API | inherited research | reported | Cross-border |
| Temu | sales | no public API | inherited research | measured | Do not build a connector on rumours |
| Ozon Global | sales | programme requires a Chinese legal entity | inherited research | reported | **Blocked** until the entity exists |
| WB China | sales | programme requires a Chinese legal entity | inherited research | reported | **Blocked** until the entity exists; strict 2FA |
| Xianyu / Goofish | supply | no public API; ToS blocks | `C:\susa ai\goofish` | measured | **Do not integrate** |

## 6. Global layer

| Channel | Role | API | Difficulty (hypothesis) | Confidence | Notes |
|---|---|---|---|---|---|
| eBay | sales | Sell APIs | medium | research | Sandbox available |
| Etsy | sales | Open API v3 | medium | research | OAuth2, app review |
| Amazon | sales | SP-API | hard | research | LWA, multiple roles, strict feeds |
| Walmart | sales | Marketplace API | hard | research | Approval required |
| TikTok Shop | sales | Partner API | hard | research | Region-specific |
| Allegro | sales | REST API | medium | research | Poland/CEE |
| Kaufland | sales | Seller API | medium | research | EU |
| Bol.com | sales | API | medium | research | NL/BE |
| Cdiscount | sales | API | medium | research | FR |
| Zalando | sales | Partner API | hard | research | Fashion only |
| Mercado Libre | sales | API | medium | research | LATAM |
| Shopee | sales | Open Platform | hard | research | SEA |
| Lazada | sales | Open Platform | hard | research | SEA |
| Rakuten | sales | RMS API | hard | research | Japan |
| Google Merchant | demand | Content API / feeds | easy | research | Feed, not a marketplace |
| Meta Commerce | demand | Catalog API | easy | research | Feed, not a marketplace |

## 7. Capability profile

Every channel has one JSON profile. Unknown values are `null`, never guessed.

```json
{
  "id": "ru.ozon.seller",
  "layer": "ru",
  "role": "sales",
  "display_name": "Ozon Seller",
  "auth": { "type": "header", "headers": ["Client-Id", "Api-Key"] },
  "api": {
    "style": "rest",
    "base_url": "https://api-seller.ozon.ru",
    "spec_path": "H:/susa ai 500/wb china/ozon-seller-api-openapi.json",
    "spec_version": null
  },
  "capabilities": {
    "product_import": "api",
    "price_write": true,
    "stock_write": true,
    "order_read": true,
    "returns": true,
    "chat": true,
    "ads": true
  },
  "limits": { "rate": null, "page_size": null, "concurrent_writes": null },
  "requirements": {
    "entity": "RU/EAEU",
    "moderation": true,
    "sandbox": false,
    "certification": true
  },
  "content": { "language": "ru", "currency": "RUB" },
  "maturity": "research"
}
```

## 8. Adapter contract

```ts
type Layer = "ru" | "cn" | "global" | "cis";
type Role = "supply" | "sales" | "both";

interface MarketplaceAdapter {
  profile(): CapabilityProfile;

  health(): Promise<Health>;

  validate(input: ListingDraft): Promise<ValidationResult>;

  publish(input: ListingDraft, ctx: WriteContext): Promise<WriteResult>;

  updatePrice(input: PriceUpdate, ctx: WriteContext): Promise<WriteResult>;

  updateStock(input: StockUpdate, ctx: WriteContext): Promise<WriteResult>;

  fetchOrders(cursor: Cursor): Promise<Page<OrderDTO>>;

  fetchReturns(cursor: Cursor): Promise<Page<ReturnDTO>>;

  verify(ref: ExternalRef): Promise<VerificationResult>;
}

interface WriteContext {
  tenantId: string;
  accountId: string;
  proposalId: string;
  policyDecisionId: string;
  idempotencyKey: string;
  traceId: string;
}
```

Rules:

1. Adapters return normalised DTOs, never raw JSON.
2. Raw payload is stored before mapping; the DTO carries `raw_blob_ref`.
3. HTTP errors are mapped inside the adapter. Nothing HTTP-shaped escapes into the core.
4. `validate()` is mandatory before `publish()`; a channel-side rejection must be predicted
   locally wherever the channel publishes its rules.
5. `publish()` is not a full-catalogue operation. It is one listing or one batch with a cursor.
6. `verify()` is not optional for price and stock writes.

## 9. Error taxonomy

| Error | Meaning | Retry? | Action |
|---|---|---|---|
| `AuthError` | key expired/revoked | no | account → `auth_error`, notify |
| `EntitlementError` | method not included in plan/role | no | disable capability in profile |
| `ValidationError` | channel rejected the payload | no | fix mapping, do not retry |
| `RateLimitError` | 429 / quota | yes, `Retry-After` | backoff, then pause account |
| `TransientError` | 5xx, timeout | yes | exponential backoff, jitter |
| `ModerationError` | card rejected by channel | no | route to operator queue |
| `UnknownError` | unmapped | once | capture raw, escalate |

## 10. Connector maturity

| Level | Definition | Exit criteria |
|---|---|---|
| L0 | Docs only | capability profile + official spec stored |
| L1 | Read | products/orders read on a real account |
| L2 | Price + stock write | write verified by re-read, idempotency tested |
| L3 | Full publish | card created/updated, moderation state tracked |
| L4 | Orders + returns | order import, tracking push, returns |
| L5 | Certified | channel certification/sandbox suite passes in CI |

A connector is not "done" because it compiles. It is done at L4, and only a verifier can mark it.

## 11. First cohort (hypothesis, 6/10)

RU first, because the Q-Parser catalogue and the existing Ozon/WB specs are RU-centric:

1. **Ozon Seller** — the official OpenAPI is already local; the write path is the best test of
   Proposal → Policy → Execution → Verification.
2. **Wildberries** — 13 official specs are local; category-scoped tokens are a good stress test
   for the entitlement model.
3. **Yandex Market** — feed-first, so it validates the YML pipeline before API writes.

Global: **Google Merchant Center** first (feed-based, service-account auth, no sandbox friction, and
it feeds Google Shopping/PMax), then **Bol.com** (clean OAuth2 client credentials, explicit
`process-status` polling) and **Walmart** (dynamic sandbox, delegated access for SaaS). Kaufland and
Allegro are the next EU pair. eBay and Etsy are P2: eBay has heavy per-API daily limits and Etsy's
Commercial Access is gated. Amazon SP-API is P1 but hard (LWA + RDT, per-operation token buckets).

CN: **1688** and **Taobao Union Overseas** are technically integrable as supply/affiliate sources;
**Ozon Global** and **WB China** require a Chinese legal entity, so they are blocked until that
entity exists. Do not build a direct 1688 seller connector from scratch: use the procurement API
with a CN receiving entity/forwarder.

## 12. Open questions for research

- Which RU channels have a real sandbox, and what does certification require?
- Does Ozon Global / WB China expose a separate API surface or reuse the RU one?
- Which global channels accept a non-local entity, and which require a local company?
- What are the actual rate limits for WB and Ozon price writes?
- Which Chinese sourcing APIs are legally available to a foreign entity, and through whom?
- Which channels require GTIN/EAN, and which accept custom SKUs?
