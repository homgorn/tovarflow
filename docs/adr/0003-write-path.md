# ADR 0003 — Writes go through Proposal → Policy → Execution → Verification

**Status:** accepted · **Date:** 2026-11-22

## Context

Price, stock and card writes are financial and reputational actions. An LLM or an operator can make
a mistake; a retry can double-apply a discount; a channel can accept a request and not apply it.
Direct API calls from the core make these failures invisible.

## Decision

Every external mutation follows four steps:

1. **Proposal** — a typed intent with before/after values and a reason.
2. **PolicyDecision** — a deterministic, versioned rule set returns
   `ALLOW / DENY / REQUIRE_APPROVAL / ESCALATE`.
3. **Execution** — an idempotent call with `idempotency_key`, `proposal_id` and `trace_id`.
4. **Verification** — a re-read of the external state returns `OK / MISMATCH / UNKNOWN / SKIPPED`.

The result is an append-only event. A write is not "done" until verification is `OK`. A mismatch
opens an incident and does not auto-retry.

## Consequences

Positive:

- Idempotency is structural, not a convention.
- Every price has an explanation and an audit trail.
- A bad batch can be rolled back as a new proposal.
- The LLM can propose without being trusted with a write key.

Negative:

- More latency and more tables.
- Policy rules must be maintained and versioned.
- Some low-risk writes feel over-engineered; they still go through the path.

## Alternatives rejected

- Direct writes with a retry wrapper: retries can double-apply.
- LLM with a write key: unbounded blast radius and no audit.
- Verification only in tests: production drift goes unnoticed.
