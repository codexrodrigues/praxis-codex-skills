---
name: praxis-charts-runtime-data
description: Use when Codex must inspect, change, or scaffold @praxisui/charts runtime behavior: PraxisXUiChartContract, chartDocument, PraxisChartConfig, x-ui.chart mapping, presentation microvisualizations and stackedBar legends, ECharts adapter boundaries, chart data sources, praxis.stats requests, AnalyticsChartConfigAdapterService, ChartStatsApiService, queryContext, drilldown, cross-filter, dashboard chart widgets, or chart public API.
---

# Praxis Charts Runtime Data

Use this skill for the Angular runtime side of Praxis charts. `@praxisui/charts` is the official runtime and cockpit materializer for governed chart decisions; it must not become the source of analytics business rules, metric vocabulary, SQL, or local dashboard semantics.

Pair it with:

- `praxis-dashboard-analytics` when backend `/stats/*`, `StatsFieldRegistry`, `@UiAnalytics`, capabilities, filters, or option sources change.
- `praxis-core-resource-runtime` when chart data depends on core analytics schema contracts, stats request builders, resource discovery, or query context.
- `praxis-charts-authoring-settings` when `config-editor`, Settings Panel, or chart widget input editing changes.
- `praxis-charts-ai-validation` when chart authoring manifests, edit plans, validators, or registry assets change.
- `praxis-charts-echarts-engine-boundary` for ECharts adapter lifecycle, option building, engine providers, point-event mapping, and raw option safety.
- `praxis-charts-analytics-interactions` for stats execution, analytics projections, `queryContext`, drilldown, cross-filter, point selection, or dashboard interactions.
- `praxis-charts-authoring-catalogs` for config editors, resource/field/target catalogs, preview mapping, and Settings Panel round-trip.
- `praxis-charts-ai-handler-contracts` for runtime paths that are authorable by manifest operations or AI edit plans.
- `praxis-angular-host-project` when a host must register providers or consume published chart packages.

## Canonical Boundary

Treat `PraxisXUiChartContract` / `x-ui.chart` as the public chart document. Treat `PraxisChartConfig` as the runtime config derived from that document. Keep raw ECharts options behind `ChartEngineAdapter`, `CHART_ENGINE`, `PraxisChartOptionBuilderService`, and provider internals.

Before adding a chart input, adapter, event, data source field, stats option, or public export, inventory what the platform already knows and classify the need:

- `ja-suportado-so-ux`: the chart/runtime can already materialize it; fix host usage, layout, or wiring.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the contract exists but chart document, projection id, resource path, label, or query mapping is wrong.
- `suportado-parcialmente`: a native chart path exists but a small platform extension is required.
- `lacuna-real-de-contrato`: `x-ui.chart`, core analytics, stats, capability, or option-source contracts lack data required for correct behavior.

Only `lacuna-real-de-contrato` justifies a new public contract. Do not solve missing metrics with frontend aliases, raw ECharts payloads, string-built stats URLs, dashboard-only field vocabularies, or keyword-based chart intent routing.

## Required Source Inventory

When local `praxis-ui-angular` source is available, inspect the focused files before editing:

- `projects/praxis-charts/src/public-api.ts`
- `projects/praxis-charts/src/lib/models/x-ui-chart.model.ts`
- `projects/praxis-charts/src/lib/models/chart-events.model.ts`
- `projects/praxis-charts/src/lib/models/chart-config.model.ts`
- `projects/praxis-charts/src/lib/models/chart-dataset.model.ts`
- `projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.ts`
- `projects/praxis-charts/src/lib/services/chart-contract-normalizer.service.ts`
- `projects/praxis-charts/src/lib/services/chart-contract-validation.service.ts`
- `projects/praxis-charts/src/lib/services/chart-schema-mapper.service.ts`
- `projects/praxis-charts/src/lib/services/chart-backend-payload-adapter.service.ts`
- `projects/praxis-charts/src/lib/services/chart-stats-api.service.ts`
- `projects/praxis-charts/src/lib/services/analytics-chart-config-adapter.service.ts`
- `projects/praxis-charts/src/lib/services/analytics-chart-contract.service.ts`
- `projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.ts`
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`
- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.ts`
- `projects/praxis-charts/src/lib/providers/charts.providers.ts`
- focused specs beside the changed service/model/component

Read `projects/praxis-charts/AGENTS.md` before editing chart runtime or authoring-adjacent code. Use `praxis-angular-agents-governance` if the local AGENTS file is missing, stale, or contradicts this skill.

## Runtime Rules

Use `<praxis-chart [chartDocument]="...">` for governed chart documents. Use `[config]` only when a canonical owner has already materialized `PraxisChartConfig`, such as a trusted adapter or a static local demo. Prefer `chartDocument` in dashboards, AI-authored widgets, page-builder widgets, and backend-provided catalog entries.

For remote analytics data:

- Use `source.kind = "praxis.stats"` with `source.resource` and `source.operation`.
- Let `PraxisChartCanonicalContractMapperService` derive `dataSource.query.statsPath` and `statsRequest`.
- Let `PraxisChartStatsApiService` execute `query.statsPath` plus `query.statsRequest`.
- Use `queryContext` for governed runtime context and cross-widget fan-out. The chart runtime merges `filters` into `query.filters` and `statsRequest.filter`, and writes `sort` and `limit` to the runtime `query` object.
- Treat dynamic `queryContext.sort`, `limit`, `page`, and `meta` as context available on `queryRequest` for a host resolver or observability. The default stats client posts only `statsRequest`; it does not translate `page`, `meta`, or dynamic sort into the stats payload. Static sort/limit authored in `x-ui.chart` remain part of the mapper-built `statsRequest` when the selected operation supports them.
- Preserve governed `queryContext.filterExpression` on `queryRequest`, but do not flatten it into `statsRequest.filter`. The current default `praxis.stats` client rejects filter expressions with an explicit runtime error until native stats expression support is proven.
- Do not claim native join support in the chart runtime. Model a cross-resource analytical need in the backend projection/stats contract or open a platform follow-up; never implement a dashboard-only join vocabulary.
- Keep capability decisions and safe metrics on the backend/catalog side; do not infer authorization from visible cards.

For declarative interactions:

- Treat `PraxisXUiChartContract.events` as the canonical authoring document for chart interactions. `PraxisChartCanonicalContractMapperService` derives `PraxisChartConfig.interactions` and `eventActions` from it; do not wire ad hoc ECharts callbacks in hosts.
- Keep `pointClick` as renderer-neutral raw point evidence. Configured point-click actions must flow through the structured `pointAction` output.
- Use the typed outputs from `chart-events.model.ts`: `PraxisChartPointActionEvent`, `PraxisChartSelectionEvent`, `PraxisChartDrillDownEvent`, and `PraxisChartCrossFilterEvent`. These outputs carry `filters`, optional governed `target`, source point evidence, and the declared action.
- Let `PraxisChartSchemaMapperService` derive widget outputs from `chart.events`: `pointAction`, `drillDown`, `selectionChange`, and `crossFilter`. Do not hand-author a different output vocabulary for Page Builder or dashboard widgets.
- Keep `praxis-chart.metadata.ts`, `PRAXIS_CHARTS_AUTHORING_MANIFEST`, component outputs, schema mapper outputs, and editor event operations aligned whenever an interaction field changes.

For `x-ui.analytics.projections`, use `AnalyticsChartContractService` and `AnalyticsChartConfigAdapterService` when the backend publishes discoverable analytics projections. The adapter may map projection intent to chart family, but the projection and executable stats fields remain owned by `praxis-metadata-starter` or the host resource.

For dashboard catalog payloads, choose the materialization path deliberately when the payload carries `widget.chart`:

- `PraxisChartBackendPayloadAdapterService.toWidgetInstance` preserves the canonical document as `chartDocument` and also derives `config`.
- `PraxisChartSchemaMapperService.toWidgetDefinition` currently materializes `config` and `data`; it does not preserve `chartDocument` for editor round-trip.
- Direct dashboard and Page Builder definitions may bind `[chartDocument]` without pre-materializing config.

Do not assume the schema mapper and backend payload adapter have identical round-trip behavior. If a flow must reopen, explain, or reauthor the governed document, preserve `chartDocument` through the canonical path instead of reconstructing it from runtime config. Do not create a parallel widget schema if `x-ui.chart` plus widget shell/canvas metadata is enough.

Current governed presentations include ordinary series plus KPI, gauge,
treemap, grouped scatter with two measures, funnel/pyramid, terms/histogram
distribution, and comparison projections where the backend contract supports
them. Each presentation must materialize from canonical capability/schema/stats
evidence; do not map a chart type to a visually similar ECharts series when its
dimension, measure, denominator, hierarchy, bucket, or comparison semantics are
missing.

## Shell Appearance Integration

Inspect `praxis-chart.component.ts` and `praxis-micro-visualization.component.ts`
when charts lose contrast inside a widget shell. Inherit shell foreground when no
explicit chart override is authored; retain deliberate chart configuration. The
accessible-data table has an opaque surface and must pair its own foreground with
that surface instead of inheriting light text onto white.

For micro visualizations, preserve `--prx-micro-text-color` precedence and use the
public `total` field for radial proportions. Card-summary radial presentations need
card-sized geometry; do not enlarge the compact table default globally. Cover both
contexts in the focused chart/micro specs and real-shell browser comparison. This
is runtime presentation, not a new governed analytics metric or chart catalog.

## Presentation Microvisualizations

For `<praxis-micro-visualization>`, inspect
`projects/praxis-charts/src/lib/components/praxis-micro-visualization/praxis-micro-visualization.component.ts`
and its spec, plus the Core presentation model and HTML renderer. This path
consumes `PraxisPresentationVisualizationConfig`; it does not need ECharts or a
new `x-ui.chart` document. Use `praxis-core-runtime-contracts` for the canonical
distribution validity and denominator policy. Do not add consumer repair logic.

For `stackedBar` outside table cells, opt into the complete category legend with
`legend: true` and optional `title`. Preserve all categories, including zero
allocations; use the resolved total for both widths and localized percentages.
An explicit total above the sum leaves unallocated space. Materialized hex colors
override tones and must match between segment and swatch; tone fallback must also
match. Never give zero values a minimum visible width or shrink valid proportions.

Consume Core's `getPraxisStackedBarPaintStyle` for segment/swatch paint and follow
the host-token policy in `praxis-core-runtime-contracts`. Host gradients and
shadows that follow each category use `currentColor`, which Core sets locally;
do not reference `--prx-micro-category-color` from an ancestor token. Keep these
effects in trusted host CSS rather than metadata or a parallel chart config.
Track entry is a one-shot opacity fade, with duration/delay defaulting to `0ms`
and easing to `ease-out`; reduced motion disables it even with host tokens set.
Preserve proportions and shadow halos: no width/scale/clip-path reveal. A zero
segment has no shadow even with host effects; its legend swatch keeps its style.

Use `PraxisI18nService.getLocale()` for visible and accessible percentages in
Charts; HTML consumers must pass the application locale to the Core renderer.
Keep explicit `ariaLabel` authoritative. Otherwise, when every segment is named,
generate the category/percentage summary even with `legend: false` or in table
cells; compact distributions with missing labels use `fallbackText`. Table cells
consume Core's normalized compact shape: no title or legend, and no HTML metadata
row. Invalid distributions render accessible `fallbackText`, with no partial bars
or fabricated percentages.

Run the focused microvisualization component spec and Core presentation model
spec, then the real Table and FieldShell DOM specs listed in
`praxis-core-runtime-contracts`. Prove computed colors, visible/zero dimensions,
all legend entries, denominator gaps, application locale selection, table
suppression, and adversarial fallback through the actual consumer. Build Core, Charts and a direct
consumer when the exported presentation contract changes; use focused consumer
E2E for affected public UI. Review package docs and public examples for parity,
and record any unexecuted consumer gates separately from source-level proof.
Apply Core's numerical regression procedure to both renderers: keep width
precision separate from rounded percentage labels; prove 201 equal categories
do not overflow, and hundreds of decimal fractions with an exact total do not
produce a false fallback, while genuinely incoherent tiny totals still fail.
Test Table with omitted/conflicting `surface`, rather than only a document that
already declares `table-cell`. For FieldShell DOM stability, require evidence that
`getPresentationHtml` ran through the OnPush view's own `ChangeDetectorRef` before
accepting an unchanged node as lifecycle proof. These gates require runtime
evidence; a skill update alone does not close a defect.
For host effects, include computed gradients/shadows, track height/radius/color,
zero-segment geometry and shadow suppression, default motion, and a real browser
reduced-motion override across Charts and the HTML consumers. A helper string or
media-query-dependent expectation alone does not prove those browser behaviors.

## Operational Proof

Prove the guidance against source and focused specs before declaring the skill current:

1. Happy path: map a valid `PraxisXUiChartContract` with `source.kind = "praxis.stats"`; verify canonical `statsPath`, operation-specific `statsRequest`, dimensions, metrics, filters, and projected rows.
2. Risk path: pass `queryContext` with `filters`, `sort`, `limit`, `page`, and `meta`; verify filters reach `statsRequest.filter`, sort/limit reach the runtime `query`, the complete context remains on `queryRequest`, and the default stats POST does not silently promise unsupported dynamic pagination or ordering.
3. Risk path: pass a governed `queryContext.filterExpression`; verify `queryRequest.queryContext.filterExpression` is preserved and default `praxis.stats` execution rejects it explicitly instead of flattening it into unsafe filters.
4. Interaction path: configure `pointClick`, `selectionChange`, `drillDown`, and `crossFilter` in `chartDocument.events`; verify runtime `interactions`, typed component outputs, schema mapper widget outputs, metadata ports, and authoring manifest operations stay aligned.
5. Adversarial path: reject raw ECharts options, a host-built stats URL, a local metric alias, a frontend join contract, or a host-specific interaction vocabulary when the canonical chart/stats owner already exists.

Use the focused Angular gate from the `praxis-ui-angular` root, adapting the include list only when the audited surface is narrower:

```bash
npx ng test praxis-charts --watch=false --progress=false \
  --include=projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.spec.ts \
  --include=projects/praxis-charts/src/lib/services/chart-contract-normalizer.service.spec.ts \
  --include=projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts \
  --include=projects/praxis-charts/src/lib/services/chart-stats-api.service.spec.ts \
  --include=projects/praxis-charts/src/lib/services/chart-schema-mapper.service.spec.ts \
  --include=projects/praxis-charts/src/lib/services/chart-backend-payload-adapter.service.spec.ts \
  --include=projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.spec.ts \
  --include=projects/praxis-charts/src/lib/praxis-chart.metadata.spec.ts \
  --include=projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts \
  --include=projects/praxis-charts/src/lib/config-editor/chart-authoring-coverage.matrix.spec.ts
npx ng build praxis-charts --configuration production
```

The focused specs prove Angular mapping and execution boundaries, not backend authorization, metric registration, or a published dashboard integration. Record those as unverified unless a real stats host and consumer smoke were also exercised.

## Public API

Public exports in `projects/praxis-charts/src/public-api.ts` are contract surface. Before changing them, map impacted consumers: Angular hosts, page-builder/dynamic widget materialization, dashboard catalogs, AI registry ingestion, docs/examples, and any packages importing chart models/services.

Do not reexport another public lib's root barrel through charts as a convenience facade. If shared types are needed, prefer the canonical owner, a minimal stable export in the owner, or a structural local contract when that avoids improper coupling.

## Validation

Use the narrowest reliable gate:

- changed model/mapper/validator: focused service specs for normalizer, validation, canonical mapper, schema mapper, and option builder as applicable.
- stats runtime: `chart-stats-api.service.spec.ts`, `analytics-chart-config-adapter.service.spec.ts`, and `analytics-chart-contract.service.spec.ts`.
- component wiring/events: focused component specs for `PraxisChartComponent`, `chart-schema-mapper.service.spec.ts`, `praxis-chart.metadata.spec.ts`, and the authoring manifest specs that prove `pointAction`, `selectionChange`, `drillDown`, `crossFilter`, ports, and widget outputs.
- public API change: build `@praxisui/charts` plus at least one direct consumer that imports the changed export.
- dashboard integration: HTTP/schema smokes for the referenced stats resource plus Angular smoke proving `chartDocument` and `queryContext` are used.

When validation is partial, state exactly which mapper/service/component specs ran and which dashboard/backend smokes remain unverified.
