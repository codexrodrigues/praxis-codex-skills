---
name: praxis-form-authoring-settings
description: Use when Codex must work on @praxisui/dynamic-form or praxis-dynamic-form package authoring, Settings Panel integration, config editor, layout editor, behavior editor, rules editor, messages editor, hooks editor, actions editor, JSON config editor, widget config editor, apply/save/reset, DynamicFormAuthoringDocument, schema preferences, presentation snapshots, or runtime/editor round-trip.
---

# Praxis Form Authoring Settings

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for Dynamic Form authoring and Settings Panel flows. A change is incomplete when runtime config works but the visual editor cannot show, edit, apply, save, reset, reopen, or round-trip the same semantics.
For the canonical document/apply-plan contract itself, load `praxis-form-editor-document-roundtrip`. For action or hook editor details, pair with `praxis-form-actions-hooks-runtime`.

When Dynamic Form opens or embeds `FieldMetadataEditorComponent`, `DynamicEditorRendererComponent`,
or `CascadeManagerTabComponent`, use `praxis-metadata-editor-consumer-bridges` for the host bridge.
If the behavior belongs to the metadata editor itself, route to
`praxis-metadata-editor-renderer-coverage` or `praxis-metadata-editor-cascade-normalization` instead
of patching Dynamic Form locally.
When Dynamic Form appears inside `@praxisui/manual-form`, route manual host-template/autosave/toolbar
concerns to `praxis-manual-form-runtime-bridge` or `praxis-manual-form-ai-authoring`. When Dynamic
Form appears inside `@praxisui/editorial-forms`, keep editorial journey/snapshot/fallback concerns in
`praxis-editorial-forms-runtime` / `praxis-editorial-forms-journey-snapshot-runtime` /
`praxis-editorial-forms-presentation-diagnostics` and adapter binding in
`praxis-editorial-forms-adapters-ai` / `praxis-editorial-forms-data-collection-adapters`.

## Source Audit

First resolve the Angular workspace root. In the platform monorepo the files may live under
`praxis-ui-angular/projects/...`; in a standalone Angular checkout they may live directly under
`projects/...`. Audit the active `praxis-ui-angular` workspace, not stale issue worktrees such as
`praxis-ui-angular-issue*`, unless the user explicitly targets one of those worktrees.

Inspect the authoring surface:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/settings-panel.providers.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-document.model.ts`
- `projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-authoring-protocol.spec.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.i18n.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.metadata.spec.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/**`
- `projects/praxis-dynamic-form/src/lib/layout-editor/**`
- `projects/praxis-dynamic-form/src/lib/behavior-editor/**`
- `projects/praxis-dynamic-form/src/lib/rules-editor/**`
- `projects/praxis-dynamic-form/src/lib/messages-editor/**`
- `projects/praxis-dynamic-form/src/lib/hooks-editor/**`
- `projects/praxis-dynamic-form/src/lib/actions-editor/**`
- `projects/praxis-dynamic-form/src/lib/json-config-editor/**`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form-widget-config-editor.ts`
- `projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form.metadata.ts`
- `projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.ts`
- `projects/praxis-dynamic-form/src/lib/utils/metadata-mappers.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-authoring-document-semantics.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-visual-builder-parity-audit.md`
- platform decision-authoring docs that mention `formRulesState`, `componentEditPlan`, or
  `rule.visualBlockGuidance.add`, especially `docs/2026-04-form-rules-state-despromocao-backlog.md`
  when the platform monorepo is available
- related JSON API docs such as `config-editor/praxis-dynamic-form-config-editor.json-api.md`, `layout-editor/praxis-layout-editor.json-api.md`, and `json-config-editor/form-json-config-editor.json-api.md`

Also inspect `projects/praxis-settings-panel/AGENTS.md` when changing `SettingsValueProvider`, drawer data, `apply`, `save`, `reset`, or persisted config.

For Settings Panel protocol changes, inspect the concrete owner files instead of inferring behavior
from Dynamic Form providers alone:

- `projects/praxis-settings-panel/src/lib/settings-panel.component.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.ref.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.ts`
- `projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- `projects/praxis-settings-panel/src/lib/ai/settings-panel-ai.adapter.spec.ts`
- `projects/praxis-settings-panel/src/lib/ai/praxis-settings-panel-authoring-manifest.spec.ts`

## Authoring Document Rules

`DynamicFormAuthoringDocument` is the canonical complete authoring snapshot:

- `config` replaces the previous config.
- `bindings` replaces previous persistible bindings.
- missing `bindings.mode` clears the persisted mode binding.
- `contextSnapshot` replaces previous persisted authoring context.
- missing `backConfig`, `presentation`, or `schemaPrefs` inside `contextSnapshot` explicitly removes that block.
- runtime discovery values such as `schemaUrl`, `submitUrl`, and `submitMethod` are diagnostics only and must not be persisted into bindings or context snapshot.

Legacy partial adapter APIs can keep merge compatibility, but canonical editor apply/save is replace-all.

Settings Panel, widget config editor, embedded config editor, JSON editor, metadata editor bridge, and AI assistant must all target the same authoring document/apply-plan semantics. Do not fix an authoring value in only one tab or host surface when the canonical editor family should own the round-trip.

`formRulesState` is internal/legacy runtime and visual-builder round-trip state. Do not present it as
the canonical authoring target for business rules, compliance, eligibility, validation policy, or
shared decisions. Those decisions belong to governed semantic authoring such as `domain-rules` /
`shared_rule_authoring` and may later materialize into `form_config`, visual guidance, or runtime
state. Keep `componentEditPlan` and `rule.visualBlockGuidance.add` scoped to component/page authoring
or optional UI projection, not primary rule authoring.

## Editor Round-Trip Checklist

For every config or context change, prove or inspect:

1. Existing config/document opens in the editor with the correct value.
2. The user can change it through the canonical editor surface.
3. Apply/save emits the expected `DynamicFormAuthoringDocument` or config shape.
4. Runtime reflects the applied change.
5. Reopening the editor preserves the value.
6. Reset removes only the intended config, bindings, or context snapshot.

If no visual editor is affected, state why.

## Editor Rules

- Start by identifying the owner path: Settings Panel provider, widget config editor, embedded config editor, layout editor, behavior editor, rules/command rules editor, messages editor, hooks editor, actions editor, JSON editor, metadata editor bridge, or AI authoring.
- Keep `fieldMetadata` patches deep-merged where needed, especially `entityLookup.optionSource`, so editor changes do not erase canonical lookup contracts.
- Keep rules, messages, hooks, actions, behavior, hints, schema preferences, navigation, presentation, and JSON editor in sync.
- Keep authoring text in the dynamic-form i18n catalog; do not add visible hardcoded strings.
- Do not create component-specific local editors in a host when `ComponentDocMeta.configEditor` or the owning Dynamic Form editor should handle it.
- Treat `Apply` working without `Save`, or `Save` working without reopen, as incomplete.
- Treat runtime-only host values shown in the editor, such as schema URL, submit URL, submit method, and resolved metadata, as read-only diagnostics unless the authoring document explicitly owns the field.
- Treat `formRulesState` echoes in visual-builder paths as derived state to preserve, not a new
  public AI/write contract.
- Treat a stale visual-builder echo, JSON-only advanced path, or tab-local fallback as a partial implementation until reopen and JSON editor paths preserve the same semantics.
- When an editor embeds `FieldMetadataEditorComponent`, `DynamicEditorRendererComponent`, or `CascadeManagerTabComponent`, use the metadata-editor consumer bridge contract instead of reimplementing metadata editor logic in Dynamic Form.
- Dynamic Form may delegate to manual-form or editorial-forms hosts, but those hosts must not redefine Dynamic Form authoring semantics through local autosave, toolbar, or journey snapshot shortcuts.

## Inventory Before New Contract

- `ja-suportado-so-ux`: the document/apply-plan and runtime support the value, but a tab, Settings Panel affordance, diagnostic, or copy is missing.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a value exists in `FormConfig`, `bindings`, `contextSnapshot`, metadata editor bridge, or JSON editor but is surfaced under the wrong editor concept or local label.
- `suportado-parcialmente`: one path works while another path, such as Settings Panel, embedded editor, JSON editor, metadata bridge, AI assistant, apply/save/reset, or reopen, drifts.
- `lacuna-real-de-contrato`: no existing authoring document, config field, binding, context snapshot, metadata bridge, or Settings Panel provider can represent the value.

Only `lacuna-real-de-contrato` justifies a new authoring/settings contract. Otherwise, fix the missing projection, provider, editor tab, i18n copy, JSON path, or validation gate.

## Validation

- Settings Panel/document semantics: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/dynamic-form-editor-capability.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-authoring-protocol.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form-widget-config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/filter-form/praxis-filter-form-widget-config-editor.spec.ts`
- Settings Panel owner protocol: `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts --include=projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts --include=projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- Settings Panel AI/protocol manifest: `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/ai/settings-panel-ai.adapter.spec.ts --include=projects/praxis-settings-panel/src/lib/ai/praxis-settings-panel-authoring-manifest.spec.ts`
- Config and JSON editor: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form.config-editor.cascade.integration.spec.ts --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.config-editor.spec.ts --include=projects/praxis-dynamic-form/src/lib/json-config-editor/json-config-editor.component.spec.ts`
- Layout editor: include `layout-editor/layout-editor.component.spec.ts`, `field-configurator.component.spec.ts`, `row-configurator.component.spec.ts`, `section-configurator.component.spec.ts`, `apply-section-preset.util.spec.ts`, and `visual-block-presets.spec.ts` when layout or visual blocks change.
- Behavior/rules/messages/hooks/actions: include focused editor specs such as `behavior-editor.component.spec.ts`, `rules-editor.component.spec.ts`, `messages-editor.component.spec.ts`, `actions-editor.component.spec.ts`, `rule-properties-panel.component.spec.ts`, and hook specs when present.
- Metadata bridge and coverage: include `praxis-dynamic-form.metadata.spec.ts`, filter-form metadata specs, and metadata-editor bridge specs when the Settings Panel embeds metadata-editor controls.
- AI authoring: include `praxis-dynamic-form-authoring-manifest.spec.ts`, `dynamic-form-agentic-authoring-turn-flow.spec.ts`, and `dynamic-form-rule-authoring-context.spec.ts` when AI assistant or component edit plans change.
- Browser authoring: Playwrights such as `form-config-editor-smoke`, `form-config-editor-layout`, `form-config-editor-rules`, `form-config-editor-messages`, `form-config-editor-hooks`, `form-config-editor-actions`, `form-config-editor-actions-custom`, `form-config-editor-behavior`, `form-config-editor-json`, `form-config-editor-hints`, `form-config-editor-cascades`, and domain demos when visible editor behavior changes.
- `npm run build:praxis-dynamic-form` when public editor APIs, metadata, providers, or exports change.
- `npm run validate:published-doc-assets` and `npm run generate:registry:ingestion` when JSON API docs, AI manifests, generated docs, or registry surfaces change.

## Companion Skills

- Use `praxis-authoring-editors` for cross-component Settings Panel and round-trip guidance.
- Use `praxis-form-runtime-submit` when authoring changes runtime construction, submit behavior, field metadata, or resource contracts.
- Use `praxis-form-editor-document-roundtrip` for `DynamicFormAuthoringDocument`, bindings, context snapshots, diagnostics, replace-all apply/save/reset, and reopen semantics.
- Use `praxis-form-schema-runtime-modes` when authoring changes schema URLs, mode bindings, presentation mode, schema preferences, or metadata reconciliation.
- Use `praxis-form-submit-payload-pipeline` when editors expose local/transient fields, `submitPolicy`, entity lookup payload mode, or payload-affecting metadata.
- Use `praxis-form-actions-hooks-runtime` for actions editor, hooks editor, global action refs, surface open payloads, and shortcut/action runtime round-trip.
- Use `praxis-form-layout-canvas` for layout editor, visual blocks, canvas, schema-driven layout policy, and presentation.
- Use `praxis-form-ai-rules-validation` for AI component edit plans, rules, diagnostics, and registry ingestion.
- Use `praxis-dynamic-fields-editorial` for field component coverage and metadata editor chains.
- Use `praxis-metadata-editor-consumer-bridges` for Dynamic Form bridge behavior around metadata-editor hosted editors.
- Use `praxis-manual-form-ai-authoring`, `praxis-editorial-forms-adapters-ai`, or `praxis-editorial-forms-data-collection-adapters` when Dynamic Form is delegated by those package owners.
