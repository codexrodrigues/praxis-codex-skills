---
name: praxis-editorial-forms-runtime
description: Use when implementing or auditing `@praxisui/editorial-forms` runtime behavior, including `EditorialFormRuntimeComponent`, `EditorialRuntimeInput`, guided journeys, resolved snapshots, fallback state, operational diagnostics/events, presentation schema, theme tokens, stepper behavior, i18n, runtime context, experiments/labs, and the boundary between editorial domain and generic `FormConfig`.
---

# Praxis Editorial Forms Runtime

Use this skill when a form experience is an editorial journey rather than a flat schema-driven form. `@praxisui/editorial-forms` is the canonical runtime for solution, journey, step, block, snapshot, fallback, presentation, and operational diagnostics.

For focused work, load the narrow companion first:

- `praxis-editorial-forms-journey-snapshot-runtime` for `EditorialRuntimeInput`, solution/instance/context merge, journey and step resolution, presets, overrides, block provenance, and `snapshotChange`.
- `praxis-editorial-forms-presentation-diagnostics` for fallback state, diagnostics, operational events, `solution.presentation`, theme tokens, stepper behavior, unsupported presentation keys, and i18n.
- `praxis-editorial-forms-data-collection-adapters` for `dataCollection` readiness, adapter registry, dynamic-form adapter, config lookup, adapter events, and `runtimeContext.formData`.
- `praxis-editorial-forms-agentic-authoring` for manifest-backed snapshot/fallback/presentation authoring, component metadata, registry, docs, and labs.

## Canonical Boundary

`@praxisui/editorial-forms` owns:

- `EditorialFormRuntimeComponent`
- `EditorialRuntimeInput`
- `EditorialRuntimeHostConfig`
- `EditorialRuntimeState`
- resolved snapshots and provenance
- fallback derivation from diagnostics
- operational events
- presentation helpers and theme token mapping
- block renderers and stepper behavior
- package i18n provider/dictionaries

`@praxisui/core` owns shared editorial domain contracts such as `EditorialSolutionDefinition` and `EditorialTemplateInstance`. `@praxisui/dynamic-form` may render `dataCollection` blocks only through optional adapters; it must not become the primary language of the editorial runtime.
When editorial presentation or narrative blocks use `RichContentDocument`, pair with `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters`; do not invent an editorial-only rich content dialect.

## Required Source Audit

Inspect:

- `projects/praxis-editorial-forms/AGENTS.md`
- `README.md`
- `docs/architecture.md`
- `docs/editorial-authoring-playbook.md`
- `docs/recovery-playbook.md`
- `src/public-api.ts`
- `src/lib/editorial-runtime.contract.ts`
- `src/lib/editorial-form-runtime.component.ts`
- `src/lib/runtime/editorial-runtime-state.ts`
- `src/lib/runtime/editorial-preset-resolver.ts`
- `src/lib/runtime/editorial-runtime-snapshot.model.ts`
- `src/lib/runtime/editorial-runtime-fallback.ts`
- `src/lib/runtime/editorial-runtime-diagnostics.model.ts`
- `src/lib/runtime/editorial-runtime-events.model.ts`
- `src/lib/runtime/editorial-runtime-presentation.helpers.ts`
- `src/lib/runtime/editorial-runtime-theme.helpers.ts`
- affected renderer specs and E2E labs when relevant

## Runtime Rules

- Treat `solution`, `instance`, and `runtimeContext` as inputs that resolve into `EditorialRuntimeSnapshot`.
- Keep `snapshotChange`, `fallbackChange`, and `operationalEvent` stable host-facing outputs.
- Derive fallback from diagnostics with modes `normal`, `warning`, `degraded`, and `blocked`; do not persist fallback as hidden domain truth.
- Unsupported `presentation` keys must emit diagnostics instead of pretending visual support.
- Presentation changes belong under `solution.presentation` and must not mutate journeys, blocks, `FormConfig`, `FieldMetadata`, or collected data.
- Preserve block provenance and deterministic override operations: append, insertBefore, insertAfter, replace, and remove.
- Keep `runtimeContext.formData` as governed runtime state shared by selection blocks, data collection adapters, review sections, and snapshots.
- Use `PraxisI18nService` and package dictionaries for internal runtime text.

## Inventory Before New Contract

Before adding public fields, metadata ports, runtime types, diagnostics, or adapter contracts, classify the need:

- `ja-suportado-so-ux`: snapshot, fallback, presentation, adapter, or event evidence exists but a host, lab, docs page, or renderer does not show it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer models editorial state as page-builder, dynamic-form, wizard, or host-local config while the editorial runtime already owns it.
- `suportado-parcialmente`: the owner exists but snapshot merge, presentation coverage, adapter readiness, event forwarding, docs, or focused validation is incomplete.
- `lacuna-real-de-contrato`: no existing solution/instance/context, snapshot, diagnostic, presentation key, adapter API, event payload, or component metadata port can express the requirement.

Only `lacuna-real-de-contrato` justifies a new public contract. Otherwise correct the editorial runtime owner or its projection.

## When Not To Use Dynamic Form

Do not collapse editorial requirements into `FormConfig.sections`, rows, columns, or a generic technical form editor. If a requirement needs journey, narrative, compliance context, fallback, diagnostic provenance, or host operational events, evolve the editorial domain/runtime or adapter.

## Validation

Minimum gates:

- compile: `npm run build:praxis-editorial-forms`
- runtime component: `src/lib/editorial-form-runtime.component.spec.ts`
- snapshot/presets: `src/lib/runtime/editorial-preset-resolver.spec.ts`
- fallback: `src/lib/runtime/editorial-runtime-fallback.spec.ts`
- presentation/theme: `src/lib/runtime/editorial-runtime-theme.helpers.spec.ts`
- renderers: focused `src/lib/renderers/*.spec.ts`
- host/lab proof: `test-dev/e2e/*.playwright.spec.ts` when runtime experiments, labs, or host integration change

Review public API, README, docs manifest, architecture docs, and examples when host-facing runtime behavior changes.
