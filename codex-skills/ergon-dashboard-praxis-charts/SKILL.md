---
name: ergon-dashboard-praxis-charts
description: Design, implement, or review the Ergon post-login Cockpit/dashboard frontend contract using Praxis Charts. Use when Codex must connect Ergon dashboard backend resources, GET /api/dashboard/catalog, x-ui.chart/PraxisXUiChartContract, x-ui.analytics.projections, @praxisui/charts, PraxisChartComponent, providePraxisCharts(), queryContext, load policies, or chart widgets before or during Angular UI implementation.
---

# Ergon Dashboard Praxis Charts

## Core Rule

Apply the root migration `AGENTS.md` before changing dashboard contracts,
analytics metadata, chart catalog shape, or Angular chart materialization.
Classify public contract or architecture changes in the phase/gate and record
whether the canonical owner is the Ergon dashboard host, `praxis-dashboard`
contracts, `praxis-metadata-starter`, `praxis-config-starter`, or
`praxis-ui-angular`.

Use this skill when working on Ergon dashboard chart materialization. Pair it with:

- `praxis-dashboard-analytics` for backend `/stats/*`, `@UiAnalytics`, `StatsFieldRegistry`, and `x-ui.analytics.projections`.
- `praxis-angular-host-project` for Angular host bootstrap, providers, routes, API URL, and Praxis package consumption.
- `praxis-ui-product-design` only when visual polish, responsive layout, or screenshot QA is explicitly in scope.
- `praxis-dto-annotations` when chart fields, filters, numeric semantics, `@UiAnalytics`, `@Schema`, `@UISchema`, `x-ui.analytics`, `/schemas/filtered`, or OpenAPI metadata change.
- `praxis-resource-entity-lookup-backend` when dashboard filters or drill-down targets use governed option sources.

Do not create a custom chart abstraction over ECharts for Ergon dashboards. Use `@praxisui/charts` and keep ECharts behind the Praxis engine adapter.

Before adding dashboard-specific frontend adapters, inventory native Praxis
Charts/analytics support and classify the need as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or
`lacuna-real-de-contrato`. Only real contract gaps should become `Praxis
Platform Follow-up`; supported cases must use the native runtime path.

## Contract Entry Gate

Before editing Ergon dashboard catalog, chart widgets, or Angular wiring, audit the canonical sources in this order:

1. `praxis-metadata-starter`: `/stats/*`, `StatsFieldRegistry`, `@UiAnalytics`, `x-ui.analytics.projections`, `/schemas/filtered`, capabilities, option sources, and the draft `docs/spec/x-ui-chart.schema.json`.
2. `praxis-ui-angular`: `@praxisui/charts`, `PraxisXUiChartContract`, `PraxisChartComponent`, `PraxisChartCanonicalContractMapperService`, `PraxisChartStatsApiService`, authoring manifest, and current component tests for `chartDocument`, `queryContext`, `crossFilter`, and load state.
3. Ergon dashboard host artifacts: `GET /api/dashboard/catalog`, load status, `loadPolicy`, capability decisions, official first-fold panels, and the stats resources that the catalog references.

Classify every requested dashboard improvement before adding a field, endpoint, adapter, or widget:

- `ja-suportado-so-ux`: native chart/stat metadata exists; the Ergon UI must render or arrange it better.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: canonical data exists but catalog keys, labels, projection ids, or chart document fields need alignment.
- `suportado-parcialmente`: a canonical surface exists but a small platform extension or host materialization is required.
- `lacuna-real-de-contrato`: the dashboard cannot be implemented correctly without extending the canonical `x-ui.chart`, stats, capability, option-source, or chart-runtime contract.

Only `lacuna-real-de-contrato` justifies a new public contract. In that case, record the canonical owner, impacted consumers, derived docs/examples, minimum tests, and breaking-change risk before editing. Do not satisfy a cockpit-specific need by publishing raw ECharts options, local metric aliases, UI-only permissions, keyword-routed filters, or dashboard-only field vocabularies.

## Workflow

1. Read the current dashboard artifacts before editing:
   - `D:\Developer\Techne\ErgonX\migracao\docs\migracao\dashboard-implementation-plan.md`
   - `D:\Developer\Techne\ErgonX\migracao\docs\migracao\dashboard-praxis-angular-charts-investigation.md`
   - `D:\Developer\Techne\ErgonX\migracao\docs\migracao\dashboard-gate.md`
2. If changing chart contracts or catalog shape, read `references/dashboard-chart-contracts.md`.
3. Prefer evolving `GET /api/dashboard/catalog` to publish official `chartDocument` entries before adding frontend hardcode.
4. Materialize official charts with `<praxis-chart [chartDocument]="...">`; use `[config]` only when the backend or host already materialized `PraxisChartConfig`.
5. Pass dashboard filters through structured `[queryContext]`; do not manually concatenate `statsPath`, derive endpoints from strings, or duplicate stats request construction in Angular when `x-ui.chart` can derive it.
6. Enforce Ergon load policy in the UI: do not query resources marked `READ_ONLY_BOUNDED_LEGACY` during first paint or without explicit bounded period.
7. Treat `STALE` as blocked by default. For pilot/demo only, it may render first-fold charts when `GET /api/dashboard/catalog` publishes `panels[].loadPolicy.allowStaleFirstPaint=true`; keep `Carga desatualizada` visible and keep `NOT_CONFIGURED`, `DENIED`, `ERROR_PUBLIC`, `RUNNING`, `PENDING`, and `READ_ONLY_BOUNDED_LEGACY` blocked.
8. Verify that user, empresa, HADES transaction, SQL, owner/schema, package names, `ROWID`, `FLAG_PACK`, and internal metric aliases stay server-side.
9. Verify that capability-protected metrics, such as folha amount charts, are absent or blocked unless the catalog publishes the required public capability decision. Do not infer authorization from menu visibility or card presence.

## Required Frontend Pattern

Register charts once in the Angular host:

```ts
import { providePraxisCharts } from '@praxisui/charts';

export const appConfig = {
  providers: [
    ...providePraxisCharts(),
  ],
};
```

Render charts through the Praxis component:

```html
<praxis-chart
  [chartDocument]="chartDocument"
  [queryContext]="queryContext"
  (queryRequest)="onQueryRequest($event)"
  (loadStateChange)="onLoadStateChange($event)"
  (crossFilter)="onCrossFilter($event)"
/>
```

## Backend Contract Preference

For Ergon Cockpit charts, prefer:

- `source.kind = "praxis.stats"`
- `source.resource = "api/dashboard/<recurso-agregado>"`
- `source.operation = "group-by" | "timeseries" | "distribution"`
- `sizing.mode = "fill-container"` inside dashboard widgets
- `theme.surface.mode = "embedded"` when the dashboard shell owns the card surface

Use `x-ui.analytics.projections` from `/schemas/filtered` for discovery and validation. Use `GET /api/dashboard/catalog` as the product-level source of official first-fold and drill-down charts.

`GET /api/dashboard/catalog` is a materialized product decision, not the owner of the chart vocabulary. It may choose which governed chart documents appear for the Cockpit, but `x-ui.chart` shape, stats operations, query context, events, sizing, theming, and validation must remain compatible with the canonical Praxis contracts.

When catalog entries include drill-down or cross-filter behavior, model them as structured `chartDocument.events` and governed `queryContext` mappings. Do not encode target selection with command words, regex matching, metric-name conventions, or Angular-specific switch statements.

## Validation

Before calling the frontend ready:

- Confirm `@praxisui/charts` is installed/available in the host.
- Confirm `providePraxisCharts()` is registered.
- Confirm official dashboard widgets receive `chartDocument` from catalog or a governed adapter, not local ad hoc ECharts options.
- Confirm each `chartDocument` validates against `PraxisXUiChartContract` and uses `source.kind="praxis.stats"` with operation/resource/fields that exist in stats metadata.
- Confirm cross-filter and drill-down mappings emit structured `queryContext` or governed navigation targets, not local keyword routing.
- Confirm `vinculos-agregados` and `folha-agregada` charts point to their validated `/stats/*` resources.
- Confirm `frequencias-agregadas` and `horas-extras-agregadas` obey `requiresExplicitPeriod=true`, `maxPeriodDays`, and `firstPaintEligible=false` when applicable.
- Confirm option-source-backed filters use governed option-source descriptors and by-ids reload behavior when selected labels must survive reopen or shared links.
- Confirm `STALE` without `allowStaleFirstPaint=true` renders no chart/canvas and calls no `/stats/*`; confirm approved `STALE` renders with a visible stale warning.
- Run the relevant Angular tests/build and, for UI changes, perform browser/screenshot QA.

For the approved Ergon pilot/demo `STALE` path, use the repeatable local gate:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File tools/migration-factory/run-dashboard-stale-approved-pilot.ps1
```

This starts isolated backend/UI ports, enables `ERGON_DASHBOARD_ALLOW_STALE_FIRST_PAINT=true`, runs HTTP smoke, readiness without override, real Angular QA, writes evidence, and shuts down the temporary servers.
