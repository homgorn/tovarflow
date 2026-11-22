# ADR 0004 — Atomised knowledge with provenance

**Status:** accepted · **Date:** 2026-11-22

## Context

Research reports are long, partly stale and hard to query. An LLM loads a 30-page report, misses the
one number that matters, and cannot tell whether a price was measured or guessed. Re-reading the
same report after a source changes is expensive.

## Decision

Store knowledge as atoms: `concept`, `source`, `finding`, `question`. One file = one claim. Every
atom has `id`, `layer`, `status`, `confidence`, `summary`, `tags`, `sources`, `reviewed`.
A `question` additionally has `resolves_when`.

Build three indexes: FTS5 over chunks, a graph of entities/edges, and a generated wiki with
backlinks. Long reports remain, but they are derivative: the atoms are the retrieval surface.

## Consequences

Positive:

- A claim can be cited, contradicted and superseded without rewriting a report.
- A refuted finding stays visible, so the team does not re-learn the same mistake.
- The graph answers relationship questions that text search cannot.

Negative:

- More files and a stricter writing discipline.
- Atomisation takes time; a lazy report is faster but less useful.
- The index builder must be run after edits.

## Alternatives rejected

- One big wiki page per topic: unmaintainable and impossible to cite precisely.
- Vector-only retrieval: good for "similar", bad for "exact price on this date".
- A database-only knowledge base: unreadable in a diff and hostile to human review.
