---
name: praxis-charts-authoring-settings
description: Use when Codex must create, inspect, or fix @praxisui/charts visual authoring: PraxisChartConfigEditor, PraxisChartWidgetConfigEditor, SettingsValueProvider, Settings Panel apply/save/reset/reopen flows, availableResources/availableFields/availableTargets catalogs, chartDocument editing, queryContext editing, preview mapping, i18n, config editor metadata, or runtime/editor round-trip.
---

# Praxis Charts Authoring Settings

Use this skill for chart config editors and Settings Panel integration. The editor's job is to author the canonical `PraxisXUiChartContract` and runtime widget inputs faithfully, not to invent a separate chart configuration language.

Pair it with:

- `praxis-settings-panel-shell` for Settings Panel shell/protocol issues.
- `praxis-settings-roundtrip-authoring` for shared apply/save/reset/reopen behavior.
- `praxis-authoring-editors` for cross-component editor governance.
- `praxis-charts-runtime-data` when the edited document must be consumed by chart runtime services.
- `praxis-charts-ai-validation` when the editor path must remain aligned with AI manifest operations.
- `praxis-charts-authoring-catalogs` for governed resource, field, target, `SettingsValueProvider`, and preview catalogs.
- `praxis-charts-analytics-interactions` for `queryContext`, stats binding, drilldown, cross-filter, and selection semantics edited from the UI.
- `praxis-charts-echarts-engine-boundary` when preview/runtime parity depends on ECharts option mapping or adapter behavior.
- `praxis-charts-ai-handler-contracts` when AI operations must mirror visual editor paths.

## Canonical Chain

Keep this chain intact:

`PraxisXUiChartContract -> PraxisChartConfigEditor state -> SettingsValueProvider output -> apply/save -> persistence -> reopen -> PraxisChartComponent runtime`

For widget-hosted editing, keep:

`inputs.chartDocument + inputs.queryContext -> PraxisChartWidgetConfigEditor -> { inputs } -> page-builder/widget host -> runtime`

Do not persist raw ECharts options, local chart aliases, one-off host wrappers, or free-form stats URLs when the canonical document can express the need. If the editor cannot express a real runtime feature, decide whether the gap belongs in `x-ui.chart`, chart runtime, Settings Panel, or the host catalog before adding UI-only state.

## Required Source Inventory

Before editing chart authoring, inspect:

- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.html`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts`
- `projects/praxis-charts/src/lib/config-editor/services/chart-editor-defaults.service.ts`
- `projects/praxis-charts/src/lib/config-editor/services/chart-editor-preview-mapper.service.ts`
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`
- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.ts` when authorable paths change
- `projects/praxis-charts/src/lib/i18n/charts.*.ts` when labels, errors, helper text, tabs, or empty states change

Also inspect `@praxisui/settings-panel` contracts when the issue is panel protocol, footer state, dirty/valid/busy handling, save/apply timing, drawer sizing, or cancellation.

## Editor Rules

`PraxisChartConfigEditor` edits the canonical chart document. It should preserve:

- `version`, `kind`, `source`, `dimensions`, `metrics`, `events`, `legend`, `tooltip`, `labels`, `theme`, `motion`, `sizing`, and state descriptors.
- governed catalogs from `availableResources`, `availableFields`, and `availableTargets`.
- validation through `ChartContractNormalizerService` and `ChartContractValidationService`.
- preview through the chart preview mapper and runtime chart component, not a separate visual model.
- i18n for internal authoring text.

`PraxisChartWidgetConfigEditor` edits widget inputs. It must preserve `inputs.chartDocument` and structured `inputs.queryContext`. The query context editor may expose JSON as an advanced surface, but saved values must parse to an object and remain a runtime input, not be merged into `chartDocument.source` as string-built filters.

When the chart source is `praxis.stats`, remove stale local `inputs.data` on save/apply so remote stats remain the source of truth. When the source is `derived`, require a clear runtime data owner before relying on local rows.

## Round-Trip Checklist

Before calling chart authoring ready, verify:

- opening an existing chart loads the same `chartDocument` without silent drift.
- editing chart kind preserves compatible metrics/dimensions or produces visible validation errors.
- adding/removing series uses `metrics[].field` as identity and governed field options.
- changing source/resource/operation uses governed resource/field catalogs.
- `queryContext` accepts valid objects, rejects invalid JSON/non-objects, and survives reopen.
- apply/save emits the canonical `SettingsValueProvider` shape expected by the host.
- reset returns to the initial document and updates dirty/valid state.
- runtime preview consumes the same document shape that will be saved.
- internal editor labels and validation messages use chart i18n.

If the editor is opened through a dynamic widget/page-builder host, also verify `ComponentDocMeta` or equivalent metadata exposes `PraxisChartWidgetConfigEditor` as the config editor and that the host preserves the returned `{ inputs }` shape.

## Validation

Run focused validation for the surface touched:

- editor state/output: `praxis-chart-config-editor.spec.ts` and/or `praxis-chart-widget-config-editor.spec.ts`.
- metadata exposure: `praxis-chart.metadata.spec.ts`.
- runtime parity: mapper/validator specs from `praxis-charts-runtime-data`.
- AI alignment: manifest spec from `praxis-charts-ai-validation`.
- public authoring surface: build `@praxisui/charts` and validate a direct widget/editor consumer when available.

State any skipped browser or screenshot QA explicitly. For visual layout changes, inspect the actual rendered editor at desktop and mobile widths.
