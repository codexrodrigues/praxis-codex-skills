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
- `projects/praxis-core/src/public-api.ts` when action models, catalogs, providers, validators, UI schemas, presets, or editor helpers are exported or public consumption changes.
- `projects/praxis-core/docs/rfc-surface-open.md`
- `projects/praxis-core/src/lib/models/global-action.model.ts`
- `projects/praxis-core/src/lib/services/global-action.service.ts`
- `projects/praxis-core/src/lib/tokens/global-action.catalog.ts`
- `projects/praxis-core/src/lib/tokens/global-action.providers.ts`
- `projects/praxis-core/src/lib/tokens/global-action.token.ts`
- `projects/praxis-core/src/lib/actions/global-action-ref.utils.ts`
- `projects/praxis-core/src/lib/actions/global-action-ui.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.ts`
- `projects/praxis-core/src/lib/services/surface-binding-runtime.service.ts`
- `projects/praxis-core/src/lib/composition/composition-validator.service.ts`
- `projects/praxis-core/src/lib/widgets/widget-page-composition.serialization.ts`
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

Treat `payloadExpr` and `SurfaceBinding` as projection mechanisms over the declared runtime envelope, not as an intent language. Allowed roots are the structured context published by `GlobalActionContext` and `SurfaceBindingRuntimeService`: `payload`, `runtime`, `pageContext`, `meta`, `context`, `action`, `sourceId`, `widgetKey`, and `output`. Do not use template strings, `${...}` interpolation, or path extraction to choose an `actionId`, infer permission, switch resource identity, or reconstruct a semantic decision that should come from the authored ref, catalog, discovery, composition link, or backend contract.

## Payload Rules

- Normalize refs with `normalizeGlobalActionRef`.
- Validate required payload keys and payload type with `validateGlobalActionRef` or `validateGlobalActionRefs`.
- Get editor fields from `getGlobalActionUiSchema(actionId)`.
- Use `GLOBAL_ACTION_CATALOG` entries and `payloadSchema` for discoverability, validation, AI authoring, and editor projection.
- Use `surface.open` with `SurfaceOpenPayload` for modal/drawer widget targets; do not revive `showAlert:...`, `openUrl:...`, `navigate:...`, `apiCall:...`, or `surface.open:{...}` strings.
- Use `onResult` plus `surface.result` or `dynamicPage.composition.dispatch` for surface outcomes. Do not patch parent widgets directly from the visual host.
- When `surface.open.onResult` is executed, the emitted surface result is exposed as `context.payload`, `runtime.value`, and
  `runtime.state.surfaceResult` for the already-authored `GlobalActionRef`. Treat that as an execution envelope only; do not
  inspect result fields to choose a different action id, infer permission, mutate metadata/config, or decide persistence locally.
  If different outcomes need different continuations, author those continuations as governed composition/action contracts.
- Treat `surface.result` as emission into the active surface runtime and
  `dynamicPage.composition.dispatch` as delivery into the page composition runtime. They are not
  config mutation APIs. Drawer result envelopes, row selections, and runtime payload snapshots should
  flow through declared composition/state/action links; do not persist them into widget
  `definition.inputs`, form config, table config, or host-local state as a shortcut.
- If a surface outcome needs to update a component, author the target as a composition link or an
  explicit component-owned action/input contract and validate feedback-cycle guards. Do not infer
  component mutation from the existence of a returned drawer result.
- `meta` is execution/display context. It may carry labels, icons, confirmation hints, authoring breadcrumbs, or the normalized action ref metadata copied into `context.meta.actionRef`; it must not be the only place where payload schema, resource identity, permission, operation id, or semantic decision is stored.
- Missing handlers or providers are explicit runtime failures such as "Global action not registered" or "Surface service not available". Do not catch these by selecting another action, parsing labels, guessing a route, or silently mutating local state; repair the catalog/provider registration or fail closed with a user-visible diagnostic.
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

- core ref validation, catalog/UI schema, execution, `payloadExpr`, `surface.result`, and `dynamicPage.composition.dispatch`:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/actions/global-action-ref.utils.spec.ts --include=projects/praxis-core/src/lib/services/global-action.service.spec.ts
```

- `surface.open` editor, presets, and binding runtime:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.spec.ts --include=projects/praxis-core/src/lib/actions/surface-open-presets.spec.ts --include=projects/praxis-core/src/lib/services/surface-binding-runtime.service.spec.ts
```

- composition persistence/validation when actions flow through dynamic pages:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/composition/composition-validator.service.spec.ts --include=projects/praxis-core/src/lib/widgets/widget-page-composition.serialization.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-record-surface-open.spec.ts
```

- visual providers when `surface.open`, `surface.result`, dialog actions, or provider registration changes:

```sh
npm run ng -- test praxis-dialog --watch=false --progress=false --include=projects/praxis-dialog/src/lib/providers/dialog-global-actions.provider.spec.ts --include=projects/praxis-dialog/src/lib/providers/surface-global-actions.provider.spec.ts
```

- authoring or component consumer proof when the action is saved/executed outside core:

```sh
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.spec.ts
npm run test:table -- --include=projects/praxis-table/src/lib/table-global-action-adapter.spec.ts --include=projects/praxis-table/src/lib/praxis-table-config-editor.global-actions.spec.ts
npm run ng -- test praxis-list --watch=false --progress=false --include=projects/praxis-list/src/lib/list-global-action-adapter.spec.ts
```

- Page Builder authoring/composition proof when `payloadExpr`, global-action targets, or `surface.open` connection editing changes:

```sh
npm run ng -- test praxis-page-builder --watch=false --progress=false --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.spec.ts --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor-graph.util.spec.ts --include=projects/praxis-page-builder/src/lib/ai/page-builder-ui-composition-plan.spec.ts --include=projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.spec.ts
```

For public or cross-lib changes, also run `npm run build:praxis-core` and a direct consumer build selected by actual imports.

For first-step issue resolution, audit a real action instance end to end: persisted shape, catalog entry, UI schema fields, validation result, runtime context used by `payloadExpr`, execution result, and failure message when the handler/provider is missing.

## Companion Skills

- Use `praxis-core-surface-materialization` when the payload is a resource-derived `surface.open`.
- Use `praxis-core-global-actions-metadata` for the broader metadata-service umbrella.
- Use `praxis-authoring-editors` when Settings Panel or config editors author the action.
- Use `praxis-core-composition-runtime` when action results flow through composition links.
- Use `praxis-angular-public-api-governance` when changing exported action contracts.
