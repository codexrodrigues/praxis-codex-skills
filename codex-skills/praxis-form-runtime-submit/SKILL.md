---
name: praxis-form-runtime-submit
description: Use when Codex must inspect, change, or scaffold @praxisui/dynamic-form or praxis-dynamic-form package runtime behavior: FormConfig, schema-driven field metadata, resourcePath/schemaUrl/readUrl/submitUrl, create/edit/view modes, local versus backend metadata-driven forms, submit payload normalization, local/transient fields, entity lookup payloads, hooks, form actions, and runtime validation.
---

# Praxis Form Runtime Submit

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the `@praxisui/dynamic-form` runtime and submit contract. Dynamic Form is the canonical Angular runtime for schema-driven forms and configuration editing, but backend resource semantics remain owned by `praxis-metadata-starter`. Shared form models and services often belong to `@praxisui/core`.

When Dynamic Form is consumed through `@praxisui/manual-form`, use `praxis-manual-form-runtime-bridge` for host template, autosave, toolbar, and metadata bridge behavior. When Dynamic Form is consumed through `@praxisui/editorial-forms` `dataCollection` blocks, use `praxis-editorial-forms-adapters-ai` for adapter binding and `praxis-editorial-forms-runtime` for snapshot/fallback semantics. When a dynamic form field performs operational upload through `pdx-material-files-upload`, use `praxis-files-upload-form-field` for `valueMode`, ControlValueAccessor behavior, and upload field UX, plus `praxis-files-upload-backend-contract` when the submit payload depends on backend file ids or metadata.
When form layouts, helper content, previews, or rich inputs use `RichContentDocument`, use `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters`; do not submit arbitrary HTML or markdown when the platform expects structured rich content.
When a dynamic form field edits CRON or schedule values through `@praxisui/cron-builder`, use `praxis-cron-builder-form-field` for CVA/form integration and `praxis-cron-schedule-authoring` for the payload choice between legacy CRON string and `ScheduleAuthoringConfig`.
For narrower runtime work, prefer `praxis-form-schema-runtime-modes` for schema URLs/modes/hydration, `praxis-form-submit-payload-pipeline` for payload normalization, `praxis-form-actions-hooks-runtime` for actions/hooks, and `praxis-form-editor-document-roundtrip` for editor document persistence.

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

- Use `praxis-form-schema-runtime-modes` for `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, `submitMethod`, create/edit/view modes, `initialValue`, metadata hot updates, and runtime reconciliation.
- Use `praxis-form-submit-payload-pipeline` for `prepareSubmitPayload`, `normalizeSubmitPayload`, date arrays, local/transient fields, `submitPolicy`, entity lookup payloads, and nested array submits.
- Use `praxis-form-actions-hooks-runtime` for form actions, hooks, global action payloads, shortcuts, surface opens, and action editor runtime behavior.
- Use `praxis-form-editor-document-roundtrip` for `DynamicFormAuthoringDocument`, bindings, context snapshots, Settings Panel apply/save/reset, and editor round-trip.
- Use `praxis-form-layout-canvas` for layout policy, schema-driven layout, visual blocks, and canvas.
- Use `praxis-form-authoring-settings` for config editors, Settings Panel, apply/save/reset, JSON editor, hooks/messages/actions editors, and round-trip.
- Use `praxis-form-ai-rules-validation` for AI manifests, rules, context packs, component edit plans, diagnostics, and registry validation.
- Use `praxis-core-resource-runtime` for schema/resource discovery, option sources, capabilities, actions, and submit/read contract grounding.
- Use `praxis-dynamic-fields-editorial` for field component metadata, option sources, async select, entity lookup, and custom field coverage.
- Use `praxis-files-upload-form-field` for upload field `valueMode`, metadata/id submit shape, ControlValueAccessor behavior, and dynamic-form upload integration.
- Use `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters` for rich helper content, previews, or structured rich-input documents embedded in form flows.
- Use `praxis-cron-builder-form-field` and `praxis-cron-schedule-authoring` for schedule fields, CRON compatibility values, structured schedule configs, timezone/locale metadata, and validation diagnostics in submit flows.
- Use `praxis-manual-form-runtime-bridge` when a manual-form wrapper owns the host template and persistence.
- Use `praxis-editorial-forms-adapters-ai` when a dynamic form is rendered as an editorial `dataCollection` adapter.
