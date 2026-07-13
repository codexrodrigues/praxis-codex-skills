---
name: praxis-settings-roundtrip-authoring
description: Use when implementing or auditing @praxisui/settings-panel or praxis-settings-panel package authoring editor round-trip for table, form, list, charts, page-builder, tabs, stepper, expansion, manual-form, CRUD, metadata-editor, or widget config editors, especially apply/save/reset/reopen/persistence/runtime-consume behavior.
---

# Praxis Settings Round-Trip Authoring

The `praxis-settings-*` skill family is the canonical Codex skill surface for `@praxisui/settings-panel` and `projects/praxis-settings-panel`; do not create parallel `praxis-settings-panel-*` guidance unless this family cannot express a proven contract gap.

Use this skill when a consumer editor is hosted by Settings Panel. The panel owns the shell protocol; the consumer lib owns the edited document semantics.

Resolve paths from `praxis-ui-angular/` unless another root is named.

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

## Required Source Audit

For shell protocol changes, inspect:

- `projects/praxis-settings-panel/AGENTS.md`
- `projects/praxis-settings-panel/docs/host-settings-panel-integration.md`
- `projects/praxis-settings-panel/src/lib/settings-panel.types.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.ref.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.component.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.component.html`
- `projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- `projects/praxis-settings-panel/src/public-api.ts`

For consumer round-trip changes, inspect the owning editor and at least one runtime consumer. Representative widget editors:

- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-table/src/lib/praxis-table-widget-config-editor.ts`
- `projects/praxis-crud/src/lib/praxis-crud-widget-config-editor.ts`
- `projects/praxis-tabs/src/lib/praxis-tabs-widget-config-editor.ts`
- `projects/praxis-stepper/src/lib/praxis-stepper-widget-config-editor.ts`
- `projects/praxis-expansion/src/lib/praxis-expansion-widget-config-editor.ts`

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
9. Missing optional blocks in a canonical document are treated according to the owning editor's
   semantics. For replace-all documents, omission may mean "clear this persisted block"; do not
   silently restore stale widget inputs or host defaults unless the owning contract declares merge
   behavior.

## Settings Panel Protocol

`SettingsValueProvider` is the hosted editor contract:

- `isDirty$`, `isValid$`, and `isBusy$` gate Apply/Save in the shell.
- `getSettingsValue()` is the Apply payload source.
- `onSave()` is the Save payload source when present.
- `onSave()` may return a value, `Promise`, or `Observable`.
- If `onSave()` resolves/emits `undefined`, the shell must not emit `saved$`.
- If `onSave()` is absent or returns `undefined` by omission, the fallback is `getSettingsValue()`.
- `reset()` is invoked only after reset confirmation and should restore the editor's intended baseline scope.
- `onBeforeClose(reason)` may return boolean, `Promise<boolean>`, or `Observable<boolean>` and can veto cancel/backdrop/esc/replacement.

`SettingsPanelRef` owns shell events:

- `apply(value)` emits `applied$` and keeps the panel open.
- `save(value)` emits `saved$` and closes with reason `save`.
- `reset()` emits `reset$`.
- `close(reason)` emits `closed$` and completes the streams.
- `DeferredSettingsPanelRef` preserves event streams when a new panel waits for the current panel to close before opening.

## Open, Replace, And Close

When `SettingsPanelService.open(...)` is called while another authoring panel is open:

- the current editor's `onBeforeClose('cancel')` is consulted first;
- if it returns `false`, the current panel remains open and the replacement ref closes with `cancel`;
- if close is allowed and the current editor is dirty, discard confirmation still applies;
- if close is allowed, the old panel closes with `cancel` and the new panel opens fresh.

Do not bypass this by disposing the overlay directly. Hosts and consumers should use `SettingsPanelService` or the canonical `SETTINGS_PANEL_BRIDGE`.

## Inputs And Widget Editors

Settings Panel injects inputs in two ways:

- Angular inputs are set only when declared by the hosted component.
- The original input envelope is also available through `SETTINGS_PANEL_DATA`.

For Page Builder/component widget config editors, the canonical pattern is:

- implement `SettingsValueProvider`;
- expose child editor dirty/valid/busy through the wrapper observables;
- initialize the child editor from widget `inputs`;
- `getSettingsValue()` returns `{ inputs: ... }` for preview/apply;
- `onSave()` returns the same canonical widget input envelope, usually by delegating to the child editor's `onSave()` or `getSettingsValue()`;
- `reset()` delegates to the child editor;
- preserve stable widget identity such as `widgetKey`, `componentInstanceId`, form/table/list ids, and binding context.

Do not persist editor-only authoring documents directly from a widget wrapper unless that document is the runtime input contract.
When a widget wrapper projects an owning editor document back into `{ inputs: ... }`, treat the
projection as host compatibility, not a second source of truth. If the child editor intentionally
clears a binding, context snapshot, action, layout block, query context, or other optional document
section, the wrapper must not rehydrate it from the original inputs by fallback unless that exact
fallback is part of the canonical owner contract.

## Diagnostics, Layout, And Runtime Separation

- `SettingsPanelConfig.diagnostics` controls status/disabled/busy/validation visibility only; it must not weaken Apply/Save gates.
- Authoring resize is enabled by default and persists by `persistSizeKey`, defaulting to `settings-panel:<id>`.
- `expanded: true` opens effectively expanded but must not persist the transient expanded width.
- Use `.praxis-settings-panel-pane` and `.praxis-settings-panel-backdrop` for authoring shell styling.
- Use `providePraxisSettingsPanelBridge()` for authoring through `SETTINGS_PANEL_BRIDGE`.
- Use the runtime surface drawer bridge for `surface.open` drawer presentation. Do not leak authoring footer/status semantics into runtime drawers.
- Runtime drawer values such as `context.surfaceRuntime`, `result$`, row selection envelopes,
  resolved surface state, or diagnostics visibility are not authoring round-trip payloads. If a user
  needs to author a connection to a runtime drawer, route that through the owning action/composition
  editor contract and persist that canonical action/composition shape, not Settings Panel shell state.

## Anti-Patterns

- Building per-component drawer/dialog shells because Settings Panel lacks a local convenience.
- Moving Apply/Save/Reset enablement into every editor.
- Persisting host wrappers instead of the owning component document or input patch.
- Creating a page-builder editor for another lib instead of consuming that lib's `configEditor`.
- Accepting JSON-only support for fields that enterprise users need in visual authoring.
- Subscribing only to `saved$` when the product promises live preview through `applied$`.
- Treating diagnostics visibility as permission to save invalid or busy editor state.
- Persisting runtime drawer context, `surfaceRuntime`, `result$` envelopes, or diagnostics output as
  component config.
- Rehydrating a cleared canonical document block from stale widget inputs after apply/save.
- Replacing an open panel without honoring `onBeforeClose` and dirty discard confirmation.
- Persisting transient expanded width as the user's preferred collapsed width.

## Validation

Use the owning lib's focused authoring specs plus Settings Panel checks when the shell protocol is touched:

- settings protocol:
  - `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts`
  - `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts`
  - `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- table: config editor, columns, filters, actions, rules, CRUD integration, widget config editor, and table authoring E2E where needed
- form: config/layout/behavior/rules/messages/hooks/actions/widget editor specs and form config editor E2Es when visual authoring paths change
- page-builder/visual-builder: config editor and persistence Playwrights when multi-step visual state matters
- CRUD/tabs/stepper/expansion/manual-form/charts/list: focused widget/config editor specs plus owning manifest specs when authoring delegation changes
- metadata-editor consumers: pair with `praxis-metadata-editor-consumer-bridges` when the hosted editor is `FieldMetadataEditorComponent`

State explicitly when no visual editor is affected and why.
