---
name: praxis-editorial-forms-adapters-ai
description: Use when changing or validating `@praxisui/editorial-forms` optional adapters and AI authoring, including `EDITORIAL_DATA_BLOCK_ADAPTER`, `EditorialDataBlockAdapterRegistry`, `provideEditorialDynamicFormAdapter`, `dataCollection` blocks, adapter diagnostics, `PRAXIS_EDITORIAL_FORMS_AUTHORING_MANIFEST`, field binding, presentation/fallback operations, registry ingestion, docs, and dynamic-form/metadata-editor delegation.
---

# Praxis Editorial Forms Adapters AI

Use this skill for optional data block adapters and AI-governed editorial authoring. Editorial Forms may bind to generic engines, but the editorial domain remains canonical.

## Required Source Audit

Inspect:

- `projects/praxis-editorial-forms/AGENTS.md`
- `docs/architecture.md`
- `docs/editorial-authoring-playbook.md`
- `src/lib/adapters/editorial-data-block-adapter.ts`
- `src/lib/adapters/editorial-data-block-adapter-registry.ts`
- `src/lib/adapters/editorial-data-collection-block-outlet.component.ts`
- `src/lib/adapters/dynamic-form/editorial-dynamic-form.adapter.ts`
- `src/lib/ai/praxis-editorial-forms-authoring-manifest.ts`
- `src/lib/editorial-form-runtime.metadata.ts`
- `src/public-api.ts`
- adapter, manifest, renderer, and registry specs for the affected path

## Adapter Boundary

`dataCollection` is an editorial block kind. The concrete form engine is optional.

- Register adapters through `EDITORIAL_DATA_BLOCK_ADAPTER` and `provideEditorialDataBlockAdapter`.
- Use `EditorialDataBlockAdapterRegistry` to distinguish missing, incompatible, and resolved adapters.
- Use `provideEditorialDynamicFormAdapter({ component: PraxisDynamicForm })` only as an optional bridge.
- The host still owns `GenericCrudService`, endpoint configuration, remote schema access, and submit behavior required by Dynamic Form.
- Validate adapter components expose required inputs such as `config`, `formId`, and `editorialContext`.
- Missing or incompatible adapters must produce diagnostics, fallback state, and operational events; do not hide them behind successful-looking fallback UI.

## Authoring Manifest Rules

Use `PRAXIS_EDITORIAL_FORMS_AUTHORING_MANIFEST` as the executable contract.

- `snapshot.set` patches inputs and preserves diagnostics.
- `fallback.configure` must be explicit and diagnostic-backed.
- `presentation.configure` may affect visual presentation only.
- `adapter.bind` validates provider binding and fallback policy.
- `dataBlock.add` and `dataBlock.remove` operate on stable journey/step/block ids.
- `fieldBinding.set` writes governed runtime context bindings and delegates `FieldMetadata` changes to metadata-editor.

Do not author `FieldMetadata` inside editorial-forms. Use `praxis-metadata-editor-ai-validation` and dynamic-fields discovery when the field shape changes. Use `praxis-form-ai-rules-validation` or dynamic-form skills when data collection form semantics change.
Use `praxis-rich-content-integration-adapters` and `praxis-rich-content-ai-security-validation` when adapter or AI work materializes `RichContentDocument` in editorial blocks, previews, or generated examples.

## AI And Registry

- Do not route editorial intent by frontend keyword lists.
- Keep assistant operations scoped to declared manifest operations and validators.
- Keep component metadata and `praxis-editorial-form-runtime` registry docs aligned with `providePraxisEditorialForms`.
- Run or require AI registry ingestion when manifest, component docs, metadata, or packaged AI assets change.

## Validation

Minimum gates:

- adapter registry: `src/lib/adapters/editorial-data-block-adapter-registry.spec.ts`
- dynamic-form adapter: `src/lib/adapters/dynamic-form/editorial-dynamic-form.adapter.spec.ts`
- data collection outlet/rendering: `src/lib/renderers/editorial-data-collection-block-outlet.component.spec.ts`
- manifest: `src/lib/ai/praxis-editorial-forms-authoring-manifest.spec.ts`
- runtime fallback/snapshot when adapter diagnostics change
- compile: `npm run build:praxis-editorial-forms`
- registry/docs: `npm run generate:registry:ingestion` when generated registry artifacts are affected

Pair with `praxis-editorial-forms-runtime` for snapshot/fallback/presentation runtime behavior and `praxis-angular-validation-gates` to choose the smallest proof.
