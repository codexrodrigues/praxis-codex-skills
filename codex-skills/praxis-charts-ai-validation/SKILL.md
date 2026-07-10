---
name: praxis-charts-ai-validation
description: Use when Codex must create, update, or audit @praxisui/charts AI authoring contracts: PRAXIS_CHARTS_AUTHORING_MANIFEST, chartDocument operations, editableTargets, validators, handler contracts, chart edit plans, queryContext/crossFilter/drilldown operations, AI registry ingestion, component metadata, generated AI assets, or assistant validation for chart authoring.
---

# Praxis Charts AI Validation

Use this skill for executable AI chart authoring. The chart manifest is a governed contract for semantic edits to `PraxisXUiChartContract` and widget inputs; it is not decorative documentation and must not devolve into arbitrary JSON patching.

Pair it with:

- `praxis-ai-authoring-manifests` for shared manifest invariants and edit-plan rules.
- `praxis-ai-registry-ingestion` when generated registry/catalog/package AI assets are affected.
- `praxis-ai-semantic-intent` when the change touches intent routing or consult/edit boundaries.
- `praxis-charts-authoring-settings` when manifest operations must match visual editor paths.
- `praxis-charts-runtime-data` when operations affect runtime chart mapping, stats requests, events, or public chart models.
- `praxis-charts-ai-handler-contracts` for operation schemas, validators, handler contracts, edit plans, and generated AI registry details.
- `praxis-charts-authoring-catalogs` when operations depend on governed resources, fields, targets, editor catalogs, or preview mapping.
- `praxis-charts-analytics-interactions` when operations affect `queryContext`, stats, cross-filter, drilldown, or selection behavior.
- `praxis-charts-echarts-engine-boundary` when a request appears to require raw ECharts options so the adapter boundary stays canonical.

## Canonical AI Boundary

AI must author chart decisions through governed targets and operations:

`semantic request -> editable target -> operation schema -> validator -> effect/handler contract -> chartDocument/queryContext path -> editor/runtime round-trip`

Do not route chart intent by keywords such as "ranking", "trend", "pie", or "KPI" in the Angular host. The assistant should use governed component manifests, available resources, available fields, analytics projections, capabilities, and declared tools for grounding. Text matching can rank field or resource candidates only after semantic scope is resolved.

Do not expose raw ECharts option patches, free-form JSON Patch, local metric aliases, or host-only command strings as the primary edit mechanism. If a requested edit needs a new semantic operation, add or revise a manifest operation with deterministic target resolution and validators.

## Required Source Inventory

Before editing chart AI behavior, inspect:

- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.ts`
- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts`
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- `projects/praxis-charts/src/lib/services/chart-contract-validation.service.ts`
- `projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.ts`
- `projects/praxis-charts/src/public-api.ts`
- AI registry ingestion outputs or generated component docs when the repo produces them

Read `projects/praxis-charts/AGENTS.md` before editing chart AI authoring contracts. Use `praxis-angular-agents-governance` if the local AGENTS file is missing, stale, or contradicts this skill.

## Manifest Rules

The chart manifest should declare:

- component identity: `componentId = praxis-chart`, owner package `@praxisui/charts`, config schema `PraxisXUiChartContract`.
- runtime inputs: `chartDocument`, `config`, `queryContext`, `remoteDataResolver`, `availableResources`, `availableFields`, and `availableTargets`.
- editable targets for chart type, series, axis, data binding, query context, cross-filter, drilldown, selection, legend, tooltip, labels, theme, sizing, motion, and state when supported.
- operations with concrete schemas for `chart.document.set`, `chart.type.set`, `series.add`, `series.remove`, `axis.configure`, `data.resource.bind`, `queryContext.set`, event mapping, and visual toggles.
- destructive operations such as series removal with confirmation.
- `compile-domain-patch` handler contracts for operations requiring semantic field/resource/target resolution.
- affected paths that overlap actual effects.
- validators that prove chart type compatibility, governed field/resource existence, stats operation support, safe query context, event target validity, and editor/runtime round-trip.

Every operation target must resolve through an editable target with `ambiguityPolicy: "fail"`. Broad object schemas are acceptable only when the downstream handler contract declares how candidates are grounded and validated.

## Chart-Specific Guardrails

For series edits, use `chartDocument.metrics[].field` as identity and validate against `availableFields[]`. For axes, preserve combo-only secondary axis constraints and cartesian versus pie/donut requirements. For data binding, validate `source.kind`, resource, operation, dimensions, and metrics against governed catalogs. For `queryContext`, require structured object semantics.

For cross-filter, drilldown, and selection, emit structured event actions such as `filter-widget`, `open-detail`, `navigate`, `update-context`, or `emit` with governed targets and field mappings. Never encode event behavior as command words, regexes, metric-name conventions, or Angular switch statements.

For capability-protected metrics, require the backend/catalog to publish the capability decision or omit/block the chart. AI must not infer authorization from labels, menu visibility, or previous examples.

## Synchronization Triggers

Review chart AI contracts when any of these change:

- `PraxisXUiChartContract`, `PraxisChartConfig`, data source, query context, events, sizing, theme, or state models.
- `PraxisChartConfigEditor` or `PraxisChartWidgetConfigEditor` editable paths.
- `PraxisChartComponent` inputs/outputs or component metadata.
- chart public API exports.
- registry ingestion, generated component docs, AI assets, context packs, quick replies, diagnostics, previews, or apply payloads.
- dashboard catalog chart document shape or chart backend payload adapter behavior.

If no manifest update is required after a public chart/runtime/editor change, state why.

## Validation

Minimum validation:

- run `praxis-charts-authoring-manifest.spec.ts` after manifest changes.
- run editor specs when changed operation paths are exposed visually.
- run runtime mapper/validator specs when operations affect `x-ui.chart` shape or runtime consumption.
- run registry ingestion validation when generated AI registry/catalog assets are expected to change.
- run assistant/edit-plan E2E or a focused harness when consult/edit response behavior changes.

When validation is partial, report which manifest invariants were checked and which registry or assistant gates remain unexecuted.
