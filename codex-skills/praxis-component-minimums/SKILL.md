---
name: praxis-component-minimums
description: Use when Codex needs to explain or implement the minimum viable setup for Praxis UI components, especially questions like what is the smallest config needed to render a dynamic form or table, where metadata comes from, whether resourcePath alone is enough, or what host services are required for schema-driven runtime bootstrap.
---

# Praxis Component Minimums

Use this skill when the task is about the minimum viable runtime setup of Praxis components.

Typical triggers:

- "qual o minimo para renderizar"
- "de onde vem os metadados"
- "é só preencher resourcePath?"
- "qual o menor host possível"
- "bootstrap mínimo"
- "quick connect"
- "schema-driven mínimo"

This skill is about runtime bootstrap and host wiring, not authoring/editor parity. If the task changes visual editors or authoring flows, also use `praxis-authoring-editors`. If the task changes `dynamic-fields` discovery/editorial chains, also use `praxis-dynamic-fields-editorial`.
If the task implements or reviews backend `RESOURCE_ENTITY` option sources, use
`praxis-resource-entity-lookup-backend`; this skill may explain why `resourcePath` alone is not
enough, but it does not define the backend contract.

Before changing this skill or answering a minimum-setup question, inspect the current source for the
target component and its host services. For Angular components this normally means component inputs,
metadata files, config editor metadata, service injections, local/remote mode tests, and the owning
`@praxisui/core` contracts. The purpose is to codify canonical Praxis runtime knowledge, not repeat
a remembered setup recipe.

## Canonical Decision Rule

Always answer by separating the component into one of these modes:

1. local-only runtime
2. backend metadata-driven runtime
3. authored/customizable runtime

Do not collapse these into a single "minimum".

## Dynamic Form Minimum

For `@praxisui/dynamic-form`, there are two different minimums:

- Local-only minimum: import `PraxisDynamicForm` and pass a `FormConfig` with
  local layout and `fieldMetadata`. This renders without backend discovery and
  is appropriate for demos, transient host-only forms, or authoring previews.
- Backend metadata-driven minimum: provide runtime endpoints the form can
  resolve. `resourcePath` can connect the form to backend discovery, but for
  metadata-driven surfaces published by the backend, prefer
  `schemaUrl + submitUrl + submitMethod` or the operation-specific inputs
  expected by the consuming CRUD/surface runtime.
- Schema-driven layout minimum: when the backend schema owns fields,
  labels, controls, groups, order, and width, do not add local
  `FormConfig.sections` or placeholder `sections: []` just to make the form
  render. Use the runtime's generated layout or `layoutPolicy` presets first.
  If the generated layout is not acceptable, classify the gap against
  metadata/runtime ownership instead of copying local sections into every host
  screen.

Local/transient field minimum:

- Host-owned fields that do not come from the backend schema belong in `FormConfig.fieldMetadata`, not in `praxis-metadata-starter` schemas.
- Mark host-only fields with `source: 'local'` or `transient: true` when they must participate in the UI, validation, rules, visibility, and `valueChange` but must not be sent to the backend by default.
- Use `submitPolicy` only when the default submit behavior must be overridden:
  - `include` sends the field even when it is local/transient.
  - `omit` always removes it from submit payloads.
  - `includeWhenDirty` sends it only when its control is dirty.
- `formSubmit.formData` is the backend payload after submit filtering; `formSubmit.rawFormData` is the complete UI value bag.
- Do not solve local/transient fields by adding backend DTO fields, ad hoc frontend aliases, or CRUD-specific payload filters. The canonical runtime owner is `@praxisui/dynamic-form` with the shared `FieldMetadata` contract in `@praxisui/core`.

Important guardrails:

- `resourcePath` is not the only path.
- `resourcePath` is not the canonical answer for every form question.
- If no `FormConfig` is provided, the runtime can generate a default layout from backend metadata.
- If the host uses runtime fetch/submit flows, confirm the host scope provides the effective API/CRUD service wiring.
- CRUD hosts consume the dynamic-form submit contract; they should not redefine local/transient field filtering.

## Table Minimum

For `@praxisui/table`, answer differently depending on local vs remote mode:

- Local minimum: pass local `data` and/or `config`; no remote schema bootstrap is required.
- Remote minimum: `resourcePath` is the canonical lightweight entry point, as long as the host already provides the Praxis API/CRUD wiring needed by the table runtime.

Important guardrails:

- `resourcePath` is enough for the remote bootstrap only when the host wiring is already present.
- Without effective `resourcePath`, the table does not enter the remote schema/data flow.
- In remote mode, the table derives columns from `/schemas/filtered` and data from the backend resource/filter contract.
- Optional collection operations, including export, are not implied by remote bootstrap. Gate them through backend `capabilities` and `_links`.

## CRUD Minimum

For `@praxisui/crud`, do not describe the minimum as "table plus `resourcePath`". CRUD is a
composed runtime with table, form launcher, action resolution, capabilities, and optional
modal/drawer form contracts.

- Local/static minimum: pass `metadata` with local resource/data/table/form structure sufficient for
  the desired static display or hosted example. This does not prove backend action availability.
- Remote resource minimum: pass `metadata.resource.path` and ensure the host provides the Praxis
  API/CRUD wiring. The runtime can use the resource path for table/schema/data flows, but create,
  view, edit, delete, and collection workflows must still be aligned with resource capabilities and
  HATEOAS links.
- Explicit form-action minimum: when a modal/drawer action uses backend-published surfaces or a
  non-generic operation, provide `metadata.actions[].form.schemaUrl`, `submitUrl`, and
  `submitMethod` instead of relying on a generic fallback from `metadata.resource.path`.
- Nested or contextual resource minimum: use `metadata.resource.schemaPath` when schema discovery
  needs the canonical schema template while `metadata.resource.path` targets a concrete nested
  collection.

Host requirements:

- effective API endpoint/CRUD service configuration
- dynamic-form dependencies for opened forms
- table dependencies for the embedded collection surface
- resource capabilities resolvable before claiming action availability

Answer "is resourcePath enough?" for CRUD as: enough only to enter a basic remote resource flow when
host wiring exists; not enough to prove action permissions, export, modal form endpoints, or nested
schema binding.

## Collection Operation Minimums

For collection operations reused by Table, List, or future collection components, separate render/data bootstrap from operation availability:

- `resourcePath` can be enough to enter remote data mode, but it is not proof that a resource supports export or another optional collection action.
- Treat `capabilities.canonicalOperations.<operation>` and matching HATEOAS links as the availability contract.
- For collection export specifically, require `canonicalOperations.export === true` or `_links.export` before telling a host to expose export UI.
- Do not infer export support from a generic base route such as `POST /{resource}/export`; the service must opt in.

## Entity Lookup Minimum

For `entityLookup`, separate render bootstrap from governed backend semantics:

- Local/manual minimum: a host can pass metadata and options directly for a local field.
- Remote generic minimum: `resourcePath` plus generic `/options/filter` can feed select-like controls, but it is not a governed entity lookup contract.
- Governed backend minimum: a business entity lookup should be published as `x-ui.optionSource.type = RESOURCE_ENTITY` with a named `/option-sources/{sourceKey}/options/filter` endpoint and matching `/by-ids` rehydration.

When a question asks whether `resourcePath` alone is enough, answer: enough only for lightweight
remote bootstrap when host wiring exists; not enough for a canonical governed entity lookup.

## Required Workflow

1. Identify the target component and whether the question is local-only, remote metadata-driven, or authoring/customizable.
2. Identify the minimum runtime inputs required for that mode.
3. Identify where metadata comes from in that mode.
4. Identify what the host must already provide.
5. Answer explicitly whether `resourcePath` is sufficient, optional, or not the preferred canonical path.
6. If the question involves an optional collection action, identify the capability or link that proves availability.
7. If the target is composed, such as CRUD, map the minimum of each embedded runtime instead of
   collapsing the answer to the outer component input.

## Required Output Shape

When answering, prefer this structure:

- minimum local path
- minimum remote/schema-driven path
- metadata source
- host requirements
- whether `resourcePath` alone is enough

## High-Risk Failure Modes

- answering with a single "minimum" when the component has distinct local and remote modes
- claiming `resourcePath` is always the canonical answer for `dynamic-form`
- claiming a component is metadata-driven without naming the metadata source
- omitting host requirements for API/CRUD wiring
- confusing runtime bootstrap with editor/authoring requirements
- assuming Table/List export is available because a base controller route exists
- treating generic `/options/filter` or `resourcePath` as equivalent to a governed `RESOURCE_ENTITY`
  option source
- treating CRUD as a thin table wrapper and omitting `metadata.actions[].form`, capabilities, row
  links, or `metadata.resource.schemaPath` when those are the contracts that make the runtime safe

## References

Load only what you need:

- `references/dynamic-form-minimums.md`
- `references/table-minimums.md`
- `references/metadata-sources.md`
