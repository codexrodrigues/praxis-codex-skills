# Quickstart dashboard analytics patterns

Use this reference when designing dashboard resources by analogy with `D:\Developer\praxis-plataform\praxis-api-quickstart`.

## Source Files Studied

Reference host instructions:

- `AGENTS.md`

Reusable base:

- `src/main/java/com/example/praxis/apiquickstart/core/controller/base/AbstractQuickstartReadOnlyController.java`
- `src/main/java/com/example/praxis/apiquickstart/core/service/base/AbstractQuickstartReadOnlyService.java`

Payroll analytics pilot:

- `src/main/java/com/example/praxis/apiquickstart/hr/controller/VwAnalyticsFolhaPagamentoController.java`
- `src/main/java/com/example/praxis/apiquickstart/hr/service/VwAnalyticsFolhaPagamentoService.java`
- `src/main/java/com/example/praxis/apiquickstart/hr/dto/VwAnalyticsFolhaPagamentoDTO.java`
- `src/main/java/com/example/praxis/apiquickstart/hr/dto/filter/VwAnalyticsFolhaPagamentoFilterDTO.java`
- `src/main/java/com/example/praxis/apiquickstart/hr/entity/VwAnalyticsFolhaPagamento.java`
- `docs/PAYROLL-ANALYTICS-DASHBOARDS.md`

Tests:

- `src/test/java/com/example/praxis/apiquickstart/hr/service/VwAnalyticsFolhaPagamentoServiceStatsTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/StatsSchemaSmokeHttpTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/VwStatsSmokeHttpTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/OpenApiGroupResolutionIsolatedIntegrationTest.java`

## Host Boundary

Quickstart rule: audit what the starter and reference host already publish before creating a new contract. Classify as:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only a real contract gap justifies a new public endpoint. For dashboards, this usually means using existing Praxis resource/stats/metadata surfaces first.

## Read-Only Analytics Resource Pattern

The payroll pilot uses an immutable view entity:

```java
@Entity
@Immutable
@Table(name = "vw_analytics_folha_pagamento", schema = "public")
public class VwAnalyticsFolhaPagamento { ... }
```

The controller is a read-only resource with `@ApiResource` and `@ApiGroup`:

```java
@ApiResource(
    value = ApiPaths.HumanResources.VW_ANALYTICS_FOLHA_PAGAMENTO,
    resourceKey = "human-resources.vw-analytics-folha-pagamento"
)
@ApiGroup("human-resources")
@RestController
public class VwAnalyticsFolhaPagamentoController
        extends AbstractQuickstartReadOnlyController<...> {
}
```

Use this pattern for aggregate/dashboard datasets that are projections, views, materialized views, or read-only tables.

## Operation Documentation

`AbstractQuickstartReadOnlyController` overrides `/stats/group-by`, `/stats/timeseries`, and `/stats/distribution` to add canonical `@Operation` examples and response examples.

Concrete controllers override stats methods again when they need:

- domain-specific `@Operation` summary/description;
- `@UiAnalytics` projections;
- resource-specific examples;
- semantic chart discovery.

Do not duplicate this if the target host uses the starter base directly and does not need richer OpenAPI. If the UI depends on `operationExamples` or `x-ui.analytics`, add focused overrides.

## Stats Registry Pattern

The payroll service defines a static registry and enables only supported operations:

```java
private static final StatsFieldRegistry STATS_FIELDS = StatsFieldRegistry.builder()
        .groupByBucket("departamento", "departamento", Set.of(StatsMetric.COUNT))
        .groupByBucket("payrollProfile", "payrollProfile", Set.of(StatsMetric.COUNT))
        .temporalTimeSeriesField("competencia", "competencia")
        .numericHistogramMeasureField("salarioLiquido", "salarioLiquido")
        .numericHistogramMeasureField("pctDesconto", "pctDesconto")
        .build();

@Override
public StatsSupportMode getGroupByStatsSupportMode() {
    return StatsSupportMode.AUTO;
}

@Override
public StatsSupportMode getTimeSeriesStatsSupportMode() {
    return StatsSupportMode.AUTO;
}

@Override
public StatsSupportMode getDistributionStatsSupportMode() {
    return StatsSupportMode.AUTO;
}
```

Service tests assert eligibility:

- dimensions are group-by or terms eligible;
- temporal fields are time-series eligible;
- numeric measures are metric and histogram eligible;
- monetary fields support `SUM`;
- percentage fields support `AVG`.

## Multi-Metric Stats

Quickstart proves both single `metric` and plural `metrics`.

Single metric:

```json
{
  "filter": {},
  "field": "competencia",
  "granularity": "MONTH",
  "metric": { "operation": "SUM", "field": "salarioLiquido" },
  "fillGaps": false
}
```

Multi-metric:

```json
{
  "filter": {},
  "field": "competencia",
  "granularity": "MONTH",
  "metrics": [
    { "operation": "SUM", "field": "salarioLiquido", "alias": "massaLiquida" },
    { "operation": "AVG", "field": "pctDesconto", "alias": "mediaPctDesconto" }
  ],
  "fillGaps": false
}
```

Tests expect:

- `data.metrics.length() == 2`
- `data.points[0].values.massaLiquida`
- `data.points[0].values.mediaPctDesconto`

Use this for combo charts, e.g. bars for value and line for percentage.

## Analytics Projections

Concrete stats operations can publish `@UiAnalytics`:

- group-by payroll ranking table;
- group-by payroll ranking chart;
- group-by profile composition chart;
- timeseries payroll trend chart.

Tests validate `x-ui.analytics.projections` in `/schemas/filtered` response schemas, including:

- projection ids;
- bindings/primary metrics;
- defaults/sort;
- default granularity;
- presentation families.

Use projections when the official UI should discover chart intent. Do not add projections for untested or unsupported stats operations.

## Option Sources For Analytics Filters

The payroll pilot uses option sources derived from the view:

- `universo`: `DISTINCT_DIMENSION`
- `payrollProfile`: `DISTINCT_DIMENSION`
- `composicaoFolha`: `DISTINCT_DIMENSION`
- salary/percentage ranges: `CATEGORICAL_BUCKET`

It also uses governed entity lookups from other resources, such as `baseId` through a `RESOURCE_ENTITY` option source.

Important descriptor patterns:

- `dependsOn` narrows options by current filter context.
- `dependencyFilterMap` maps UI/filter field names when the source field differs, e.g. `universo -> universoContexto`.
- `OptionSourcePolicy(... allowSearch=true, allowIncludeIds=true ...)` supports Angular-like search plus selected-value rehydration.

Tests validate:

- schema publishes `x-ui.optionSource.key` and `type`;
- dependency metadata appears in schema;
- endpoint path points to `/option-sources/{sourceKey}/options/filter`;
- filter endpoint returns `id` and `label`;
- `includeIds` can merge selected values into the result;
- `/by-ids` preserves input order.

## Schema And Catalog Smokes

Stats schema tests cover:

- `/schemas/filtered?path=<stats-path>&operation=post&schemaType=request`
- `/schemas/filtered?path=<stats-path>&operation=post&schemaType=response`
- request fields such as `filter`, `field`, `metric`, `metrics`, `granularity`;
- response fields such as `field`, `buckets`, `points`, `metrics`;
- `x-ui.operationExamples.request`;
- `x-ui.operationExamples.response`;
- `/schemas/catalog?path=<stats-path>&operation=post`;
- catalog group resolution and schema links.

Use these checks when claiming stats metadata is ready for a metadata-driven dashboard UI.

## Quickstart Validation Commands

For quickstart metadata integration changes, AGENTS recommends:

```powershell
mvn "-Dtest=OpenApiGroupResolutionIsolatedIntegrationTest,QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest" test
```

For focused stats work, useful suites observed in the reference host:

```powershell
mvn "-Dtest=VwAnalyticsFolhaPagamentoServiceStatsTest" test
mvn "-Dtest=StatsSchemaSmokeHttpTest,VwStatsSmokeHttpTest" test
```

Some HTTP smoke classes are guarded by `PRAXIS_EXTERNAL_SMOKE_TESTS=true`; do not report them as executed unless the environment variable and runtime conditions were actually satisfied.
