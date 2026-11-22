# Spec 005 — Operations, observability and reconciliation

**Status:** draft for approval · **Date:** 2026-11-22 · **Depends on:** specs 001–004.

## 1. Why

A catalogue platform fails quietly: a token expires, a price is not applied, a card is rejected, a
supplier removes a product, and the storefront keeps selling. Operations is not a dashboard; it is
the set of checks that make silence impossible.

## 2. User scenarios

### US1 — Know that a sync failed (P0)
As an operator, I want an alert within 5 minutes when a channel stops syncing.

Acceptance:
1. A sync job has a heartbeat and a last-success timestamp.
2. A missed heartbeat raises a `sync_stale` alert with the channel and account.
3. Auth expiry raises `auth_expired` and pauses the account.
4. A price mismatch raises `price_mismatch` with old, new and observed values.
5. Alerts include a runbook link.

### US2 — Reconcile the day (P0)
As an operator, I want a daily report: parsed, published, rejected, sold, settled.

Acceptance:
1. Counts are computed from events, not from UI state.
2. Every delta has a reason code.
3. An unexplained delta > 0.5% raises an incident.
4. The report is reproducible for a given date.

### US3 — Recover from a bad write (P0)
As an operator, I want to roll back a price batch.

Acceptance:
1. A batch has a before/after snapshot.
2. Rollback is a new proposal, not a database edit.
3. Rollback is verified by re-read.
4. A rollback cannot go below the floor without approval.

### US4 — Restore the system (P1)
As an operator, I want a tested restore procedure.

Acceptance:
1. Postgres PITR is enabled; a restore drill is run monthly.
2. Object storage has versioning; a deleted blob is recoverable.
3. Secrets are restorable from the secret manager, not from a laptop.
4. RTO <= 4 h, RPO <= 15 min for the runtime database.

### US5 — Control cost (P1)
As an owner, I want cost per 1k SKU and per channel.

Acceptance:
1. AI points, scraping, storage and egress are metered per tenant.
2. A budget threshold raises an alert before the invoice.
3. A runaway job is stopped by a hard limit, not by a surprise bill.

## 3. Functional requirements

- **FR-001** OpenTelemetry traces for API, queue and DB; a trace id propagates to channel requests.
- **FR-002** Structured logs with tenant, job, channel, proposal and idempotency key; secrets redacted.
- **FR-003** Metrics: ingestion lag, parse failures, goods/sec, listing states, price writes,
  verification results, order lag, reconciliation deltas, queue depth.
- **FR-004** Alerts: `sync_stale`, `auth_expired`, `rate_limited`, `price_mismatch`,
  `moderation_rejected`, `reconciliation_delta`, `queue_backlog`, `storage_quota`.
- **FR-005** An append-only event log is the source of truth for audits and reports.
- **FR-006** A daily reconciliation job with reason codes.
- **FR-007** Backups: Postgres PITR, S3 versioning, monthly restore drill.
- **FR-008** Secrets in a manager, referenced by `secret_ref`; rotation runbook.
- **FR-009** Per-tenant usage metering and hard budgets.
- **FR-010** Runbooks for: auth expiry, rate limit storm, price mismatch, moderation flood,
  duplicate listings, storage full, queue backlog.

## 4. Non-functional requirements

- **NFR-001** Alert delivery < 5 min from detection.
- **NFR-002** Dashboard load < 2 s for 30-day ranges.
- **NFR-003** Event log retention: 13 months hot, 3 years cold.
- **NFR-004** Reconciliation completes in < 15 min for 1M SKU.
- **NFR-005** A single channel outage does not stop other channels.

## 5. Data model

```text
event(id, tenant_id, type, aggregate, aggregate_id, payload JSONB, actor, trace_id, created_at)
job_run(id, tenant_id, kind, channel, status, heartbeat_at, started_at, finished_at, error)
alert(id, tenant_id, kind, severity, subject, details JSONB, acknowledged_at, resolved_at)
reconciliation_run(id, tenant_id, day, status, counts JSONB, deltas JSONB, report_url)
usage_meter(id, tenant_id, day, metric, value, unit, cost_minor)
```

## 6. Acceptance scenarios

```gherkin
Scenario: a stale channel is detected
  Given a channel with a 15-minute sync interval
  When no successful sync happens for 30 minutes
  Then sync_stale is raised within 5 minutes
  And the runbook is linked

Scenario: reconciliation explains every delta
  Given 1000 parsed, 950 published, 30 rejected, 20 pending
  When reconciliation runs
  Then 1000 = 950 + 30 + 20
  And each rejected card has a reason code

Scenario: rollback a price batch
  Given a batch that changed 200 prices
  When I roll back the batch
  Then 200 new proposals are created
  And each is verified by re-read
  And the original batch remains in the audit log
```

## 7. Out of scope

- A full BI suite. Start with the operator console and SQL reports.
- On-call rotation before the first live channel.
- Multi-region active-active.

## 8. Open questions

- Which alert channel: Telegram, email, or both?
- What is the acceptable price-mismatch rate for a channel before auto-pause?
- Which metrics are billable to a tenant in the SaaS phase?
