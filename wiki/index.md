---
id: "index"
title: "Q-Parser Knowledge Base"
tags:
  - qparser
  - index
sources:
  - https://q-parser.ru/howto/api
confidence: "measured"
updated: "2026-11-27"
---

# Q-Parser Knowledge Base

128 страниц документации Q-Parser, 16 REST-эндпоинтов, 72 формата выгрузки и 4 тарифа. Корпус собран 22.11.2026: 0 пропусков, 442 579 символов; каждый факт имеет URL-источник и дату.

| Артефакт | Значение | Источник |
|---|---|---|
| API-эндпоинты | 16 | https://q-parser.ru/howto/api |
| Форматы выгрузки | 72 | https://q-parser.ru/howto/format |
| Тарифы | 4 | https://q-parser.ru/tariffs |

**Corpus:** 128 pages · **API endpoints:** 16 · **Export formats:** 72 · **Tariff plans:** 4 · **Claims:** 15

This wiki is generated from the fetched corpus. Every page has a source URL and a SHA-256
in `docs/research/qparser/manifest.jsonl`. Facts are labelled `measured`, `reported` or `inferred`.

## Start here

- [[topics/api]] — the complete REST contract (16 methods).
- [[topics/limits-and-quotas]] — concurrency, pagination, trial limits.
- [[topics/formats]] — all 72 export formats by category.
- [[topics/pricing]] — Day / Lite / Pro / Trial.
- [[topics/webhooks]] — signed automation callbacks.
- [[topics/modifiers]] — product and image transforms before export.
- [[topics/ai]] — AI editing, image generation, watermark removal, AI Points.
- [[topics/storage]] — FTP/SFTP/S3 delivery.

## Indexes

- [[indexes/by-endpoint]]
- [[indexes/by-format]]
- [[indexes/by-platform]]
- [[indexes/by-marketplace]]
- [[indexes/claims]]
- [[indexes/sources]]

## Machine-readable artefacts

- `data/qparser.sqlite` — sources, pages, chunks, endpoints, formats, plans, claims, edges + FTS5.
- `data/qparser.graph.json` — nodes and edges with provenance.
- `data/qparser.graphml` — the same graph for Gephi / yEd.
- `docs/research/qparser/extracted/` — raw structured JSON.

## Research tracks

- [[research/index]] — all research tracks, records and gaps.
- [[research/inherited-assets]] — reusable projects and license policy.
- [[indexes/marketplaces-world]] — world coverage map with status and priority.
- [[research/adr]] — architecture decisions.
- [[topics/aeo]] — Answer-First contract for AI search ranking.

## Research tracks (raw)

- `docs/research/competitors/` — direct and adjacent competitors.
- `docs/research/marketplaces/` — RU / CN / global sales channels.
- `docs/research/platforms/` — storefront platform comparison.
- `docs/research/demand/` — demand, keyword and niche research.
