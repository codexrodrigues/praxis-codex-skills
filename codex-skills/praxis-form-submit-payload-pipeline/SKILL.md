---
name: praxis-form-submit-payload-pipeline
description: Use when Codex must inspect, change, or test @praxisui/dynamic-form or praxis-dynamic-form package submit payload normalization, prepareSubmitPayload, normalizeSubmitPayload, normalizeDateArrays, local/transient fields, submitPolicy, entity lookup payloadMode, dirty-field filtering, dotted custom-field paths, nested date hydration/filter restoration, nested array item schemas, or submit validation.
---

# Praxis Form Submit Payload Pipeline

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the canonical client-side submit pipeline of `@praxisui/dynamic-form`. The submit payload is a projection of form value plus field metadata; do not patch payload shape in host components when the issue belongs to metadata, `@praxisui/core`, or backend DTO/schema semantics.

## Source Audit

Inspect these files before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/nested-field-path.ts` and its spec
- `projects/praxis-dynamic-form/src/lib/utils/custom-fields-submit.integration.spec.ts`
- `projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form.ts` and its spec
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts` and `praxis-dynamic-form.schema-loading.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.json-api.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`

Inspect these `@praxisui/core` files before changing field submit or lookup payload contracts:

- `projects/praxis-core/src/lib/models/component-metadata.interface.ts`
- `projects/praxis-core/src/lib/models/field-scalar-items.model.ts` and `helpers/scalar-array-value.ts`
- `projects/praxis-core/src/lib/models/form/schema-field-lifecycle.spec.ts`
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

1. Normalize legacy date tuples only in fields declared temporal by existing metadata, recursing through collection item schemas.
2. Normalize local datetime strings only on those temporal fields, adding the local ISO offset when missing. Preserve ordinary/unknown strings verbatim, including spaces and date-like text, and keep non-temporal/unknown numeric tuples as arrays.
3. Filter fields according to metadata.
4. Project scalar arrays through the shared Core normalizer and serialize entity lookup values through the shared Core helper.
5. Recurse into array item schemas.

Respect these semantics:

- The submit payload is a projection of raw form value plus `FieldMetadata`, dirty paths, and the request schema; host components must not add local payload transforms for canonical cases.
- A metadata name such as `customFields.numero_calcado` addresses a nested record value, not a literal dotted JSON key. Read, normalize, omit and write that leaf while retaining sibling values and the nested wire structure. Apply ordinary submit policies, dates, lookup serialization, required/dirty handling and array item schemas at that full field path.
- Do not manufacture a missing nested value/container or replace a null/scalar container during submit. Copy changed record ancestors so filtering and normalization do not mutate API data or the raw form value. Preserve the flat-field branch: one initial record draft plus direct writes/deletes, without copying the whole root for every field. Array items remain governed by their item schema, not generic record-path traversal.
- Temporal hydration/submit normalization shares `normalizeTemporalFieldValues` with field metadata and item schemas, using one private draft rather than root copies per transformed field. `DateInput` follows the existing date-only serialization. Do not infer temporal meaning from the numeric/string shape alone; `[2026, 10, 27]` can be data in a non-temporal field.
- Preserve the same flat draft/accumulator branch in date hydration, filter restoration and computed contexts, not only submit. Copy-on-write helpers are for dotted paths; a private temporal draft can update its admitted own leaf directly.
- The internal `nested-field-path` helper also supports date hydration and filter metadata rebuilds. Nested date controls must receive the same coercion as top-level date controls. Filter restoration must retain existing nested values, including disabled controls, skip only names absent from the final delivered metadata and respect explicit defaults as reset intent. A server-removed field may remain as disabled/omit metadata for continuity; raw restoration must not make it applicable or required. Hidden/local legitimate fields keep their own semantics. Keep the helper internal; this path does not require a new public export or host adapter.
- The record-path helper rejects `__proto__` and empty segments and never follows inherited values. Own `constructor` and `prototype` properties are legitimate data keys in flat and nested payload/helper records; do not blanket-ban them in generic utility records or relax the canonical backend reserved-name policy for controls from these utility tests. Writing a path creates own record properties rather than traversing inherited objects. Do not traverse arrays or non-record values as if they were ordinary object containers.
- A same-context metadata rebuild must capture and restore nested dirty/touched leaf paths through groups and FormArray items without touching unrelated controls. Do not generalize this to autosave across resets, retry, record or tenant switches; explicit filter defaults retain reset intent.
- Successful empty definitions are authoritative, including saved configuration and manual sync. Use Core's shared reconciliation policy for all lanes: nonlocal orphans hidden/disabled/omit, explicit local fields preserved, current server constraints restored on reappearance. Prove empty-last-field, required-null orphan and returning optional field through reconciliation/FormGroup/submit and Filter, not just container migration; no host property strips or blanket hidden omission.
- Read-only/disabled is not generic omission. The canonical backend command request excludes read-only custom fields; response/filter may retain them for their operation. Use that exact request instead of merging response or adding an unsupported x-ui.submitPolicy mapping. Inspect backend schema guidance for reserved keys and request publication; utility own-key support is not field admission.
- Scalar arrays use FieldMetadata.items and the public Core normalizeScalarArrayValue, separately from object-array itemSchema. Keep validators, prepareSubmitPayload and all query consumers aligned on typed tokens/formats/enum. Reject invalid/null items without partial conversion; optional null container and [] remain distinct, required still applies. Do not hand-roll per-control parsing or claim safe integer support beyond JavaScript's range.
- New schema-loading cycles revalidate HTTP and normalize the body; compiled L1, saved metadata or status0 cache cannot establish readiness. Loading/error/known unconfirmed enterprise context blocks submit; denied/invalid schema never falls back to response/catalog or old config. Captured confirmed tenant/locale/version governs the scope; context switch cancels stale generations and invalidates old seeds, not cross-tenant autosave. A scalar projection error in payloadPreviewChange emits formData:null/isValid:false with raw data intact; consumers must not apply it.
- `source: "local"` and `transient: true` are omitted by default.
- `submitPolicy: "include" | "omit" | "includeWhenDirty"` overrides the default omission policy.
- Legacy `"never"` may be defensively normalized to `"omit"`, but the public contract remains `"omit"`.
- Empty optional fields are omitted when they were not dirty.
- Required fields, dirty fields, and nested dirty paths must remain eligible for submit.
- For array item schemas, recurse through `array.itemSchema.fields`. An item path such as `participantes.0` can make `includeWhenDirty` fields in that item eligible, but the parent collection path such as `participantes` must not mark every item field dirty.
- Cleared optional fields inside nested collections must remain eligible only when their specific nested dirty path is present. Compose dotted collection fields such as `customFields.items` with item-schema leaves such as `customFields.reason`; both `customFields.items.0.customFields.reason` and `customFields.items[0].customFields.reason` dirty paths must preserve the intended cleared leaf without marking the sibling item dirty.
- `entityLookup` and `inlineEntityLookup` payloads must respect `payloadMode`, `multiple`, and `optionSource.entityKey`, using `serializeEntityLookupValueForPayload` from `@praxisui/core`.
- If a backend needs `id`, `ids`, `entityRef`, or `entityRefs`, fix metadata/request schema/core helper usage; do not reshape lookup values in the host.
- `RESOURCE_ENTITY` display evidence such as `label`, `code`, `status`, `disabledReason`, rich fields, and `OptionDTO.extra` belongs to selection/display UX, not to the persisted submit payload unless the request schema explicitly models an `entityRef` projection. A successful Cockpit, HTTP, or LLM option-source example does not authorize submitting the full lookup object or label.
- In migrations such as Ergon, first prove whether the field metadata declares the correct `controlType`, `payloadMode`, `multiple`, and `optionSource.entityKey`. If the submitted value is wrong while metadata is present, fix the shared `prepareSubmitPayload`/core serialization path; if metadata is absent, route to backend/schema authoring. Do not add screen-local transforms that strip labels or extract IDs per form.
- Retained invalid values are still serialized by canonical identity. `allowRetainInvalidExistingValue`, `disabledReason`, and selection-state evidence affect whether the UI can display or keep an existing value; they do not by themselves change the submit payload shape.
- Rule, action, and hook execution may change form values or trigger submit, but must not fork submit semantics. The final persisted payload still goes through `prepareSubmitPayload`.
- Hook extras, command-rule runtime context, and intermediate `form.value` snapshots are operational context, not the persisted submit contract. The persisted command payload is the `formSubmit.formData` computed in `onSubmit()` after `beforeSubmit` completes and `prepareSubmitPayload(...)` filters/serializes the raw value; use `rawFormData` only for diagnostics, audit, UI hooks, or local/transient context.
- `formCommandRules` and global action `payloadExpr` values that read `runtime.formData` must receive the same prepared payload used by submit events and HTTP requests. Do not evaluate command-rule conditions or `payloadExpr` against `form.getRawValue()`, local/transient fields, or a pre-filter snapshot unless the contract explicitly asks for diagnostic `rawFormData`.
- Computed rule values that affect persisted fields must stabilize before payload preparation. `FormRulesService` must materialize dotted computed targets into the nested evaluation `formData` consumed by JSON Logic, with the same structure as wire values and no literal dotted aliases. Keep `result.fieldValues` as the flat target-ID map used to apply values to controls. Read only own properties, preserve the flat draft branch and copy only changed nested record ancestors; do not mutate raw form data or the FormGroup during context stabilization. Record-path helpers do not traverse array intermediates; item-schema submit recursion is a separate path. Visual-only rule targets never become payload fields.
- Visual blocks, helper content, and local presentation-only state must not enter `formSubmit.formData` or the HTTP payload.
- When adopting a changed request schema, test both fresh and saved form configuration. Core `reconcileFormConfig` knows whether a retained field is absent from the current server definitions: absent `source` or `source: "schema"` means a legacy schema field, while a noncolliding explicit `source: "local"` field keeps its local policy; obsolete containers colliding with current custom-field children yield to the server shape through Core reconciliation. A removed schema field is retained for layout continuity but materialized as `formHidden: true`, `disabled: true`, `submitPolicy: "omit"`. This prevents stale required validators from blocking the form and prevents GET hydration plus `getRawValue()` from resubmitting the removed property. Do not implement a host-specific property strip or omit every hidden field: hidden fields still in the request schema may be required contextual inputs. When the server publishes the field again, reconciliation restores current server enabled/visibility and submit semantics. Prove the real reconciler → `DynamicFormService` FormGroup → read hydration → prepared payload chain, including required-null orphans, returning fields, valid hidden fields and explicit local include. When testing through the Core public package, verify that it contains the corrected reconciler; a stale installed package is not evidence about the changed source.
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

For dotted field names, also prove helper immutability/unsafe-path handling, own
`constructor`/`prototype` round-trips without inherited traversal, preserved flat
normalization/omission without per-field root copies, submit policies and lookup
serialization at the nested leaf, absent/null
containers, nested date hydration, filter metadata rebuild/default behavior, and
composition of custom-field collections with dotted/bracket item dirty paths.
Also prove metadata-aware temporal conversion, numeric/unknown arrays and ordinary
strings preserved verbatim, DateInput date-only values, and nested dirty/touched
restoration without changing unrelated controls.
Also prove scalar items/enum parity in real controls and prepared payload,
invalid preview emits null without throwing, successful empty schema is
authoritative and reconciles normally while denied schema fails closed, and
context transitions/fresh cycles revalidate rather than using L1.
The saved-container integration must prove normalization → each of the three
reconciliation paths → `DynamicFormService` controls → prepared nested payload,
including number/date values and source immutability:

```bash
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/utils/nested-field-path.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/custom-fields-submit.integration.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.spec.ts --include=projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form.spec.ts
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

When rules, command rules, actions, or hooks can affect submitted values, add focused service specs before browser validation. For dotted computed targets, prove a nested-to-flat chain declared in reverse dependency order stabilizes before conditions run, including true/false branches, source immutability, no dotted aliases and no false iteration-limit diagnostic for unsupported array traversal:

```bash
npx ng test praxis-dynamic-form --watch=false --progress=false \
  --include=projects/praxis-dynamic-form/src/lib/services/form-rules.service.spec.ts \
  --include=projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.spec.ts
```

Use Playwright smokes only after unit specs prove payload behavior. Prefer the smallest browser spec that exercises the changed path: select interaction for lookup value identity, rules/domain-rules/business-rules for computed values, config-editor command rules for structured action payload authoring, and surface-open demo for action-triggered submit flows.

For public API changes, run `npm run build:praxis-dynamic-form` plus the direct consumer that imports the changed surface.

## Companion Skills

- Use `praxis-core-resource-runtime` for `customFieldsContainer` expansion and preservation of custom-field identity from `FieldDefinition` into `FieldMetadata`.
- Use `praxis-form-schema-runtime-modes` for `resourcePath`, schema/read/submit URLs, modes, and hydration.
- Use `praxis-form-actions-hooks-runtime` when submit is triggered, intercepted, or decorated by form actions or hooks.
- Use `praxis-form-authoring-settings` when editors expose `submitPolicy`, local fields, or entity lookup payload configuration.
- Use `praxis-dynamic-fields-editorial` for field-level control metadata and entity lookup editor behavior.
- Use `praxis-fields-option-sources` for `optionSource`, selected-value reload, dependency filters, and by-ids option hydration.
- Use `praxis-fields-selection-lookup-controls` when select, async select, entity lookup, chips, list, or tree value identity affects submit semantics.
