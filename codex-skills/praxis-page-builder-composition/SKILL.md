---
name: praxis-page-builder-composition
description: Use when Codex must inspect, change, or scaffold @praxisui/page-builder composition behavior: DynamicPageBuilderComponent, WidgetPageDefinition, praxis-dynamic-page runtime materialization, component palette, ComponentMetadataRegistry, widget keys, canvas layout, page.composition.links, connection editor graph, nestedPath component-port endpoints, page state, global-action endpoints, or public API.
---

# Praxis Page Builder Composition

Use this skill for the Page Builder runtime/composition surface. `@praxisui/page-builder` is the canonical visual editor for dynamic pages based on `WidgetPageDefinition` and the `praxis-dynamic-page` runtime; it must not become a parallel component runtime, host-local connection language, or owner of child widget semantics.

Pair it with:

- `praxis-core-composition-runtime` for shared `WidgetPageDefinition`, widget events, widget shell, composition links, transforms, runtime observations, and dynamic page materialization.
- `praxis-page-builder-authoring` for page config editors, shell editor, Settings Panel bridge, and visual round-trip.
- `praxis-page-builder-ai-agentic` for agentic page composition, AI catalogs, manifests, streaming authoring, and preview/apply flows.
- the owning child component skill, such as charts, table, form, fields, or CRUD, when a widget input/config document changes.

## Canonical Boundary

Persist and materialize `WidgetPageDefinition`. Do not reintroduce `GridPageDefinition` as the canonical builder shape. Legacy `options`, `layout`, `x/y/cols/rows`, and similar compatibility fields must be normalized explicitly and not promoted as current guidance.

Page Builder owns:

- visual page editing around `praxis-dynamic-page`;
- component palette insertion from `ComponentMetadataRegistry`, `ComponentDocMeta`, and insertion presets;
- stable `widget.key` identity and canvas items;
- page-level shell, grouping, theme/layout presets, state, context, device layouts, and slot assignments;
- `page.composition.links`, connection graph UX, diagnostics, nested component-port paths, state endpoints, and global-action endpoints.

Child components own their inputs, runtime behavior, config editors, authoring manifests, and validation. Page Builder may host or delegate those editors; it must not special-case table/form/chart/list semantics locally.

## Required Source Inventory

Before editing Page Builder composition, inspect:

- `projects/praxis-page-builder/AGENTS.md`
- `projects/praxis-page-builder/src/public-api.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-builder.component.ts`
- `projects/praxis-page-builder/src/lib/praxis-page-builder.metadata.ts`
- `projects/praxis-page-builder/src/lib/editor/component-palette-dialog.component.ts`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.ts`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor-graph.util.ts`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/*.{ts,spec.ts}` for graph, geometry, layout, port order, trace, and wire changes
- `projects/praxis-core/src/lib/composition/**`, `widgets/**`, and composition model files when runtime contracts are affected
- focused specs called out by the local `AGENTS.md`

## Composition Rules

Use stable widget keys for all widget, canvas, shell, and composition operations. Never address widgets by array index in persisted links or AI/edit operations.

Model wiring as canonical `page.composition.links`:

- component endpoints: `{ kind: "component-port", ref: { widget, port, direction, bindingPath?, nestedPath? } }`
- state endpoints: `{ kind: "state", ref: { path, layer? } }`
- global-action endpoints: `{ kind: "global-action", ref: { actionId, payload?, payloadExpr?, meta? } }`
- link identity: stable `id`
- intent: use the runtime `LinkIntent` vocabulary, not command strings
- conditions/transforms: use the shared composition transform/JSON Logic path

For nested widgets, preserve `nestedPath` and terminal child widget identity. Do not flatten nested component ports into string aliases that cannot round-trip through the runtime.

For palette work, derive entries from `ComponentMetadataRegistry` and `ComponentDocMeta`. `ComponentDocMeta.configEditor`, actions, commands, insertion presets, tags, icon, and descriptions are owned by the component metadata source, not by a Page Builder hardcoded list.

## Public API

Treat `projects/praxis-page-builder/src/public-api.ts` as public contract. Changes can affect hosts, AI registry ingestion, `@praxisui/core`, Settings Panel bridge, child component config editors, docs, and examples. Map those consumers before changing exports.

Do not make Page Builder a transitively convenient root barrel for another public lib. Prefer the canonical owner for shared types and expose only Page Builder's own intentional surface.

## Validation

Use the smallest reliable gate:

- composition graph/link changes: `connection-editor.component.spec.ts` plus relevant graph/layout/port-order/trace/wire util specs.
- palette changes: `component-palette-dialog.component.spec.ts` and browser smoke when insertion UX changes.
- runtime page shape changes: `dynamic-page-builder.component.spec.ts`, core composition runtime specs, and `ng build praxis-page-builder`.
- public API changes: build `praxis-page-builder` and at least one direct consumer when feasible.
- browser interaction changes: local Playwright lane for palette insertion or page-builder authoring, not GitHub Actions as the first diagnostic tool.

When validation is partial, state exactly which specs or browser lanes ran and which runtime/materialization gates remain.
