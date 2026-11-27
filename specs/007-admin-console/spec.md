# Spec 007 — Admin console

**Status:** draft for approval · **Date:** 2026-11-27 · **Depends on:** constitution, specs 001–006,
research `docs/research/admin/`.

## 1. Direct answer

Use a **hybrid**: Medusa Admin v2 (extended with UI routes) owns commerce screens; a separate
**Next.js 15 + Refine (Ant Design) + shadcn/ui** console owns platform operations. Both consume the
same PostgreSQL schema with `tenant_id` and RLS (`app.current_tenant`), and the same policy engine.
Hybrid scored ~93 versus 89 for a standalone console and 87 for Medusa Admin alone. Confidence 8/10;
the main risk is that Medusa multi-tenancy RLS is a community pattern, so pin the version and test
RLS on every upgrade.

## 2. Required screens

| Screen | Owner | Primary action |
|---|---|---|
| Tenants / storefronts | Refine | provision, suspend, clone |
| Suppliers / sources / parse runs | Refine | add source, test parse, view diff |
| Category / attribute mapping | Refine | map, validate, import/export |
| Products / variants / offers | Medusa Admin | browse, edit, publish |
| Margin / pricing explanation | Refine | set rule, simulate, approve |
| Media rights | Refine | attach proof, block publish |
| Marketplace accounts / capability profiles | Refine | connect, test, rotate |
| Listing state / moderation queue | Refine | review, approve, reject |
| Orders / returns / settlements | Medusa Admin + Refine | view, reconcile, dispute |
| Proposal approval queue (L0–L3) | Refine | auto-approve, review, trace |
| Reconciliation deltas | Refine | diff, resolve, export |
| Alerts / runbooks | Refine | acknowledge, resolve |
| Demand / niche briefs | Refine | generate, score, assign |
| WordPress fleet health | Refine | monitor, bulk update, backup |

## 3. Functional requirements

- **FR-001** One schema, two route prefixes: `/admin` (Medusa) and `/platform` (custom API).
- **FR-002** RLS on every tenant table via `app.current_tenant`; platform admins see all.
- **FR-003** CASL abilities loaded from `role_policy`; shared by Medusa auth and Refine auth provider.
- **FR-004** Append-only `audit_log` with actor, tenant, entity, action, before/after, at.
- **FR-005** Impersonation «View as Tenant» sets `app.current_tenant` for the session and logs it.
- **FR-006** Proposal screens show policy decision id, rule ids and idempotency key.
- **FR-007** Every write screen has a dry-run/simulate mode where the domain supports it.
- **FR-008** Answer-First content on operator help pages (150–300 char lead, table, source link).

## 4. Non-functional requirements

- **NFR-001** Console load < 2 s for 30-day ranges.
- **NFR-002** No cross-tenant read in any view (automated test).
- **NFR-003** WCAG 2.2 AA for approval and reconciliation screens.
- **NFR-004** All admin actions auditable within 24 hours.

## 5. Phases

1. **Phase 0 (2 weeks):** schema, RLS, audit, CASL, Medusa Store Module.
2. **Phase 1 (4 weeks):** MVP — tenants, sources, parse runs, margin, proposals, listings, reconciliation, WP fleet health.
3. **Phase 2 (6 weeks):** operator console — orders/returns/settlements, moderation, alerts, demand briefs.
4. **Phase 3 (6 weeks):** tenant self-service and themes.

## 6. Acceptance scenarios

```gherkin
Scenario: cross-tenant read is impossible
  Given tenant A session
  When the console queries tenant B listing ids
  Then RLS returns zero rows and an audit event is written

Scenario: proposal approval is traceable
  Given a price proposal with policy DENY
  When an operator overrides it
  Then the override is a new decision with actor and reason
  And the idempotency key of the original proposal is preserved

Scenario: listing moderation queue
  Given a rejected card with a reason code
  When an operator fixes the mapping and resubmits
  Then a new proposal is created
  And the old rejection stays in the audit log
```

## 7. Out of scope

- A full BI tool; ad-hoc analytics stays in SQL/Superset later.
- Custom theme editor in the first release.
- White-label tenant branding before H6.
