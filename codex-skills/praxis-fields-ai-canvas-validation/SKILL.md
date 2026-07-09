---
name: praxis-fields-ai-canvas-validation
description: Use when changing or auditing Praxis Dynamic Fields AI authoring manifest, control-type AI catalog, authoring profiles, AI registry ingestion, canvas integration tokens, playground recipes, generated component docs, or validation that dynamic field runtime/editorial/canvas coverage is actually available to AI-assisted authoring.
---

# Praxis Fields AI Canvas Validation

Use this skill to prove that `@praxisui/dynamic-fields` knowledge is available to AI-assisted authoring and canvas/editor surfaces. This is the validation layer for decisions, not a place to invent field semantics.

## Canonical AI/Canvas Surfaces

Inspect the actual sources:

- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
- relevant `src/lib/ai/*-ai-capabilities.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.recipes.ts`
- `src/lib/canvas-integration/canvas-state.token.ts`
- generated AI registry artifacts when the task requires registry ingestion proof

The family manifest should capture shared `FieldMetadata`, registry, and editorial semantics. Component profiles should express per-control differences such as text, numeric, option, temporal, upload, display, and entity-lookup behavior.

## Required Reasoning

For each AI/canvas change, answer:

- What canonical semantic decision is being authored?
- Which runtime/editorial source proves the field exists?
- Which profile or capability tells AI how to choose, configure, or avoid the field?
- Which materialization is derived: catalog, recipe, component docs, metadata editor, canvas state, or runtime preview?
- What would fail if the AI only emitted JSON without grounding in the registry/catalog?

Do not use keyword routing as the primary way to pick a field. AI authoring should ground the user intent into canonical control types, option-source contracts, component profiles, and declared tools/catalogs.

## Coverage Rules

- Do not duplicate a full manifest per runtime control when a family manifest plus component-level profile is enough.
- Do not claim AI coverage for a package-owned field unless the registry extractor can see either literal `ComponentDocMeta` or a supported editorial factory such as `createWave1ComponentDocMeta(descriptor)`.
- Keep runtime coverage, editorial discovery, AI profile coverage, and canvas/playground coverage as separate statuses.
- Validate option-source and entity lookup controls with `praxis-fields-option-sources`; AI should understand by-ids reload, dependencies, and partial backend waivers instead of authoring a local select workaround.
- Keep canvas integration as a projection of field metadata/editorial state. Do not create a second concept layer for canvas-only field behavior when the canonical registry already knows it.

## Validation

Prefer focused checks:

- `praxis-dynamic-fields-authoring-manifest.spec.ts`
- `control-type-ai-catalog.spec.ts`
- `inline-filter-recipes.spec.ts` when inline recipes changed
- `catalog-derivation.spec.ts` and playground catalog specs when discovery materialization changed
- AI registry generation/ingestion only when the changed source must appear in generated component docs

For canvas-facing work, also verify that the field can be discovered, selected, configured, and previewed through the canonical runtime/editorial chain. A static manifest entry without runtime/editorial proof is not enough.
