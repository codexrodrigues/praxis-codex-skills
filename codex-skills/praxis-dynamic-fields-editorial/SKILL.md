---
name: praxis-dynamic-fields-editorial
description: Use when changing Praxis Dynamic Fields control types, aliases, discovery, editorial descriptors, metadata registry entries, selector mappings, inline filter tooling coverage, or any change where runtime support and editor/tooling support may diverge.
---

# Praxis Dynamic Fields Editorial

Use this skill for the special authoring/discovery model of `@praxisui/dynamic-fields`.

For focused changes, pair this general editorial skill with the specialized family:
`praxis-fields-runtime-loader` for loader/registry/runtime coverage,
`praxis-fields-option-sources` for async selects, option sources, and entity lookup,
`praxis-fields-editorial-discovery` for descriptor/catalog/tooling coverage, and
`praxis-fields-ai-canvas-validation` for AI manifest, registry ingestion, recipes, or canvas proof.
Use `praxis-fields-control-profile-ai` for per-control AI profiles and capability catalogs,
`praxis-fields-inline-overlay-runtime` for inline overlay apply/cancel/clear semantics,
`praxis-fields-text-number-time-controls` for text, numeric, currency, date, time, and range families,
and `praxis-fields-selection-lookup-controls` for select, autocomplete, chips, tree, list, and lookup families.
For visual authoring coverage inside `@praxisui/metadata-editor`, pair this with
`praxis-metadata-editor-renderer-coverage`; for cascade or option-source dependency normalization in
the editor, use `praxis-metadata-editor-cascade-normalization`.
For operational file upload fields, use `praxis-files-upload-form-field` for `pdx-material-files-upload`,
`valueMode`, ControlValueAccessor behavior, and upload-specific field UX. Return here only when the
dynamic-fields catalog, selector mapping, aliases, or metadata discovery for that field changes.
For rich content or rich-input fields, use `praxis-rich-content-runtime` and
`praxis-rich-content-integration-adapters` for `RichContentDocument` semantics. Return here only when
dynamic-fields metadata discovery, control aliases, selector mapping, or editor/tooling coverage changes.
For CRON or schedule fields, use `praxis-cron-builder-form-field`, `praxis-cron-builder-runtime`, and
`praxis-cron-schedule-authoring` for field/runtime semantics. Return here only when dynamic-fields
catalog registration, selector mapping, aliases, editorial descriptors, or tooling discovery changes.

This library does not primarily follow the pattern "runtime component has its own config editor". Runtime rendering, editorial discovery, metadata tooling, and editor coverage are separate layers.

Before changing this skill or a dynamic-fields feature, inspect the current source for the involved
runtime and metadata path. For ordinary controls this means the component, `.metadata.ts`,
`ComponentRegistryService`, `ComponentMetadataRegistry`, editorial registry, catalog/AI files, and
selector mapping in `@praxisui/core`. For option-source controls, also inspect
`OptionSourceMetadata`, `GenericCrudService.filterOptionSourceOptions`,
`GenericCrudService.getOptionSourceOptionsByIds`, and the backend `x-ui.optionSource` projection.
For wrapper controls, inspect the owning package skill first: files upload, rich content, and CRON
field behavior belong to those package contracts; dynamic-fields owns only control registration,
metadata discovery, selector mapping, catalogs, and downstream materialization.
The goal is to encode working Praxis platform knowledge into the skill, not merely document a UI
convention.

If the task is to implement or review backend `RESOURCE_ENTITY` option sources, use
`praxis-resource-entity-lookup-backend` first. Use this skill when that backend change affects
Angular runtime registry, editorial descriptors, metadata-editor coverage, recipes, catalogs, or
AI registry projection.

## Canonical Model

Treat these as distinct:

1. runtime render
2. forms integration
3. metadata/editorial discovery
4. hot metadata behavior

Do not assume runtime support implies editor/tooling support.

For metadata-driven option-source cascades, keep the boundary explicit:

- `x-ui.optionSource.dependsOn` is the canonical backend/editor dependency declaration.
- `x-ui.optionSource.dependencyFilterMap` is the canonical explicit mapping when the dependent field name differs from the backend filter key.
- `x-ui.optionSource.includeIds` is an explicit runtime permission. Option-source filters must send `includeIds` only when this flag is `true`; when it is `false` or absent, selected-value rehydration must use the canonical by-ids/display path instead of adding `includeIds` to filter requests.
- `x-ui.optionSource.filterEndpoint`, `byIdsEndpoint`, `selectedReloadPolicy`, and `invalidSortPolicy` are backend runtime-contract facts. Editors and examples may display or validate them, but must not synthesize them from local host assumptions when the backend publishes them.
- `dependencyFields` and `dependencyFilterMap` are the runtime/manual metadata consumed by select components.
- A bridge may derive runtime metadata from `optionSource`, but it should not synthesize authoring state or reset/reload policy unless the canonical contract says so.
- For dependent sources, editor/runtime support is incomplete until selected-value reload is proven on reopen/edit. If the selected ID is not self-contained, the runtime must use a contextual option-source by-ids path or downgrade the claim according to `selectedReloadPolicy`; do not assume the filter cascade proves hydration.

If `selectedReloadPolicy` is `required` or `supported`, verify that presentation mode, reopen/edit,
and selected-value preload call the option-source by-ids path rather than a generic options path.
If it is `unsupported-with-waiver`, the UI may show a degraded retained value, but the example or
editor must mark the source as partial and point back to the backend/platform waiver.

## Canonical Boundaries

- `ComponentRegistryService` owns runtime component resolution by `controlType`.
- `ComponentMetadataRegistry` owns editorial discovery metadata.
- `src/lib/editorial/**` owns canonical package editorial descriptors.
- `@praxisui/core` owns `FieldControlType`, `OptionSourceMetadata`,
  `DEFAULT_FIELD_SELECTOR_CONTROL_TYPE_MAP`, and selector registry tokens. Do not add a
  dynamic-fields-only alias when the canonical type or selector mapping belongs in core.
- Agentic authoring uses one family-level manifest for shared `FieldMetadata`/registry/editorial semantics plus component-level control profiles for granular per-control operation hints; use `praxis-fields-control-profile-ai` for that layer and do not duplicate a full manifest per runtime control when a profile can express the semantic difference.
- Derived catalogs and inventories must stay aligned with the editorial source.
- AI Registry component docs must remain extractable from either literal `ComponentDocMeta` metadata files or supported editorial factories such as `createWave1ComponentDocMeta(descriptor)`. If a package-owned field uses a metadata factory, verify the registry extractor still projects it before claiming catalog coverage.
- `@praxisui/metadata-editor`, `@praxisui/dynamic-form`, `praxis-filter`, and related tooling consume this chain downstream.
- `@praxisui/dynamic-form` materializes `FieldMetadata` through this chain; it should not carry a
  private control map when the package registry/editorial catalog already owns the decision.
- `@praxisui/metadata-editor` must expose the same package-owned metadata shape that runtime fields
  consume; renderer coverage gaps should be fixed in the editor bridge, not hidden in docs.
- Shared overlay infrastructure, layer tokens, and CDK stacking order belong to `@praxisui/core`. If an inline field renders but overlay clicks are blocked, verify the core layer scale before patching the field, filter host, or landing app.
- Shared overlay color/contrast tokens also belong to `@praxisui/core`. If a dynamic field overlay opens with low contrast, first verify `@praxisui/core/theme-bridge.css` and the host `.cdk-overlay-container` mappings for `--pdx-overlay-surface` and `--pdx-overlay-on-surface`; only add a host override when the host intentionally uses an overlay surface that differs from the global Material theme.
- Package-owned inline field and panel surface/contrast tokens belong to the inline components in `@praxisui/dynamic-fields` (`--pdx-inline-field-*` and `--pdx-inline-panel-*`). If host global `.mat-mdc-form-field`, `.mat-mdc-select-panel`, or Material option/select token styles break inline filters, fix or preserve these component tokens before adding host-only overrides.
- Inline overlay commit semantics belong to the shared `inlineOverlay` contract. Do not create local `confirm`, `commitPolicy`, or per-component Apply/Cancel contracts when `inlineOverlay.applyMode` and `inlineOverlay.actions.*` can represent the workflow. The public vocabulary is `applyMode: "auto" | "explicit"`: use `auto` for simple, reversible, single-step inline interactions; use `explicit` when an overlay has a real draft state such as ranges, multi-selection, presets, sliders, or exploratory visual choices. In `explicit`, Apply commits, Cancel/Escape/outside close restore the last committed value, and Clear is distinct from Cancel.

## Package-Owned Fields vs Host Custom Fields

Package-owned Praxis fields must follow the canonical library path:

- editorial descriptor
- derived metadata
- derived catalog

Host custom fields may use:

- `ComponentRegistryService.register(...)`
- `ComponentMetadataRegistry.register(ComponentDocMeta)`

Do not solve package-owned field issues with host-only patches.

## Trigger Conditions

Use this skill when the task changes any of:

- `controlType`
- aliases
- selector mapping
- runtime registry entries
- editorial descriptors
- component metadata
- inventory or catalog content
- inline filter discoverability
- naming/icon/discovery in editor/tooling
- package-owned field onboarding
- host custom field extension path
- official examples or recipes that project backend `RESOURCE_ENTITY` metadata into package-owned
  dynamic field behavior

## Required Workflow

1. Decide whether the field is package-owned or host custom.
2. Check runtime registry resolution.
3. Check metadata/editorial resolution.
4. Check downstream discovery in editor/tooling.
5. Check runtime/editor coverage status and any documented mismatch.
6. Update the governed docs/catalog/inventory that mirror this chain when the canonical editorial source changed.

## Required Checks

Always verify:

- runtime component still resolves for the target `controlType`
- editorial metadata still resolves friendly name, icon, and discoverable identity
- aliases still resolve correctly
- selector-to-control mapping is correct in the `@praxisui/core` default selector map or in an
  explicit host override, with defaults disabled only at the root injector when intended
- downstream tooling can still discover the field
- any editor/tooling coverage claim remains true
- option-source controls honor backend `includeIds`, dependency maps, selected reload policy, and
  invalid sort policy instead of hiding backend contract gaps in local runtime code
- package-owned controls projected into AI registry have an applicable authoring control profile when the task touches agentic authoring semantics
- package-owned metadata factories are visible in `tools/ai-registry/component-docs.json` after `generate:registry:ingestion`
- governed docs such as inventory, field catalog, field selection guide, and inline runtime contract still match the real behavior
- derived surfaces such as docs, playground catalog, AI registry, metadata-editor coverage, and dynamic-form materialization are either updated or explicitly not affected

If a field renders but becomes undiscoverable in editor/tooling, the change is incomplete.

## High-Risk Failure Modes

- runtime registry updated but metadata registry not updated
- new `controlType` added without editorial descriptor
- alias works in runtime but not in tooling
- catalog updated manually without updating canonical editorial source
- metadata exported through a factory renders in runtime/editorial tooling but is skipped by the AI Registry extractor, causing missing `authoringManifestProfiles`
- consumer patched locally instead of fixing registry/editorial chain
- coverage claimed without evidence
- family authoring manifest projected to components without component-level profiles, causing text, numeric, option, temporal, or specialized controls to look semantically identical to agents
- inline overlay panels appear open but cannot be clicked because a CDK backdrop or shared overlay layer sits above the connected overlay pane
- inline overlay panels mix a dark-theme text token with a light overlay surface, or the inverse, because the host skipped the canonical `--pdx-overlay-surface` / `--pdx-overlay-on-surface` bridge
- inline filter controls mix a host-forced Material field surface with package-owned inline text tokens because global `.mat-mdc-form-field` overrides leaked into `pdx-inline-*` controls
- inline select panels lose dark-theme contrast or visible hover because host/global Material select panel tokens override the package-owned `--pdx-inline-panel-*` surface and state tokens
- inline field autosize appears correct in the component but is visually ignored because a consumer shell such as `praxis-filter` forces `width: auto !important`, grid minimums, or field-shell width variables over the package-owned inline width tokens
- inline chips render clear, dropdown/toggle, prefix, or suffix icons in the same visual lane without reserved spacing, causing overlap, redundant actions, or wider-than-needed compact filters

## Validation Guidance

Prefer focused checks in this order:

- registry/component specs
- editorial/metadata contract specs
- catalog derivation specs
- downstream editor/tooling specs where affected
- Playwright or integration evidence when visual discovery is part of the change

Always distinguish:

- runtime coverage
- schema/type coverage
- editor/tooling coverage

Do not collapse them into a single "supported" statement.

## References

Load these only as needed:

- `references/runtime-vs-editorial-chain.md`
- `references/package-owned-vs-host-custom.md`
- `references/coverage-semantics.md`
- `references/downstream-consumers.md`
