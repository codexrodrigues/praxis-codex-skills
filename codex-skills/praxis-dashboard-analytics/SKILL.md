---
name: praxis-dashboard-analytics
description: Design and implement dashboard, chart, KPI, cockpit, and analytics APIs on Java/Spring hosts that use praxis-metadata-starter. Use when Codex must decide between Praxis read-only aggregate resources and custom dashboard endpoints, model /stats/group-by, /stats/timeseries, /stats/distribution, StatsFieldRegistry, @UiAnalytics, dashboard filter DTOs, option sources for chart dimensions, capabilities, export, or metadata-driven Angular/Praxis dashboard contracts.
---

# Praxis Dashboard Analytics

## Overview

Use this skill to design dashboard APIs that stay native to `praxis-metadata-starter` instead of inventing ad hoc chart endpoints. Pair it with:

- `praxis-java-host-project` for host/resource implementation.
- `praxis-dto-annotations` for DTO, filter, `@Schema`, `@UISchema`, `@Filterable`, and governance metadata.
- `praxis-resource-entity-lookup-backend` when chart filters use `OptionSourceRegistry`, `RESOURCE_ENTITY`, `LIGHT_LOOKUP`, or `DISTINCT_DIMENSION`.
- `praxis-ui-product-design` when dashboard visual quality or UX is in scope.

Before changing this skill or implementing a dashboard, inspect the resolved starter/source for
`StatsFieldRegistry`, `StatsFieldDescriptor`, `StatsSupportMode`, stats request/response DTOs,
`@UiAnalytics`, `UiAnalyticsOpenApiCustomizer`, option-source descriptors, capabilities, export,
`/schemas/filtered`, `/schemas/catalog`, and a representative reference-host analytics resource
when available. The goal is to model what Praxis already publishes before adding custom dashboard
contracts.

## Classification

Classify work before editing:

- `contrato-publico`: adding/changing resource paths, dashboard paths, DTO fields, `StatsFieldRegistry`, `@UiAnalytics`, `/schemas/filtered`, option sources, capabilities, actions, surfaces, or export.
- `arquitetural`: deciding dashboard/resource boundaries, aggregate storage, query strategy, or starter extension.
- `docs-apenas`: planning or investigation only.
- `local-pequena`: private service/repository implementation with no public schema change.

For `contrato-publico` or `arquitetural`, map impacted consumers, OpenAPI, schemas, Angular runtime, security, test evidence, and breaking-change risk before patching.

## Decision Rule

Prefer a Praxis read-only aggregate resource when the dashboard panel can be represented as one analytic dataset with fields, filters, dimensions, and metrics.

Use a custom dashboard endpoint only when the response composes several resources, expresses product layout, returns cross-resource KPIs, reports load status, or generates a composed executive artifact.

First inventory whether the need is already supported by resource `/filter`, `/stats/*`,
`StatsFieldRegistry`, `@UiAnalytics`, option sources, capabilities, collection export, surfaces, or
catalog/domain metadata. Classify the gap as already supported but missing in UX, supported but
poorly materialized, partial support, or a real contract gap. Only a real contract gap justifies a
new public dashboard endpoint or starter contract.

Default split:

| Need | Use |
| --- | --- |
| Chart drill-down over one aggregate dataset | `@ApiResource` + `AbstractReadOnlyResourceController` |
| Ranking, composition, distribution, trend | resource `/stats/*` |
| Filtered table behind a chart | resource `/filter` |
| Chart filter options | resource option sources |
| Dashboard first fold with multiple cards | custom `/api/dashboard/summary` |
| UI catalog/layout for home cockpit | custom `/api/dashboard/catalog` |
| Cross-resource permissions | custom `/api/dashboard/capabilities` plus resource capabilities |
| Load freshness/status | custom `/api/dashboard/loads` |
| Tabular export of one dataset | resource export |
| Composed PDF with several panels | custom dashboard export |

## Resource Pattern

Create aggregate read-only resources with stable paths and keys:

```java
@ApiResource(
        value = ApiPaths.Dashboard.VINCULOS_AGREGADOS,
        resourceKey = "dashboard.vinculos-agregados"
)
@ApiGroup("dashboard")
public class VinculoAgregadoController extends AbstractReadOnlyResourceController<
        VinculoAgregadoDTO,
        String,
        VinculoAgregadoFilterDTO> {
}
```

Do not add `@RestController` by reflex when the resolved starter's `@ApiResource` already supplies
the controller/request-mapping semantics. Keep extra stereotypes only when the target host version
or local base pattern explicitly requires them.

Expected resource operations:

```text
POST /<resource>/filter
POST /<resource>/filter/cursor
POST /<resource>/stats/group-by
POST /<resource>/stats/timeseries
POST /<resource>/stats/distribution
POST /<resource>/options/filter
GET  /<resource>/options/by-ids
POST /<resource>/option-sources/{sourceKey}/options/filter
GET  /<resource>/option-sources/{sourceKey}/options/by-ids
GET  /<resource>/capabilities
GET  /schemas/filtered?path=<path>&operation=<operation>&schemaType=<request|response>
```

Confirm exact paths by OpenAPI/runtime smoke for the target starter version before reporting them as verified.

For runtime `/filter` smoke on `AbstractReadOnlyResourceController` resources, send the `FilterDTO` itself as the JSON body and put paging/sort in the query string, for example:

```text
POST /api/dashboard/vinculos-agregados/filter?page=0&size=10
```

Do not wrap the filter body as `{ "filter": ..., "page": ..., "size": ... }`; that wrapper shape is for stats request DTOs and will fail on standard `/filter` endpoints.

When the host has a local base controller like the quickstart, use it to keep repeated `@Operation` examples for `/stats/*` in one place. Override concrete stats methods only when the resource needs `@UiAnalytics`, domain-specific summaries, or operation examples.

## Stats Modeling

Override stats support deliberately:

```java
@Override
public StatsSupportMode getGroupByStatsSupportMode() {
    return StatsSupportMode.AUTO;
}

@Override
public StatsSupportMode getTimeSeriesStatsSupportMode() {
    return StatsSupportMode.AUTO;
}

@Override
public StatsFieldRegistry getStatsFieldRegistry() {
    return StatsFieldRegistry.builder()
            .temporalTimeSeriesField("competencia", "competencia")
            .categoricalGroupByBucket("situacao", "situacao")
            .categoricalGroupByBucket("setor", "setor")
            .numericMeasureField("quantidade", "quantidade")
            .numericMeasureField("valor", "valor")
            .build();
}
```

Only register fields that are valid for the operation:

- dimensions: status, category, organization unit, month, rubrica group, frequency type.
- measures: amount, count, days, hours, percentage, average, min/max when meaningful.
- never register technical IDs, document numbers, codes, `ROWID`, legacy locator fields, phone numbers, postal codes, or fiscal IDs as numeric measures.
- treat legacy numeric codes as text/categorical dimensions unless users do arithmetic with them.

Use native requests:

```json
{
  "filter": {},
  "field": "situacao",
  "metric": {
    "operation": "SUM",
    "field": "quantidade",
    "alias": "total"
  },
  "limit": 10,
  "orderBy": "DESC"
}
```

For trends, use `/stats/timeseries` with a temporal field and `DAY`, `WEEK`, or `MONTH` granularity.

Support both single-metric and multi-metric requests when the frontend needs combo charts:

```json
{
  "filter": {},
  "field": "competencia",
  "granularity": "MONTH",
  "metrics": [
    { "operation": "SUM", "field": "valorLiquido", "alias": "massaLiquida" },
    { "operation": "AVG", "field": "percentualDesconto", "alias": "mediaDesconto" }
  ],
  "fillGaps": false
}
```

Validate aliases and multi-metric response shape; clients may use `points[].values.<alias>` for combo charts.

## Analytics Metadata

Use `@UiAnalytics` and `@AnalyticsProjection` when the UI should discover chart intent instead of hardcoding it.

Model:

- `GROUP_BY` for ranking/composition by dimension.
- `TIMESERIES` for trend lines and monthly evolution.
- `DISTRIBUTION` for histograms/terms distributions.
- `RANKING`, `TREND`, `COMPOSITION`, `COMPARISON`, or `DISTRIBUTION` as chart intent.

Keep `@UiAnalytics` honest: declare projections only for operations backed by real stats support and tests.

`@UiAnalytics` publishes `x-ui.analytics.projections` on real OpenAPI operations. It is not a
dashboard manifest, not a second schema source, and not a place to invent metrics, SQL, filters, or
layout unavailable from the stats operation. Bind projection fields only to `StatsFieldRegistry`
fields and DTO semantics that are executable by the resource.

For chart-discoverable resources, assert that `/schemas/filtered` response schemas publish `x-ui.analytics.projections` with ids, bindings, defaults, presentation families, sort, drill-down, and granularity where applicable.

In `praxis-metadata-starter` `8.0.0-rc.24`, the first runtime resolution of grouped OpenAPI for `/schemas/filtered` response schemas can be slow while the group document is initialized and cached. Use a smoke timeout of at least 60 seconds for the first analytics schema pass, then rely on cached calls for faster repeat checks.

## Filters And Option Sources

Create a `FilterDTO` for dashboard filters instead of accepting raw maps.

Required rules:

- Use `@Filterable` for executable filters.
- Use `@UISchema` for labels, controls, ranges, option endpoints, and presentation.
- Use Bean Validation for date ranges, required bounds, and list sizes.
- Use option sources for chart dimensions and multiselects.
- Use `DISTINCT_DIMENSION` for dimensions derived from the aggregate dataset.
- Use `CATEGORICAL_BUCKET` for precomputed ranges or buckets such as salary ranges, percentage bands, age bands, SLA buckets, or absence ranges.
- Use `LIGHT_LOOKUP` for small/catalog lookup sources.
- Use `RESOURCE_ENTITY` only for real governed entities with `by-ids`, rich display, selection policy, and optional detail navigation.
- Use `dependsOn` and `dependencyFilterMap` when option values must cascade from other dashboard filters; test that the published schema contains the dependency metadata and that the runtime endpoint applies it.

Do not publish provider details, SQL, table names, internal package/procedure names, tenant context, or private bind parameters through `x-ui`, `@UISchema.extraProperties`, option source metadata, or `OptionDTO.extra`.

For AI-authored dashboards, do not route dashboard intent by keywords such as "ranking", "trend",
or "pie" inside the host. Expose semantic resources, stats capabilities, analytics projections,
catalog/domain metadata, and option-source contracts so the governed authoring flow can resolve the
intent semantically and then ground it against executable stats operations.

## Custom Dashboard Endpoints

Keep custom endpoints thin and compositional:

```text
GET  /api/dashboard/catalog
GET  /api/dashboard/capabilities
POST /api/dashboard/summary
GET  /api/dashboard/loads
POST /api/dashboard/exports/pdf
```

Guidelines:

- `catalog` returns dashboard layout, panel definitions, resource links, operation names, labels, refresh policy, and feature flags.
- `capabilities` consolidates user permissions across resources and product panels.
- `summary` returns cross-resource KPI cards for the first viewport.
- `loads` returns aggregate freshness/status without stack traces or SQL.
- composed PDF/export may remain custom when it crosses multiple resources.

Do not duplicate `/stats/*` or `/filter` behavior in custom dashboard endpoints unless a real product response shape requires it.

Custom dashboard endpoints may materialize product composition, first-viewport summaries, load
freshness, or cross-resource capabilities, but they must link back to canonical resource paths,
operation names, schema links, capabilities, and option sources. They should not hide unsupported
stats or turn SQL/provider internals into public dashboard contract.

## Legacy-Backed Hosts

For legacy-backed hosts:

- Resolve user, organization, permissions, tenant, and database context server-side.
- Do not accept company/user/profile/permission context in dashboard filter bodies unless the host has an explicit trusted admin use case.
- Do not query high-volume transactional legacy tables during login or dashboard first load.
- Use aggregate tables, views, materializations, or validated cockpit sources.
- Mark every indicator with source, refresh/version, period key, scope, and parity evidence.
- Keep details behind migrated resources or legacy drill-down links until individual-detail permission is proven.

## Validation

Minimum validation for a dashboard resource:

- compile/test proof for DTO/controller/service changes;
- OpenAPI path exists;
- `/schemas/filtered` for request and response, including operation examples for stats operations when the host publishes them;
- `/schemas/catalog` has resolvable schema links for stats operations when the host exposes the catalog;
- `x-ui.analytics.projections` appears for every operation annotated with `@UiAnalytics`;
- `/filter` smoke with representative filters;
- `/stats/group-by`, `/stats/timeseries`, and `/stats/distribution` smoke for every enabled stats support mode;
- multi-metric stats smoke when combo charts or multiple measures are advertised;
- option-source filter and by-ids smoke for each chart lookup;
- option-source search, `includeIds`, dependency filter, and by-ids order preservation when those policies are enabled;
- capability behavior for allowed and denied users;
- no leaked private fields in schema, response, option metadata, or errors;
- aggregate parity check against the legacy/source dataset for at least one period.

Schema smokes can run against an isolated H2/test datasource when they only assert OpenAPI,
`/schemas/filtered`, catalog links, `x-ui.analytics`, and option-source metadata. Content smokes
that expect non-empty buckets, points, or option lists require seeded fixture data or the approved
published/local reference database; do not treat an empty H2 dataset failure as proof that the
dashboard contract is broken without checking data setup.

When validation is partial, report exactly which endpoints were executed and which remain planned.

## Iteration During Implementation

Update this skill during real endpoint implementation when you discover a reusable rule, failure mode, validation checklist item, or starter-version behavior that will matter for future dashboard work.

Do update the skill for:

- confirmed starter behavior from OpenAPI, tests, `javap`, source, or runtime smoke;
- a better boundary rule between aggregate resource and custom dashboard endpoint;
- a recurring security or metadata leakage issue;
- a reliable `StatsFieldRegistry`, `@UiAnalytics`, option-source, or capability pattern;
- a validation command or smoke pattern worth repeating.

Do not update the skill for:

- one-off consumer or domain business decisions that belong in host-specific docs;
- endpoint names that are still speculative;
- unverified assumptions about starter behavior;
- implementation details that only make sense in one service class.

When updating, keep `SKILL.md` concise and move version-specific observations to `references/`.

## Reference

Read `references/praxis-metadata-starter-8-rc24.md` when you need confirmed classes, methods, or endpoint families observed in `praxis-metadata-starter` `8.0.0-rc.24`.

Read `references/quickstart-dashboard-patterns.md` when you need concrete reference-host patterns from `praxis-api-quickstart`, especially payroll analytics, `@UiAnalytics`, multi-metric stats, option-source dependencies, and smoke test shapes.

Treat references as versioned evidence, not the current source of truth. When local starter or
quickstart source is available, prefer the current source/tests over older reference notes.
