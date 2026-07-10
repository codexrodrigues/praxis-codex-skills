---
name: praxis-charts-analytics-interactions
description: Use when Codex must implement or audit governed @praxisui/charts analytics execution and interactions: x-ui.analytics projections, praxis.stats plans, capabilities, queryContext precedence, remote request lifecycle, group-by/timeseries/distribution response mapping, point selection, cross-filter, drill-down, declarative event actions, Page Builder composition links, or chart/table dashboard coordination.
---

# Praxis Charts Analytics Interactions

Use this skill when a chart materializes a governed analytics projection, executes `praxis.stats`, or coordinates another widget from a user interaction. Treat analytics intent, executable eligibility, visual materialization, runtime context, engine events, and cross-widget routing as distinct contracts with explicit owners.

Pair it with:

- `praxis-dashboard-analytics` for `@UiAnalytics`, `StatsFieldRegistry`, stats endpoints, capabilities, and backend proof.
- `praxis-metadata-schema-contracts` and `praxis-metadata-discovery-capabilities` for `/schemas/filtered`, `x-ui.analytics`, operation/schema identity, ETag, and current availability.
- `praxis-core-resource-runtime` for `AnalyticsSchemaContractService`, `AnalyticsStatsRequestBuilderService`, resource capabilities, and canonical `PraxisDataQueryContext`.
- `praxis-charts-runtime-data` for `PraxisXUiChartContract` to runtime config mapping and stats response projection.
- `praxis-charts-authoring-catalogs` when resource, field, metric, aggregation, or interaction targets are selected.
- `praxis-charts-echarts-engine-boundary` for renderer-neutral point/category identity and engine lifecycle.
- `praxis-core-composition-runtime` and `praxis-page-builder-composition` for component ports, state, transforms, global actions, nested paths, diagnostics, and delivery policies.
- `praxis-charts-ai-handler-contracts` when AI authors `queryContext` or event actions.

## Canonical Execution Chain

Do not collapse these owners into a dashboard-local service:

1. The real backend operation publishes `x-ui.analytics.projections[]` through `/schemas/filtered`. A projection recommends analytic intent, `praxis.stats` source, bindings, defaults, presentation families, and supported interaction hints.
2. Resource capabilities and `stats.fields[]` prove current operation and field/metric eligibility. A projection is not authorization and cannot override capabilities.
3. `AnalyticsSchemaContractService` loads the projection with schema cache identity. `AnalyticsPresentationResolver` selects a compatible family.
4. `AnalyticsStatsRequestBuilderService` derives the operation-specific `statsPath`, `statsRequest`, dimensions, metrics, sort, and limit. `AnalyticsChartConfigAdapterService` derives renderer-neutral chart config.
5. `PraxisChartComponent` merges current host context into the remote query, emits `queryRequest`, executes via a host resolver or `PraxisChartStatsApiService`, and normalizes the backend envelope into chart rows.
6. The engine emits renderer-neutral point evidence. Charts derives semantic selection/filter payloads. `composition.links` routes those outputs to state, widget inputs, surfaces, or global actions.

`PraxisXUiChartContract` persists the selected chart decision. `queryContext` is runtime context. Stats responses and point payloads are observations. None of them should become a second source of domain rules.

## Required Source Audit

Read the root and Charts `AGENTS.md`, then inspect:

- `projects/praxis-charts/src/lib/models/{x-ui-chart,chart-config,chart-dataset,chart-events}.model.ts`
- `projects/praxis-charts/src/lib/services/analytics-chart-{contract,config-adapter}.service.ts`
- `projects/praxis-charts/src/lib/services/chart-{canonical-contract-mapper,stats-api,data-transformer,contract-validation}.service.ts`
- `projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.{ts,spec.ts}`
- the active engine adapter and its click specs;
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`, AI manifest, README, and concrete dashboard hosts.

Inspect canonical owners as applicable:

- metadata-starter `@UiAnalytics`, `AnalyticsProjection`, mapper, stats DTOs, capabilities, and `StatsEligibility`;
- core analytics presentation models, schema loader, stats request builder, query-context model, composition engine, link executor, validator, transforms, diagnostics, and component ports;
- Page Builder connection editor and the concrete page definition, including nested widgets.

Repository search is mandatory. A configured boolean such as `drillDown: true` proves authoring/mapping only after a public output and a real composition path consume it.

## Projection And Capability Rules

- Resolve projections by stable `id` on the operation that publishes them. Do not select by title, labels, keywords, or array position.
- Validate source operation, dimension, metrics, aggregation, mode, and granularity against current capabilities before execution.
- `presentationHints.preferredFamilies` is a recommendation. Resolve against available families and report incompatibility; do not force Chart when another family is canonical.
- Preserve provenance: distinguish `bootstrap`, `remote`, and `fallback` configs plus the load error. A local fallback may keep an explicit demo/degraded shell usable, but must not masquerade as current metadata, eligibility, or authorization.
- Cache by API/tenant/locale/schema identity. Recompute when ETag/hash or governed context changes.
- Never hand-build stats paths from user text or infer metrics from visible rows.

## Stats Request Lifecycle

For every remote execution, prove this sequence:

1. Build a valid plan for `group-by`, `timeseries`, or `distribution` from canonical bindings.
2. Apply runtime context without mutating the persisted chart document or reusable base config.
3. Emit the exact effective `queryRequest` for observation and optional host resolution.
4. Cancel or invalidate the previous request when source, config, resolver, or `queryContext` changes. A late response must never replace newer data or state.
5. Drive `idle/loading/ready/empty/error` from the active request only and normalize technical failures through i18n/diagnostics.
6. Normalize buckets/points and multi-metric values into rows while preserving canonical category, metric alias, key, interval, and count evidence.

`PraxisChartStatsApiService` requires `query.statsPath` and `query.statsRequest`; a generic remote resolver is an explicit host-owned execution override, not permission to bypass capability and contract validation.

## Query Context

Use canonical `PraxisDataQueryContext` semantics for cross-widget runtime context. The intended precedence for currently materialized flat filters is:

1. persisted chart/source filters;
2. legacy `filterCriteria` compatibility bridge;
3. runtime `queryContext.filters`, which wins on key collision.

Runtime `queryContext.sort` and `limit` override query defaults when present. `page` and `meta` may travel as context, but do not claim they alter a stats body unless the executing adapter proves that behavior.

Do not silently flatten `filterExpression` or discard its governance/projection evidence. If Charts exposes a local bridge that omits canonical query-context fields, classify the behavior as partial and either materialize the canonical contract in the proper owner or fail closed for unsupported expression semantics. In particular, never degrade `OR`, nested groups, or governed predicates into an accidental flat `AND` map.

Cross-filter links should normally transform a chart payload into `{ filters: ... }` or another canonical query-context fragment through `composition.links`. Use link `condition`, transform pipeline, `distinct`, `distinctBy`, `debounceMs`, missing-value policy, and diagnostics where appropriate. Avoid component callbacks that manually rewrite sibling inputs.

## Interaction Semantics

Keep four layers distinct:

- engine evidence: a renderer-neutral `PraxisChartPointEvent` with truthful chart/series/category/value/data identity;
- semantic derivation: selected state and mapped source-to-target filters;
- declared action: `filter-widget`, `open-detail`, `navigate`, `update-context`, or `emit`, with governed target/mapping;
- orchestration: canonical component-port/state/global-action links execute delivery outside the chart renderer.

Rules:

- `pointClick` is raw point evidence. Do not fabricate a first-series identity for an ambiguous grid/category click.
- `selectionChange` must define select, deselect, replacement, and multi-select semantics before claiming stateful selection. A click that always emits `selected: true` is only partial selection support.
- `crossFilter` carries mapped canonical filters, target/action evidence, and its source selection. Route it to `queryContext` through a typed composition transform.
- `drillDown` needs an observable runtime event/action path; a mapped boolean without an output or dispatch is not implemented drill-down.
- `open-detail` should resolve a governed surface/action; `navigate` a governed route/action; `update-context` a state/context endpoint. The chart must not execute arbitrary strings.
- Mappings use canonical source and target field identities. Missing source values, stale targets, denied actions, and incompatible port schemas fail closed with diagnostics.
- For nested charts, preserve `nestedPath` and let the composition runtime deduplicate legacy widget-event bridges.

The AI manifest, editor, canonical mapper, component outputs, component metadata, Page Builder port catalog, runtime dispatch, and docs must agree. Validator names or authored event objects do not prove execution by themselves.

## Loop And Consistency Safety

- Use stable widget keys, port ids, link ids, action ids, and state paths.
- Model one source of shared filter truth when multiple charts/tables observe the same context.
- Use `distinct`/`distinctBy` to suppress equivalent deliveries and `debounceMs` only for real burst control, not to hide cycles.
- Detect chart A -> state -> chart B -> event -> chart A loops during composition validation and runtime diagnostics. Do not solve them with host flags or timing guesses.
- Clear or revalidate selections when data source, eligibility, target composition, or effective filters change.
- Keep technical trace payloads serializable and redacted before using runtime observations as AI grounding.

## Inventory Before New Contract

- `ja-suportado-so-ux`: the stats/event/composition path works, but loading, selection, diagnostics, trace, fallback provenance, or docs are weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host callbacks, command strings, duplicated stats paths, local query-context bridges, or manual sibling mutation replace existing canonical contracts.
- `suportado-parcialmente`: projection and config map correctly, but capabilities, query-context fields, request cancellation, event payload, public output, metadata port, composition route, or tests are incomplete.
- `lacuna-real-de-contrato`: no canonical backend fact, query-context representation, renderer-neutral event datum, target/action contract, or shared composition endpoint can express the behavior.

Only a real gap justifies a public contract. Name the missing datum and owner, affected consumers, migration, derived artifacts, and minimum proof. During beta, remove the parallel bridge/command path when canonical materialization lands.

## Validation Matrix

Prove at least:

- projection: remote success, missing id, incompatible family, capability denial, cache identity, and explicit fallback provenance;
- plan: group-by, timeseries, terms/histogram distribution, multi-metric aliases, invalid aggregation, and count semantics;
- context: precedence, collision, empty context, sort/limit override, unsupported filter expression, and immutability;
- request: default client, host resolver, sync/promise/observable result, loading/empty/error, context change, cancellation, and late-response rejection;
- interaction: point identity, mapping, no source value, select/deselect semantics, cross-filter, drill-down, every declared action kind, denied/stale target, and nested path;
- composition: event-to-state, event-to-widget `queryContext`, global action/surface, transform failure, distinct/debounce, loop diagnostics, save/reopen, and trace evidence.
- host locale: analytics labels and diagnostics are asserted under an explicitly selected locale, with global/browser locale restored between specs; do not waive an English/PT-BR mismatch as an analytics pass.

Typical focused gates are:

```bash
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/services/analytics-chart-contract.service.spec.ts' --include='projects/praxis-charts/src/lib/services/analytics-chart-config-adapter.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-stats-api.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' --include='projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.spec.ts'
npx ng test praxis-core --watch=false --progress=false --include='projects/praxis-core/src/lib/services/analytics-schema-contract.service.spec.ts' --include='projects/praxis-core/src/lib/services/analytics-stats-request-builder.service.spec.ts' --include='projects/praxis-core/src/lib/composition/link-executor.service.spec.ts' --include='projects/praxis-core/src/lib/composition/composition-runtime.engine.spec.ts'
npx ng test praxis-ui-workspace --watch=false --progress=false --include='src/app/features/table-connections-lab/table-connections-lab.page.spec.ts' --include='src/app/features/payroll-analytics-lab/payroll-analytics-lab.page.spec.ts'
npm run build:praxis-charts
```

Add metadata-starter/quickstart HTTP proof when projection, capability, eligibility, or stats DTO behavior changes. Add the focused Page Builder browser lane when interaction routing, nested ports, connection authoring, or visible diagnostics change. State exactly which backend, capability, query-context, request-race, engine, composition, browser, AI manifest, and real-host surfaces were not exercised.
