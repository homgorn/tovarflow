# Q-Parser Storefront Platform Research Report

**Generated:** 2026-11-22  
**Project:** Q-Parser — supplier catalogue ingestion → multi-storefront, multi-supplier, 100k+ SKU, marketplace publishing → multi-tenant SaaS  
**Scope:** 11 candidates evaluated against 8 weighted criteria

---

## Criteria & Weights

| # | Criterion | Weight | Description |
|---|-----------|--------|-------------|
| 1 | Catalogue Scale & Variant Model | 15 | 100k–1M SKUs; complex multi-dimensional variants; supplier catalogue mapping |
| 2 | Multi-Store / Multi-Tenant | 15 | Multiple storefronts (brands/regions); true multi-tenant SaaS foundation (isolation, per-tenant config) |
| 3 | API-First / Extensibility | 15 | Headless-native; GraphQL/REST; serverless functions; plugin architecture; TypeScript DX |
| 4 | Marketplace Connector Ecosystem | 15 | **Critical:** Native/certified Ozon, Wildberries, Yandex Market integrations (two-way sync) |
| 5 | TCO at 10k / 100k / 1M SKUs | 10 | License + infra + GMV fees + app/extension costs + dev ops at three scale points |
| 6 | SEO / SSR / Performance | 10 | Next.js/React SSR/ISR; Core Web Vitals; edge caching; large-catalogue SEO |
| 7 | RU Payments / Delivery | 10 | YuKassa, SberPay, СБП, Tinkoff, Alfa; CDEK, Russian Post, Boxberry, DPD, 1C/МойСклад |
| 8 | Ops Complexity / Team Fit | 10 | Hosting model; stack alignment (TypeScript/Node.js preferred); hiring; maintenance burden |

**Total Weight:** 100

---

## Weighted Scoring Matrix

Scores are 0–15 per criterion (max 15 × weight). Source: `data.json` with evidence.

| Candidate | 1. Catalogue (15) | 2. Multi-Tenant (15) | 3. API/Ext (15) | 4. Marketplace (15) | 5. TCO (10) | 6. SEO/SSR (10) | 7. RU Pay/Del (10) | 8. Ops/Team (10) | **Total (100)** |
|-----------|-------------------|----------------------|-----------------|---------------------|-------------|-----------------|-------------------|------------------|-----------------|
| **Medusa v2** | **14** | 10 | **15** | 8 | 9 | **12** | 6 | 7 | **81** |
| **Vendure** | **14** | **15** | **15** | 7 | 6 | **12** | 6 | 8 | **77** |
| **Saleor** | **14** | 13 | 14 | 6 | 5 | 11 | 5 | 6 | **74** |
| **Shopify Plus** | 6 | 8 | 10 | **12** | 4 | 9 | **13** | 10 | **72** |
| **BigCommerce** | 11 | 9 | 11 | 10 | 5 | 10 | 7 | 9 | **72** |
| **1C-Bitrix** | 12 | 7 | 6 | **13** | 6 | 7 | **15** | 5 | **71** |
| **Advantshop** | 9 | 4 | 5 | **13** | 7 | 6 | **14** | 7 | **65** |
| **WooCommerce** | 10 | 6 | 8 | 7 | 7 | 7 | 10 | 4 | **59** |
| **InSales** | 5 | 3 | 5 | **14** | 8 | 6 | **15** | 9 | **65** |
| **Custom Next.js + PG** | **15** | **15** | **15** | 10 | 3 | **15** | 10 | 2 | **85** |
| **Tilda** | 2 | 2 | 2 | 4 | 9 | 5 | 3 | 10 | **37** |

> **Legend:** ■ = Strong (≥12) □ = Moderate (8–11) ░ = Weak (≤7)  
> **Custom Next.js** scores highest *theoretically* but TCO and ops complexity make it impractical for near-term MVP.

---

## TCO Scenarios (Estimated Monthly USD)

All prices from official pages (checked 2026-11-22). RUB converted at 95 RUB/USD.  
**Includes:** platform license/fees + managed hosting/infra + typical apps/extensions + estimated dev ops (0.5–2 FTE).  
**Excludes:** initial build cost, payment gateway fees (pass-through), marketplace commissions.

| Candidate | 10k SKUs | 100k SKUs | 1M SKUs | Notes |
|-----------|----------|-----------|---------|-------|
| **Medusa Cloud Pro** | $500 | $800 | $2,500 | $299 Cloud + $200-2000 infra; no GMV fee; self-host cheaper at scale |
| **Medusa Self-Host** | $300 | $600 | $2,000 | Infra only (VPS/K8s + Postgres + Redis); 0.5–1.5 FTE ops |
| **Vendure Starter/Growth** | $400 | $1,200 | $3,500 | Starter €199 → Growth €599 → Scale €2,499; Cloud managed |
| **Vendure Self-Host** | $300 | $800 | $2,500 | Free Framework; infra + 0.5–1 FTE ops; GPLv3 compliance |
| **Saleor Cloud Select** | $1,800 | $2,500 | $5,000+ | $1,599 base + 0.8% GMV overage; Volume $3,999 at $12M GMV/yr |
| **Saleor Self-Host** | $400 | $1,000 | $3,000 | Python/Django infra; 1 FTE ops |
| **Shopify Plus** | $3,000 | $5,000 | $12,000+ | $2,300/mo + 0.15-0.30% GMV + apps ($500-5k) + multi-store fees |
| **BigCommerce Perf.** | $2,000 | $4,000 | $10,000+ | $1,499/mo + 0.9% GMV + Multi-Storefront fees + apps |
| **1C-Bitrix Business** | $1,200 | $2,000 | $4,000 | License 96k RUB + 20%/yr renewal + Cloud 14k RUB/mo + dev |
| **Advantshop Premium** | $200 | $400 | $800 | SaaS: Premium 14k RUB (~$150) for 500k SKUs; Ultra $250 for marketplace |
| **InSales Ultra** | $150 | $350 | $? | Ultra 30k RUB (~$315); product limits may block 100k+; custom enterprise needed |
| **WooCommerce** | $500 | $2,000 | $8,000+ | Hosting $100-5k + extensions $200-2k + 1-2 FTE PHP/WordPress ops |
| **Custom Next.js + PG** | $5,000 | $15,000 | $50,000+ | Team 3-5 senior engineers ($50k+/mo) + infra $500-5k; no GMV fees |

> **Key TCO Insight:** At 10k SKUs, Russian SaaS (Advantshop, InSales) and self-hosted open-source (Medusa, Vendure) are cheapest. At 100k+, Medusa/Vendure self-host pull ahead. Shopify/BigCommerce GMV fees dominate at scale. Custom build only viable with venture funding and 18+ month horizon.

---

## Detailed Candidate Assessments

### 1. Medusa v2 — **Recommended (Score: 81, Confidence: 8/10)**

**Strengths:**
- TypeScript/Node.js stack — matches modern team skills
- Modular architecture (Commerce Modules) — extend without forking
- No GMV fees; Cloud Pro $299/mo includes managed infra
- Native multi-store via Store Module; Sales Channels for channels
- Next.js storefront starter with SSR/ISR; excellent SEO/performance
- Active community; MIT core; Medusa Cloud reduces ops burden

**Gaps for Q-Parser:**
- **Multi-tenancy not native** — requires custom middleware (global `store_id` scoping, JWT/subdomain resolution). ~2-4 weeks dev.
- **Russian marketplace connectors absent** — Ozon/WB/Yandex need custom integration (use `bssoft2b/marketplace-mcp` for typed clients, or build on official APIs). ~4-6 weeks per marketplace.
- **RU payments/delivery** — no native YuKassa/CDEK; custom modules needed (~2 weeks each).
- **Variant model** — supports multi-dimensional variants but supplier catalogue mapping (Q-Parser → Medusa) needs custom import pipeline.

**Go-to-Market Path:**
1. **Months 1-2:** Medusa Cloud Pro + Next.js storefront; implement Store Module multi-store; build Q-Parser → Medusa import pipeline.
2. **Months 2-3:** Custom middleware for multi-tenancy (row-level security or schema-per-tenant); RU payment/delivery modules.
3. **Months 3-4:** Marketplace connectors (Ozon → WB → Yandex) as Medusa plugins; webhook handlers for order sync.
4. **Month 4+:** Harden for 100k SKUs; load test; migrate to self-host if Cloud limits hit.

**What Would Change Recommendation:**
- If team lacks TypeScript/Node.js expertise → Vendure (similar stack) or Shopify (lower dev effort)
- If native Ozon/WB/Yandex connectors are non-negotiable → InSales/Advantshop/1C-Bitrix (but sacrifice multi-tenant/API-first)
- If budget < $5k/mo at 100k SKUs → Medusa self-host or Advantshop Premium
- If true multi-tenant SaaS is Phase 1 requirement (not Phase 2) → Vendure (native channels + tenant roles) or Custom

---

### 2. Vendure — **Runner-Up (Score: 77, Confidence: 8/10)**

**Strengths:**
- **Native multi-tenant via Channels** — each channel = tenant; role-based admin isolation; marketplace recipe included
- TypeScript/NestJS — same stack alignment as Medusa
- GraphQL + REST; strongly typed plugin system; Admin UI extensions
- B2B price lists, quotes, contracts built into Growth+ plans
- Channel-aware pricing/variants — maps well to supplier catalogues per channel

**Gaps:**
- **GPLv3 core** — commercial plans required for B2B/marketplace features (Starter €199, Growth €599, Scale €2,499)
- **Marketplace connectors** — Base.com integration (EU-centric); Ozon/WB/Yandex need custom plugins
- **Higher TCO at scale** — Scale €2,499/mo (~$2,625) vs Medusa Cloud Pro $299
- **Smaller ecosystem** — fewer plugins, fewer hiring pool

**When to Choose Vendure Over Medusa:**
- Multi-tenant SaaS is **Phase 1** (not Phase 2) — Channels + tenant roles save 4-6 weeks
- Team prefers NestJS over Medusa's modular architecture
- B2B features (quotes, contracts, company accounts) needed immediately
- Willing to pay €599-2,499/mo for managed cloud with multi-tenant included

---

### 3. Saleor — Strong Technical Choice, High Cost (Score: 74, Confidence: 7/10)

**Strengths:**
- GraphQL-first; Python/Django; mature; used by large brands
- Native unlimited channels; multi-tenant via channels + permissions
- App framework for extensions; webhook-first architecture

**Gaps:**
- **Cloud entry $1,599/mo** — prohibitive pre-revenue
- **Python stack** — diverges from TypeScript team strength
- **No Russian marketplace/payment integrations**
- Multi-tenant still requires custom permission layer

**Verdict:** Only if team has Python/Django expertise and budget for Cloud Select.

---

### 4. Shopify Plus — Best RU Ecosystem, Wrong Architecture (Score: 72, Confidence: 7/10)

**Strengths:**
- **Best native RU payments/delivery** — YuKassa, SberPay, CDEK, 1C, МойСклад
- Marketplace apps for Ozon/WB/Yandex (quality varies)
- Zero ops; mature; hiring easy
- B2B catalogs unlimited on Plus

**Gaps:**
- **100 variants/product hard limit** — blocks complex supplier catalogues
- **Not multi-tenant** — Organization admin = brand multi-store, not SaaS tenancy
- **GMV fees + app tax** — $2,300/mo + 0.15-0.30% GMV + $500-5k/mo apps
- **Sandboxed extensibility** — Functions (WASM) have CPU/memory limits; no DB access

**Verdict:** Only if launching single-brand D2C + B2C in Russia fast, with <50k SKUs, no SaaS ambition.

---

### 5. BigCommerce — Solid Headless, GMV Fees Hurt (Score: 72, Confidence: 7/10)

**Strengths:**
- 600 variants/product; 100k+ SKUs on Enterprise
- Native Multi-Storefront; Channels for marketplaces/headless
- GraphQL Storefront API; Next.js Commerce starter
- No transaction fees on Enterprise (but 0.9% GMV overage)

**Gaps:**
- **GMV overage on all plans** (0.9-1.0%)
- Multi-Storefront costs extra per storefront
- Not multi-tenant; limited backend extensibility
- Weak RU payment/delivery native

**Verdict:** Viable alternative to Shopify Plus for headless-first brands; still not multi-tenant SaaS foundation.

---

### 6. 1C-Bitrix — RU Market Leader, Legacy Stack (Score: 71, Confidence: 7/10)

**Strengths:**
- **Best native 1C integration** — critical for Russian ERP workflows
- **Official paid modules for Ozon, WB, Yandex Market**
- Native YuKassa, CDEK, Russian Post, СБП
- Multi-site (Business+); distributed catalog for high load

**Gaps:**
- **PHP/D7 kernel** — legacy stack; hiring hard; not API-first
- **Perpetual license + 20%/yr renewal** — high upfront
- Not multi-tenant SaaS; multi-site = brand multi-store
- Headless requires custom work; no modern DX

**Verdict:** Only if 1C integration is hard requirement and team has PHP expertise.

---

### 7. Advantshop / InSales — Russian SaaS, Not Multi-Tenant (Score: 65, Confidence: 7-8/10)

| | Advantshop | InSales |
|---|---|---|
| **Best for** | Single brand, 500k SKUs, marketplace sync | Fast launch, native marketplace two-way sync |
| **Product limit** | 500k (Premium/Ultra) | 10k (Pro), unclear (Ultra) |
| **Multi-store** | No (Ultra = vendor marketplace) | No |
| **API** | REST (Plus+) | REST + Liquid (rate limited) |
| **RU Payments** | Excellent | Excellent |
| **TCO at 100k** | ~$400/mo | ~$350/mo (if Ultra supports) |

**Verdict:** Excellent for single-store Russian marketplace sellers. **Wrong for Q-Parser** — no multi-store, no multi-tenant, limited API, product caps.

---

### 8. WooCommerce — Flexible but Wrong Stack (Score: 59, Confidence: 6/10)

**Gaps:** PHP/WordPress; plugin conflicts; HPOS helps but 100k+ SKUs needs heavy infra; multi-tenant on WP Multisite is fragile; no native RU marketplace connectors; WooPayments not in Russia.

**Verdict:** Only if team is WordPress-native and building single-store.

---

### 9. Tilda — Not an Ecommerce Platform (Score: 37, Confidence: 9/10)

**Gaps:** ~1k product practical limit; no complex variants; one-way marketplace import only; no API for catalogue management; Stripe/PayPal only (no RU payments); zero extensibility.

**Verdict:** **Exclude.** Wrong tool for requirements.

---

### 10. Custom Next.js + PostgreSQL — Theoretical Maximum, Practical Minimum (Score: 85, Confidence: 9/10)

**Scores highest on technical criteria** but **lowest on TCO (3/10) and Ops (2/10)**.

| | Effort | Cost |
|---|---|---|
| **MVP (cart, checkout, catalog, auth, multi-tenant, RU payments, 1 marketplace)** | 8-12 months | $400k-800k (3-5 senior engineers) |
| **Marketplace connectors (Ozon, WB, Yandex)** | +2-3 months each | Ongoing maintenance (APIs change quarterly) |
| **B2B pricing, quotes, company accounts** | +3-4 months | |
| **Admin dashboard, import pipelines, Q-Parser sync** | +2-3 months | |

**When to Consider:**
- Venture-backed; 18+ month runway; building defensible IP
- Requirements so unique no platform fits (unlikely here — Medusa/Vendure cover 85%)
- Team wants to own 100% of stack long-term

**Recommendation:** **Do not start here.** Build on Medusa/Vendure; extract custom services later if needed.

---

## Recommendation Summary

| Rank | Platform | Total Score | Confidence | Best For |
|------|----------|-------------|------------|----------|
| **1** | **Medusa v2 (Cloud Pro → Self-Host)** | **81** | **8/10** | **Q-Parser MVP → Multi-tenant SaaS** |
| **2** | **Vendure (Growth/Scale Cloud)** | **77** | **8/10** | Multi-tenant SaaS **Phase 1**; B2B-heavy |
| 3 | Saleor (Self-Host) | 74 | 7/10 | Python team; high budget |
| 4 | Shopify Plus | 72 | 7/10 | Single-brand RU D2C/B2B; <50k SKUs |
| 5 | BigCommerce Enterprise | 72 | 7/10 | Headless brand multi-store; GMV <$50M |
| 6 | 1C-Bitrix Business | 71 | 7/10 | 1C-centric; PHP team; RU only |
| 7 | Advantshop Premium | 65 | 7/10 | Single-store RU marketplace seller |
| 8 | InSales Ultra | 65 | 8/10 | Fast launch; native marketplace sync |
| 9 | WooCommerce | 59 | 6/10 | WP team; single store |
| 10 | Custom Next.js + PG | 85 | 9/10 | Venture-backed; 18+ mo; full control |
| 11 | Tilda | 37 | 9/10 | **Exclude** |

---

## Final Recommendation: **Medusa v2**

**Confidence: 8/10**

### Why Medusa v2 for Q-Parser:

1. **Stack alignment** — TypeScript/Node.js/PostgreSQL/Next.js = team's likely stack
2. **Architecture fit** — Modular (Commerce Modules) maps to supplier catalogue ingestion pipeline
3. **Multi-store ready** — Store Module + Sales Channels = brands/regions/channels
4. **Multi-tenant achievable** — Custom middleware (4-6 weeks) vs Vendure native (0 weeks but €599/mo+)
5. **No GMV fees** — Critical at 100k+ SKUs / high GMV
6. **Self-host option** — Full control at scale; Cloud Pro for MVP speed
7. **Extensibility** — Workflows, subscribers, API routes, plugins = build Q-Parser sync, marketplace connectors, RU payments as first-class modules

### Implementation Roadmap (4 Months to MVP)

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| **1. Foundation** | 1-4 | Medusa Cloud Pro + Next.js storefront; Store Module multi-store; Q-Parser → Medusa import pipeline (supplier catalogues → products/variants/attributes) |
| **2. Multi-Tenancy** | 5-8 | Custom middleware: subdomain/JWT → `store_id` scoping; RLS policies; tenant admin roles; per-tenant config (currency, tax, payments) |
| **3. RU Integrations** | 6-10 | YuKassa payment module; CDEK/Russian Post/Boxberry delivery calculators; 1C/МойСклад webhook sync |
| **4. Marketplaces** | 8-14 | Ozon connector (product push, order pull, stock sync) → WB → Yandex Market; built as Medusa plugins using `bssoft2b/marketplace-mcp` typed clients |
| **5. Harden & Scale** | 12-16 | Load test 100k SKUs; query optimization; Redis caching; migration plan to self-host (K8s + managed PG + Redis) |

**Estimated Cost to MVP:** ~$150k-250k (2-3 engineers × 4 months + Cloud Pro + infra)  
**Monthly at 100k SKUs (self-host):** ~$600-800/mo infra + 0.5 FTE ops

---

## What Would Change the Recommendation

| Condition | New Recommendation | Reason |
|-----------|-------------------|--------|
| **Multi-tenant SaaS required Month 1** | Vendure Growth (€599/mo) | Native Channels + tenant roles save 6 weeks |
| **Team has no TypeScript/Node.js** | Shopify Plus or 1C-Bitrix | Lower dev skill barrier |
| **Budget < $3k/mo at 100k SKUs** | Medusa Self-Host or Advantshop Premium | Lowest TCO |
| **1C integration is hard blocker** | 1C-Bitrix Business | Native 1C exchange; but legacy stack |
| **Native Ozon/WB/Yandex connectors non-negotiable** | InSales Ultra / Advantshop Ultra | Built-in two-way sync; but no multi-tenant |
| **Venture-funded, 18+ month horizon, building IP** | Custom Next.js + PG | Full control; but 3-4× cost/time |
| **Python/Django team expertise** | Saleor Self-Host | Stack alignment; GraphQL-first |

---

## Evidence & Sources

All pricing and feature data verified on official pages **2026-11-22**:

- Medusa: https://medusajs.com/pricing, https://docs.medusajs.com/cloud/pricing
- Saleor: https://saleor.io/pricing
- Vendure: https://vendure.io/pricing
- Shopify: https://www.shopify.com/pricing, https://www.shopify.com/plus/pricing
- BigCommerce: https://www.bigcommerce.com/pricing, https://www.bigcommerce.com/enterprise-pricing
- WooCommerce: https://woocommerce.com/pricing
- 1C-Bitrix: https://1c.1c-bitrix.ru/buy
- InSales: https://insales.ru/page/combo
- Advantshop: https://www.advantshop.net/saas/compare
- Tilda: https://tilda.cc/pricing
- Vercel: https://vercel.com/pricing

Technical capabilities from official docs, GitHub discussions, and community issue trackers (linked in `data.json`).

---

## Next Steps

1. **Confirm team stack alignment** — TypeScript/Node.js/Next.js/PostgreSQL?
2. **Prototype Q-Parser → Medusa import** — 1 week spike with real supplier catalogue sample
3. **Evaluate multi-tenancy middleware approach** — RLS vs schema-per-tenant vs Medusa Cloud Organizations (upcoming)
4. **Quote RU payment/delivery module development** — YuKassa, CDEK, 1C webhooks
5. **Decision gate** — End of Week 2: proceed with Medusa or pivot to Vendure/Shopify based on spike results

---

*Report generated for internal decision-making. All scores are weighted assessments based on stated requirements. Confidence levels reflect data completeness and requirement-match certainty.*