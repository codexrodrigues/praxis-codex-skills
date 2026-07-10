---
name: praxis-form-actions-hooks-runtime
description: Use when Codex must work on @praxisui/dynamic-form actions, hooks, PraxisFormActionsComponent, action authoring, global action refs, surface open payloads, action visibility/shortcuts, submit/cancel/reset/custom action behavior, hook registries, or action editor round-trip.
---

# Praxis Form Actions Hooks Runtime

Use this skill for Dynamic Form action surfaces and hook execution. Actions and hooks are runtime materializations of declared `FormConfig`, global action catalogs, and hook registries; do not implement host-local command parsing or keyword-driven routing.

## Source Audit

Inspect the affected owner before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.ts`
- `projects/praxis-dynamic-form/src/lib/components/praxis-form-actions/praxis-form-actions.component.ts`
- `projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.ts`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`

Inspect `@praxisui/core` for `GlobalActionRef`, global action catalogs, payload validation helpers, `SurfaceOpenPayload`, action metadata, and effect policies.

## Runtime Rules

- Default actions are submit, cancel, and reset; custom actions come from `FormConfig.actions.custom`.
- Runtime rule overrides may alter visibility, disabled state, labels, classes, or other supported action fields.
- `PraxisFormActionsComponent` owns action rendering, collapsed/mobile grouping, shortcut registration, invalid submit hints, and emits `PraxisFormActionEvent`.
- Submit actions must still pass through the canonical submit pipeline.
- Global actions must be represented as declared action refs with validated payloads.
- Surface open payloads should use the canonical `SurfaceOpenPayload` shape, including presentation, widget, bindings, and context.
- Hooks should execute through the registered hook contract and declared stages, not through arbitrary host callbacks hidden in config.

When a required command is missing, extend the canonical action/hook/global action contract. Do not add regex, aliases, or local prompt parsing as the primary decision path.

## Authoring Rules

- Use the injected global action catalog when available; fallback catalogs are for local authoring coverage, not new semantics.
- Preserve unknown but valid payload fields only when the canonical payload schema allows them.
- Required action params must be validated with the core helper.
- Actions editor, hooks editor, JSON editor, and Settings Panel must round-trip the same config shape.
- Put framework-owned visible text in dynamic-form i18n, not hardcoded component copy.

## Aderence Inventory

Classify action/hook changes before adding a contract:

- `ja-suportado-so-ux`: runtime works, but editor affordance, label, diagnostics, or shortcut behavior is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: global action catalog, hook registry, or payload schema exists but is not surfaced correctly.
- `suportado-parcialmente`: the declared action exists, but one runtime/editor branch is missing.
- `lacuna-real-de-contrato`: no declared action, hook stage, payload schema, or global action contract can express the requirement.

Only `lacuna-real-de-contrato` should create a new public action or hook contract.

## Validation

- action rendering: `praxis-form-actions.component.spec.ts` or focused component specs
- action authoring: `actions-editor` specs and `global-action-authoring.util.spec.ts` when present
- hooks: `hooks-editor` specs and focused runtime hook specs
- command/rule effects: `form-rules.service.spec.ts` and `praxis-dynamic-form.spec.ts`
- browser validation when action placement, mobile collapse, shortcuts, or visible command behavior changes

Run `npm run build:praxis-dynamic-form` for exported action/hook API changes.

## Companion Skills

- Use `praxis-form-submit-payload-pipeline` when actions trigger or affect submit payloads.
- Use `praxis-form-editor-document-roundtrip` when actions/hooks are edited through Settings Panel or authoring documents.
- Use `praxis-form-ai-rules-validation` when actions or hooks are authored through component edit plans or rule diagnostics.
- Use `praxis-core-global-actions-metadata` for shared global actions, catalogs, payload schemas, and metadata registry behavior.
