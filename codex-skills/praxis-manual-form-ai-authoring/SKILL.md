---
name: praxis-manual-form-ai-authoring
description: Use when changing or validating `@praxisui/manual-form` authoring surfaces, including `ManualFormConfigEditorComponent`, Settings Panel integration, `PRAXIS_MANUAL_FORM_AUTHORING_MANIFEST`, `MANUAL_FORM_AI_CAPABILITIES`, agentic authoring turn flow, component edit plans, formRules JSON Logic, toolbar/autosave/submit operations, metadata bridge configuration, AI registry ingestion, docs, and round-trip validation.
---

# Praxis Manual Form AI Authoring

Use this skill for governed manual-form authoring. Manual Form AI must compile to manifest-backed component edit plans; it must not emit arbitrary JSON patches over host templates or duplicate `dynamic-form`/`metadata-editor` semantics.

## Required Source Audit

Inspect:

- `projects/praxis-manual-form/AGENTS.md`
- `src/lib/components/manual-form-config-editor/manual-form-config-editor.component.ts`
- `src/lib/ai/praxis-manual-form-authoring-manifest.ts`
- `src/lib/ai/manual-form-ai-capabilities.ts`
- `src/lib/ai/manual-form-ai.adapter.ts`
- `src/lib/ai/manual-form-context-pack.ts`
- `src/lib/ai/manual-form-agentic-authoring-turn-flow.ts`
- `src/lib/praxis-manual-form.metadata.ts`
- `src/public-api.ts`
- README, API docs, docs manifest, and focused specs

## Authoring Boundary

Manual Form authoring owns manual-form concerns:

- manual field add/remove metadata
- labels and basic field metadata patches
- host-template-aware layout configuration
- toolbar enablement and editable flags
- autosave enablement/debounce/persistence keys
- submit/reset/cancel behavior
- metadata bridge configuration

Delegate advanced `FieldMetadata` shape changes to `@praxisui/metadata-editor`. Delegate advanced `FormConfig` layout/config semantics to `@praxisui/dynamic-form`. Delegate rule graph editing to the visual rules owner when the task becomes a general rule-builder concern.

## Manifest Rules

Use `PRAXIS_MANUAL_FORM_AUTHORING_MANIFEST` as the executable contract.

- `manualField.add` must verify unique field name, host-template field existence, control-type discovery, and metadata-editor delegation when advanced metadata is required.
- `manualField.remove` is destructive and requires confirmation before metadata/layout/value loss.
- `manualField.label.set` should write through the metadata bridge, not a host-local label map.
- `layout.configure` must not replace the host-owned template layout.
- `toolbar.configure` stays behind `enableCustomization`.
- `autosave.enabled.set` must validate deterministic storage key composition and safe debounce.
- `metadataBridge.configure` must preserve `praxis-metadata-editor` and dynamic-fields discovery ownership.

`formRules` is the authorable rules surface and conditions must be JSON Logic objects. Treat `formRulesState` as internal visual-editor round-trip state.

## AI And Registry

- Do not route prompts by keywords in the frontend.
- Use component edit plans and declared operations.
- Keep `MANUAL_FORM_AI_CAPABILITIES` aligned with the manifest, config editor, and runtime behavior.
- Update AI registry ingestion when component metadata, capabilities, manifests, or docs projections change.
- Keep internal authoring text in the manual-form i18n catalogs.

## Validation

Minimum gates:

- manifest: `src/lib/ai/praxis-manual-form-authoring-manifest.spec.ts`
- capabilities: `src/lib/ai/manual-form-ai-capabilities.spec.ts`
- turn flow: `src/lib/ai/manual-form-agentic-authoring-turn-flow.spec.ts`
- config editor and Settings Panel: focused config-editor specs
- i18n: `src/lib/i18n/manual-form.i18n.spec.ts`
- compile: `ng build praxis-manual-form`
- registry/docs: `npm run generate:registry:ingestion` only when generated AI/component registry artifacts are affected

Pair with `praxis-manual-form-runtime-bridge` for runtime/autosave/bridge changes and `praxis-angular-validation-gates` to choose the smallest proof.
