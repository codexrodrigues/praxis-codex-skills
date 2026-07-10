---
name: praxis-charts-authoring-catalogs
description: Use when Codex must implement, audit, or consume @praxisui/charts visual authoring catalogs: PraxisChartConfigEditor, PraxisChartWidgetConfigEditor, ChartEditorResourceOption, ChartEditorFieldOption, ChartEditorTargetOption, availableResources, availableFields, availableTargets, chart editor defaults, preview mapper, SettingsValueProvider, Settings Panel round-trip, chart widget config editor, i18n, and docs/playground evidence.
---

# Praxis Charts Authoring Catalogs

Use this skill for chart authoring editors and governed resource/field/target catalogs. The editor authors `PraxisXUiChartContract` and widget inputs; catalogs ground user choices and AI/editor operations in real resources, fields, metrics, and targets.

Pair it with:

- `praxis-charts-authoring-settings` for the broader chart editor and Settings Panel workflow.
- `praxis-charts-runtime-data` when editor output must map to runtime.
- `praxis-charts-analytics-interactions` when catalogs represent stats/projection/queryContext behavior.
- `praxis-charts-ai-handler-contracts` when manifest operations must match editor catalogs.
- `praxis-angular-docs-playgrounds` when docs, examples, playgrounds, or AI recipes change.

## Source Audit

Inspect:

- `src/lib/config-editor/praxis-chart-config-editor.ts`
- `src/lib/config-editor/praxis-chart-config-editor.html`
- `src/lib/config-editor/praxis-chart-config-editor.spec.ts`
- `src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- `src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts`
- `src/lib/config-editor/models/*.ts`
- `src/lib/config-editor/services/chart-editor-defaults.service.ts`
- `src/lib/config-editor/services/chart-editor-preview-mapper.service.ts`
- `src/lib/praxis-chart.metadata.ts`
- `src/lib/i18n/charts.*.ts`
- relevant docs/playground/example files

Read `projects/praxis-charts/AGENTS.md` before editing chart authoring catalogs. Use `praxis-angular-agents-governance` if the local AGENTS file is missing, stale, or contradicts this skill.

## Catalog Rules

- `availableResources`, `availableFields`, and `availableTargets` are governed catalogs, not decorative dropdown data.
- Do not let the editor invent resource paths, field names, metric aliases, or event targets when catalogs are missing.
- Adding/removing series should use governed fields and preserve `metrics[].field` identity.
- Changing chart kind should preserve compatible dimensions/metrics or show validation errors.
- Widget editor must preserve `{ inputs.chartDocument, inputs.queryContext }` shape.
- Query context JSON is an advanced editor path; saved values must parse to structured objects.
- Preview must use the same runtime document shape that save/apply emits.
- Internal labels, helper text, empty states, and validation messages belong in chart i18n.

## Inventory Before New Contract

- `ja-suportado-so-ux`: catalogs and editor state exist but the UI, preview, messages, or docs are weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the editor uses local dropdown values where governed catalogs already carry resource, field, target, or metric identity.
- `suportado-parcialmente`: editor can author the path but preview, save/reopen, widget host, i18n, AI manifest, or docs evidence is incomplete.
- `lacuna-real-de-contrato`: no catalog, editor event/model, Settings Panel shape, runtime input, or validation path can express the authoring decision.

Only real gaps justify editor model or public API changes.

## Validation

Use focused gates:

- `praxis-chart-config-editor.spec.ts`;
- `praxis-chart-widget-config-editor.spec.ts`;
- `praxis-chart.metadata.spec.ts` when config editor exposure changes;
- chart runtime mapper/validator specs for output parity;
- manifest specs when AI/editor paths overlap;
- docs/playground validation when public examples change.

For visual layout changes, inspect the rendered editor at desktop and narrow widths.
