---
name: praxis-metadata-editor-consumer-bridges
description: Use when integrating or reviewing consumers of `@praxisui/metadata-editor`, including dynamic-form canvas/layout editor, table filter settings, manual-form metadata bridge, Page Builder hosted editors, Settings Panel open/apply/save flows, lazy imports of `FieldMetadataEditorComponent`, cascade tab hosting, JSON Merge Patch application, and avoiding duplicate metadata semantics in consumers.
---

# Praxis Metadata Editor Consumer Bridges

Use this skill when another Praxis lib opens or delegates to `@praxisui/metadata-editor`. Consumers should bridge to the canonical editor; they should not redefine FieldMetadata editing, cascade semantics, or dynamic-fields coverage locally.

Resolve paths from `praxis-ui-angular/` unless another root is named.

## Canonical Consumers

Known consumers include:

- `@praxisui/dynamic-form`: canvas/form builder field metadata editing and `all-fields-metadata-editor` E2E coverage.
- `@praxisui/table`: filter settings, `praxis-filter`, always-visible field override editing, and `filter-inline-metadata-editor` E2E coverage.
- `@praxisui/manual-form`: `ManualFieldMetadataBridgeService` delegates advanced field metadata edits.
- `@praxisui/crud`: owns CRUD shell metadata but delegates FormConfig and FieldMetadata edits to dynamic-form/metadata-editor manifests.
- `@praxisui/page-builder`: hosts child component config editors and must delegate child metadata semantics through child component manifests/config editors instead of editing child input semantics locally.
- `@praxisui/editorial-forms`: delegates FieldMetadata authoring to metadata-editor/dynamic-fields and owns only editorial binding/orchestration.

## Required Source Audit

Inspect the metadata-editor sources plus the affected consumer:

- `projects/praxis-metadata-editor/AGENTS.md`
- `docs/metadata-editors-architecture.praxis.md`
- `src/public-api.ts`
- consumer `AGENTS.md`
- dynamic-form: `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`, `src/lib/layout-editor/layout-editor.component.ts`, `src/lib/config-editor/praxis-dynamic-form-config-editor.ts`, `src/lib/utils/metadata-mappers.ts`, and `test-dev/e2e/all-fields-metadata-editor.playwright.spec.ts`
- table: `projects/praxis-table/src/lib/filter-settings/filter-settings.component.ts`, `src/lib/components/praxis-filter/praxis-filter.component.ts`, `src/lib/ai/table-component-edit-plan.ts`, and `test-dev/e2e/filter-inline-metadata-editor.playwright.spec.ts`
- manual-form: `projects/praxis-manual-form/src/lib/services/manual-field-metadata-bridge.service.ts`, `src/lib/ai/praxis-manual-form-authoring-manifest.ts`, plus `praxis-manual-form-toolbar-metadata-bridge` for field toolbar, `pdxManualEdit`, Settings Panel, metadata-editor lazy loading, patch diagnostics, and draft persistence side effects
- CRUD: `projects/praxis-crud/src/lib/open-crud-metadata-editor.ts`, `src/lib/crud-metadata-editor.component.ts`, `src/lib/ai/praxis-crud-authoring-manifest.ts`, and focused authoring entrypoint specs
- Page Builder: `projects/praxis-page-builder/src/lib/dynamic-page-builder.component.ts`, `src/lib/ai/praxis-page-builder-authoring-manifest.ts`, widget config editor hosting, child component manifest resolution, and `SETTINGS_PANEL_BRIDGE`
- editorial forms: `projects/praxis-editorial-forms/src/lib/ai/praxis-editorial-forms-authoring-manifest.ts` when a flow wants to change field metadata from editorial contexts

## Bridge Rules

- Use `FieldMetadataEditorComponent` for advanced FieldMetadata edits.
- Pass canonical `controlType` and `seed`; normalize aliases through core helpers before opening.
- Lazy-load `@praxisui/metadata-editor` when the consumer should avoid a hard authoring dependency in the runtime path, but fail visibly through diagnostics/snackbar/logging when the module or `FieldMetadataEditorComponent` export is unavailable.
- Wire at least one canonical patch path, and preferably both when supported by the host: `hostBridge.applyPatch` for immediate editor-to-host application and Settings Panel `applied$`/`saved$` subscriptions for Apply/Save.
- Receive delta patch from `hostBridge`, `applied$`, or Settings Panel save and apply JSON Merge Patch semantics, including `null` removal where the consumer stores metadata overrides.
- Do not copy metadata-editor configs into consumers.
- Do not add consumer-only fields for metadata that belongs to `FieldMetadata`, dynamic-fields descriptors, or backend `x-ui`.
- Preserve host/product responsibility: consumers may choose when to open the editor and where to persist accepted patches, but the edited semantics belong to metadata-editor/core/dynamic-fields.
- Preserve immutable identity in consumers. Field edits may change metadata properties, but field lookup identity such as `name` must be kept unless the task is explicitly a rename flow with downstream layout/rule/reference migration.
- Keep consumer transforms narrow and evidence-backed. For example, dynamic-form may map rating-specific metadata, and table may sanitize override values, but neither may redefine the metadata-editor schema.

## Current Consumer Patterns

Use the existing implementation as the default pattern:

- dynamic-form `praxis-dynamic-form.ts`: lazy import, Settings Panel id `field-meta.<formId>.<fieldName>`, `hostBridge.applyPatch`, `applied$`/`saved$`, `applyNullDeletionPatch`, `stripNullMarkersFromPatch`, and form rebuild after patch.
- dynamic-form `layout-editor.component.ts`: lazy import, Settings Panel id `layout.fieldMetadata.<fieldName>`, `hostBridge.applyPatch`, `applied$`/`saved$`, patch merged into `config.fieldMetadata`, and `name` preserved.
- table `filter-settings.component.ts`: optional module id override, fallback to static `@praxisui/metadata-editor`, Settings Panel id `filter-field-meta.<configKey>.<fieldName>`, `applied$`/`saved$`, JSON Merge Patch into `alwaysVisibleFieldMetadataOverrides`, and empty override removal.
- table `praxis-filter.component.ts`: lazy import, Settings Panel id `filter-field-meta.<formId|filterId>.<fieldName>`, `applied$`/`saved$`, sanitized field override merge, schema re-application, and `saveConfig()`.
- manual-form `ManualFieldMetadataBridgeService`: lazy import, Settings Panel id `manual-field.<formId>.<fieldName>`, `hostBridge.applyPatch`, `applied$`/`saved$`, duplicate patch suppression, `instance.patchFieldMetadata(...)`, and draft persistence.
- CRUD and Page Builder: treat child component configuration as delegated authoring. CRUD must not locally write FormConfig/TableConfig/FieldMetadata semantics; Page Builder must use child manifests/config editors and Settings Panel bridge for widget inputs.

## Settings Panel

When hosted in Settings Panel:

- Verify open, apply, save, reset/cancel, and reopen.
- Use the editor's dirty/valid/busy state when exposed.
- Do not swallow `applied$` or `saved$` events; bridge them to the consumer's canonical patch application.
- If both `hostBridge.applyPatch` and `applied$`/`saved$` can emit the same patch, use idempotent application or duplicate suppression where necessary.
- If lazy import fails, surface a diagnostic instead of silently falling back to incomplete local editing.
- Settings Panel ids should be stable and field-scoped so reopen/dirty state does not cross-contaminate unrelated fields.

## Patch Application

Consumer patch application must respect the consumer storage model without changing metadata-editor semantics:

- Direct `fieldMetadata[]` owners update the matching field by `name`, preserve `name`, emit config changes, and rebuild/re-render as required.
- Override-map owners merge into the field-specific override entry and remove the entry when a JSON Merge Patch leaves it empty.
- Manual-form owners patch the `ManualFormInstance` and persist draft after accepted patch.
- If a consumer cannot represent `null` removal correctly, fix the bridge/helper before changing metadata-editor output.
- Do not treat `undefined` and `null` as equivalent without checking the local helper contract. In metadata-editor patch semantics, `null` is explicit removal.

## Consumer Validation

Choose the consumer proof:

- dynamic-form field editor:
  - `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts`
  - `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/layout-editor/layout-editor.component.spec.ts`
  - E2E when visual editor coverage changes: `projects/praxis-dynamic-form/test-dev/e2e/all-fields-metadata-editor.playwright.spec.ts`
- table filters:
  - focused `filter-settings` or `praxis-filter` specs
  - E2E when inline filter editor coverage changes: `projects/praxis-table/test-dev/e2e/filter-inline-metadata-editor.playwright.spec.ts`
- manual-form bridge:
  - focused manual-form bridge/specs with `praxis-manual-form-toolbar-metadata-bridge`
  - `projects/praxis-manual-form/src/lib/ai/praxis-manual-form-authoring-manifest.spec.ts` when delegation semantics change
- CRUD delegation:
  - `npx ng test praxis-crud --watch=false --progress=false --include=projects/praxis-crud/src/lib/crud-metadata-editor.component.spec.ts`
  - authoring entrypoint specs when Settings Panel open/apply behavior changes
- Page Builder hosting:
  - component palette/config editor round-trip E2E or focused `dynamic-page-builder.component.spec.ts` when widget hosting or child-operation delegation changes
- Editorial forms:
  - `projects/praxis-editorial-forms/src/lib/ai/praxis-editorial-forms-authoring-manifest.spec.ts` when FieldMetadata delegation is touched

Also run metadata-editor focused specs for the changed owner behavior. Use `praxis-manual-form-toolbar-metadata-bridge` for manual-form bridge side effects, `praxis-manual-form-field-detection-instance` for field resolution, and `praxis-authoring-editors`/`praxis-settings-roundtrip-authoring` for shared round-trip expectations.
