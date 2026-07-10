---
name: praxis-table-rule-ai-validation
description: Use when Codex must change, audit, or validate AI-assisted authoring for `@praxisui/table-rule-builder` or the praxis-table-rule-builder package, including `PRAXIS_TABLE_RULE_BUILDER_AUTHORING_MANIFEST`, table-rule-builder AI adapter, capabilities, context packs, effect registry operations, `rule.add`, `rule.remove`, `condition.set`, `effect.add`, `effect.update`, `effect.remove`, `preset.apply`, `animation.set`, `tableIntegration.delegate`, diagnostics, docs, examples, or registry ingestion.
---

# Praxis Table Rule AI Validation

The `praxis-table-rule-*` skill family is the canonical Codex skill surface for `@praxisui/table-rule-builder` and `projects/praxis-table-rule-builder`; do not create parallel `praxis-table-rule-builder-*` guidance unless this family cannot express a proven contract gap.

Use this skill for agentic authoring of table visual effects. AI should author governed table visual decisions, not raw CSS patches, local table config writes, or keyword-routed command strings.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-table-rule-builder/AGENTS.md`
- `projects/praxis-table-rule-builder/src/lib/ai/praxis-table-rule-builder-authoring-manifest.ts`
- `projects/praxis-table-rule-builder/src/lib/ai/table-rule-builder-ai.adapter.ts`
- `projects/praxis-table-rule-builder/src/lib/ai/table-rule-builder-ai-capabilities.ts`
- `projects/praxis-table-rule-builder/src/lib/ai/table-rule-builder-context-pack.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/**`
- `projects/praxis-table/src/lib/ai/praxis-table-authoring-manifest.ts` when operations delegate to table
- `tools/ai-registry/**` when registry projection changes
- focused manifest, adapter, capability, context-pack, effects, and registry specs

## Canonical Boundary

`PRAXIS_TABLE_RULE_BUILDER_AUTHORING_MANIFEST` governs table visual effect authoring only. It owns rule/effect identity, condition attachment to table context, effect registry categories, default presets, semantic animations, fail-closed conversion, and explicit delegation to `praxis-table`.

It does not own table columns, datasource, renderer placement, table ordering, `TableConfigV2`, or general visual-builder JSON Logic. Those must route through `praxis-table`, `praxis-visual-builder-rules`, or the focused `praxis-visual-builder-jsonlogic-roundtrip` skill when the concern is condition parsing/export.

## AI Authoring Rules

- Route intent through declared manifest operations and semantic targets, not keyword lists or local regexes.
- Use stable `ruleId`, `effectId`, and `presetKey`; never use array index as canonical identity.
- Use `rule.add` and `condition.set` only after table context and field/column availability are grounded.
- Use `effect.add`, `effect.update`, and `effect.remove` only for registry-backed effect categories.
- Use `preset.apply` only for known `DEFAULT_EFFECT_PRESETS` keys: `aprovado`, `alerta`, `erro`, and `info`.
- Use `animation.set` only after resolving canonical presets or aliases through the animation catalog.
- Use `tableIntegration.delegate` when the user asks for table-owned config, including columns, datasource, renderer placement, sorting, ordering, or table behavior.
- Require confirmation for destructive `rule.remove` and `effect.remove`.
- Preserve validators, affected paths, submission impact, preconditions, and failure modes when adding operations.
- Do not persist a local `ruleEffects.rules` tree as the canonical table config. Visual effect payloads must become `RuleEffectDefinition` or delegated table authoring operations.

## Validation Rules

The manifest validators are operational promises:

- rule identity and existence validators
- condition table-context validators
- effect registry and style safety validators
- preview-class-not-persisted validator
- preset and animation catalog validators
- table-owned-config-delegated validators
- destructive confirmation validators

When behavior changes, prove that the AI adapter snapshot, effect panel payload, delegated table operation, registry projection, and docs/examples agree.

## Inventory Before New Contract

Classify AI gaps before adding operations or schema fields:

- `ja-suportado-so-ux`: manifest, context pack, preset, validator, or example exists but the assistant cannot explain or surface it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: an AI patch shape should map to existing `RuleEffectDefinition`, preset, animation alias, or delegation operation.
- `suportado-parcialmente`: manifest can represent the decision but adapter, capability, context pack, table delegation, registry, docs, or tests need completion.
- `lacuna-real-de-contrato`: no manifest operation, target, validator, effect model, preset, or table delegation can safely carry the semantic decision.

For real gaps, update the canonical manifest and specs before adding host assistant behavior.

## Validation

Use the smallest reliable proof:

- `praxis-table-rule-builder-authoring-manifest.spec.ts`
- `table-rule-builder-ai.adapter.spec.ts`
- capability/context-pack specs when grounding changes
- `animation-presets.spec.ts`, `apply-effects.util.spec.ts`, and rule effects specs when operations affect runtime payloads
- table AI manifest or table editor specs when delegated operations change
- `npm run generate:registry:ingestion` or narrower registry validation when projection changes

Report exact positive and negative prompts validated, especially unknown effects, unknown animations, direct table config write attempts, and destructive removals.

## Companion Skills

- Use `praxis-table-rule-effects-runtime` for `RuleEffectDefinition`, registry-backed effects, labels, and preview conversion.
- Use `praxis-table-rule-animation-presets` for `animation.set`, aliases, overrides, and fail-closed animation resolution.
- Use `praxis-table-rule-table-integration` for table-owned placement and delegation to `@praxisui/table`.
- Use `praxis-table-ai-validation`, `praxis-ai-authoring-manifests`, and `praxis-ai-registry-ingestion` for shared table/AI registry governance.
