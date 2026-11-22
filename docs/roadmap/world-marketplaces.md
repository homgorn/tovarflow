# World marketplaces — coverage plan

> "Весь мир" is a direction, not a first release. This file is the complete map so that no region
> is forgotten, and a status so that nothing looks done when it is only named.
>
> Statuses: `research` (docs being read) · `queued` (profile + spec written) · `building` ·
> `live` · `blocked` (entity/legal/API unavailable) · `not-planned`.
>
> Priority: P0 = first RU loop, P1 = next 12 months, P2 = later, P3 = watch.

## RU / EAEU / CIS

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Ozon Seller | RU | sales | P0 | research | Official OpenAPI local, 482 paths |
| Wildberries | RU | sales | P0 | research | 13 official specs local |
| Yandex Market | RU | sales | P0 | research | Feed-first, Partner API |
| Megamarket | RU | sales | P1 | research | YML/XML first |
| Avito | RU | sales | P2 | research | Classifieds model |
| Kaspi.kz | KZ | sales | P1 | research | CIS expansion |
| Uzum Market | UZ | sales | P2 | research | Uzbekistan |
| Wildberries KZ/BY | CIS | sales | P2 | research | Same API family, local entity |

## China and cross-border

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| 1688 | CN | supply | P0 | research | API for foreign developer account; procurement needs a CN receiving entity. See CN report |
| Taobao / Tmall | CN | supply / affiliate | P2 | research | Taobao Union Overseas affiliate only; no foreign seller API |
| Alibaba.com | CN | supply | P1 | research | B2B, export-oriented; Russia blocked for affiliate |
| Pinduoduo | CN | supply | P3 | research | No public API |
| JD.com | CN | supply / sales | P2 | research | Chinese entity required |
| Douyin | CN | sales | P3 | research | Chinese entity required |
| AliExpress | cross-border | sales / affiliate | P1 | research | Seller + affiliate APIs |
| Temu | cross-border | sales | P3 | blocked | No public API (verified) |
| Shein Marketplace | cross-border | sales | P3 | research | Approval required |
| Ozon Global | CN → RU | sales | P0 | blocked | Requires a Chinese legal entity; CNY/RUB control |
| WB China | CN → RU | sales | P0 | blocked | Requires a Chinese legal entity; strict 2FA |
| Xianyu / Goofish | CN | supply | P3 | blocked | No public API, ToS blocks |

## Europe

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Amazon EU | EU | sales | P1 | research | SP-API, local entity/VAT |
| eBay | EU/UK | sales | P1 | research | Sandbox, OAuth2; heavy per-API daily limits |
| Etsy | EU/UK | sales | P2 | research | OAuth2; Commercial Access is gated; 100-ID batch limit |
| Allegro | PL | sales | P1 | research | REST API; HMAC/OAuth, 9k req/min, sandbox |
| Kaufland | DE/EU | sales | P1 | research | HMAC-signed REST; 30 feeds/day CSV limit; playground |
| Bol.com | NL/BE | sales | P1 | research | Clean OAuth2 client credentials; `process-status` polling; demo env |
| Cdiscount | FR | sales | P2 | research | Login-walled Octopia portal; 100 req/min |
| Zalando | EU | sales | P2 | research | Partner-only; 2-hour JWT; per-API limits |
| OTTO | DE | sales | P2 | research | Approval required |
| Fnac | FR | sales | P3 | research | — |
| ManoMano | EU | sales | P2 | research | DIY/garden |
| eMAG | RO | sales | P2 | research | Marketplace API |
| Heureka | CZ | feeds | P3 | research | Price comparison |
| Idealo | DE/EU | feeds | P3 | research | Price comparison |

## North America

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Amazon US/CA | NA | sales | P1 | research | SP-API, LWA + RDT, hardest compliance |
| eBay US | NA | sales | P1 | research | Sandbox; Inventory 2M/day limit |
| Etsy US | NA | sales | P2 | research | Handmade/vintage rules; Commercial Access gated |
| Walmart | US | sales | P1 | research | Dynamic sandbox; 15-min tokens; delegated access |
| TikTok Shop US | US | sales | P2 | research | Partner API; compliance review 3+ weeks |
| Newegg | US | sales | P3 | research | Electronics |
| Wayfair | US | sales | P2 | research | Furniture |
| Target Plus | US | sales | P3 | research | Invite only |
| Best Buy | US/CA | sales | P3 | research | Invite only |

## Latin America

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Mercado Libre | LATAM | sales | P2 | research | AR/BR/MX/CL/CO |
| Amazon Brazil | BR | sales | P3 | research | SP-API |
| Magazine Luiza | BR | sales | P3 | research | — |
| Americanas | BR | sales | P3 | research | — |
| Falabella | CL/PE/CO | sales | P3 | research | — |

## Asia-Pacific

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Shopee | SEA | sales | P2 | research | Open Platform |
| Lazada | SEA | sales | P2 | research | Open Platform |
| Tokopedia | ID | sales | P3 | research | — |
| TikTok Shop SEA | SEA | sales | P2 | research | Partner API |
| Rakuten | JP | sales | P2 | research | RMS API |
| Yahoo Shopping | JP | sales | P3 | research | — |
| Mercari | JP | sales | P3 | research | Consumer marketplace |
| Coupang | KR | sales | P2 | research | — |
| Naver Smart Store | KR | sales | P2 | research | — |

## Middle East / Africa / Oceania

| Channel | Region | Role | Priority | Status | Notes |
|---|---|---|---|---|---|
| Amazon.ae | AE | sales | P2 | research | SP-API |
| Noon | AE/SA | sales | P2 | research | API |
| Trendyol | TR | sales | P2 | research | API |
| Hepsiburada | TR | sales | P2 | research | API |
| n11 | TR | sales | P3 | research | — |
| Jumia | AF | sales | P3 | research | — |
| Takealot | ZA | sales | P3 | research | — |
| Amazon AU | AU | sales | P2 | research | SP-API |
| eBay AU | AU | sales | P2 | research | — |
| Catch | AU | sales | P3 | research | — |
| Trade Me | NZ | sales | P3 | research | — |

## Feeds and demand surfaces (not marketplaces)

| Channel | Role | Priority | Status | Notes |
|---|---|---|---|---|
| Google Merchant Center | feed / demand | P0 | research | Content API + XML; service account; no sandbox friction |
| Meta Commerce | feed / demand | P1 | research | Catalog API; App Review required |
| Microsoft Shopping | feed | P2 | research | — |
| Pinterest Catalogs | feed | P2 | research | — |
| Criteo | feed | P2 | research | — |
| TikTok Catalog | feed | P2 | research | — |

## Definition of done for a connector

A channel is not "connected" because a request returns 200. It is done when:

1. `capability-profile.json` exists with auth, limits, requirements, currency, language.
2. Official docs URL and observed date are recorded.
3. Fixtures and contract tests exist for every implemented method.
4. L1 read works on a real account or a documented sandbox.
5. L2 price/stock write is idempotent and verified by re-read.
6. L3 card publish handles moderation and rejection.
7. L4 orders and returns are normalised and reconciled.
8. L5 certification/sandbox suite passes in CI.
9. Legal/entity requirements and prohibited categories are documented.
10. A rollback path exists for every write.

## Entity and legal gates

Before a connector moves from `research` to `building`, answer:

- Which legal entity can open the seller account?
- Which documents are required (tax, certification, labelling)?
- Which categories are restricted or banned?
- Which content rights do we have for images and descriptions?
- Which currency and settlement account are used?
- Which fulfilment model is supported (FBO/FBS/DBS/3PL)?

If any answer is unknown, the connector stays `research`. A connector built on an account that
cannot legally operate is wasted work.
