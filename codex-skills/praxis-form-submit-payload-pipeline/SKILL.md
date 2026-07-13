---
name: praxis-form-submit-payload-pipeline
description: Use when Codex must inspect, change, or test @praxisui/dynamic-form or praxis-dynamic-form package submit payload normalization, prepareSubmitPayload, normalizeSubmitPayload, normalizeDateArrays, local/transient fields, submitPolicy, entity lookup payloadMode, dirty-field filtering, nested array item schemas, or submit validation.
---

# Praxis Form Submit Payload Pipeline

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the canonical client-side submit pipeline of `@praxisui/dynamic-form`. The submit payload is a projection of form value plus field metadata; do not patch payload shape in host components when the issue belongs to metadata, `@praxisui/core`, or backend DTO/schema semantics.

## Source Audit

Inspect these files before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.json-api.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`

Inspect these `@praxisui/core` files before changing field submit or lookup payload contracts:

- `projects/praxis-core/src/lib/models/component-metadata.interface.ts`
- `projects/praxis-core/src/lib/models/material-field-metadata.interface.ts`
- `projects/praxis-core/src/lib/models/option-source.model.ts`
- `projects/praxis-core/src/lib/models/option-source.model.spec.ts`
- `projects/praxis-core/src/lib/models/form/form-config.model.ts`
- `projects/praxis-core/src/lib/models/form/form-config.model.spec.ts`

Use browser specs only after unit behavior is proven. Relevant smoke candidates include:

- `projects/praxis-dynamic-form/test-dev/e2e/funcionarios-form-demo-select-interaction.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/funcionarios-form-demo-rules.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/funcionarios-form-demo-domain-rules.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/business-rules-form-demo.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-command-rules.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/surface-open-form-demo.playwright.spec.ts`

## Payload Rules

The canonical order is:

1. Normalize date arrays.
2. Normalize local datetime strings by adding the local ISO offset when missing.
3. Filter fields according to metadata.
4. Serialize entity lookup values through the shared core helper.
5. Recurse into array item schemas.

Respect these semantics:

- The submit payload is a projection of raw form value plus `FieldMetadata`, dirty paths, and the request schema; host components must not add local payload transforms for canonical cases.
- `source: "local"` and `transient: true` are omitted by default.
- `submitPolicy: "include" | "omit" | "includeWhenDirty"` overrides the default omission policy.
- Legacy `"never"` may be defensively normalized to `"omit"`, but the public contract remains `"omit"`.
- Empty optional fields are omitted when they were not dirty.
- Required fields, dirty fields, and nested dirty paths must remain eligible for submit.
- For array item schemas, recurse through `array.itemSchema.fields`. An item path such as `participantes.0` can make `includeWhenDirty` fields in that item eligible, but the parent collection path such as `participantes` must not mark every item field dirty.
- Cleared optional fields inside nested collections must remain eligible only when their specific nested dirty path is present.
- `entityLookup` and `inlineEntityLookup` payloads must respect `payloadMode`, `multiple`, and `optionSource.entityKey`, using `serializeEntityLookupValueForPayload` from `@praxisui/core`.
- If a backend needs `id`, `ids`, `entityRef`, or `entityRefs`, fix metadata/request schema/core helper usage; do not reshape lookup values in the host.
- `RESOURCE_ENTITY` display evidence such as `label`, `code`, `status`, `disabledReason`, rich fields, and `OptionDTO.extra` belongs to selection/display UX, not to the persisted submit payload unless the request schema explicitly models an `entityRef` projection. A successful Cockpit, HTTP, or LLM option-source example does not authorize submitting the full lookup object or label.
- In migrations such as Ergon, first prove whether the field metadata declares the correct `controlType`, `payloadMode`, `multiple`, and `optionSource.entityKey`. If the submitted value is wrong while metadata is present, fix the shared `prepareSubmitPayload`/core serialization path; if metadata is absent, route to backend/schema authoring. Do not add screen-local transforms that strip labels or extract IDs per form.
- Retained invalid values are still serialized by canonical identity. `allowRetainInvalidExistingValue`, `disabledReason`, and selection-state evidence affect whether the UI can display or keep an existing value; they do not by themselves change the submit payload shape.
- Rule, action, and hook execution may change form values or trigger submit, but must not fork submit semantics. The final persisted payload still goes through `prepareSubmitPayload`.
- Computed rule values that affect persisted fields must stabilize before payload preparation. Visual-only rule targets never become payload fields.
- Visual blocks, helper content, and local presentation-only state must not enter `formSubmit.formData` or the HTTP payload.
- `formSubmit.formData` is the persistable filtered payload. `formSubmit.rawFormData` is for diagnostics, audit, or UI hooks that need local/transient values, not a replacement submit contract.
- `schemaUrl`, `readUrl`, `submitUrl`, `resourcePath`, and request schema selection are grounding for the canonical command surface; they are not a license to patch payload shape locally.
- Authoring surfaces that expose `submitPolicy`, local/transient fields, or lookup `payloadMode` must preserve round-trip semantics in config editors and JSON editors.

If backend submission fails, audit field metadata, request schema, option source, submit policy, and DTO contract before adding ad hoc transforms.

## Aderence Inventory

Classify submit changes before adding a contract:

- `ja-suportado-so-ux`: payload is right, but diagnostics or validation copy is weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: metadata already has `source`, `transient`, `submitPolicy`, or `payloadMode`, but the editor/runtime exposes it poorly.
- `suportado-parcialmente`: pipeline covers the common case but lacks one canonical branch, such as nested dirty paths, array item schemas, lookup cardinality, or editor round-trip.
- `lacuna-real-de-contrato`: the required payload cannot be expressed by metadata, request schema, or core helper.

Only the last category justifies a new public field or helper.

## Validation

Start with focused unit tests:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.spec.ts
```

When entity lookup serialization or payload mode changes, also run:

```bash
npx ng test praxis-core --watch=false --progress=false \
  --include=projects/praxis-core/src/lib/models/option-source.model.spec.ts \
  --include=projects/praxis-core/src/lib/models/form/form-config.model.spec.ts
```

When authoring or metadata round-trip changes, also run:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/json-config-editor/json-config-editor.component.spec.ts
```

When rules, command rules, actions, or hooks can affect submitted values, add focused service specs before browser validation:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/services/form-rules.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.spec.ts
```

Use Playwright smokes only after unit specs prove payload behavior. Prefer the smallest browser spec that exercises the changed path: select interaction for lookup value identity, rules/domain-rules/business-rules for computed values, config-editor command rules for structured action payload authoring, and surface-open demo for action-triggered submit flows.

For public API changes, run `npm run build:praxis-dynamic-form` plus the direct consumer that imports the changed surface.

## Companion Skills

- Use `praxis-form-schema-runtime-modes` for `resourcePath`, schema/read/submit URLs, modes, and hydration.
- Use `praxis-form-actions-hooks-runtime` when submit is triggered, intercepted, or decorated by form actions or hooks.
- Use `praxis-form-authoring-settings` when editors expose `submitPolicy`, local fields, or entity lookup payload configuration.
- Use `praxis-dynamic-fields-editorial` for field-level control metadata and entity lookup editor behavior.
- Use `praxis-fields-option-sources` for `optionSource`, selected-value reload, dependency filters, and by-ids option hydration.
- Use `praxis-fields-selection-lookup-controls` when select, async select, entity lookup, chips, list, or tree value identity affects submit semantics.
