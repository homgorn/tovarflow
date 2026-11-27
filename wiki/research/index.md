---
id: "research-index"
title: "Research knowledge base"
tags:
  - research
  - index
sources:
  - (none)
confidence: "measured"
updated: "2026-11-27"
---

# Research knowledge base

**Tracks complete:** 8/9 · **Records:** 102 · **Marketplaces mapped:** 68 · **Inherited assets:** 14

Each track keeps a narrative `REPORT.md`, machine-readable `data.json` and a source/date on
every fact. The SQLite file `data/research.sqlite` holds the same records plus FTS5.

## Tracks

| Track | Status | Records | Report | Data |
|---|---|---|---|---|
| [[research/competitors\|Competitor Research Report — Q-Parser Platform]] | complete | 33 | [REPORT](../../docs/research/competitors/REPORT.md) | [data.json](../../docs/research/competitors/data.json) |
| [[research/marketplaces-ru\|RU Marketplace Capability Matrix]] | complete | 6 | [REPORT](../../docs/research/marketplaces/ru/REPORT.md) | [data.json](../../docs/research/marketplaces/ru/data.json) |
| [[research/marketplaces-cn\|Chinese Marketplaces: Supply vs Sales Channel Analysis]] | complete | 11 | [REPORT](../../docs/research/marketplaces/cn/REPORT.md) | [data.json](../../docs/research/marketplaces/cn/data.json) |
| [[research/marketplaces-global\|Global Marketplace API Comparison Report]] | complete | 16 | [REPORT](../../docs/research/marketplaces/global/REPORT.md) | [data.json](../../docs/research/marketplaces/global/data.json) |
| [[research/platforms\|Q-Parser Storefront Platform Research Report]] | complete | 11 | [REPORT](../../docs/research/platforms/REPORT.md) | [data.json](../../docs/research/platforms/data.json) |
| [[research/demand\|Demand Data Sources & Pipeline Research]] | complete | 25 | [REPORT](../../docs/research/demand/REPORT.md) | [data.json](../../docs/research/demand/data.json) |
| [[research/inherited\|inherited]] | pending | 0 | — | — |
| [[research/wordpress\|WordPress Synchronisation Transport & Architecture Decision (2026)]] | complete | 0 | [REPORT](../../docs/research/wordpress/REPORT.md) | [data.json](../../docs/research/wordpress/data.json) |
| [[research/admin\|Admin Console Decision: Medusa Admin Extended vs Separate Operator Console]] | complete | 0 | [REPORT](../../docs/research/admin/REPORT.md) | [data.json](../../docs/research/admin/data.json) |

## Marketplaces

- [[indexes/marketplaces-world]] — the full world coverage map with status and priority.

## Synthesis

- [SYNTHESIS.md](../../docs/research/SYNTHESIS.md) — cross-track decisions, gaps and build order.

## Decisions and assets

- [[research/inherited-assets]] — reusable projects and license policy.
- [[research/adr]] — architecture decision records.

## Query

```bash
python tools/query_research.py "WB token scope"
python tools/query_research.py --sql "select name,layer,role,status from marketplaces"
```
