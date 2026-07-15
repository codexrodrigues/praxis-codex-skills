---
name: praxis-manual-form-runtime-bridge
description: Use when implementing or auditing `@praxisui/manual-form` runtime behavior, including declarative manual forms with `pdx-*` projected fields, host `FormGroup` adoption, field autodetection, `ManualFormInstance`, autosave/persistence through `ASYNC_CONFIG_STORAGE`, `ManualFieldKeyService`, field toolbar, `pdxManualEdit`, `ManualFieldMetadataBridgeService`, metadata-editor lazy bridge, and dynamic-fields/core integration.
---

# Praxis Manual Form Runtime Bridge

Use this skill when the host owns the Angular template but Praxis must still govern metadata, persistence, hot updates, field editing, and autosave. `@praxisui/manual-form` is not a local convenience wrapper; it is the canonical runtime for declarative manual Praxis forms.

For focused work, load the narrow companion first:

- `praxis-manual-form-field-detection-instance` for projected `pdx-*` controls, host `FormGroup` adoption, `ManualFormInstance`, seeds, metadata streams, and field-key resolution.
- `praxis-manual-form-autosave-persistence` for `saveDraft()`, `resetToSeed()`, `ASYNC_CONFIG_STORAGE`, storage keys, debounce, and persisted reload.
- `praxis-manual-form-toolbar-metadata-bridge` for `enableCustomization`, field toolbar, `pdxManualEdit`, Settings Panel, metadata-editor lazy bridge, and JSON Merge Patch behavior.
- `praxis-manual-form-rules-agentic` for manifest-backed AI operations, `formRules`, config editor, and registry projections that touch runtime behavior.

## Canonical Boundary

`@praxisui/manual-form` owns:

- `ManualFormComponent`
- `ManualFormInstance` and `ManualFormInstanceFactory`
- `createManualFormSeed`
- field autodetection and selector/constructor control-type mapping
- `ManualFieldKeyService`
- `ManualFieldMetadataBridgeService`
- field toolbar and `pdxManualEdit`
- autosave and draft persistence using `ASYNC_CONFIG_STORAGE`

Do not move these concerns into hosts. Prefer `@praxisui/dynamic-form` when the whole screen should be generated from schema/FormConfig. Prefer `@praxisui/metadata-editor` for advanced `FieldMetadata` editing. Manual Form bridges to those owners; it does not redefine them.

## Required Source Audit

Inspect before editing:

- `projects/praxis-manual-form/AGENTS.md`
- `README.md`
- `docs/host-manual-form-integration.md`
- `docs/manual-form-api-reference.md`
- `docs/2026-01-17/manual-form-toolbar.md`
- `src/public-api.ts`
- `src/lib/components/manual-form/manual-form.component.ts`
- `src/lib/stores/manual-form-instance.ts`
- `src/lib/seeds/manual-form.seed.ts`
- `src/lib/services/manual-field-key.service.ts`
- `src/lib/services/manual-field-metadata-bridge.service.ts`
- `src/lib/components/manual-field-toolbar/manual-field-toolbar.component.ts`
- focused specs for the affected path

## Runtime Rules

- Require a stable `formId` for production flows.
- Adopt the host `FormGroup` when `[formGroup]` is applied to `<praxis-manual-form>`; do not monkey-patch host forms.
- Use `usePathNames=true` only when nested `FormControlName.path` should become the canonical `FieldMetadata.name`.
- Field inference may rank selectors/constructors after the component context is known, but it must not become primary semantic intent routing.
- Use `ManualFieldKeyService` for path/last-segment resolution and treat ambiguous matches as a diagnostic.
- Preserve `ManualFormInstance.patchFieldMetadata()` as the patch application point so `FormConfig`, `FieldMetadata`, `FormGroup`, bound components, and state streams stay synchronized.
- Treat `ManualFormInstance` as the runtime document for manual forms. `currentConfig`, `currentFieldMetadata`, `metadataChanges()`, `formConfigChanges$`, `fieldMetadataChanges$`, and `stateChanges$` are projections of the same instance state, not separate places for consumers to author divergent metadata.
- Treat `getFieldMetadata(fieldName)` results and metadata stream values as read models. Apply changes through `patchFieldMetadata(fieldName, patch)` or `replaceConfig(config)` so JSON Merge Patch semantics, cloned snapshots, `FormGroup` validators/state, toolbar metadata, and bound component refresh remain coherent.
- Use `bindComponent(fieldName, component)`/`unbindComponent(fieldName)` for projected component hot updates. Do not create host subscriptions that write directly to component inputs while also expecting `ManualFormInstance` to be authoritative.
- Treat JSON Merge Patch `null` values from metadata-editor as removals.

## Inventory Before New Contract

Before adding inputs, exports, DTOs, metadata fields, or host conventions, classify the need:

- `ja-suportado-so-ux`: the runtime state already exists but is poorly surfaced in toolbar, docs, examples, or diagnostics.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer uses local names for concepts already owned by `FieldMetadata`, `ManualFormInstance`, persistence options, or metadata-editor patches.
- `suportado-parcialmente`: the owner exists but a projected control, bridge path, autosave path, or validation proof is incomplete.
- `lacuna-real-de-contrato`: no existing runtime, metadata, storage, bridge, or authoring contract can express the required behavior.

Only `lacuna-real-de-contrato` justifies a new public contract. Otherwise correct the canonical manual-form path or its materialization.

## Persistence And Autosave

Autosave belongs to `ManualFormInstance.saveDraft()` and `ASYNC_CONFIG_STORAGE`.

- Compose persistence with `formId`, `componentInstanceId`, and `ManualFormPersistenceOptions`.
- Keep storage browser/server safe; do not assume `localStorage` under SSR.
- Do not add host-parallel draft persistence for the same form state.
- Validate debounce and storage availability when changing autosave behavior.

## Metadata Bridge And Toolbar

Runtime field editing is gated by `enableCustomization`.

- The toolbar may toggle required, read-only, hidden, disabled, and open the metadata editor.
- `pdxManualEdit` and programmatic `tryOpenFieldEditor(fieldName)` must resolve to a real field.
- `ManualFieldMetadataBridgeService` lazy-loads `FieldMetadataEditorComponent` from `@praxisui/metadata-editor`.
- The bridge must pass canonical `controlType`, seed, and host bridge patch handlers.
- If `@praxisui/metadata-editor` cannot load, surface a diagnostic in dev mode instead of silently applying incomplete local edits.

## Validation

Use the smallest reliable proof:

- compile: `ng build praxis-manual-form`
- runtime/field detection: `components/manual-form/manual-form.component.spec.ts`
- docs example/showcase: `components/manual-form-doc-example/*.spec.ts` and `examples/manual-form-doc-example-showcase.component.spec.ts`
- key resolution: `services/manual-field-key.service.spec.ts`
- i18n: `i18n/manual-form.i18n.spec.ts`
- metadata bridge changes: pair with `praxis-metadata-editor-consumer-bridges`

Review `README.md`, docs manifests, public API, examples, and official docs when runtime behavior changes.
