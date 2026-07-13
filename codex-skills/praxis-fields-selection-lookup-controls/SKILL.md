---
name: praxis-fields-selection-lookup-controls
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields or praxis-dynamic-fields package selection controls: select, searchable-select, async-select, entityLookup, autoComplete, multiSelect, multiSelectTree, treeSelect, selectionList, transferList, chipInput, chipList, checkbox, radio, toggle/buttonToggle, inline select/autocomplete/async/entity/multi/tree controls, option identity, value/display fields, optionSource, selected-value reload, chips, and related AI profiles.
---

# Praxis Fields Selection Lookup Controls

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill for option-bearing and lookup controls in `@praxisui/dynamic-fields`. These controls are grounded by option identity and source semantics; they must not be reduced to labels, local arrays, or host-only search widgets.

Pair it with:

- `praxis-fields-option-sources` for backend option sources, `RESOURCE_ENTITY`, cascades, by-ids reload, dependency maps, and selected reload policies.
- `praxis-fields-runtime-loader` for runtime registration and loader behavior.
- `praxis-fields-editorial-discovery` for metadata, catalog, descriptors, JSON API docs, and selection guidance.
- `praxis-fields-inline-overlay-runtime` for compact inline select/multi-select/autocomplete/lookup overlay behavior.
- `praxis-fields-control-profile-ai` for AI profiles such as select, entity lookup, tree select, list transfer, toggle, and chips-related capabilities.
- `praxis-resource-entity-lookup-backend` when backend entity lookup contracts change.

## Source Audit

Inspect:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `README.md`
- `docs/dynamic-fields-field-catalog.md`
- `docs/dynamic-fields-field-selection-guide.md`
- `docs/dynamic-fields-inline-filter-runtime-contract.md`
- selection component folders under `src/lib/components/**`
- selection `*.metadata.ts` and `*.json-api.md`
- `src/lib/base/option-store.ts`
- `src/lib/base/simple-base-select.component.ts`
- `src/lib/services/option-display-resolver.service.ts`
- `src/lib/components/inline-entity-lookup/**`
- `src/lib/components/material-select/**`
- `src/lib/components/material-searchable-select/**`
- `src/lib/components/material-async-select/**`
- `src/lib/components/material-autocomplete/**`
- `src/lib/components/material-multi-select/**`
- `src/lib/components/material-multi-select-tree/**`
- `src/lib/components/material-tree-select/**`
- `src/lib/components/material-selection-list/**`
- `src/lib/components/material-transfer-list/**`
- `src/lib/components/material-chips/**`
- `src/lib/components/material-checkbox-group/**`
- `src/lib/components/material-radio-group/**`
- `src/lib/components/material-slide-toggle/**`
- `src/lib/components/material-button-toggle/**`
- inline selection folders such as `inline-select`, `inline-searchable-select`, `inline-async-select`, `inline-autocomplete`, `inline-multi-select`, and `inline-tree-select`
- `src/lib/ai/select-controls-ai-capabilities.ts`
- `src/lib/ai/chips-controls-ai-capabilities.ts`
- `src/lib/ai/list-controls-ai-capabilities.ts`
- `src/lib/ai/tree-controls-ai-capabilities.ts`
- `src/lib/ai/toggle-controls-ai-capabilities.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts` and spec
- `src/lib/editorial/wave1/material-select.editorial.ts`
- `src/lib/editorial/wave1/entity-lookup.editorial.ts`
- `src/lib/editorial/wave1/material-slide-toggle.editorial.ts`
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts` and catalog specs
- `projects/praxis-core/src/lib/helpers/field-definition-mapper.ts` and spec when optionSource metadata is normalized from backend/schema
- `projects/praxis-core/src/lib/services/schema-normalizer.service.ts` and spec when `x-ui` optionSource, value/display fields, cascades, or entity lookup contracts change
- option-source and component specs

## Canonical Families

- Simple selection: `select`, `radio`, `checkbox`, `buttonToggle`, `toggle`.
- Search/remote: `searchable-select`, `async-select`, `autoComplete`, `entityLookup`.
- Multiple/list/tree: `multiSelect`, `multiSelectTree`, `treeSelect`, `selectionList`, `transferList`, `chipInput`, `chipList`.
- Inline selection: `inlineSelect`, `inlineSearchableSelect`, `inlineAsyncSelect`, `inlineEntityLookup`, `inlineAutocomplete`, `inlineMultiSelect`, `inlineTreeSelect`, plus specialized inline status/sentiment/color label controls when used as selections.

## Runtime Rules

- Preserve value identity. Display labels are not persisted identity unless the canonical option contract says so.
- Prefer `optionSource` for remote/entity-backed data and local `options` only for genuinely local lists.
- `entityLookup` should use canonical `RESOURCE_ENTITY` semantics, stable value/display paths, by-ids rehydration when required, dependency maps, and selection policy.
- Selected-value reload must use by-ids/display paths when the source requires it; do not fake hydration with generic filter calls.
- Selected display outside the open panel should route through `OptionDisplayResolverService`, `OptionStore`, or the owning select component path; do not persist labels as a shortcut for display.
- Legacy `valueField`/`displayField` must be normalized toward canonical option identity/display keys through the core mapper/normalizer; do not create a second alias layer in the component.
- `searchable-select`, `async-select`, and autocomplete need explicit search/load policy and clear value shape.
- Tree controls require stable node identity and parent/children semantics.
- Chips/list/transfer controls must preserve array value shape, order policy, and max-selection rules.
- Toggle/radio/checkbox/button-toggle controls are still option-bearing when labels, values, disabled states, or i18n are derived from metadata; do not treat them as plain booleans unless the control contract is boolean.
- Inline selection overlays use `inlineOverlay` when selections are drafted before commit.
- Dynamic Form, metadata-editor, table filters, CRUD dialogs, and host projects should consume the same identity/source contract. Do not fork lookup behavior per consumer.

## Inventory Before New Contract

- `ja-suportado-so-ux`: options/source identity exists but UI, labels, selected display, empty state, or docs are weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host-local option arrays, display labels, aliases, or search endpoints duplicate canonical `optionSource`, value/display fields, or entity lookup semantics.
- `suportado-parcialmente`: runtime renders but selected reload, cascade dependency, metadata-editor coverage, AI profile, catalog, or inline overlay behavior is incomplete.
- `lacuna-real-de-contrato`: no current control type, option source contract, value identity, by-ids reload path, metadata path, profile, or validator can express the selection decision.

Only real gaps justify new metadata or backend contracts. Most select/lookup bugs should complete the existing option-source and profile chain.

## Validation

Use focused gates:

- Base option loading, display, selected reload, or identity changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/base/option-store.spec.ts --include=projects/praxis-dynamic-fields/src/lib/base/simple-base-select.component.spec.ts`
  - Add the focused spec for `OptionDisplayResolverService` when one exists or create it with the behavior change; selected display/rehydration should not remain untested.
- Simple/search/remote/entity selection controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/material-select/material-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-searchable-select/material-searchable-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-async-select/material-async-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-autocomplete/material-autocomplete.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-select/inline-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-searchable-select/inline-searchable-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-async-select/inline-async-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-autocomplete/inline-autocomplete.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-entity-lookup/inline-entity-lookup.component.spec.ts`
- Multi/list/tree/chips controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/material-multi-select/material-multi-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-multi-select-tree/material-multi-select-tree.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-tree-select/material-tree-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-tree-select/inline-tree-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-multi-select/inline-multi-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-selection-list/material-selection-list.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-transfer-list/material-transfer-list.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-chips/material-chips.component.spec.ts`
- Toggle/radio/checkbox/button toggle controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/material-checkbox-group/material-checkbox-group.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-radio-group/material-radio-group.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-slide-toggle/material-slide-toggle.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-button-toggle/material-button-toggle.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-toggle/inline-toggle.component.spec.ts`
- Registry/loader changes:
  - Run the focused gates from `praxis-fields-runtime-loader`, especially `component-registry.service.spec.ts` when a selection `controlType` is added or remapped.
- Core metadata normalization, optionSource, `RESOURCE_ENTITY`, cascades, value/display fields, or by-ids changes:
  - `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/helpers/field-definition-mapper.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer-array.service.spec.ts`
- Metadata/editorial/catalog discovery changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts`
- AI profile/catalog changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts`
- Selected reload/reopen tests for remote/entity options:
  - Include the relevant component spec plus `option-store`/display resolver proof; add regression coverage before relying on manual QA.
- Playwright for inline selection overlays, multi-select draft behavior, lookup UX, and contrast:
  - `projects/praxis-dynamic-fields/test-dev/e2e/entity-lookup-procurement.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/entity-lookup-funcionarios.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-searchable-select-panel-ux.playwright.spec.ts`
  - `projects/praxis-dynamic-fields/test-dev/e2e/inline-all-components-smoke.playwright.spec.ts`
- Direct consumer checks when a selection control is exposed through dynamic-form, metadata-editor, table filter, CRUD, or a host example.
- `npm run build:praxis-dynamic-fields` when public exports, metadata contracts, AI profiles, or package-owned control coverage changes.

State which runtime, option identity, selected reload, editor/tooling, AI profile, and overlay checks were run.
