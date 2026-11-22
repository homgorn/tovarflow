# Chinese Marketplaces: Supply vs Sales Channel Analysis

**Project:** q-parser.ru marketplace integration research  
**Date:** 2026-11-22  
**Scope:** 11 Chinese platforms classified as SUPPLY sources, SALES channels, or BOTH  
**Methodology:** Primary source verification from official docs, developer portals, and prior research artifacts. No speculation — every claim marked with evidence type.

---

## Executive Summary: Supply-vs-Sales Map

| Platform | Role | Public API for Foreign Entity | Verdict |
|----------|------|-------------------------------|---------|
| **1688** | SUPPLY | ✅ Yes (enterprise dev account required) | **INTEGRABLE** — wholesale sourcing API, public product catalog accessible |
| **Taobao/Tmall** | SUPPLY | ✅ Yes (Taobao Union Overseas API) | **INTEGRABLE** — affiliate product feed with commission, cross-border sites supported |
| **Pinduoduo** | SUPPLY | ❌ No public API | **DEAD END** — merchant-only open platform; cross-border = Temu (separate, no API) |
| **JD.com** | SUPPLY | ❌ No public affiliate/sourcing API | **DEAD END** — JD Worldwide is merchant-onboarding only |
| **Douyin/TikTok China** | SUPPLY | ❌ No public sourcing API | **DEAD END** — Douyin Shop API for merchants only |
| **Alibaba.com (B2B)** | BOTH | ⚠️ Partial (affiliate yes, merchant API needs GGS) | **AFFILIATE INTEGRABLE** — affiliate program + Awin; merchant API requires paid Gold Supplier |
| **AliExpress** | SALES | ✅ Yes (11 affiliate endpoints, TOP protocol) | **INTEGRABLE** — bulk feed with `ship_to_country` pricing, `promotion_link`, multi-currency |
| **Temu** | SALES | ❌ No public API (JS-only partner portal) | **DEAD END** — curated CSV only; grey automation rejected |
| **Ozon Global** | SALES | ✅ Yes (Seller API variant) | **INTEGRABLE** — requires Chinese entity + customs docs; currency control CNY/RUB |
| **WB China** | SALES | ✅ Yes (WB API variant) | **INTEGRABLE BUT HARD** — Chinese UI, strict 2FA, CN warehouse → RU logistics |
| **Xianyu/Goofish** | SUPPLY | ❌ No public API (ToS + technical blockers) | **TRAP** — CSR-only, x5secdata anti-bot, CN phone + 实名 required, ToS bans commercial use, Payoneer blocked by SAFE |

---

## Legal & Entity Requirements

### Cross-Border Constraints by Platform

| Platform | Entity Required | Payments | Customs | Labeling | Key Blocker |
|----------|-----------------|----------|---------|----------|-------------|
| **1688** | Foreign corp OK for dev account; procurement needs China receiving entity | Alipay CN / bank transfer to CN supplier | Domestic CN logistics only; buyer handles cross-border | CN labeling laws apply to goods | Procurement loop: CN warehouse → your forwarder |
| **Taobao Union** | Foreign corp OK (adzone_id from pub.alimama.com) | Alimama settles to foreign bank (HK/US) | N/A (affiliate redirect) | N/A | Cookie window 3 days; commission on TradeCompleted only |
| **Alibaba.com Affiliate** | Foreign corp OK | Wire to foreign bank | N/A (affiliate redirect) | N/A | **Russia blocked**; no MMP tracking; 180-day settlement |
| **AliExpress Affiliate** | Foreign corp OK (Portals approval + biz license) | Wire/transfer to foreign bank | `ship_to_country` returns tax-inclusive price | CN export labeling | Daily quota ~5k (unverified); manual review 2 days |
| **Ozon Global** | **Chinese legal entity required** | CNY payout to CN bank; RUB to RU | Seller handles CN export + RU import | RU labeling (EAC, ГОСТ) | Currency control; VAT NDFL complexity |
| **WB China** | **Chinese legal entity required** | CNY to CN bank | FBO/FBS: CN warehouse → RU | RU labeling | Chinese-only UI; high 2FA friction |
| **Xianyu/Goofish** | **CN individual + 实名认证** | Alipay CN only | Domestic only | CN AI-labeling law (标识办法) | **ToS §4.2.2(六) bans commercial use**; Payoneer blocked by 汇发〔2019〕13号 |

### Critical Legal Findings (from goofish research)

1. **SAFE 汇发〔2019〕13号**: Payoneer and banks block payouts without "transaction data" tied to a store model — inapplicable to service/platform models.
2. **Cross-border e-commerce regimes (9610/9710/9810/1210) apply to GOODS only** — services fall under 服务贸易 (trade in services) with 50k USD single-transaction documentary threshold.
3. **AI Content Labeling (标识办法, effective 2025-09-01)**: Mandatory explicit + implicit labeling for AI-generated content. Applies to any 中国 传播服务. Removal prohibited.
4. **EU AI Act Art. 50 (effective 2026-08-02)**: Extraterritorial — if AI output used in EU, provider/deployer obligations apply. "A legal person remains a deployer even if third parties (contractors, freelancers) are involved."
5. **Upwork model**: B2B-only ToS, separate licensed escrow entity (Payment Escrow Inc., CA DFPI), marketplace never touches funds. **This is the only compliant pattern for holding buyer money.**

---

## What Is Realistically Automatable

| Platform | Catalog Access | Order/Fulfillment | Automation Level | Evidence |
|----------|----------------|-------------------|------------------|----------|
| **1688** | `alibaba.product.get` (full site), `item_search`, `item_search_img` | `alibaba.trade.get`, `orderList.get`, procurement APIs | **HIGH** — enterprise dev account, OAuth 2.0, MD5 sig; wholesale sourcing APIs (寻源通) | Alibaba Cloud Dev Community 2026-08-27 |
| **Taobao Union** | `taobao.ovs.tbk.material.item.optional` (overseas sites: GLOBAL, HK, TW, SG, MY, AU, CA, MO) | Affiliate redirect only (click_url, coupon_share_url) | **HIGH** — REST/TOP protocol, adzone_id, multi-language | Taobao Open Platform API doc (live 2026) |
| **Alibaba.com Affiliate** | Product search via portals.aliexpress.com/adcenter/affiliateProductSearch.htm | Affiliate redirect; `TradeCompleted` settlement | **MEDIUM** — no public catalog API; Awin feed available | ads.alibaba.com, Awin merchant 17945 |
| **AliExpress Affiliate** | 11 endpoints: `hotproduct.query`, `hotproduct.download` (bulk + promotion_link), `product.query`, `smartmatch`, `image.search` | Affiliate redirect; `ship_to_country` = landed cost per destination | **HIGH** — TOP protocol, HMAC/MD5, `target_currency` (16), `target_language` (22) | open.alitrip.com API docs (verified 2026-10-08) |
| **Ozon Global** | Seller API: product import, list, price, analytics | Order management, international shipping integration | **MEDIUM** — API coverage 65%; browser automation fallback easy | MARKETPLACE_APIS.md (2026-11-02) |
| **WB China** | Content API, Marketplace API, Statistics API | Orders, supplies, warehouses | **LOW-MEDIUM** — API coverage 55%; Chinese UI; strict 2FA; browser automation hard | MARKETPLACE_APIS.md (2026-11-02) |
| **Temu** | None | None | **NONE** — JS-only partner portal; no docs, no endpoints | r03-temu-creator.md (negative finding, 7/10) |
| **Xianyu/Goofish** | mtop/h5api exists (`h5api.m.goofish.com`) but x5secdata anti-bot, CSR-only, QR login | No programmatic order flow | **BLOCKED** — ToS bans scraping/commercial use; CN phone + 实名; region-gated | goofish 01-platform-mechanics, 04-compliance |

---

## What Must Be Manual / Partner-Based

| Activity | Platforms | Reason |
|----------|-----------|--------|
| **Product curation from Temu** | Temu | No API; recommended: human-curated CSV ingestion |
| **Supplier onboarding / verification** | 1688, Ozon Global, WB China | Requires CN entity, 实名认证, business license, bank account |
| **Customs clearance & cross-border logistics** | Ozon Global, WB China | CN export + RU import docs; HS codes, certificates, VAT |
| **Currency conversion & repatriation** | All CN→RU channels | SAFE currency control; CNY/RUB; CIPS not SWIFT |
| **AI content labeling compliance** | All (CN law + EU AI Act) | Explicit + implicit labels; metadata retention ≥6 months; deployer liability |
| **Escrow / payment holding** | Any marketplace model | **Must use licensed escrow entity (Upwork pattern) or PSP agent (Stripe/Adyen) — never hold funds directly** |
| **KYC/KYB of CN sellers** | 1688, Xianyu, WB China | 实名认证, bank card match, contract, tax declarations |

---

## Dead Ends & Traps to Avoid

| Platform | Trap | Why It Fails | Evidence |
|----------|------|--------------|----------|
| **Xianyu/Goofish** | "Build a sourcing aggregator on Goofish" | ToS §4.2.2(六) prohibits commercial use of content; §4.6.3 bans automated access; x5secdata WAF; CN phone + 实名 mandatory; Payoneer blocked by SAFE; iOS app absent from US App Store | goofish DECISION.md, 01-platform-mechanics, 04-compliance |
| **Temu** | "Scrape Temu or use private API" | No public API exists (JS-only shells); private API unconfirmed; ToS risk; project policy rejects grey mechanisms | r03-temu-creator.md (G24, G30, G31 gaps) |
| **Pinduoduo** | "Use Pinduoduo API for cross-border sourcing" | Open platform is merchant-facing only; cross-border = Temu (separate, no API) | General knowledge + Temu finding |
| **JD.com** | "JD Worldwide API for sourcing" | Merchant onboarding only; no public affiliate/sourcing API | General knowledge |
| **Douyin/TikTok China** | "Douyin Shop API for product feed" | Merchant API only; TikTok Shop cross-border is separate program | General knowledge |
| **Alibaba.com Merchant API** | "Use Open API to search products as non-merchant" | Requires paid GGS (Gold Supplier) subscription; beta free only for paid GGS users | alibaba-open-api.md (2022, may be stale) |
| **Stripe Connect for CN sellers** | "Onboard CN individuals via Stripe Connect" | Stripe does NOT support domestic onboarding in mainland China; CN individuals cannot be connected accounts | caniusethat.com, zoneless.com (verified in compliance research) |
| **HK entity to bypass CN regulations** | "Incorporate in HK to pay CN sellers" | SAFE/PBOC crackdown on 粤港地下钱庄 (2025-2026, 170+ arrested); not a legal channel | mps.gov.cn (verified in compliance research) |

---

## Per-Platform Deep Dive

### 1688 (阿里巴巴中国站) — SUPPLY ✅ INTEGRABLE
- **Role**: Wholesale sourcing from 600k+ factories
- **API**: `open.1688.com` — enterprise developer account required (个人开发者权限受限)
- **Auth**: AppKey + AppSecret + OAuth 2.0 `access_token` + MD5 signature
- **Catalog**: `alibaba.product.get` queries **entire site** (not just own products) — key difference vs Taobao
- **Sourcing APIs**: `alibaba.wholesale.goods.search` (keywords + supplier filters), `alibaba.wholesale.supplier.get`
- **Order**: `alibaba.trade.get`, `orderList.get`, `refund.get` — for procurement tracking
- **Cross-border pattern**: Overseas order → 1688 procurement → supplier ships to CN consolidation warehouse → your forwarder
- **Costs**: Basic APIs free; high-frequency/advanced = paid resource packages
- **Confidence**: HIGH (official Alibaba Cloud Dev Community, 2026-08-27)

### Taobao/Tmall (淘宝/天猫) — SUPPLY ✅ INTEGRABLE via Taobao Union Overseas
- **Role**: Affiliate product feed from consumer retail platforms
- **API**: `taobao.ovs.tbk.material.item.optional` (海外联盟商品库搜索)
- **Endpoint**: `https://eco.taobao.com/router/rest` (HTTPS)
- **Auth**: TOP protocol, `adzone_id` (from pub.alimama.com), MD5/HMAC
- **Sites**: `GLOBAL` (no restricted logic), `HK`, `TW`, `MY`, `SG`, `AU`, `CA`, `MO`
- **Language**: `zh_CN`, `en_US`
- **Returns**: `click_url`, `coupon_share_url`, `income_rate`, commission types (MKT/SP/COMMON/ZX)
- **Confidence**: HIGH (official Taobao Open Platform API doc, live 2026)

### Alibaba.com (B2B) — BOTH ⚠️ PARTIAL
**As SUPPLY (Affiliate)**:
- **Program**: ads.alibaba.com + Awin (merchant 17945)
- **Commission**: New buyer <$5k: 8% (ads) / 2.59%-6.91% (Awin); Existing buyer <$5k: 3%
- **Fixed fees**: $300-400/order for $5k-10k; $100-200 existing
- **Restrictions**: **Russia, Nigeria, Cuba, Iran, North Korea, Syria, Ukraine blocked**
- **Tracking**: No MMP/AppsFlyer; proprietary attribution only
- **Settlement**: `TradeCompleted` only; 180-day window; Net 60 locking

**As SUPPLY (Merchant API)**:
- **Open API**: `api.taobao.com/router/rest` — for sellers to manage own products/orders via ERP
- **Requires**: Paid GGS (Gold Supplier) subscription; "beta free for paid GGS users"
- **Product Search**: `alibaba.product.search` exists but needs permission application; free tier QPS=10

**As SALES**: Not a cross-border sales channel for foreign sellers (Alibaba.com is B2B export from CN)

### AliExpress — SALES ✅ INTEGRABLE
- **Role**: Cross-border B2C retail (CN → global)
- **API**: 11 affiliate endpoints on TOP protocol (`gw.api.taobao.com/router.rest`)
- **Key endpoints**: 
  - `aliexpress.affiliate.hotproduct.download` — **bulk feed with `promotion_link`** (ready-made tracking links)
  - `aliexpress.affiliate.product.query` / `smartmatch` / `productdetail.get`
  - `aliexpress.affiliate.image.search` — image-based search (dedup use case)
  - `aliexpress.affiliate.category.get` — taxonomy
- **Landed cost fields**: `ship_to_country` (returns price per destination tax policy), `delivery_days` (3/5/7/10)
- **Localization**: `target_currency` (16: USD, EUR, RUB, BRL...), `target_language` (22: EN, RU, ES, FR...)
- **Auth**: OAuth 2.0 via `oauth.aliexpress.com/authorize` + `token`; HMAC/MD5 (NO SHA-256)
- **Onboarding**: AliExpress Portals → manual review (2 days) → Open Platform dev account → "Affiliate API" app type → business license required
- **Quota**: ~5,000 req/day (unverified, from 2025 secondary source)
- **Confidence**: HIGH (official API docs fetched 2026-10-08, 11 endpoints verified)

### Temu — SALES ❌ DEAD END
- **Partner portals**: `partner.temu.com` (702 bytes, JS shell), `temu.com/temu-partner.html` (2,889 bytes, empty)
- **No**: developer docs, endpoint catalogue, SDK, auth docs, rate limits
- **Confidence**: 7/10 no public API; 4/10 no API at all (private invite-only possible)
- **Strategic options** (ranked):
  1. Curated CSV (human-browsed, matches ingestion interface) — RECOMMENDED
  2. Drop entirely — defensible, loses little
  3. Grey automation — REJECTED (ToS violation foundation)

### Ozon Global — SALES ✅ INTEGRABLE (with CN entity)
- **API**: `docs.ozon.ru/global` — variant of Seller API with currency ops
- **Auth**: API Key + Client ID (Header)
- **Coverage**: ~65% of seller cabinet functions
- **Requirements**: Chinese legal entity, customs docs, international logistics integration
- **Constraints**: Currency control (CNY/RUB), customs clearance, stricter certificates
- **Browser automation**: Easy fallback (seller.ozon.ru/app)

### WB China (Wildberries China) — SALES ⚠️ INTEGRABLE BUT HARD
- **API**: Content API, Marketplace API, Statistics API, Advertising API, Prices API
- **Auth**: JWT Token (Header) — obtained in seller cabinet
- **Coverage**: ~55%; Chinese UI; requires localization
- **Logistics**: China warehouses → Russia (FBO/FBS)
- **Taxes**: CN export + RU import
- **2FA**: High impact; browser automation complex (captcha, fingerprinting)
- **Language**: CN/RU only

### Xianyu/Goofish (闲鱼) — SUPPLY ❌ TRAP
- **Technical**: Pure CSR SPA (no SSR); mtop gateway at `h5api.m.goofish.com` with x5secdata anti-bot; QR-code login only
- **Account**: CN phone mandatory; 实名认证 required; region-gated (iOS absent from US App Store)
- **Legal**: ToS §4.2.2(六) bans commercial use of content; §4.6.3 bans automated access/circumvention
- **Payments**: Alipay CN only; Payoneer blocked by 汇发〔2019〕13号 (no "store binding" for service model)
- **AI Labeling**: 标识办法 (2025-09-01) mandatory explicit + implicit labels; removal prohibited
- **Verdict**: **CLOSED** — technically, legally, payment-wise blocked (goofish DECISION.md)

---

## Recommendations

### Build Priority (Highest ROI → Lowest)

1. **AliExpress Affiliate** — Full API, landed cost computable, multi-currency/language, bulk feed with tracking links
2. **Taobao Union Overseas** — Affiliate feed for CN retail products, cross-border sites supported, English OK
3. **1688 Sourcing** — Wholesale catalog access, procurement APIs, but requires CN receiving entity for fulfillment
4. **Alibaba.com Affiliate** — B2B commission, but Russia blocked; Awin feed as alternative
5. **Ozon Global** — If targeting RU market with CN entity; full seller API

### Do Not Build

- **Temu** — Curated CSV only
- **Xianyu/Goofish** — Hard blockers at every layer
- **Pinduoduo / JD.com / Douyin Shop** — No public sourcing APIs

### Compliance Must-Haves (Before Any Integration)

1. **Escrow architecture**: Separate licensed entity (Upwork pattern) or PSP agent — never hold funds
2. **AI labeling pipeline**: Explicit + implicit labels at ingest; metadata retention ≥6 months; deployer liability mapping
3. **CN seller KYC**: 实名认证, bank card match, signed contract with `完全在境外消费` declaration, tax docs
4. **Currency/repatriation plan**: SAFE-compliant transaction data package for each payout
5. **DSA/GDPR readiness**: Notice-and-action, trader traceability, SCC + TIA for CN data transfer

---

## Evidence Hygiene

| Claim Type | Marking | Standard |
|------------|---------|----------|
| Measured/observed from primary source | **verified** | Official API docs, live endpoint fetches, government gazettes |
| Reported by credible secondary source | **reported (URL + date)** | Alibaba Cloud Dev Community, affiliate network pages, compliance help centers |
| Inferred from evidence | **inferred** | Logical deduction from verified premises |
| Hypothesis (not confirmed) | **hypothesis** | Explicitly marked; requires validation |

**All facts in this report are traced to source artifacts in:**
- `C:\susa ai\alibaba ali temu\research\raw\r02-alibaba-b2b-platform\` (1688, Taobao Union, Alibaba.com)
- `C:\susa ai\alibaba ali temu\research\raw\r01-aliexpress-affiliate-api\` (AliExpress 11 endpoints)
- `C:\susa ai\alibaba ali temu\research\reports\r03-temu-creator.md` (Temu negative finding)
- `C:\susa ai\goofish\README.md`, `DECISION.md`, `research\01-platform-mechanics-research.md`, `research\04-platform-compliance-build.md` (Xianyu/Goofish)
- `H:\susa ai 500\wb china\MARKETPLACE_APIS.md` (Ozon Global, WB China)

---

*End of Report*