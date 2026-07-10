---
name: praxis-manual-form-toolbar-metadata-bridge
description: Use when implementing or auditing `@praxisui/manual-form` field customization UI, floating toolbar, `enableCustomization`, required/readOnly/hidden/disabled toggles, `pdxManualEdit`, `tryOpenFieldEditor()`, `ManualFieldMetadataBridgeService`, Settings Panel integration, lazy `@praxisui/metadata-editor` loading, or metadata patch diagnostics.
---

# Praxis Manual Form Toolbar Metadata Bridge

Use this skill when manual-form field editing must remain governed by canonical field metadata while still feeling local to a projected template. The toolbar and metadata bridge are runtime entry points into `FieldMetadata`; they are not separate persisted toolbar contracts.

## Source Audit

Inspect before editing:

- `projects/praxis-manual-form/AGENTS.md`
- `projects/praxis-manual-form/README.md`
- `projects/praxis-manual-form/docs/2026-01-17/manual-form-toolbar.md`
- `projects/praxis-manual-form/src/lib/components/manual-form/manual-form.component.ts`
- `projects/praxis-manual-form/src/lib/components/manual-field-toolbar/manual-field-toolbar.component.ts`
- `projects/praxis-manual-form/src/lib/directives/manual-field-editor-on-dblclick.directive.ts`
- `projects/praxis-manual-form/src/lib/services/manual-field-metadata-bridge.service.ts`
- `projects/praxis-manual-form/src/lib/services/manual-field-key.service.ts`
- `projects/praxis-metadata-editor/src/public-api.ts` and `FieldMetadataEditorComponent` when the bridge contract changes
- focused toolbar, bridge, and metadata-editor consumer specs

## Canonical Boundary

Manual Form owns:

- toolbar overlay placement and quick field actions
- `pdxManualEdit` and `tryOpenFieldEditor(fieldName)`
- bridge seed creation from `ManualFormInstance.getFieldMetadata(fieldName)`
- patch application through `ManualFormInstance.patchFieldMetadata()`
- duplicate patch suppression and draft persistence after successful bridge patches

`@praxisui/metadata-editor` owns advanced `FieldMetadata` editing. `@praxisui/settings-panel` owns the panel shell. Do not reimplement those editors inside manual-form or in hosts.

## Toolbar Rules

- Gate runtime editing behind `enableCustomization`.
- Resolve the active field with `ManualFieldKeyService`; ambiguous matches must be surfaced as diagnostics.
- Quick toggles may update required, read-only, hidden, and disabled metadata.
- Required toggles must keep `required` and `validators.required` consistent with current runtime conventions.
- Hidden state must update metadata and bound component visibility through the instance.
- Keep toolbar actions keyboard accessible and positioned relative to the field anchor.
- Closing, reopening, and metadata stream updates must not leave stale overlay state.

## Metadata Bridge Rules

- Lazy-load `FieldMetadataEditorComponent` from `@praxisui/metadata-editor`.
- Open through `SettingsPanelService` with a stable panel id such as `manual-field.<formId>.<fieldName>`.
- Pass the field seed and bridge handlers; do not pass free host JSON patches.
- Apply `applied$` and `saved$` patches through `ManualFieldMetadataBridgeService.handlePatch()`.
- Suppress duplicate rapid patches by signature and field.
- Treat JSON Merge Patch `null` values as removals via the instance.
- Persist draft after bridge patches when storage is available.
- In dev mode, log missing metadata, missing metadata-editor export, panel failures, and persistence failures; do not silently claim the bridge succeeded.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: the field can be patched but the toolbar affordance, diagnostics, or docs evidence is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer models toolbar flags as separate config while they are already `FieldMetadata` patches.
- `suportado-parcialmente`: a field opens the editor but lacks a supported editor renderer, patch normalization, persistence, or accessibility behavior.
- `lacuna-real-de-contrato`: no existing `FieldMetadata`, metadata-editor bridge handler, settings-panel contract, or instance patch path can express the requested edit.

Only a real gap justifies a new public bridge contract.

## Validation

Use focused local proof:

- toolbar and overlay behavior: focused `ManualFormComponent`/`ManualFieldToolbarComponent` specs
- double-click editor launch: directive or component specs around `pdxManualEdit`
- metadata bridge: `manual-field-metadata-bridge` specs and `praxis-metadata-editor-consumer-bridges`
- public integration: `ng build praxis-manual-form`; build metadata-editor only when its public exports or editor contract changed
- docs evidence: toolbar docs and examples when public behavior changes

Pair with `praxis-manual-form-field-detection-instance` for field resolution and with `praxis-metadata-editor-consumer-bridges` for cross-lib bridge behavior.
