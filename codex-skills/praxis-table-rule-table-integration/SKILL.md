---
name: praxis-table-rule-table-integration
description: Use when Codex must integrate `@praxisui/table-rule-builder` effects with `@praxisui/table`, including table config editor rule surfaces, `effects: RuleEffectDefinition[]`, singular-effect normalization, `rowConditionalRenderers`, `columns[].conditionalRenderers`, conditional style placement, renderer animation precedence, `tableIntegration.delegate`, Settings Panel round-trip, public API, docs, examples, or avoiding duplicated table-owned config writes.
---

# Praxis Table Rule Table Integration

Use this skill when table visual effects cross the boundary between `@praxisui/table-rule-builder` and `@praxisui/table`. The key decision is ownership: table-rule-builder owns visual effect payloads; table owns where and how those payloads attach to table config.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-table-rule-builder/AGENTS.md`
- `projects/praxis-table-rule-builder/README.md`
- `projects/praxis-table-rule-builder/src/lib/effects/README.md`
- `projects/praxis-table-rule-builder/src/lib/effects/models/rule-effects.model.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/apply-effects.util.ts`
- `projects/praxis-table-rule-builder/src/lib/ai/praxis-table-rule-builder-authoring-manifest.ts`
- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/rules-editor/**`
- `projects/praxis-table/src/lib/praxis-table-config-editor.*`
- `projects/praxis-table/src/lib/ai/praxis-table-authoring-manifest.ts`
- table renderer/config editor specs when placement or round-trip changes

## Canonical Boundary

`@praxisui/table-rule-builder` owns:

- `RuleEffectDefinition`
- effect editor/preset/animation semantics
- fail-closed effect conversion
- preview-only class exclusion
- AI operation contract for visual effects

`@praxisui/table` owns:

- `TableConfigV2`
- row and column renderer placement
- datasource and column identity
- rule conditions in table row/column context
- Settings Panel table editor round-trip
- table authoring manifest operations for table-owned config

Do not write table config directly from a rule-builder operation. Use explicit delegation such as `tableIntegration.delegate` or the table authoring manifest when the user asks for column, datasource, renderer placement, ordering, or table behavior.

## Integration Rules

- Persist embedded visual rule payloads as `effects: RuleEffectDefinition[]`.
- Normalize old singular `effects: RuleEffectDefinition` payloads on load/apply; do not keep a parallel singular contract.
- Attach effects only after resolving table context: row scope, column key, known fields, and supported condition operators.
- Preserve stable `ruleId`, `effectId`, and `presetKey`; array index is not identity.
- Keep `rowConditionalRenderers` and `columns[].conditionalRenderers` owned by table.
- Preserve documented animation precedence: `rule.animation > rule.renderer.animation`.
- Use `toCellClassAndStyle(effect, { includeAnimationPreview: false })` for persisted renderer style/class mapping.
- Do not let preview classes, panel labels, or transient editor state leak into table config.
- If table config editor, Settings Panel, or docs claim support, prove open/edit/apply/save/reopen/runtime reflection.

## Inventory Before New Contract

Classify requested integration changes:

- `ja-suportado-so-ux`: the table/editor/runtime already carries the effect but authoring or docs do not make it visible.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a local table rule shape should normalize to `effects: RuleEffectDefinition[]` or delegate to table.
- `suportado-parcialmente`: effect payload exists but round-trip, table placement, AI delegation, docs, or tests are incomplete.
- `lacuna-real-de-contrato`: neither table-rule-builder nor table exposes a canonical way to carry the placement/effect decision.

Only real gaps justify changing public table or rule-builder contracts. Decide owner before editing.

## Validation

Use the smallest reliable proof:

- table-rule-builder `apply-effects.util.spec.ts` and rule effects specs for payload projection
- table `rules-editor` specs for config editor integration
- table config editor/Settings Panel specs for apply/save/reset/reopen
- table runtime renderer specs for row/column materialization and animation precedence
- AI manifest specs for delegated table operations
- docs/playground validation when examples or public guides change

Report which owner was validated: rule-builder effect payload, table placement, or both.

## Companion Skills

- Use `praxis-table-rule-effects-runtime` for effect payload semantics.
- Use `praxis-table-rule-animation-presets` for animation preset/alias/precedence concerns.
- Use `praxis-table-rule-ai-validation` for manifest operations and delegated authoring behavior.
- Use `praxis-table-authoring-settings`, `praxis-table-runtime-data`, and `praxis-table-ai-validation` for table-owned config, runtime, and AI contracts.
