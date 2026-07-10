---
name: praxis-fields-control-profile-ai
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields or praxis-dynamic-fields package AI control profiles: PRAXIS_DYNAMIC_FIELDS_AUTHORING_MANIFEST, PRAXIS_DYNAMIC_FIELDS_AUTHORING_PROFILES, control-type AI catalog, per-control family operations, validators, profile componentIds, runtime/editorial/canvas coverage, generated AI registry docs, inline recipes, or AI-assisted field selection/configuration.
---

# Praxis Fields Control Profile AI

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill for AI-readable control-family knowledge in `@praxisui/dynamic-fields`. The family manifest owns shared `FieldMetadata`, registry, alias, selector, runtime coverage, and editor coverage semantics; component-level profiles own differences between text, numeric, currency, select, entity lookup, temporal, upload, collection, display, and shell controls.

Pair it with:

- `praxis-fields-ai-canvas-validation` for the broader AI/canvas validation workflow.
- `praxis-fields-runtime-loader` when a profile claim depends on `ComponentRegistryService` runtime resolution.
- `praxis-fields-editorial-discovery` when profile coverage depends on descriptors, metadata files, catalog entries, or component docs extraction.
- `praxis-fields-inline-overlay-runtime` when profile behavior uses compact inline filters, overlay commit semantics, or inline value shapes.
- `praxis-fields-text-number-time-controls` or `praxis-fields-selection-lookup-controls` for family-specific runtime semantics.
- `praxis-ai-registry-ingestion` when profile/catalog changes must appear in generated AI registry assets.

## Source Audit

Inspect:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `projects/praxis-dynamic-fields/README.md`
- `src/public-api.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
- relevant `src/lib/ai/*-ai-capabilities.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.recipes.ts`
- `src/lib/canvas-integration/canvas-state.token.ts`
- docs/inventory/catalog files when profiles claim public guidance or examples
- manifest/profile/catalog/inline recipe specs

## Canonical Boundary

The AI contract already knows:

- manifest targets for `controlType`, `controlAlias`, `editorialDescriptor`, `selectorMapping`, `fieldMetadataPath`, `runtimeCoverage`, and `editorCoverage`;
- operations for control registration, alias add/remove, descriptor update, selector mapping, metadata mapping, editor coverage validation, and runtime coverage validation;
- profile operations such as `field.text.configure`, `field.numeric.configure`, `field.currency.configure`, `field.select.configure`, `field.entityLookup.configure`, `field.treeSelect.configure`, `field.date.configure`, `field.dateRange.configure`, `field.timeRange.configure`, `field.toggle.configure`, and related specialized profiles;
- validators that separate runtime resolution, editor/tooling discovery, aliases, selector mapping, option identity, temporal bounds, and metadata compatibility.

Do not create one manifest per control. Add or correct a component profile when the family manifest can already represent the semantic operation.

## Inventory Before New Contract

- `ja-suportado-so-ux`: the profile/capability exists but assistant UI, canvas, docs, or examples do not expose it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a control is described through host labels or ad hoc aliases while `controlType`, profile `componentIds`, or catalog entries already provide canonical identity.
- `suportado-parcialmente`: the profile exists, but runtime/editorial evidence, registry extraction, canvas preview, examples, or validators are incomplete.
- `lacuna-real-de-contrato`: no manifest target, profile operation, validator, capability catalog, or canonical metadata path can express the control-family decision.

Only real gaps justify manifest/profile changes. Prefer profile correction over local prompt routing or broad JSON patches.

## AI Rules

- Resolve intent semantically into a control family and declared operation. Do not choose controls primarily through keywords or regexes.
- Use text/fuzzy search only after the semantic family is known, for ranking declared controls, fields, or options.
- Runtime coverage, editorial discovery, AI profile coverage, canvas coverage, and registry projection are separate evidence statuses.
- A profile claim is incomplete if the component renders but is missing from metadata/editorial discovery or AI registry extraction.
- Profile `componentIds` must align with exported metadata, runtime registration, docs/catalog, and generated component docs.
- Profile operations must produce canonical `FieldMetadata` paths; they must not invent canvas-only state.
- Wrapper controls should be represented by the dynamic-fields profile only for control selection/discovery. Their deeper package semantics must be delegated to files upload, rich content, or CRON AI skills.

## Validation

Use focused gates:

- `praxis-dynamic-fields-authoring-manifest.spec.ts`
- `control-type-ai-catalog.spec.ts`
- specs around `praxis-dynamic-fields-authoring-profiles.ts`
- `inline-filter-recipes.spec.ts` when inline/profile recipes change
- `catalog-derivation.spec.ts` and playground catalog specs when profile materialization changes
- `npm run generate:registry:ingestion` only when registry assets must update

Report whether runtime, editorial, profile, canvas, registry, docs/playground, and downstream consumer evidence were all validated or explicitly skipped.
