# Content rights gate

> This is an operating policy, not legal advice. A lawyer must review the first supplier contract
> and the first marketplace listing.

## Why

The catalogue is assembled from parsed supplier pages. Product descriptions and images may be
protected by copyright, and marketplace terms require the seller to have the right to use the
content. A takedown or an account suspension is a business-ending event for a small storefront.

## Rule

No product or image is published without a `content_right` record.

```text
content_right(
  id, tenant_id, product_id, image_id, basis, holder, evidence_url,
  valid_from, valid_to, reviewed_by, reviewed_at, notes
)
```

Allowed `basis` values:

| Basis | Meaning | Evidence |
|---|---|---|
| `supplier_contract` | The supplier permits resale and content use | Contract clause / signed permission |
| `own_content` | We created the photo, text or translation | Internal record |
| `licensed_feed` | The feed licence permits redistribution | Licence terms |
| `affiliate_terms` | The programme allows promotion but not resale | Programme terms |
| `public_domain` | The asset is public domain | Source |
| `unknown` | No basis established | Cannot publish |

## Publishing gate

1. `basis = unknown` → the product can be stored and priced but not published.
2. `basis = affiliate_terms` → the product can be linked/promoted, not republished as our own.
3. An image without a record blocks the whole listing, not only the image.
4. A translation is a new content item; it needs its own record if the source is third-party.

## Watermarks

- Removing a watermark is allowed only when the right holder permits it and the permission is
  recorded.
- A watermark on a supplier image is a signal that the image may be licensed; do not strip it by
  default.

## Takedown procedure

1. A contact address is published on the storefront.
2. A complaint is logged with the product, the claimant and the evidence.
3. The listing is unpublished within 24 hours while the claim is reviewed.
4. The outcome is recorded; a repeated claim blocks the supplier.
5. The marketplace account is notified if the content was published there.

## Supplier onboarding

Before the first parse of a supplier:

- identify the legal entity and the contact;
- obtain a contract or a written permission that covers resale and content;
- record the permitted channels and territories;
- record prohibited categories;
- record the permitted image use and whether watermark removal is allowed.

If the supplier cannot provide a basis, the catalogue can be used for research, not for sale.
