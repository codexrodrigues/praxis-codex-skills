---
name: praxis-metadata-editor-ai-validation
description: Use when changing or validating `@praxisui/metadata-editor` AI authoring, including `PRAXIS_METADATA_EDITOR_AUTHORING_MANIFEST`, metadata editor AI capabilities, context packs, AI adapter, FieldMetadata edit operations, controlType discovery, optionSource/cascade operations, renderer coverage operations, registry ingestion, and assistant validation.
---

# Praxis Metadata Editor AI Validation

Use this skill for AI-assisted metadata authoring. The AI contract is the executable metadata-editor manifest and capabilities catalog, not free-form patches over field JSON.

Use `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, `praxis-ai-semantic-intent`, and the metadata-editor renderer/cascade skills as companions.

## Required Source Audit

Inspect:

- `projects/praxis-metadata-editor/AGENTS.md`
- `src/lib/ai/praxis-metadata-editor-authoring-manifest.ts`
- `src/lib/ai/metadata-editor-ai-capabilities.ts`
- `src/lib/ai/metadata-editor-ai.adapter.ts`
- `src/lib/ai/metadata-editor-context-pack.ts`
- `src/lib/ai/*.spec.ts`
- `src/lib/praxis-metadata-editor.metadata.ts`
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

## Operation Safety

For each changed authorable path:

- verify the input schema can express the intended value
- verify the handler contract names reads/writes, identity keys, failure modes, and validation
- verify the path has visual renderer coverage when visual coverage is required
- verify operation validators include round-trip and canonical shape checks
- verify option-source and cascade operations preserve backend `x-ui.optionSource` semantics
- verify control type changes require dynamic-fields discovery and metadata-editor coverage

Broad parent paths are not enough. If the manifest exposes a nested path, focused specs must prove the operation can express and validate it.

## Registry And Docs

Run or require registry ingestion when manifest, component metadata, component docs, or AI capability catalogs change. Review `docs/praxis-docs.manifest.json` and public docs when authoring behavior is published.

## Validation

Minimum gates:

- manifest changes: `src/lib/ai/praxis-metadata-editor-authoring-manifest.spec.ts`
- adapter changes: `src/lib/ai/metadata-editor-ai.adapter.spec.ts`
- metadata component projection: focused metadata specs if present
- registry projection: `npm run generate:registry:ingestion` when AI registry artifacts are affected
- renderer/cascade operation changes: also run the focused renderer/cascade specs named by the companion skills

Use `praxis-angular-validation-gates` to select the smallest proof and state clearly if registry ingestion, consumer E2E, or backend sync was not run.
