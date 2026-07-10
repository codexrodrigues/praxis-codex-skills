---
name: praxis-form-layout-canvas
description: Use when Codex must work on @praxisui/dynamic-form or praxis-dynamic-form package layout materialization, schema-driven layout policy, generated layout presets, layout editor, visual blocks, FormColumn.items, canvas editors, section/row/column/field placement, compact presentation, grouped command forms, or visual layout validation.
---

# Praxis Form Layout Canvas

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for Dynamic Form layout, visual blocks, canvas, and schema-driven layout materialization. Layout is a governed projection of field metadata and authoring config; it must not become a second source of business semantics.

## Source Audit

Inspect the affected source:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/layout-editor/**`
- `projects/praxis-dynamic-form/src/lib/canvas/**`
- `projects/praxis-dynamic-form/src/lib/services/dynamic-form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-form-config.ts`
- `projects/praxis-dynamic-form/src/lib/utils/section-header.utils.ts`
- `projects/praxis-dynamic-form/src/lib/utils/visual-block-rule-content-overrides.util.ts`
- `projects/praxis-dynamic-form/docs/schema-driven-layout-materialization-rfc.md`
- `projects/praxis-dynamic-form/docs/layout-items-visual-blocks.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`

Inspect `@praxisui/core` form layout models when changing `FormConfig`, `FormLayout`, `FormColumn.items`, visual block rules, or `DynamicFormLayoutPolicy`.

## Canonical Layout Rules

- `FormColumn.items[]` is the canonical order for fields and visual blocks inside a column.
- `fields[]` is only a compatibility/migration projection.
- API fields remain in `fieldMetadata[]` and appear in layout as `items[]` with `kind: "field"`.
- Visual blocks are `items[]` with `kind: "richContent"` and a valid `RichContentDocument`.
- Visual blocks do not create `FormControl`, do not enter `fieldMetadata[]`, and do not enter submit payloads.
- Presets are authoring shortcuts only; persisted runtime semantics are still rich content documents.

Do not represent visual guidance as local fields, transient fields, DTO fields, or backend metadata unless it is genuinely domain data.

## Schema-Driven Layout Policy

Treat schema-driven layout as opt-in and explicit:

- default remains authored config.
- `layoutPolicy.source = "schema"` makes schema metadata the layout source for that runtime surface.
- `compactPresentation` with `intent: "detail"` is for read-only detail summaries.
- `groupedCommand` is for create/edit command forms.
- authored `FormConfig.sections` must not be silently overwritten unless policy says schema owns layout.
- non-layout config, such as actions, messages, hooks, behavior, submit behavior, and hints, can still come from authored config.

Classify repeated local section configs as `ja-suportado-mal-nomeado-ou-mal-materializado` or `suportado-parcialmente` before proposing backend metadata changes. The backend may already publish `group`, `order`, `width`, labels, help text, read-only hints, and presentation metadata.

## Validation

- layout editor: `layout-editor/*.spec.ts`, field/row/section configurator specs, visual block preset specs
- canvas: `canvas/**/*.spec.ts`
- schema-driven layout: `dynamic-form-layout.service.spec.ts`, `form-layout.service.spec.ts`, layout policy specs
- visual blocks: `visual-block-rule-content-overrides.util.spec.ts`, rich content/editorial specs, visual blocks E2E
- browser layout: Playwrights such as `visual-blocks-responsive-ux`, `form-config-editor-layout`, and narrow viewport checks when UI layout changed

## Companion Skills

- Use `praxis-form-schema-runtime-modes` when `layoutPolicy`, generated presets, or presentation mode depend on schema-driven create/edit/view runtime.
- Use `praxis-form-runtime-submit` when layout affects runtime form construction or submit payload boundaries.
- Use `praxis-form-authoring-settings` when layout is edited through config editor, Settings Panel, JSON editor, or apply/save/reset.
- Use `praxis-form-editor-document-roundtrip` when layout changes must persist through `DynamicFormAuthoringDocument` and reopen exactly.
- Use `praxis-form-ai-rules-validation` when layout or visual blocks are authorable by AI/rules.
- Use `praxis-ui-product-design` for visual hierarchy, density, accessibility, and screenshot validation.
- Use `praxis-dynamic-fields-editorial` when field discovery or editor metadata coverage changes.
