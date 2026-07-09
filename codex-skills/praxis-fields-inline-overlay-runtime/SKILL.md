---
name: praxis-fields-inline-overlay-runtime
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields inline filter controls and overlays: inline* controlTypes, praxis-filter promotion, inlineOverlay.applyMode auto/explicit, apply/cancel/clear actions, draft versus committed value, overlay/panel tokens, CDK layer issues, clearButton, inlineAutoSize, inline context tooltips, compact toolbar value shapes, and inline filter docs/catalogs.
---

# Praxis Fields Inline Overlay Runtime

Use this skill for compact inline filter controls in `@praxisui/dynamic-fields`. Inline controls are package-owned compact field renderers with a runtime/filter contract; they are not default form controls unless the authoring context is explicitly filter-focused.

Pair it with:

- `praxis-fields-runtime-loader` for registry, loader, selector, and hot metadata behavior.
- `praxis-dynamic-fields-editorial` and `praxis-fields-editorial-discovery` for inline catalog, descriptors, docs, and tooling discovery.
- `praxis-fields-control-profile-ai` when AI profiles or inline recipes need to understand overlay behavior.
- `praxis-fields-text-number-time-controls` for text, numeric, currency, date, time, period, and range value shapes.
- `praxis-fields-selection-lookup-controls` for select, async select, autocomplete, entity lookup, multi-select, tree, and chips behavior.
- `praxis-table-runtime-data` or table/filter skills when the issue is `praxis-filter` promotion or emitted filter payloads.

## Source Audit

Inspect:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `README.md`
- `docs/dynamic-fields-inline-filter-runtime-contract.md`
- `docs/dynamic-fields-inline-components-guide.md`
- `docs/dynamic-fields-inline-filter-catalog.md`
- `docs/dynamic-fields-inline-filter-selection-guide.md`
- `src/lib/components/inline-*/**`
- `src/lib/services/component-registry/component-registry.service.ts`
- `projects/praxis-core/src/lib/utils/inline-filter-controls.util.ts`
- focused inline component specs and `test-dev/e2e/*.playwright.spec.ts` when visual overlay behavior changes

## Canonical Boundary

Dynamic Fields owns:

- canonical `inline*` control types and runtime components;
- package-owned `--pdx-inline-field-*` and `--pdx-inline-panel-*` tokens;
- inline field density, pill states, clear button behavior, context tooltip behavior, and component-level value shape;
- `inlineOverlay.applyMode` and action metadata consumed by inline panels.

`praxis-filter` owns when generic controls are promoted to inline variants in filter toolbars. Backend metadata/range normalizers own the final HTTP payload shape.

## Inline Overlay Rules

- Use `inlineOverlay.applyMode: "auto"` for simple, reversible, single-step interactions.
- Use `inlineOverlay.applyMode: "explicit"` when a panel has draft state: ranges, multi-selection, presets, sliders, exploratory visual choices, or complex remote lookup.
- In explicit mode, Apply commits, Cancel/Escape/outside close restores the last committed value, and Clear is distinct from Cancel.
- Do not add local `confirm`, `commitPolicy`, or per-component Apply/Cancel contracts when `inlineOverlay.actions.apply|cancel|clear` can represent the workflow.
- Keep `clearButton` as rendering/runtime metadata. It is not backend payload.
- Do not document component internal value shape as the final HTTP DTO; range normalization may happen later in host/backend contracts.
- Fix blocked overlays through shared layer/token contracts before adding host-only z-index or color overrides.

## Inventory Before New Contract

- `ja-suportado-so-ux`: the inline component or overlay contract exists but the chip, panel, tooltip, action, or docs do not make it clear.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a component uses local Apply/Cancel flags, local z-indexes, or host CSS where `inlineOverlay`, tokens, or shared CDK layers already carry the semantics.
- `suportado-parcialmente`: runtime works but filter promotion, value shape docs, e2e overlay behavior, AI profile, or catalog discovery is incomplete.
- `lacuna-real-de-contrato`: no `inline*` control, overlay action contract, token, value shape, promotion rule, or docs/cata­log path can represent the needed compact interaction.

Only real gaps justify new public metadata. Prefer completing `inlineOverlay` support before creating per-control contracts.

## Validation

Use focused gates:

- relevant `inline-*` component specs;
- `dynamic-field-loader` and `ComponentRegistryService` specs when control resolution changes;
- inline filter recipe/catalog specs when discovery changes;
- Playwright/e2e for overlay clickability, close behavior, Apply/Cancel/Clear, and theme contrast;
- table/filter payload validation when promotion or submitted filter DTO changes;
- build `praxis-dynamic-fields` for public API or exported contract changes.

State which overlay behavior, visual contrast, registry, docs/catalog, and payload checks were run.
