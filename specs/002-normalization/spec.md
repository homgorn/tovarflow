# Spec 002 — Normalisation, identity, pricing and media

**Status:** draft for approval · **Date:** 2026-11-22 · **Depends on:** spec 001, domain model.

## 1. Why

Q-Parser returns `goods` with a free-form `data` map. Marketplaces require typed attributes,
category-specific enums and media rules. Between the two there is a normalisation layer. Without
it, every channel connector re-implements attribute mapping and every price is a guess.

This spec defines: the canonical product model, attribute mapping, identity candidates, the margin
ledger, the media pipeline and translation.

## 2. User scenarios

### US1 — A raw good becomes a canonical product (P0)
As an operator, I want a parsed good to become a product with variants and offers, so that it can
be priced and published.

Acceptance:
1. `title`, `brand`, `description`, `category`, `images` are mapped.
2. `price`, `old_price`, `currency` become `Offer` fields in minor units.
3. `data` keys become canonical attributes where a mapping exists; unmapped keys are preserved in
   `attributes_raw` and reported.
4. `publish = null` stays unknown; it is not converted to `true` or `false`.

### US2 — Deduplicate across suppliers (P1)
As an operator, I want candidate matches, so that the same product from two suppliers is not shown
twice.

Acceptance:
1. Exact GTIN matches are candidates with `confidence = 0.99`.
2. Brand + article matches are candidates with a recorded normalisation.
3. Image hash + title similarity produces a candidate, never a merge.
4. A candidate is confirmed or rejected by a human; `reviewed_at` and `review_outcome` are stored.
5. Two products are never merged automatically.

### US3 — Explain a price (P0)
As an operator, I want to see why a product costs what it costs, so that I can trust the margin.

Acceptance:
1. The price is computed from purchase, inbound delivery, duty, certification, packaging,
   fulfilment, return loss, acquiring, tax, commission and target margin.
2. Each component has a source and a version.
3. An unknown component makes the result `incomplete`; an incomplete price cannot be auto-published.
4. A floor price is enforced by policy; a price below the floor is denied.
5. Currency conversion stores the rate and the rate date.

### US4 — Media is safe and fast (P0)
As a customer, I want product images that load quickly and are not broken.

Acceptance:
1. Images are downloaded, hashed and stored in S3; duplicates are not re-uploaded.
2. WebP/AVIF variants are generated; the original is preserved.
3. EXIF is stripped; a watermark is not added unless the rights allow it.
4. A missing image is reported, not replaced by a placeholder silently.
5. URLs are stable and content-addressed.

### US5 — Translate without publishing garbage (P1)
As an operator, I want RU ↔ CN/EN product content with review, so that a translated card is not
published unreviewed.

Acceptance:
1. The original is preserved with a locale tag.
2. Machine translation is a draft with `review_state = pending`.
3. A glossary enforces brand and category terms.
4. A reviewed translation has a reviewer id and a timestamp.
5. A marketplace that requires local-language content rejects an unreviewed translation.

## 3. Functional requirements

- **FR-001** Canonical entities: `product`, `variant`, `offer`, `media`, `attribute`,
  `category`, `product_identity_match`.
- **FR-002** Attribute dictionary is versioned; a mapping change creates a new version.
- **FR-003** Money is integer minor units + ISO-4217; no floats; no implicit currency.
- **FR-004** Unknown values are `NULL`; `0` is a real value and must not be used as "unknown".
- **FR-005** Identity candidates store individual signals (GTIN, brand+article, image hash,
  title similarity) and a similarity score; they are never auto-merged.
- **FR-006** The margin ledger is versioned per tenant, category and channel.
- **FR-007** A price result has `is_complete`, `floor_price`, `explanation[]` and `version`.
- **FR-008** Media is content-addressed; the original, WebP and AVIF variants are stored.
- **FR-009** Translation is per locale with `review_state` and a glossary.
- **FR-010** Category mapping is external-taxonomy-versioned; a taxonomy diff is detectable.
- **FR-011** If a supplier product has no brand, the feed uses the supplier name from the site
  catalogue as `vendor` and records `fallback_vendors` in the feed report. This is a visible data
  quality signal, not a silent correction. A human can override it per category later.

## 4. Non-functional requirements

- **NFR-001** Normalise 10k goods in under 5 minutes without AI calls.
- **NFR-002** Attribute mapping is deterministic; the same input yields the same output.
- **NFR-003** Media pipeline is resumable and idempotent.
- **NFR-004** A price explanation is reproducible from stored inputs.
- **NFR-005** All AI enrichment is optional, versioned and recorded as a proposal, not a fact.

## 5. Data model

```text
product(id, tenant_id, canonical_sku, title, brand, description, category_id,
        attributes JSONB, attributes_raw JSONB, status, created_at, updated_at)
variant(id, tenant_id, product_id, sku, barcode, attributes JSONB, status)
offer(id, tenant_id, variant_id, supplier_id, purchase_price_minor, currency,
      moq, stock_qty, lead_time_days, condition, warehouse_ref, is_active)
media(id, tenant_id, product_id, role, sha256, width, height, mime, s3_key, alt, position)
attribute_definition(id, tenant_id, key, type, unit, enum_values, version)
attribute_mapping(id, tenant_id, source_key, attribute_id, transform, version)
category(id, tenant_id, parent_id, name, path, taxonomy_version)
channel_category(id, channel, external_id, name, path, version)
category_mapping(id, tenant_id, category_id, channel_category_id, confidence, reviewed_at)
product_identity_match(id, tenant_id, product_a, product_b, confidence, method,
                       signals JSONB, reviewed_at, review_outcome)
price_observation(...)  -- see domain model
margin_rule(id, tenant_id, category_id, channel, version, components JSONB, floor_pct)
translation(id, tenant_id, entity, entity_id, locale, field, text, review_state,
            reviewer_id, reviewed_at, glossary_version)
```

## 6. Acceptance scenarios

```gherkin
Scenario: unknown stock is not zero
  Given a good with publish=null
  When it is normalised
  Then the offer stock is unknown
  And the product is not marked in stock

Scenario: incomplete price is blocked
  Given a product with unknown duty
  When the pricing engine computes a price
  Then is_complete is false
  And the price cannot be auto-published
  And the missing component is named

Scenario: two suppliers, same product
  Given two goods with the same GTIN
  When identity matching runs
  Then a candidate is created with confidence 0.99
  And no product is merged
  And a human can confirm or reject

Scenario: unreviewed translation is not published
  Given a CN product with a machine translation
  When a marketplace requires RU content
  Then the listing is blocked
  And the review queue is shown
```

## 7. Out of scope

- Automatic cross-supplier merging.
- A full PIM with workflow approvals for every field.
- AI-generated product photos before a rights policy exists.
- Tax advice; tax rules are data with a version and a source.

## 8. Open questions

- Which attribute dictionary should be canonical: our own, Google Product Taxonomy, or a
  marketplace taxonomy? (Recommendation: our own keys, mapped outward.)
- How many Q-Parser `data` keys are actually used across the catalogue?
- Do supplier images carry watermarks that must be removed? (Rights question, not only technical.)
- Which categories require certification documents before listing?

## 9. Test plan

- Golden files: 20 real goods → expected canonical JSON.
- Property test: unknown never becomes zero.
- Price explanation reconstruction test.
- Identity candidate test with GTIN, brand+article, image hash, and conflicting signals.
- Media: broken URL, duplicate hash, huge image, EXIF, CMYK.
- Translation: glossary enforcement, unreviewed publish block.
