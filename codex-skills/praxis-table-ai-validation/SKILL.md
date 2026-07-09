---
name: praxis-table-ai-validation
description: Use when Codex must inspect, change, or validate @praxisui/table AI authoring: AI manifests, component edit plans, table AI capabilities, runtime operations, filter/action intent grounding, context packs, selected-record context, registry ingestion, AI recipes, or table assistant Playwright flows.
---

# Praxis Table AI Validation

Use this skill for table AI authoring and validation. The table assistant must operate through declared semantic contracts: component edit plans, runtime operations, capability catalogs, filter field catalogs, selected-record context, global action catalogs, resource surfaces, and AI registry ingestion. It must not route primary intent through local keyword matching.

For shared AI runtime, manifest, registry, or semantic intent work, pair this skill with `praxis-ai-assistant-runtime`, `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, or `praxis-ai-semantic-intent`.

## Source Audit

Inspect the AI and registry surface:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/ai/praxis-table-authoring-manifest.ts`
- `projects/praxis-table/src/lib/ai/table-component-edit-plan.ts`
- `projects/praxis-table/src/lib/ai/table-component-ai-capabilities.ts`
- `projects/praxis-table/src/lib/ai/table-ai-capabilities.ts`
- `projects/praxis-table/src/lib/ai/table-authoring-registry.ts`
- `projects/praxis-table/src/lib/ai/table-agentic-authoring-turn-flow.ts`
- `projects/praxis-table/src/lib/ai/table-ai.adapter.ts`
- `projects/praxis-table/src/lib/ai/table-context-pack.ts`
- `projects/praxis-table/src/lib/ai/filter-form-dialog-host-context-pack.ts`
- `projects/praxis-table/src/lib/ai/*.spec.ts`
- `projects/praxis-table/test-dev/e2e/table-ai-*.playwright.spec.ts`
- `projects/praxis-table/test-dev/e2e/table-ai-assistant-selection-context.playwright.spec.ts`

Inspect `tools/ai-registry/AGENTS.md` when registry ingestion or component authoring catalog output changes.

## AI Contract Rules

- Component edit plans are for authoring config changes, not for executing runtime operations.
- Runtime operations are for declared immediate actions such as applying filters, exporting data, or opening related surfaces.
- Filter questions must be grounded in `filterFieldCatalog`, resource metadata, and runtime operations.
- Column visibility, public/private presentation, format, renderer, style, value mapping, computed columns, toolbar, row, bulk, and export authoring must use declared edit plan change kinds and operation ids.
- Capability discovery questions should answer from the catalog and stay consultative until the user explicitly asks to add, apply, or materialize.
- Global actions must be chosen from declared catalogs and payload schemas. Ask concise clarification when required payload cannot be grounded.
- Selected-record context must be sanitized and human-facing; do not expose raw IDs, internal fields, endpoint paths, schema keys, or payload examples unless explicitly requested.
- Do not invent unsupported OR/nested boolean filters when the resource/runtime contract does not materialize them.

## Intent Guardrail

Do not add local keyword, regex, alias, or fuzzy matching as the primary intent router. Text matching is allowed only after a canonical intent/operation scope exists, for ranking declared fields/actions/surfaces or asking clarification.

When a required operation is missing, model or extend the canonical AI/tool contract. Do not replace the missing tool with local prompt parsing inside table components.

## Validation

- Manifest changes: `praxis-table-authoring-manifest.spec.ts` and table authoring registry specs.
- Component edit plans: `table-component-edit-plan` specs and AI adapter specs.
- Runtime operations: `table-agentic-authoring-turn-flow.spec.ts`, `table-ai.adapter.spec.ts`, and E2E flows for selected records, filters, export, and consultative follow-up.
- AI registry: `npm run generate:registry:ingestion` and `npm run validate:catalog` when the manifest/catalog surface changes.
- Browser-real AI: use focused Playwrights such as `table-ai-assistant-component-edit-plan`, `table-ai-assistant-selection-context`, `table-ai-assistant-consultative-follow-up`, and opt-in live matrix only when live AI is intentionally required.

State whether live AI E2E was skipped. Do not use GitHub Actions as exploratory validation.

## Companion Skills

- Use `praxis-table-runtime-data` for runtime state, selection, local/remote data mode, export, analytics, and renderers.
- Use `praxis-table-filter-actions` for filter/action operation grounding.
- Use `praxis-table-authoring-settings` for Settings Panel and config editor round-trip.
- Use `praxis-table-rule-ai-validation` when AI authoring targets table visual effects, presets, semantic animations, or `tableIntegration.delegate`.
- Use `praxis-table-rule-table-integration` when table-owned renderer placement must coordinate with table-rule-builder effect payloads.
- Use `praxis-core-runtime-contracts` and `praxis-core-resource-runtime` for shared AI contracts, resource capabilities, surfaces, and schema grounding.
- Use `praxis-authoring-editors` for cross-component authoring/persistence patterns.
