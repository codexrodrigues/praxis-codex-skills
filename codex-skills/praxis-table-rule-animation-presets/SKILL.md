---
name: praxis-table-rule-animation-presets
description: Use when Codex must implement, audit, document, or validate semantic animations in `@praxisui/table-rule-builder`, including `RuleAnimationPreset`, `RULE_ANIMATION_PRESETS`, `RULE_ANIMATION_PRESET_ALIASES`, `resolveRuleAnimationPresetKey`, `resolveRuleAnimationConfig`, animation override normalization, reduced-motion behavior, preview-only animation classes, runtime precedence, docs, public API, or table rule animation validation.
---

# Praxis Table Rule Animation Presets

Use this skill for semantic table rule animations. Treat animations as governed visual feedback attached to table rule effects, not as arbitrary CSS animation names.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-table-rule-builder/AGENTS.md`
- `projects/praxis-table-rule-builder/README.md`
- `projects/praxis-table-rule-builder/src/lib/effects/README.md`
- `projects/praxis-table-rule-builder/src/lib/effects/animation-presets.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/animation-presets.spec.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/apply-effects.util.ts`
- `projects/praxis-table-rule-builder/src/lib/effects/rule-effects-panel.component.ts`
- `projects/praxis-table-rule-builder/src/lib/ai/praxis-table-rule-builder-authoring-manifest.ts`
- table runtime specs when row/column renderer animation precedence changes

## Canonical Boundary

`animation-presets.ts` owns canonical semantic animation presets, aliases, supported animation types, triggers, repeats, intensities, and normalization. `toCellClassAndStyle(...)` owns preview class/style projection for effects. `@praxisui/table` owns where row/column renderer animations are applied and the documented precedence `rule.animation > rule.renderer.animation`.

Do not persist preview-only classes or raw animation CSS as the canonical schedule. Do not let host CSS invent new semantic animation names without updating the preset catalog and validation.

## Animation Rules

- Use canonical presets: `info-soft`, `success-confirm`, `warning-attention`, `critical-alert`, `audit-review`, and `sync-pending`.
- Use aliases only as governed compatibility or domain-friendly mapping: `sla-warning`, `sla-breach`, `risk-elevated`, `risk-critical`, `audit-warning`, and `sync-warning`.
- Resolve aliases through `resolveRuleAnimationPresetKey` and `resolveRuleAnimationPreset`.
- Normalize animation payloads with `resolveRuleAnimationConfig`.
- Empty overrides must not erase preset defaults. Preserve fail-closed behavior for blank `type`, `repeat`, `trigger`, `intensity`, or duration values.
- Unsupported animation types must resolve to no animation instead of leaking unknown classes.
- Respect reduced-motion behavior in preview. Do not force motion when the runtime suppresses animation classes.
- Keep runtime precedence aligned with table: `rule.animation` overrides `rule.renderer.animation`, and first-match applies only when there is a real effect.

## Inventory Before New Contract

Classify changes before adding animation vocabulary:

- `ja-suportado-so-ux`: existing preset/alias exists but the editor, docs, or preview does not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host/domain names should map to existing aliases or canonical presets.
- `suportado-parcialmente`: runtime can resolve the animation but table renderer, docs, AI manifest, or tests do not prove it.
- `lacuna-real-de-contrato`: no existing preset, alias, type, trigger, repeat, intensity, or table runtime path can represent the semantic motion safely.

For real gaps, update preset catalog, AI manifest enum, specs, docs, and table integration evidence in the same cycle.

## Validation

Use the smallest reliable proof:

- `animation-presets.spec.ts`
- `apply-effects.util.spec.ts` for preview class/style projection
- `rule-effects-panel.component.spec.ts` for clean emitted animation payloads
- table renderer specs when precedence or runtime application changes
- AI manifest specs when animation operation enums or validators change
- visual/browser validation when motion, reduced-motion, or preview behavior is user-facing

Report whether preview classes were checked separately from persisted payload mapping.

## Companion Skills

- Use `praxis-table-rule-effects-runtime` for the surrounding effect panel and `RuleEffectDefinition`.
- Use `praxis-table-rule-table-integration` when animation reaches row/column conditional renderers.
- Use `praxis-table-rule-ai-validation` when AI applies `animation.set` or validates preset/alias choices.
- Use `praxis-angular-i18n-governance` when animation names or panel chrome text change.
