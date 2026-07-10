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

## Canonical Runtime Chain

Audit this chain before editing:

1. `@praxisui/core` owns `FieldControlType`, aliases, inline control utilities, selector registry tokens, and shared `FieldMetadata`.
2. `ComponentRegistryService` owns runtime `controlType -> lazy component` resolution and default package registrations.
3. `DynamicFieldLoaderDirective` owns rendering, `FormGroup` binding, shell wrapping, lifecycle cleanup, hot metadata refresh, and render error events.
4. The field component owns CVA/form-control behavior and `setInputMetadata` or signal-based metadata updates.
5. Host custom fields use `ComponentRegistryService.register(...)`; package-owned fields must be fixed in the package-owned registry path.

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
- `src/lib/directives/dynamic-field-loader.directive.ts`
- `src/lib/providers.ts`
- relevant `src/lib/components/**` component, `*.metadata.ts`, and `*.json-api.md`
- `src/lib/base/**` for shared input/select behavior
- `projects/praxis-core/src/lib/**` when changing `FieldControlType`, aliases, selector defaults, inline controls, or shared metadata
- docs/inventory/catalog files when a runtime claim changes

## Runtime Decision Rules

- Prefer a canonical `FieldControlType` from `@praxisui/core`; add aliases only when they normalize deterministically to one existing type and the alias belongs in core.
- Register package-owned fields in `ComponentRegistryService.initializeDefaultComponents()` with lazy imports; do not solve package-owned fields through host bootstrap code.
- Keep selector resolution in `FieldSelectorRegistry`, `DEFAULT_FIELD_SELECTOR_CONTROL_TYPE_MAP`, or explicit host override. Disable defaults only at the intended root provider boundary.
- Preserve `DynamicFieldLoaderDirective` reentrancy, component disposal, shell lifecycle, subscriptions, `enableExternalControlBinding`, and render error event shape.
- Require form compatibility: `ControlValueAccessor`, `[formControl]`, or `setExternalControl` must work with dynamic forms.
- Require hot metadata compatibility for fields used in editors/builders: `setInputMetadata`, writable metadata signal, or equivalent documented refresh path.
- Keep provider variants intentional: default packages should register package-owned controls, while no-defaults providers are for hosts that deliberately own registration boundaries.
- For wrapper controls such as upload, rich content, and CRON, verify runtime registration here but route value-shape and package-specific semantics to the owning wrapper skill.

## Coverage Semantics

Do not say "supported" unless the correct layer is true:

- `runtime coverage`: `ComponentRegistryService.isRegistered(controlType)` resolves the component and loader renders it.
- `schema/type coverage`: `FieldMetadata`, `FieldControlType`, aliases, selector mapping, and public exports support the type.
- `editor/tooling coverage`: metadata/editorial registries, catalogs, AI profiles, and downstream builders can discover it.

Runtime-only support is valid for some host custom fields, but package-owned fields should normally progress through all three layers.

## Validation

Use the smallest sufficient checks:

- registry changes: `component-registry.service.spec.ts`
- loader changes: `dynamic-field-loader*.spec.ts`
- field component changes: the component spec plus loader smoke when binding behavior changed
- inline/filter rendering: relevant `test-dev/e2e/*.playwright.spec.ts`
- dynamic-form or metadata-editor materialization: consumer specs only when loader behavior or control metadata changed the downstream rendering path
- public API or package-owned `controlType` changes: build `praxis-dynamic-fields` and at least one direct consumer when feasible

Also update governed inventory/catalog docs when runtime registration, aliases, selectors, or coverage changes. Declare explicitly when no derived artifact needs updating.
