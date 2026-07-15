---
name: praxis-fields-runtime-loader
description: Use when changing or reviewing @praxisui/dynamic-fields or praxis-dynamic-fields package runtime rendering, DynamicFieldLoaderDirective behavior, ComponentRegistryService registrations, controlType normalization, selector mappings, package-owned field loading, host custom field registration, hot metadata updates, or runtime coverage claims for metadata-driven Angular fields.
---

# Praxis Fields Runtime Loader

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill for runtime field rendering in `@praxisui/dynamic-fields`. Treat the loader and registry as the canonical Angular runtime for metadata-driven fields; do not patch consumers with local `controlType` maps when the issue belongs in the package registry, selector registry, or field component.

Pair it with `praxis-fields-inline-overlay-runtime` for compact inline overlay behavior,
`praxis-fields-text-number-time-controls` for scalar/temporal control semantics,
`praxis-fields-selection-lookup-controls` for option-bearing controls, and
`praxis-fields-control-profile-ai` when runtime coverage must be reflected in AI profiles or generated registry docs.

When locating files, first resolve the Angular workspace root. Paths below are relative to
`praxis-ui-angular/projects/praxis-dynamic-fields` unless they explicitly start with
`projects/praxis-core/`.

## Canonical Runtime Chain

Audit this chain before editing:

1. `@praxisui/core` owns `FieldControlType`, aliases, inline control utilities, selector registry tokens/providers, `DEFAULT_FIELD_SELECTOR_CONTROL_TYPE_MAP`, and shared `FieldMetadata`.
2. `FieldSelectorRegistry` owns selector-to-`FieldControlType` resolution. It normalizes selector keys, applies base and override maps, and is the canonical place for package selector defaults or intentional host overrides.
3. `ComponentRegistryService` owns runtime `controlType -> lazy component` resolution, default package registrations, control type normalization, and registration of default selectors into `FieldSelectorRegistry`.
4. `ComponentPreloaderService` owns optional preloading over the same registry contract; it must not introduce a second field discovery source.
5. `DynamicFieldLoaderDirective` owns rendering, `FormGroup` binding, shell wrapping, lifecycle cleanup, hot metadata refresh, presentation/global states, select rebinding, and render error events.
6. The field component owns CVA/form-control behavior and `setInputMetadata`, `setExternalControl`, or signal-based metadata updates.
7. Host custom fields use `ComponentRegistryService.register(...)`; package-owned fields must be fixed in the package-owned registry path.

If a field can render only because a host imports or maps it manually, classify that as a registry gap unless the field is intentionally host custom.

## Required Inventory

Inspect the affected files, not only docs:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `src/public-api.ts`
- `README.md`
- `docs/dynamic-fields-inventory.md`
- `docs/dynamic-fields-field-catalog.md`
- `docs/dynamic-fields-field-selection-guide.md`
- `src/lib/services/component-registry/component-registry.service.ts`
- `src/lib/services/component-registry/component-registry.interface.ts`
- `src/lib/services/component-preloader.service.ts`
- `src/lib/directives/dynamic-field-loader.directive.ts`
- `src/lib/providers.ts`
- `src/lib/catalog/**`
- `src/lib/ai/control-type-ai-catalog.spec.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts`
- relevant `src/lib/components/**` component, `*.metadata.ts`, and `*.json-api.md`
- `src/lib/base/**` for shared input/select behavior
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- `projects/praxis-core/src/lib/services/field-selector-registry.service.ts` and spec when changing selector defaults or overrides
- `projects/praxis-core/src/lib/metadata/field-selector-control-type.constants.ts`
- `projects/praxis-core/src/lib/providers/field-selector-registry.providers.ts`
- `projects/praxis-core/src/lib/tokens/field-selector-registry.token.ts`
- `projects/praxis-core/src/lib/**` when changing `FieldControlType`, aliases, selector defaults, inline controls, or shared metadata
- docs/inventory/catalog files when a runtime claim changes

## Runtime Decision Rules

- Prefer a canonical `FieldControlType` from `@praxisui/core`; add aliases only when they normalize deterministically to one existing type and the alias belongs in core.
- Treat control-type normalization fallback as a compatibility warning, not support. A control is canonically supported only when the requested selector/control type resolves through `FieldSelectorRegistry` or `FieldControlType` aliases to a registered package component without relying on the registry returning the raw unknown string.
- Do not use a successful `normalizeControlType(...)` call, a preserved raw token, or an absence of thrown errors as runtime coverage evidence. The fallback path exists to preserve the requested value for logging and `renderError` diagnostics; support claims require `ComponentRegistryService.isRegistered(...)` or an actual `getComponent(...)` resolution to a registered lazy component.
- Register package-owned fields in `ComponentRegistryService.initializeDefaultComponents()` with lazy imports; do not solve package-owned fields through host bootstrap code.
- Keep `ComponentPreloaderService` aligned with registry semantics. Preload should exercise registrations, caching, and failures, not become a side catalog.
- Keep selector resolution in `FieldSelectorRegistry`, `DEFAULT_FIELD_SELECTOR_CONTROL_TYPE_MAP`, `provideFieldSelectorRegistryBase(...)`, `provideFieldSelectorRegistryOverride(...)`, or explicit runtime registration through `provideFieldSelectorRegistryRuntime(...)`. Disable defaults only at the intended root provider boundary.
- If selector defaults are disabled or a base selector map replaces package defaults, the host now owns that registration boundary. Do not silently recreate package defaults locally; document the provider boundary and prove the host override still resolves every required package-owned selector.
- Do not add consumer-local selector maps to compensate for missing package-owned selectors. Add the selector default in core when it is canonical, or use an override only when the host intentionally owns that selector.
- Keep the registry boundary two-step: selector resolution produces a `FieldControlType`; component resolution maps that `FieldControlType` to a lazy component. Do not collapse this into a direct selector-to-component lookup.
- Missing component resolution must surface through `renderError`/diagnostics with the requested and normalized `controlType`; do not replace an unregistered package-owned component with a visually similar fallback just to keep the form rendering.
- Preserve `DynamicFieldLoaderDirective` reentrancy, component disposal, shell lifecycle, subscriptions, `enableExternalControlBinding`, and render error event shape.
- Preserve in-place metadata updates for same render shape, `FormGroup` rebind without component recreation, and explicit skip-snapshot behavior for metadata changes that should not reset existing value/control state. If a component lacks `setInputMetadata`, writable metadata signal, or compatible external control binding, classify it as partial loader coverage until the refresh/rebind path is implemented or explicitly documented as unsupported.
- Require form compatibility: `ControlValueAccessor`, `[formControl]`, or `setExternalControl` must work with dynamic forms.
- Require hot metadata compatibility for fields used in editors/builders: `setInputMetadata`, writable metadata signal, or equivalent documented refresh path.
- Keep provider variants intentional: default packages should register package-owned controls, while no-defaults providers are for hosts that deliberately own registration boundaries.
- For wrapper controls such as upload, rich content, and CRON, verify runtime registration here but route value-shape and package-specific semantics to the owning wrapper skill.

## Coverage Semantics

Do not say "supported" unless the correct layer is true:

- `runtime coverage`: `ComponentRegistryService.isRegistered(controlType)` resolves the component and loader renders it.
- `schema/type coverage`: `FieldMetadata`, `FieldControlType`, aliases, selector mapping, selector providers/tokens, and public exports support the type.
- `editor/tooling coverage`: metadata/editorial registries, catalogs, AI profiles, and downstream builders can discover it.
- `preload coverage`: `ComponentPreloaderService` can preload the same package-owned field through registry resolution without duplicate discovery data.

Runtime-only support is valid for some host custom fields, but package-owned fields should normally progress through all three layers. When authoring catalogs or AI profiles, never infer package support from normalization aliases alone; cross-check the registered component list and the loader path that would emit `component_missing` for an unregistered control.

Published catalog/playground entries are runtime claims, not just documentation. Keep
`dynamic-fields-playground.catalog.spec.ts` proving every published `controlType` resolves through
`ComponentRegistryService.getComponent(...)`. If an entry only exists in docs, selector defaults,
or AI catalogs but `getComponent(...)` returns `null`, classify it as partial/declared-only and fix
registry registration before using it as migration guidance.

## Validation

Use the smallest sufficient checks:

- Registry/default registration/selector/preload changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/services/component-registry/component-registry.service.spec.ts`
  - `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/services/field-selector-registry.service.spec.ts` when selector defaults or aliases change.
- Loader lifecycle, hot metadata, global state, presentation mode, skip snapshot, or select rebind changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.directive.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.metadata-refresh.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader-global-states.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.presentation-mode.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.skip-snapshot.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.select-rebind.spec.ts`
- Field component changes:
  - Run the component spec plus the loader smoke above when CVA, `[formControl]`, `setExternalControl`, shell wrapping, or metadata refresh behavior changed.
- Catalog/editorial/AI coverage changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts`
- Inline/filter rendering:
  - Select the relevant `projects/praxis-dynamic-fields/test-dev/e2e/*.playwright.spec.ts`; use `inline-all-components-smoke.playwright.spec.ts` when the change affects broad runtime registration or loader behavior.
- Dynamic-form or metadata-editor materialization:
  - Run consumer specs only when loader behavior, control metadata, or public control type coverage changes the downstream rendering path.
- Public API or package-owned `controlType` changes:
  - `npm run build:praxis-dynamic-fields`
  - Build at least one direct consumer when feasible.

Also update governed inventory/catalog docs when runtime registration, aliases, selectors, or coverage changes. Declare explicitly when no derived artifact needs updating.
