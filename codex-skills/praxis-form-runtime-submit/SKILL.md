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
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.json-api.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-layout.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`
- `projects/praxis-dynamic-form/docs/hot-metadata-updates.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`

Also inspect these `@praxisui/core` models/services when the change touches `FormConfig`, `FieldMetadata`, `DynamicFormService`, schema metadata, hooks, global actions, effect policies, layout policy, or submit events:

- `projects/praxis-core/src/lib/models/form/form-events.model.ts`
- `projects/praxis-core/src/lib/models/resolved-crud-operation.model.ts`
- `projects/praxis-core/src/lib/services/crud-operation-resolution.service.ts`
- `projects/praxis-core/src/lib/services/crud-operation-resolution.service.spec.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts`
- `projects/praxis-core/src/lib/services/dynamic-form.service.ts`
- `projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts`

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

## Runtime Submit Semantics

Keep these runtime boundaries explicit:

- `onSubmit()` is the canonical runtime entrypoint. Guard duplicate submits with `submitting` and block submit while `entityHydrationPending` is true.
- Run `beforeValidate` before invalid checks. For invalid forms, mark controls touched, update validity, optionally focus/scroll the first invalid control, run `afterValidate`, and do not emit HTTP or CRUD requests.
- Run `afterValidate` for valid forms, then `beforeSubmit` as the cancelable hook. `beforeSubmit` must run before snapshotting form values so hook mutations can affect the payload.
- Snapshot `rawFormData` from `form.getRawValue()` only after cancelable hooks complete, then derive `formData` with `prepareSubmitPayload(...)` and current dirty paths.
- Emit `formSubmit` with `stage: "before"` before executing the request, `stage: "after"` on success, and `stage: "error"` on request failure. Preserve both `formData` and `rawFormData` in every stage.
- Resolve operation from submit method first: `post` -> `create`, `put` -> `update`, `patch` -> `patch`. Without explicit method, use `resourceId` to choose update versus create.
- Treat `submitUrl` and `submitMethod` as a pair. If both are present, execute the canonical HTTP request against the resolved API origin; if neither is present, the runtime may use the legacy/inferred CRUD service path; if only one is present, fail explicitly instead of guessing.
- Only `post`, `put`, and `patch` are Dynamic Form submit methods. Do not add local delete submit handling here; delete belongs to action/surface orchestration.
- When a related child surface materializes a full CRUD experience, create/edit form targets may carry `submitUrl`/`submitMethod` into CRUD action metadata, and delete may be represented as a CRUD action with its own submit target. Keep that delete contract in the CRUD/action materialization layer; do not retrofit `praxis-dynamic-form` to submit `delete` or persist delete targets as form authoring state.
- Resolve `{id}` placeholders with `resourceId` or pending entity id. Missing entity id for a templated submit URL is a runtime contract failure, not a reason to synthesize a path locally.
- `submitUrl`, `submitMethod`, `schemaUrl`, `readUrl`, `responseSchemaUrl`, `apiEndpointKey`, and `apiUrlEntry` are runtime inputs produced by resource/surface/action discovery. They may be shown as read-only diagnostics in authoring, but must not be persisted into `DynamicFormAuthoringDocument` bindings or context snapshots.
- Surface/action adapters in `@praxisui/core` are responsible for materializing canonical `submitUrl` and `submitMethod` into Dynamic Form widget inputs. Fix those adapters or metadata discovery when a form opens with the wrong write target.
- `formSubmit.formData` is the persistence payload. `formSubmit.rawFormData` exists for diagnostics, UI hooks, and local/transient context only.
- `afterSubmit` receives `{ result, formData, rawFormData, operation }`; `onError` receives `{ error, formData, rawFormData, operation }`. Do not make hooks depend on host-only globals when the runtime already provides the canonical context.
- Success behavior such as configured snack messages, `clearAfterSave`, and `redirectAfterSave` happens after a successful request. Keep navigation failures logged and non-fatal.
- If entity lookup dependency policy blocks retained values, submit must remain invalid and no HTTP/CRUD request should run. If policy allows retained legacy values or reset-on-dependency-change marks fields dirty, submit should preserve the canonical value/null/empty-array shape through the payload pipeline.

When a migration needs less cognitive work from implementers, prefer strengthening metadata discovery, surface/action materialization, request schema, or Dynamic Form runtime diagnostics over writing host glue code.

## Platform Aderence Inventory

Before adding an input, output, config key, service, hook, field shape, submit transform, or public export, classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public contract. Prefer materializing existing metadata, `FormConfig`, field metadata, submit policy, hooks, or core services before inventing a host-specific convention.

## Validation

Start with focused Dynamic Form runtime specs:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts
```

For payload behavior inside submit, add the focused payload specs:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.spec.ts
```

For runtime hydration, context, or config persistence:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.first-config-hydration.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/form-context.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/form-config.service.spec.ts
```

For submit targets materialized by resource actions, surfaces, or CRUD operation resolution:

```bash
npx ng test praxis-core --watch=false --progress=false \
  --include=projects/praxis-core/src/lib/services/crud-operation-resolution.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts
```

For rules or hooks affecting runtime submit, add focused service specs before browser validation:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/services/form-rules.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.spec.ts
```

For public API/exported contract changes, run `npm run build:praxis-dynamic-form` plus a direct consumer when applicable. Use Playwright only after unit tests prove the runtime behavior, choosing the smallest flow that exercises schema-driven open, submit HTTP, invalid form handling, or action-triggered surface open.

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
