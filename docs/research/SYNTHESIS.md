# Research synthesis — what the market says, and what we almost missed

> Generated 2026-11-22 from six research tracks. Every number below has a source in the track's
> `data.json`; this document is the decision layer, not the evidence layer.

## 1. The short answer

Q-Parser is a strong **supply ingestion** product with a real moat: 7,000+ pre-configured supplier
sites, AI enrichment included, unlimited SKUs at 995–2,495 RUB/mo, and ~71 export formats. It is not
a sales channel. The gap between "parsed" and "sold" is the product:

1. a canonical catalogue with attributes and media,
2. a margin ledger that knows real channel costs,
3. native marketplace APIs for listings, price, stock and orders,
4. a storefront that is readable by search engines and AI answer engines,
5. a demand layer that chooses what to sell before we build a storefront.

No RU competitor bundles all five. The closest are feed managers (DataFeedWatch, Channable) and
multichannel listing tools (Sellbrite, LitCommerce), which solve channels but not supply ingestion.
That intersection is the opening.

## 2. Competitive position

### What Q-Parser already wins

- Supplier coverage: 7,000+ sites, categories and cities.
- Price: 995–2,495 RUB/mo with unlimited SKUs, versus MarketParser at 9,500–49,000 RUB/mo for
  repricing-heavy plans.
- AI Points included; AI editing, image generation, watermark removal.
- ~71 export formats, including direct CMS and social formats.
- Automation and signed webhooks.

### The ten gaps that matter

| # | Gap | Why it matters | Our answer |
|---|---|---|---|
| 1 | No native marketplace API sync | YML/CSV is a file, not a listing lifecycle | RU/CN/global adapters with L2–L4 maturity |
| 2 | No headless API for storefronts | Cannot feed Medusa/Saleor/Vendure cleanly | Catalog Hub API + webhooks |
| 3 | No repricing / competition monitoring | Price is the main lever on marketplaces | Margin ledger + price observations + policy |
| 4 | No canonical attribute model | `data` keys are free-form; marketplaces need enums | Attribute dictionary + category mapping |
| 5 | No settlement reconciliation | Orders ≠ money; commissions and returns eat margin | Settlement ledger and daily reconciliation |
| 6 | RUB-only, RU-only docs | Blocks China and global | Layer packs + localization |
| 7 | No rights/compliance workflow | Content and certification can suspend an account | Rights gate + certification checklist |
| 8 | No demand layer | We would build storefronts on a hunch | Niche Radar sidecar + marketplace demand |
| 9 | No tenant model | A future SaaS would require a rewrite | `tenant_id` + RLS from day one |
| 10 | No connector certification | "Works once" is not a connector | L0–L5 maturity + verifier |

### Direct RU competitors (measured where possible)

| Vendor | Price | What it does | Weakness |
|---|---|---|---|
| CloudParser | 950 RUB/mo | 100K SKUs, 300 auto-upload rules | Parser, not a channel platform |
| ALL RIVAL | Free tier 1,750 SKUs | Repricing, API, auto-matching | Price monitoring, not catalogue publishing |
| MarketParser | 9,500–49,000 RUB/mo | Repricing across cabinets | Expensive, narrow |
| ParserOK | 4,200 RUB once | Desktop parser, unlimited SKUs | No SaaS, no channel lifecycle |

Feed management: DataFeedWatch $64/$84/$239; GoDataFeed from $99; Productsup/Lengow/Feedonomics
custom/enterprise. Multichannel: LitCommerce $29 (1,000 listings, 3 channels), Sellbrite
$29/$79/$179, Shopify Marketplace Connect free for 50 orders then 1% capped at $99/mo.

## 3. Cross-track decisions

| Decision | Choice | Evidence |
|---|---|---|
| Storefront platform | Medusa v2 + Next.js | Score 81/100; MIT; $299 Cloud Pro; no GMV fee |
| Runner-up | Vendure | 77/100; native channels, but GPLv3 + €599/mo |
| First sales channels | Ozon, WB, Yandex Market | Official specs local; RU catalogue fit |
| First global channel | Google Merchant Center | No seller gate, service account, feeds Shopping/PMax |
| Next global | Bol.com, Walmart | Clean OAuth2/async contracts; dynamic sandbox |
| China | Supply-first: 1688, Taobao Union | APIs exist; procurement needs a CN receiving entity |
| China sales | Ozon Global / WB China | **Blocked** until a Chinese legal entity exists |
| Do not build | Temu direct, Xianyu, Pinduoduo, JD/Douyin for foreign sellers | No public API or hard legal blockers |
| Demand | Niche Radar as a sidecar | Schema + metrics + MCP cover ~80% |
| Write path | Proposal → Policy → Execution → Verification | Adopted from `wb china`; price safety |

## 4. Build order (four vertical slices)

### Slice 1 — Ingest one domain, prove the contract
Q-Parser client, categories, parse polling, goods pagination, raw capture, canonical product for
1,000 goods. Exit: replay produces the same hash; 0 lost pages; 0 unknown-to-zero conversions.

### Slice 2 — Price and storefront
Margin ledger, media pipeline, Medusa + Next.js storefront. Exit: a price is explainable line by
line; LCP < 2.5 s; primary content in raw HTML; YML validates.

### Slice 3 — RU sales loop
Ozon L2, WB L2, Yandex feed. Exit: 100 listings, one price write verified, one order imported, one
reconciliation with zero unexplained deltas.

### Slice 4 — Demand and global
Niche Radar sidecar, Google Merchant feed, then Bol/Walmart. Exit: a storefront starts from a demand
brief; a global feed publishes and a price is verified.

## 5. What we almost missed

These layers were not in the first brief. Each one can kill a launch if ignored.

| # | Layer | Why it is critical | First artefact |
|---|---|---|---|
| 1 | **Settlement and unit economics** | Orders are not money; commissions, returns, fines and logistics decide profit | `settlement` ledger + daily P&L |
| 2 | **Fulfilment and cross-border** | FBO/FBS/DBS/3PL, customs, consolidation, lead times | Fulfilment profile per channel |
| 3 | **Payments and currency control** | Acquiring, payouts, CNY/RUB, entity restrictions | Payment provider matrix |
| 4 | **Content rights** | A takedown can close the store | `content_right` gate (ADR-0005) |
| 5 | **Product compliance** | Certification, labelling (Честный знак), GPSR, prohibited categories | Category compliance checklist |
| 6 | **Tax and accounting** | VAT/USN, 54-ФЗ receipts, 1C/MoySklad | Tax profile per region |
| 7 | **Catalogue quality** | GTIN/EAN, attributes, taxonomy, dedupe | Attribute dictionary v1 |
| 8 | **Translation and localisation** | Machine translation without review is a liability | Glossary + review queue |
| 9 | **Search and merchandising** | Facets, synonyms, typo tolerance, ranking | Search index spec |
| 10 | **SEO / AEO** | If crawlers cannot read it, the storefront does not exist | Crawler-view test, `llms.txt` |
| 11 | **Supplier onboarding** | MOQ, lead time, stock truth, contract | Supplier scorecard |
| 12 | **Customer support and returns** | Marketplace penalties and ratings | Return reason taxonomy |
| 13 | **Repricing and competition** | Price is the main conversion lever | Price observation + floor policy |
| 14 | **Marketplace certification** | No write sandbox on Ozon/WB/Kaspi | Fixtures + live certification plan |
| 15 | **Security and tenancy** | A leak or cross-tenant read is fatal | RLS tests, secret manager |
| 16 | **Observability and reconciliation** | Silent failure is the default failure | Heartbeats + daily report |
| 17 | **Cost control** | AI points, scraping, storage and egress compound | Usage meter + budgets |
| 18 | **Affiliate/partner channel** | A second demand source without inventory risk | Admitad/Taobao Union evaluation |
| 19 | **Brand, domain, legal entity** | Marketplace accounts need an entity and documents | Entity checklist per layer |
| 20 | **Data licensing and privacy** | Parsing ToS and personal data law | Rights/privacy register |

## 6. Numbers to keep on the wall

- Q-Parser: 100 concurrent parses/exports; 1,000 records per page; 50-goods trial; no parse webhook.
- WB: 12–13 category-scoped JWT tokens; Stats 1 request/min; three consecutive 429s pause the
  account.
- Ozon: 482 paths in the official schema; no write sandbox; finance window ≤ 31 days.
- Yandex Market: granular API-key scopes; `pageToken`, limit ≤ 100.
- Global: Google Merchant is feed-based with service-account auth; Bol uses a 299-second JWT;
  Walmart uses 15-minute tokens and a dynamic sandbox; eBay Inventory limit is 2M/day; Etsy
  Commercial Access is gated.
- Medusa: $29/$99/$299 Cloud; self-host ~$600–800/mo at 100k SKU; no GMV fee.
- DataFeedWatch: $64/$84/$239; LitCommerce: $29 for 1,000 listings/3 channels.

## 7. Confidence

| Claim | Confidence |
|---|---|
| Q-Parser's moat is supplier coverage + price + AI | 8/10 |
| Native marketplace sync is the missing layer | 9/10 |
| Medusa v2 is the right MVP platform | 8/10 |
| RU first, CN supply-first, global Google-first | 8/10 |
| Ozon/WB have no write sandbox | 8/10 (reported/measured mix) |
| Temu has no public API; Xianyu is a trap | 8/10 |
| Settlement reconciliation is under-scoped | 7/10 (inferred from marketplace economics) |

## 8. What would change the plan

- A Chinese legal entity appears → Ozon Global / WB China move from `blocked` to `queued`.
- A marketplace sandbox appears for Ozon/WB → connector velocity doubles.
- Multi-tenant SaaS becomes month-1 → Vendure re-enters the platform decision.
- A supplier contract grants full content rights → the rights gate becomes a checklist, not a
  blocker.
- A paid demand account is available → niche scoring moves from `reported` to `measured`.
