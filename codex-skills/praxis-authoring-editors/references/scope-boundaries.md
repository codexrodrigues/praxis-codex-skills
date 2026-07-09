# Scope Boundaries

## Fix In `settings-panel` When

- the shell semantics of `Apply` / `Save` / `Reset` are wrong
- the bridge opens the wrong content or wrong inputs
- footer behavior, shortcuts, or drawer semantics are wrong
- the issue is transversal across multiple editors

When the fix belongs in `@praxisui/settings-panel`, also review the governed artifacts of that canonical lib:

- `README.md`
- `docs/host-settings-panel-integration.md`
- `src/public-api.ts`

## Fix In `metadata-editor` When

- dynamic editor coverage is wrong or stale
- schema normalization, contextual hints, or cascade authoring broke
- `field-metadata-editor` or `dynamic-editor-renderer` disagree with the intended metadata contract
- the issue is structural authoring behavior, not just one consumer's label or wrapper

When the fix belongs in `@praxisui/metadata-editor`, also review:

- `README.md`
- `docs/architecture.praxis.md`
- `docs/metadata-editors-architecture.praxis.md`
- `docs/EDITOR-COVERAGE-CHECKLIST.md`
- `src/public-api.ts`

## Fix In Consumer Lib When

- that lib's config/document semantics changed
- the lib editor stopped exposing a field
- the lib payload is wrong
- runtime interpretation of that lib's config is wrong

Bias to the canonical subarea docs and artifacts for the owning lib:

- `dynamic-form`: `docs/dynamic-form-authoring-document-semantics.md`, `docs/hot-metadata-updates.md`, `src/public-api.ts`
- `table`: filter and authoring docs under `docs/`, adapter public API when relevant, `src/public-api.ts`
- `list`: `README.md`, subarea docs, `src/public-api.ts`
- `page-builder`: `README.md`, builder specs, `src/public-api.ts`
- `settings-panel` consumers: only after ruling out a shell contract bug

## Escalate To Cross-Lib Review When

- `SettingsValueProvider` contract and consumer behavior disagree
- one lib changed config shape and another lib's editor or builder depends on it
- a settings-panel bridge change affects multiple editors
- runtime works but the canonical editor, metadata renderer, or governed docs drifted

## Redirect To `praxis-dynamic-fields-editorial` When

- the task changes `controlType`
- aliases or selector mapping changed
- discovery/editorial metadata is involved
- the field exists in runtime but not in editor/tooling
- the change depends on descriptors in `src/lib/editorial/**`

## Do Not Confuse With Docs

If runtime and editor are correct but public explanation is stale, treat it as documentation sync, not an authoring bug.

## I18n Guardrail

If the change touches labels, placeholders, section titles, helper text, empty states, or other internal authoring text, review the workspace i18n rules before concluding the task.
