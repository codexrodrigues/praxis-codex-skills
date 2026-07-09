# Dashboard Chart Contracts

Use this reference when editing Ergon dashboard catalog entries, Angular chart widgets, or chart contract tests.

## Canonical Angular Package

Use `@praxisui/charts`.

Treat `PraxisXUiChartContract` as the public `x-ui.chart` document. The Ergon
dashboard catalog chooses and materializes chart documents for the Cockpit, but
does not redefine chart kinds, stats source semantics, event mappings, sizing,
theme, or query-context shape.

Public surfaces:

- `PraxisChartComponent`
- `PraxisChartDrilldownPanelComponent`
- `PraxisChartStateProbeComponent`
- `PraxisChartCanonicalContractMapperService`
- `PraxisChartStatsApiService`
- `AnalyticsChartContractService`
- `AnalyticsChartConfigAdapterService`

Main component selector:

```html
<praxis-chart />
```

Core inputs:

- `[chartDocument]`: `PraxisXUiChartContract`
- `[config]`: `PraxisChartConfig`
- `[data]`: `PraxisChartDataRow[]`
- `[queryContext]`: dashboard filters/context
- `[remoteDataResolver]`: host-owned resolver when not using default `praxis.stats`
- `[enableCustomization]`: enable chart editor only when authorized

Core outputs:

- `(queryRequest)`
- `(loadStateChange)`
- `(pointClick)`
- `(selectionChange)`
- `(crossFilter)`
- `(chartDocumentApplied)`
- `(chartDocumentSaved)`

## Ergon Resource Paths

Validated first-fold resources:

```text
api/dashboard/vinculos-agregados
api/dashboard/folha-agregada
```

Official first-fold chart ids:

```text
dashboard-vinculos-ranking
dashboard-folha-valor-ranking
```

Bounded/safe-on-demand resources:

```text
api/dashboard/frequencias-agregadas
api/dashboard/horas-extras-agregadas
```

Expected stats operations:

```text
POST /api/dashboard/{resource}/stats/group-by
POST /api/dashboard/{resource}/stats/timeseries
POST /api/dashboard/{resource}/stats/distribution
```

## Minimal x-ui.chart For Ergon

```json
{
  "version": "0.1.0",
  "kind": "bar",
  "chartId": "dashboard-vinculos-por-situacao",
  "sizing": { "mode": "fill-container", "minHeight": 180 },
  "theme": { "surface": { "mode": "embedded" } },
  "source": {
    "kind": "praxis.stats",
    "resource": "api/dashboard/vinculos-agregados",
    "operation": "group-by",
    "options": { "orderBy": "value-desc", "limit": 8 }
  },
  "dimensions": [
    { "field": "dimensao", "role": "category", "label": "Situacao" }
  ],
  "metrics": [
    { "field": "quantidade", "aggregation": "sum", "label": "Vinculos" }
  ],
  "events": {
    "crossFilter": { "action": "filter-widget", "target": "dashboard-table" }
  }
}
```

## Catalog Shape Recommendation

For each chart-capable panel in `GET /api/dashboard/catalog`, publish:

- `chartDocument`: full `PraxisXUiChartContract`
- `resourcePath`
- `operation`
- `projectionId`, when mirrored by `@UiAnalytics`
- `requiredCapabilities`
- `loadPolicy`
- `defaultQueryContext`
- `drillDown`
- `states`
- `optionSources`, when filters need governed labels, by-ids reload, or shared-link reopening

Treat `/schemas/filtered` and `x-ui.analytics.projections` as discovery/validation. Treat catalog as the product decision for what the dashboard should render.

Use public executable stats fields in `defaultStatsRequest` and `chartDocument`, not card aliases. For current P0:

- `field = "dimensao"` for `group-by`.
- `metricField = "quantidade"` for vinculos.
- `metricField = "valor"` for folha charts that require `dashboard:viewAmounts`.

Before adding a catalog field, classify the need:

- `ja-suportado-so-ux`: change only the Ergon Angular layout/rendering.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: align catalog keys, labels, projection ids, or chart document fields with existing Praxis metadata.
- `suportado-parcialmente`: extend the host materialization while keeping canonical `x-ui.chart`/stats semantics.
- `lacuna-real-de-contrato`: extend the canonical Praxis contract first and update docs/examples/tests.

Do not put raw ECharts options, SQL fragments, HADES context, internal metric
aliases, owner/schema names, or Angular switch discriminators into the catalog.

## Interaction Contract

Use structured chart events:

- `events.crossFilter` for filtering another widget through `queryContext`.
- `events.drillDown` for governed navigation or detail opening.
- `events.selectionChange` when the selected chart point becomes page state.

The target must be a governed widget/resource/surface reference. Do not route
interactions by command words, regexes, metric labels, or hardcoded Angular case
lists. If the target cannot be expressed with the current chart/page contracts,
record a platform follow-up instead of inventing a dashboard-only convention.

## HTTP Smoke Validation

Before Angular wiring, run the narrow catalog smoke when the host is available:

```powershell
.\tools\migration-factory\run-dashboard-first-fold-smoke.ps1 `
  -BaseUrl "http://localhost:8094" `
  -CatalogOnly `
  -Authorization "Basic <token-ou-header>" `
  -RequestTimeoutSec 30 `
  -OutputPath "docs/migracao/oracle-results/dashboard-chart-catalog-http-smoke.json"
```

Expected summary:

- `failed = 0`
- `catalogFailed = 0`
- `vinculos` publishes `dashboard-vinculos-ranking` over `api/dashboard/vinculos-agregados` with metric `quantidade`.
- `folha` publishes `dashboard-folha-valor-ranking` over `api/dashboard/folha-agregada` with metric `valor`.
- `frequencias` and `horas-extras` do not publish `chartDocument` until a governed aggregate/cache is approved.
- capability-protected amount charts are absent or blocked when `dashboard:viewAmounts` is unavailable.
- every published `chartDocument` uses `source.kind="praxis.stats"` and fields present in stats metadata.

## Load Policy Constraints

First paint may use only panels that are eligible by catalog/load status.

Never auto-query `READ_ONLY_BOUNDED_LEGACY` resources on login. Require explicit bounded period and enforce:

- `firstPaintEligible=false`
- `requiresExplicitPeriod=true`
- `maxPeriodDays`
- public state such as `NOT_CONFIGURED`, `STALE`, `EMPTY`, or `ERROR_PUBLIC`

For `STALE`, render a chart only when the catalog explicitly sets
`loadPolicy.allowStaleFirstPaint=true`; the widget must expose a visible stale
state and must not silently promote stale data to `OK`.

## Anti-Patterns

- Do not expose `EChartsOption` as a dashboard API contract.
- Do not manually build `statsPath` in each Angular component.
- Do not treat `GET /api/dashboard/catalog` as the owner of `x-ui.chart`; it is a product materialization over canonical Praxis contracts.
- Do not derive chart interactions from local keyword matching or label parsing.
- Do not make `empresa`, user, HADES transaction, schema, package, SQL, `ROWID`, or `FLAG_PACK` public filters.
- Do not let financial folha metrics render unless `viewAmounts` is authorized.
- Do not promote stale Cockpit tables to `OK` cards without `loads` confirming freshness.
