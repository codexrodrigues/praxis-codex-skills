---
name: praxis-metadata-editor-ai-validation
description: Use when changing or validating `@praxisui/metadata-editor` AI authoring, including `PRAXIS_METADATA_EDITOR_AUTHORING_MANIFEST`, metadata editor AI capabilities, context packs, AI adapter, FieldMetadata edit operations, controlType discovery, optionSource/cascade operations, renderer coverage operations, registry ingestion, and assistant validation.
---

# Praxis Metadata Editor AI Validation

Use this skill for AI-assisted metadata authoring. The AI contract is the executable metadata-editor manifest and capabilities catalog, not free-form patches over field JSON.

Use `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, `praxis-ai-semantic-intent`, and the metadata-editor renderer/cascade skills as companions.

When locating files, first resolve the Angular workspace root. Paths below are relative to
`praxis-ui-angular/projects/praxis-metadata-editor` unless another package is explicitly named.

## Required Source Audit

Inspect:

- `projects/praxis-metadata-editor/AGENTS.md`
- `src/lib/ai/praxis-metadata-editor-authoring-manifest.ts`
- `src/lib/ai/praxis-metadata-editor-authoring-manifest.spec.ts`
- `src/lib/ai/metadata-editor-ai-capabilities.ts`
- `src/lib/ai/metadata-editor-ai.adapter.ts`
- `src/lib/ai/metadata-editor-ai.adapter.spec.ts`
- `src/lib/ai/metadata-editor-context-pack.ts`
- `src/lib/ai/*.spec.ts`
- `src/lib/praxis-metadata-editor.metadata.ts`
- `src/lib/components/field-metadata-editor/field-metadata-editor.component.ts`
- `src/lib/services/schema-normalizer.service.ts`
- `src/lib/services/dynamic-form-factory.service.ts`
- `src/lib/registry/config-registry.service.ts`
- `docs/praxis-docs.manifest.json`
- renderer/cascade docs if manifest operations touch those paths

## Canonical AI Boundary

AI edits must compile to manifest-backed operations:

- `fieldMetadata.property.set`
- `controlType.set`
- `optionSource.configure`
- `cascade.configure`
- `renderer.configure`
- validation/hint/normalization operations declared by the manifest

Do not let assistant flows route intent by keywords or emit arbitrary JSON patch shapes. Ground the operation in canonical `FieldMetadata`, dynamic-fields discovery, metadata-editor config registry, cascade rules, schema normalizer, and backend `x-ui` semantics where present.

`MetadataEditorAiAdapter` must expose `preferredResponse: componentEditPlan`, publish the manifest
operation ids, and reject free-form `patch` responses over `seed` or `controlType`. Context packs may
provide options and hints, but `actionCatalog` must not become a keyword/template router.

Some manifest operations are intentionally not materialized as local patch shortcuts. For example,
`renderer.configure` and `normalization.apply` require specialized runtime/editor handlers and must
return an error if an assistant tries to compile them into a simple local seed patch.
`normalization.apply` is especially not a cleanup patch over arbitrary metadata JSON: it is a
SchemaNormalizerService/DynamicFormFactoryService operation over `normalizedSeed`, `form`, and
`fieldMetadata`, with explicit failure modes for lost advanced properties and runtime/editor drift.
When migration friction points to normalization, fix or invoke the normalizer/factory contract and
focused specs instead of teaching the assistant to rewrite one consumer's seed.

## Operation Safety

For each changed authorable path:

- verify the input schema can express the intended value
- verify the handler contract names reads/writes, identity keys, failure modes, and validation
- verify the path has visual renderer coverage when visual coverage is required
- verify operation validators include round-trip and canonical shape checks
- verify option-source and cascade operations preserve backend `x-ui.optionSource` semantics
- verify cascade operations keep backend `x-ui.optionSource.dependsOn` and
  `x-ui.optionSource.dependencyFilterMap` as read/hydration/grounding inputs unless the operation is
  explicitly an option-source migration/configuration operation. Ordinary `cascade.configure`
  operations should write the metadata-editor runtime cascade paths produced by
  `CascadeRulesService.dehydratePatch()` / `clearPatch()`, not silently promote backend grounding paths
  into AI writes.
- verify control type changes require dynamic-fields discovery and metadata-editor coverage
- verify `affectedPaths` and handler writes stay within canonical metadata-editor paths such as
  `fieldMetadata.*`, `properties`, `editorCoverage`, `normalizedSeed`, or `form`
- verify every compile-domain-patch effect has a handler contract with reads, writes, identity keys,
  input schema, failure modes, and operational description
- verify `submissionImpact` is typed honestly: option source/cascade affect remote binding,
  validation affects submission, context hints are visual-only, renderer/normalization are config-only

Broad parent paths are not enough. If the manifest exposes a nested path, focused specs must prove the operation can express and validate it.

Date range shortcut authoring must stay static and governed. Built-in ids and static business periods
are allowed, but executable metadata such as `calculateRange`, fiscal/legal/electoral rules, holiday
logic, or business-day counting must not be embedded in field metadata.

## Registry And Docs

Run or require registry ingestion when manifest, component metadata, component docs, or AI capability catalogs change. Review `docs/praxis-docs.manifest.json` and public docs when authoring behavior is published.

## Validation

Minimum gates:

- manifest changes: `src/lib/ai/praxis-metadata-editor-authoring-manifest.spec.ts`
- adapter changes: `src/lib/ai/metadata-editor-ai.adapter.spec.ts`
- capability/context changes: `src/lib/ai/metadata-editor-ai.adapter.spec.ts` plus targeted checks for `metadata-editor-ai-capabilities.ts` or `metadata-editor-context-pack.ts`
- renderer/visual coverage operation changes: `src/lib/components/dynamic-editor-renderer/dynamic-editor-renderer.component.spec.ts`, `src/lib/components/field-metadata-editor/field-metadata-editor.component.spec.ts`, and `src/lib/config/inline-editor-coverage.spec.ts` as applicable
- normalization changes: `src/lib/testing/schema-normalizer.service.spec.ts`
- form/control creation changes: `src/lib/testing/dynamic-form-factory.service.spec.ts`
- metadata component projection: focused metadata specs if present
- registry projection: `npm run generate:registry:ingestion` when AI registry artifacts are affected
- renderer/cascade operation changes: also run the focused renderer/cascade specs named by the companion skills
- cascade AI boundary changes: pair manifest/adapter specs with `praxis-metadata-editor-cascade-normalization`
  expectations, including a focused assertion that `cascade.configure` writes root-level cascade paths
  and treats `optionSource.*` dependency paths as preserved/read-only unless the operation is explicitly
  option-source migration/configuration

Use `praxis-angular-validation-gates` to select the smallest proof and state clearly if registry ingestion, consumer E2E, or backend sync was not run.
