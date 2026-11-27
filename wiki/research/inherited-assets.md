---
id: "inherited-assets"
title: "Inherited assets"
tags:
  - research
  - assets
  - reuse
sources:
  - (none)
confidence: "measured"
updated: "2026-11-27"
---

# Inherited assets

Existing projects on this machine that we reuse instead of rebuilding.

## architecture

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Proposal -> Policy -> Execution -> Verification | `H:/susa ai 500/wb china/docs/architecture/` | proprietary, owner's project | adopt | ADR-001 hexagonal core, ADR-006 no browser in nightly, ADR-007 MCP as product. |

## contract

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Marketplace adapter specification | `H:/susa ai 500/wb china/docs/specs/002-marketplace-adapters/spec.md` | proprietary, owner's project | adopt | Capability profiles, error mapping, rate limiter, idempotency, contract tests. |

## demand

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Demand metrics and niche model | `C:/susa ai/niche-radar/docs/data-model.md` | check repository LICENSE | adopt or sidecar | B/R/A/G/C/P, priority_v1, niches, hypotheses, read-only MCP. |

## knowledge

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Atomised knowledge contract | `C:/susa ai/china auto/wiki/SCHEMA.md` | check repository LICENSE | adopt | concept/source/finding/question, confidence, status, resolves_when. |

## marketplace-spec

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Ozon Seller API OpenAPI schema | `H:/susa ai 500/wb china/ozon-seller-api-openapi.json` | vendor terms; keep local | read-only reference | 4.25 MB, 482 paths. Do not commit; fetch with a script. |
| Wildberries 13 OpenAPI specs | `H:/susa ai 500/wb china/wb-api-specs/` | vendor terms; keep local | read-only reference | general, products, orders FBS/DBW/DBS, pickup, FBW, promotion, communications, tariffs, analytics, reports, finances. |

## policy

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Open-source stack and license traps | `H:/susa ai 500/wb china/docs/competitive/OPENSOURCE_STACK.md` | proprietary, owner's project | adopt | MIT repricer, MCP catalogs, GPL/AGPL traps, Temporal/Redis choices. |

## research

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| RU seller-tools market graph | `H:/susa ai 500/wb china/docs/market/KNOWLEDGE_GRAPH.md` | proprietary, owner's project | merge | JAFO, MPSTATS, Kirsty, MPSpace, TrueStats, SalesFinder; capability matrix. |
| Xianyu / Goofish negative results | `C:/susa ai/goofish/DECISION.md` | owner's project | avoid | ToS bans automation, CSR shell, CN phone + real-name, payment blockers. |

## schema

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Destination-aware price observation schema | `C:/susa ai/alibaba ali temu/db/migrations/0002_pricing.sql` | check repository LICENSE | adopt | price is a function of product + destination; is_complete; daily rollup; fake-discount anomaly. |
| Marketplace platform Postgres schema | `H:/susa ai 500/wb china/docs/data/schema.sql` | proprietary, owner's project | adopt and extend | tenant/RLS, account/credential, product/listing/offer/price_history, orders, proposal/policy/execution/verification/event. |
| Product identity candidate model | `C:/susa ai/alibaba ali temu/db/migrations/0002_pricing.sql` | check repository LICENSE | adopt | candidate matches with signals, never auto-merged. |

## storefront

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Static-first storefront with .md twins and llms.txt | `C:/susa ai/alibaba ali temu/apps/web/` | check repository LICENSE | adopt | server-rendered HTML, L7 guard, sitemap, llms.txt. |

## verification

| Asset | Path | License | Reuse | Notes |
|---|---|---|---|---|
| Crawler-view site verification | `C:/susa ai/china auto/tools/verify_site.py` | check repository LICENSE | adopt | checks the raw HTTP response, not the rendered DOM. |

See [ASSETS.md](../../docs/research/inherited/ASSETS.md) for the full registry.
