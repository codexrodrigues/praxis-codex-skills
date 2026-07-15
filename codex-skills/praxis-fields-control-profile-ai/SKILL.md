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

When locating files, first resolve the Angular workspace root. Paths below are relative to
`praxis-ui-angular/projects/praxis-dynamic-fields` unless another package or examples path is
explicitly named.

## Source Audit

Inspect:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `projects/praxis-dynamic-fields/README.md`
- `src/public-api.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts`
- `src/lib/ai/control-type-ai-catalog.ts`
- `src/lib/ai/control-type-ai-catalog.spec.ts`
- `src/lib/ai/inline-filter-recipes.spec.ts`
- relevant capability families in `src/lib/ai/*-ai-capabilities.ts`, including text, numeric, price range, select, tree, list, chips, date, time range, year, toggle, color, Brazil documents, file upload, and display action controls
- `examples/ai-recipes/praxis-dynamic-fields/*.json` when inline recipe projection changes
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.recipes.ts`
- `src/lib/canvas-integration/canvas-state.token.ts`
- `src/lib/services/component-registry/component-registry.service.ts` and dynamic field loader specs when a profile claims runtime coverage
- `src/lib/editorial/metadata-contract.spec.ts` when a profile changes supported `FieldMetadata` paths or editor-facing metadata
- docs/inventory/catalog files when profiles claim public guidance or examples
- manifest, control catalog, inline recipe, catalog derivation, metadata contract, registry, loader, and canvas specs relevant to the changed control family

## Canonical Boundary

The AI contract already knows:

- manifest targets for `controlType`, `controlAlias`, `editorialDescriptor`, `selectorMapping`, `fieldMetadataPath`, `runtimeCoverage`, and `editorCoverage`;
- operations for control registration, alias add/remove, descriptor update, selector mapping, metadata mapping, editor coverage validation, and runtime coverage validation;
- profile operations such as `field.text.configure`, `field.numeric.configure`, `field.currency.configure`, `field.select.configure`, `field.entityLookup.configure`, `field.treeSelect.configure`, `field.date.configure`, `field.dateRange.configure`, `field.timeRange.configure`, `field.toggle.configure`, and related specialized profiles;
- validators that separate runtime resolution, editor/tooling discovery, aliases, selector mapping, option identity, temporal bounds, and metadata compatibility.

Do not create one manifest per control. Add or correct a component profile when the family manifest can already represent the semantic operation.

Treat `PRAXIS_DYNAMIC_FIELDS_AUTHORING_MANIFEST` as the shared contract for targets, operations, affected paths, and ambiguity policy. Treat `PRAXIS_DYNAMIC_FIELDS_AUTHORING_PROFILES` as the place for family operations, `componentIds`, validators, examples, and canonical `FieldMetadata` paths. Treat `control-type-ai-catalog.ts` and the per-family capability files as projections used for discovery, registry ingestion, docs, recipes, and assistant grounding.

Component IDs are not decorative labels. When a profile lists `componentIds`, each ID must remain coherent with runtime registration, exported metadata, editorial discovery, playground catalog entries, generated registry assets, and the public docs surface. If one of those projections is missing, classify the change as partial coverage instead of claiming the control family is fully AI-ready.

The manifest spec keeps a projected dynamic-fields component list. If a component ID is added,
removed, or renamed, update profile coverage and evidence together: runtime registration,
metadata/editorial discovery, catalog/docs, inline recipe if applicable, and registry ingestion
assets. Do not hide a missing profile by dropping the component from the projected list.

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
- Runtime coverage claims must follow `praxis-fields-runtime-loader`: fallback normalization, host-only imports, visually similar fallback components, or missing hot metadata/rebind support are partial evidence, not a fully supported profile.
- Treat `getControlTypeCatalog(...)` as capability-family routing, not renderability proof. Direct `FieldControlType` entries and declared inline aliases can select a specialized AI capability catalog, while unknown aliases intentionally fall back to `FIELD_METADATA_CAPABILITIES`; neither path proves that a package component is registered, exported, or safe to claim as full profile coverage.
- Capability aliases in `control-type-ai-catalog.ts` are not profile identities. A value such as
  `pdx-inline-entity-lookup` may route to `SELECT_CONTROLS_AI_CAPABILITIES` so AI can ask better
  questions, but that does not make it a valid `appliesTo.componentIds` proof by itself. Profile
  readiness still requires the component ID to close the loop with exported metadata, runtime
  registration, editorial/catalog coverage, and generated component docs.
- Profile `componentIds` must align with exported metadata, runtime registration, docs/catalog, and generated component docs.
- When a profile or generated registry asset claims a component family is AI-ready, cross-check three identities together: profile `componentIds`, canonical `fieldMetadata.controlType`, and runtime registry coverage from `ComponentRegistryService`. A component ID present only in the projected manifest list or capability catalog is partial coverage until registry/editorial/docs evidence closes the loop.
- Also cross-check published catalog/playground evidence from `praxis-fields-runtime-loader`.
  `dynamic-fields-playground.catalog.spec.ts` must prove every published `controlType` resolves
  through `ComponentRegistryService.getComponent(...)`. A control family can have a profile operation
  and capability catalog but still be only partial/declared-only if the published catalog or runtime
  registry cannot materialize it.
- Profile operations must produce canonical `FieldMetadata` paths. Operation `affectedPaths` for component profiles must start with `fieldMetadata.` and must not invent canvas-only, assistant-only, prompt-only, or local UI state.
- Profile validators must be declared either in the base manifest validators or in the profile's own validators. Every operation validator should be traceable to one of those declarations.
- Profile operations must remain executable and schema-addressable: `operationId` starts with `field.`, target resolver is `field-metadata-json-path`, ambiguity policy is `fail`, examples exist, and destructive profile operations are not introduced without a reviewed manifest-level contract.
- Keep profile `affectedPaths` aligned with the actual `FieldMetadata` paths read by runtime/editorial code. Do not add canvas, assistant, or prompt-only paths as substitutes for platform metadata.
- Keep `submissionImpact` honest. For example, avatar display metadata can be `visual-only`; option sources, entity lookup, collection, file upload, and schema-backed field decisions must not be mislabeled as visual-only convenience changes.
- For option-bearing controls, delegate option source semantics to `praxis-fields-option-sources` and preserve canonical `optionSource`, identity fields, dependency maps, and value/display shape instead of inventing local select metadata.
- Select/entity lookup profiles must preserve governed option-source evidence when present: `filterEndpoint`, `byIdsEndpoint`, `selectedReloadPolicy`, `invalidSortPolicy`, `includeIds`, `dependencyFilterMap`, `capabilities.byIds`, and selection/display governance. A profile example that only sets `valueField`/`displayField` is local metadata, not proof of governed remote lookup support.
- Entity lookup profiles must preserve selection and payload semantics from `praxis-fields-selection-lookup-controls`: `selectable`/`blocked`/`legacy`, `selectionPolicy`, `payloadMode`, rich display fields, disabled reasons, and canonical identity for multi/chip operations.
- For inline filter or compact authoring behavior, delegate overlay commit and inline value-shape checks to `praxis-fields-inline-overlay-runtime`.
- Inline profile and recipe claims must state whether the control is `auto` or `explicit` apply. For explicit overlays, the profile is incomplete unless Apply/Cancel/Clear, draft isolation, and committed-value display are covered by profile examples, validators, catalog recipes, or runtime evidence.
- Inline recipe projection must keep `templateMeta.registryKey` aligned with `fieldMetadata.controlType`; tags must keep `dynamic-fields` plus `inline` or `inline-filter`.
- `getControlTypeCatalog(...)` may resolve direct `FieldControlType` values and declared inline aliases, but unknown aliases must fall back to `FIELD_METADATA_CAPABILITIES` rather than silently selecting a specialized family. Do not upgrade that fallback to a profile operation; resolve the semantic family first, then prove the control through manifest validators and runtime/editorial evidence.
- Do not promote an inline alias used only by `getControlTypeCatalog(...)` into a new profile
  `componentId` unless the same ID is present in the canonical projected component list or has a
  matching platform change that adds runtime/editorial/registry extraction evidence. Capability
  routing helps intent grounding; profile `componentIds` are coverage assertions.
- For text, numeric, temporal, selection, upload, rich content, and CRON wrappers, keep the dynamic-fields profile focused on selection, metadata wiring, and capability exposure; use the specialized package skill for deeper behavior.
- If a new profile operation or validator is needed, update manifest/profile source plus the specs that prove operation identity, affected paths, examples, validators, catalog derivation, and registry extraction. Do not ship prompt-only guidance as the source of truth.
- Wrapper controls should be represented by the dynamic-fields profile only for control selection/discovery. Their deeper package semantics must be delegated to files upload, rich content, or CRON AI skills.

## Validation

Use focused gates:

- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/inline-filter-recipes.spec.ts` for manifest, control catalog, and inline profile recipes.
- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts` when profile materialization, catalog, or `FieldMetadata` editorial contract changes.
- `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/services/component-registry/component-registry.service.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.directive.spec.ts` when profile coverage depends on runtime registration or loader behavior.
- Add the specific loader, canvas, selection, text/number/time, option source, upload, rich content, or wrapper-control specs that own the changed control family.
- `npm run generate:registry:ingestion` when generated AI registry assets, component docs extraction, catalogs, or registry ingestion can change.
- `npm run validate:published-doc-assets` when published docs/assets reflect the changed profile or generated registry output.
- `npm run build:praxis-dynamic-fields` when public exports, profile constants, catalog exports, or runtime registrations change.

Report whether runtime, editorial, profile, canvas, registry, docs/playground, and downstream consumer evidence were all validated or explicitly skipped.
