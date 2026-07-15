---
name: praxis-manual-form-rules-agentic
description: Use when implementing or auditing `@praxisui/manual-form` AI authoring, `PRAXIS_MANUAL_FORM_AUTHORING_MANIFEST`, `MANUAL_FORM_AI_CAPABILITIES`, component edit plans, `ManualFormConfigEditorComponent`, Settings Panel round-trip, `formRules`, `formRulesState`, JSON Logic alignment, agentic turn flow, context packs, registry ingestion, or governed rule handoff.
---

# Praxis Manual Form Rules Agentic

Use this skill when manual-form authoring is performed by a visual editor or AI assistant. Manual Form AI must compile to manifest-backed component edit plans and governed rule handoffs, not arbitrary JSON patches over host templates.

## Source Audit

Inspect before editing:

- `projects/praxis-manual-form/AGENTS.md`
- `projects/praxis-manual-form/README.md`
- `projects/praxis-manual-form/src/lib/components/manual-form-config-editor/manual-form-config-editor.component.ts`
- `projects/praxis-manual-form/src/lib/ai/praxis-manual-form-authoring-manifest.ts`
- `projects/praxis-manual-form/src/lib/ai/manual-form-ai-capabilities.ts`
- `projects/praxis-manual-form/src/lib/ai/manual-form-ai.adapter.ts`
- `projects/praxis-manual-form/src/lib/ai/manual-form-context-pack.ts`
- `projects/praxis-manual-form/src/lib/ai/manual-form-agentic-authoring-turn-flow.ts`
- `projects/praxis-manual-form/src/lib/praxis-manual-form.metadata.ts`
- AI manifest, capability, turn-flow, config-editor, i18n, and registry specs

## Canonical Boundary

`PRAXIS_MANUAL_FORM_AUTHORING_MANIFEST` is the executable authoring contract. `ManualFormConfigEditorComponent` is the visual editor projection. `MANUAL_FORM_AI_CAPABILITIES`, context packs, registry ingestion, and agentic turn flow are derived or consuming surfaces that must stay aligned.

Manual Form owns authoring for:

- manual field add/remove/label operations
- host-template-aware layout metadata
- toolbar enablement and quick editable flags
- autosave enablement, debounce, and persistence keys
- submit/reset/cancel behavior
- metadata bridge configuration
- `formRules` authoring as manual-form config

Delegate advanced `FieldMetadata` edits to `@praxisui/metadata-editor`, advanced `FormConfig` semantics to `@praxisui/dynamic-form`, and general rule graph editing to `@praxisui/visual-builder`.

## Manifest Rules

- Use `componentEditPlan` validated against `PRAXIS_MANUAL_FORM_AUTHORING_MANIFEST`.
- Reject free patches and require manifest operations.
- Every operation must resolve its declared target through manifest target metadata and fail on ambiguity. Do not recover ambiguous fields, layout entries, actions, persistence keys, or bridge targets with prompt keyword matching, local aliases, or nearest-match heuristics.
- `manualField.add` must validate unique field name, host template field existence, control-type discovery, metadata bridge boundaries, and round-trip.
- `manualField.remove` is destructive and requires confirmation before metadata, layout, or value loss.
- `manualField.label.set` should write through field metadata, not a host-local label map.
- `layout.configure` must not replace the host-owned Angular template.
- `toolbar.configure` remains coupled to `enableCustomization` and field metadata patches.
- `autosave.enabled.set` must validate deterministic storage key composition and safe debounce.
- `metadataBridge.configure` must preserve metadata-editor ownership.
- Shared business policy, eligibility, validation, compliance, or domain rules must hand off to governed domain/shared rule authoring before local runtime materialization.

## Rules And JSON Logic

- `formRules` is the authorable persisted rules surface.
- Each `effect.condition` must be a JSON Logic object or `null`.
- Do not generate JavaScript handlers, textual expressions, or legacy JSON Schema condition blocks for new manual-form rules.
- Treat `formRulesState` as visual-editor round-trip state and read-only/internal for AI, hosts, and tools. Preserve it when needed for reopening the visual editor, but do not author rules by writing to it; edit `formRules` and let round-trip state be derived or preserved by the editor workflow.
- Pair with `praxis-visual-builder-jsonlogic-roundtrip` when a rule comes from or returns to the visual rule graph.
- Pair with `praxis-form-ai-rules-validation` when rule semantics must materialize consistently with dynamic-form behavior.

## Editor And Registry Rules

- The config editor must preserve apply/save/reset/reopen parity with the runtime config document.
- Settings Panel integration must emit canonical config patches, not local wrappers.
- Internal authoring labels, helper text, errors, and quick replies belong in manual-form i18n catalogs.
- Keep `praxis-manual-form.metadata.ts`, component docs, authoring manifest refs, registry ingestion, and AI-ready docs aligned when public authoring behavior changes.
- The frontend must not route prompts by keywords; use semantic intent, declared operations, context packs, and governed tools.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: the manifest/config path exists but editor feedback, registry docs, or assistant UI does not expose it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer calls JSON Logic a script/expression while the canonical shape already exists as `formRules`.
- `suportado-parcialmente`: the manifest advertises an operation but config editor, validator, context pack, registry, or focused spec is incomplete.
- `lacuna-real-de-contrato`: no manifest operation, editable target, config path, rule shape, or governed handoff can express the requested authoring decision.

Only a real gap justifies a new manifest operation, capability, context-pack field, or public config path.

## Validation

Use focused local proof:

- manifest: `src/lib/ai/praxis-manual-form-authoring-manifest.spec.ts`
- capabilities: `src/lib/ai/manual-form-ai-capabilities.spec.ts`
- turn flow: `src/lib/ai/manual-form-agentic-authoring-turn-flow.spec.ts`
- config editor/Settings Panel: focused config-editor specs
- rules JSON: config-editor rules specs and visual-builder JSON Logic specs when round-trip is involved
- i18n: `src/lib/i18n/manual-form.i18n.spec.ts`
- compile: `ng build praxis-manual-form`
- registry/docs: `npm run generate:registry:ingestion` only when generated registry/component docs are affected

Pair with `praxis-manual-form-field-detection-instance`, `praxis-manual-form-autosave-persistence`, and `praxis-manual-form-toolbar-metadata-bridge` according to the affected operation.
