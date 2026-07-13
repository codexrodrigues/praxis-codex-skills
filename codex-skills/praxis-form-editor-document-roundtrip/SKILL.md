---
name: praxis-form-editor-document-roundtrip
description: Use when Codex must work on @praxisui/dynamic-form or praxis-dynamic-form package DynamicFormAuthoringDocument, editor capability apply plans, Settings Panel round-trip, bindings, contextSnapshot, presentation snapshots, schema preferences, backConfig, legacy editor payload migration, diagnostics, apply/save/reset, or runtime/editor synchronization.
---

# Praxis Form Editor Document Roundtrip

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the canonical authoring document contract of `@praxisui/dynamic-form`. The editor document is the complete snapshot exchanged by Settings Panel/editor surfaces; runtime discovery values are evidence, not persisted semantic ownership.

## Source Audit

Inspect these files before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-document.model.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`
- `projects/praxis-dynamic-form/src/lib/settings-panel.providers.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-authoring-protocol.spec.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.first-config-hydration.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.config-editor.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.spec.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/**`
- `projects/praxis-dynamic-form/src/lib/behavior-editor/**`
- `projects/praxis-dynamic-form/src/lib/rules-editor/**`
- `projects/praxis-dynamic-form/src/lib/messages-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/json-config-editor/**`
- `projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.ts`
- `projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`
- `projects/praxis-dynamic-form/src/lib/json-config-editor/form-json-config-editor.json-api.md`
- related JSON API docs for editor surfaces when public docs or generated docs can change

Inspect `projects/praxis-settings-panel/AGENTS.md` when changing Settings Panel providers, drawer values, `apply`, `save`, `reset`, ETag, or persistence behavior.

For Settings Panel protocol changes, inspect these concrete files:

- `projects/praxis-settings-panel/src/lib/settings-panel.component.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.ref.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- `projects/praxis-settings-panel/src/lib/ai/praxis-settings-panel-authoring-manifest.ts`
- `projects/praxis-settings-panel/src/lib/ai/praxis-settings-panel-authoring-manifest.spec.ts`

## Document Contract

`DynamicFormAuthoringDocument` has:

- `kind: "praxis.dynamic-form.editor"`
- `version: 1`
- `config: FormConfig`
- optional `bindings`, currently including `mode`
- optional `contextSnapshot`, including `backConfig`, `presentation`, and `schemaPrefs`

Canonical apply/save is replace-all:

- `config` replaces previous config.
- `bindings` replaces previous persistible bindings.
- missing `bindings.mode` clears persisted mode.
- `contextSnapshot` replaces previous authoring context.
- missing `backConfig`, `presentation`, or `schemaPrefs` inside `contextSnapshot` clears that block.
- runtime values such as `schemaUrl`, `submitUrl`, `submitMethod`, and resolved resource metadata are diagnostics only; do not persist them into bindings or context snapshots.
- editor `runtimeContext` is read-only operational evidence. It may expose `resolvedContract.schemaUrl`, `submitUrl`, or `submitMethod` in the UI, but must not be copied into the authoring document.
- `formRulesState` is internal derived round-trip state for the visual builder. Do not make AI, JSON authoring, or manual editor workflows write it directly; derive or preserve it through the existing editor paths.

Legacy editor payloads may be normalized into the canonical document, but new code should author the document shape directly.

`DynamicFormAuthoringDocument` owns authoring state only. `FormConfig` owns form config. `bindings` owns persistible runtime mode preferences. `contextSnapshot` owns persistible authoring context such as `backConfig`, presentation, and schema preferences. Host discovery values, resolved schema URLs, submit endpoints, HTTP methods, and current resource metadata are read-only diagnostics and may appear in editor UI only as evidence.

Field metadata editor patches may use merge semantics inside the edited field. For nested `entityLookup.optionSource`, preserve existing canonical values such as `key`, `resourcePath`, `valuePropertyPath`, and `capabilities.byIds` when editing only `dependsOn`, `selectionPolicy`, `detail`, or audit metadata.

`domainRules` is a runtime input for consuming governed materializations from
`/api/praxis/config/domain-rules/materializations`; it is not a field of
`DynamicFormAuthoringDocument`. Do not save materialized `DomainRuleMaterialization` rules back into
`config.formRules` as if the editor authored them locally. If a product explicitly needs to detach a
governed projection into local config, require a named migration/detach decision and preserve
`metadata.domainRule` provenance so the loss of governance is visible.

Schema/layout materializations with `layoutPolicy.persistence='transient'` are runtime projections.
Do not persist generated sections, runtime `domainRules`, resolved schema URLs, submit endpoints, or
materialized domain rules into the authoring document just because the user opened Settings Panel.

Filter form and dynamic form widget editors must follow the same document semantics. Do not create a separate filter-form authoring document unless the shared contract cannot represent a proven gap.

## Apply Plan Rules

The editor capability should produce an apply plan that names what changes:

- `canonicalConfig`
- `bindingsPatch`
- `contextSnapshot`
- persistence flags for config, bindings, and context snapshot
- runtime refresh flags for mode, presentation, schema state, and back navigation
- metadata flags such as schema snapshot attachment
- diagnostics for invalid document kind/version, config shape, mode, schema prefs, presentation, and command rules

Do not silently merge partial editor state when the canonical document requires replacement semantics.

When `replaceContext` is active, absence is intentional: absent `bindings.mode`, `contextSnapshot.presentation`, `contextSnapshot.schemaPrefs`, or `contextSnapshot.backConfig` should emit clear flags/patches that remove previously persisted values. A partial editor form that does not own a block must either preserve it explicitly or declare why replacement is correct.

AI-generated edit plans must target the canonical document/apply-plan surface. Do not let AI output ad hoc config patches, prompt-only field moves, or local editor state when the existing capability can express the change.

For Ergon-style migrations, distinguish authored local form configuration from reusable platform
decisions before applying/saving: local layout polish can round-trip through the document, but legal
guidance, shared validation, command availability, approval policy, option-source policy, and other
governed decisions should remain in `domain-rules` or metadata-backed contracts and project into the
runtime. A successful editor reopen is not proof that the canonical owner is correct if the save
silently converted governed runtime evidence into local `FormConfig`.

## Round-Trip Checklist

For every editor change, prove or inspect:

1. Existing runtime/editor document opens with the correct values.
2. The canonical editor surface can modify the values.
3. Apply emits the expected document/apply plan.
4. Runtime reflects the applied values.
5. Save persists the intended config, bindings, and context snapshot.
6. Reopen reconstructs the same document.
7. Reset clears only the intended block.

If the change has no visual editor impact, state why.

Also identify which path owns the proof:

- Settings Panel provider lifecycle: drawer value, apply, save, reset, ETag/persistence integration.
- Widget config editor: dynamic form and filter form document creation, serialization, and reopen.
- Config editor tabs: layout, behavior, rules, messages, hooks, actions, JSON, and cascades.
- Runtime hydration: first config hydration, external config hydration, mode/presentation/schema refresh, and back navigation.
- AI authoring: manifest operation, turn flow, diagnostics, and generated apply plan.
- Governed runtime projections: `domainRules` options, materialization status, provenance in
  `metadata.domainRule`, and whether save/reopen preserves the projection as external evidence
  instead of converting it into local authored `formRules`.

## Aderence Inventory

Classify editor gaps before adding a contract:

- `ja-suportado-so-ux`: document/apply plan is right, but editor UI or diagnostics are incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a value exists in config, bindings, or context snapshot but is surfaced under the wrong editor concept.
- `suportado-parcialmente`: one editor path round-trips while Settings Panel, JSON editor, or reopen path does not.
- `lacuna-real-de-contrato`: the value cannot be represented by `FormConfig`, bindings, context snapshot, or existing settings provider.

Only `lacuna-real-de-contrato` justifies a new public document field.

Treat a value that works in one editor tab but fails in another path as `suportado-parcialmente`, not a new contract. First repair the missing editor, JSON, Settings Panel, apply-plan, or reopen projection.

## Validation

- Document normalization/apply plan: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-authoring-protocol.spec.ts`
- Widget editor round-trip: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form-widget-config-editor.spec.ts`
- Runtime hydration/context: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.first-config-hydration.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.layout-policy.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.compact-presentation-dom.spec.ts`
- Config/editor paths: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/json-config-editor/json-config-editor.component.spec.ts`
- Tab-specific editor paths: add the focused specs under `behavior-editor`, `rules-editor`, `messages-editor`, `hooks-editor`, `actions-editor`, and `config-editor/rule-properties-panel.component.spec.ts` when those blocks change.
- Settings Panel protocol: `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts --include=projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts --include=projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- Settings Panel AI/protocol manifest: `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/ai/praxis-settings-panel-authoring-manifest.spec.ts`
- AI/rule authoring: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.spec.ts`
- Browser authoring: focused Playwright such as `form-config-editor-smoke`, `form-config-editor-json`, `form-config-editor-layout`, `form-config-editor-behavior`, `form-config-editor-rules`, `form-config-editor-messages`, `form-config-editor-hooks`, `form-config-editor-actions`, `form-config-editor-cascades`, and apply/save/reset/reopen flows when visible behavior changes.
- `npm run build:praxis-dynamic-form` when public document models, capability exports, Settings Panel providers, or editor public APIs change.
- `npm run validate:published-doc-assets` and `npm run generate:registry:ingestion` when JSON API docs, generated docs, AI manifests, or registry surfaces change.

## Companion Skills

- Use `praxis-form-authoring-settings` for the broader editor family and Settings Panel workflow.
- Use `praxis-form-schema-runtime-modes` when bindings/context affect runtime mode, schema prefs, or presentation.
- Use `praxis-form-actions-hooks-runtime` for actions/hooks editor round-trip.
- Use `praxis-form-ai-rules-validation` for AI component edit plans, diagnostics, and registry ingestion.
