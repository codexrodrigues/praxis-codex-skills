---
name: praxis-table-rule-effects-runtime
description: Use when Codex must implement, audit, document, or consume `@praxisui/table-rule-builder` visual effect runtime surfaces, including `RuleEffectsPanelComponent`, `RuleEffectDefinition`, `RuleScope`, effect editor tabs, `EffectRegistryService`, `DEFAULT_EFFECT_PRESETS`, `toCellClassAndStyle`, preview classes, labels/i18n overrides, component metadata, public API, docs, examples, or conditional table visual effects.
---

# Praxis Table Rule Effects Runtime

Use this skill for the canonical conditional visual effect editor in `@praxisui/table-rule-builder`. Treat it as the table-facing visual effects authoring surface, not as a generic CSS editor or business rules engine.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-table-rule-builder/AGENTS.md`
- `projects/praxis-table-rule-builder/README.md`
- `projects/praxis-table-rule-builder/src/public-api.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/README.md`
- `projects/praxis-table-rule-builder/src/lib/effects/rule-effects-panel.component.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/models/rule-effects.model.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/services/effect-registry.service.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/apply-effects.util.ts`
- `projects/praxis-table-rule-builder/src/lib/praxis-table-rule-builder.metadata.ts`
- focused effect panel, apply-effects, metadata, i18n, and docs manifest specs

## Canonical Boundary

`@praxisui/table-rule-builder` owns:

- `RuleEffectsPanelComponent`
- `RuleEffectDefinition`
- `RuleScope`
- effect editor categories: `estilo`, `layout`, `icone`, `fundo`, `animacao`, and `tooltip`
- `EffectRegistryService` plugin ordering and category availability
- default effect presets
- conversion to class/style through `toCellClassAndStyle(...)`
- panel i18n namespace and host `labels` overrides

`@praxisui/table` owns table config placement, columns, datasource, `rowConditionalRenderers`, `columns[].conditionalRenderers`, and renderer precedence. `@praxisui/visual-builder` owns general JSON Logic visual rule authoring. Do not move table visual effect semantics into table CSS hacks, host-local classes, or a parallel visual-builder DSL.

## Runtime Rules

- Use `RuleEffectsPanelComponent` for authoring one aggregate `RuleEffectDefinition`.
- Persist table embedded rules as `effects: RuleEffectDefinition[]` when the table rule surface expects the canonical array.
- Accept singular legacy `effects: RuleEffectDefinition` only as import compatibility and normalize to the canonical array on apply.
- Use `scope: cell | row | column | table` to describe where the effect applies. Do not infer scope from labels or CSS selectors.
- Use `EffectRegistryService.register(...)` for new editor categories; do not bypass the registry with hardcoded host panels.
- Keep preview classes out of persisted payloads. For persisted table mapping, use `toCellClassAndStyle(effect, { includeAnimationPreview: false })`.
- Treat `cssClass` and `inlineStyle` as advanced escape hatches that still need safety review.
- Keep panel chrome text in the package i18n catalog. Use `labels` only for host-specific overrides and never persist labels as rule semantics.

## Inventory Before New Contract

Classify requested changes before adding fields:

- `ja-suportado-so-ux`: the effect, preview, labels, tabs, or preset exists but is not surfaced clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: consumers use CSS classes, singular effects, or local aliases where `RuleEffectDefinition` or the registry already carries the semantics.
- `suportado-parcialmente`: table placement, visual-builder condition editing, docs, or AI registry projection needs completion around an existing effect model.
- `lacuna-real-de-contrato`: no current effect model, registry category, preset, conversion util, metadata, or table delegation path can represent the visual decision.

Only real contract gaps justify public API changes. Name the canonical owner, affected consumers, docs/examples, AI manifest impact, and minimum validation before editing.

## Validation

Use the smallest reliable proof:

- `rule-effects-panel.component.spec.ts`
- `apply-effects.util.spec.ts`
- `praxis-table-rule-builder.metadata` specs when component discovery changes
- i18n catalog checks when labels or panel chrome change
- `ng build praxis-table-rule-builder` when public API or package exports change
- table focused validation when effects materialize in row or column renderers

Report exactly what remained unvalidated, especially visual preview, persisted payload, and table runtime integration.

## Companion Skills

- Use `praxis-table-rule-animation-presets` for semantic animations, aliases, reduced-motion, and fail-closed animation resolution.
- Use `praxis-table-rule-table-integration` when effects are embedded into `@praxisui/table` rules, renderers, config editors, or Settings Panel.
- Use `praxis-table-rule-ai-validation` for AI authoring manifest operations, validators, examples, and registry ingestion.
- Use `praxis-visual-builder-rules` for general JSON Logic rule editing and visual/textual round-trip outside table visual effect payloads.
