---
name: praxis-settings-roundtrip-authoring
description: Use when implementing or auditing @praxisui/settings-panel or praxis-settings-panel package authoring editor round-trip for table, form, list, charts, page-builder, tabs, stepper, expansion, manual-form, CRUD, metadata-editor, or widget config editors, especially apply/save/reset/reopen/persistence/runtime-consume behavior.
---

# Praxis Settings Round-Trip Authoring

The `praxis-settings-*` skill family is the canonical Codex skill surface for `@praxisui/settings-panel` and `projects/praxis-settings-panel`; do not create parallel `praxis-settings-panel-*` guidance unless this family cannot express a proven contract gap.

Use this skill when a consumer editor is hosted by Settings Panel. The panel owns the shell protocol; the consumer lib owns the edited document semantics.

## Canonical Chain

Every authoring change must preserve:

`runtime config -> editor state -> SettingsValueProvider value -> applied/saved payload -> persistence -> reopen/reload -> runtime consume`

Do not treat "the field is visible" or "JSON can edit it" as enough. A semantic config field is complete only when visual editor, apply, save, reset, reopen, and runtime interpretation agree.

## Owner Decision

- Shell, footer, close, resize, diagnostics: `@praxisui/settings-panel`.
- Table config document: `@praxisui/table`.
- Dynamic form authoring document: `@praxisui/dynamic-form`.
- List, charts, page-builder, tabs, stepper, expansion, manual-form, CRUD: the owning lib.
- Component input editors for widgets: owning component via `ComponentDocMeta.configEditor`, not a host-local editor.
- Persistence storage: normally `praxis-config-starter` or the host's declared config storage contract.

If the owner is unclear, do not create a host workaround; map the canonical document and runtime consumer first.

## Required Round-Trip Checks

For each editable path, prove or inspect:

1. Existing persisted/current config opens with the correct value.
2. Editor UI changes the canonical path, not an editor-only alias.
3. `getSettingsValue()` and `onSave()` emit the expected document or patch shape.
4. `applied$` updates preview/runtime without closing when supported.
5. `saved$` persists the same canonical shape.
6. `reset()` returns only the intended scope to baseline.
7. Reopen reloads the value without silent normalization drift.
8. Runtime consumes the saved/applied value without hidden adapters.

## Anti-Patterns

- Building per-component drawer/dialog shells because Settings Panel lacks a local convenience.
- Moving Apply/Save/Reset enablement into every editor.
- Persisting host wrappers instead of the owning component document or input patch.
- Creating a page-builder editor for another lib instead of consuming that lib's `configEditor`.
- Accepting JSON-only support for fields that enterprise users need in visual authoring.

## Validation

Use the owning lib's focused authoring specs plus Settings Panel checks when the shell protocol is touched:

- table: config editor, columns, filters, actions, rules, CRUD integration, and table authoring E2E where needed
- form: config/layout/behavior/rules/messages/hooks/actions/widget editor specs
- page-builder/visual-builder: config editor and persistence Playwrights when multi-step visual state matters
- settings protocol: `SettingsValueProvider`, open editor, apply/save/reset, and reopen specs

State explicitly when no visual editor is affected and why.
