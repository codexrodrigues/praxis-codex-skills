---
name: praxis-table-authoring-settings
description: Use when Codex must work on @praxisui/table authoring, Settings Panel integration, config editors, columns editor, behavior editor, filter settings editor, toolbar actions editor, rules editor, CRUD integration editor, value mapping, visual formula builder, JSON config editor, apply/save/reset, or runtime/editor round-trip.
---

# Praxis Table Authoring Settings

Use this skill for table authoring and Settings Panel flows. A table change is incomplete when runtime config works but the visual editor cannot show, edit, apply, save, reset, reopen, or round-trip the same semantics.

## Source Audit

Inspect the real authoring surface:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/praxis-table-config-editor.ts`
- `projects/praxis-table/src/lib/praxis-table-config-editor.html`
- `projects/praxis-table/src/lib/praxis-table-widget-config-editor.ts`
- `projects/praxis-table/src/lib/table-editor-document.model.ts`
- `projects/praxis-table/src/lib/table-editor-capability.ts`
- `projects/praxis-table/src/lib/columns-config-editor/**`
- `projects/praxis-table/src/lib/behavior-config-editor/**`
- `projects/praxis-table/src/lib/filter-settings/**`
- `projects/praxis-table/src/lib/toolbar-actions-editor/**`
- `projects/praxis-table/src/lib/rules-editor/**`
- `projects/praxis-table/src/lib/crud-integration-editor/**`
- `projects/praxis-table/src/lib/value-mapping-editor/**`
- `projects/praxis-table/src/lib/visual-formula-builder/**`
- `projects/praxis-table/src/lib/json-config-editor/**`
- `projects/praxis-table/src/lib/i18n/table-editor.i18n.ts`
- `projects/praxis-table/docs/table-authoring-document-completeness-checklist.md`
- `projects/praxis-table/docs/visual-rules-editor-transition.md`

Also inspect `projects/praxis-settings-panel/AGENTS.md` and the Settings Panel bridge when the change touches `SettingsValueProvider`, drawer data, `apply`, `save`, `reset`, or persisted config.

## Authoring Rules

- Keep the canonical pair `runtime/config <-> editor` in sync.
- Test sparse host configurations and compare the entire persisted document after a single-field edit. Editor defaults must remain transient for untouched settings; action label edits must not author export, row-action or layout defaults. Reuse the Table internal initial/edited projection merge (`table-authoring-changes.ts`) rather than replacing complete config groups. Preserve coupled semantics when explicitly selected, such as hybrid row-action behavior.
- `PraxisTableConfigEditor` implements `SettingsValueProvider`; preserve `isDirty$`, `isValid$`, `isBusy$`, `getSettingsValue`, and apply/save/reset behavior.
- Treat `resourcePath`, `idField`, schema hash, local-data mode, and CRUD context as governed authoring state. Do not silently drop them when normalizing config.
- For columns, always validate runtime rendering, editor visibility, order, type/format, renderer, computed expressions, value mapping, conditional styles, sticky state, and headers.
- For filters, keep `behavior.filtering.advancedFilters.settings` synchronized with `FilterSettingsComponent`.
- For rules and formulas, preserve the rule compiler/operator registry and do not reintroduce prohibited old Visual Builder dependencies.
- For actions, preserve global action validation and effect shapes.
- For `surface.open` actions, combine mounted child raw-draft validity with Table document and
  main JSON validation. Invalid-only text must count as dirty, block Apply/Save, survive tab changes,
  and clear only through explicit Reset/Cancel. Track the mounted editor, not label/index identity,
  and prevent removal or replacement that would silently discard the draft.
- Project runtime action availability out of authoring before cloning, normalizing or diffing action arrays. Use the Table owner’s `table-action-authoring-projection.ts` for toolbar, row, bulk and nested children; do not strip arbitrary business payloads or patch only the Page Builder adapter.
- Capture the host-authored `disabled` state before availability overrides it. A later allowed capability must not erase an explicit host denial, and a session denial must not become an authored restriction after a label/order edit. Internal `__praxis*` provenance is runtime bookkeeping, never a public setting or persisted action field.
- For older snapshots without recoverable origin, preserve `disabled: true` and diagnose the ambiguity. Never infer origin from labels, array positions, duplicate identifiers or assumed credentials. Test clean/legacy input, explicit false/true/absent disabled, nested menus, reorder and save/reopen through the real editor.
- For i18n, put editor chrome text in `table-editor.i18n.ts`; do not add visible hardcoded text.

Column visibility, reorder, resize, auto-fit, density, and other runtime
customizations must serialize through one persistence lane. Queue/coalesce
overlapping mutations deliberately, acknowledge success, and handle 409/412 by
loading the remote document and reconciling only the changed semantic field.
Never blindly retry a stale whole document or report persisted before the
storage acknowledgement.

## Round-Trip Checklist

For every editable field, prove or inspect:

1. Existing config opens in the editor with the correct value.
2. The user can change it through the canonical editor surface.
3. Apply/save emits the expected config/document shape.
4. Runtime reflects the applied change.
5. Reopening the editor preserves the value.
6. Reset does not erase unrelated table state.

Also switch from visual controls to JSON without closing the editor: an untouched
JSON projection must follow current visual edits. Preserve unapplied manual JSON,
including invalid or empty text, instead of overwriting it on input changes. After
the host acknowledges an applied JSON draft, subsequent visual edits must sync
again. Compare the complete document so unknown authored keys are not silently lost.

If no visual editor is affected, say so explicitly and explain why.

## Validation

- Config editor or Settings Panel: `config-editors-integration.spec.ts`, `open-table-settings.spec.ts`, and focused editor specs.
- Columns: `columns-config-editor*.spec.ts` and renderer-specific specs when output changes.
- Filters: `filter-settings*.spec.ts` plus filter E2E when browser interaction matters.
- Rules/formulas: `table-rules-editor*.spec.ts`, `rule-compiler.service.spec.ts`, `visual-formula-builder*.spec.ts`, and `npm run verify:no-visual-builder` when relevant.
- CRUD integration: `crud-integration-editor` coverage plus config editor integration.
- Visual authoring: Playwrights such as `table-json-authoring`, `table-json-rules`, `table-rules-editor`, `column-drag`, and expansion authoring.

## Companion Skills

- Use `praxis-angular-accessibility-governance` for keyboard resize/reorder, focus, and live persistence feedback.

- Use `praxis-authoring-editors` for cross-component editor, persistence, Settings Panel, and round-trip principles.
- Use `praxis-table-data-source-precedence` for authoring `resourcePath`, local-data mode, bindings, apply-plan diagnostics, and source precedence.
- Use `praxis-table-selection-export-runtime` when Settings Panel authors export, bulk actions, row actions, or selection-dependent behavior.
- Use `praxis-table-renderer-state-diagnostics` when editors change renderer config, formatting, state copy, or visible diagnostics.
- Use `praxis-table-runtime-data` for broader runtime behavior that the editor materializes.
- Use `praxis-table-filter-actions` for filters, actions, CRUD action wiring, and export operation authoring.
- Use `praxis-table-ai-validation` for AI component edit plan coverage and registry ingestion.
- Use `praxis-table-rule-effects-runtime`, `praxis-table-rule-animation-presets`, and `praxis-table-rule-table-integration` when the table rules editor embeds `@praxisui/table-rule-builder` effects, presets, animations, or renderer placement.
- Use `praxis-table-rule-ai-validation` when table visual rule effects are AI-authorable or delegated from the table assistant.
- Use `praxis-ui-product-design` for editor layout, density, accessibility, and screenshot validation.
