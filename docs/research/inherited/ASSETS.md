# Inherited assets registry

> Inventoried 2026-11-22. These are existing projects on this machine that can be reused
> instead of rebuilt. Nothing in the source folders was modified or deleted.
>
> Rule: reuse **ideas, schemas and contracts** first. Copy code only after a license check.
> Official marketplace specifications stay outside the repository (see `docs/legal`).

## 1. `H:\susa ai 500\wb china` — MAP (Marketplace Agent Platform)

The single most valuable source. It is an architecture-stage project for managing Ozon / WB /
Ozon Global / WB China seller accounts with an LLM, but the reusable part is the **adapter and
governance layer**, not the agent UI.

| Asset | Path | What it gives | Reuse decision |
|---|---|---|---|
| Ozon Seller API schema | `ozon-seller-api-openapi.json` (4.25 MB, 482 paths) | Official machine-readable contract | Read-only reference; do not commit |
| WB OpenAPI specs | `wb-api-specs/01-general.yaml` … `13-finances.yaml` | 13 official sections, ~2 MB | Read-only reference; do not commit |
| Endpoint indexes | `ozon-api-endpoints-index.md`, `wb-api-endpoints-index.md` | Human-readable method maps | Copy the **index**, not the specs |
| Business maps | `ozon-api-business-map.md`, `OZON_API_REFERENCE.md`, `WB_API_REFERENCE.md` | Domain grouping and coverage | Adapt into `docs/research/marketplaces/ru/` |
| Adapter spec | `docs/specs/002-marketplace-adapters/spec.md` | Capability profiles, error mapping, rate limiter, idempotency, contract tests | **Adopt as the connector contract** |
| Database schema | `docs/data/schema.sql` | tenant/RLS, account/credential, product/listing/offer/price_history, campaign, orders, proposal/policy/execution/verification/event | **Adopt and extend** |
| ADRs | `docs/architecture/03-adr/` | hexagonal core, no browser in nightly, MCP as edge | Reuse decisions |
| Market graph | `docs/market/KNOWLEDGE_GRAPH.md`, `graph.json` | RU seller-tool landscape (JAFO, MPSTATS, Kirsty, MPSpace, TrueStats, SalesFinder) | Merge into our graph as `competitor` nodes |
| Legal | `docs/legal/tos-and-compliance.md` | ToS, data handling, spec storage | Adopt |
| OSS stack | `docs/competitive/OPENSOURCE_STACK.md` | MIT repricer, MCP catalogs, license traps (GPL/AGPL) | Adopt as sourcing policy |

Key principles to carry over:

1. The LLM never calls a marketplace write API. It emits a typed **Proposal**.
2. A deterministic **Policy Engine** decides `ALLOW / DENY / REQUIRE_APPROVAL / ESCALATE`.
3. **Execution Engine** runs approved writes idempotently.
4. **Verifier** re-reads state and confirms the effect.
5. Every write has `idempotency_key`, `policy_decision` and an append-only event.
6. Autonomy starts at `L0_SHADOW` (observe only), then `L1_ASSIST`, `L2_GUARDED`, `L3_AUTO`.
7. `tenant_id` in every domain table; PostgreSQL RLS enabled.
8. Raw marketplace payload goes to object storage, referenced by `raw_blob_ref`.

## 2. `C:\susa ai\alibaba ali temu` — affiliate intelligence platform

A working TypeScript monorepo with 24 tables, 152 tests and a static-first storefront. Mostly
useful for **pricing, provenance and LLM discoverability**, not for marketplace connectors.

| Asset | Path | What it gives | Reuse decision |
|---|---|---|---|
| Price schema | `db/migrations/0002_pricing.sql` | price keyed by `(product, destination_country, observed_at)`, `is_complete`, daily rollup, fake-discount anomaly flag | **Adopt the price-observation model** |
| Core schema | `db/migrations/0001_core.sql` | products, categories, sources, ingestion runs | Compare with our domain model |
| Identity candidates | `0002_pricing.sql` | `product_identity_match` with signals and `reviewed_at`, never auto-merged | **Adopt the candidate pattern** |
| Static-first site | `apps/web/` | server-rendered HTML, `.md` twins, `llms.txt`, sitemap | **Adopt for storefront SEO/AEO** |
| L7 guard | `apps/web/scripts/verify-site.mjs` | fails if primary content is absent from raw HTML | **Adopt as a storefront gate** |
| Research corpus | `research/raw/r02-alibaba-b2b-platform/` | 1688 sourcing API, Taobao Union, cross-border notes | Feed into CN research |
| Verifier discipline | `feature_list.json`, `scripts/verify-*.ts` | features only pass after end-to-end verification | Adopt |

Key design points:

- A price is a function of product **and destination**, not a scalar.
- Unknown cost components are `NULL`, never `0`; a total with unknowns is marked incomplete.
- Cross-network identity matches are candidates; merging destroys attribution and is irreversible.
- Every page ships complete HTML on the server; JavaScript-only content is not acceptable.

## 3. `C:\susa ai\china auto` — evidence-first research repo

A Python project about Chinese vehicle landed prices; the domain is irrelevant, the **knowledge
method** is directly reusable.

| Asset | Path | What it gives | Reuse decision |
|---|---|---|---|
| Wiki contract | `wiki/SCHEMA.md` | atomised `concept / source / finding / question`, `confidence`, `status`, `resolves_when` | **Adopt for our research wiki** |
| Findings | `wiki/findings/` (77 files) | examples of one-claim-per-file, provenance, refutations | Use as templates |
| Verification | `tools/verify_site.py` | checks the raw HTTP response as a crawler sees it | Adopt for storefront checks |
| Tax/landed cost | `docs/06-tax-verification.md`, `data/rules.purchase-tax.json` | date-aware rule resolver with caps and refusals | Reference for CN landed cost |

The strongest idea: **a question is a first-class artefact**. `questions/open-x.md` with a
`resolves_when` clause is more durable than a confident guess.

## 4. `C:\susa ai\goofish` — negative results on Xianyu

Research on Xianyu (Goofish). The verdict is that localisation is closed technically (CSR shell,
RGV587), legally (ToS), and payment-wise (Alipay, HK only). Reuse it as a **do-not-repeat** list,
not as a code source.

## 5. `C:\susa ai\niche-radar` — demand research engine

A Laravel + React + PostgreSQL tool that turns Yandex Wordstat / Bukvarix CSV exports into
niche hypotheses. It already has the right metrics and a read-only MCP.

| Asset | Path | What it gives | Reuse decision |
|---|---|---|---|
| Data model | `docs/data-model.md` | `source_files`, `datasets`, `keywords`, `observations`, `metric_runs`, `niche_versions`, `hypotheses` | **Adopt schema and metric definitions** |
| Metrics | `docs/data-model.md` §formulas | B/R/A/G/C/P, priority_v1, presets | Reuse as `demand.metrics.v1` |
| MCP | `docs/mcp-client.example.json` | read-only tools for an external agent | Reuse as the demand-layer interface |
| Import | `bin/import` | CSV import with coverage types | Reuse or reimplement |

Decision: run niche-radar as a **sidecar service** first; copy the schema into the platform only
when multi-tenant demand data is needed.

## 6. Adjacent assets

| Path | What it is | Use |
|---|---|---|
| `C:\susa ai\admitad\research\feeds-and-exports\sources\07_aliexpress_api.md` | AliExpress affiliate API notes | CN channel research |
| `C:\susa ai\APIFY\research\rapidapi\02-marketplace.md` | API marketplace landscape | Competitor context |
| `C:\susa ai\seo` | SEO skill platform and research | Storefront SEO playbooks |
| `C:\susa ai\brain` | small schema + data | Knowledge-store patterns |

## 7. License and copying policy

| Source | License / status | Policy |
|---|---|---|
| `wb china` | Proprietary (per its README) | Ideas and schemas reusable inside the owner's projects; no external distribution |
| `alibaba ali temu` | Check `LICENSE` before copying code | Reuse schema/design; copy code only if the license allows |
| `china auto` | Check `LICENSE`/README | Reuse methodology and templates |
| `niche-radar` | Check repository license | Prefer sidecar integration |
| Official Ozon / WB specs | Vendor terms | Keep local, do not commit; fetch with a script |

## 8. What this changes in our plan

1. Do **not** write Ozon/WB connectors from scratch. Start from the 13 WB specs and the Ozon
   OpenAPI schema, and implement only the methods required by our scenarios.
2. Adopt the Proposal → Policy → Execution → Verification write path for every marketplace.
3. Use the price-observation model (destination-aware, completeness flag, daily rollup).
4. Keep identity matching as candidates with signals; never auto-merge.
5. Build the storefront static-first with `.md` twins and `llms.txt` from day one.
6. Use the atomised wiki contract (`concept/source/finding/question`) for research, not long
   undifferentiated reports.
7. Reuse niche-radar for demand before building a new demand engine.
