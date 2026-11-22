# Constitution

> Version 1.0 · 2026-11-22 · Supersedes nothing. Amended only by an explicit ADR and the owner's
> approval.

This document is the highest authority in the repository. A spec, ticket or implementation that
contradicts it is wrong by definition, even if it works.

## Article 1 — Evidence before assertion

Every durable claim has a source URL and an observation date. A fact is labelled `measured`,
`reported`, `inferred` or `unverified`. A number without a source is not a fact; it is a draft.
If a source cannot be reached, the claim keeps its last observation and is marked stale, not
deleted.

## Article 2 — Spec before code

No implementation starts without an approved spec in `specs/`. A spec has user scenarios,
functional requirements, acceptance criteria, non-functional requirements, data model and
out-of-scope. Code that exists without a spec is a prototype, not a product.

## Article 3 — External systems behind an anti-corruption layer

Q-Parser, Ozon, WB, Amazon and every other external system are accessed through an adapter. Their
vocabulary never leaks into the domain. The adapter owns HTTP, auth, retries, pagination, error
mapping and raw capture. The core owns the domain.

## Article 4 — All writes follow Proposal → Policy → Execution → Verification

An LLM or a UI never calls a write API directly. It emits a typed proposal. A deterministic policy
returns `ALLOW / DENY / REQUIRE_APPROVAL / ESCALATE`. Execution is idempotent. Verification
re-reads the external state. The result is an append-only event.

## Article 5 — Idempotency everywhere

Every write has an `idempotency_key`. A repeat with the same key returns the first result and does
not send a second request. This applies to price, stock, card publish, order acknowledgement and
refunds. A retry without a key is a bug.

## Article 6 — Raw payload is preserved

Before mapping, the raw request and response are stored in object storage with a hash and a
reference. The normalised DTO carries `raw_blob_ref`. If a mapping bug is found six months later,
the evidence still exists.

## Article 7 — Tenant isolation from day one

Every domain table carries `tenant_id`. RLS is enabled. Object paths and search indexes are
tenant-scoped. The first deployment has one tenant; the schema does not know that.

## Article 8 — Money is exact

Money is integer minor units plus an ISO-4217 currency. No floats. Unknown cost components are
`NULL`, never `0`. A total with unknowns is marked `is_complete = false` and cannot be published
as final. Currency conversion stores the rate and the rate date.

## Article 9 — Rights before reach

No product image, description or brand asset is republished without a recorded right to do so.
A supplier agreement, an affiliate licence or an explicit permission is a record, not a
conversation. A takedown procedure exists before the first storefront goes live.

## Article 10 — No browser automation in autonomous paths

Autonomous flows use official APIs. Browser automation is allowed only as a manual, supervised
tool, with an ADR, and never in a nightly or unattended job. It is brittle, hard to audit and
legally risky.

## Article 11 — License discipline

MIT, Apache-2.0 and BSD code may be used. GPL, AGPL and unlicensed code require an ADR and a legal
review before any dependency is added. Official marketplace specifications stay outside the
repository unless their terms allow redistribution.

## Article 12 — Nothing is deleted without double confirmation

No agent, script or human deletes a file, drops a table, or overwrites a source artefact without
explicit double confirmation from the owner. Refuted knowledge stays, marked `refuted`. A
superseded spec gets a new version; the old one stays. Deleting data to "clean up" is prohibited.

## Article 13 — Observability and reconciliation

Every write emits an event with a trace id. A daily reconciliation compares parsed, published,
rejected, sold and settled counts. An unexplained delta is an incident, not a rounding error. A
price change is not done until it is verified by a read.

## Article 14 — Reproducibility

A corpus fetch, a build and a test run are reproducible from a clean checkout. Randomness is
seeded. Time is injected. A result that cannot be replayed is not evidence. The research corpus
keeps raw HTML, cleaned Markdown, hashes and a manifest.

## Article 15 — Language and content quality

Machine translation is a draft, never a publication. Product content has a glossary, a review
state and a per-locale hash. A translated card that nobody reviewed is marked as unreviewed and
cannot be published to a marketplace that requires local-language content.

## Article 16 — Secrets never touch the repository

Credentials live in a secret manager and are referenced by `secret_ref`. Logs redact headers and
tokens. A leaked key is rotated, not deleted from history and forgotten.

## Article 17 — One-way doors need a human

Deleting a catalogue, merging two suppliers' products, changing a price floor, publishing to a new
channel, or dropping a table are one-way doors. They require explicit human approval and a
recorded decision. Reversible experiments do not.

## Amendment process

1. Write an ADR in `docs/adr/` with the proposed change and the reason.
2. State which article is amended and what breaks.
3. Get the owner's explicit approval.
4. Bump the constitution version and record the date.

## Enforcement

- `tools/verify_coverage.py` and `tools/build_knowledge.py` are gates for the corpus.
- Contract tests and a verifier agent are gates for connectors.
- The crawler-view test is a gate for the storefront.
- A PR that violates an article is rejected even if all tests pass.
