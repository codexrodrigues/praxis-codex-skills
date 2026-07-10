---
name: praxis-editorial-forms-agentic-authoring
description: Use when implementing or auditing `@praxisui/editorial-forms` AI authoring, `PRAXIS_EDITORIAL_FORMS_AUTHORING_MANIFEST`, component edit plans, snapshot/fallback/presentation operations, adapter binding, data block add/remove, field binding, registry ingestion, component metadata, docs, labs, and governed handoff to dynamic-form, metadata-editor, rich-content, or page-builder.
---

# Praxis Editorial Forms Agentic Authoring

Use this skill when editorial experiences are authored by AI, tools, or visual editors. Editorial authoring must compile to manifest-backed operations over the editorial runtime document; it must not emit arbitrary JSON patches or collapse the domain into dynamic-form config.

## Source Audit

Inspect before editing:

- `projects/praxis-editorial-forms/AGENTS.md`
- `projects/praxis-editorial-forms/README.md`
- `projects/praxis-editorial-forms/docs/editorial-authoring-playbook.md`
- `projects/praxis-editorial-forms/docs/editorial-authoring-plan.md`
- `projects/praxis-editorial-forms/src/lib/ai/praxis-editorial-forms-authoring-manifest.ts`
- `projects/praxis-editorial-forms/src/lib/editorial-form-runtime.metadata.ts`
- `projects/praxis-editorial-forms/src/lib/praxis-editorial-forms.ts`
- `projects/praxis-editorial-forms/src/public-api.ts`
- manifest, component metadata, registry, docs, lab, and E2E specs for the affected path

## Canonical Boundary

`PRAXIS_EDITORIAL_FORMS_AUTHORING_MANIFEST` is the executable authoring contract for `EditorialRuntimeInput`. Component metadata and `providePraxisEditorialForms()` publish the runtime to dynamic widget composition. Registry ingestion and docs are derived projections; they must not redefine editorial semantics.

Use domain operations, not free patches:

- `snapshot.set`
- `fallback.configure`
- `presentation.configure`
- `adapter.bind`
- `dataBlock.add`
- `dataBlock.remove`
- `fieldBinding.set`

## Authoring Rules

- `snapshot.set` must preserve diagnostics and validate solution, journey, and step existence.
- `fallback.configure` must be explicit and diagnostic-backed; fallback is derived, not domain truth.
- `presentation.configure` writes only under `solution.presentation` and must not mutate journeys, blocks, `FormConfig`, `FieldMetadata`, or runtime data.
- `adapter.bind` validates adapter registry existence, support, component inputs, fallback policy, and event forwarding.
- `dataBlock.add` and `dataBlock.remove` operate on stable journey/step/block ids; destructive removal requires confirmation and must reject live field-binding references.
- `fieldBinding.set` governs `runtimeContext.formData` paths and delegates `FieldMetadata` changes to metadata-editor.
- Rich/narrative blocks must use canonical rich-content contracts when the authored payload is a `RichContentDocument`; do not create an editorial-only rich text dialect.
- Dynamic-page/page-builder embedding must use component metadata ports and `providePraxisEditorialForms()`, not local component registries.
- Do not route editorial intent through frontend keyword lists, regexes, or aliases. Use semantic intent, manifest operations, context packs, registry docs, and declared tools.

## Registry And Docs Rules

- Keep `EDITORIAL_FORM_RUNTIME_COMPONENT_METADATA` aligned with public inputs, outputs, ports, layout hints, and dynamic widget id `praxis-editorial-form-runtime`.
- Review `docs/praxis-docs.manifest.json`, README, architecture docs, labs, and generated registry docs when public authoring/runtime behavior changes.
- Run registry ingestion only when component metadata, authoring manifest, generated AI assets, or docs projections are affected.
- Keep labs honest: `/lab/editorial-runtime` and experimental cases are technical validation hosts, not final product UX.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: manifest/component metadata exists but editor, registry, docs, or lab projection is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer describes an operation as a page-builder/dynamic-form edit while the editorial manifest already owns it.
- `suportado-parcialmente`: operation, validator, metadata, docs, registry, or focused spec exists but is not aligned.
- `lacuna-real-de-contrato`: no existing manifest operation, target, validator, component port, registry field, or delegated owner can express the authoring decision.

Only a real gap justifies a new manifest operation, target, validator, public metadata port, or generated registry contract.

## Validation

Use focused local proof:

- manifest: `src/lib/ai/praxis-editorial-forms-authoring-manifest.spec.ts`
- component metadata/provider: `src/lib/editorial-form-runtime.metadata.spec.ts`
- runtime round-trip: `src/lib/editorial-form-runtime.component.spec.ts`
- adapter operations: adapter registry and dynamic-form adapter specs
- docs/registry: `npm run generate:registry:ingestion` only when generated registry artifacts are affected
- build: `npm run build:praxis-editorial-forms`
- labs/E2E: focused `test-dev/e2e/*.playwright.spec.ts` when host experiments or labs change

Pair with `praxis-editorial-forms-journey-snapshot-runtime`, `praxis-editorial-forms-presentation-diagnostics`, and `praxis-editorial-forms-data-collection-adapters` according to the operation being authored.
