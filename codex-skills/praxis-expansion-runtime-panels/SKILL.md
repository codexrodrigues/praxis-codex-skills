---
name: praxis-expansion-runtime-panels
description: Use when Codex must implement, audit, document, or author `@praxisui/expansion` surfaces, including metadata-first expansion panels, accordion defaults, `expansionId` persistence, `providePraxisExpansionMetadata`, `providePraxisExpansionDefaults`, lazy panel content, panel events, imperative open or close methods, Settings Panel editors, widget events, AI authoring manifests, docs, examples, or host integration for Praxis expansion panels.
---

# Praxis Expansion Runtime Panels

Use this skill for the canonical `@praxisui/expansion` runtime and authoring surface. Treat expansion panels as governed metadata-first containers, not as local accordions.

## Source Audit

Before editing code or guidance, inspect the relevant source:

- `projects/praxis-expansion/AGENTS.md`
- `projects/praxis-expansion/README.md`
- `projects/praxis-expansion/src/public-api.ts`
- `projects/praxis-expansion/src/lib/praxis-expansion.ts`
- `projects/praxis-expansion/src/lib/praxis-expansion.spec.ts`
- `projects/praxis-expansion/src/lib/praxis-expansion.metadata.ts`
- `projects/praxis-expansion/src/lib/praxis-expansion-widget-config-editor*`
- `projects/praxis-expansion/src/lib/ai/**`

If public docs, registry, playgrounds, or examples mention expansion panels, also audit those derived artifacts before declaring the issue complete.

## Canonical Boundary

`@praxisui/expansion` owns:

- `ExpansionMetadata`, `PanelMetadata`, accordion behavior, panel identity, appearance, content, widgets, and action button semantics
- `providePraxisExpansionMetadata()` registration in `ComponentMetadataRegistry`
- `providePraxisExpansionDefaults()` and Material expansion defaults, with instance `defaultOptions` taking precedence
- `expansionId`, `componentInstanceId`, and persistence through `ASYNC_CONFIG_STORAGE`
- lazy panel rendering through Material expansion panel content
- panel events including `opened`, `closed`, `expandedChange`, `afterExpand`, `afterCollapse`, and `destroyed`
- imperative methods including `open`, `close`, `toggle`, `openAll`, and `closeAll`
- `widgetEvent` propagation from nested widgets with panel-aware path context
- Settings Panel widget config editor, AI assistant integration, and `PRAXIS_EXPANSION_AUTHORING_MANIFEST`

Hosts and docs consume these contracts. Do not create host-local accordions, parallel panel config, or local event buses when the expansion lib owns metadata, events, persistence, and nested widget materialization.

## Runtime Rules

- Require a stable `expansionId` for persisted or customizable surfaces. Add `componentInstanceId` when the same logical expansion component can appear multiple times on a route.
- Keep `panels[].id` stable. Authoring, event payloads, DOM ids, widget paths, persistence, and nested references should resolve by id before title or index.
- Use `providePraxisExpansionMetadata()` when the component must be discoverable by registries, dynamic pages, or page-builder-style hosts.
- Use `providePraxisExpansionDefaults()` for app-level defaults and instance `defaultOptions` for local overrides. Do not hardcode Material defaults in consumers.
- Prefer metadata `content` and `widgets` inside panels. Use host projection only when the host intentionally owns the nested component lifecycle.
- Forward nested widget events through `widgetEvent` instead of app-specific event relays.
- Keep action buttons as local component actions unless a canonical global action or composition link contract is explicitly introduced by the owning platform surface.

## Authoring Rules

- Use the package widget config editor, manifest capabilities, context packs, and `PRAXIS_EXPANSION_AUTHORING_MANIFEST` for governed authoring.
- Keep Settings Panel apply/save/reset/reopen aligned with runtime config consumption.
- Keep i18n for authoring chrome and assistant labels in the package i18n path.
- When AI authors panel changes, ensure operations target stable panel ids and preserve event/persistence semantics.
- If a requested edit cannot be represented by the existing manifest or editor capability, classify it as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato` before adding a contract.

## Validation

Use the smallest reliable proof for the touched surface:

- `ng build praxis-expansion` or the repo's equivalent focal build
- focused specs for expansion runtime, metadata provider registration, persistence, panel events, widget events, and editor behavior
- registry or dynamic page validation when provider metadata or `ComponentMetadataRegistry` integration changes
- Settings Panel round-trip validation when config editor behavior changes
- AI registry or authoring manifest validation when `ai/**`, capabilities, manifest refs, or registry docs change
- docs/playground validation when public examples or docs are updated

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-navigation-containers-ai-validation` for expansion AI manifests, registry projection, context packs, assistant turns, and cross-container validation.
- Use `praxis-authoring-editors` for Settings Panel editor round-trip.
- Use `praxis-core-composition-runtime` for nested widgets, widget events, composition links, dynamic page materialization, and registry-hosted components.
- Use `praxis-angular-i18n-governance`, `praxis-angular-public-api-governance`, `praxis-angular-docs-playgrounds`, and `praxis-angular-validation-gates` when the change touches their governed areas.
