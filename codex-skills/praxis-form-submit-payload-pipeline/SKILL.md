---
name: praxis-form-submit-payload-pipeline
description: Use when Codex must inspect, change, or test @praxisui/dynamic-form submit payload normalization, prepareSubmitPayload, normalizeSubmitPayload, normalizeDateArrays, local/transient fields, submitPolicy, entity lookup payloadMode, dirty-field filtering, nested array item schemas, or submit validation.
---

# Praxis Form Submit Payload Pipeline

Use this skill for the canonical client-side submit pipeline of `@praxisui/dynamic-form`. The submit payload is a projection of form value plus field metadata; do not patch payload shape in host components when the issue belongs to metadata, `@praxisui/core`, or backend DTO/schema semantics.

## Source Audit

Inspect these files before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-date-arrays.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`

Inspect `@praxisui/core` models/helpers when touching `FieldMetadata`, `FieldSubmitPolicy`, `MaterialEntityLookupMetadata`, `payloadMode`, or `serializeEntityLookupValueForPayload`.

## Payload Rules

The canonical order is:

1. Normalize date arrays.
2. Normalize local datetime strings by adding the local ISO offset when missing.
3. Filter fields according to metadata.
4. Serialize entity lookup values through the shared core helper.
5. Recurse into array item schemas.

Respect these semantics:

- `source: "local"` and `transient: true` are omitted by default.
- `submitPolicy: "include" | "omit" | "includeWhenDirty"` overrides the default omission policy.
- Legacy `"never"` may be defensively normalized to `"omit"`, but the public contract remains `"omit"`.
- Empty optional fields are omitted when they were not dirty.
- Required fields, dirty fields, and nested dirty paths must remain eligible for submit.
- `entityLookup` and `inlineEntityLookup` payloads must respect `payloadMode`, `multiple`, and `optionSource.entityKey`.
- Visual blocks, helper content, and local presentation-only state must not enter the payload.

If backend submission fails, audit field metadata, request schema, option source, submit policy, and DTO contract before adding ad hoc transforms.

## Aderence Inventory

Classify submit changes before adding a contract:

- `ja-suportado-so-ux`: payload is right, but diagnostics or validation copy is weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: metadata already has `source`, `transient`, `submitPolicy`, or `payloadMode`, but the editor/runtime exposes it poorly.
- `suportado-parcialmente`: pipeline covers the common case but lacks one canonical branch.
- `lacuna-real-de-contrato`: the required payload cannot be expressed by metadata, request schema, or core helper.

Only the last category justifies a new public field or helper.

## Validation

- payload filtering: `prepare-submit-payload.spec.ts`
- temporal normalization: `normalize-submit-payload.spec.ts`, `normalize-date-arrays.spec.ts`
- entity lookup serialization: focused dynamic-form/core specs around `payloadMode`, `multiple`, and `optionSource.entityKey`
- nested arrays and dirty filtering: add or update focused unit specs before browser validation
- end-to-end submit: browser/API smoke only after the payload unit behavior is proven

For public API changes, run `npm run build:praxis-dynamic-form` plus the direct consumer that imports the changed surface.

## Companion Skills

- Use `praxis-form-schema-runtime-modes` for `resourcePath`, schema/read/submit URLs, modes, and hydration.
- Use `praxis-form-actions-hooks-runtime` when submit is triggered, intercepted, or decorated by form actions or hooks.
- Use `praxis-form-authoring-settings` when editors expose `submitPolicy`, local fields, or entity lookup payload configuration.
- Use `praxis-dynamic-fields-editorial` for field-level control metadata and entity lookup editor behavior.
