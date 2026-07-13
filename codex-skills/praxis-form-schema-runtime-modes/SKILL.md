---
name: praxis-form-schema-runtime-modes
description: Use when Codex must work on @praxisui/dynamic-form or praxis-dynamic-form package schema-driven runtime inputs, resourcePath, schemaUrl, readUrl, submitUrl, submitMethod, create/edit/view modes, initialValue hydration, metadata hot updates, layoutPolicy mode effects, or runtime contract reconciliation.
---

# Praxis Form Schema Runtime Modes

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the runtime contract that turns backend metadata and host inputs into a live `PraxisDynamicForm`. The form runtime is the Angular materialization owner; backend schema semantics remain canonical in `praxis-metadata-starter`, and config persistence remains canonical in `praxis-config-starter`.

## Source Audit

Inspect the real runtime before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/public-api.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.json-api.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.first-config-hydration.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.layout-policy.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-config.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-context.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/dynamic-form-layout.service.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-layout.service.spec.ts`
- `projects/praxis-dynamic-form/docs/hot-metadata-updates.md`
- `projects/praxis-dynamic-form/docs/schema-driven-layout-materialization-rfc.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`

Also inspect these `@praxisui/core` resource/schema services when the behavior depends on `resourcePath`, operation schemas, capabilities, action links, surfaces, read projections, or option sources:

- `projects/praxis-core/src/lib/models/resource-discovery.model.ts`
- `projects/praxis-core/src/lib/models/resolved-crud-operation.model.ts`
- `projects/praxis-core/src/lib/services/crud-operation-resolution.service.ts`
- `projects/praxis-core/src/lib/services/crud-operation-resolution.service.spec.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts`
- `projects/praxis-core/src/lib/services/generic-crud.service.ts`
- `projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts`

## Runtime Contract

Separate these inputs before changing behavior:

- `resourcePath`: base resource contract resolved by Praxis services; do not include `/api`, `/filter`, item ids, or operation URLs.
- `schemaUrl`: explicit schema endpoint; use when a host intentionally bypasses resource-derived schema resolution.
- `readUrl`: explicit entity read endpoint; placeholders require a resource id.
- `submitUrl` + `submitMethod`: canonical explicit submit pair. Do not configure one without the other.
- `responseSchemaUrl`: diagnostic/read-only response contract, not a source for editable command fields.
- `apiEndpointKey` and `apiUrlEntry`: origin resolution inputs for detached overlays/dialogs; do not hardcode API origins in consumers.
- `mode`: `create`, `edit`, or `view`; it controls data lifecycle, not whether customization UI is enabled.
- `initialValue`: create-mode seed or host-provided patch; it must not redefine schema semantics.

For metadata-driven flows, prefer `/schemas/filtered` request/response schemas and operation-aware metadata over host-authored field lists. If table/list works but form fails, inspect id field, schema operation, and resource metadata before adding frontend aliases.

Keep these runtime rules explicit:

- Corporate initialization requires `formId` and either `resourcePath` or `schemaUrl`. Local-only forms may render from explicit local `config`, but should not masquerade as metadata-driven runtime.
- `resourcePath` remains the owner resource path. `schemaUrl`, `readUrl`, `submitUrl`, and `responseSchemaUrl` are concrete operation/surface URLs published by discovery or supplied explicitly.
- Explicit component inputs have precedence over persisted connection/input preferences. Persisted connection can hydrate `resourcePath` only when the host did not provide one.
- `schemaUrl` can initialize schema-backed runtime without `resourcePath`, but command/read/submit behavior still needs the correct operation URLs and resource identity when applicable.
- `readUrl` replaces `crud.getById(...)` for item read surfaces and read projections; when absent, entity hydration falls back to `resourcePath` + `resourceId`; when both are absent, `initialValue` may hydrate local entity state.
- `initialValue` is a runtime value seed or materialized read-projection payload. It must not be used to define fields, validators, option sources, actions, layout ownership, or backend semantics.
- External `config` updates must rebuild/reconcile with server schema without erasing canonical schema-backed metadata. Preserve explicit local fields, but refresh server-backed field semantics from schema.
- Schema status, server hash, ETag, `X-Schema-Hash`, and outdated warnings are diagnostics/governance for drift; do not turn them into local schema forks.
- Runtime/discovery values such as `schemaUrl`, `submitUrl`, and `submitMethod` may be displayed in authoring as read-only diagnostics, but must not be persisted into `DynamicFormAuthoringDocument` bindings or context snapshots.
- Core `ResourceSurfaceOpenAdapterService` and `ResourceActionOpenAdapterService` should materialize widget inputs for schema/read/submit URLs, API origin, mode, form id, and resource id/bindings. Fix these adapters or metadata discovery when surfaces open with incorrect runtime inputs.
- Core `SurfaceOpenMaterializerService` may materialize read projections into Dynamic Form `initialValue` plus transient schema layout policy; this is a runtime projection, not authored local config.

## Mode And Presentation Rules

- `view` is read-only by data lifecycle. `readonlyModeGlobal` can also force read-only behavior.
- `presentationModeGlobal=true` is only effective in `view`; edit/create should render input mode.
- `layoutPolicy.source="schema"` is explicit opt-in for schema-owned layout.
- `intent="detail"` plus `preset="compactPresentation"` belongs to read-only detail summaries.
- `intent="command"` plus grouped command layout belongs to create/edit command forms.
- Command forms must use request schema metadata. Rendering create/edit from response/detail schema is a contract defect, because derived/read-only fields can become editable.
- Detail/read-only summaries should use response schema metadata and may request presentation through `layoutPolicy.intent="detail"` or `preset="compactPresentation"` while keeping `presentationModeGlobal=false` available for traditional readonly controls.
- `layoutPolicy.persistence="transient"` prevents generated schema layout from being persisted as authored local sections. Prefer this for schema-driven command/detail materialization unless the user explicitly detaches/authorizes a layout.
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

Start with focused Dynamic Form runtime specs:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts
```

For hydration, persisted config, runtime context, or `initialValue` behavior:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.first-config-hydration.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/form-context.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/form-config.service.spec.ts
```

For schema layout policy, presentation mode, or generated layout behavior:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.layout-policy.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/dynamic-form-layout.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/form-layout.service.spec.ts
```

For schema/read/submit inputs materialized by resource surfaces/actions or CRUD operation resolution:

```bash
npx ng test praxis-core --watch=false --progress=false \
  --include=projects/praxis-core/src/lib/services/crud-operation-resolution.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts
```

For schema normalization or option metadata that feeds runtime forms:

```bash
npx ng test praxis-core --watch=false --progress=false \
  --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts
```

For public input/export changes, run `npm run build:praxis-dynamic-form` and a direct consumer build when applicable. Use browser validation when mode, presentation, schema-driven layout, or metadata hot update changes visible UX.

State explicitly when live API/browser validation was skipped.

## Companion Skills

- Use `praxis-form-submit-payload-pipeline` for payload normalization and local/transient submit semantics.
- Use `praxis-form-layout-canvas` for `layoutPolicy`, visual blocks, generated presets, and canvas/editor placement.
- Use `praxis-form-editor-document-roundtrip` when runtime inputs are exposed through Settings Panel or authoring documents.
- Use `praxis-fields-runtime-loader` when a schema-backed `controlType` does not render or hot metadata does not reach the field component.
- Use `praxis-fields-option-sources` and `praxis-fields-selection-lookup-controls` when schema metadata materializes `optionSource`, async select, entity lookup, or selection controls.
- Use `praxis-core-resource-runtime` for schema/resource discovery, capabilities, actions, and option sources.
- Use `praxis-metadata-schema-contracts` when `/schemas/filtered`, `schemaUrl`, `schemaId`, `x-ui`, `idField`, `readOnly`, ETag, or `X-Schema-Hash` are missing, stale, or contradictory.
- Use `praxis-metadata-domain-option-sources` when schema-backed option sources, field access, domain governance, entity lookup publication, or by-ids reload are missing or contradictory.
