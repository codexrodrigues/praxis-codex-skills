---
name: praxis-fields-inline-overlay-runtime
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields or praxis-dynamic-fields package inline filter controls and overlays: inline* controlTypes, praxis-filter promotion, inlineOverlay.applyMode auto/explicit, apply/cancel/clear actions, draft versus committed value, overlay/panel tokens, CDK layer issues, clearButton, inlineAutoSize, inline context tooltips, compact toolbar value shapes, and inline filter docs/catalogs.
---

# Praxis Fields Inline Overlay Runtime

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

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
- `docs/dynamic-fields-inline-filter-custom-component-guide.md`
- `docs/dynamic-fields-inline-filter-catalog.md`
- `docs/dynamic-fields-inline-filter-inventory.md`
- `docs/dynamic-fields-inline-filter-selection-guide.md`
- `docs/dynamic-fields-inline-filter-troubleshooting.md`
- `src/lib/components/inline-*/**`
- `src/lib/components/material-date-range/date-range-shortcuts-overlay.component.ts`
- `src/lib/utils/inline-display-mask.util.ts` and spec
- `src/lib/i18n/dynamic-fields.i18n.ts`
- `src/lib/i18n/dynamic-fields.en-US.ts`
- `src/lib/i18n/dynamic-fields.pt-BR.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.recipes.ts`
- `src/lib/catalog/catalog-derivation.spec.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.spec.ts`
- `src/lib/ai/inline-filter-recipes.spec.ts`
- `src/lib/ai/control-type-ai-catalog.ts` and spec
- `src/lib/services/component-registry/component-registry.service.ts`
- `src/lib/directives/dynamic-field-loader.directive.ts`
- `src/lib/directives/dynamic-field-loader.presentation-mode.spec.ts`
- `src/lib/directives/dynamic-field-loader-global-states.spec.ts`
- `src/lib/directives/dynamic-field-loader.metadata-refresh.spec.ts`
- `src/lib/directives/dynamic-field-loader.select-rebind.spec.ts`
- `src/lib/directives/dynamic-field-loader.skip-snapshot.spec.ts`
- `projects/praxis-core/src/lib/utils/inline-filter-controls.util.ts`
- focused inline component specs and `test-dev/e2e/*.playwright.spec.ts` when visual overlay behavior changes

## Canonical Boundary

Dynamic Fields owns:

- canonical `inline*` control types and runtime components;
- package-owned `--pdx-inline-field-*` and `--pdx-inline-panel-*` tokens;
- inline field density, pill states, clear button behavior, context tooltip behavior, and component-level value shape;
- `inlineOverlay.applyMode` and action metadata consumed by inline panels.
- overlay action labels, aria labels, and shared inline copy through dynamic-fields i18n catalogs.

`praxis-filter` owns when generic controls are promoted to inline variants in filter toolbars. Backend metadata/range normalizers own the final HTTP payload shape.

## Inline Overlay Rules

- Use `inlineOverlay.applyMode: "auto"` for simple, reversible, single-step interactions.
- Use `inlineOverlay.applyMode: "explicit"` when a panel has draft state: ranges, multi-selection, presets, sliders, exploratory visual choices, or complex remote lookup.
- In explicit mode, Apply commits, Cancel/Escape/outside close restores the last committed value, and Clear is distinct from Cancel.
- Do not add local `confirm`, `commitPolicy`, or per-component Apply/Cancel contracts when `inlineOverlay.actions.apply|cancel|clear` can represent the workflow.
- Keep `clearButton` as rendering/runtime metadata. It is not backend payload.
- Keep overlay labels and aria strings in dynamic-fields i18n catalogs; do not hardcode Apply/Cancel/Clear per inline component.
- Use `inline-display-mask` for display-only compact summaries. It must not mutate the committed value shape.
- Presentation mode, skip snapshot, metadata refresh, select rebind, and global disabled/readonly/loading states must remain compatible with inline overlays.
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

- Inline scalar/temporal/range component changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/inline-input/inline-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-number/inline-number.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-currency/inline-currency.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-currency-range/inline-currency-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-range-slider/inline-range-slider.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-date/inline-date.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-date-range/inline-date-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-time/inline-time.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-time-range/inline-time-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-period-range/inline-period-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-month-range/inline-month-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-year-range/inline-year-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-relative-period/inline-relative-period.component.spec.ts`
- Inline selection/lookup component changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/inline-select/inline-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-searchable-select/inline-searchable-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-async-select/inline-async-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-autocomplete/inline-autocomplete.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-entity-lookup/inline-entity-lookup.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-multi-select/inline-multi-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-tree-select/inline-tree-select.component.spec.ts`
- Inline visual/status component changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/inline-color-label/inline-color-label.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-sentiment/inline-sentiment.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-pipeline-status/inline-pipeline-status.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-rating/inline-rating.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-distance-radius/inline-distance-radius.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-score-priority/inline-score-priority.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-toggle/inline-toggle.component.spec.ts`
- Shared display mask, registry, loader, metadata refresh, presentation mode, global states, or rebind behavior:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/utils/inline-display-mask.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/services/component-registry/component-registry.service.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.directive.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.presentation-mode.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader-global-states.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.metadata-refresh.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.select-rebind.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.skip-snapshot.spec.ts`
- Inline docs/catalog/AI/profile discovery changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/inline-filter-recipes.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts`
- I18n/action label changes:
  - Pair affected inline component specs with `metadata-i18n-contract.spec.ts` when catalog/editorial text changes.
- Playwright/e2e for overlay clickability, close behavior, Apply/Cancel/Clear, responsive layout, and theme contrast:
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-all-components-smoke.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-date-range-visual.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-date-range-business-shortcuts.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-searchable-select-panel-ux.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-layout-overflow.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-visual-states-design.playwright.spec.ts`
- Table/filter payload validation when promotion or submitted filter DTO changes.
- `npm run build:praxis-dynamic-fields` for public API, metadata, token, i18n, or exported contract changes.

State which overlay behavior, visual contrast, registry, docs/catalog, and payload checks were run.
