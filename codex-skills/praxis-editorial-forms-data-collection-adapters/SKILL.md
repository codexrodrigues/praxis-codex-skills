---
name: praxis-editorial-forms-data-collection-adapters
description: Use when implementing or auditing `@praxisui/editorial-forms` `dataCollection` blocks, `EditorialDataBlockAdapter`, `EDITORIAL_DATA_BLOCK_ADAPTER`, `EditorialDataBlockAdapterRegistry`, adapter resolution statuses, `EditorialDataCollectionBlockOutletComponent`, `provideEditorialDynamicFormAdapter()`, runtime form config lookup, adapter diagnostics, and dynamic-form delegation.
---

# Praxis Editorial Forms Data Collection Adapters

Use this skill when editorial blocks collect data through optional engines. `dataCollection` is an editorial block kind; concrete form engines are adapters, not the canonical editorial domain.

## Source Audit

Inspect before editing:

- `projects/praxis-editorial-forms/AGENTS.md`
- `projects/praxis-editorial-forms/README.md`
- `projects/praxis-editorial-forms/docs/architecture.md`
- `projects/praxis-editorial-forms/docs/dynamic-form-hygiene-plan.md`
- `projects/praxis-editorial-forms/src/lib/adapters/editorial-data-block-adapter.ts`
- `projects/praxis-editorial-forms/src/lib/adapters/editorial-data-block-adapter-registry.ts`
- `projects/praxis-editorial-forms/src/lib/adapters/editorial-data-collection-block-outlet.component.ts`
- `projects/praxis-editorial-forms/src/lib/adapters/dynamic-form/editorial-dynamic-form.adapter.ts`
- `projects/praxis-editorial-forms/src/lib/renderers/editorial-data-collection-block-outlet.component.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-preset-resolver.ts`
- adapter registry, dynamic-form adapter, data collection outlet, runtime fallback, and E2E specs

## Canonical Boundary

Editorial Forms owns:

- `dataCollection` block readiness in the snapshot
- form config lookup for `block.formConfig`, `instance.overrides.runtimeFormConfigs`, and `instance.compatibilityFormConfigs`
- adapter token, registry, resolution status, and adapter operational diagnostics
- runtime context merge for adapter-emitted form data

`@praxisui/dynamic-form` owns `FormConfig`, schema-backed field semantics, form submit behavior, `GenericCrudService` usage, and field metadata behavior. `@praxisui/editorial-forms` may provide `provideEditorialDynamicFormAdapter({ component: PraxisDynamicForm })` as an optional bridge only.

## Adapter Rules

- Register adapters through `EDITORIAL_DATA_BLOCK_ADAPTER` or `provideEditorialDataBlockAdapter()`.
- Use `EditorialDataBlockAdapterRegistry` to distinguish `resolved`, `missing`, and `incompatible`.
- Validate dynamic-form compatible components expose `config`, `formId`, and `editorialContext`.
- Adapter resolution failures must produce diagnostics, fallback state, and operational events.
- Missing adapters must not render as a successful data collection experience.
- Do not import `@praxisui/dynamic-form` into the central runtime model; keep it in optional adapter/provider paths.
- Keep host responsibilities explicit: `GenericCrudService`, endpoints, remote schema access, and submit behavior belong to the host/dynamic-form setup.

## Data Collection State Rules

- `dataCollectionState.readiness` may be `ready`, `requiresAdapter`, `missingConfig`, or `invalid`.
- Resolve configs by `formBlockId`/`formConfigRef` through the declared source order; ambiguous matches must become diagnostics.
- `runtimeContext.formData` is the canonical shared value bag for selection blocks, data collection adapters, review sections, and snapshots.
- Adapter value changes may merge or replace form data, and may remove keys only through the declared event shape.
- Field binding authoring should set governed `runtimeContext.formData` paths and delegate `FieldMetadata` shape changes to metadata-editor/dynamic-fields.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: adapter diagnostics/readiness exist but the outlet, docs, or lab does not show them clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer calls a dataCollection config local dynamic-form state while the runtime already has `dataCollectionState`.
- `suportado-parcialmente`: lookup, adapter support, component validation, event forwarding, or dynamic-form default mapping is incomplete.
- `lacuna-real-de-contrato`: no existing block state, adapter API, lookup key, runtime context event, or dynamic-form adapter hook can express the requirement.

Only a real gap justifies new public adapter contracts.

## Validation

Use focused local proof:

- adapter registry: `src/lib/adapters/editorial-data-block-adapter-registry.spec.ts`
- dynamic-form adapter: `src/lib/adapters/dynamic-form/editorial-dynamic-form.adapter.spec.ts`
- outlet/rendering: `src/lib/renderers/editorial-data-collection-block-outlet.component.spec.ts`
- runtime snapshot/fallback when readiness affects diagnostics: `editorial-preset-resolver.spec.ts` and `editorial-runtime-fallback.spec.ts`
- build: `npm run build:praxis-editorial-forms`
- host/lab: E2E labs when adapter behavior is validated in a real host

Pair with `praxis-form-authoring-settings`, `praxis-form-runtime-submit`, and `praxis-metadata-editor-ai-validation` when delegated dynamic-form or field metadata semantics change.
