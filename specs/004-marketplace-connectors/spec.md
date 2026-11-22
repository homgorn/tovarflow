# Spec 004 — Marketplace connectors

**Status:** draft for approval · **Date:** 2026-11-22 · **Depends on:** constitution, specs 001–002.

## 1. Why

Marketplace integrations are where catalogue platforms die: auth expires, a price write is
retried twice, a card is rejected by moderation, a category mapping is wrong, and nobody can tell
which listing produced which order. This spec defines one adapter contract for RU, CN and global
channels, and a write path that is safe enough to run unattended.

## 2. Scope and layers

| Layer | Channels in scope | First release |
|---|---|---|
| `ru` | Ozon, Wildberries, Yandex Market, Megamarket, Avito, Kaspi | Ozon, WB, Yandex |
| `cn` | 1688, Taobao, Alibaba.com, AliExpress, Ozon Global, WB China, Temu, Xianyu | Ozon Global, WB China (sales); 1688 via partner (supply) |
| `global` | Amazon, eBay, Etsy, Walmart, TikTok Shop, Allegro, Kaufland, Bol, Cdiscount, Zalando, Mercado Libre, Shopee, Lazada, Rakuten | eBay, Etsy |
| `feeds` | Google Merchant, Meta, Microsoft, Pinterest | Google Merchant |

A channel has a **role**: `supply`, `sales` or `both`. Supply adapters and sales adapters are
different ports. They do not share a base class.

## 3. User scenarios

### US1 — Publish a listing (P0)
As an operator, I want a validated product to become a live listing on a channel.

Acceptance:
1. `validate()` runs before `publish()`; a missing required attribute fails locally.
2. The card is submitted; the channel returns an external id or a moderation task.
3. The listing state becomes `submitted` then `moderation` then `live`, or `rejected` with a reason.
4. A duplicate submission with the same idempotency key does not create a second card.
5. The raw request/response is stored.

### US2 — Change a price (P0)
As an operator, I want a price change to be applied once and verified.

Acceptance:
1. The proposal carries old price, new price, reason and floor.
2. Policy returns `ALLOW`, `DENY` or `REQUIRE_APPROVAL`.
3. Execution sends one request; a retry with the same key sends none.
4. Verification re-reads the price; `MISMATCH` opens an incident.
5. A price below the floor is denied before HTTP.

### US3 — Sync stock (P0)
As an operator, I want stock to reflect the supplier's real availability.

Acceptance:
1. Unknown stock is not sent as zero.
2. A zero stock update is explicit and verified.
3. A channel that requires warehouse-level stock receives the right warehouse mapping.
4. A stock write failure does not block a price write and vice versa.

### US4 — Import orders (P0)
As an operator, I want orders from a channel to become normalised orders.

Acceptance:
1. Orders are fetched with a cursor; the cursor is persisted.
2. An order is idempotent by `(channel, account, external_id)`.
3. Status transitions are mapped to the canonical state machine.
4. Tracking is pushed back and verified.
5. A return is stored with a reason code.

### US5 — Know the capability before calling (P0)
As a developer, I want a capability profile, so that the core never guesses whether a method exists.

Acceptance:
1. `capabilities()` returns booleans and enum values for product import, price, stock, orders,
   returns, chat, ads.
2. A disabled capability raises `EntitlementError` before HTTP.
3. A new region is added by a profile, not by a code branch.

### US6 — Certify a connector (P1)
As a release manager, I want a certification suite, so that "done" is measurable.

Acceptance:
1. Contract tests cover every implemented method with fixtures from the official spec.
2. A sandbox or a recorded account run passes.
3. A write is verified by re-read.
4. Rate-limit and auth-expiry scenarios pass.
5. The connector is marked L5 only after the suite is green in CI.

## 4. Adapter contract

```ts
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
```

`WriteContext` is mandatory: `tenantId`, `accountId`, `proposalId`, `policyDecisionId`,
`idempotencyKey`, `traceId`.

Rules:

- Adapters return DTOs, not raw JSON.
- HTTP errors are mapped inside the adapter.
- `validate()` is mandatory before `publish()`.
- `verify()` is mandatory after price and stock writes.
- No adapter stores a secret beyond the call.

## 5. Write path

```text
Intent -> Proposal -> PolicyDecision -> Execution -> Verification -> Event
```

Policy rules (v1):

| Rule | Example | Decision |
|---|---|---|
| Floor price | new price < floor | DENY |
| Max daily change | > 20% in 24h | REQUIRE_APPROVAL |
| Stock sanity | qty > 10x last known | REQUIRE_APPROVAL |
| Forbidden category | channel prohibits the category | DENY |
| Missing rights | no content right record | DENY |
| Auth invalid | key expired | DENY + account pause |
| First publish | new listing | ALLOW if validated |

Autonomy levels: `L0_SHADOW` (observe, no write), `L1_ASSIST` (proposal only),
`L2_GUARDED` (write with policy), `L3_AUTO` (write within limits). Default is `L0_SHADOW` for a
new channel; `L2_GUARDED` for a proven channel.

## 6. Error taxonomy

`AuthError`, `EntitlementError`, `ValidationError`, `RateLimitError`, `TransientError`,
`ModerationError`, `UnknownError`.

Mapping rules:

- 401/403 → `AuthError`; pause the account, do not retry.
- 429 → `RateLimitError`; honor `Retry-After`, then exponential backoff.
- 5xx/timeout → `TransientError`; retry with jitter, max 5.
- 400/422 with a field list → `ValidationError`; do not retry, route to mapping fix.
- A card rejected in moderation → `ModerationError`; operator queue.

## 7. Rate limiting and scheduling

- A limiter per `(tenant, account, scope)`, not per process.
- Limit values come from the capability profile; unknown means conservative.
- 429 pauses the scope for `Retry-After` or 60 s.
- Three consecutive 429s pause the account and raise an alert.
- Price and stock jobs are split; a stock flood must not starve price updates.
- Order polling has its own budget.

## 8. Capability profile

Every channel ships `profiles/<layer>/<channel>.json`:

```json
{
  "id": "ru.wildberries",
  "layer": "ru",
  "role": "sales",
  "auth": { "type": "token", "scopes": ["content", "marketplace", "statistics", "prices"] },
  "api": { "style": "rest", "base_url": "https://suppliers-api.wildberries.ru", "spec_dir": "local" },
  "capabilities": { "product_import": "api", "price_write": true, "stock_write": true,
                    "order_read": true, "returns": true, "chat": true, "ads": true },
  "limits": { "rate": null, "page_size": null },
  "requirements": { "entity": "RU/EAEU", "moderation": true, "sandbox": null },
  "content": { "language": "ru", "currency": "RUB" },
  "maturity": "research"
}
```

Unknown values are `null`. A profile with `null` limits cannot run at `L3_AUTO`.

## 9. First cohort and acceptance

### Ozon (L2)
- Read products, write price and stock, verify by re-read.
- 20 methods covered by contract tests.
- Auth expiry → `AuthError`, account paused.
- Price write idempotent.

### Wildberries (L2)
- Category-scoped tokens; missing token → `EntitlementError` before HTTP.
- Price drop > 3x produces a quarantine warning in `WriteResult`.
- Stats rate limit respected by the scheduler.
- Contract tests from the 13 local specs.

### Yandex Market (feed-first, L2)
- YML feed validates.
- Category mapping is complete.
- A price/stock update via the Partner API is verified.

### Google Merchant Center (feed, L1/L2)
- Service-account auth; DataSource + ProductInputs.
- GTIN-centric mapping; price and availability attributes.
- No sandbox; a test Merchant Center account is used.
- This is the first non-RU channel because it has no seller-account gate and no write sandbox
  friction.

### Bol.com (L2)
- OAuth2 client credentials; 299-second JWT.
- Offers API for EAN-based price/stock; `process-status` polling for async writes.
- Demo environment with fixed sample data.

### Walmart (L2)
- OAuth2 client credentials; 15-minute tokens.
- Feeds + Items/Inventory/Orders; dynamic sandbox.
- Delegated access is required for the SaaS phase.

## 10. Acceptance scenarios

```gherkin
Scenario: duplicate price write
  Given a price proposal with idempotency key K
  When execution is retried with K
  Then only one HTTP request is sent
  And the second call returns the first result

Scenario: price below floor
  Given a floor of 1000 RUB
  When a proposal sets 900 RUB
  Then policy returns DENY
  And no HTTP request is sent

Scenario: missing WB token
  Given an account without the "marketplace" token
  When an order read is requested
  Then EntitlementError is raised before HTTP
  And the account is not paused

Scenario: moderation rejection
  Given a card rejected for a missing attribute
  When the rejection is received
  Then the listing state is rejected
  And the reason is stored
  And the operator sees a fix queue

Scenario: verification mismatch
  Given a price write returns 200
  When the re-read returns the old price
  Then Verification is MISMATCH
  And an incident is opened
  And no blind retry happens
```

## 11. Out of scope

- Full coverage of all 482 Ozon or 290 WB methods.
- Browser automation in autonomous paths.
- Unofficial/private APIs.
- Advertising bid management in the first release.
- Global channels before the RU loop is proven.

## 12. Open questions

- Exact rate limits for Ozon and WB price writes.
- Which channels expose sandboxes, and which require a live account.
- Does Ozon Global / WB China reuse the RU API surface or a separate one?
- Which global channels accept a non-local entity?
- Which connectors require GTIN/EAN, and which accept custom SKUs?
