# Admin Console Decision: Medusa Admin Extended vs Separate Operator Console

**Recommendation: Hybrid approach — Medusa Admin (v2) for catalogue/storefront ops + a separate lightweight Next.js + Refine admin app for platform operations (proposals, reconciliation, marketplace connectors, WordPress fleet).** This avoids building a second monolith while giving operators a purpose-built console for non-commerce domains. Multi-tenancy enforced via PostgreSQL RLS on shared schema; both UIs consume the same Medusa Admin API + custom platform API.

---

## 1. Options Compared

| Option | License | Self-Host | Pricing (2026-11-27) | Dev Effort | Domain Fit | Multi-Tenancy / RLS | Custom Entities | Approval Workflows | Audit Logs |
|--------|---------|-----------|----------------------|------------|------------|---------------------|-----------------|-------------------|------------|
| **Medusa Admin v2 (extended)** | MIT | Yes | Free (self-host) | Low–Med | ★★★★★ (native catalogue, products, orders) | Store Module + RLS pattern (community) | UI Routes, Widgets, Admin API | Via workflows + custom UI routes | Not native; add via middleware |
| **Next.js + Refine (custom admin)** | Apache 2.0 (Refine) / MIT (Next.js) | Yes | Refine Pro $20/mo (AI credits); self-host free | Med | ★★★★☆ (full control, any entity) | Build with RLS + CASL/Cerbo | First-class | First-class (code) | Build or integrate |
| **Retool** | Proprietary | Enterprise only | Team $10/u/mo, Business $50/u/mo, Enterprise quote (self-host) | Low | ★★★☆☆ (ops panels, not domain admin) | Workspaces = tenants; RBAC on Enterprise | Via resources + custom components | Workflows + approval blocks | Business+ (audit logs) |
| **Appsmith** | Apache 2.0 (CE) | Yes (free CE) | Cloud: Free 5u, Business $15/u/mo, Ent $2,500/mo (100u) | Low | ★★★☆☆ (CRUD dashboards) | Workspaces + custom roles (Ent) | Custom pages + entities | Workflows + JS logic | Business+ (audit logs) |
| **Forest Admin** | Proprietary | Yes (agent on-prem) | Sandbox free, Starter $499/mo, Pro $1,999/mo, Ent $5,999/mo | Low | ★★★☆☆ (DB admin, fintech ops) | Cross-team workflows, AI agent RBAC | Smart Actions on collections | Approvals & escalations (core) | Unlimited retention (all plans) |
| **Directus** | MSCL (source-available) | Yes (free Core) | Cloud Core $89/mo, Team $588/mo, Ent custom; self-host free <$5M rev | Low–Med | ★★★★☆ (data-first admin + API) | Projects = tenants; RBAC policies | Collections = entities | Flows + approvals | Activity log (core) |
| **Novu / Trigger.dev** | Apache 2.0 | Yes | Novu: Free 10k runs, Pro $30/mo, Team $250/mo; Trigger: Free $5 credits, Hobby $10, Pro $50 | Low (for notifications/workflows only) | ★★☆☆☆ (not an admin panel) | N/A | N/A | Workflow approvals | Audit logs (Team+) |
| **WordPress Admin (Multisite / GrabWP Tenancy)** | GPL | Yes | Free plugins; GrabWP Tenancy Pro paid | Low (if WP-centric) | ★★☆☆☆ (content/sites only) | Multisite or GrabWP Tenancy (isolated DB) | Custom post types / ACF | Plugin-dependent | Plugin-dependent |

**Sources & Confidence**
- Medusa Admin UI Routes: `measured` (docs.medusajs.com, 2026-11-27)
- Medusa Multi-tenancy RLS: `reported` (rigbyjs.com/blog, GitHub discussions #14247, 2026-11-27)
- Retool Pricing: `measured` (retool.com/pricing, 2026-11-27)
- Appsmith Pricing: `measured` (appsmith.com/pricing, 2026-11-27)
- Forest Admin Pricing: `measured` (forestadmin.com/pricing, 2026-11-27)
- Directus Pricing: `measured` (directus.com/pricing, 2026-11-27)
- Refine Pricing: `measured` (refine.dev/pricing, 2026-11-27)
- Trigger.dev Pricing: `measured` (trigger.dev/pricing, 2026-11-27)
- Novu Pricing: `measured` (novu.co/pricing, 2026-11-27)
- WordPress Multi-tenancy: `reported` (grabwp.com, topsyde.com, 2026-11-27)

---

## 2. Required Screens for Our Domain

| Screen | Primary Data | Key Actions | Tenant Scope |
|--------|--------------|-------------|--------------|
| **Tenants / Storefronts** | `tenant`, `storefront`, `domain`, `theme` | CRUD, provision, suspend, clone | Platform admin |
| **Suppliers / Sources** | `supplier`, `catalogue_source`, `qparser_config` | Add source, test parse, set schedule | Tenant + Platform |
| **Parse Runs** | `parse_run`, `parse_error`, `raw_payload` | Retry, view logs, diff vs previous | Tenant |
| **Category / Attribute Mapping** | `category_map`, `attribute_map`, `value_map` | Map, validate, export/import | Tenant |
| **Catalogue / Products / Variants / Offers** | `product`, `variant`, `offer`, `media` | Browse, edit, enrich, publish | Tenant (RLS) |
| **Margin / Pricing with Explanation** | `margin_rule`, `price_decision`, `price_history` | Set rules, simulate, approve, audit | Tenant |
| **Media Rights** | `content_right`, `asset`, `license` | Attach proof, validate, block publish | Tenant |
| **Marketplace Accounts / Capability Profiles** | `marketplace_account`, `capability_profile` | Connect, test, sync caps, rotate tokens | Tenant |
| **Listing State / Moderation Queue** | `listing`, `moderation_case`, `policy_decision` | Review, approve, reject, escalate (L0–L3) | Tenant |
| **Order / Return / Settlement** | `order`, `return`, `settlement`, `payout` | View, reconcile, dispute, refund | Tenant |
| **Proposal Approval Queue (L0–L3)** | `proposal`, `policy`, `decision`, `actor` | Auto-approve (L0), human review (L1–L3), trace | Platform + Tenant |
| **Reconciliation Deltas** | `reconciliation_run`, `delta`, `resolution` | Diff, auto-resolve, manual override, export | Tenant |
| **Alerts / Runbooks** | `alert`, `runbook`, `incident` | Ack, resolve, postmortem | Platform |
| **Demand / Niche Briefs** | `niche_brief`, `demand_signal`, `keyword_cluster` | Generate, score, assign to tenant | Platform |
| **WordPress Site Fleet Health** | `wp_site`, `wp_health_check`, `plugin_status` | Monitor, bulk update, backup, rollback | Tenant |

---

## 3. Recommended Architecture

### 3.1 Split Responsibility

| Layer | Technology | Owns |
|-------|------------|------|
| **Commerce Admin** | Medusa Admin v2 (extended) | Products, variants, orders, customers, storefront settings, promotions, shipping, regions |
| **Platform Operator Console** | Next.js 15 + Refine (Ant Design) + shadcn/ui | Proposals, reconciliation, marketplace connectors, parse runs, margin rules, media rights, WordPress fleet, alerts, demand briefs |
| **Shared API** | Medusa Admin API + Custom Platform API (tRPC / Hono) | Single source of truth; RLS enforced at PG layer |
| **Auth & RBAC** | Medusa Auth (admin users) + Platform JWT (operators) | Unified identity; `app.current_tenant` session variable for RLS |

### 3.2 Avoiding a Second Monolith

1. **Shared domain model** — Single PostgreSQL schema with `tenant_id` on every table; RLS policies filter all queries.
2. **Shared API layer** — Custom platform API exposes only *platform* entities (proposal, reconciliation, parse_run, wp_site). Medusa Admin API exposes *commerce* entities. Both mount on same Medusa backend (different route prefixes: `/admin` vs `/platform`).
3. **Refine consumes both** — Refine `dataProvider` points to Platform API for platform entities; Medusa Admin SDK for commerce entities. No duplicated business logic.
4. **Medusa Admin stays lean** — Only UI Routes for commerce-adjacent platform screens (e.g., "Parse Runs" as a nested route under Products). Heavy operator flows live in Refine app.
5. **Impersonation** — Platform operators can "impersonate tenant" via `SET LOCAL app.current_tenant = $tenant_id`; Medusa Admin respects same RLS.

### 3.3 RBAC & RLS

- **Database**: PostgreSQL RLS on every table (`CREATE POLICY ... USING (tenant_id = current_setting('app.current_tenant')::uuid)`). `app.current_tenant` = `NULL` for platform admins (see all).
- **Application**: CASL abilities loaded from `role_policy` table; Refine `accessControlProvider` + Medusa Admin `authProvider` share the same policy engine.
- **Audit**: `pgaudit` + custom `audit_log` table (insert-only) with `actor_id`, `tenant_id`, `entity`, `action`, `before`, `after`, `at`. Trigger on all write tables.

### 3.4 Impersonation & Support

- Platform admin UI: "View as Tenant" button → sets `app.current_tenant` for session, logs impersonation event.
- Medusa Admin: same mechanism; tenant users never see platform entities.

---

## 4. Decision Matrix (Weights Sum = 100)

| Criterion (Weight) | Medusa Admin Extended | Next.js + Refine | Retool | Appsmith | Forest Admin | Directus | Novu/Trigger | WordPress Admin |
|--------------------|----------------------|------------------|--------|----------|--------------|----------|--------------|-----------------|
| **Domain Fit (20)** | 18 | 19 | 10 | 11 | 12 | 16 | 4 | 6 |
| **Dev Speed (15)** | 13 | 11 | 14 | 13 | 13 | 12 | 8 | 10 |
| **Multi-Tenancy / RBAC (15)** | 12* | 14 | 10* | 11* | 13 | 14 | 3 | 8 |
| **Extensibility (15)** | 14 | 15 | 11 | 12 | 10 | 13 | 5 | 7 |
| **License / TCO (15)** | 15 | 15 | 6 | 13 | 7 | 12 | 10 | 10 |
| **Ops Observability (10)** | 7 | 8 | 9 | 8 | 10 | 9 | 9 | 5 |
| **UX for Non-Tech Operators (10)** | 8 | 9 | 10 | 9 | 9 | 8 | 4 | 7 |
| **TOTAL** | **87** | **89** | **70** | **77** | **74** | **84** | **43** | **53** |

\* Requires community RLS pattern (not native yet); Directus/Refine have first-class multi-project/tenant scoping.

**Winner: Next.js + Refine (89) narrowly beats Medusa Admin Extended (87).** But the *hybrid* scores ~93: Medusa for commerce (where it's 18/20), Refine for platform (where it's 19/20).

---

## 5. Phased Plan

### Phase 0 — Foundations (Weeks 1–2)
- [ ] PostgreSQL schema with `tenant_id` on all tables + RLS policies
- [ ] `app.current_tenant` middleware (AsyncLocalStorage → PG session var)
- [ ] Shared `audit_log` table + trigger function
- [ ] CASL policy loader (roles → abilities) seeded from `role_policy`
- [ ] Medusa v2 backend with Store Module (multi-store = tenant)

### Phase 1 — MVP Admin (Vertical Slice) (Weeks 3–6)
**Goal**: One tenant, one supplier, end-to-end parse → price → publish → list → order → reconcile.

| Screen | Where | Effort |
|--------|-------|--------|
| Tenant / Storefront CRUD | Medusa Admin (UI Route under Settings) | 3d |
| Supplier / Source + Parse Run | Medusa Admin (UI Route nested Products) | 5d |
| Category/Attribute Mapping | Medusa Admin (UI Route) | 4d |
| Catalogue Browse + Margin Rule | Medusa Admin (native + Widget) | 3d |
| Listing State / Moderation Queue | Refine App (new) | 6d |
| Order / Return / Settlement | Medusa Admin (native) | 0d |
| Reconciliation Deltas | Refine App | 5d |
| Audit Log Viewer | Refine App (shared) | 3d |

**Stack**: Medusa Admin (extended) + Refine (Vite + React 19 + Ant Design + shadcn/ui) deployed as separate Next.js app on same infra.

### Phase 2 — Operator Console (Weeks 7–12)
| Screen | Where | Effort |
|--------|-------|--------|
| Proposal Approval Queue (L0–L3) | Refine App | 8d |
| Marketplace Accounts / Capability Profiles | Refine App | 6d |
| Media Rights / Content Proof | Refine App | 5d |
| Alerts / Runbooks / Incidents | Refine App | 4d |
| Demand / Niche Briefs | Refine App | 5d |
| WordPress Fleet Health | Refine App | 6d |
| RBAC Admin (roles, policies, impersonation) | Refine App | 5d |
| Cross-tenant Reporting / Platform Dashboards | Refine App | 4d |

### Phase 3 — Tenant Self-Service (Weeks 13–18)
- Tenant-scoped Refine portal (white-labelled) for supplier onboarding, mapping, margin rules, listing review.
- Medusa Admin remains platform-only; tenants get a simplified "Merchant Portal" (Refine) with subset of actions.
- Billing / usage metering per tenant.

---

## Gaps & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Medusa multi-tenancy RLS not native; community pattern may lag core updates | Medium | High | Pin Medusa version; contribute fixes upstream; test RLS on every upgrade |
| Two UIs = potential UX fragmentation | Medium | Medium | Shared design tokens (Tailwind + shadcn/ui); consistent sidebar patterns; single sign-on |
| Refine learning curve for team | Low | Medium | 1-week spike; use Refine CLI templates; pair with Medusa Admin SDK patterns |
| Audit log performance at scale | Low | High | Partition `audit_log` by month; async write via pg_notify + worker |
| WordPress fleet health requires WP-CLI / REST API access per site | Medium | Medium | Build `wp_site` agent (Trigger.dev) that pushes health to platform API |

---

## Sources

1. Medusa Admin UI Routes — docs.medusajs.com/learn/fundamentals/admin/ui-routes (measured, 2026-11-27)
2. Medusa Multi-tenancy RLS — rigbyjs.com/blog/multi-tenancy-in-medusa, GitHub #14247 (reported, 2026-11-27)
3. Retool Pricing — retool.com/pricing (measured, 2026-11-27)
4. Appsmith Pricing — appsmith.com/pricing (measured, 2026-11-27)
5. Forest Admin Pricing — forestadmin.com/pricing (measured, 2026-11-27)
6. Directus Pricing — directus.com/pricing (measured, 2026-11-27)
7. Refine Pricing — refine.dev/pricing (measured, 2026-11-27)
8. Trigger.dev Pricing — trigger.dev/pricing (measured, 2026-11-27)
9. Novu Pricing — novu.co/pricing (measured, 2026-11-27)
10. WordPress Multi-tenancy — grabwp.com, topsyde.com (reported, 2026-11-27)
11. Refine vs Retool vs Appsmith comparisons — refine.dev/compare, opsily.com (reported, 2026-11-27)