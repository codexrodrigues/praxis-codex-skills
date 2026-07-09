---
name: praxis-fields-editorial-discovery
description: Use when changing Praxis Dynamic Fields editorial descriptors, ComponentMetadataRegistry entries, component doc metadata, field catalogs, inventory, metadata-editor/dynamic-form discovery, i18n copy, control friendly names/icons/tags, or any case where a field renders at runtime but must also be discoverable by authoring tools.
---

# Praxis Fields Editorial Discovery

Use this skill when a field must be found, explained, configured, or selected by Praxis authoring tools. Runtime rendering alone is not enough for package-owned `@praxisui/dynamic-fields` controls.

## Canonical Discovery Chain

For package-owned fields, keep this chain coherent:

1. runtime component and `ComponentRegistryService` registration
2. component `*.metadata.ts` or editorial descriptor in `src/lib/editorial/**`
3. `ComponentMetadataRegistry.register(...)` and `registerEditorial(...)`
4. generated/derived `ComponentDocMeta`
5. catalog/inventory/playground discovery
6. downstream consumers: `@praxisui/metadata-editor`, `@praxisui/dynamic-form`, `praxis-filter`, landing examples, AI registry

Host custom fields may register `ComponentDocMeta` through the host registry. Package-owned fields should not be solved by host-only metadata patches.

## Required Inventory

Inspect:

- `src/lib/editorial/dynamic-fields-wave-1.registry.ts`
- affected `src/lib/editorial/wave1/*.editorial.ts`
- affected component `*.metadata.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/catalog-derivation.spec.ts`
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- `src/lib/i18n/dynamic-fields.*.ts`
- docs: inventory, field catalog, field selection guide, host custom field guide, inline filter catalog/contract where relevant

## Editorial Rules

- Friendly name, description, icon, family, track, tags, and inputs for package-owned controls belong in the canonical descriptor/metadata source, not in a downstream editor map.
- If a control is visible in runtime but missing in metadata editor, dynamic form builder, or playground, fix the registry/discovery chain rather than adding a consumer-local list.
- Keep `ComponentDocMeta.id`, `controlType`, selector, and runtime registration aligned.
- Keep i18n coverage in sync when editorial copy changes; do not add English-only copy for a package-owned control unless the package already treats it as technical-only.
- Preserve the distinction between primary form controls and specialized inline filter controls. Inline controls should not appear as default corporate form choices unless the authoring context is filter-focused.
- Keep public docs and exported catalog aligned with runtime and editorial truth. Markdown explains; the package catalog should drive official host/playground discovery.

## Integration With Other Skills

- Use `praxis-fields-runtime-loader` for loader, registry, selector, or hot metadata behavior.
- Use `praxis-fields-option-sources` for `optionSource`, async select, searchable select, and entity lookup behavior.
- Use `praxis-fields-ai-canvas-validation` when the change affects AI manifests, component profiles, canvas integration, or generated registry ingestion.
- Use `praxis-authoring-editors` when downstream metadata editor behavior must be changed.

## Validation

Prefer focused checks:

- editorial descriptors: `metadata-contract.spec.ts`
- i18n: `metadata-i18n-contract.spec.ts`
- catalogs: `catalog-derivation.spec.ts` and `dynamic-fields-playground.catalog.spec.ts`
- downstream discovery: metadata-editor or dynamic-form specs only when the consumer behavior changed

The change is incomplete if a package-owned field renders but cannot be found with the right name, icon, tags, inputs, and usage guidance in authoring tooling.
