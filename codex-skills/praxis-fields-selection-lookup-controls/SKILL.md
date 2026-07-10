---
name: praxis-fields-selection-lookup-controls
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields selection controls: select, searchable-select, async-select, entityLookup, autoComplete, multiSelect, multiSelectTree, treeSelect, selectionList, transferList, chipInput, chipList, checkbox, radio, toggle/buttonToggle, inline select/autocomplete/async/entity/multi/tree controls, option identity, value/display fields, optionSource, selected-value reload, chips, and related AI profiles.
---

# Praxis Fields Selection Lookup Controls

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
- `src/lib/components/inline-entity-lookup/**`
- `src/lib/components/material-async-select/**`
- `src/lib/ai/select-controls-ai-capabilities.ts`
- `src/lib/ai/chips-controls-ai-capabilities.ts`
- `src/lib/ai/list-controls-ai-capabilities.ts`
- `src/lib/ai/tree-controls-ai-capabilities.ts`
- `src/lib/ai/toggle-controls-ai-capabilities.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
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
- `searchable-select`, `async-select`, and autocomplete need explicit search/load policy and clear value shape.
- Tree controls require stable node identity and parent/children semantics.
- Chips/list/transfer controls must preserve array value shape, order policy, and max-selection rules.
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

- component specs for affected select/lookup/chips/list/tree controls;
- `option-store` and option-source specs when option loading or identity changes;
- metadata/editorial/catalog specs when discovery changes;
- AI profile/catalog specs when assistant guidance changes;
- selected reload/reopen tests for remote/entity options;
- Playwright for inline selection overlays, multi-select draft behavior, and contrast.
- direct consumer checks when a selection control is exposed through dynamic-form, metadata-editor, table filter, CRUD, or a host example.

State which runtime, option identity, selected reload, editor/tooling, AI profile, and overlay checks were run.
