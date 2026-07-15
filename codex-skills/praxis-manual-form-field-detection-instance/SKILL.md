---
name: praxis-manual-form-field-detection-instance
description: Use when implementing or auditing `@praxisui/manual-form` field autodetection, projected `pdx-*` controls, host `FormGroup` adoption, `usePathNames`, `ManualFormInstance`, seed creation, metadata synchronization, bound component refresh, or `ManualFieldKeyService` resolution.
---

# Praxis Manual Form Field Detection Instance

Use this skill when the host owns the Angular template but Praxis must infer and govern the manual form runtime model. `@praxisui/manual-form` is the canonical bridge between projected `pdx-*` controls and the platform `FormConfig`/`FieldMetadata` state.

## Source Audit

Inspect before editing:

- `projects/praxis-manual-form/AGENTS.md`
- `projects/praxis-manual-form/README.md`
- `projects/praxis-manual-form/src/public-api.ts`
- `projects/praxis-manual-form/src/lib/components/manual-form/manual-form.component.ts`
- `projects/praxis-manual-form/src/lib/stores/manual-form-instance.ts`
- `projects/praxis-manual-form/src/lib/seeds/manual-form.seed.ts`
- `projects/praxis-manual-form/src/lib/models/manual-form.types.ts`
- `projects/praxis-manual-form/src/lib/services/manual-field-key.service.ts`
- focused specs for manual-form component, seed, instance, and key resolution

## Canonical Boundary

`ManualFormComponent` owns projected field discovery and creates the seed used by `ManualFormInstance`. The instance owns synchronized runtime state:

`detected fields -> FieldMetadata -> FormConfig -> FormGroup -> metadata streams -> bound components`

Do not duplicate this chain in a host component, quickstart, docs example, or consumer wrapper. Hosts may provide the template and an external `[formGroup]`; the manual-form runtime owns adoption, metadata inference, and hot updates.

## Detection Rules

- Detect supported projected Praxis controls after content projection is stable.
- Infer `FieldMetadata` from component inputs and control type mapping; do not treat selector matching as primary semantic intent routing.
- Preserve a stable `FieldMetadata.name`. Use `usePathNames=true` only when nested `FormControlName.path` is intentionally the canonical name.
- Treat `ManualFieldKeyService.resolveFieldName(...)` as the canonical identity boundary for toolbar/editor activation after fields have been detected. An `ok` result returns the exact key to pass into `ManualFormInstance.getFieldMetadata(...)`, `patchFieldMetadata(...)`, `bindComponent(...)`, and metadata bridge opening.
- Stop activation on `missing` or `ambiguous` resolution and surface diagnostics or UX feedback from that state. Do not fall back to visible labels, placeholder text, CSS selectors, nearest host component identity, fuzzy command matching, or manually composed aliases to decide the target field.
- Preserve the resolved key unchanged through toolbar actions and editor patches. Renaming a field is a dedicated authoring operation that must update the runtime model, layout references, persisted values, and host template contract intentionally; it is not a side effect of field toolbar metadata patches.
- Adopt a host `FormGroupDirective` when `[formGroup]` is applied to `<praxis-manual-form>`.
- Delegate host control wiring to Angular forms APIs when an external `FormGroupDirective` exists.
- Create an internal `FormGroup` only when the host does not provide one.
- Use `createManualFormSeed(formId, config, options)` as the seed boundary; avoid constructing ad hoc seed objects in hosts.

## Instance Rules

- Use `ManualFormInstanceFactory.create(seed, persistenceOptions, externalForm?)` so `DynamicFormService` and `ASYNC_CONFIG_STORAGE` come from DI.
- Keep `patchFieldMetadata(fieldName, patch)` as the mutation point for field patches.
- Expect `patchFieldMetadata()` to update `currentConfig.fieldMetadata`, `currentFieldMetadata`, `FormGroup` validators/state, state streams, and bound components.
- Treat `metadataChanges()`, `formConfigChanges$`, `fieldMetadataChanges$`, and `stateChanges$` as derived runtime streams, not separate sources of truth.
- Use `bindComponent()`/`unbindComponent()` when a projected field must receive metadata hot updates without custom host subscriptions.
- Treat JSON Merge Patch `null` values as property removals.
- Use `ManualFieldKeyService` for toolbar/editor field resolution. Ambiguous or missing matches are diagnostics, not opportunities for fuzzy primary intent routing.
- When a resolved field key has no `FieldMetadata` in the instance, treat it as an inconsistent detection/runtime state and do not open the toolbar or metadata editor. Fix the detection seed, `usePathNames` choice, or metadata synchronization path instead of patching around the missing metadata in a host.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: metadata/state exists but the host, toolbar, docs, or example does not show it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer calls the field key a selector, path, or alias while the runtime already has `FieldMetadata.name`/path resolution.
- `suportado-parcialmente`: a projected control is detected but metadata inference, validators, path names, bound component refresh, or docs evidence is incomplete.
- `lacuna-real-de-contrato`: the runtime cannot represent the field, control type, FormGroup path, metadata patch, or state stream needed by consumers.

Only a real contract gap justifies new public types, inputs, exports, or metadata shape.

## Validation

Use the smallest local proof:

- field detection/FormGroup adoption: `components/manual-form/manual-form.component.spec.ts`
- instance state and patches: focused `manual-form-instance` specs when present, otherwise a narrow spec around the touched path
- field key resolution: `services/manual-field-key.service.spec.ts`
- public exports: `src/public-api.ts` audit plus `ng build praxis-manual-form` when exports or public contracts change
- docs/showcase evidence: manual-form doc example/showcase specs when examples are changed

Pair with `praxis-manual-form-autosave-persistence` for draft storage, `praxis-manual-form-toolbar-metadata-bridge` for field editing, and `praxis-manual-form-rules-agentic` for AI/component edit plans.
