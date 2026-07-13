---
name: praxis-fields-ai-canvas-validation
description: Use when changing or auditing @praxisui/dynamic-fields or praxis-dynamic-fields package AI authoring manifest, control-type AI catalog, authoring profiles, AI registry ingestion, canvas integration tokens, playground recipes, generated component docs, or validation that dynamic field runtime/editorial/canvas coverage is actually available to AI-assisted authoring.
---

# Praxis Fields AI Canvas Validation

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill to prove that `@praxisui/dynamic-fields` knowledge is available to AI-assisted authoring and canvas/editor surfaces. This is the validation layer for decisions, not a place to invent field semantics.

For focused profile work, use `praxis-fields-control-profile-ai`. For inline overlay recipes or
compact filter semantics, use `praxis-fields-inline-overlay-runtime`. For family-specific control
semantics, use `praxis-fields-text-number-time-controls` or
`praxis-fields-selection-lookup-controls` before updating AI catalogs or registry projections.

## Canonical AI/Canvas Surfaces

Inspect the actual sources:

- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
- relevant `src/lib/ai/*-ai-capabilities.ts` capability families for the changed control family
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.recipes.ts`
- `src/lib/canvas-integration/canvas-state.token.ts`
- `src/lib/services/component-registry/component-registry.service.ts`
- `src/lib/editorial/dynamic-fields-wave-1.registry.ts`
- component `*.metadata.ts` files and colocated `*.json-api.md` files for the changed controls
- `docs/dynamic-fields-field-catalog.md`
- `docs/dynamic-fields-field-selection-guide.md`
- `docs/dynamic-fields-inline-filter-runtime-contract.md`
- `docs/dynamic-fields-inventory.md`
- `docs/dynamic-fields-playground-catalog-plan.md`
- `docs/dynamic-fields-host-custom-field-guide.md` when host/custom-field behavior is involved
- `tools/ai-registry/extract-component-docs.js`
- `tools/ai-registry/generate-registry-ingestion.ts`
- `tools/ai-registry/validate-catalog-governance.js`
- `tools/ai-registry/validate-authoring-contracts-acceptance.js`
- generated AI registry artifacts when the task requires registry ingestion proof

The family manifest should capture shared `FieldMetadata`, registry, and editorial semantics. Component profiles should express per-control differences such as text, numeric, option, temporal, upload, display, and entity-lookup behavior.

The playable catalog is the canonical host/canvas projection for discovery and preview. Hosts, landing pages, playgrounds, and canvas surfaces should derive menus, cards, preview recipes, icons, snippets, and doc links from the exported catalog instead of maintaining manual lists. Markdown docs explain the contract; they must not be parsed as the runtime source of truth.

## Required Reasoning

For each AI/canvas change, answer:

- What canonical semantic decision is being authored?
- Which runtime/editorial source proves the field exists?
- Which profile or capability tells AI how to choose, configure, or avoid the field?
- Which materialization is derived: catalog, recipe, component docs, metadata editor, canvas state, or runtime preview?
- What would fail if the AI only emitted JSON without grounding in the registry/catalog?
- Which evidence statuses are complete, partial, or intentionally skipped: runtime registry, metadata registry, profile/capability, playable catalog, canvas state, registry ingestion, docs, and downstream consumers?

Do not use keyword routing as the primary way to pick a field. AI authoring should ground the user intent into canonical control types, option-source contracts, component profiles, and declared tools/catalogs.

## Coverage Rules

- Do not duplicate a full manifest per runtime control when a family manifest plus component-level profile is enough.
- Do not claim AI coverage for a package-owned field unless the registry extractor can see either literal `ComponentDocMeta` or a supported editorial factory such as `createWave1ComponentDocMeta(descriptor)`.
- Keep runtime coverage, editorial discovery, AI profile coverage, canvas/playground coverage, generated registry coverage, and docs coverage as separate statuses.
- Validate option-source and entity lookup controls with `praxis-fields-option-sources`; AI should understand by-ids reload, dependencies, and partial backend waivers instead of authoring a local select workaround.
- Keep canvas integration as a projection of field metadata/editorial state. Do not create a second concept layer for canvas-only field behavior when the canonical registry already knows it.
- Canvas state may store selection, draft, focus, validation, or preview state, but it must not become the canonical owner of control semantics, metadata shape, aliases, option-source rules, or runtime registration.
- A playable catalog entry is incomplete if its `controlType` is not resolvable by the default `ComponentRegistryService`, unless it is explicitly marked as experimental or host-owned.
- A preview recipe is incomplete if it demonstrates a control with metadata paths or value shapes not supported by the profile, capability, runtime component, or metadata editor contract.
- Docs and inventories should reference the exported catalog and registry chain. If a host needs custom fields, it may register its own runtime and metadata entries, but it must not override the platform catalog to redefine package-owned semantics.
- For wrapper controls, AI/canvas may choose and place the field through dynamic-fields, but package-specific policy must come from the owning package AI/runtime skill.

## Inventory Before New Contract

- `ja-suportado-so-ux`: registry/profile/catalog evidence exists, but canvas, playground, assistant UI, or docs do not expose it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the canvas or docs use labels, aliases, or manual seeds while the exported catalog already has canonical `controlType`, interaction pattern, icon, snippet, and doc link.
- `suportado-parcialmente`: some projections exist, but runtime registry, metadata registry, AI profile, capability family, playable catalog, registry ingestion, or docs are not all in sync.
- `lacuna-real-de-contrato`: no canonical manifest target, profile operation, runtime/editorial registration, catalog entry, or registry ingestion path can represent the field decision.

Only `lacuna-real-de-contrato` justifies new contract work. Otherwise, repair the missing projection and validation gate in the existing chain.

## Validation

Prefer focused checks:

- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/inline-filter-recipes.spec.ts` when manifest, control catalog, capability profile, or inline recipes change.
- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts` when playable catalog, preview recipe, discovery materialization, snippets, icons, doc links, or registry parity change.
- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts` when metadata/editorial coverage or docs-facing metadata changes.
- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/services/component-registry/component-registry.service.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.directive.spec.ts` when runtime registration, loader, or preview resolution changes.
- Add the focused dynamic-field loader specs for metadata refresh, presentation mode, select rebind, skip snapshot, or global states when the canvas/preview workflow depends on those paths.
- `npm run generate:registry:ingestion` when generated component docs, AI metadata, catalog governance, authoring contracts, or registry ingestion can change.
- `npm run validate:published-doc-assets` when public docs or generated docs assets reflect the changed AI/canvas surface.
- `npm run build:praxis-dynamic-fields` when public exports, catalog exports, profile constants, registry metadata, or runtime registration change.

For canvas-facing work, also verify that the field can be discovered, selected, configured, previewed, and projected into dynamic-form/metadata-editor consumers through the canonical runtime/editorial chain. A static manifest entry without runtime/editorial proof is not enough.
