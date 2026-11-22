# ADR 0001 — Layered channel adapters (RU / CN / global / CIS)

**Status:** accepted · **Date:** 2026-11-22

## Context

RU, Chinese and global marketplaces differ in entity requirements, auth, language, currency, tax,
fulfilment and legal rules. A single `Marketplace` abstraction with nullable columns becomes
unmaintainable: half the fields are always empty and the core accumulates
`if platform == "ozon"` branches.

## Decision

Split channels into layers: `ru`, `cn`, `global`, `cis`. Each layer is a folder of capability
profiles plus thin adapters. A shared `kernel` owns retries, rate limits, idempotency, raw capture
and error mapping. The core resolves a profile and calls the adapter port; it never branches on a
country or a platform name.

## Consequences

Positive:

- A new channel is a profile + adapter, not a core change.
- Region-specific legal/entity rules are explicit.
- Tests can run per layer.

Negative:

- Some duplication between similar channels in the same layer.
- A cross-layer channel (Ozon Global) needs a clear owner and a profile that references the RU
  family.
- More files; the registry must be generated and validated.

## Alternatives rejected

- One universal marketplace model: hides real differences and produces nullable soup.
- One adapter per platform with shared code copied: diverges and multiplies bugs.
