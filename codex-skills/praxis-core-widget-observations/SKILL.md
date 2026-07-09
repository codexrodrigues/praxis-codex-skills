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

- `dynamic-widget-loader.directive.spec.ts`
- `dynamic-widget-page.component.spec.ts`
- widget event/path normalizer specs
- widget page model/presets/state runtime specs
- composition runtime facade/engine/store/validator specs
- runtime component observation registry/model specs
- `npm run build:praxis-core` plus a Page Builder or direct widget consumer build when public contracts change

Report whether runtime observations were checked for serializability and redaction.

## Companion Skills

- Use `praxis-core-composition-runtime` for composition links, widget events, surface hosts, and runtime observations.
- Use `praxis-page-builder-composition` for Page Builder authoring/runtime composition on top of core.
- Use `praxis-core-providers-bootstrap` when widget loading requires provider/registry wiring.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` for public exports and validation scope.
