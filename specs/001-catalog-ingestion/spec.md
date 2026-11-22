# Spec 001 — Catalog ingestion from Q-Parser

**Status:** draft for approval · **Date:** 2026-11-22 · **Depends on:** constitution, architecture
overview, domain model.

## 1. Why

Q-Parser is the first supply source. It can parse a supplier site, return categories and goods,
and export to a file. What it does not provide is a durable, idempotent, replayable ingestion
contract for our catalogue. This spec defines that contract.

The ingestion service must survive: expired keys, 429s, `unprocessable` due to the 100-job
concurrency limit, partial parses, archived parses, and the absence of a parse-completion webhook.

## 2. User scenarios

### US1 — Discover the catalogue (P0)
As an operator, I want to search Q-Parser's site catalogue and inspect a site's parser options, so
that I know whether a supplier can be ingested and what credentials/options it needs.

Acceptance:
1. Given a query, `GET /catalog` returns a page of sites with `domain`, `title`, `slug`,
   `private`, `free_until`, `categories`, `cities`.
2. Given a domain, `GET /website/:domain` returns `auth_required`, `manual_categories` and
   `options`.
3. Pagination stops when `offset + limit >= total`.

### US2 — Collect categories (P0)
As an operator, I want to collect the category tree of a site so that I can choose what to parse.

Acceptance:
1. `POST /categories` returns `{id, status}`; if cached, `status = completed` immediately.
2. `GET /categories/:id` is polled until `completed` or `error`; `categories` is `null` while
   running.
3. A category URL must belong to the same domain; invalid entries are dropped before the call.

### US3 — Start a parse (P0)
As an operator, I want to start a full or trial parse, so that goods become available.

Acceptance:
1. A paid site with an active plan starts a full parse; a free site starts without a plan.
2. A trial parse sends `trial: true` and is limited to 50 goods.
3. If `categories` is empty, Q-Parser loads the category list automatically.
4. A concurrency-limit response (`unprocessable`) is retried with backoff and never loses the job.

### US4 — Track a parse (P0)
As an operator, I want the parse status and progress, so that I can detect stalls and failures.

Acceptance:
1. `GET /parser/:id` returns `status`, `goods_processed`, `goods_limited`,
   `categories_total`, `categories_processed`, `created`, `finished`, `archive`, `error`.
2. Polling uses exponential backoff: 2 s, 5 s, 15 s, 30 s, 60 s, capped at 60 s.
3. A parse in `queued` or `running` for longer than the expected window raises a `stalled` alert.
4. `canceled` and `error` are terminal for the ingestion run until an explicit resume.

### US5 — Fetch goods (P0)
As an operator, I want every good, paginated, so that the catalogue is complete.

Acceptance:
1. `GET /parser/:id/goods?limit=1000&offset=N` is paged until `offset + limit >= total`.
2. The fields `title, article, url, price, old_price, currency, brand, quantity, publish, images,
   file_links, video_links, category_title, category_url, description, short_description, data`
   are persisted.
3. An archived parse returns `unprocessable`; the run is marked `archived` and no goods are requested.
4. A page shorter than `limit` does not terminate the loop unless `total` has been reached.

### US6 — Export (P1)
As an operator, I want a file export, so that I can bootstrap a marketplace feed before the native
connector is ready.

Acceptance:
1. `GET /format` returns formats and their option schema.
2. `POST /export` accepts `parser_id`, `format`, `options`, optional `offset`/`limit`.
3. `GET /export/:id` is polled until `completed`; `files` and `links` are stored.
4. A failed export is retried only for transient errors; a validation error is not retried.

### US7 — Scheduled refresh (P1)
As an operator, I want a scheduled parse with a signed webhook, so that the catalogue stays fresh.

Acceptance:
1. An automation with a webhook receives `POST` with `event = automata.finished`.
2. The signature `X-QParser-Signature: sha256=<HMAC>` over `<timestamp>.<body>` is verified with
   the per-webhook secret.
3. `X-QParser-Delivery` is stored and used to deduplicate retries.
4. The handler acknowledges within 10 s and processes asynchronously.

## 3. Functional requirements

- **FR-001** Base URL is `https://q-parser.ru/api/v1`; auth is `Authorization: Bearer` or
  `X-Api-Key`; the key is never logged.
- **FR-002** All errors are mapped to the domain taxonomy: `AuthError`, `ValidationError`,
  `EntitlementError`, `RateLimitError` (`unprocessable`/429), `TransientError`, `UnknownError`.
- **FR-003** Every request has a timeout; GET retries 3 times with jitter; POST retries only when
  the operation is idempotent or the server confirms no side effect.
- **FR-004** Pagination is cursor-by-offset and stops on `total`, not on an empty page.
- **FR-005** A parse run is persisted before the first poll; its raw status snapshots are appended.
- **FR-006** Goods are written in a transaction per page; a failed page does not lose previous pages.
- **FR-007** `archive = true` is recorded and blocks `goods` calls.
- **FR-008** The service enforces a per-tenant concurrency budget below the global 100 limit.
- **FR-009** The 1000-record page size is respected; no assumption of a single page.
- **FR-010** The trial limit (50 goods) is detected and surfaced, not treated as a full catalogue.
- **FR-011** A schema-drift check compares the live API heading set with the stored endpoint set.
- **FR-012** Every raw request/response is stored with a hash and a `raw_blob_ref`.
- **FR-013** A parse id replay produces the same canonical output hash.
- **FR-014** Q-Parser `data` keys are stored raw and never silently dropped.
- **FR-015** Automata webhooks are verified and deduplicated by `X-QParser-Delivery`.

## 4. Non-functional requirements

- **NFR-001** Ingest 100k goods in under 30 minutes with 10 concurrent page workers, respecting
  the API's limits.
- **NFR-002** No secret in logs, traces or error messages.
- **NFR-003** Every job has a trace id; every state transition is an event.
- **NFR-004** Retries are bounded; a permanently failing run does not spin forever.
- **NFR-005** The ingestion worker can resume after a crash from the last committed page.
- **NFR-006** Storage is tenant-scoped and encrypted at rest.

## 5. Data model

```text
supplier(id, tenant_id, name, country, status)
source(id, tenant_id, supplier_id, kind, domain, auth_required, manual_categories, options_json)
parse_run(id, tenant_id, source_id, external_id, status, goods_processed, goods_limited,
          categories_total, categories_processed, archive, error, created_at, finished_at)
source_product(id, tenant_id, parse_run_id, external_id, title, article, url, price_minor,
               old_price_minor, currency, brand, quantity, publish, category_title,
               category_url, description, short_description, attributes_raw JSONB, raw_blob_ref)
raw_blob(id, tenant_id, sha256, bytes, content_type, s3_key, created_at)
```

Invariants:

- `parse_run.external_id` is unique per tenant.
- `source_product` is unique per `(parse_run_id, external_id)` when an external id exists;
  otherwise `(parse_run_id, url)`.
- Money is minor units + currency; `price` missing is `NULL`, not `0`.
- `publish` is tri-state.

## 6. Contracts

The machine-readable contract is `docs/research/qparser/extracted/endpoints.json` (16 endpoints).
The first slice implements 9 of them:

`GET /catalog`, `GET /website/:domain`, `POST /categories`, `GET /categories/:id`,
`POST /parser`, `GET /parser/:id`, `GET /parser/:id/goods`, `GET /format`, `POST /export`,
`GET /export/:id`.

## 7. Acceptance scenarios

```gherkin
Scenario: a trial parse on a paid site is capped
  Given a paid site without an active plan
  When I start a parse with trial=true
  Then the parse completes with at most 50 goods
  And the run is marked trial_limited

Scenario: concurrency limit does not lose the job
  Given 100 unfinished parses
  When I start another parse
  Then the API returns unprocessable
  And the job is retried with backoff
  And it starts when a slot is free

Scenario: archived parse is not silently empty
  Given a parse with archive=true
  When I request goods
  Then the API returns unprocessable
  And the run is marked archived
  And no empty catalogue is published

Scenario: webhook replay is deduplicated
  Given a webhook delivery id
  When the same delivery arrives twice
  Then the second is acknowledged and ignored
```

## 8. Out of scope

- Browser automation of the Q-Parser UI.
- Bypassing the trial limit or the plan.
- Parsing sites that Q-Parser does not support.
- Content rights verification (handled before publish, not at ingest).

## 9. Open questions

- What is the actual rate limit per key, beyond the 100-job limit? (not documented)
- Does `POST /parser` return an existing id for an identical running request, or a new one?
- How long are raw files retained in Q-Parser's storage?
- Is `goods` stable while a parse is running, or only after `completed`?

## 10. Test plan

- Contract tests with recorded fixtures for all 16 endpoints.
- A live smoke test against a free site, guarded by an environment flag.
- Replay test: same parse id → same canonical hash.
- Fault injection: 401, 429, 500, timeout, `unprocessable`, archived goods.
- Pagination property test: 0, 1, 999, 1000, 1001, 10k goods.
- Webhook signature test with a known secret and a tampered body.
