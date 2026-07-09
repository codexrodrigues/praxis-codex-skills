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
- `PraxisTableConfigEditor` implements `SettingsValueProvider`; preserve `isDirty$`, `isValid$`, `isBusy$`, `getSettingsValue`, and apply/save/reset behavior.
- Treat `resourcePath`, `idField`, schema hash, local-data mode, and CRUD context as governed authoring state. Do not silently drop them when normalizing config.
- For columns, always validate runtime rendering, editor visibility, order, type/format, renderer, computed expressions, value mapping, conditional styles, sticky state, and headers.
- For filters, keep `behavior.filtering.advancedFilters.settings` synchronized with `FilterSettingsComponent`.
- For rules and formulas, preserve the rule compiler/operator registry and do not reintroduce prohibited old Visual Builder dependencies.
- For actions, preserve global action validation and effect shapes.
- For i18n, put editor chrome text in `table-editor.i18n.ts`; do not add visible hardcoded text.

## Round-Trip Checklist

For every editable field, prove or inspect:

1. Existing config opens in the editor with the correct value.
2. The user can change it through the canonical editor surface.
3. Apply/save emits the expected config/document shape.
4. Runtime reflects the applied change.
5. Reopening the editor preserves the value.
6. Reset does not erase unrelated table state.

If no visual editor is affected, say so explicitly and explain why.

## Validation

- Config editor or Settings Panel: `config-editors-integration.spec.ts`, `open-table-settings.spec.ts`, and focused editor specs.
- Columns: `columns-config-editor*.spec.ts` and renderer-specific specs when output changes.
- Filters: `filter-settings*.spec.ts` plus filter E2E when browser interaction matters.
- Rules/formulas: `table-rules-editor*.spec.ts`, `rule-compiler.service.spec.ts`, `visual-formula-builder*.spec.ts`, and `npm run verify:no-visual-builder` when relevant.
- CRUD integration: `crud-integration-editor` coverage plus config editor integration.
- Visual authoring: Playwrights such as `table-json-authoring`, `table-json-rules`, `table-rules-editor`, `column-drag`, and expansion authoring.

## Companion Skills

- Use `praxis-authoring-editors` for cross-component editor, persistence, Settings Panel, and round-trip principles.
- Use `praxis-table-runtime-data` for runtime behavior that the editor materializes.
- Use `praxis-table-filter-actions` for filters, actions, CRUD action wiring, and export operation authoring.
- Use `praxis-table-ai-validation` for AI component edit plan coverage and registry ingestion.
- Use `praxis-ui-product-design` for editor layout, density, accessibility, and screenshot validation.
