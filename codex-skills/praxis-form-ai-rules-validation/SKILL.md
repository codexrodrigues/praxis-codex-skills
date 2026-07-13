---
name: praxis-form-ai-rules-validation
description: Use when Codex must inspect, change, or validate @praxisui/dynamic-form or praxis-dynamic-form package AI authoring: authoring manifests, component edit plans, form AI catalogs, dynamic form rules, visual block guidance, Json Logic, diagnostics, rule authoring context, context packs, agentic turn flow, AI registry ingestion, or assistant Playwright flows.
---

# Praxis Form AI Rules Validation

This `praxis-form-*` skill family is the canonical Codex skill surface for `@praxisui/dynamic-form` and `projects/praxis-dynamic-form`; do not create parallel `praxis-dynamic-form-*` guidance unless this family cannot express a proven contract gap.

Use this skill for Dynamic Form AI authoring, rules, and validation. Form AI must operate through declared semantic contracts: component authoring manifest, component edit plans, rule authoring context, diagnostics, allowed targets/properties, context packs, and registry ingestion. It must not route primary intent through local keyword matching.

For shared AI runtime, manifest, registry, or semantic intent work, pair this skill with `praxis-ai-assistant-runtime`, `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, or `praxis-ai-semantic-intent`.

When a form rule is authored or previewed through `@praxisui/visual-builder`, pair with
`praxis-visual-builder-jsonlogic-roundtrip` for JSON Logic support and with
`praxis-visual-builder-schemas-templates` for field schemas, target/property schemas, context
variables, and template-compatible rules. Use `praxis-visual-builder-ai-validation` when the same
rule path is exposed through visual-builder AI operations.

When a rule is authored inside `@praxisui/manual-form`, pair with
`praxis-manual-form-rules-agentic`. Manual-form persists authorable rules in `formRules`, treats
`formRulesState` as visual-editor round-trip state, and must hand off shared business decisions to
governed domain/shared rule authoring before local materialization.

## Source Audit

First resolve the Angular workspace root. In the platform monorepo the files may live under
`praxis-ui-angular/projects/...`; in a standalone Angular checkout they may live directly under
`projects/...`. Audit the active `praxis-ui-angular` workspace, not stale issue worktrees such as
`praxis-ui-angular-issue*`, unless the user explicitly targets one of those worktrees.

Inspect the AI/rules surface:

- `projects/praxis-dynamic-form/AGENTS.md`
- `projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.ts`
- `projects/praxis-dynamic-form/src/lib/ai/form-ai.adapter.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-ai.adapter.ts`
- `projects/praxis-dynamic-form/src/lib/ai/form-ai-catalog.ts`
- `projects/praxis-dynamic-form/src/lib/ai/form-ai-capabilities.ts`
- `projects/praxis-dynamic-form/src/lib/ai/form-component-ai-capabilities.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-context-pack.ts`
- `projects/praxis-dynamic-form/src/lib/ai/filter-form-context-pack.ts`
- `projects/praxis-dynamic-form/src/lib/ai/dynamic-form-ai-recipes.spec.ts`
- `projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.ts`
- `projects/praxis-dynamic-form/src/lib/utils/rule-property.utils.ts`
- `projects/praxis-dynamic-form/src/lib/utils/rule-converters.ts`
- `projects/praxis-dynamic-form/src/lib/utils/form-rule.utils.ts`
- `projects/praxis-dynamic-form/src/lib/config-editor/rule-properties-panel.component.ts`
- `projects/praxis-dynamic-form/src/lib/rules-editor/rules-editor.component.ts`
- `projects/praxis-dynamic-form/src/lib/actions-editor/actions-editor.component.ts`
- `projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.ts`
- `projects/praxis-dynamic-form/src/lib/model/form-rules.model.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-llm-rule-authoring-guide.md`
- `projects/praxis-dynamic-form/docs/dynamic-form-rules-authoring-plan.md`
- `projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.json-api.md`
- `projects/praxis-dynamic-form/src/lib/config-editor/praxis-dynamic-form-config-editor.json-api.md`
- `projects/praxis-dynamic-form/test-dev/e2e/form-ai-assistant-live.playwright.spec.ts`

Inspect `tools/ai-registry/AGENTS.md` when registry ingestion or component authoring catalog output changes.

When the platform monorepo is available, also inspect the decision-authoring readiness docs before
changing manifest, adapter, recipe, registry, or public docs involving `componentEditPlan`,
`formRulesState`, `visualBlockGuidance`, or `rule.visualBlockGuidance.add`:

- `docs/2026-04-final-surface-scan-readiness.md`
- `docs/2026-04-release-readiness-decision-authoring-surface-cleanup.md`
- `docs/2026-04-form-rules-state-despromocao-backlog.md`
- `docs/2026-04-form-rules-state-inventario-superficies.md`
- `docs/2026-04-routing-canonico-intencao-backlog.md`

## AI Contract Rules

- Use component edit plans only for Dynamic Form component authoring.
- Route business-rule, policy, eligibility, validation, compliance, and shared decision authoring to governed domain/shared rule authoring before projecting local form config.
- Treat `componentEditPlan` as valid only for component/page authoring. If the prompt asks for
  business rules, policy, eligibility, validation, compliance, or shared decisions, the correct
  response is a governed `domain-rules` / `shared_rule_authoring` handoff or materialization path,
  not a local Dynamic Form edit plan.
- `field.local.add` is for local form-only fields. Do not create backend DTO fields for local/transient UI needs.
- Never write `formRulesState` directly; write `formRules` and let internals derive builder state.
- Use Json Logic only; do not generate JavaScript handlers or arbitrary functions.
- Do not assume every visual-builder node or value type is form-rule-ready. Context-variable and
  custom-function operands require a canonical JSON Logic shape before they can be projected into
  dynamic-form rules.
- Use allowed targets from rule authoring context: fields, sections, rows, columns, actions, messages, visual blocks.
- Use `RULE_PROPERTY_SCHEMA`/diagnostics as the allowed property source.
- Visual block guidance writes only visual rules or `columns[].items[]`; it must not create `FormControl`, `fieldMetadata`, or submit payload.
- `rule.visualBlockGuidance.add` and `visualBlockGuidance` may remain as optional visual
  materialization/projection of an already governed decision or a local visual request. Do not
  promote them as the recommended operation for primary business-rule authoring.
- Mark LLM-authored rules for human review when the workflow expects review.
- `formCommandRules` is the command/side-effect channel. Keep it separate from property `formRules`, validate `GlobalActionRef`, preserve structured `payload`, and treat `payloadExpr` as an advanced JSON escape hatch.
- `domainRules` materializations are shared/governed rule projections. Do not collapse them into local `formRules` as if the form were the primary business-rule owner.
- Context packs are grounding artifacts. Keep dynamic-form and filter-form context packs aligned with allowed targets, diagnostics, existing rules, actions, fields, visual blocks, and runtime/read-only evidence.
- Computed field values must use the canonical closed envelope when authoring structured values: exactly `{ "expression": <JSON Logic> }` or exactly `{ "literal": <value> }`.
- The visual property panel is a guided projection of the JSON/rule contract. Unsupported or JSON-only rule capabilities must remain visible as advanced/diagnostic state rather than being silently dropped.

## Intent Guardrail

Do not add keyword, regex, alias, or fuzzy matching as the primary intent router. Text matching is allowed only after a canonical intent/operation scope exists, for ranking declared fields/actions/targets or asking clarification.

When a required operation is missing, model or extend the canonical AI/tool contract. Do not replace the missing operation with local prompt parsing inside the form component.

Before accepting a manifest/adapter/registry change, ask whether it reduces the chance that a
business-rule prompt falls back to `componentEditPlan`, `formRulesState`, or
`rule.visualBlockGuidance.add`. If it only creates another local component route for a shared
decision, it is probably the wrong platform cut.

## Inventory Before New Contract

- `ja-suportado-so-ux`: the manifest/context/rule contract supports the operation, but assistant UI, diagnostics, property panel, or explanation is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the value exists in `formRules`, `formCommandRules`, `domainRules`, context pack, or JSON editor, but is surfaced through a local label, prompt-only wording, or visual-builder state.
- `suportado-parcialmente`: one path works while another path, such as JSON editor, visual property panel, AI assistant, diagnostics, runtime application, command-rule preview, domain-rule materialization, or reopen, drifts.
- `lacuna-real-de-contrato`: no manifest operation, component edit plan, context pack, rule schema, diagnostics path, runtime rule service, or registry ingestion surface can represent the authoring decision.

Only `lacuna-real-de-contrato` justifies new AI/rule contract work. Otherwise, repair the missing projection, diagnostic, context pack, editor bridge, or validation gate.

## Validation

- Manifest/catalog/capabilities: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/form-ai-catalog.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-ai-recipes.spec.ts`
- Context packs and AI flow: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-context-pack.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-rule-authoring-context.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/form-ai.adapter.spec.ts --include=projects/praxis-dynamic-form/src/lib/ai/dynamic-form-agentic-authoring-turn-flow.spec.ts`
- Rule runtime/diagnostics: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/services/form-rules.service.spec.ts --include=projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/form-rule.utils.spec.ts`
- Rule conversion/property authoring: `npx ng test praxis-dynamic-form --watch=false --progress=false --include=projects/praxis-dynamic-form/src/lib/utils/rule-converters.spec.ts --include=projects/praxis-dynamic-form/src/lib/utils/rule-property.utils.spec.ts --include=projects/praxis-dynamic-form/src/lib/config-editor/rule-properties-panel.component.spec.ts --include=projects/praxis-dynamic-form/src/lib/rules-editor/rules-editor.component.spec.ts`
- Actions/command rules: add `action-authoring/global-action-authoring.util.spec.ts`, `actions-editor/actions-editor.component.spec.ts`, `components/praxis-form-actions/praxis-form-actions.component.spec.ts`, and command-rule editor specs when global actions or command rules change.
- Visual block rules: add `visual-block-rule-content-overrides.util.spec.ts` and layout visual-block specs when AI/rules affect `targetType: "visualBlock"` or `columns[].items[]`.
- Registry: `npm run generate:registry:ingestion`, `npm run validate:catalog`, and `npm run validate:authoring-contracts` when manifest/catalog/capability/context-pack surfaces change.
- Decision-authoring cleanup regression: run a focused textual scan for
  `formRulesState|componentEditPlan|recommendedOperation|rule\\.visualBlockGuidance\\.add|visualBlockGuidance`
  across Dynamic Form manifests/docs/recipes and generated registry surfaces when changing AI
  authoring guidance. Classify each hit as component authoring, visual materialization, internal
  runtime state, historical doc, or canonical drift.
- Browser AI/rules: focused Playwrights for `form-ai-assistant-live`, `form-config-editor-rules`, `form-config-editor-command-rules`, `business-rules-form-demo`, `funcionarios-form-demo-rules`, and `funcionarios-form-demo-domain-rules` when visible AI/rule behavior changes.
- `npm run build:praxis-dynamic-form` when public AI/rule exports, services, docs-facing contracts, or editor APIs change.

State whether live AI E2E was skipped. Do not use GitHub Actions as exploratory validation.

## Companion Skills

- Use `praxis-form-runtime-submit` for runtime state, submit payload, field metadata, local/transient fields, and schema contracts.
- Use `praxis-form-schema-runtime-modes` for runtime inputs, schema/read/submit URL grounding, mode/presentation rules, and metadata reconciliation used by AI context.
- Use `praxis-form-submit-payload-pipeline` when AI-authored local fields, `submitPolicy`, entity lookup payloads, or nested arrays affect submit semantics.
- Use `praxis-form-actions-hooks-runtime` when AI edits form actions, hooks, global action refs, shortcuts, or surface open payloads.
- Use `praxis-form-editor-document-roundtrip` when AI output must become a `DynamicFormAuthoringDocument`, apply plan, Settings Panel save, or registry-ingested editor document.
- Use `praxis-form-layout-canvas` for layout, visual blocks, canvas, and schema-driven materialization.
- Use `praxis-form-authoring-settings` for Settings Panel and editor round-trip.
- Use `praxis-core-runtime-contracts` and `praxis-core-resource-runtime` for shared AI contracts, schema/resource grounding, option sources, and global actions.
- Use `praxis-authoring-editors` for cross-component authoring/persistence patterns.
