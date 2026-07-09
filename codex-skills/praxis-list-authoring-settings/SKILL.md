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

## Global Actions

List actions should use canonical `GlobalActionRef` shape:

`globalAction: { actionId, payload?, payloadExpr?, meta? }`

Use `getGlobalActionUiSchema(...)`, `preserveListGlobalActionRefPayload(...)`, and `withListGlobalActionPayload(...)` when editing structured payloads. Do not persist command strings such as `surface.open:...`, `navigate:...`, or `showAlert:...`.

## i18n

All editor chrome is framework-owned text. Section labels, helper text, placeholders, validation messages, empty states, tab names, action labels, and defaults must come from Praxis i18n catalogs where the lib already provides them. Domain labels inside item templates may remain host/schema data.

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
- visual/round-trip authoring changes: `test-dev/e2e/list-authoring-canonical.playwright.spec.ts` when browser proof is needed
- public docs/manifest impact: use `praxis-list-docs-evidence` and `praxis-list-ai-validation`

Report explicitly whether the editor was validated for open, edit, apply/save, reset, reopen, and runtime consume.
