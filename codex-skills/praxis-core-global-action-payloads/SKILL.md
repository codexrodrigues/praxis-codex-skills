---
name: praxis-core-global-action-payloads
description: Use when Codex must implement, audit, migrate, or validate @praxisui/core GlobalActionRef payload contracts: GlobalActionService, global action catalogs/providers, validateGlobalActionRef(s), getGlobalActionUiSchema, payloadExpr, surface.open payload schemas, onResult, dynamicPage.composition.dispatch, or command-string cleanup.
---

# Praxis Core Global Action Payloads

Use this skill when the work is about the executable `GlobalActionRef` contract and its payloads.

Global actions are governed runtime decisions, not string commands. Persist and execute them as structured refs with cataloged payload schema, UI schema, validation, and host-provided handlers.

## Source Audit

Inspect before editing:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/docs/rfc-surface-open.md`
- `projects/praxis-core/src/lib/models/global-action.model.ts`
- `projects/praxis-core/src/lib/services/global-action.service.ts`
- `projects/praxis-core/src/lib/tokens/global-action.catalog.ts`
- `projects/praxis-core/src/lib/tokens/global-action.providers.ts`
- `projects/praxis-core/src/lib/tokens/global-action.token.ts`
- `projects/praxis-core/src/lib/actions/global-action-ref.utils.ts`
- `projects/praxis-core/src/lib/actions/global-action-ui.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.ts`
- focused specs and the consumer/editor that persists or executes the action.

## Canonical Shape

Persist actions as:

```ts
{
  actionId: 'surface.open',
  payload: { /* typed payload */ },
  payloadExpr: undefined,
  meta: { label: 'Open details' }
}
```

Use `payloadExpr` only when the payload is intentionally derived from runtime context such as `payload.row`, `runtime.selection`, `runtime.formData`, or `pageContext`. Do not encode expressions in labels, route strings, command prefixes, or component-local fields.

## Payload Rules

- Normalize refs with `normalizeGlobalActionRef`.
- Validate required payload keys and payload type with `validateGlobalActionRef` or `validateGlobalActionRefs`.
- Get editor fields from `getGlobalActionUiSchema(actionId)`.
- Use `GLOBAL_ACTION_CATALOG` entries and `payloadSchema` for discoverability, validation, AI authoring, and editor projection.
- Use `surface.open` with `SurfaceOpenPayload` for modal/drawer widget targets; do not revive `showAlert:...`, `openUrl:...`, `navigate:...`, `apiCall:...`, or `surface.open:{...}` strings.
- Use `onResult` plus `surface.result` or `dynamicPage.composition.dispatch` for surface outcomes. Do not patch parent widgets directly from the visual host.
- Built-in handlers are shared runtime capabilities. Host-specific handlers may be registered, but their action ids and payloads should still be cataloged and validated.

## Aderence Inventory

Classify before introducing or changing a global action:

- `ja-suportado-so-ux`: catalog/schema/handler exists; editor, docs, or consumer UX hides it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: command string or local action wrapper should become `GlobalActionRef`.
- `suportado-parcialmente`: handler exists but catalog, UI schema, validation, onResult, or direct consumer proof is incomplete.
- `lacuna-real-de-contrato`: no action id, handler boundary, payload schema, or runtime context can express the decision.

For a real gap, update the core catalog/schema/validation, provider or handler, docs, specs, public API if needed, and at least one direct consumer.

## No Keyword Routing

Do not select an action by matching button text, labels, route fragments, aliases, or keywords as the primary decision. Semantic scope must come from the authored action ref, catalog entry, component metadata, resource/action/surface discovery, or governed AI contract. Text matching may rank already-scoped candidates only.

## Validation

Use focused validation:

- `global-action-ref.utils.spec.ts`
- `global-action.service.spec.ts`
- surface open preset/editor specs
- provider/catalog specs
- authoring editor or direct consumer specs where the action is saved and executed.

For first-step issue resolution, audit a real action instance end to end: persisted shape, catalog entry, UI schema fields, validation result, runtime context used by `payloadExpr`, execution result, and failure message when the handler/provider is missing.

## Companion Skills

- Use `praxis-core-surface-materialization` when the payload is a resource-derived `surface.open`.
- Use `praxis-core-global-actions-metadata` for the broader metadata-service umbrella.
- Use `praxis-authoring-editors` when Settings Panel or config editors author the action.
- Use `praxis-core-composition-runtime` when action results flow through composition links.
- Use `praxis-angular-public-api-governance` when changing exported action contracts.
