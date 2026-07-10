---
name: praxis-charts-echarts-engine-boundary
description: Use when Codex must implement, audit, or consume @praxisui/charts chart engine behavior: EChartsEngineAdapter, ChartEngineAdapter, CHART_ENGINE provider, providePraxisCharts, PraxisChartOptionBuilderService, ECharts option safety, renderer/module registration, resize/destroy lifecycle, pointClick/category click mapping, compact micro-visualization boundary, or raw ECharts option leakage.
---

# Praxis Charts ECharts Engine Boundary

Use this skill for the adapter boundary between Praxis chart contracts and Apache ECharts. Hosts and AI authoring should depend on `PraxisXUiChartContract`/`PraxisChartConfig`; raw ECharts options are implementation detail behind `ChartEngineAdapter`, `CHART_ENGINE`, and `PraxisChartOptionBuilderService`.

Pair it with:

- `praxis-charts-runtime-data` for the broader chart runtime contract.
- `praxis-charts-analytics-interactions` when point events feed query context, drilldown, cross-filter, or stats execution.
- `praxis-charts-authoring-catalogs` when editor preview must render through the same runtime path.
- `praxis-charts-ai-handler-contracts` when AI operations would otherwise patch raw ECharts options.

## Source Audit

Inspect:

- `projects/praxis-charts/README.md`
- `projects/praxis-charts/src/public-api.ts`
- `src/lib/adapters/chart-engine.adapter.ts`
- `src/lib/adapters/echarts/echarts-engine.adapter.ts`
- `src/lib/tokens/chart-engine.token.ts`
- `src/lib/providers/charts.providers.ts`
- `src/lib/services/chart-option-builder.service.ts`
- `src/lib/services/chart-data-transformer.service.ts`
- `src/lib/components/praxis-chart/praxis-chart.component.ts`
- `src/lib/components/praxis-micro-visualization/praxis-micro-visualization.component.ts`
- focused adapter, option builder, component, and micro-visualization specs

If `projects/praxis-charts/AGENTS.md` is absent, use `praxis-angular-agents-governance`, record that governance gap, and do not invent local validation commands in a one-off patch.

## Boundary Rules

- Do not expose raw ECharts options as the primary public config, AI operation payload, or editor persistence format.
- Add chart semantics to `PraxisXUiChartContract`, mappers, validators, or `PraxisChartConfig` before changing ECharts option building.
- Keep ECharts module registration inside the adapter/provider path.
- Preserve lifecycle: initialize once per host, update via `setOption`, remove old event handlers, resize, and dispose cleanly.
- Point and category click events must emit structured `PraxisChartPointEvent` data, not ECharts params directly.
- Grid/category fallback clicks must remain defensive: ignore invalid pixels, missing axes, or missing categories.
- `PraxisMicroVisualizationComponent` is not an ECharts adapter; it renders core presentation visualizations for dense cells/list/form summaries.

## Inventory Before New Contract

- `ja-suportado-so-ux`: Praxis config already expresses the visual decision; option builder, sizing, labels, theme, or event wiring needs polish.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: callers pass ECharts-shaped names where chart document or runtime config already has semantic fields.
- `suportado-parcialmente`: chart document/runtime supports the decision but option builder, adapter lifecycle, events, or tests are incomplete.
- `lacuna-real-de-contrato`: no chart document field, runtime config model, mapper, validator, or engine adapter path can express the needed behavior.

Only real gaps justify public API or contract changes. Prefer adding semantic chart contracts over accepting engine-specific option blobs.

## Validation

Use focused gates:

- `echarts-engine.adapter.spec.ts` for adapter lifecycle/events;
- `chart-option-builder.service.spec.ts` and `chart-data-transformer.service.spec.ts` for option safety;
- `praxis-chart.component.spec.ts` for component wiring;
- `praxis-micro-visualization.component.spec.ts` for compact visualization boundary;
- build `praxis-charts` for public API/provider changes.

Report exactly which adapter, option builder, event, micro-visualization, and build checks ran.
