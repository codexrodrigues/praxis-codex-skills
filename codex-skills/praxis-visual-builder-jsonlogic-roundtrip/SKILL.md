---
name: praxis-visual-builder-jsonlogic-roundtrip
description: Use when Codex must implement, audit, or consume @praxisui/visual-builder JSON Logic authoring: RuleBuilderService import/export, currentJSON, loadFromConditionExpression, buildConditionExpressionFromGraph, JSON/form-config payloads, FormLayoutRule bridge, field-to-field conditions, unsupported context/function operands, legacy expression safeguards, dsl.roundTrip.validate, or visual/textual round-trip stability.
---

# Praxis Visual Builder JSON Logic Round Trip

Use this skill for JSON Logic conditions and import/export stability in `@praxisui/visual-builder`. JSON Logic is the canonical persisted condition contract for new authoring; JavaScript expressions and legacy textual DSL are not baseline payloads.

Pair it with:

- `praxis-visual-builder-graph-runtime` for `RuleBuilderState`, node identity, graph edges, validation errors, and registry integrity.
- `praxis-visual-builder-schemas-templates` for field schemas, target property schemas, template-compatible rules, and context variables.
- `praxis-visual-builder-ai-validation` for manifest operation `condition.set`, `effect.set`, and `dsl.roundTrip.validate`.
- `praxis-form-ai-rules-validation` when exported form rules materialize in dynamic-form behavior.
- `praxis-core-runtime-contracts` when shared `JsonLogicExpression`, `JsonLogicValue`, `FormLayoutRule`, or `RULE_PROPERTY_SCHEMA` contracts change.

## Source Audit

Before editing round-trip behavior, inspect:

- `projects/praxis-visual-builder/AGENTS.md`
- `projects/praxis-visual-builder/README.md`
- `projects/praxis-visual-builder/src/public-api.ts`
- `projects/praxis-visual-builder/src/lib/models/rule-builder.model.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-builder.service.ts`
- `projects/praxis-visual-builder/src/lib/ai/praxis-visual-builder-authoring-manifest.ts`
- round-trip specs and rule-builder service specs

Inspect `@praxisui/core` contracts when a change touches `JsonLogicExpression`, `FormLayoutRule`, target property schema, or property sanitization.

## Canonical Boundary

`RuleBuilderService` owns the supported conversions:

- builder-state import from `{ nodes, rootNodes }` or nested `builderState`;
- form-rule import from `FormLayoutRule[]` or `{ formRules }`;
- JSON export as `{ formRules, builderState }`;
- `currentJSON` projection from the visual graph;
- condition-only import through `loadFromConditionExpression(...)`;
- condition export through `buildConditionExpressionFromGraph(...)`;
- validation of graph structure and supported node configs before persistence.

The exported `ExportOptions` advertises `json`, `typescript`, and `form-config`, but the current service only implements JSON export. Do not document or rely on TypeScript/form-config export as finished runtime behavior unless code and tests are completed in the same change.

## JSON Logic Rules

- Persist conditions as JSON Logic objects or `null`, not JavaScript strings.
- Treat `RuleNodeType.EXPRESSION` and `ExpressionConfig.expression` as legacy textual expression support, not the preferred contract for new authoring.
- Field conditions can serialize literal comparisons and field-to-field comparisons when they map to supported JSON Logic operators.
- `valueType: "context"` and `valueType: "function"` currently produce validation errors because they do not yet have canonical JSON Logic serialization in the visual builder.
- Boolean groups must preserve supported operator semantics and child order where order affects meaning.
- `propertyRule` conditions can use inline JSON Logic or `conditionNodeId`, but both must validate against graph state and export deterministically.
- `buildConditionExpressionFromGraph(...)` and import paths must be treated as a semantic round trip, not as string formatting.

## Inventory Before New Contract

Classify requested additions:

- `ja-suportado-so-ux`: JSON Logic exists but the editor, preview, error message, or validation result is not visible enough.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host calls the contract “DSL”, “expression”, or “script” while the actual supported payload is JSON Logic.
- `suportado-parcialmente`: the model exposes a node or value type, but parse/export/validation/docs do not fully support it yet.
- `lacuna-real-de-contrato`: no supported JSON Logic representation, parser branch, validation rule, core type, or form-rule materialization can express the condition.

Only a real contract gap justifies adding operators, operands, or exported types. If context variables or custom functions are needed as condition operands, define the canonical JSON Logic shape and consumers before authoring local UI behavior.

## Validation

Use focused local gates:

- `rule-builder.service.spec.ts` for import/export and validation behavior;
- round-trip specs for JSON Logic condition graphs;
- `field-condition-editor.component.spec.ts` when editor controls or operator support changes;
- property-effect specs when conditions are attached to effects;
- AI manifest specs when `dsl.roundTrip.validate`, `condition.set`, or failure modes change;
- `npm run build:praxis-visual-builder` for public model or export changes.

Every completed issue should state whether JSON export, import back, graph validation, semantic drift detection, and dynamic-form/form-rule materialization were actually tested.
