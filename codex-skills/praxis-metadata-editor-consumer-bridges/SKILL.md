---
name: praxis-metadata-editor-consumer-bridges
description: Use when integrating or reviewing consumers of `@praxisui/metadata-editor`, including dynamic-form canvas/layout editor, table filter settings, manual-form metadata bridge, Page Builder hosted editors, Settings Panel open/apply/save flows, lazy imports of `FieldMetadataEditorComponent`, cascade tab hosting, JSON Merge Patch application, and avoiding duplicate metadata semantics in consumers.
---

# Praxis Metadata Editor Consumer Bridges

Use this skill when another Praxis lib opens or delegates to `@praxisui/metadata-editor`. Consumers should bridge to the canonical editor; they should not redefine FieldMetadata editing, cascade semantics, or dynamic-fields coverage locally.

## Canonical Consumers

Known consumers include:

- `@praxisui/dynamic-form`: canvas/form builder field metadata editing and `all-fields-metadata-editor` E2E coverage.
- `@praxisui/table`: filter settings and always-visible field override editing.
- `@praxisui/manual-form`: `ManualFieldMetadataBridgeService` delegates advanced field metadata edits.
- `@praxisui/page-builder`: hosts child component config editors and must delegate child metadata semantics.

## Required Source Audit

Inspect the metadata-editor sources plus the affected consumer:

- `projects/praxis-metadata-editor/AGENTS.md`
- `docs/metadata-editors-architecture.praxis.md`
- `src/public-api.ts`
- consumer `AGENTS.md`
- dynamic-form: `praxis-dynamic-form.ts`, `layout-editor.component.ts`, `config-editor`, and related specs/E2E
- table: `filter-settings.component.ts`, `praxis-filter.component.ts`, and focused specs
- manual-form: `manual-field-metadata-bridge.service.ts`
- Page Builder: widget config editor hosting and component metadata resolution

## Bridge Rules

- Use `FieldMetadataEditorComponent` for advanced FieldMetadata edits.
- Pass canonical `controlType` and `seed`; normalize aliases through core helpers before opening.
- Receive delta patch from `applied`/Settings Panel save and apply JSON Merge Patch semantics, including `null` removal.
- Do not copy metadata-editor configs into consumers.
- Do not add consumer-only fields for metadata that belongs to `FieldMetadata`, dynamic-fields descriptors, or backend `x-ui`.
- Preserve host/product responsibility: consumers may choose when to open the editor and where to persist accepted patches, but the edited semantics belong to metadata-editor/core/dynamic-fields.

## Settings Panel

When hosted in Settings Panel:

- Verify open, apply, save, reset/cancel, and reopen.
- Use the editor's dirty/valid/busy state when exposed.
- Do not swallow `applied` or save events; bridge them to the consumer's canonical patch application.
- If lazy import fails, surface a diagnostic instead of silently falling back to incomplete local editing.

## Consumer Validation

Choose the consumer proof:

- dynamic-form field editor: focused `praxis-dynamic-form.spec.ts`, `editor-resolution.spec.ts`, `layout-editor.component.spec.ts`, or `test-dev/e2e/all-fields-metadata-editor.playwright.spec.ts`
- table filters: focused `filter-settings` or `praxis-filter` specs
- manual-form bridge: focused manual-form bridge/specs
- Page Builder hosting: component palette/config editor round-trip E2E when widget hosting changes

Also run metadata-editor focused specs for the changed owner behavior. Use `praxis-authoring-editors` and `praxis-settings-roundtrip-authoring` for shared round-trip expectations.
