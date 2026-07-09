# Dashboard Chart Contracts

Use this reference when editing Ergon dashboard catalog entries, Angular chart widgets, or chart contract tests.

## Canonical Angular Package

Use `@praxisui/charts`.

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

Treat `/schemas/filtered` and `x-ui.analytics.projections` as discovery/validation. Treat catalog as the product decision for what the dashboard should render.

Use public executable stats fields in `defaultStatsRequest` and `chartDocument`, not card aliases. For current P0:

- `field = "dimensao"` for `group-by`.
- `metricField = "quantidade"` for vinculos.
- `metricField = "valor"` for folha charts that require `dashboard:viewAmounts`.

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

## Load Policy Constraints

First paint may use only panels that are eligible by catalog/load status.

Never auto-query `READ_ONLY_BOUNDED_LEGACY` resources on login. Require explicit bounded period and enforce:

- `firstPaintEligible=false`
- `requiresExplicitPeriod=true`
- `maxPeriodDays`
- public state such as `NOT_CONFIGURED`, `STALE`, `EMPTY`, or `ERROR_PUBLIC`

## Anti-Patterns

- Do not expose `EChartsOption` as a dashboard API contract.
- Do not manually build `statsPath` in each Angular component.
- Do not make `empresa`, user, HADES transaction, schema, package, SQL, `ROWID`, or `FLAG_PACK` public filters.
- Do not let financial folha metrics render unless `viewAmounts` is authorized.
- Do not promote stale Cockpit tables to `OK` cards without `loads` confirming freshness.
