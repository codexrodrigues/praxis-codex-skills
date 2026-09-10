---
name: praxis-list-authoring-settings
description: Use when creating, changing, or auditing `@praxisui/list` authoring surfaces: list config editor, widget config editor, JSON config editor, Settings Panel integration, `ListAuthoringDocument`, `SettingsValueProvider`, apply/save/reset/reopen, template/action/selection/skin editors, i18n chrome, and runtime/editor parity.
---

# Praxis List Authoring Settings

Use this skill for visual authoring of `@praxisui/list`. A list config editor change is complete only when the canonical document, editor UI, Settings Panel payload, persistence, reopen, and runtime interpretation remain coherent.

Use `praxis-authoring-editors` for shared editor rules, `praxis-settings-roundtrip-authoring` for drawer round-trip, and `praxis-angular-i18n-governance` for internal authoring text.

## Required Source Audit

Inspect:

- `projects/praxis-list/AGENTS.md`
- `src/lib/editors/list-config-editor.component.ts`
- `src/lib/editors/list-widget-config-editor.component.ts`
- `src/lib/editors/json-config-editor.component.ts`
- `src/lib/list-editor-document.model.ts`
- `src/lib/list-editor-capability.ts`
- `src/lib/list-global-action-adapter.ts`
- `src/lib/i18n/list.i18n.ts`, `list.pt-BR.ts`, and `list.en.ts`
- `src/lib/editors/*.spec.ts`
- `src/lib/list-editor-capability.spec.ts`
- `test-dev/e2e/list-authoring-canonical.playwright.spec.ts`

## Canonical Authoring Chain

The root `@praxisui/list` API includes `PraxisListConfigEditor`,
`PraxisListWidgetConfigEditor`, `PraxisListWidgetEditorInputs` and
`PraxisListWidgetEditorValue`. Preserve these published owner-local imports.
Generic hosts resolve the widget editor with
`PRAXIS_LIST_COMPONENT_METADATA.configEditor.loadComponent`; asynchronous
resolution does not promise a separate downloaded chunk when the classes are
also statically exported. Before changing this boundary, use
`praxis-angular-public-api-governance`, compare the published package, and run
`src/lib/list-public-api.spec.ts` plus an owning/direct-consumer package build.
Do not remove the interfaces to optimize runtime loading: type-only exports
have no executable cost. A metadata loader alone does not migrate direct imports.

Preserve:

`PraxisListConfig -> ListAuthoringDocument(kind='praxis.list.editor', version=1) -> editor state -> SettingsValueProvider.getSettingsValue/onSave -> persisted config -> reopen -> PraxisList runtime`

The editor may hydrate or normalize a legacy config, but the save/apply output must be the canonical list config shape consumed by runtime. Do not create host-only wrappers for list settings.

## Editor Coverage

When the task touches a config path, verify whether it is:

- reachable in `list-config-editor`
- reachable in `list-widget-config-editor` if used by widget hosts/Page Builder
- preserved by `json-config-editor`
- represented by `ListAuthoringDocument`
- validated by `validateListAuthoringDocument`
- projected by `projectListAuthoringDocument`
- covered by focused editor specs
- represented in AI manifest if authorable by assistant

JSON-only support is incomplete for frequently edited paths such as templating, actions, selection, skin, data binding, export, localization, and accessibility.

For `surface.open` actions, aggregate mounted child raw-draft validity with the main JSON,
query and document validators. Invalid-only text is dirty, blocks Apply/Save, survives unrelated
tab visits, and is discarded only by explicit Reset/Cancel. Track contributors by mounted editor
identity rather than mutable labels or indices; do not rewrite the main JSON editor from a
validation-only notification or remove an action while its unresolved draft would be lost.

## Global Actions

List actions should use canonical `GlobalActionRef` shape:

`globalAction: { actionId, payload?, payloadExpr?, meta? }`

Use `getGlobalActionUiSchema(...)`, `preserveListGlobalActionRefPayload(...)`, and `withListGlobalActionPayload(...)` when editing structured payloads. Do not persist command strings such as `surface.open:...`, `navigate:...`, or `showAlert:...`.

## i18n

All editor chrome is framework-owned text. Section labels, helper text, placeholders, validation messages, empty states, tab names, action labels, and defaults must come from Praxis i18n catalogs where the lib already provides them. Domain labels inside item templates may remain host/schema data.

Author `configPersistenceStrategy` explicitly, including `volatile` for
transient/public documents. Collection toolbar controls, filters, actions,
selection, responsive row slots, and feature templates round-trip through the
List owner document/editor; do not persist runtime-discovered links or
capabilities as config.

## Standalone Save Boundary

`PraxisList.openConfigEditorPanel` supplies an owner-local `persistSettings` callback
through `SETTINGS_PANEL_DATA` and binds the panel to the List `DestroyRef` owner.
Destroying the owner closes its panel without Save; late responses cannot publish
into the destroyed target. The config editor awaits persistence in `onSave()` before
Settings Panel emits `saved$` and closes. The host validates/projects the authoring
document, checks its storage target, and awaits `ASYNC_CONFIG_STORAGE.saveConfig`.
The subsequent `saved$` consumes the accepted config without a second storage write.
`volatile` completes locally; a widget editor without this callback retains its
local value-returning protocol. Do not move remote persistence into an unawaited
`saved$` subscription or swallow storage errors.

Run `src/lib/components/praxis-list.editor-persistence.spec.ts` with the real editor,
Settings Panel and a controlled storage response. Prove rejection, draft retention,
retry, single write, stale-response suppression, volatile mode and reopen/runtime
consumption. This adapter test is not an HTTP/backend durability certificate.

## Runtime Parity

Do not make the editor present declared-only fields as active runtime features. If the editor exposes `virtualScroll`, `stickySectionHeader`, `events.*`, `emitPayload`, `highContrast`, or `reduceMotion`, label or validate the limitation consistently with README/json-api docs and AI manifest warnings.

When promoting a declared-only path to runtime-active, update runtime, editor, manifest, docs, examples, and validation in the same cycle.

## Validation

Minimum useful gates:

- config editor changes: `src/lib/editors/list-config-editor.component.spec.ts`
- widget editor changes: `src/lib/editors/list-widget-config-editor.component.spec.ts`
- JSON editor changes: `src/lib/editors/json-config-editor.component.spec.ts`
- authoring document/projection changes: `src/lib/list-editor-capability.spec.ts`
- global action changes: `src/lib/list-global-action-adapter.spec.ts`
- surface action drafts: mount the Core Surface editor and prove invalid text, tab preservation,
  correction, independent contributors, removal guard and Reset through the List owner.
- visual/round-trip authoring changes: `test-dev/e2e/list-authoring-canonical.playwright.spec.ts` when browser proof is needed
- public docs/manifest impact: use `praxis-list-docs-evidence` and `praxis-list-ai-validation`

Report explicitly whether the editor was validated for open, edit, apply/save, reset, reopen, and runtime consume.
