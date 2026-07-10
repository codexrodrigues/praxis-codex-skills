---
name: praxis-navigation-container-composition-events
description: Use when Codex must implement, audit, or consume composition behavior for Praxis navigation containers: @praxisui/tabs, @praxisui/stepper, PraxisWizardFormComponent, @praxisui/expansion, nested widgets, WidgetEventEnvelope path enrichment, dynamic page embedding, renderBody/external panel ownership, lazy content, component metadata registry, gridster/page-builder hosting, and composition links.
---

# Praxis Navigation Container Composition Events

Use this skill for nested widget composition, dynamic page materialization, and event propagation across tabs, stepper/wizard, and expansion. These components are governed containers; they should forward canonical widget events and component metadata rather than creating local callback buses.

Pair it with:

- `praxis-tabs-runtime-authoring` for tabs group/nav selection, `renderBody`, lazy loading, and tab/link ids.
- `praxis-stepper-wizard-runtime` for step-aware widget events, dynamic-form steps, and wizard wrapper flows.
- `praxis-expansion-runtime-panels` for panel-aware events, lazy panel content, provider metadata, and action buttons.
- `praxis-core-composition-runtime` for `WidgetDefinition`, `WidgetEventEnvelope`, composition links, nested ports, runtime observations, and dynamic page materialization.
- `praxis-page-builder-composition` when the container is authored or consumed inside Page Builder.
- `praxis-authoring-editors` when nested config is edited through Settings Panel.

## Source Audit

Inspect:

- `projects/praxis-tabs/AGENTS.md`, `README.md`, `src/lib/praxis-tabs.ts`, `src/lib/praxis-tabs-widget-event.spec.ts`, metadata and quick setup specs.
- `projects/praxis-stepper/AGENTS.md`, `README.md`, `src/lib/praxis-stepper.ts`, wizard adapter/component files, and stepper widget specs.
- `projects/praxis-expansion/AGENTS.md`, `README.md`, `src/lib/praxis-expansion.ts`, `src/lib/praxis-expansion.metadata.ts`, metadata specs, and widget event specs.
- `projects/praxis-core/src/lib/composition/**`, widget models, nested port contracts, dynamic widget page, and runtime observation services when events cross component boundaries.
- Page Builder or dynamic page hosts when the task mentions canvas, gridster, nested config, or composition links.

## Canonical Boundary

The container library owns container-local identity, selection/expanded state, lazy materialization, and path enrichment. Core owns the shared widget, event, composition link, nested port, and runtime observation contracts. Hosts own route-level state and business effects.

Do not replace `WidgetEventEnvelope`, composition links, global actions, or surface metadata with app-local event buses, command strings, keyword routers, or label-based callback names.

## Composition Rules

- Stable ids are the path anchors: `tabs[].id`, `nav.links[].id`, `steps[].id`, and `panels[].id`.
- Container event paths must include container context and the selected tab/link, step, or panel segment.
- Use `group.renderBody=false` or `nav.renderBody=false` only when a host intentionally owns the active body outside tabs.
- Preserve lazy content semantics: tabs lazy cache, expansion `matExpansionPanelContent`, and wizard/stepper deferred child runtime should not require eager child instances.
- Prefer container `content`/`widgets` metadata over host projection unless the host intentionally owns child lifecycle.
- Action buttons inside expansion remain local component actions unless mapped through a canonical global action or composition link.
- Dynamic pages and Page Builder should consume metadata/provider registrations rather than hardcoding container selectors.

## Inventory Before New Contract

- `ja-suportado-so-ux`: container events, lazy content, or dynamic page embedding already work; UI, docs, or host wiring needs correction.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local callbacks, labels, indexes, or selector names are used where stable ids, `WidgetEventEnvelope`, or component metadata already exists.
- `suportado-parcialmente`: container supports the path but event enrichment, registry metadata, nested config, docs, or focused tests are incomplete.
- `lacuna-real-de-contrato`: no container metadata, core widget/event contract, composition link, nested port, or runtime observation can express the composition decision.

Only a real gap justifies a new shared composition or public component contract.

## Validation

Use focused gates:

- tabs widget event, selection, renderBody, lazy, and metadata specs;
- stepper widget event, dynamic-form step, validation, and wizard adapter/component specs;
- expansion metadata/provider, panel event, lazy content, and widget event specs;
- core composition link, nested port, dynamic widget page, or runtime observation specs when events cross containers;
- Page Builder/dynamic page smoke when the behavior depends on a host canvas.

State exactly which container, core composition, dynamic page, and docs/registry checks ran.
