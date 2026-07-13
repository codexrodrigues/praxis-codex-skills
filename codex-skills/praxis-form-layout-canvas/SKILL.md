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
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-document.model.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.ts`
- `projects/praxis-dynamic-form/src/lib/layout-editor/**`
- `projects/praxis-dynamic-form/src/lib/canvas/**`
- `projects/praxis-dynamic-form/src/lib/services/dynamic-form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-form-config.ts`
- `projects/praxis-dynamic-form/src/lib/utils/section-header.utils.ts`
- `projects/praxis-dynamic-form/src/lib/utils/visual-block-rule-content-overrides.util.ts`
- `projects/praxis-dynamic-form/docs/schema-driven-layout-materialization-rfc.md`
- `projects/praxis-dynamic-form/docs/layout-items-visual-blocks.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-rules-authoring-plan.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-visual-builder-parity-audit.md`
- `projects/praxis-dynamic-form/docs/hot-metadata-updates.md`
- related JSON API docs such as `layout-editor/praxis-layout-editor.json-api.md` and `config-editor/praxis-dynamic-form-config-editor.json-api.md`

Inspect `@praxisui/core` form layout models when changing `FormConfig`, `FormLayout`, `FormColumn.items`, visual block rules, or `DynamicFormLayoutPolicy`.

Concrete `@praxisui/core` files to inspect for layout ownership and schema materialization:

- `projects/praxis-core/src/lib/models/form/form-config.model.ts`
- `projects/praxis-core/src/lib/models/form/form-config.model.spec.ts`
- `projects/praxis-core/src/lib/models/form/form-layout-items.model.ts`
- `projects/praxis-core/src/lib/helpers/ensure-ids.helper.ts`
- `projects/praxis-core/src/lib/helpers/ensure-ids.helper.spec.ts`
- `projects/praxis-core/src/lib/helpers/form-layout-materializer.ts`
- `projects/praxis-core/src/lib/helpers/form-layout-materializer.spec.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts`
- `projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.ts`
- `projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts`

## Canonical Layout Rules

- `FormColumn.items[]` is the canonical order for fields and visual blocks inside a column.
- `fields[]` is only a compatibility/migration projection.
- API fields remain in `fieldMetadata[]` and appear in layout as `items[]` with `kind: "field"`.
- Visual blocks are `items[]` with `kind: "richContent"` and a valid `RichContentDocument`.
- Visual blocks do not create `FormControl`, do not enter `fieldMetadata[]`, and do not enter submit payloads.
- Presets are authoring shortcuts only; persisted runtime semantics are still rich content documents.
- `DynamicFormAuthoringDocument` is the complete authoring snapshot. Do not persist runtime/discovery-only values such as host `schemaUrl`, `submitUrl`, or `submitMethod` inside authoring bindings.
- Layout editor, canvas editor, config editor, JSON editor, and AI authoring must round-trip the same `FormConfig.sections[].rows[].columns[].items[]` semantics.
- Rule targets may include visual blocks, sections, rows, columns, actions, and fields, but visual-block rules remain visual-only and must not mutate domain payload semantics.
- Normalize IDs and legacy layout shape through the shared core helpers. `ensureIds(...)` must preserve rich content items, normalize legacy `fields[]` into canonical `items[]`, and keep `fields[]` synchronized as a field-only projection.
- Use `getFormColumnFieldNames(...)`/layout item helpers instead of reading `column.fields` directly when code must understand current field order.
- Surface materialization can project read data into Dynamic Form `initialValue` and a transient schema `layoutPolicy`; that is runtime materialization, not authored local `FormConfig.sections`.
- Dynamic widget loading must pass `layoutPolicy` and related runtime inputs through to Dynamic Form instead of flattening them into host-specific config.
- "Add API field" means place an existing `fieldMetadata[].name` into canonical `items[]`
  (`kind: "field"`) and preserve `fieldMetadata[]`. It is not permission to create DTO/schema
  fields, clone metadata, or patch backend semantics from the canvas.
- Local fields are a separate authoring path and must carry safe local semantics such as
  `source: "local"`, `transient: true`, and `submitPolicy: "omit"` unless a submit contract
  explicitly owns them. Do not use a local field to stand in for missing backend metadata.

Do not represent visual guidance as local fields, transient fields, DTO fields, or backend metadata unless it is genuinely domain data.

## Schema-Driven Layout Policy

Treat schema-driven layout as opt-in and explicit:

- default remains authored config.
- `layoutPolicy.source = "schema"` makes schema metadata the layout source for that runtime surface.
- `compactPresentation` with `intent: "detail"` is for read-only detail summaries.
- `groupedCommand` is for create/edit command forms.
- authored `FormConfig.sections` must not be silently overwritten unless policy says schema owns layout.
- non-layout config, such as actions, messages, hooks, behavior, submit behavior, and hints, can still come from authored config.
- `DynamicFormLayoutPolicy.schemaType` and `schemaOperation` must agree with the schema URL when declared. Detail/read-only surfaces use response schema; create/edit command surfaces use request schema.
- `SurfaceOpenMaterializerService` may default read projections to `compactPresentation` + `schemaType: "response"` and related command forms to `groupedCommand` + `schemaType: "request"`. Fix this materializer or discovery metadata before copying local sections into consumers.
- With `layoutPolicy.source="schema"` and `persistence="transient"`, generated sections, rows,
  columns, `items[]`, spans, and section order are runtime projections. Opening the editor or
  Settings Panel must not convert them into authored config unless an explicit detach/authorable
  flow is chosen.

Classify repeated local section configs as `ja-suportado-mal-nomeado-ou-mal-materializado` or `suportado-parcialmente` before proposing backend metadata changes. The backend may already publish `group`, `order`, `width`, labels, help text, read-only hints, and presentation metadata.

## Inventory Before New Contract

- `ja-suportado-so-ux`: `items[]`, layout policy, visual block, or schema metadata already supports the need, but the canvas/editor does not expose the workflow clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local `sections`, `fields[]`, visual seeds, labels, or presets duplicate semantics already present in `fieldMetadata[]`, `items[]`, schema metadata, or `DynamicFormAuthoringDocument`.
- `suportado-parcialmente`: runtime layout works, but editor round-trip, canvas state, JSON editor, AI manifest, visual builder parity, docs, responsive UX, or submit-boundary tests are incomplete.
- `lacuna-real-de-contrato`: no `FormConfig`, `FormLayout`, `FormColumn.items`, `DynamicFormLayoutPolicy`, authoring document, schema metadata, or visual-block contract can represent the layout decision.

Only `lacuna-real-de-contrato` justifies a new public layout contract. Otherwise, repair the missing projection, editor affordance, validation, or documentation in the existing chain.

## AI/Canvas Rules

- AI and canvas authoring must resolve the semantic layout operation first: add API field, reorder field, add visual block, move section/row/column, apply preset, materialize schema layout, or configure compact/grouped presentation.
- Do not route layout intent primarily by text labels, section names, CSS classes, or visual position guesses. Use canonical field names, layout item IDs, `kind`, authoring manifest operations, and schema metadata as grounding.
- Canvas state may store selection, focus, draft edits, drag state, or diagnostics. It must not become the owner of field order, field semantics, visual block document shape, submit payload, or schema-derived layout policy.
- When schema owns layout, generated sections are transient. Do not persist generated schema sections back into authored config unless the product explicitly supports an authoring conversion flow.
- When authored config owns layout, schema metadata can enrich labels, help, width, group, and read-only hints, but it must not silently overwrite authored structure.
- For Ergon or other migration consumers, treat repeated hand-authored sections as transitional debt when DTO/schema metadata can own grouping/order. Document consumer work separately instead of hardcoding Ergon-specific shortcuts into Praxis.
- For Ergon-style operational screens, prefer schema-owned grouping/order/width for scalable
  detail and command surfaces. If the layout only looks correct after local sections, local labels,
  duplicated visual seeds, or fake hidden fields, route the gap to metadata/schema materialization
  or consumer follow-up instead of institutionalizing that screen as a Praxis layout pattern.

## Validation

- Layout editor: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/layout-editor/layout-editor.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/layout-editor/field-configurator.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/layout-editor/row-configurator.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/layout-editor/section-configurator.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/layout-editor/apply-section-preset.util.spec.ts --include=projects/praxis-dynamic-form/src/lib/layout-editor/visual-block-presets.spec.ts`
- Canvas editor: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/canvas/components/section-editor/section-editor.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/canvas/components/row-editor/row-editor.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/canvas/components/column-editor/column-editor.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/canvas/components/canvas-toolbar/canvas-toolbar.component.spec.ts`
- Schema/layout services: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/services/dynamic-form-layout.service.spec.ts --include=projects/praxis-dynamic-form/src/lib/services/form-layout.service.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.layout-policy.spec.ts`
- Core layout contracts: `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/models/form/form-config.model.spec.ts --include=projects/praxis-core/src/lib/helpers/ensure-ids.helper.spec.ts --include=projects/praxis-core/src/lib/helpers/form-layout-materializer.spec.ts`
- Surface materialization: `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts`
- Authoring document/config editor: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-authoring-protocol.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.spec.ts`
- AI/rule layout authoring: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.spec.ts`
- Visual blocks: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/utils/visual-block-rule-content-overrides.util.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/rule-converters.spec.ts`
- Submit boundary: add `normalize-submit-payload.spec.ts` when layout/visual-block changes could affect payload construction.
- Browser layout: Playwrights such as `projects/praxis-dynamic-form/test-dev/e2e/visual-blocks-responsive-ux.playwright.spec.ts`, `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-layout.playwright.spec.ts`, and narrow viewport checks when UI layout changed.
- `npm run build:praxis-dynamic-form` when public exports, layout models, config editor, runtime layout services, or generated presets change.
- `npm run validate:published-doc-assets` and `npm run generate:registry:ingestion` when public docs, JSON API docs, or generated AI/registry surfaces change.

## Companion Skills

- Use `praxis-form-schema-runtime-modes` when `layoutPolicy`, generated presets, or presentation mode depend on schema-driven create/edit/view runtime.
- Use `praxis-form-runtime-submit` when layout affects runtime form construction or submit payload boundaries.
- Use `praxis-form-authoring-settings` when layout is edited through config editor, Settings Panel, JSON editor, or apply/save/reset.
- Use `praxis-form-editor-document-roundtrip` when layout changes must persist through `DynamicFormAuthoringDocument` and reopen exactly.
- Use `praxis-form-ai-rules-validation` when layout or visual blocks are authorable by AI/rules.
- Use `praxis-ui-product-design` for visual hierarchy, density, accessibility, and screenshot validation.
- Use `praxis-dynamic-fields-editorial` when field discovery or editor metadata coverage changes.
