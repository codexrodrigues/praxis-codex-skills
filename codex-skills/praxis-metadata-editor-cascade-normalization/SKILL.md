---
name: praxis-metadata-editor-cascade-normalization
description: Use when implementing or auditing `@praxisui/metadata-editor` cascade rules, option-source dependency mapping, schema normalization, seed hydration, `SchemaNormalizerService`, `DynamicFormFactoryService`, contextual validators, remote source configs, `x-ui.optionSource.dependsOn`, `dependencyFilterMap`, and JSON Merge Patch semantics for FieldMetadata patches.
---

# Praxis Metadata Editor Cascade Normalization

Use this skill for metadata cascade and normalization contracts. Cascades are platform metadata authoring, not host-specific filter hacks.

Resolve paths from `praxis-ui-angular/projects/praxis-metadata-editor/` unless another root is named.

## Canonical Rule

Preserve the distinction between backend metadata shape and editor save shape:

- Backend `x-ui.optionSource`: `optionSource.dependsOn` and `optionSource.dependencyFilterMap`
- Metadata-editor save/runtime shape: `dependencyFields`, `dependencyFilterMap`, `dependencyValuePath`, `dependencyMergeStrategy`, `dependencyDebounceMs`, `dependencyLoadOnChange`, and related flags

The editor may hydrate from backend `x-ui` shape, but ordinary cascade-editor saves emit the metadata-editor runtime shape. Do not write back to `optionSource.dependsOn` or `optionSource.dependencyFilterMap` during normal cascade edits unless the task explicitly includes a canonical metadata migration.

When both shapes are present, root-level `dependencyFields`/`dependencyFilterMap` are the editor/runtime override. `optionSource.*` remains the backend grounding shape for discovery and entity option-source authoring.

Apply the same boundary to AI authoring manifests and adapters. A cascade operation may read
`fieldMetadata.optionSource.dependsOn` and `fieldMetadata.optionSource.dependencyFilterMap` for
hydration, grounding, or preservation checks, but it should not list or emit those backend `x-ui`
paths as ordinary writes unless the operation is explicitly an option-source migration/configuration
operation. Normal cascade authoring writes the metadata-editor runtime paths produced by
`CascadeRulesService.dehydratePatch()`.

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
- `src/lib/config/select.config.ts`
- `src/lib/config/entity-lookup.config.ts`
- `src/lib/testing/entity-lookup.fixtures.ts`
- `src/lib/testing/schema-normalizer.service.spec.ts`
- `src/lib/testing/dynamic-form-factory.service.spec.ts`
- `src/lib/tabs/cascade-manager/cascade-rules.service.spec.ts`
- `src/lib/ai/praxis-metadata-editor-authoring-manifest.ts` when AI operations can change option-source, dependency, or normalized field metadata
- `src/lib/ai/metadata-editor-ai.adapter.ts` when assistant materialization can emit cascade/option-source patches

## Patch Semantics

Metadata editor patches follow JSON Merge Patch semantics:

- Changed primitive/object value: emit the new value.
- Cleared property: emit `null`.
- Host consumers must interpret `null` as property removal.

Do not replace this with host-local patch semantics. Consumers such as dynamic-form, table filters, and manual-form must adapt to the metadata-editor patch contract.

For cascade clearing, `CascadeRulesService.clearPatch()` intentionally emits `dependencyFields: []`, `enableDependencyCascade: false`, `resetOnDependentChange: false`, and `null` for nullable cascade fields such as `dependencyFilterMap`, `dependencyValuePath`, `dependencyMergeStrategy`, `dependencyDebounceMs`, and `dependencyLoadOnChange`.

## Cascade Rules

When changing cascades:

- Ensure all dependent/source fields exist.
- Prevent cycles.
- Preserve existing unrelated metadata.
- Accept backend `optionSource.dependsOn` as either a string or an array, but hydrate it to an editor dependency array.
- Normalize dependency arrays by trimming string entries and ignoring non-string/empty values.
- Normalize multiline/JSON editor input into arrays or objects before emitting patches.
- Keep `dependencyLoadOnChange` modes explicit: `respectLoadOn`, `immediate`, or `manual`.
- Preserve merge strategy and debounce semantics.
- Preserve current defaults unless a contract change is intentional and spec-backed: `enableDependencyCascade=true` unless explicitly `false`, `resetOnDependentChange=false`, `dependencyMergeStrategy='merge'`, `dependencyDebounceMs=150`, and `dependencyLoadOnChange='respectLoadOn'`.
- Keep `suggest()` behavior deterministic: dependency filter map defaults to `dep -> dep`, and `dependencyValuePath` defaults to `id` unless an explicit value path is supplied.
- Prefer governed `RESOURCE_ENTITY` option-source semantics for business entity lookup, including identity, display, search, selection policy, capabilities, and detail/surface metadata.
- Remote option-source authoring uses `resourcePath`; do not reintroduce legacy `endpoint` in select, radio, button-toggle, transfer-list, or entity lookup configs.
- `RESOURCE_ENTITY` coverage must include `optionSource.key`, `type`, `entityKey`, `resourcePath`, value/label/code/description/status paths, search/filtering metadata, `dependsOn`, `dependencyFilterMap`, selection policy, `capabilities.byIds`, detail/create metadata, dialog columns, and actions.
- Do not confuse RESOURCE_ENTITY option-source authoring with cascade rule authoring. Editing
  `optionSource.dependsOn` inside an option-source editor configures backend/discovery grounding;
  editing a cascade rule configures `dependencyFields` and root-level cascade behavior for
  metadata-editor/runtime consumption.

## Normalization

`SchemaNormalizerService` hydrates defaults from seed by dot path and stringifies complex defaults only for textarea-friendly editors. Do not let normalizer drop advanced canonical properties such as `options`, `optionSource`, validators, presentation metadata, `submitPolicy`, or entity lookup display/detail blocks.

Current complex default stringification is intentionally narrow. It is limited to textarea-oriented editor names such as `options`, `filterCriteria`, `paletteSettings.colors`, `views`, and `adaptiveSubtitle`. Add new JSON stringification targets only with a focused spec that proves the editor is textarea-friendly and round-trips safely.

Property-level `defaultValue` wins over seed hydration. Seed defaults are fallback materialization by dot path, not a way to override explicit editor-property defaults.

`DynamicFormFactoryService` must assign controls by dot path and preserve form-level contextual validators. If a normalized property path is impossible to represent in the form, fix the factory/registry rather than flattening the contract.

## Validation

Minimum gates:

- cascade hydration/dehydration: `tabs/cascade-manager/cascade-rules.service.spec.ts`
- remote source coverage: `config/configs-remote-source.spec.ts`
- schema normalization: `testing/schema-normalizer.service.spec.ts`
- dynamic form factory: `testing/dynamic-form-factory.service.spec.ts`
- contextual validators: focused validator specs such as `validators/gradient-color.validators.spec.ts`
- consumer patch behavior: use `praxis-metadata-editor-consumer-bridges` and run the relevant consumer spec when patch semantics cross package boundaries

Useful focused Angular gate:

```bash
npx ng test praxis-metadata-editor --watch=false --progress=false \
  --include=projects/praxis-metadata-editor/src/lib/tabs/cascade-manager/cascade-rules.service.spec.ts \
  --include=projects/praxis-metadata-editor/src/lib/config/configs-remote-source.spec.ts \
  --include=projects/praxis-metadata-editor/src/lib/testing/schema-normalizer.service.spec.ts \
  --include=projects/praxis-metadata-editor/src/lib/testing/dynamic-form-factory.service.spec.ts
```

If AI authoring operations can emit these patches, add focused AI gates:

```bash
npx ng test praxis-metadata-editor --watch=false --progress=false \
  --include=projects/praxis-metadata-editor/src/lib/ai/praxis-metadata-editor-authoring-manifest.spec.ts \
  --include=projects/praxis-metadata-editor/src/lib/ai/metadata-editor-ai.adapter.spec.ts
```

For AI cascade changes, specs should prove the handler contract keeps backend `optionSource.*`
dependency paths read-only/preserved unless the operation explicitly targets option-source
migration/configuration, and that emitted patches follow `CascadeRulesService.dehydratePatch()` /
`clearPatch()` semantics.

If entity lookup option-source runtime behavior changes, pair this skill with `praxis-fields-option-sources` and validate the direct runtime consumer.

Use `praxis-angular-validation-gates` to decide whether `ng build praxis-metadata-editor` or broader consumer validation is required.
