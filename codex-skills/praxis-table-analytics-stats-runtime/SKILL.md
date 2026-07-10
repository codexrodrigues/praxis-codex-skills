---
name: praxis-table-analytics-stats-runtime
description: Use when Codex must implement, audit, or debug @praxisui/table analytics table runtime: analytics projections, analytic-table family resolution, AnalyticsTableContractService, AnalyticsTableStatsApiService, AnalyticsTableConfigAdapterService, stats request builders, queryContext filters, fallback rows, dashboard table views, or analytics diagnostics.
---

# Praxis Table Analytics Stats Runtime

Use this skill when table behavior is driven by governed analytics projections or stats endpoints.

Analytics tables are materializations of canonical `x-ui.analytics` projections. `@praxisui/core` resolves and builds analytics stats requests; `@praxisui/table` adapts the projection into `TableConfig` plus local rows. Do not invent dashboard-specific metric payloads in table consumers.

## Source Audit

Inspect before editing:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/analytics/analytics-table.model.ts`
- `projects/praxis-table/src/lib/analytics/analytics-table-contract.service.ts`
- `projects/praxis-table/src/lib/analytics/analytics-table-stats-api.service.ts`
- `projects/praxis-table/src/lib/analytics/analytics-table-config-adapter.service.ts`
- `projects/praxis-core/src/lib/services/analytics-presentation-resolver.service.ts`
- `projects/praxis-core/src/lib/services/analytics-schema-contract.service.ts`
- `projects/praxis-core/src/lib/services/analytics-stats-request-builder.service.ts`
- focused analytics table and core analytics specs.

Inspect `praxis-metadata-starter` when the projection or stats endpoint contract changes.

## Canonical Flow

1. Load analytics schema from core `AnalyticsSchemaContractService`.
2. Find the projection by `projectionId`.
3. Resolve presentation with `AnalyticsPresentationResolver`, preferring `analytic-table`.
4. Build the stats execution plan with core `AnalyticsStatsRequestBuilderService`.
5. Apply normalized table `queryContext.filters` to the stats request.
6. Execute stats API and project buckets/points into `AnalyticsTableRow[]`.
7. Adapt projection into a local-mode `TableConfig` with pagination/sorting client strategies.
8. Fall back to declared fallback projection/rows with an explicit source/error when remote analytics fails.

## Analytics Rules

- The projection must publish a primary dimension and at least one metric.
- Ambiguous projections should fall back to `analytic-table` only when the resolver says so; do not force charts or tables from label matching.
- Time-series, group-by, and distribution responses must map through the stats API adapter; do not create per-dashboard response parsers.
- Query filters must come from `PraxisDataQueryContext`, not bespoke dashboard filter objects.
- Fallback rows are operational fallback evidence; they are not the canonical source of analytics semantics.
- Keep analytics table config local-mode, with client pagination/sorting, disabled row/bulk actions unless a governed action is explicitly modeled.

## Aderence Inventory

Classify before adding analytics fields or services:

- `ja-suportado-so-ux`: projection/stats data exists but the table/dashboard does not present source, error, or fallback clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: dashboard payload should map to `PraxisAnalyticsProjection`, stats request, or `AnalyticsTableViewModel`.
- `suportado-parcialmente`: projection can be resolved but request building, query context, row projection, fallback, docs, or consumer proof is incomplete.
- `lacuna-real-de-contrato`: no analytics projection, stats operation, query context, or table view model can express the analytic decision.

Only real gaps justify backend/core analytics contract changes.

## Validation

Use focused proof:

- `analytics-table-contract.service.spec.ts`
- `analytics-table-stats-api.service.spec.ts`
- `analytics-table-config-adapter.service.spec.ts`
- core analytics resolver/schema/request builder specs when projection semantics change.
- dashboard or host smoke when the analytics table is user-visible.

For first-step issue resolution, audit: projection id, resolved family/reason, stats path/request, queryContext filters, row mapping, fallback source/error, generated `TableConfig`, and empty/loading/error presentation.

## Companion Skills

- Use `praxis-table-runtime-data` for table rendering and local data behavior.
- Use `praxis-dashboard-analytics` when a dashboard consumes the table view model.
- Use `praxis-core-resource-runtime` for core analytics projection and request contracts.
- Use `praxis-angular-public-api-governance` if analytics exports change.
