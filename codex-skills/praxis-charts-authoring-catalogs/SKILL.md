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
- `src/lib/config-editor/services/praxis-chart-config-editor-context-resolver.service.{ts,spec.ts}`
- `src/lib/config-editor/services/chart-resource-capability-catalog.adapter.{ts,spec.ts}`
- `src/lib/config-editor/services/chart-composition-target-catalog.adapter.{ts,spec.ts}`
- `src/lib/config-editor/services/chart-editor-preview-mapper.service.ts`
- `src/lib/services/chart-contract-validation.service.ts`
- `src/lib/praxis-chart.metadata.{ts,spec.ts}` and `src/lib/providers/charts.providers.spec.ts`
- `src/lib/ai/praxis-charts-authoring-manifest.ts`
- `src/lib/i18n/charts.*.ts`, README, examples, playgrounds, and the official Settings Panel smoke

For canonical producers/consumers, inspect as applicable:

- metadata-starter `StatsFieldCapability`, `StatsCapability`, `CapabilitySnapshot`, `StatsFieldRegistry`, `@UiAnalytics`, and schema/catalog controllers;
- core `ResourceCapabilitySnapshot`, `ResourceDiscoveryService`, `SchemaMetadataClient`, `AnalyticsSchemaContractService`, analytics models, and option-source models;
- Page Builder/core config-editor hosting, current widget definitions, `ComponentMetadataRegistry`, `PortContract`, `NestedPortCatalogService`, composition validation, global actions, and route/surface catalogs;
- the concrete host that currently constructs `availableResources`, `availableFields`, or `availableTargets`.

Repository search is required. A polished demo array is evidence of local duplication until its provenance is proven.

## Resource Discovery

- Enumerate candidate resources from `/schemas/catalog`; group endpoints by canonical `resourceKey` and require unambiguous catalog evidence for the collection capabilities href and published stats operations. Do not maintain a host switch or path list.
- Normalize resource identity separately from execution: stable `resourceKey`/operation identity for governance, canonical `resourcePath` for requests, and localized label for presentation.
- Keep discovery lazy: load the catalog to enumerate candidates, then fetch collection capabilities only for the selected resource through the exact capabilities href published by that catalog projection. Do not rebuild the href from a resource label/key or infer stats support by trial requests.
- Accept a selected `resourceKey` as semantic identity when reopening, but normalize the persisted `chartDocument.source.resource` to the selected candidate's canonical operational path before runtime execution. Never concatenate a `resourceKey` as though it were an HTTP path.
- Offer only operations whose canonical capability is true: `statsGroupBy`, `statsTimeSeries`, `statsDistribution`, and/or `statsComparison`. Map these exact operation identities to `group-by`, `timeseries`, `distribution`, and `comparison`; do not accept aliases or infer support from field names.
- Require strict root-relative operational paths and exact catalog/capability parity. Reject absolute, protocol-relative, or relative paths, and fail closed when the capability href resolves to a different resource path than the catalog entry. Normalizing a trailing slash is acceptable; synthesizing a leading slash or rebuilding identity from a label/key is not.
- Deduplicate only concurrent in-flight catalog/capability reads. Bound each read with the current 10-second timeout, evict the request on completion or failure, allow a later resolution to retry, and reject stale async results when the selection changes. Do not retain settled permission-sensitive discovery projections until the canonical backend/client contract publishes an explicit authorization-context epoch or equivalent tenant/principal/profile cache scope. Do not pretend `/schemas/catalog` or capabilities inherit `/schemas/filtered` ETag/hash semantics.
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
- `distribution/histogram`: histogram field requires `distributionHistogramEligible`; histogram uses the backend's fieldless `COUNT` metric and requires the governed bucket-size contract.
- `comparison`: bucket dimension requires governed grouping eligibility, the period field requires `timeSeriesEligible`, metric fields remain capability-gated, and only `COUNT`, `DISTINCT_COUNT`, and `SUM` are accepted by the canonical comparison endpoint.
- `count`: expose the derived editor option only when the selected resource capability publishes `COUNT`; keep its runtime request fieldless rather than treating `count` as a physical property or permitting field-specific `COUNT` on arbitrary metrics.

Materialize `distributionModes` per option instead of treating every distribution field as valid for both modes. Terms dimensions come only from `distributionTermsEligible`, histogram dimensions only from `distributionHistogramEligible`, regular metric fields remain terms-scoped, and the capability-backed fieldless count option can serve the modes supported by the selected resource. Switching to terms must remove histogram-only bucket settings; switching modes must invalidate fields that no longer match.

Changing resource, operation, or distribution mode must recompute dependent candidates. Preserve a selected value only if it remains eligible; otherwise show a stale-selection diagnostic and block Apply/Save until the user resolves it. Do not silently remap by label or fuzzy text.

## Comparison Authoring Boundary

Treat `comparison` as one governed analytics operation, not as a chart convenience assembled from independent requests:

- expose it only when the selected resource publishes `canonicalOperations.statsComparison === true`;
- persist one complete `source.options.comparisonPeriod` with canonical `field`, explicit `timezone`, backend-supported `preset`, and `PREVIOUS_ALIGNED` or `PREVIOUS_CALENDAR_PERIOD` mode;
- require at least one bucket dimension and one or more unique metric field identities; constrain comparison aggregations to `count`, `distinct-count`, and `sum`;
- materialize exactly one `POST /{resource}/stats/comparison` request with mandatory `metrics[]`; never emit the singular `metric` shape and never downgrade to multiple `group-by` calls;
- leave preset resolution, calendar arithmetic, bucket union, baseline detection, delta, and delta-percent calculation to the canonical backend response;
- project each response metric alias to current/previous runtime series using the shared comparison response adapter. These projection fields are derived runtime identities, not values to persist as business configuration;
- preserve `bucket.key` as filter/event identity and use `bucket.label` only for presentation. A visible label must never become the cross-filter value;
- keep visual editor controls, normalizer, validator, canonical mapper, preview sample, AI manifest, i18n, examples, and registry acceptance on the same operation vocabulary.

Fail closed when the resource operation, period field, bucket field, metric field, aggregation, alias uniqueness, or comparison period is not proven. A backend 403/501 or incompatible response is an explicit runtime state, not permission to retry through a different stats operation.

## Target Catalogs

Resolve targets after the structured event action is known:

- `filter-widget`: current page widgets/ports that accept compatible filter or query-context semantics;
- `update-context`: governed page state/context targets and compatible ports;
- `open-detail`: declared detail surfaces/panels/actions with compatible payload contracts;
- `navigate`: governed route/action catalog entries, never an arbitrary JavaScript or host string;
- `emit`: may require no target, but mappings still reference canonical source fields.

Use stable widget keys, state paths, action ids, surface ids, route ids, and port contracts. Labels may rank already-scoped candidates only after semantic scope is resolved; they never decide intent or compatibility. Revalidate target existence and mapping compatibility on reopen because page composition can change.

In the current Page Builder projection, `ChartCompositionTargetCatalogAdapter` intentionally admits only existing, nondeprecated top-level links whose source is the current chart and whose exact output port maps to the edited event. A configured point-click action is proven by the structured `pointAction` output; the raw observational `pointClick` output does not authorize that action. A widget target must terminate in a public, nondeprecated `query-context` input; a state target must be in the `values` layer, explicitly writable, declared in page state schema, and carried by a `state-write` link. Merge duplicate target identities only by accumulating the exact governed source events in `availableTargets[].events`. A target proved for `crossFilter` must not become authorable for `pointClick`.

Nested targets, self-links, undeclared state paths, routes, surfaces, panels, and global actions are not silently inferred. Until their owning composition contracts publish compatible evidence, keep them out of the catalog and emit diagnostics rather than widening the target model locally.

Treat a chart interaction target as governed compatibility evidence, not as proof that the target workflow, permission, backend side effect, or business policy exists. `pointClick`, `drillDown`, `crossFilter`, and `selection` may persist canonical action, target, and field mapping, but execution must still be grounded in the target widget/port/surface/global-action contract; when that grounding is absent, fail closed with catalog diagnostics or open the owning composition/platform follow-up instead of encoding host-local event behavior in `x-ui.chart`.

## Transient Editor Context

Classify every value passed to an editor:

- persisted component input: runtime behavior intentionally stored in `widget.definition.inputs`;
- transient authoring context: current schemas, capabilities, resource/field catalogs, page targets, diagnostics, and search state;
- canonical selection: resource/field/target identities persisted inside `chartDocument` or `queryContext`.

Do not persist transient catalog snapshots by spreading the editor's input object back into the widget. They become stale, inflate page documents, and create a second metadata source.

Use `ComponentDocMeta.configEditor.contextResolver` as the canonical shared transient-context hook. Charts installs the DI-backed resolver through its metadata provider, while the Page Builder supplies the current page, widget identity, metadata, and persisted inputs. The resolver returns `availableResources`, `availableFields`, `availableTargets`, and diagnostics for the editor invocation; the static metadata declaration must remain serializable and must not capture a mutable global.

If another host can pass only widget inputs and cannot invoke the shared resolver, classify that as a host-integration gap. Do not hide it with chart-specific globals, mutable registry metadata, or duplicated runtime inputs. Apply/Save must write only the normalized chart contract/query context; catalogs, diagnostics, loading/cache state, capabilities, and composition evidence are transient and must never be spread into `widget.definition.inputs`.

## Editor And Validation Rules

- Governed remote resources, dimensions, metrics, aggregations, and targets fail closed when their catalog is unavailable.
- Validation must receive or resolve catalog context. Rendering a dropdown does not prove that saved values are governed.
- Preserve canonical ids as values and use localized labels/descriptions only for UX.
- Large catalogs need canonical searchable option-source behavior, debounce/cancellation, no-result state, selected-value rehydration, and dependency filtering.
- Internal loading, denied, empty, stale, no-match, and validation copy belongs in Charts i18n (`pt-BR` and `en-US`). Backend business labels remain backend data.
- AI and visual authoring must consume the same candidate identities and eligibility rules. Manifest validator names are promises only when executable handlers/validators actually enforce them.
- Backend AI parity is a release gate, not documentation parity. Before declaring governed chart authoring complete, prove that `chart-event-point-click-configure` has an executable handler, that `point-click-action-structured` and `query-context-filter-expression-stats-unsupported` have executable validators, and that backend `validationContext`/target validation consumes action-specific `availableTargets[].events`. `validationContext` may supplement the validation view, but canonical `config` must win on overlapping paths and the context must never enter `proposedConfig`.
- Distinguish direct backend parity from host parity. Even when handler, resolver, validators, and compile-patch pass directly, keep the Page Builder/assistant surface as `suportado-parcialmente` until production requests project the governed target catalog through `validationContext` and expose fail-closed diagnostics to the author. Prove this bridge with HTTP/client evidence; a manifest fixture alone is insufficient.
- Transform compatibility is also a governed projection. The current Charts adapter's local `semanticKind` inference is provisional; do not widen it into a public contract. Require a Core-owned, composition-validated transform-output projection plus the target input-schema/port fields needed to validate mappings before claiming end-to-end compatibility.
- Treat the backend registry snapshot as a coordinated release artifact. If the current Angular aggregate contains unrelated parallel changes, do not copy it wholesale merely to erase drift; keep the exact drift explicit and synchronize the snapshot in the release cut that validates all affected components.
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
- discovery concurrency path: concurrent resolutions share only the in-flight read, the 10-second timeout releases a stalled read, completion/failure evicts it, and a later resolution performs a fresh permission-sensitive request;
- operational path: only strict root-relative catalog/capability paths are accepted, trailing-slash normalization preserves identity, and absolute/protocol-relative/relative or parity-drift inputs fail closed;
- identity path: an existing semantic resource key reopens against the catalog and is normalized to the canonical operational resource path before save/runtime;
- distribution path: terms and histogram candidates, metrics, bucket options, and fieldless count semantics remain mode/capability-gated;
- comparison path: exact `statsComparison` capability, eligible period/bucket/metric fields, complete period vocabulary, unique aliases, supported metrics, one `metrics[]` request, current/previous projection, and no local period or delta calculation are proven together;
- event target path: the same target linked from one chart output event is unavailable to unrelated events, `availableTargets[].events` preserves that exact evidence, and raw `pointClick` never substitutes for structured `pointAction`;
- AI parity path: the point-click handler, named validators, and backend consumption of action-specific target events execute against the same governed candidates as the visual editor;
- adversarial path: reject manual URL, invented field/metric, unsupported aggregation, stale target, label-based identity, unsafe route, and raw ECharts option.

Typical focused gates are:

```bash
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/services/praxis-chart-config-editor-context-resolver.service.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/services/chart-resource-capability-catalog.adapter.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/services/chart-composition-target-catalog.adapter.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' --include='projects/praxis-charts/src/lib/praxis-chart.metadata.spec.ts' --include='projects/praxis-charts/src/lib/providers/charts.providers.spec.ts' --include='projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts'
npx ng test praxis-core --watch=false --progress=false --include='projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts' --include='projects/praxis-core/src/lib/services/analytics-schema-contract.service.spec.ts' --include='projects/praxis-core/src/lib/composition/nested-port-catalog.service.spec.ts'
npx ng test praxis-core --watch=false --progress=false --include='projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts'
npm run build:praxis-charts
npx playwright test --config tools/e2e/playwright/praxis-charts-settings-panel.playwright.config.ts
```

When backend capability shape changes, add focused metadata-starter/quickstart HTTP proof and an Angular direct-consumer build. For visual selector changes, use desktop and narrow browser evidence with one successful search and one no-result search. Report which backend, Angular, Page Builder, AI registry, persistence, and browser surfaces were not exercised.
