---
name: praxis-tabs-runtime-authoring
description: Use when Codex must implement, audit, document, or author `@praxisui/tabs` surfaces, including group or nav modes, `tabsId` persistence, `selectedIndex`, lazy tab content, `renderBody`, quick setup, Settings Panel editors, widget events, AI authoring manifests, docs, examples, or host integration for Praxis tabs.
---

# Praxis Tabs Runtime Authoring

Use this skill for the canonical `@praxisui/tabs` runtime and authoring surface. Treat tabs as a governed Praxis navigation/container component, not as a local Angular Material wrapper.

## Source Audit

Before editing code or guidance, inspect the relevant source:

- `projects/praxis-tabs/AGENTS.md`
- `projects/praxis-tabs/README.md`
- `projects/praxis-tabs/src/public-api.ts`
- `projects/praxis-tabs/src/lib/praxis-tabs.ts`
- `projects/praxis-tabs/src/lib/praxis-tabs.spec.ts`
- `projects/praxis-tabs/src/lib/praxis-tabs-widget-event.spec.ts`
- `projects/praxis-tabs/src/lib/quick-setup/**`
- `projects/praxis-tabs/src/lib/praxis-tabs-config-editor*`
- `projects/praxis-tabs/src/lib/tabs-editor-capability*`
- `projects/praxis-tabs/src/lib/ai/**`

If public docs, registry, playgrounds, or examples mention tabs, also audit those derived artifacts before declaring the issue complete.

## Canonical Boundary

`@praxisui/tabs` owns:

- `TabsMetadata`, `TabGroupMetadata`, `TabNavMetadata`, tab/link identity, content, widgets, appearance, and behavior semantics
- group mode and nav mode behavior, including `group.renderBody=false` and `nav.renderBody=false` for host-owned external panels
- `tabsId`, `componentInstanceId`, and `configPersistenceStrategy` based persistence through `ASYNC_CONFIG_STORAGE`
- controlled and uncontrolled `selectedIndex` behavior
- lazy tab body loading and visible-index mapping for hidden or disabled items
- `widgetEvent` propagation from nested widgets with path segments that include the tabs container and selected tab/link
- Settings Panel config editor, quick setup, AI assistant trigger, editor capability, and `PRAXIS_TABS_AUTHORING_MANIFEST`

Hosts and docs consume these contracts. Do not create host-local tab config aliases, keyword-routed tab commands, or parallel JSON patch formats when the lib manifest/editor capability can express the decision.

## Runtime Rules

- Require a stable `tabsId` for persisted or customizable surfaces. Add `componentInstanceId` when the same logical tabs component can appear multiple times on a route.
- Choose `configPersistenceStrategy` deliberately. Use `input-first` for governed previews or nested widget materializations where input config must dominate stored customization.
- Preserve `selectedIndex` semantics. External `selectedIndex` input updates the active tab without implying a user selection event; user selection emits `selectedIndexChange`.
- Preserve stable `tabs[].id` and `nav.links[].id`. Authoring, event paths, removal, reordering, disabled state, visibility, and reselection should resolve by id before label or index.
- Use `group.renderBody=false` or `nav.renderBody=false` only when the host intentionally owns the content panel. Otherwise let tabs render `content` and `widgets` internally.
- Use `config.behavior.lazyLoad` for expensive tab bodies instead of ad hoc `*ngIf` wrappers in consumers.
- Forward nested widget events through the component `widgetEvent` output instead of creating a host-only event bus.

## Authoring Rules

- Use `PraxisTabsConfigEditor`, `TabsQuickSetupComponent`, `TabsAuthoringDocument`, `buildTabsApplyPlan`, and `PRAXIS_TABS_AUTHORING_MANIFEST` as the canonical authoring path.
- Treat tab add/remove/reorder/label/icon/visibility/disabled/renderBody/layout operations as manifest-governed decisions. Do not substitute free JSON patches for these operations.
- Keep Settings Panel apply/save/reset/reopen aligned with runtime config consumption.
- Keep i18n for authoring chrome and assistant labels in the package i18n path.
- If a requested edit cannot be represented by the existing manifest or editor capability, classify whether it is `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato` before adding a contract.

## Validation

Use the smallest reliable proof for the touched surface:

- `ng build praxis-tabs` or the repo's equivalent focal build
- focused tabs specs for runtime selection, metadata, quick setup, widget events, lazy loading, and editor capability
- Settings Panel round-trip validation when config editor behavior changes
- AI registry or authoring manifest validation when `ai/**`, capabilities, manifest refs, or registry docs change
- docs/playground validation when public examples or docs are updated

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-navigation-containers-ai-validation` for tabs AI manifests, registry projection, context packs, assistant turns, and cross-container validation.
- Use `praxis-authoring-editors` for Settings Panel editor round-trip.
- Use `praxis-core-composition-runtime` for nested widgets, widget events, composition links, and dynamic page materialization.
- Use `praxis-angular-i18n-governance`, `praxis-angular-public-api-governance`, `praxis-angular-docs-playgrounds`, and `praxis-angular-validation-gates` when the change touches their governed areas.
