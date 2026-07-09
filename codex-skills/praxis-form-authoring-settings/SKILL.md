---
name: praxis-form-authoring-settings
description: Use when Codex must work on @praxisui/dynamic-form authoring, Settings Panel integration, config editor, layout editor, behavior editor, rules editor, messages editor, hooks editor, actions editor, JSON config editor, widget config editor, apply/save/reset, DynamicFormAuthoringDocument, schema preferences, presentation snapshots, or runtime/editor round-trip.
---

# Praxis Form Authoring Settings

Use this skill for Dynamic Form authoring and Settings Panel flows. A change is incomplete when runtime config works but the visual editor cannot show, edit, apply, save, reset, reopen, or round-trip the same semantics.

## Source Audit

Inspect the authoring surface:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/config-editor/**`
- `projects/praxis-dynamic-form/src/lib/layout-editor/**`
- `projects/praxis-dynamic-form/src/lib/behavior-editor/**`
- `projects/praxis-dynamic-form/src/lib/rules-editor/**`
- `projects/praxis-dynamic-form/src/lib/messages-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/json-config-editor/**`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/settings-panel.providers.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-document.model.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`

Also inspect `projects/praxis-settings-panel/AGENTS.md` when changing `SettingsValueProvider`, drawer data, `apply`, `save`, `reset`, or persisted config.

## Authoring Document Rules

`DynamicFormAuthoringDocument` is the canonical complete authoring snapshot:

- `config` replaces the previous config.
- `bindings` replaces previous persistible bindings.
- missing `bindings.mode` clears the persisted mode binding.
- `contextSnapshot` replaces previous persisted authoring context.
- missing `backConfig`, `presentation`, or `schemaPrefs` inside `contextSnapshot` explicitly removes that block.
- runtime discovery values such as `schemaUrl`, `submitUrl`, and `submitMethod` are diagnostics only and must not be persisted into bindings or context snapshot.

Legacy partial adapter APIs can keep merge compatibility, but canonical editor apply/save is replace-all.

## Editor Round-Trip Checklist

For every config or context change, prove or inspect:

1. Existing config/document opens in the editor with the correct value.
2. The user can change it through the canonical editor surface.
3. Apply/save emits the expected `DynamicFormAuthoringDocument` or config shape.
4. Runtime reflects the applied change.
5. Reopening the editor preserves the value.
6. Reset removes only the intended config, bindings, or context snapshot.

If no visual editor is affected, state why.

## Editor Rules

- Keep `fieldMetadata` patches deep-merged where needed, especially `entityLookup.optionSource`, so editor changes do not erase canonical lookup contracts.
- Keep rules, messages, hooks, actions, behavior, hints, schema preferences, navigation, presentation, and JSON editor in sync.
- Keep authoring text in the dynamic-form i18n catalog; do not add visible hardcoded strings.
- Do not create component-specific local editors in a host when `ComponentDocMeta.configEditor` or the owning Dynamic Form editor should handle it.
- Treat `Apply` working without `Save`, or `Save` working without reopen, as incomplete.

## Validation

- config editor: `config-editor/*.spec.ts`, cascade integration, JSON editor specs
- Settings Panel/document semantics: editor capability specs, authoring protocol specs, widget config editor specs
- rules/messages/hooks/actions: focused editor specs plus relevant E2E when UI behavior changes
- browser authoring: Playwrights such as `form-config-editor-smoke`, `layout`, `rules`, `messages`, `hooks`, `actions`, `behavior`, `json`, `hints`, and `cascades`

## Companion Skills

- Use `praxis-authoring-editors` for cross-component Settings Panel and round-trip guidance.
- Use `praxis-form-runtime-submit` when authoring changes runtime construction, submit behavior, field metadata, or resource contracts.
- Use `praxis-form-layout-canvas` for layout editor, visual blocks, canvas, schema-driven layout policy, and presentation.
- Use `praxis-form-ai-rules-validation` for AI component edit plans, rules, diagnostics, and registry ingestion.
- Use `praxis-dynamic-fields-editorial` for field component coverage and metadata editor chains.
