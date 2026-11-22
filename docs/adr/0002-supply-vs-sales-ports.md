# ADR 0002 — Supply adapters and sales adapters are different ports

**Status:** accepted · **Date:** 2026-11-22

## Context

A marketplace can be a source of goods (1688, Taobao) or a sales channel (Ozon, eBay), and sometimes
both (AliExpress, Amazon). A single `MarketplaceAdapter` with `readCatalog()` and `publish()` forces
every adapter to implement methods it does not have and blurs the failure modes: a sourcing failure
is a missing product, a sales failure is a lost order.

## Decision

Two ports:

- `SupplyAdapter`: `search()`, `fetchProduct()`, `fetchCategories()`, `createPurchaseOrder()`,
  `fetchPurchaseOrder()`.
- `SalesAdapter`: `validate()`, `publish()`, `updatePrice()`, `updateStock()`, `fetchOrders()`,
  `fetchReturns()`, `verify()`.

A platform that is both ships two adapters and two profiles. They may share HTTP plumbing, but not
a domain interface.

## Consequences

Positive:

- Clear ownership and failure semantics.
- The catalogue ingestion does not depend on a sales channel being available.
- A supply adapter can be tested without a seller account.

Negative:

- Two registries and two capability schemas.
- Some duplication for a both-role platform.

## Alternatives rejected

- One port with optional methods: every caller must check `supportsX`, and a missing method becomes
  a runtime error.
- Treating sourcing as "just another feed": loses purchase orders, MOQ and lead times.
