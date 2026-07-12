---
name: praxis-charts-echarts-engine-boundary
description: Use when Codex must implement, audit, or consume @praxisui/charts engine behavior: PraxisChartEngineAdapter, PRAXIS_CHART_ENGINE_FACTORY, providePraxisCharts, EChartsEngineAdapter, internal option compilation, module registration, host/resize/dispose lifecycle, point and category event mapping, micro-visualization separation, or ECharts type leakage through public APIs.
---

# Praxis Charts ECharts Engine Boundary

Use this skill for the boundary that materializes canonical Praxis chart decisions in Apache ECharts. Hosts, authoring flows, metadata, AI tools, and persisted documents depend on `PraxisXUiChartContract`, `PraxisChartConfig`, and renderer-neutral events. ECharts modules, instances, options, params, and timing heuristics remain adapter-owned implementation details.

Pair it with:

- `praxis-charts-runtime-data` for config normalization, data resolution, transformation, and runtime states.
- `praxis-charts-analytics-interactions` when point events become selection, drilldown, cross-filter, or query context.
- `praxis-charts-authoring-settings` and `praxis-charts-authoring-catalogs` when editor previews must use the production materialization path.
- `praxis-charts-ai-handler-contracts` and `praxis-charts-ai-validation` when AI operations could bypass canonical chart decisions.
- `praxis-angular-public-api-governance` before exporting an adapter, token, provider, compiler, or engine-owned type.

## Canonical Ownership

Follow this direction of dependency:

`x-ui.chart` -> normalizer/validator/mapper -> `PraxisChartConfig` plus resolved rows -> internal engine option compiler -> `PraxisChartEngineAdapter` -> ECharts instance

- Add missing semantics to the canonical chart document, mapper, validator, or runtime config before changing ECharts options.
- Treat `PraxisChartEngineAdapter`, `PRAXIS_CHART_ENGINE_FACTORY`, and `providePraxisCharts({ engineFactory })` as the renderer-neutral extension boundary when they are public.
- Keep the option compiler adapter-owned. A service that returns `EChartsCoreOption` is not a renderer-neutral public Praxis service and must not be root-exported merely for convenience.
- Never persist, accept from AI, or expose raw `EChartsCoreOption`, formatter functions, ECharts params, or module constructors as the primary host contract.
- Keep `PraxisMicroVisualizationComponent` separate. It materializes compact core presentation contracts with lightweight HTML/CSS/SVG and does not share ECharts lifecycle or option semantics.

## Source Audit

Read `projects/praxis-charts/AGENTS.md` before editing. Inspect at least:

- `projects/praxis-charts/README.md` and `src/public-api.ts`
- `src/lib/adapters/chart-engine.adapter.ts`
- `src/lib/adapters/echarts/echarts-engine.adapter.ts`
- `src/lib/tokens/chart-engine.token.ts`
- `src/lib/providers/charts.providers.ts`
- `src/lib/services/chart-option-builder.service.ts`
- `src/lib/services/chart-data-transformer.service.ts`
- `src/lib/components/praxis-chart/praxis-chart.component.ts`
- `src/lib/components/praxis-micro-visualization/praxis-micro-visualization.component.ts`
- direct consumers, authoring manifests, README examples, and focused specs for all of the above

Do not infer coverage from a spec filename. Read its assertions and compare them with the lifecycle and event matrix below.

## Provider Boundary

- `providePraxisCharts()` installs the default ECharts renderer through `PRAXIS_CHART_ENGINE_FACTORY`. Hosts replace the renderer through the documented `providePraxisCharts({ engineFactory })` path, or by intentionally providing the factory token from the same canonical owner.
- A component-level provider shadows environment/root providers. Do not provide the concrete ECharts adapter locally when the public contract promises host replacement through the provider bundle.
- Preserve one mutable engine instance per chart component or host element. The factory may be shared by DI, but the component must call it to obtain a fresh adapter instance for that chart.
- Test the real public registration path. `TestBed.overrideComponent()` proves test substitution, not that `providePraxisCharts({ engineFactory })` is replaceable in production.
- Keep metadata registration and table inline-renderer registration in the provider bundle independent from the choice of chart engine.

## Engine Lifecycle

The mutable instance belongs to a specific host element:

1. Initialize once for the current host after it has a renderable size.
2. Re-render canonical config/data with replacement semantics appropriate to the full derived option; stale series or handlers must not survive.
3. Remove prior ECharts, zrender, and DOM handlers before installing callbacks for the new payload.
4. Resize from the observed current host without creating a second instance.
5. If the host element changes, detach handlers, dispose the old instance, observe the new element, and initialize again.
6. On loading, empty, error, or component destruction, cancel scheduled work, disconnect/reset observers, remove handlers, and dispose idempotently.

Track host identity explicitly in the adapter or owning runtime. `if (!chart) init(host)` is insufficient if `render()` can receive another element. A cached `ResizeObserver` must likewise rebind when Angular recreates `#chartHost` after a state transition.

Keep ECharts `use(...)`, renderer selection, and browser-only initialization centralized in the implementation path. Audit SSR/import safety separately from DOM-time safety; a browser guard around `render()` does not make module-level side effects automatically SSR-safe.

## Event Materialization

- Convert series clicks to `PraxisChartPointEvent`; never emit raw ECharts params.
- Preserve the canonical chart id, semantic series identity, category, normalized value, and source data needed by governed interactions.
- Grid/category fallback must reject non-finite coordinates, pixels outside the plot, unavailable axes, failed conversions, and out-of-range categories without emitting.
- Do not silently assign a category click to the first series in a multi-series chart. First classify whether existing optional event fields can represent a category-only interaction; introduce a contract only if downstream selection/cross-filter semantics cannot be expressed correctly.
- Audit vertical and horizontal category axes, multiple series, tuples, object values, primitive values, missing category data, and unsupported chart families.
- Deduplicate ECharts, zrender, and captured DOM notifications deterministically where possible. A short wall-clock window is a heuristic, not proof that two callbacks represent the same user action.
- Re-rendered callbacks must use the newest payload and must never retain stale config, rows, or handlers.

## Option Safety

- Compile only validated Praxis semantics into ECharts options. Engine defaults are derived materialization, not a second source of truth.
- Preserve stable ids and replace removed series, axes, titles, legends, datasets, visual maps, and interaction state when config changes.
- Keep formatters and callbacks library-owned; do not execute arbitrary functions supplied by metadata, persisted config, AI output, or host JSON.
- Register only required ECharts modules and renderers, and update tests/build whenever a supported Praxis chart family needs another module.
- Keep theme, accessibility, labels, sizing, and visual decisions aligned with canonical config. Do not add ECharts-shaped aliases when an existing Praxis field is merely under-materialized.

## Inventory Before New Contract

Classify each request before editing:

- `ja-suportado-so-ux`: canonical config already expresses the decision; sizing, theme, label, state, or event presentation needs correction.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: an exported option compiler or ECharts-shaped name duplicates semantics already owned by Praxis contracts.
- `suportado-parcialmente`: token/provider, host lifecycle, event model, option compiler, or observer exists but substitution, cleanup, mapping, or tests are incomplete.
- `lacuna-real-de-contrato`: no canonical document field, runtime model, renderer-neutral event, or adapter operation can express required behavior.

Only `lacuna-real-de-contrato` justifies a new public field or API. During beta, correct the canonical export/provider surface and update consumers in the same cycle instead of adding compatibility aliases.

## Validation Matrix

Choose the smallest commands that prove the changed behavior, but require assertions for every affected row:

- adapter instance: init once, update, current-host identity, host replacement, resize, idempotent destroy, and re-render after destroy;
- handlers: ECharts `off/on`, zrender detach/attach, DOM capture detach/attach, latest payload, and deterministic duplicate suppression;
- fallback events: invalid/outside pixels, vertical/horizontal categories, bounds, multi-series semantics, tuples, objects, and primitives;
- component DI: default registration and a custom engine through the real host/provider path, with multiple chart components isolated;
- component host: zero-size defer, ready -> non-ready -> ready host recreation, observer rebind, scheduled-frame cancellation, and final cleanup;
- option compiler and transformer: supported chart families, replacement safety, canonical mapping, and no executable/raw option ingress;
- micro visualization: remains functional without instantiating ECharts;
- public API: focal library build plus a direct consumer build when exports or providers change.

Typical focal gates are:

```bash
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/adapters/echarts/echarts-engine.adapter.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-option-builder.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-data-transformer.service.spec.ts'
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.spec.ts' --include='projects/praxis-charts/src/lib/components/praxis-micro-visualization/praxis-micro-visualization.component.spec.ts'
npm run build:praxis-charts
```

An existing helper-only adapter spec does not prove lifecycle or event wiring. Report exact assertions that ran, gaps left unproved, derived docs/examples/manifests reviewed, and whether a direct consumer build was required.
