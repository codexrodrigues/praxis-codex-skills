---
name: praxis-charts-authoring-catalogs
description: Use when Codex must implement or audit governed @praxisui/charts authoring catalogs: resource discovery, stats capabilities and field eligibility, x-ui.analytics projections, availableResources/availableFields/availableTargets, operation-dependent cascades, Page Builder target resolution, transient editor context, catalog validation, preview samples, i18n, or AI/editor grounding parity.
---

# Praxis Charts Authoring Catalogs

Use this skill when a chart editor must answer which resources, stats operations, dimensions, metrics, aggregations, and interaction targets are genuinely authorable. Catalogs are governed projections of backend metadata and current composition. They are not arrays of convenient labels maintained by a dashboard page.

Pair it with:

- `praxis-charts-authoring-settings` for document/widget envelopes and Settings Panel round-trip.
- `praxis-charts-runtime-data` and `praxis-charts-analytics-interactions` for stats execution and runtime mapping.
- `praxis-metadata-schema-contracts` for `/schemas/catalog`, `/schemas/filtered`, schema identity, `x-ui`, ETag, and hash semantics.
- `praxis-metadata-discovery-capabilities` and `praxis-dashboard-analytics` for resource capabilities, `StatsFieldRegistry`, stats modes, and analytics projections.
- `praxis-core-resource-runtime` for Angular schema/capability discovery and `praxis-core-component-registry-contracts` for component/port targets.
- `praxis-fields-option-sources` when a catalog control needs remote search, dependencies, or selected-value rehydration.
- `praxis-page-builder-authoring` and `praxis-page-builder-composition` for widget/state/port target context.
- `praxis-charts-ai-handler-contracts` and `praxis-charts-ai-validation` when the same catalogs ground AI operations.

## Canonical Knowledge Graph

Do not invent one endpoint or DTO that duplicates all metadata. Materialize the catalog from complementary owners:

1. `/schemas/catalog` enumerates documentary/discovery candidates and canonical operation/schema references. It is not the field schema source of truth.
2. `/schemas/filtered` resolves operation-specific structure, property metadata, labels, types, `x-ui`, option sources, and schema identity.
3. `GET /{resource}/capabilities` proves collection availability and stats operations. Its `stats.fields[]` is the public projection of `StatsFieldRegistry` and owns field eligibility and allowed metrics.
4. `x-ui.analytics.projections[]`, when published, provides governed recommended intents, bindings, defaults, presentation families, and interactions. It does not override capability eligibility.
5. Current Page Builder/dynamic-page composition plus `ComponentMetadataRegistry`, ports, state paths, global actions, and governed route/surface catalogs owns interaction targets.
6. The Charts adapter maps those facts into editor view models. `PraxisXUiChartContract` persists selected canonical identities, not a metadata snapshot.

Absence has semantics. A schema catalog entry proves discovery, not current authorization. A stats endpoint in OpenAPI does not make every field eligible. A field in `/schemas/filtered` is not automatically a metric. A widget label is not a stable target id.

## Required Source Audit

Read `projects/praxis-charts/AGENTS.md` and inspect:

- `src/lib/config-editor/models/chart-config-editor-options.model.ts`
- `src/lib/config-editor/praxis-chart-config-editor.{ts,html,spec.ts}`
- `src/lib/config-editor/praxis-chart-widget-config-editor.{ts,spec.ts}`
- `src/lib/config-editor/services/chart-editor-preview-mapper.service.ts`
- `src/lib/services/chart-contract-validation.service.ts`
- `src/lib/praxis-chart.metadata.ts`
- `src/lib/ai/praxis-charts-authoring-manifest.ts`
- `src/lib/i18n/charts.*.ts`, README, examples, playgrounds, and the official Settings Panel smoke

For canonical producers/consumers, inspect as applicable:

- metadata-starter `StatsFieldCapability`, `StatsCapability`, `CapabilitySnapshot`, `StatsFieldRegistry`, `@UiAnalytics`, and schema/catalog controllers;
- core `ResourceCapabilitySnapshot`, `ResourceDiscoveryService`, `SchemaMetadataClient`, `AnalyticsSchemaContractService`, analytics models, and option-source models;
- Page Builder/core config-editor hosting, current widget definitions, `ComponentMetadataRegistry`, `PortContract`, `NestedPortCatalogService`, composition validation, global actions, and route/surface catalogs;
- the concrete host that currently constructs `availableResources`, `availableFields`, or `availableTargets`.

Repository search is required. A polished demo array is evidence of local duplication until its provenance is proven.

## Resource Discovery

- Enumerate candidate resource operations from canonical schema/discovery data; do not maintain a host switch or path list.
- Normalize resource identity separately from execution: stable `resourceKey`/operation identity for governance, canonical `resourcePath` for requests, and localized label for presentation.
- After selection, fetch collection capabilities and the relevant filtered request/response schema. Do not infer stats support by trial requests.
- Offer only operations whose canonical capability is true: `statsGroupBy`, `statsTimeSeries`, and/or `statsDistribution`.
- Preserve ETag/hash caching and stale-response protection. A slow response for resource A must not replace the catalog after the user selects resource B.
- Treat forbidden, unavailable, empty, stale, and network-error states distinctly. Never fall back to an arbitrary URL input for governed remote authoring.

## Stats Field Materialization

Backend `stats.fields[]` carries canonical facts such as:

- `field`: public identity accepted by stats payloads;
- `label`: fallback presentation label;
- `metrics`: allowed aggregate operations such as `COUNT`, `DISTINCT_COUNT`, `SUM`, `AVG`, `MIN`, `MAX`;
- `groupByEligible`, `timeSeriesEligible`, `distributionTermsEligible`, `distributionHistogramEligible`, and `metricFieldEligible`;
- `propertyPath`: backend implementation detail, not a value to persist in `x-ui.chart`.

Enrich these facts with `/schemas/filtered` property type/title/description/format and `x-ui`. Do not replace explicit capability facts with heuristics such as “number means metric” or “date means timeseries”.

Filter editor controls by the selected operation:

- `group-by`: dimension fields require `groupByEligible`; metric fields require `metricFieldEligible`; aggregation must occur in the field's `metrics`.
- `timeseries`: the time dimension requires `timeSeriesEligible`; metrics and aggregations remain capability-gated.
- `distribution/terms`: bucket dimension requires `distributionTermsEligible`.
- `distribution/histogram`: histogram field requires `distributionHistogramEligible`; metric semantics remain governed by the published request contract.
- `count`: model the backend's fieldless/field-specific count semantics explicitly; do not synthesize a fake `count` field unless the canonical capability publishes it.

Changing resource, operation, or distribution mode must recompute dependent candidates. Preserve a selected value only if it remains eligible; otherwise show a stale-selection diagnostic and block Apply/Save until the user resolves it. Do not silently remap by label or fuzzy text.

## Target Catalogs

Resolve targets after the structured event action is known:

- `filter-widget`: current page widgets/ports that accept compatible filter or query-context semantics;
- `update-context`: governed page state/context targets and compatible ports;
- `open-detail`: declared detail surfaces/panels/actions with compatible payload contracts;
- `navigate`: governed route/action catalog entries, never an arbitrary JavaScript or host string;
- `emit`: may require no target, but mappings still reference canonical source fields.

Use stable widget keys, state paths, action ids, surface ids, route ids, and port contracts. Labels may rank already-scoped candidates only after semantic scope is resolved; they never decide intent or compatibility. Revalidate target existence and mapping compatibility on reopen because page composition can change.

## Transient Editor Context

Classify every value passed to an editor:

- persisted component input: runtime behavior intentionally stored in `widget.definition.inputs`;
- transient authoring context: current schemas, capabilities, resource/field catalogs, page targets, diagnostics, and search state;
- canonical selection: resource/field/target identities persisted inside `chartDocument` or `queryContext`.

Do not persist transient catalog snapshots by spreading the editor's input object back into the widget. They become stale, inflate page documents, and create a second metadata source.

If `ComponentDocMeta.configEditor`/Settings Panel can pass only widget inputs and has no governed context resolver, classify that as a real host-contract gap. Add the smallest canonical transient-context hook in the shared owner; do not hide the problem with chart-specific globals, mutable registry metadata, or duplicated runtime inputs.

## Editor And Validation Rules

- Governed remote resources, dimensions, metrics, aggregations, and targets fail closed when their catalog is unavailable.
- Validation must receive or resolve catalog context. Rendering a dropdown does not prove that saved values are governed.
- Preserve canonical ids as values and use localized labels/descriptions only for UX.
- Large catalogs need canonical searchable option-source behavior, debounce/cancellation, no-result state, selected-value rehydration, and dependency filtering.
- Internal loading, denied, empty, stale, no-match, and validation copy belongs in Charts i18n (`pt-BR` and `en-US`). Backend business labels remain backend data.
- AI and visual authoring must consume the same candidate identities and eligibility rules. Manifest validator names are promises only when executable handlers/validators actually enforce them.
- Never route primary intent by keywords, labels, regexes, aliases, or fuzzy field names. Text matching may rank candidates only inside a semantically resolved resource/operation/target scope.

## Preview Boundary

The preview must use the same normalized `PraxisXUiChartContract` and runtime mapper as Apply/Save.

- Synthetic local rows may demonstrate layout without calling the backend, but must honor selected field identities, chart family, operation shape, and basic property types.
- Label the preview as synthetic/local; do not imply capability, authorization, query validity, or live data proof.
- A live preview, if introduced, must execute through canonical stats services with cancellation, loading/error states, capability checks, and no persistence of sample rows.
- Preview samples are derived evidence, not another field catalog or source of default business values.

## Inventory Before New Contract

- `ja-suportado-so-ux`: canonical metadata/capability exists; loading, search, diagnostics, labels, or preview presentation is weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: manual host arrays, field-type heuristics, free-form URL/target fallback, or persisted catalog snapshots duplicate governed facts.
- `suportado-parcialmente`: backend publishes facts but Angular models/adapters, cascades, validators, target projection, AI parity, or tests omit them.
- `lacuna-real-de-contrato`: no shared channel can carry required transient editor context, no governed target catalog exists for an action kind, or backend capability lacks a required eligibility fact.

Only `lacuna-real-de-contrato` justifies a public contract. Name the missing datum, owner, impacted consumers, derived artifacts, migration, and proof before editing. During beta, remove manual parallel catalogs in the same cycle as canonical materialization.

## Validation Matrix

Prove at least:

- happy path: enumerate a resource, load capabilities/schema, derive operation-specific fields/aggregations, select canonical ids, preview, save, reopen, and revalidate;
- cascade path: switch resource/operation/mode while requests race; stale selections and stale responses cannot survive silently;
- denied/empty path: no capabilities, no eligible fields, unavailable target, no-match search, and network failure remain distinct and fail closed;
- target path: action-specific widget/port/state/surface/route candidates and mapping compatibility update when composition changes;
- persistence path: `chartDocument/queryContext` persist, transient catalogs and diagnostics do not;
- adversarial path: reject manual URL, invented field/metric, unsupported aggregation, stale target, label-based identity, unsafe route, and raw ECharts option.

Typical focused gates are:

```bash
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' --include='projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts'
npx ng test praxis-core --watch=false --progress=false --include='projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts' --include='projects/praxis-core/src/lib/services/analytics-schema-contract.service.spec.ts' --include='projects/praxis-core/src/lib/composition/nested-port-catalog.service.spec.ts'
npx ng test praxis-core --watch=false --progress=false --include='projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts'
npm run build:praxis-charts
npx playwright test --config tools/e2e/playwright/praxis-charts-settings-panel.playwright.config.ts
```

When backend capability shape changes, add focused metadata-starter/quickstart HTTP proof and an Angular direct-consumer build. For visual selector changes, use desktop and narrow browser evidence with one successful search and one no-result search. Report which backend, Angular, Page Builder, AI registry, persistence, and browser surfaces were not exercised.
