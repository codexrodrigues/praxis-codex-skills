---
name: praxis-form-runtime-submit
description: Use when Codex must inspect, change, or scaffold @praxisui/dynamic-form runtime behavior: FormConfig, schema-driven field metadata, resourcePath/schemaUrl/readUrl/submitUrl, create/edit/view modes, local versus backend metadata-driven forms, submit payload normalization, local/transient fields, entity lookup payloads, hooks, form actions, and runtime validation.
---

# Praxis Form Runtime Submit

Use this skill for the `@praxisui/dynamic-form` runtime and submit contract. Dynamic Form is the canonical Angular runtime for schema-driven forms and configuration editing, but backend resource semantics remain owned by `praxis-metadata-starter`. Shared form models and services often belong to `@praxisui/core`.

When Dynamic Form is consumed through `@praxisui/manual-form`, use `praxis-manual-form-runtime-bridge` for host template, autosave, toolbar, and metadata bridge behavior. When Dynamic Form is consumed through `@praxisui/editorial-forms` `dataCollection` blocks, use `praxis-editorial-forms-adapters-ai` for adapter binding and `praxis-editorial-forms-runtime` for snapshot/fallback semantics.

## Source Audit

Inspect the real source before changing form runtime behavior:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/public-api.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.ts`
- `projects/praxis-dynamic-form/docs/hot-metadata-updates.md`

Also inspect `@praxisui/core` models/services when the change touches `FormConfig`, `FieldMetadata`, `DynamicFormService`, schema metadata, hooks, global actions, effect policies, layout policy, or submit events.

## Runtime Modes

Separate the target mode before designing a fix:

- Local-only: local `config` and `fieldMetadata`; no backend schema discovery is required.
- Backend metadata-driven: `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, mode, entity id, and schema metadata govern runtime behavior.
- Authored/customizable: runtime config is editable and may be persisted through Settings Panel/config storage.

Do not create DTO/backend fields for local-only or transient UX state already supported by Angular runtime. Use `source: "local"`, `transient: true`, or `submitPolicy` where the field is intentionally local.

## Submit Contract

Use the canonical payload pipeline:

- normalize date arrays and local datetime strings before submit.
- omit `source: "local"` and `transient: true` fields unless `submitPolicy` explicitly includes them.
- support `submitPolicy: "include" | "omit" | "includeWhenDirty"`.
- omit empty optional fields when they were not dirty.
- serialize entity lookup values through the shared core helper, respecting `payloadMode`, `multiple`, and `optionSource.entityKey`.
- filter nested array item fields recursively using their item schema metadata.

Do not patch around submit gaps in hosts. If backend submission fails, first inspect whether field metadata, option source, submit policy, DTO schema, or metadata starter contract is wrong.

## Platform Aderence Inventory

Before adding an input, output, config key, service, hook, field shape, submit transform, or public export, classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public contract. Prefer materializing existing metadata, `FormConfig`, field metadata, submit policy, hooks, or core services before inventing a host-specific convention.

## Validation

- submit payload: `prepare-submit-payload.spec.ts`, `normalize-submit-payload.spec.ts`, `normalize-date-arrays.spec.ts`
- runtime hydration or metadata: `praxis-dynamic-form.*hydration*.spec.ts`, `form-context.service.spec.ts`, `form-config.service.spec.ts`
- form rules or hooks affecting runtime: focused service specs plus `praxis-dynamic-form.spec.ts`
- schema-driven runtime: `praxis-dynamic-form.metadata.spec.ts`, metadata update specs, and browser flow when UI materialization matters
- public API/exported contract: `npm run build:praxis-dynamic-form` plus a direct consumer when applicable

## Companion Skills

- Use `praxis-form-layout-canvas` for layout policy, schema-driven layout, visual blocks, and canvas.
- Use `praxis-form-authoring-settings` for config editors, Settings Panel, apply/save/reset, JSON editor, hooks/messages/actions editors, and round-trip.
- Use `praxis-form-ai-rules-validation` for AI manifests, rules, context packs, component edit plans, diagnostics, and registry validation.
- Use `praxis-core-resource-runtime` for schema/resource discovery, option sources, capabilities, actions, and submit/read contract grounding.
- Use `praxis-dynamic-fields-editorial` for field component metadata, option sources, async select, entity lookup, and custom field coverage.
- Use `praxis-manual-form-runtime-bridge` when a manual-form wrapper owns the host template and persistence.
- Use `praxis-editorial-forms-adapters-ai` when a dynamic form is rendered as an editorial `dataCollection` adapter.
