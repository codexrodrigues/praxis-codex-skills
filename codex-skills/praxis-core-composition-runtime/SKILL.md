---
name: praxis-core-composition-runtime
description: Use when Codex must inspect, change, or rely on @praxisui/core composition and widget runtime contracts: DynamicWidgetPageComponent, widget definitions, widget events, widget shell, composition links, nested ports, connection/link execution, transform runtime, surface hosts, related-resource outlets, runtime observations, or dynamic page materialization.
---

# Praxis Core Composition Runtime

Use this skill for `@praxisui/core` composition, widget, dynamic page, connection, and surface-host runtime contracts.

This area materializes governed component and page decisions. It should not become a local page-builder dialect, host-only composition language, or keyword-routed action system. Page Builder and Visual Builder may author decisions, but core owns the shared runtime structures that execute them.

## Source Audit

Inspect the affected source before changing guidance or code:

- `projects/praxis-core/docs/connection-editor.md`
- `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md`
- `projects/praxis-core/src/lib/composition/**`
- `projects/praxis-core/src/lib/widgets/**`
- `projects/praxis-core/src/lib/surfaces/praxis-surface-host.component.ts`
- `projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.component.ts`
- `projects/praxis-core/src/lib/models/composition-*.ts`
- `projects/praxis-core/src/lib/models/port-contract.model.ts`
- `projects/praxis-core/src/lib/models/runtime-component-observation.model.ts`
- `projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.ts`
- `projects/praxis-core/src/lib/services/surface-binding-runtime.service.ts`

Read the focused specs for composition runtime, link execution, nested ports, widget loader, dynamic widget page, runtime observations, and surface hosts before deciding a contract is missing.

## Canonical Boundary

Core owns:

- `WidgetDefinition`, `WidgetPageDefinition`, widget shell contracts, widget events, nested widget config access
- dynamic widget loading and materialized widget runtime
- composition link model, transform pipeline, diagnostics, runtime traces, link execution, nested ports
- surface host and related-resource outlet runtime
- runtime component observation and event propagation

Page Builder, Visual Builder, component libraries, and host apps consume these contracts. They should not redefine the same config/event/link semantics locally.

## Decision Rules

- If the task is about authoring a page/editor graph, use the builder skill as the functional owner and this skill for the runtime contract.
- If the task is specifically about `@praxisui/page-builder`, pair with `praxis-page-builder-composition` for palette, canvas, graph, connection editor, and page-builder-owned authoring semantics.
- If the task is about `SettingsValueProvider`, apply/save/reset, or config editor round-trip, use `praxis-authoring-editors` as well.
- If the task is about a specific widget's visual/product UX, use `praxis-ui-product-design` with the owning component skill.
- If a host composes a page by copying local event buses, action routers, or link transforms, prefer the core composition runtime or open a core follow-up.
- Do not persist local command strings such as `showAlert:...`, `surface.open:...`, or `navigate:...` when `GlobalActionRef`, surface metadata, or composition links can express the decision.

## Runtime Evidence

Before declaring composition complete, identify:

- source of the widget/component catalog entry
- canonical config shape being materialized
- event and output contract
- link or transform that moves data between widgets
- diagnostics when a target, port, or transform cannot resolve
- runtime observation evidence when behavior is user-visible
- public API and AI manifest impact when the component is public

## Validation Guidance

Prefer focused specs:

- composition runtime engine/facade/store specs
- link executor and transform runtime specs
- nested port catalog specs
- dynamic widget loader and dynamic widget page specs
- widget recipe specs for rich table, nested path, actions workspace, and record surface open
- surface host and related-resource outlet specs

For visual/editor flows, add screenshot or browser validation through the official host route when feasible.

## Companion Skills

- Use `praxis-core-runtime-contracts` for public API, shared models, tokens, i18n, logging, and providers.
- Use `praxis-authoring-editors` for editor/runtime round-trip and Settings Panel behavior.
- Use `praxis-page-builder-composition`, `praxis-page-builder-authoring`, and `praxis-page-builder-ai-agentic` when the shared runtime contract is being authored or exercised through `@praxisui/page-builder`.
- Use `praxis-ui-product-design` for visual hierarchy, accessibility, and screenshot QA.
