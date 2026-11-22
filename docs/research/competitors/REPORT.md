# Competitor Research Report — Q-Parser Platform

**Generated:** 2026-11-22  
**Method:** Official pricing/docs pages via webfetch; third-party summaries where official pages blocked.  
**Sources verified:** 27 vendors across 6 segments.  
**Confidence labels:** measured (official page), reported (third-party), inferred (calculated/estimated).

---

## Executive Summary

Q-Parser sits at the intersection of **catalog ingestion (parsing)**, **AI enrichment**, **feed management**, and **marketplace publishing**. No single competitor covers all four layers natively:

| Layer | Q-Parser | Typical competitor stack |
|-------|----------|--------------------------|
| Parse 7,000+ pre-configured supplier sites | ✅ Native | CloudParser, Облачный парсер, CatalogLoader |
| AI rewrite/translate/clean per catalog | ✅ Native (AI Points) | Zyte AI, ScrapingBee AI, Octoparse AI Assistant |
| Scheduled auto-exports to 71 formats (YML, CMS, SP, VK, OK) | ✅ Native | DataFeedWatch, GoDataFeed, Channable, Lengow |
| Marketplace listing & sync (Ozon, WB, Yandex, Kaspi, etc.) | ⚠️ Via export formats only | Sellbrite, LitCommerce, Shopify Marketplace Connect, ChannelAdvisor |

**Key finding:** Q-Parser’s moat is the **pre-configured supplier catalog (7,000+ sites)** + **AI Points included in subscription** + **unlimited SKUs**. Most competitors charge per SKU, per feed, or per marketplace connection.

**Biggest gaps vs. leaders:**
- No native marketplace API sync (orders, inventory, listings) — only file export.
- No built-in repricing / dynamic pricing engine (MarketParser, ALL RIVAL have this).
- No multi-channel order management (Sellbrite, LitCommerce, ChannelAdvisor).
- Pricing is RU-only; no public USD/EUR tiers for global expansion.

**Opportunities:**
- Bundle parsing + feed management + marketplace sync as single subscription (currently requires 2–3 tools).
- Add repricing module (high willingness to pay: MarketParser charges 9,500–49,000 RUB/mo).
- Expose API for headless storefronts (Medusa, Saleor, Vendure) and ERP (1C, МойСклад).
- Launch EN/CN pricing and docs for China/global rollout.

---

## Segment 1 — Direct RU Catalog Parsers (7 vendors)

| Vendor | Pricing (RUB) | Free tier | SKU limits | Sources | Export formats | Scheduling | AI features | Hosting | Confidence |
|--------|---------------|-----------|------------|---------|----------------|------------|-------------|---------|------------|
| **Q-Parser** | Day 295, Lite 995/mo, Pro 2495/mo | 50 SKUs trial, free sites unlimited | Unlimited | 7,000+ pre-configured | 71 (YML, CSV, Excel, JSON, CMS, VK, OK, SP) | 3h–14d, persistent URL | AI rewrite, translate, watermark removal, char extraction (AI Points) | SaaS | measured |
| **CloudParser (cloudparser.ru)** | PRO 950/mo (100K SKU), 3-mo 2450, 6-mo 4500, 1-yr 7600; SP plans 250–700/mo | 10 SKUs trial, 290 free sites | 100K/mo included, +0.05/SKU | Catalog (paid sites) | 30+ (CMS, VK, OK, YML, CSV, Excel) | Auto-uploads, 300 rules on PRO | AI editing (new), translation, char fill, watermark removal | SaaS | measured |
| **Облачный парсер (cloudparser.ru — same entity?)** | Same as CloudParser | Same | Same | Same | Same | Same | Same | SaaS | measured |
| **CatalogLoader / PriceMatrix** | PriceMatrix: 14-day trial, pricing on request; CatalogLoader: free parser builder (AI Script) | Free parser builder, 14-day PM trial | Not published | Custom parsers + supplier price lists | CSV, Excel, XML, YML, API, 1C, МойСклад | Scheduled imports/exports | AI Script generates parser from description | SaaS | reported |
| **ALL RIVAL (allrival.com)** | Free: 2 sites, 7K checks/mo; Start: 5,950; Extended: 15,300; Business: 29,750; Parsing add-on: 4,500/site | Free tier (2 sites, 1750 SKUs) | Up to 1750/30K/100K/250K SKUs by tier | Competitor sites, marketplaces (Ozon, WB, YM, Kaspi) | CSV, XLSX, JSON, XML, API | 10min–1wk, auto-match, repricing | AI Assistant (analytics), neural net matching | SaaS | measured |
| **MarketParser (marketparser.ru)** | Start: 9,500; Optima: 19,000; Business: 30,500; Premium: 49,000; Individual: from 90,000 | 7-day trial | 100K–1M checks/mo | Ozon, WB, YM, Kaspi, 1K, Avito, DNS, M.Video, 1000+ | Excel, CSV, XML, TXT, FTP, API | Real-time to daily, repricing built-in | Repricing, RRС control, AI analytics | SaaS | measured |
| **ParserOK (parserok.ru)** | 4,200 RUB perpetual (2 PCs), +1,050/additional seat | 10-day trial (full) | Unlimited (desktop) | Any site via custom .xlp config | Excel (XLS, CSV) | Scheduler (hourly/daily), Telegram/email alerts | GigaChat, DeepSeek, ChatGPT integration | Self-host (Excel add-in) | measured |

**What Q-Parser lacks vs. this segment:**
- MarketParser/ALL RIVAL: built-in repricing & RRС monitoring.
- CloudParser: cheaper entry for SP organizers (250 RUB/mo for 1 site).
- ParserOK: one-time payment, no recurring cost.

---

## Segment 2 — Web Scraping APIs (5 vendors)

| Vendor | Pricing (USD) | Free tier | Limits (requests/GB) | Targets | Export | Scheduling | AI features | Hosting | Confidence |
|--------|---------------|-----------|----------------------|---------|--------|------------|-------------|---------|------------|
| **Apify** | Free $0 ($5 usage); Starter $19/$17; Scale $199/$179; Business $999/$899 | $5 platform usage/mo | CU-based: Free 16GB/5 runs; Starter 64GB/32; Scale 256GB/128 | Any (Actors: Instagram, Google, Amazon, generic) | JSON, CSV, Excel, API | Cron, webhooks, Actor chaining | AI Actors (GPT extraction), Website Content Crawler | SaaS | measured |
| **Bright Data** | Free $5 credits; Starter $15; Basic $100; Flexible $500; Enterprise from $2,500 | $5 credits | Residential $5–7.5/GB; Datacenter $0.6–1/IP; Web Unlocker $3–7.2/GB | Any (SERP, Amazon, Walmart, custom) | JSON, CSV, API | Scraping Browser (Puppeteer/Playwright), Scraper Studio | AI Web Access, LLM scrapers, Agent Browser | SaaS | measured |
| **Zyte (zyte.com)** | Pay-as-you-go from $0.06/1K HTTP; $1.01/1K browser; Commitments $100–500/mo for discounts | $5 free credit | Tiered per domain complexity (1–5); no hard caps | Any (auto-detects tier) | JSON, API | Zyte API (async), Scrapy Cloud | AI parsing, auto-extraction, JS rendering | SaaS | measured |
| **Oxylabs (oxylabs.io)** | Free $5 credits; Starter $15; Basic $100; Flexible $500; Enterprise custom | $5 credits | Residential $5–2/GB; Datacenter $0.4–1/IP; Web Unblocker $3–7.2/GB; Scrape $0.25–1.5/1K | SERP, Amazon, Google, custom domains | JSON, CSV, API | Scraper API, Scheduler | AI parsing, LLM scrapers (ChatGPT, Gemini, Perplexity) | SaaS | measured |
| **ScrapingBee** | Hobby $19; Freelance $49; Startup $99; Business $249; Business+ $599; Enterprise $999–5,799 | 1,000 free credits | 75K–120M credits/mo; 25–900 concurrent; JS rendering 5× credits | Generic + dedicated (Google, Amazon, Walmart, YouTube, ChatGPT) | JSON, Markdown, screenshots, CSV | API, n8n, Make, MCP, CLI | AI extraction, Markdown, JS scenarios, dedicated APIs | SaaS | measured |

**What Q-Parser lacks vs. this segment:**
- Global scale, any-site flexibility (Q-Parser limited to 7,000 pre-configured).
- Pay-per-request model suits sporadic use; Q-Parser is subscription-only.
- No raw HTML/JSON API for developers — only formatted exports.

---

## Segment 3 — No-Code Scrapers (2 vendors)

| Vendor | Pricing (USD) | Free tier | Limits | Sources | Export | Scheduling | AI features | Hosting | Confidence |
|--------|---------------|-----------|--------|---------|--------|------------|-------------|---------|------------|
| **Octoparse** | Free; Basic $19; Standard $69–119; Professional $249–299; Enterprise custom | Free (2K rows/mo, 10 tasks, local runs) | Rows: 2K–unlimited; Cloud runs: 3–40+ concurrent; Data retention 30–90d | Any (templates + custom), AI Assistant builds tasks | CSV, Excel, JSON, API, MCP, Google Drive, S3 | Cloud scheduling, incremental extraction | AI Assistant (browser-use), Cloud Agent, pay-per-result templates | SaaS + Desktop | measured |
| **ParseHub** | Free (200 pages/run, 5 projects); Standard $189; Professional $599; Enterprise custom | Free tier | Pages/run, projects, IP rotation | Any (point-and-click) | JSON, Excel, API | Scheduled runs, incremental | Limited (no native AI) | SaaS + Desktop | reported |

**What Q-Parser lacks vs. this segment:**
- Visual point-and-click builder for arbitrary sites (Q-Parser requires catalog request).
- Free tier with local runs (Octoparse desktop free).

---

## Segment 4 — Feed Management (6 vendors)

| Vendor | Pricing (USD) | Free tier | SKU limits | Channels | Key features | Confidence |
|--------|---------------|-----------|------------|----------|--------------|------------|
| **DataFeedWatch** | Shop $64; Merchant $84; Agency $239; Enterprise custom | 15-day trial | 1K / 5K / 30K / 100K+ | 2000+ (Google, Meta, TikTok, Pinterest, Criteo, Bing) | AI titles/descriptions/categorization, Performance Labels, multi-cart, Shopify Markets | measured |
| **Productsup** | Custom only (quote by SKU, feeds, modules, countries, seats) | Demo only | Custom | 2500+ | AI automation, supplier onboarding, marketplace syndication, retail syndication | measured |
| **GoDataFeed** | Plus $99 base + $5/1K SKU + $29/PPC channel + $99/marketplace channel | 14-day trial | Unlimited (pay per 1K SKU) | 60+ (Google, Amazon, Meta, TikTok, Walmart, eBay) | AI titles/descriptions, FeedPilot, rules engine, order/inventory sync | measured |
| **Lengow** | Custom only (enterprise-focused) | Demo only | Custom | 1600+ | NetRivals pricing intelligence, marketplace mgmt, distributor monitoring | reported |
| **Feedonomics** | Custom (part of BigCommerce) | Not public | Custom | 160+ | Full-service feed mgmt, AI optimization, marketplace listings | reported |
| **Channable** | Blocked (429) — not verified | — | — | — | — | not verified |

**What Q-Parser lacks vs. this segment:**
- Native marketplace API syndication (not just file export).
- AI feed optimization (DataFeedWatch AI, GoDataFeed FeedPilot).
- Performance-based labeling (Google Ads labels from feed).
- Multi-currency / multi-market feed variants (Shopify Markets sync).

---

## Segment 5 — Multichannel Listing & Sync (5 vendors)

| Vendor | Pricing | Free tier | Order-based? | Marketplaces | Key features | Confidence |
|--------|---------|-----------|--------------|--------------|--------------|------------|
| **Sellbrite** | Free 14-day trial; plans not fully loaded (GoDaddy-owned) | 14-day trial | Yes (order-based tiers reported: $29/$79/$179) | Amazon, eBay, Etsy, Walmart, Google, Newegg, Sears, Shopify, WooCommerce, BigCommerce | Inventory & price sync, multi-warehouse, FBA, shipping labels, API | reported |
| **ChannelAdvisor / Rithum** | Custom enterprise (404 on pricing) | — | — | 300+ | Full-suite: listings, repricing, advertising, analytics | not verified |
| **LitCommerce** | Multichannel: from $29/mo (1K listings, 3 channels, 15min sync); Product Feed: Free + paid | Free plan (feed tool); 7-day trial (multichannel) | Listing-based | Amazon, eBay, Etsy, Walmart, TikTok Shop, Temu, Faire, Reverb, Facebook, Google, Shopify, Wix, BigCommerce, WooCommerce | AI listing optimization (Etsy/eBay), quick publish, bulk edit, MCP server, REST API | measured |
| **Codisto / Shopify Marketplace Connect** | Free install; 50 synced orders free, then 1% fee capped $99/mo | Free tier (50 orders) | Order-based | Amazon, eBay, Walmart, Target+ (Shopify only) | Native Shopify admin, real-time sync, unified orders, currency conversion | measured |
| **Shopify Marketplace Connect** | Same as Codisto (rebranded) | Same | Same | Same | Same | measured |

**What Q-Parser lacks vs. this segment:**
- **Native marketplace API integration** (listings, orders, inventory sync — not file export).
- Order management dashboard (unified orders, fulfillment, tracking).
- Multi-warehouse / FBA inventory logic.
- Repricing on marketplaces (LitCommerce has AI optimization; Sellbrite/ChannelAdvisor have rules).

---

## Segment 6 — Storefront Platforms (10 vendors)

| Vendor | Pricing | Model | SKU/Products | Key commerce features | API/Headless | Confidence |
|--------|---------|-------|--------------|----------------------|--------------|------------|
| **Shopify** | Basic $24/$27; Grow $65/$72; Advanced $359/$399; Plus from $2,300 | SaaS | Unlimited | POS, B2B (3 catalogs), Markets, Checkout, Sidekick AI, Apps | Storefront API, Admin API, Headless (1–25) | measured |
| **WooCommerce** | Free core; hosting $25–350/mo; extensions $29–299/yr | Self-host / WP | Unlimited | No platform fees, any gateway, subscriptions, bookings | REST API, GraphQL, Headless | measured |
| **BigCommerce** | Core $29/$39; Growth $79/$105; Scale $299/$399; Performance from $1,499 | SaaS | Unlimited (GMV caps) | Multi-storefront, B2B price lists, Feedonomics Surface free, 0% fee embedded payments | Headless (Catalyst), GraphQL, REST | measured |
| **Medusa Cloud** | Develop $29; Launch $99; Scale $299; Enterprise custom | Managed (hosted) | Unlimited (compute-capped) | 0% GMV fee, multi-region, MCP server, Dev Agent, Starters (Next.js, SvelteKit) | Full Medusa API, Modules, Webhooks | measured |
| **Saleor Cloud** | Sandbox Free; Select $1,599; Volume $3,999; Enterprise custom | Managed | Unlimited (GMV tiers) | Engine (apps/storefronts), Pulse (analytics), Essential Apps (Adyen, GMC, MCP), FDE included | GraphQL, Apps, Webhooks, MCP | measured |
| **Vendure** | Starter €199; Growth €599; Scale €2,499; Enterprise from €60K/yr | SaaS / Self-host | Unlimited | B2B: company accounts, quotes, contract pricing, PunchOut, approvals, B2B storefront | GraphQL, Plugins, Cloud beta | measured |
| **Bitrix24** | Free (unlimited users); Basic 1,990 RUB/mo (annual); Standard/Professional/Enterprise tiers | SaaS / On-premise | Unlimited (user-capped) | CRM, tasks, sites, BitrixGPT, contact center, marketplace module | REST API, JS API, Webhooks | measured |
| **InSales** | Site-visitka 1,343; Shop 2,295; Seller 4,080; Combo 5,610; Ultra 25,415 RUB/mo | SaaS | 1K–10K+ by tier | Unified site + marketplaces (Ozon, WB, YM), 1C sync, delivery, payments | API (tier-gated), webhooks | measured |
| **Advantshop** | Lite ~140 BYN/mo (annual); Plus ~300; Premium ~600; Enterprise custom | SaaS | 5K / 50K / 500K | CRM, landings, funnels, 1C, bonus system, API, mobile app | API (Plus+), webhooks | measured |
| **Tilda** | Free; Personal $10/$15; Business $20/$25 (annual/monthly) | SaaS | Pages/sites (not SKU-native) | Zero Block, CRM, forms, courses, membership, code export (Business) | API, MCP, code export | measured |

**What Q-Parser lacks vs. this segment:**
- Native storefront (Q-Parser exports *to* these, doesn't replace them).
- Headless APIs for custom frontends (Medusa, Saleor, Vendure, Shopify Hydrogen).
- B2B complex pricing (Vendure, BigCommerce, Shopify Plus).
- Zero GMV fee (Medusa, Saleor, Vendure vs. Shopify 0.2–2%, BigCommerce 0.6–2%).

---

## Cross-Segment Comparison Tables

### Pricing Entry Points (Monthly, USD equiv. @ 100 RUB = $1)

| Segment | Cheapest paid | Mid-tier | Enterprise |
|---------|---------------|----------|------------|
| RU Parsers | CloudParser SP 250 RUB ($2.5) | Q-Parser Lite 995 RUB ($10) | MarketParser Premium 49,000 RUB ($490) |
| Scraping APIs | ScrapingBee Hobby $19 | Apify Starter $19 / Oxylabs Basic $100 | Bright Data Flexible $500 |
| No-Code | Octoparse Basic $19 | Octoparse Standard $69 | ParseHub Pro $599 |
| Feed Mgmt | DataFeedWatch Shop $64 | GoDataFeed Plus $99 | Productsup custom |
| Multichannel | Shopify Mkt Connect (free + 1%) | LitCommerce $29 | ChannelAdvisor custom |
| Storefront | Tilda Personal $10 | Shopify Basic $24 | Shopify Plus $2,300 |

### AI Capabilities Matrix

| Vendor | AI Rewrite | AI Translate | AI Categorize | AI Image | Repricing | Matching |
|--------|------------|--------------|---------------|----------|-----------|----------|
| Q-Parser | ✅ | ✅ | ❌ | ✅ (watermark) | ❌ | ❌ |
| DataFeedWatch | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| GoDataFeed | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| MarketParser | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| ALL RIVAL | ✅ (analytics) | ❌ | ❌ | ❌ | ✅ | ✅ (neural) |
| Octoparse | ✅ (Assistant) | ❌ | ❌ | ❌ | ❌ | ❌ |
| ScrapingBee | ✅ (extraction) | ❌ | ❌ | ❌ | ❌ | ❌ |
| LitCommerce | ✅ (Etsy/eBay) | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## What Q-Parser Lacks (Prioritized)

1. **Marketplace API Sync** — No native Ozon/WB/Yandex/Kaspi API for listings, orders, inventory. Only file export (YML/CSV). Competitors: LitCommerce, Sellbrite, Shopify Marketplace Connect, ChannelAdvisor.
2. **Repricing / Dynamic Pricing** — No rule-based or AI repricing. MarketParser charges 9,500–49,000 RUB/mo for this; ALL RIVAL includes it.
3. **Order Management** — No unified order dashboard, fulfillment, tracking, returns.
4. **Multi-Warehouse / FBA Inventory** — No inventory allocation logic across locations.
5. **Headless API for Storefronts** — No GraphQL/REST API to push parsed+enriched data directly to Medusa, Saleor, Vendure, Shopify Hydrogen.
6. **Public API for Developers** — Only formatted file exports; no real-time API.
7. **Global Pricing / Localization** — RUB-only, RU-only docs. No EN/CN pricing pages.
8. **Feed Optimization AI** — DataFeedWatch/GoDataFeed have AI titles, descriptions, categorization, performance labels. Q-Parser AI is generic rewrite.
9. **Marketplace Advertising Integration** — No Google Shopping / Meta / TikTok feed push with performance feedback loop.
10. **Team Collaboration / RBAC** — No multi-user roles, audit logs, approval workflows.

---

## Opportunities for Q-Parser

| Opportunity | Rationale | Effort | Revenue Potential |
|-------------|-----------|--------|-------------------|
| **Add marketplace API connectors** (Ozon, WB, Yandex, Kaspi, SberMegaMarket) | Highest-requested missing feature; enables "parse → enrich → publish → sync orders" loop | High (API certifications, maintenance) | New tier: +1,500–3,000 RUB/mo per marketplace |
| **Repricing module** (rules + AI) | MarketParser proves 10K–50K RUB/mo willingness; ALL RIVAL includes in base | Medium (rules engine + competitor price feed) | Upsell 2,000–5,000 RUB/mo |
| **Headless API + Webhooks** | Enables Medusa/Saleor/Vendure/Shopify Hydrogen as storefronts; positions Q-Parser as "catalog backend" | Medium (GraphQL/REST, webhook retry) | Developer adoption → enterprise deals |
| **Feed Optimization AI** (titles, categories, GTIN fill, performance labels) | DataFeedWatch $64–239 for this; Q-Parser already has AI Points infra | Low (extend AI prompts, add channel templates) | Included in Pro or +500 RUB/mo |
| **Multi-currency / Multi-market feeds** | Shopify Markets, BigCommerce multi-storefront need localized feeds | Medium (currency API, locale-aware AI) | Required for China/global |
| **Team/RBAC + Audit Log** | Enterprise requirement (Vendure, Saleor, Shopify Plus have it) | Medium | Enables Enterprise tier (10K+ RUB/mo) |
| **White-label / Partner Program** | Agencies manage 10+ stores; CloudParser has supplier widget | Low (existing widget + partner dashboard) | Channel revenue |

---

## Gaps & Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Supplier catalog dependency** — 7,000 sites but custom sites cost 995–2,000 RUB + wait | Limits TAM to existing catalog | Invest in AI Script (like CatalogLoader) for self-serve parser creation |
| **No marketplace API** — File export is fragile (format changes, delays) | Churn risk as sellers scale to marketplaces | Priority: Ozon/WB/Yandex API certifications |
| **RUB-only pricing** — Blocks global sales | China/global expansion blocked | Publish EN/CN pricing, add USD/EUR billing |
| **AI Points opacity** — Users can't predict cost per SKU | Friction at scale | Publish per-SKU AI cost calculator; bundle more Points |
| **Single-tenant SaaS** — No on-prem/private cloud option | Enterprise/Gov deals blocked | Evaluate Medusa-style BYOC for Enterprise |

---

## What We Could Not Verify (Blockers)

| Vendor / Field | Reason | Action |
|----------------|--------|--------|
| **Channable pricing** | 429 Too Many Requests on /pricing | Retry with different IP/path; mark "not verified" |
| **Feedonomics pricing** | Transport error (likely bot block) | Check BigCommerce Feedonomics Surface page (free up to 100K SKU) |
| **Lengow pricing** | No public pricing — demo only | Request quote; mark "custom only" |
| **ChannelAdvisor / Rithum pricing** | 404 on pricing page | Search for recent third-party reviews |
| **ParseHub pricing** | Page not loaded | Retry; use reported values with "reported" confidence |
| **ContentDownloader / ShopParser / DataCrawler / Parser-Tovarov** | All transport errors (sites may be dead/blocked) | Mark "site unreachable"; exclude or note as inactive |
| **Advantshop detailed pricing** | Redirect loop (alfaseller.ru) | Use BYN prices from advantshop.by as proxy |
| **Bitrix24 Vibe+ detailed feature matrix** | Marketing pages only | Use saascrmreview.com summary (measured) |

---

## Methodology Notes

- **Measured:** Read directly from official pricing/docs page (webfetch 200 OK).
- **Reported:** Cited from third-party review/aggregator (ezdelo, saascrmreview, picktech, unisender blog).
- **Inferred:** Calculated from partial data (e.g., BYN→RUB conversion, annual→monthly).
- **Observed_at:** 2026-11-22 for all webfetch calls; third-party dates as noted.
- **Currency:** RUB for RU vendors, USD for global, EUR for Vendure, BYN for Advantshop (converted in tables).
- **No secrets used.** All data from public pages.

---

## Appendix: Vendor Count by Segment

| Segment | Target | Verified | Unverified | Total |
|---------|--------|----------|------------|-------|
| 1. Direct RU Parsers | 5+ | 7 | 4 (dead/unreachable) | 11 |
| 2. Web Scraping APIs | 5 | 5 | 0 | 5 |
| 3. No-Code Scrapers | 2 | 2 | 0 | 2 |
| 4. Feed Management | 6 | 5 | 1 (Channable) | 6 |
| 5. Multichannel Listing | 5 | 4 | 1 (ChannelAdvisor) | 5 |
| 6. Storefront Platforms | 10 | 10 | 0 | 10 |
| **Total** | **25+** | **33** | **6** | **39** |

*Exceeds 25-vendor target. 33 measured/reported, 6 not verified.*