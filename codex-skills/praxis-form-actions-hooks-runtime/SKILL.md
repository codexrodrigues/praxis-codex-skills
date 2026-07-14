---
name: praxis-form-actions-hooks-runtime
description: Use when Codex must work on @praxisui/dynamic-form or praxis-dynamic-form package actions, hooks, PraxisFormActionsComponent, action authoring, global action refs, surface open payloads, action visibility/shortcuts, submit/cancel/reset/custom action behavior, hook registries, or action editor round-trip.
---

# Praxis Form Actions Hooks Runtime

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for Dynamic Form action surfaces and hook execution. Actions and hooks are runtime materializations of declared `FormConfig`, global action catalogs, and hook registries; do not implement host-local command parsing or keyword-driven routing.

## Source Audit

First resolve the Angular workspace root. In the platform monorepo the files may live under
`praxis-ui-angular/projects/...`; in a standalone Angular checkout they may live directly under
`projects/...`. Audit the active `praxis-ui-angular` workspace, not stale issue worktrees such as
`praxis-ui-angular-issue*`, unless the user explicitly targets one of those worktrees.

Inspect the affected owner before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.html`
- `projects/praxis-dynamic-form/src/lib/components/praxis-form-actions/praxis-form-actions.component.ts`
- `projects/praxis-dynamic-form/src/lib/components/praxis-form-actions/praxis-form-actions.json-api.md`
- `projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.ts`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`
- `projects/praxis-dynamic-form/src/lib/utils/prepare-submit-payload.ts`
- `projects/praxis-dynamic-form/src/lib/utils/normalize-submit-payload.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-visual-builder-parity-audit.md`
- `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-actions.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-actions-custom.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-command-rules.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-hooks.playwright.spec.ts`
- `projects/praxis-dynamic-form/test-dev/e2e/surface-open-form-demo.playwright.spec.ts`

Inspect `@praxisui/core` for `GlobalActionRef`, global action catalogs, payload validation helpers, `SurfaceOpenPayload`, action metadata, and effect policies.
In core, check these concrete files when `surface.open` payloads or global action behavior change:

- `projects/praxis-core/docs/rfc-surface-open.md`
- `projects/praxis-core/src/lib/models/global-action.model.ts`
- `projects/praxis-core/src/lib/models/surface-action.model.ts`
- `projects/praxis-core/src/lib/actions/global-action-ref.utils.ts`
- `projects/praxis-core/src/lib/actions/global-action-ref.utils.spec.ts`
- `projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.ts`
- `projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.spec.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.spec.ts`
- `projects/praxis-core/src/lib/services/global-action.service.ts`
- `projects/praxis-core/src/lib/services/global-action.service.spec.ts`
- `projects/praxis-core/src/lib/services/surface-binding-runtime.service.ts`
- `projects/praxis-core/src/lib/services/surface-binding-runtime.service.spec.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts`
- `projects/praxis-core/src/lib/tokens/global-action.catalog.ts`

## Runtime Rules

- Default actions are submit, cancel, and reset; custom actions come from `FormConfig.actions.custom`.
- Runtime rule overrides may alter visibility, disabled state, labels, classes, or other supported action fields.
- `PraxisFormActionsComponent` owns action rendering, collapsed/mobile grouping, shortcut registration, invalid submit hints, and emits `PraxisFormActionEvent`.
- Submit actions must still pass through the canonical submit pipeline.
- Global actions must be represented as declared action refs with validated payloads.
- Surface open payloads should use the canonical `SurfaceOpenPayload` shape, including presentation, widget, bindings, and context.
- Preserve the full canonical `surface.open` payload where supported by core: `beforeWidget`,
  `widget`, `afterWidget`, `bindings`, `context`, and `onResult`. Do not let a Dynamic Form
  normalizer/editor silently drop semantic return handling or composed surface slots.
- Hooks should execute through the registered hook contract and declared stages, not through arbitrary host callbacks hidden in config.
- `beforeSubmit` is cancelable and runs before `PraxisDynamicForm` snapshots `form.getRawValue()`;
  hook mutations that should affect persistence must update controls before that stage completes.
- After submit starts, use `formSubmit.formData` as the persistence/command payload. `rawFormData`
  and hook extras are diagnostic or UI context and must not become a parallel submit contract.
- `formCommandRules` is the conditional command/side-effect channel. Keep it separate from `formRules` property effects and execute global actions through `GlobalActionService.executeRef(...)`.
- `payload` is the structured authoring path for global actions; `payloadExpr` is an advanced JSON/expression escape hatch and must be preserved when structured payload is absent.
- Treat `payloadExpr` as an advanced projection of runtime context, not as a scripting or policy
  engine. If a command needs legal/compliance policy, approval, or transactional guardrails, route
  the decision to governed `domain-rules` materializations such as `workflow_action`,
  `approval_policy`, or `backend_validation`; do not encode that policy in a Dynamic Form
  expression or hook callback.
- `surface.open` authoring should reuse the canonical core surface-open editor/presets/schema. Dynamic Form must not invent a parallel payload DSL for opening forms, dialogs, drawers, or related-resource surfaces.
- `surface.open` is horizontal platform capability owned by `@praxisui/core`, not a Dynamic
  Form feature. Dynamic Form may host or configure it, but contract changes belong in core first.
- Action rule overrides may affect action UI state, but they must not bypass submit validation, `formIsValid`, invalid-submit hints, or the submit payload pipeline.
- Hook stages are declared lifecycle extension points. If a workflow needs business orchestration, prefer governed actions/domain rules over hidden host callbacks.
- In Ergon-style migrations, legal write commands, payment/approval gates, status transitions, and
  auditable side effects should be classified before implementation: UI-only affordances can remain
  Dynamic Form actions, but reusable or regulated command policy belongs to `domain-rules` and a
  materialized runtime target. Dynamic Form should consume the resulting action availability,
  validation, approval, or workflow policy; it should not become the canonical command engine.

When a required command is missing, extend the canonical action/hook/global action contract. Do not add regex, aliases, or local prompt parsing as the primary decision path.

## Authoring Rules

- Use the injected global action catalog when available; fallback catalogs are for local authoring coverage, not new semantics.
- Preserve unknown but valid payload fields only when the canonical payload schema allows them.
- Required action params must be validated with the core helper.
- Actions editor, hooks editor, JSON editor, and Settings Panel must round-trip the same config shape.
- Put framework-owned visible text in dynamic-form i18n, not hardcoded component copy.
- Keep shortcut semantics stable: `PraxisFormActionsComponent` owns registration/disposal and emits `PraxisFormActionEvent`; the host decides how to handle `submit`, `cancel`, `reset`, and custom action IDs.
- In command-rule authoring, preserve structured `GlobalActionRef` data and fail closed when required payload/params are invalid. Do not downgrade failed mutable actions to `customAction`.
- For command rules produced by AI or migration tooling, require an explicit `GlobalActionRef`
  backed by the catalog and keep `payload`, `payloadExpr`, and `meta` intact through editor
  round-trip. If the catalog cannot express the command, add or extend the canonical catalog/action
  contract; do not store a host command name in a custom action label.
- When editing `surface.open`, verify that Dynamic Form wrapper utilities preserve core-owned
  fields rather than reducing the payload to only the fields currently visible in the form editor.
- For AI-authored actions/hooks, route through the Dynamic Form authoring manifest/edit-plan surface and the core global-action catalog. Do not generate ad hoc click handlers, host callbacks, or prompt-only action strings.

## Aderence Inventory

Classify action/hook changes before adding a contract:

- `ja-suportado-so-ux`: runtime works, but editor affordance, label, diagnostics, or shortcut behavior is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: global action catalog, hook registry, or payload schema exists but is not surfaced correctly.
- `suportado-parcialmente`: the declared action exists, but one runtime/editor branch is missing.
- `lacuna-real-de-contrato`: no declared action, hook stage, payload schema, or global action contract can express the requirement.

Only `lacuna-real-de-contrato` should create a new public action or hook contract.

## Validation

- Action rendering/runtime: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/components/praxis-form-actions/praxis-form-actions.component.spec.ts`
- Action authoring: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/actions-editor/actions-editor.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.spec.ts`
- Submit boundary: add `prepare-submit-payload.spec.ts` and `normalize-submit-payload.spec.ts` when actions, hooks, or rules affect submit data.
- Command/rule effects: add `form-rules.service.spec.ts`, `rule-converters.spec.ts`, `rule-properties-panel.component.spec.ts`, and config-editor command-rule specs when `formCommandRules`, action targets, or `surface.open` payload authoring changes.
- Hooks: use focused hooks-editor specs when present; if no dedicated spec exists, validate through config editor, JSON editor, and browser hooks flows.
- Core global actions: run focused `@praxisui/core` specs for `global-action-ref.utils`,
  `global-action.service`, `surface-open-action-editor`, `surface-open-presets`,
  `surface-binding-runtime.service`, `surface-open-materializer`, and surface binding/runtime
  when shared global action behavior changes.
- Surface open round-trip: include Dynamic Form action authoring specs plus core
  `surface-open-action-editor.component.spec.ts`, `surface-binding-runtime.service.spec.ts`, and
  `surface-open-materializer.service.spec.ts` when `beforeWidget`, `afterWidget`, `bindings`,
  `context`, `widget.inputs`, or `onResult` can be changed or preserved.
- Browser validation: focused Playwrights for `form-config-editor-actions`, `form-config-editor-actions-custom`, `form-config-editor-command-rules`, `form-config-editor-hooks`, and `surface-open-form-demo` when visible action/hook behavior changes.
- Docs/registry: validate JSON API docs and generated AI/registry surfaces when action/hook public contracts or authoring catalogs change.

Run `npm run build:praxis-dynamic-form` for exported action/hook API changes.
Run core build/focused tests too when the canonical global-action or surface-open contract changes.

## Companion Skills

- Use `praxis-form-submit-payload-pipeline` when actions trigger or affect submit payloads.
- Use `praxis-form-editor-document-roundtrip` when actions/hooks are edited through Settings Panel or authoring documents.
- Use `praxis-form-ai-rules-validation` when actions or hooks are authored through component edit plans or rule diagnostics.
- Use `praxis-core-global-actions-metadata` for shared global actions, catalogs, payload schemas, and metadata registry behavior.
