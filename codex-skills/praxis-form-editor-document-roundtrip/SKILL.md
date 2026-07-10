---
name: praxis-form-editor-document-roundtrip
description: Use when Codex must work on @praxisui/dynamic-form DynamicFormAuthoringDocument, editor capability apply plans, Settings Panel round-trip, bindings, contextSnapshot, presentation snapshots, schema preferences, backConfig, legacy editor payload migration, diagnostics, apply/save/reset, or runtime/editor synchronization.
---

# Praxis Form Editor Document Roundtrip

Use this skill for the canonical authoring document contract of `@praxisui/dynamic-form`. The editor document is the complete snapshot exchanged by Settings Panel/editor surfaces; runtime discovery values are evidence, not persisted semantic ownership.

## Source Audit

Inspect these files before editing:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-document.model.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`
- `projects/praxis-dynamic-form/src/lib/settings-panel.providers.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/**`
- `projects/praxis-dynamic-form/src/lib/behavior-editor/**`
- `projects/praxis-dynamic-form/src/lib/rules-editor/**`
- `projects/praxis-dynamic-form/src/lib/messages-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/json-config-editor/**`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`

Inspect `projects/praxis-settings-panel/AGENTS.md` when changing Settings Panel providers, drawer values, `apply`, `save`, `reset`, ETag, or persistence behavior.

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

Legacy editor payloads may be normalized into the canonical document, but new code should author the document shape directly.

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

## Aderence Inventory

Classify editor gaps before adding a contract:

- `ja-suportado-so-ux`: document/apply plan is right, but editor UI or diagnostics are incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a value exists in config, bindings, or context snapshot but is surfaced under the wrong editor concept.
- `suportado-parcialmente`: one editor path round-trips while Settings Panel, JSON editor, or reopen path does not.
- `lacuna-real-de-contrato`: the value cannot be represented by `FormConfig`, bindings, context snapshot, or existing settings provider.

Only `lacuna-real-de-contrato` justifies a new public document field.

## Validation

- document normalization/validation: `dynamic-form-editor-capability.spec.ts`
- Settings Panel: provider and widget config editor specs
- config/editor paths: focused specs under `config-editor`, `behavior-editor`, `rules-editor`, `messages-editor`, `hooks-editor`, `actions-editor`, and `json-config-editor`
- browser authoring: focused Playwright for apply/save/reset/reopen when visible editor behavior changes
- public API changes: `npm run build:praxis-dynamic-form`

## Companion Skills

- Use `praxis-form-authoring-settings` for the broader editor family and Settings Panel workflow.
- Use `praxis-form-schema-runtime-modes` when bindings/context affect runtime mode, schema prefs, or presentation.
- Use `praxis-form-actions-hooks-runtime` for actions/hooks editor round-trip.
- Use `praxis-form-ai-rules-validation` for AI component edit plans, diagnostics, and registry ingestion.
