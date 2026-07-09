# praxis-metadata-starter 8.0.0-rc.24 dashboard reference

Use this reference when designing or validating dashboard APIs against `praxis-metadata-starter` `8.0.0-rc.24`.

## Confirmed Source

Observed locally from:

```text
~/.m2/repository/io/github/codexrodrigues/praxis-metadata-starter/8.0.0-rc.24/praxis-metadata-starter-8.0.0-rc.24.jar
```

Inspection used `jar tf` and `javap`; no source jar was present in the inspected local repository.

## Controller Base

`AbstractReadOnlyResourceController<ResponseDTO, ID, FD>` extends `AbstractResourceQueryController<ResponseDTO, ID, FD>`.

Public methods observed on `AbstractResourceQueryController`:

```text
filter(FD, int, int, List<ID>, MultiValueMap<String,String>)
filterByCursor(FD, String, String, int, MultiValueMap<String,String>)
locate(FD, ID, int, MultiValueMap<String,String>)
groupByStats(GroupByStatsRequest<FD>)
timeSeriesStats(TimeSeriesStatsRequest<FD>)
distributionStats(DistributionStatsRequest<FD>)
exportCollection(CollectionExportRequest<FD>)
getAll()
getByIds(List<ID>)
filterOptions(FD, int, int, MultiValueMap<String,String>)
filterOptionSourceOptions(String, OptionSourceFilterRequest<FD>, String, List<String>, int, int, MultiValueMap<String,String>)
getOptionsByIds(List<ID>)
getOptionSourceOptionsByIds(String, List<String>)
getById(ID)
getItemSurfaces(ID)
getItemActions(ID)
getCollectionActions()
getCollectionCapabilities()
getItemCapabilities(ID)
getSchema()
```

Path constants observed in bytecode include:

```text
/filter
/filter/cursor
/stats/group-by
/stats/timeseries
/stats/distribution
/all
/{id}
/schemas
/schemas/filtered
```

`ApiDocsController` recognizes/normalizes endpoint families including:

```text
/options/filter
/options/by-ids
/option-sources/
/locate
/batch
```

Always verify exact final paths via OpenAPI or HTTP smoke in the target host.

## Stats

Core classes:

```text
StatsFieldRegistry
StatsFieldDescriptor
StatsMetric
StatsSupportMode
GroupByStatsRequest
TimeSeriesStatsRequest
DistributionStatsRequest
GroupByStatsResponse
TimeSeriesStatsResponse
DistributionStatsResponse
```

`StatsMetric` values:

```text
COUNT
DISTINCT_COUNT
SUM
AVG
MIN
MAX
```

`TimeSeriesGranularity` values:

```text
DAY
WEEK
MONTH
```

`StatsSupportMode` values:

```text
AUTO
DISABLED
```

Useful `StatsFieldDescriptor` factories:

```text
groupByBucket(field, propertyPath, metrics)
timeSeriesField(field, propertyPath)
metricField(field, propertyPath, metrics)
histogramField(field, propertyPath, metrics)
distributionTermsBucket(field, propertyPath, metrics)
categoricalGroupByBucket(field, propertyPath)
categoricalTermsBucket(field, propertyPath)
temporalTimeSeriesField(field, propertyPath)
numericMeasureField(field, propertyPath)
numericHistogramMeasureField(field, propertyPath)
distinctCountField(field, propertyPath)
```

## Analytics Annotations

Observed:

```text
@UiAnalytics
@AnalyticsProjection
@AnalyticsMetricBinding
@AnalyticsDimensionBinding
AnalyticsOperation
AnalyticsIntent
AnalyticsGranularity
```

`AnalyticsOperation`:

```text
GROUP_BY
TIMESERIES
DISTRIBUTION
```

`AnalyticsIntent`:

```text
RANKING
TREND
DISTRIBUTION
COMPOSITION
COMPARISON
CORRELATION
```

`AnalyticsGranularity`:

```text
UNSPECIFIED
DAY
WEEK
MONTH
```

## Option Sources

Observed:

```text
OptionSourceRegistry
OptionSourceDescriptor
OptionSourcePolicy
OptionSourceType
OptionSourceFilterRequest
OptionSourceProvider
CompositeOptionSourceQueryExecutor
```

`OptionSourceType`:

```text
RESOURCE_ENTITY
DISTINCT_DIMENSION
CATEGORICAL_BUCKET
LIGHT_LOOKUP
STATIC_CANONICAL
```

## Field Controls

`FieldControlType` in `8.0.0-rc.24` exposes `DATE_RANGE` for date interval controls; do not use the unverified alias `DATE_RANGE_PICKER`.

## Capabilities Actions Surfaces

Observed:

```text
CapabilityService
CapabilitySnapshot
ActionCatalogService
SurfaceCatalogService
@WorkflowAction
@UiSurface
@ResourceIntent
```

Use these for metadata-driven discovery and user-specific availability. Keep security decisions server-side.

## Export

Observed:

```text
CollectionExportRequest
CollectionExportCapability
CollectionExportFormat
CollectionExportScope
CollectionExportResult
```

`CollectionExportFormat`:

```text
CSV
JSON
EXCEL
PDF
PRINT
```

`CollectionExportScope`:

```text
AUTO
SELECTED
FILTERED
CURRENT_PAGE
ALL
```

Confirm the effective export route with OpenAPI/HTTP smoke before documenting it as runtime-confirmed.
