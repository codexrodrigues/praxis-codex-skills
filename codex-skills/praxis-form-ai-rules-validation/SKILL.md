---
name: praxis-form-ai-rules-validation
description: Use when Codex must inspect, change, or validate @praxisui/dynamic-form AI authoring: authoring manifests, component edit plans, form AI catalogs, dynamic form rules, visual block guidance, Json Logic, diagnostics, rule authoring context, context packs, agentic turn flow, AI registry ingestion, or assistant Playwright flows.
---

# Praxis Form AI Rules Validation

Use this skill for Dynamic Form AI authoring, rules, and validation. Form AI must operate through declared semantic contracts: component authoring manifest, component edit plans, rule authoring context, diagnostics, allowed targets/properties, context packs, and registry ingestion. It must not route primary intent through local keyword matching.

For shared AI runtime, manifest, registry, or semantic intent work, pair this skill with `praxis-ai-assistant-runtime`, `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, or `praxis-ai-semantic-intent`.

## Source Audit

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
- `projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.ts`
- `projects/praxis-dynamic-form/src/lib/services/form-rules.service.ts`
- `projects/praxis-dynamic-form/docs/dynamic-form-llm-rule-authoring-guide.md`
- `projects/praxis-dynamic-form/test-dev/e2e/form-ai-assistant-live.playwright.spec.ts`

Inspect `tools/ai-registry/AGENTS.md` when registry ingestion or component authoring catalog output changes.

## AI Contract Rules

- Use component edit plans only for Dynamic Form component authoring.
- Route business-rule, policy, eligibility, validation, compliance, and shared decision authoring to governed domain/shared rule authoring before projecting local form config.
- `field.local.add` is for local form-only fields. Do not create backend DTO fields for local/transient UI needs.
- Never write `formRulesState` directly; write `formRules` and let internals derive builder state.
- Use Json Logic only; do not generate JavaScript handlers or arbitrary functions.
- Use allowed targets from rule authoring context: fields, sections, rows, columns, actions, messages, visual blocks.
- Use `RULE_PROPERTY_SCHEMA`/diagnostics as the allowed property source.
- Visual block guidance writes only visual rules or `columns[].items[]`; it must not create `FormControl`, `fieldMetadata`, or submit payload.
- Mark LLM-authored rules for human review when the workflow expects review.

## Intent Guardrail

Do not add keyword, regex, alias, or fuzzy matching as the primary intent router. Text matching is allowed only after a canonical intent/operation scope exists, for ranking declared fields/actions/targets or asking clarification.

When a required operation is missing, model or extend the canonical AI/tool contract. Do not replace the missing operation with local prompt parsing inside the form component.

## Validation

- manifest/catalog: `praxis-dynamic-form-authoring-manifest.spec.ts`, `form-ai-catalog.spec.ts`, component capability specs
- rules: `dynamic-form-rule-authoring-context.spec.ts`, `rule-authoring-diagnostics.spec.ts`, `form-rules.service.spec.ts`, rule converter/property specs
- AI adapter/turn flow: `form-ai.adapter.spec.ts`, `dynamic-form-agentic-authoring-turn-flow.spec.ts`, dynamic-form AI recipe specs
- registry: `npm run generate:registry:ingestion` and `npm run validate:catalog` when the manifest/catalog surface changes
- browser AI/rules: focused Playwrights for form assistant, command rules, business rules, domain rules, and config editor rules

State whether live AI E2E was skipped. Do not use GitHub Actions as exploratory validation.

## Companion Skills

- Use `praxis-form-runtime-submit` for runtime state, submit payload, field metadata, local/transient fields, and schema contracts.
- Use `praxis-form-layout-canvas` for layout, visual blocks, canvas, and schema-driven materialization.
- Use `praxis-form-authoring-settings` for Settings Panel and editor round-trip.
- Use `praxis-core-runtime-contracts` and `praxis-core-resource-runtime` for shared AI contracts, schema/resource grounding, option sources, and global actions.
- Use `praxis-authoring-editors` for cross-component authoring/persistence patterns.
