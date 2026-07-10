---
name: praxis-charts-ai-handler-contracts
description: Use when Codex must implement, audit, or consume @praxisui/charts AI handler contracts: PRAXIS_CHARTS_AUTHORING_MANIFEST operations, editable targets, compile-domain-patch handlers, chart.document.set, chart.type.set, series.add/remove, axis.configure, data.resource.bind, queryContext.set, crossFilter/drilldown/selection configure, validators, failure modes, edit plans, generated AI registry assets, and assistant chart authoring.
---

# Praxis Charts AI Handler Contracts

Use this skill for executable AI chart authoring operations. AI should resolve chart intent semantically into manifest targets, operations, validators, and handler contracts; it must not patch raw chart JSON or ECharts options by keyword.

Pair it with:

- `praxis-charts-ai-validation` for the broader chart AI manifest workflow.
- `praxis-ai-authoring-manifests` for shared manifest invariants.
- `praxis-ai-registry-ingestion` when generated registry assets or component docs change.
- `praxis-charts-authoring-catalogs` when operations depend on available resource/field/target catalogs.
- `praxis-charts-analytics-interactions` for queryContext, cross-filter, drilldown, and stats binding.
- `praxis-charts-echarts-engine-boundary` when an AI request appears to require raw engine options.

## Source Audit

Inspect:

- `src/lib/ai/praxis-charts-authoring-manifest.ts`
- `src/lib/ai/praxis-charts-authoring-manifest.spec.ts`
- `src/lib/praxis-chart.metadata.ts`
- `src/lib/config-editor/praxis-chart-config-editor.ts`
- `src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- runtime validation and mapper services used by affected operations
- AI registry outputs when generated assets are expected to change

Read `projects/praxis-charts/AGENTS.md` before editing chart AI handlers. Use `praxis-angular-agents-governance` if the local AGENTS file is missing, stale, or contradicts this skill.

## Handler Rules

- Target resolution must use manifest editable targets with `ambiguityPolicy: "fail"`.
- `chart.document.set` must preserve `PraxisXUiChartContract` shape and version.
- `chart.type.set` must validate chart kind, orientation, series, and axis compatibility.
- `series.add/remove` uses `metrics[].field` as identity and validates governed fields/aggregations.
- `axis.configure` validates dimension/metric fields and secondary-axis constraints.
- `data.resource.bind` uses governed resources and fields; no free-form stats URLs.
- `queryContext.set` requires structured serializable objects.
- `crossFilter.configure`, `drilldown.configure`, and `selection.configure` emit structured event actions with governed targets and mappings.
- Visual toggles such as legend/tooltip remain visual-only unless they affect data binding.

## Inventory Before New Contract

- `ja-suportado-so-ux`: manifest operation exists but assistant UI, examples, diagnostics, or preview do not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: broad JSON patches or raw option edits are used where manifest operations already carry semantics.
- `suportado-parcialmente`: operation exists but handler contract, validators, editor parity, runtime round-trip, registry docs, or examples are incomplete.
- `lacuna-real-de-contrato`: no editable target, operation, validator, handler contract, or runtime path can express the chart authoring decision.

Only real gaps justify new AI operations. Prefer tightening handler contracts and validators over local intent heuristics.

## Validation

Use focused gates:

- `praxis-charts-authoring-manifest.spec.ts`;
- editor specs when operation paths are visually exposed;
- runtime mapper/validator specs when operations affect chart document consumption;
- registry ingestion validation when generated AI docs/assets should update;
- assistant/edit-plan harness or E2E when consult/edit behavior changes.

Report exactly which manifest, handler, editor, runtime, registry, and assistant checks were run.
