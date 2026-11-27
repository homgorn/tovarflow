---
id: "limits-and-quotas"
title: "Limits and quotas"
tags:
  - qparser
  - limits
  - api
sources:
  - https://q-parser.ru/howto/api
confidence: "measured"
updated: "2026-11-27"
---

# Limits and quotas

Источник: https://q-parser.ru/howto/api. Измерено 22.11.2026.

These are hard constraints the ingestion pipeline must respect. Values are measured from the API page.

| Constraint | Value | Consequence |
|---|---|---|
| Concurrent unfinished parsings | 100 | `POST /parser` returns `unprocessable` above it |
| Concurrent unfinished exports | 100 | `POST /export` returns `unprocessable` above it |
| Page size (`/catalog`, `/parser/list`, `/goods`) | max 1000 | paginate, do not assume one page |
| Trial parsing | 50 goods | cannot be used for a full catalogue |
| Parallel downloads per plan | 1 / 3 / 10 / 20 | planner must cap jobs per tenant |
| Webhook addresses per automation | 5 | shard by event type if more are needed |
| Webhook response timeout | 10 s | acknowledge fast, process asynchronously |
| Webhook retries | 1, 5, 10, 30, 60 s | deduplicate with `X-QParser-Delivery` |

## Missing webhook for parser completion

The API documents webhooks only for `automata.finished`. A one-off `POST /parser` has no callback.
Therefore the ingestion service must poll `GET /parser/:id` with exponential backoff and persist
`status`, `goods_processed`, `categories_processed` and `error` on every poll.

## Archive behaviour

Archived parsings have no goods (`GET /parser/:id/goods` returns `unprocessable`).
Archive state must be recorded at ingest time, otherwise a re-export silently loses the catalogue.
