---
name: praxis-fields-editorial-discovery
description: Use when changing @praxisui/dynamic-fields or praxis-dynamic-fields package editorial descriptors, ComponentMetadataRegistry entries, component doc metadata, field catalogs, inventory, metadata-editor/dynamic-form discovery, i18n copy, control friendly names/icons/tags, or any case where a field renders at runtime but must also be discoverable by authoring tools.
---

# Praxis Fields Editorial Discovery

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill when a field must be found, explained, configured, or selected by Praxis authoring tools. Runtime rendering alone is not enough for package-owned `@praxisui/dynamic-fields` controls.

When the discovery issue is downstream visual editing in `@praxisui/metadata-editor`, use
`praxis-metadata-editor-renderer-coverage` to audit `FieldMetadataEditorComponent`,
`DynamicEditorRendererComponent`, `EditorProperty[]` configs, and JSON-only fallback claims. When the
same field depends on `optionSource`, cascade, remote-source, or schema-normalizer behavior, pair it
with `praxis-metadata-editor-cascade-normalization`.

When locating files, first resolve the Angular workspace root. Paths below are relative to
`praxis-ui-angular/projects/praxis-dynamic-fields` unless another package is explicitly named.

## Canonical Discovery Chain

For package-owned fields, keep this chain coherent:

1. runtime component and `ComponentRegistryService` registration
2. component `*.metadata.ts` and the matching editorial descriptor in `src/lib/editorial/**`
3. `PRAXIS_DYNAMIC_FIELDS_WAVE_1_COMPONENT_METADATA` plus `PRAXIS_DYNAMIC_FIELDS_EDITORIAL_WAVE_1`
4. `ComponentMetadataRegistry.register(...)` and `registerEditorial(...)`
5. generated/derived `ComponentDocMeta`
6. `DYNAMIC_FIELDS_PLAYGROUND_CATALOG` derivation, inventory docs, and field selection guidance
7. AI authoring surfaces: `CONTROL_TYPE_AI_CATALOGS`, authoring profiles, and `PRAXIS_DYNAMIC_FIELDS_AUTHORING_MANIFEST`
8. downstream consumers: `@praxisui/metadata-editor`, `@praxisui/dynamic-form`, `praxis-filter`, landing examples, AI registry

Host custom fields may register `ComponentDocMeta` through the host registry. Package-owned fields should not be solved by host-only metadata patches.

## Required Inventory

Inspect:

- `src/lib/editorial/dynamic-fields-wave-1.registry.ts`
- affected `src/lib/editorial/wave1/*.editorial.ts`
- affected component `*.metadata.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.spec.ts`
- `src/lib/catalog/catalog-derivation.spec.ts`
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- `src/lib/ai/control-type-ai-catalog.ts` and spec when discovery affects AI control capability lookup
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts` and spec when discovery affects AI-editable targets, operations, or registry ingestion
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts` when per-control authoring capability text changes
- `src/lib/i18n/dynamic-fields.*.ts`
- docs: inventory, field catalog, field selection guide, host custom field guide, inline filter catalog/contract where relevant

## Editorial Rules

- Friendly name, description, icon, family, track, tags, and inputs for package-owned controls belong in the canonical descriptor/metadata source, not in a downstream editor map.
- If a control is visible in runtime but missing in metadata editor, dynamic form builder, or playground, fix the registry/discovery chain rather than adding a consumer-local list.
- Keep `ComponentDocMeta.id`, `componentType`, descriptor `controlType`, selector, descriptor component reference, icon, lib, inputs, outputs, and runtime registration aligned.
- Keep `PRAXIS_DYNAMIC_FIELDS_WAVE_1_COMPONENT_METADATA` and `PRAXIS_DYNAMIC_FIELDS_EDITORIAL_WAVE_1` in the same semantic order unless you deliberately update the contract spec.
- Catalog entries should derive canonical friendly name, description, and descriptor icon from the editorial registry. Keep showcase-only data local to the catalog: recommended/avoid guidance, preview seeds, presets, snippets, interaction pattern overrides, and docs slugs.
- Keep i18n coverage in sync when editorial copy changes; do not add English-only copy for a package-owned control unless the package already treats it as technical-only.
- Preserve the distinction between primary form controls and specialized inline filter controls. Inline controls should not appear as default corporate form choices unless the authoring context is filter-focused.
- Do not publish compatibility aliases as primary authoring choices. Aliases may support ingestion or migration, but catalog choices should be canonical `FieldControlType` values.
- Keep public docs and exported catalog aligned with runtime and editorial truth. Markdown explains; the package catalog should drive official host/playground discovery.
- When a control becomes AI-discoverable, align `CONTROL_TYPE_AI_CATALOGS`, authoring profiles, and `PRAXIS_DYNAMIC_FIELDS_AUTHORING_MANIFEST` validators/targets so AI authoring resolves the same canonical control identity as runtime/editorial discovery.

## Integration With Other Skills

- Use `praxis-fields-runtime-loader` for loader, registry, selector, or hot metadata behavior.
- Use `praxis-fields-option-sources` for `optionSource`, async select, searchable select, and entity lookup behavior.
- Use `praxis-fields-ai-canvas-validation` when the change affects AI manifests, component profiles, canvas integration, or generated registry ingestion.
- Use `praxis-fields-control-profile-ai` when the field needs per-control AI profile or capability coverage.
- Use `praxis-fields-inline-overlay-runtime` when the discovery claim is about inline filter controls, `inlineOverlay`, compact pills, or overlay actions.
- Use `praxis-fields-text-number-time-controls` or `praxis-fields-selection-lookup-controls` when discovery must preserve the semantics of a specific control family.
- Use `praxis-authoring-editors` when downstream metadata editor behavior must be changed.
- Use `praxis-metadata-editor-renderer-coverage` when the downstream behavior is specifically metadata-editor visual coverage or renderer parity.

## Validation

Prefer focused checks:

- editorial descriptors:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts`
- i18n:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts`
- catalogs:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts`
- AI authoring discovery:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts`
- downstream discovery: metadata-editor or dynamic-form specs only when the consumer behavior changed

The change is incomplete if a package-owned field renders but cannot be found with the right name, icon, tags, inputs, and usage guidance in authoring tooling.
