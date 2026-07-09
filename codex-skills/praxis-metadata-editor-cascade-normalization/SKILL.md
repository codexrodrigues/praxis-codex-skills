---
name: praxis-metadata-editor-cascade-normalization
description: Use when implementing or auditing `@praxisui/metadata-editor` cascade rules, option-source dependency mapping, schema normalization, seed hydration, `SchemaNormalizerService`, `DynamicFormFactoryService`, contextual validators, remote source configs, `x-ui.optionSource.dependsOn`, `dependencyFilterMap`, and JSON Merge Patch semantics for FieldMetadata patches.
---

# Praxis Metadata Editor Cascade Normalization

Use this skill for metadata cascade and normalization contracts. Cascades are platform metadata authoring, not host-specific filter hacks.

## Canonical Rule

Preserve the distinction between backend metadata shape and editor save shape:

- Backend `x-ui.optionSource`: `optionSource.dependsOn` and `optionSource.dependencyFilterMap`
- Metadata-editor save/runtime shape: `dependencyFields`, `dependencyFilterMap`, `dependencyValuePath`, `dependencyMergeStrategy`, `dependencyDebounceMs`, `dependencyLoadOnChange`, and related flags

The editor may hydrate from backend `x-ui` shape, but it must not silently migrate persistence unless the task explicitly includes that migration.

## Required Source Audit

Inspect:

- `projects/praxis-metadata-editor/AGENTS.md`
- `docs/metadata-editors-architecture.praxis.md`
- `docs/EDITOR-FLOW-OPTIONS.md`
- `src/lib/tabs/cascade-manager/cascade-manager-tab.component.ts`
- `src/lib/tabs/cascade-manager/cascade-rules.service.ts`
- `src/lib/services/schema-normalizer.service.ts`
- `src/lib/services/dynamic-form-factory.service.ts`
- `src/lib/registry/context-validator-registry.service.ts`
- `src/lib/validators/context-validators.ts`
- `src/lib/config/configs-remote-source.spec.ts`
- `src/lib/testing/schema-normalizer.service.spec.ts`
- `src/lib/tabs/cascade-manager/cascade-rules.service.spec.ts`

## Patch Semantics

Metadata editor patches follow JSON Merge Patch semantics:

- Changed primitive/object value: emit the new value.
- Cleared property: emit `null`.
- Host consumers must interpret `null` as property removal.

Do not replace this with host-local patch semantics. Consumers such as dynamic-form, table filters, and manual-form must adapt to the metadata-editor patch contract.

## Cascade Rules

When changing cascades:

- Ensure all dependent/source fields exist.
- Prevent cycles.
- Preserve existing unrelated metadata.
- Normalize multiline/JSON editor input into arrays or objects before emitting patches.
- Keep `dependencyLoadOnChange` modes explicit: `respectLoadOn`, `immediate`, or `manual`.
- Preserve merge strategy and debounce semantics.
- Prefer governed `RESOURCE_ENTITY` option-source semantics for business entity lookup, including identity, display, search, selection policy, capabilities, and detail/surface metadata.

## Normalization

`SchemaNormalizerService` hydrates defaults from seed by dot path and stringifies complex defaults only for textarea-friendly editors. Do not let normalizer drop advanced canonical properties such as `options`, `optionSource`, validators, presentation metadata, `submitPolicy`, or entity lookup display/detail blocks.

`DynamicFormFactoryService` must assign controls by dot path and preserve form-level contextual validators. If a normalized property path is impossible to represent in the form, fix the factory/registry rather than flattening the contract.

## Validation

Minimum gates:

- cascade hydration/dehydration: `tabs/cascade-manager/cascade-rules.service.spec.ts`
- remote source coverage: `config/configs-remote-source.spec.ts`
- schema normalization: `testing/schema-normalizer.service.spec.ts`
- dynamic form factory: `testing/dynamic-form-factory.service.spec.ts`
- contextual validators: focused validator specs such as `validators/gradient-color.validators.spec.ts`
- consumer patch behavior: use `praxis-metadata-editor-consumer-bridges` and run the relevant consumer spec when patch semantics cross package boundaries

Use `praxis-angular-validation-gates` to decide whether `ng build praxis-metadata-editor` or broader consumer validation is required.
