# Domain model

> Status: proposed. The marketplace research may add channel-specific fields, but the
> invariants below should survive it.

## 1. Aggregates

```text
Tenant
  └── Storefront
  └── ChannelAccount ── Credential
  └── Supplier ── Source ── ParseRun ── SourceProduct
  └── CanonicalProduct ── Variant ── Offer
  └── Listing ── PriceObservation
  └── Order ── Return ── Settlement
  └── MarginRule ── Proposal ── PolicyDecision ── Execution ── Verification
  └── Event (append-only)
```

## 2. Entities and invariants

### Tenant

The isolation boundary. Every domain row carries `tenant_id`. Object-storage keys are prefixed
with the tenant. RLS is enabled on all tenant tables.

### Supplier / Source / ParseRun

- `Supplier` is a commercial counterparty, not a website.
- `Source` is a concrete data origin: a Q-Parser domain, a feed URL, an API account.
- `ParseRun` maps to a Q-Parser parse id (`id1234567`) or an equivalent run in another supply
  adapter. It stores status, progress counters, archive flag, raw payload references and timings.
- A `ParseRun` is immutable once finished. Re-parsing creates a new run; it never mutates history.

### SourceProduct

The raw shape returned by a supply adapter, before normalisation:

```text
title, article, url, price, old_price, currency, brand, quantity, publish,
images[], file_links[], video_links[], category_title, category_url,
description, short_description, data{}
```

`data` is a map with human-readable keys. It is **not** a domain model. It is stored as
`attributes_raw JSONB` and mapped by a versioned attribute dictionary.

### CanonicalProduct / Variant / Offer

- `CanonicalProduct` is what a customer sees: title, brand, description, category, media,
  attributes.
- `Variant` is the sellable variation (size, colour, bundle).
- `Offer` is a supplier-specific commercial proposal for a variant: supplier, purchase price,
  currency, MOQ, stock, lead time, condition, warehouse.
- One product may have many offers. The storefront picks an offer by a pricing/availability
  policy, not by "the first one".

Invariants:

1. A variant belongs to exactly one canonical product.
2. An offer belongs to exactly one variant and one supplier.
3. Prices and costs are integer minor units + ISO-4217 currency. Never floats.
4. Unknown cost components are `NULL`, never `0`. A total with unknowns is marked
   `is_complete = false` and cannot be shown as final.
5. `publish` is tri-state: `true / false / null`. `null` means unknown, not "in stock".

### Identity and deduplication

Identity signals, in order of strength:

1. GTIN / EAN / UPC (when present and valid).
2. Brand + manufacturer article (normalised).
3. Source URL (same domain + path) for the same supplier.
4. Image hash + title similarity.
5. Manual confirmation.

Cross-supplier matches are **candidates**, stored in `product_identity_match` with individual
signals and a similarity score. They are never auto-merged. Merging destroys per-supplier
attribution and is practically irreversible.

### Category mapping

Channel categories are external, versioned taxonomies. We store:

- `category` — our internal tree;
- `channel_category` — external id, name, path, version;
- `category_mapping` — internal → external with confidence and review state.

A mapping is never edited in place without a new version. A channel taxonomy change must be
detectable by a diff job.

### Listing

A listing is a product/variant published to a channel account.

```text
listing(id, tenant_id, account_id, variant_id, external_id, offer_id,
        status, moderation_state, content_hash, raw_blob_ref, synced_at)
```

States: `draft → validated → submitted → moderation → live → paused → archived`,
plus `rejected` and `error`. Transitions are events, not overwrites.

`UNIQUE(account_id, external_id)`; `offer_id` is the seller-side article and must be stable.

### PriceObservation

Adopted from `C:\susa ai\alibaba ali temu\db\migrations\0002_pricing.sql`:

```text
price_observation(
  product_id, channel, destination_country, observed_at,
  currency, sale_price_minor, original_price_minor,
  commission_rate, delivery_days, shipping_minor, duty_minor,
  is_complete, price_anomaly, source, source_run_id
)
```

A price is a function of product **and** channel **and** destination, not a scalar. Daily rollups
survive raw-data retention. `original_price < sale_price` is stored as-is and flagged
(`original_lt_sale`), never silently corrected.

### MarginRule and pricing

```text
landed_cost = purchase_price
            + inbound_shipping
            + duty
            + certification
            + packaging
            + payment_fee

channel_price >= (landed_cost
                + fulfillment_cost
                + expected_return_loss
                + acquiring_fee
                + tax
                + fixed_channel_fee)
               / (1 - commission_rate - target_margin)
```

Rules are versioned per tenant, category and channel. The engine returns a **price range** and a
`min_price` floor; a policy may reject a price below the floor. Unknown components make the
result `incomplete`, and an incomplete price cannot be auto-published.

### Order / Return / Settlement

- `Order` is channel-specific but normalised: channel, account, external id, lines, amounts,
  currency, status, fulfilment model, created_at.
- `Return` references an order line and a reason code.
- `Settlement` is the money actually received, with commission, logistics, fines and adjustments.
  Unit economics are computed from settlements, not from list prices.

Order states: `new → acknowledged → shipped → delivered → closed`, plus `cancelled`,
`returned`, `lost`. Every transition is an event with a source (`channel`, `operator`, `system`).

### Proposal / Policy / Execution / Verification

This is the write-side aggregate, adopted from `H:\susa ai 500\wb china`:

```text
Proposal        typed intent (PRICE, STOCK, CARD_CONTENT, CARD_IMAGE, DELIST, ANSWER)
PolicyDecision  ALLOW | DENY | REQUIRE_APPROVAL | ESCALATE, with rule ids and version
Execution       idempotency_key, request hash, attempt, result, raw_blob_ref
Verification    OK | MISMATCH | UNKNOWN | SKIPPED, observed value, checked_at
```

Invariants:

1. No external write without an `ALLOW` decision (or an approval record).
2. Repeating the same `idempotency_key` returns the first result; it does not send a second request.
3. A price write is not "done" until `Verification = OK`.
4. A mismatch opens an incident; it does not retry blindly.

### Event

Append-only, tenant-scoped, monthly partitions. Fields: `id`, `tenant_id`, `type`, `aggregate`,
`aggregate_id`, `payload`, `actor`, `trace_id`, `created_at`. Events are the audit trail and the
source for reconciliation and morning reports.

## 3. Multi-store and multi-tenant

- `Storefront` belongs to a tenant and has its own domain, theme, locale, currency and catalogue
  filter.
- `ChannelAccount` belongs to a tenant and a channel profile.
- A product can be published to many storefronts and many channels without duplication: the
  canonical product is shared, the listing is per channel, the storefront visibility is a rule.

## 4. What is deliberately not modelled

- Marketplace-specific raw fields in the core. They live in `raw_blob_ref` and in adapter DTOs.
- A single global price. Price is contextual.
- A single global stock. Stock is per offer and warehouse.
- Automatic cross-supplier merging. Candidates only.
- Customer accounts before the first storefront checkout. The model allows them, but the first
  slice does not need them.
