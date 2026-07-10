---
name: praxis-form-schema-runtime-modes
description: Use when Codex must work on @praxisui/dynamic-form schema-driven runtime inputs, resourcePath, schemaUrl, readUrl, submitUrl, submitMethod, create/edit/view modes, initialValue hydration, metadata hot updates, layoutPolicy mode effects, or runtime contract reconciliation.
---

# Praxis Form Schema Runtime Modes

Use this skill for the runtime contract that turns backend metadata and host inputs into a live `PraxisDynamicForm`. The form runtime is the Angular materialization owner; backend schema semantics remain canonical in `praxis-metadata-starter`, and config persistence remains canonical in `praxis-config-starter`.

## Source Audit

Inspect the real runtime before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/public-api.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.ts`
- `projects/praxis-dynamic-form/docs/hot-metadata-updates.md`
- `projects/praxis-dynamic-form/docs/schema-driven-layout-materialization-rfc.md`

Also inspect `@praxisui/core` resource/schema services when the behavior depends on `resourcePath`, operation schemas, capabilities, action links, or option sources.

## Runtime Contract

Separate these inputs before changing behavior:

- `resourcePath`: base resource contract resolved by Praxis services; do not include `/api`, `/filter`, item ids, or operation URLs.
- `schemaUrl`: explicit schema endpoint; use when a host intentionally bypasses resource-derived schema resolution.
- `readUrl`: explicit entity read endpoint; placeholders require a resource id.
- `submitUrl` + `submitMethod`: canonical explicit submit pair. Do not configure one without the other.
- `mode`: `create`, `edit`, or `view`; it controls data lifecycle, not whether customization UI is enabled.
- `initialValue`: create-mode seed or host-provided patch; it must not redefine schema semantics.

For metadata-driven flows, prefer `/schemas/filtered` request/response schemas and operation-aware metadata over host-authored field lists. If table/list works but form fails, inspect id field, schema operation, and resource metadata before adding frontend aliases.

## Mode And Presentation Rules

- `view` is read-only by data lifecycle. `readonlyModeGlobal` can also force read-only behavior.
- `presentationModeGlobal=true` is only effective in `view`; edit/create should render input mode.
- `layoutPolicy.source="schema"` is explicit opt-in for schema-owned layout.
- `intent="detail"` plus `preset="compactPresentation"` belongs to read-only detail summaries.
- `intent="command"` plus grouped command layout belongs to create/edit command forms.
- External `config` or metadata updates must rebuild or reconcile the runtime without erasing canonical schema-backed metadata.

Do not create `FormConfig.sections` or `sections: []` merely to make a schema-driven form initialize. If generated layout is weak, classify the gap and fix metadata/runtime materialization.

## Aderence Inventory

Before creating any input, config key, endpoint convention, or public export, classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Most schema/mode issues are already supported by runtime inputs, schema metadata, `layoutPolicy`, `initialValue`, or authoring snapshots. Only add a contract when the behavior cannot be expressed by those canonical surfaces.

## Validation

- schema runtime: `praxis-dynamic-form.metadata.spec.ts`, hydration specs, metadata update specs
- mode/read/submit wiring: focused `praxis-dynamic-form.spec.ts` cases around `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, `submitMethod`, and `initialValue`
- schema layout policy: `dynamic-form-layout.service.spec.ts`, `form-layout.service.spec.ts`
- public input/export changes: `npm run build:praxis-dynamic-form` and a direct consumer build when applicable
- browser validation when mode, presentation, or metadata hot update changes visible UX

State explicitly when live API/browser validation was skipped.

## Companion Skills

- Use `praxis-form-submit-payload-pipeline` for payload normalization and local/transient submit semantics.
- Use `praxis-form-layout-canvas` for `layoutPolicy`, visual blocks, generated presets, and canvas/editor placement.
- Use `praxis-form-editor-document-roundtrip` when runtime inputs are exposed through Settings Panel or authoring documents.
- Use `praxis-fields-runtime-loader` when a schema-backed `controlType` does not render or hot metadata does not reach the field component.
- Use `praxis-fields-option-sources` and `praxis-fields-selection-lookup-controls` when schema metadata materializes `optionSource`, async select, entity lookup, or selection controls.
- Use `praxis-core-resource-runtime` for schema/resource discovery, capabilities, actions, and option sources.
