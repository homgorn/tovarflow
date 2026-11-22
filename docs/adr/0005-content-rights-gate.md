# ADR 0005 — Content rights gate before publishing

**Status:** accepted · **Date:** 2026-11-22

## Context

The catalogue is assembled from parsed supplier pages. Product descriptions and images may be
protected by copyright, and marketplace terms require the seller to have the right to use the
content. A takedown or an account suspension is a business-ending event for a small storefront.

## Decision

No product is published without a `content_right` record. The record states the basis:

- supplier contract or explicit permission;
- own content (photo, text, translation);
- licensed feed with redistribution rights;
- affiliate programme terms that allow the use.

If the basis is unknown, the product can be stored and priced but not published. A takedown
procedure and a contact are documented before the first storefront goes live. Watermark removal is
allowed only when the right holder permits it.

## Consequences

Positive:

- A clear answer when a rights holder complains.
- Marketplace account risk is reduced.
- Content ownership becomes a product feature (own photo pipeline, own descriptions).

Negative:

- Some supplier catalogues cannot be published as-is.
- The rights record adds a step to onboarding.
- Legal review is needed for the first supplier contract.

## Alternatives rejected

- "Everyone parses, so it is fine": not a legal basis and not an audit trail.
- Removing watermarks by default: increases infringement risk.
