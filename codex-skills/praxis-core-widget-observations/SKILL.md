---
name: praxis-core-widget-observations
description: Use when Codex must implement, audit, document, or consume `@praxisui/core` dynamic widget infrastructure, including `WidgetDefinition`, `WidgetPageDefinition`, dynamic widget loader, widget shell, dynamic widget page, widget events, nested widget config accessor, widget page state runtime, composition runtime facade, connection manager, runtime component observation envelopes, observation registry, diagnostics, docs, public API, or Page Builder/runtime observation integration.
---

# Praxis Core Widget Observations

Use this skill for core dynamic widgets, dynamic pages, widget events, composition links, and runtime observations. Treat these as shared runtime contracts for materialized Praxis decisions, not as Page Builder-only implementation details.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md`
- `projects/praxis-core/docs/connection-editor.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/src/lib/widgets/**`
- `projects/praxis-core/src/lib/composition/**`
- `projects/praxis-core/src/lib/models/runtime-component-observation.model.ts`
- `projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.ts`
- `projects/praxis-core/src/lib/widgets/widget-event-path-normalizer.ts`
- `projects/praxis-core/src/lib/widgets/nested-widget-config-accessor.ts`
- `projects/praxis-core/src/lib/widgets/widget-page-state-runtime.service.ts`
- focused widget, composition, observation, and dynamic page specs

## Canonical Boundary

`@praxisui/core` owns shared widget/page models, widget loader primitives, widget shell, widget event model/path normalization, nested widget config access, widget page state runtime, composition runtime contracts, runtime trace/diagnostics, and runtime component observation envelopes.

`@praxisui/page-builder` may author pages and canvases, and vertical packages may provide widgets, but they should consume the core contracts instead of inventing local widget graphs, event paths, observation payloads, or composition link semantics.

## Runtime Rules

- Use `WidgetDefinition`, `WidgetPageDefinition`, `WidgetPageLayout`, and related core models for page/runtime structure.
- Use `DynamicWidgetLoaderDirective` and widget metadata rather than local selector switches when loading governed widgets.
- Use `WidgetEvent` and normalized event paths for widget output wiring.
- Use core composition services/facade for links, transforms, nested ports, traces, and diagnostics.
- Runtime observations must be serializable `PraxisRuntimeComponentObservationEnvelope` values with redaction diagnostics.
- Do not include functions, symbols, bigint, circular references, raw secrets, or unredacted large data snapshots in observations.
- Preserve identity fields: instance id, component id/type, widget key, owner package, route key, resource refs, page id, and manifest refs.
- Use observation claims for component, manifest, resource, schema field, selection, operation, surface, action, state digest, or data digest facts. Do not expose full backend payloads when a digest/ref is enough.

## Inventory Before New Contract

Classify gaps before adding widget or observation contracts:

- `ja-suportado-so-ux`: model/observation exists but Page Builder, docs, or diagnostics do not show it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a local widget/event/observation shape should map to existing core contracts.
- `suportado-parcialmente`: core model exists but loader, registry, composition, observation, docs, or consumer validation is incomplete.
- `lacuna-real-de-contrato`: no core widget, composition, event, observation, or diagnostic contract can carry the runtime fact.

For real gaps, update core models/specs and at least one direct consumer proof.

## Validation

Use the smallest reliable proof:

- widget loader, shell, event paths, nested widget access, page models, presets, and state runtime:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-shell.component.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-event-path-normalizer.spec.ts --include=projects/praxis-core/src/lib/widgets/nested-widget-config-accessor.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page.model.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page-presets.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page-state-runtime.service.spec.ts
```

- dynamic widget page, composition serialization/factory, and record surface/open recipes:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page-composition.serialization.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page-composition.factory.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-record-surface-open.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-page-rich-table-recipe.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-page-actions-workspace-recipe.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-page-nested-path-recipe.spec.ts
```

- composition runtime evidence consumed by observations:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/composition/composition-runtime.engine.spec.ts --include=projects/praxis-core/src/lib/composition/composition-runtime.facade.spec.ts --include=projects/praxis-core/src/lib/composition/composition-runtime-store.spec.ts --include=projects/praxis-core/src/lib/composition/composition-validator.service.spec.ts
```

- runtime observation envelopes, registry, serializability, redaction, and Page Builder collection integration:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-runtime-observation.spec.ts
npm run ng -- test praxis-page-builder --watch=false --progress=false --include=projects/praxis-page-builder/src/lib/dynamic-page-builder.component.spec.ts --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor-graph.util.spec.ts
```

- `npm run build:praxis-core` plus a Page Builder or direct widget consumer build when public contracts change.

Report whether runtime observations were checked for serializability and redaction.

## Companion Skills

- Use `praxis-core-composition-runtime` for composition links, widget events, surface hosts, and runtime observations.
- Use `praxis-core-component-registry-contracts` when widget discovery depends on component metadata registry entries, editorial descriptors, ports, insertion presets, or AI component context.
- Use `praxis-core-global-action-payloads` when widget events execute structured global actions or emit `surface.result`/composition dispatch payloads.
- Use `praxis-page-builder-composition` for Page Builder authoring/runtime composition on top of core.
- Use `praxis-core-providers-bootstrap` when widget loading requires provider/registry wiring.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` for public exports and validation scope.
