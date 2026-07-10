---
name: praxis-charts-analytics-interactions
description: Use when Codex must implement, audit, or consume @praxisui/charts analytics contracts: praxis.stats chart sources, ChartStatsApiService, AnalyticsChartContractService, AnalyticsChartConfigAdapterService, queryContext, statsRequest, group-by/timeseries/distribution, drilldown, cross-filter, point selection, event mappings, dashboard widget charts, analytics projections, and dashboard/backend boundary.
---

# Praxis Charts Analytics Interactions

Use this skill when charts materialize governed analytics decisions rather than static visual widgets. The canonical boundary is: backend/resource analytics publishes executable stats and projections; `@praxisui/charts` maps them into chart documents/config and structured interactions.

Pair it with:

- `praxis-dashboard-analytics` for backend `/stats/*`, `@UiAnalytics`, `StatsFieldRegistry`, capabilities, option sources, and dashboard catalog decisions.
- `praxis-core-resource-runtime` for core analytics schema contracts, stats request builders, resource discovery, and query context.
- `praxis-charts-runtime-data` for chart document/runtime mapping.
- `praxis-charts-echarts-engine-boundary` when point/category clicks are involved.
- `praxis-charts-ai-handler-contracts` when AI operations author event mappings or data bindings.

## Source Audit

Inspect:

- `projects/praxis-charts/README.md`
- `src/lib/models/x-ui-chart.model.ts`
- `src/lib/models/chart-dataset.model.ts`
- `src/lib/models/chart-events.model.ts`
- `src/lib/services/chart-stats-api.service.ts`
- `src/lib/services/analytics-chart-contract.service.ts`
- `src/lib/services/analytics-chart-config-adapter.service.ts`
- `src/lib/services/chart-canonical-contract-mapper.service.ts`
- `src/lib/services/chart-backend-payload-adapter.service.ts`
- `src/lib/services/chart-schema-mapper.service.ts`
- `src/lib/components/praxis-chart-drilldown-panel/**`
- focused stats, analytics adapter, contract, drilldown, and component specs

If `projects/praxis-charts/AGENTS.md` is absent, use `praxis-angular-agents-governance` and record the missing local governance for chart validation gates and backend/dashboard boundary.

## Canonical Boundary

`@praxisui/charts` owns:

- `PraxisXUiChartContract.source.kind = "praxis.stats" | "derived"`;
- chart-side `queryContext` merge into remote requests;
- mapping analytics projections into `PraxisChartConfig`;
- executing chart stats through `PraxisChartStatsApiService` when `statsPath` and `statsRequest` are provided;
- structured event actions: `filter-widget`, `open-detail`, `navigate`, `update-context`, and `emit`.

Backend/resource owners own stats support, metrics, dimensions, capabilities, and option-source semantics. Hosts own dashboard layout and product shell.

## Interaction Rules

- Use `queryContext` for runtime filters, sort, limit, page, joins, host period bounds, and cross-widget context.
- Do not fold contextual filters into string-built stats paths or metric aliases.
- `crossFilter`, `drillDown`, and `selectionChange` must emit structured event actions with governed targets and field mappings.
- Capability-protected metrics must come from backend/catalog decisions; charts must not infer authorization from visible widgets.
- For analytics projections, prefer `AnalyticsChartContractService` and `AnalyticsChartConfigAdapterService` before creating custom chart payloads.
- For dashboard catalog payloads, use chart backend payload/schema mapper paths when `widget.chart` already exists.

## Inventory Before New Contract

- `ja-suportado-so-ux`: stats/queryContext/event support exists but UI, docs, panel, or host wiring is weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: chart uses local metric aliases, free-form URLs, or host event commands where stats/projection/queryContext/event contracts already exist.
- `suportado-parcialmente`: analytics path exists but mapper, adapter, drilldown, cross-filter, docs, or smoke coverage is incomplete.
- `lacuna-real-de-contrato`: no stats/projection/queryContext/event/action/catalog contract can express the analytic decision.

Only real gaps justify new public analytics or chart contracts.

## Validation

Use focused gates:

- `chart-stats-api.service.spec.ts`;
- `analytics-chart-contract.service.spec.ts`;
- `analytics-chart-config-adapter.service.spec.ts`;
- canonical mapper/backend payload/schema mapper specs;
- `praxis-chart.component.spec.ts` or drilldown panel specs for interaction wiring;
- backend/dashboard HTTP smokes only when the changed path depends on live stats metadata.

State which stats, projection, queryContext, interaction, dashboard/backend, and runtime checks were run.
