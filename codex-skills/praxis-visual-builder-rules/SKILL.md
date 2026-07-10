---
name: praxis-visual-builder-rules
description: Use when Codex must inspect, change, or scaffold @praxisui/visual-builder rule authoring: JSON Logic visual round-trip, RuleBuilderState, RuleNode, RuleBuilderService, RuleNodeRegistryService, field schemas, context variables, property effects, collection validators, rule templates, validation errors, visual/textual conversion, PRAXIS_VISUAL_BUILDER_AUTHORING_MANIFEST, VisualBuilderAiAdapter, or legacy mini-DSL migration.
---

# Praxis Visual Builder Rules

Use this skill for visual rule and expression authoring in `@praxisui/visual-builder`. JSON Logic is the canonical contract for new authoring, persistence, and runtime integration. The legacy mini-DSL is migration reference material only.

Pair it with:

- `praxis-visual-builder-graph-runtime` when the task touches `RuleBuilderState`, `RuleNode`, graph identity, `rootNodes`, `children`, registry integrity, selection, undo/redo, orphan/cycle validation, or visual editor state.
- `praxis-visual-builder-jsonlogic-roundtrip` when the task touches JSON Logic import/export, `currentJSON`, condition parsing, `FormLayoutRule` bridge, unsupported context/function operands, legacy expression safeguards, or round-trip stability.
- `praxis-visual-builder-schemas-templates` when the task touches field schemas, target schemas, property schemas, `FieldSchemaService`, context variables, collection validators, or reusable templates.
- `praxis-visual-builder-ai-validation` when the task touches `PRAXIS_VISUAL_BUILDER_AUTHORING_MANIFEST`, `VisualBuilderAiAdapter`, capabilities, editable targets, operation validators, examples, or AI registry ingestion.
- `praxis-core-runtime-contracts` when shared JSON Logic, form-rule, metadata, or public model contracts change.
- `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion` when the visual builder AI manifest or generated assets change.
- `praxis-authoring-editors` when the visual builder is hosted as a config editor in another component.
- `praxis-page-builder-authoring` and `praxis-page-builder-ai-agentic` when Visual Builder is hosted inside Page Builder widget config or page agentic flows.
- `praxis-form-ai-rules-validation` when form rules, field visibility, submit behavior, or dynamic-form rule materialization are involved.
- `praxis-table-rule-effects-runtime`, `praxis-table-rule-table-integration`, and `praxis-table-rule-ai-validation` when the rule expression is specifically table visual conditional effects owned by `@praxisui/table-rule-builder`.

## Canonical Boundary

`@praxisui/visual-builder` owns:

- `RuleBuilderState`, `RuleNode`, rule graph identity, registry integrity, undo/redo, validation state, and export/import requests;
- JSON Logic condition editing and visual/textual round-trip;
- field schemas, target schemas, context variables, custom functions, property effects, and collection validators;
- typed `VisualBuilderError` categories for validation, conversion, registry, expression, context, configuration, network, and internal failures;
- visual-builder AI manifest and adapter for governed authoring.

Consumers should not create local parsers, local mini-DSLs, or duplicate rule graph models. If a consumer needs a rule editor, it should host the visual builder or a component-owned editor that delegates to this contract.

This skill is the umbrella entrypoint. For implementation work, load the narrow companion skill that owns the active subdomain before editing so the audit can distinguish existing support from a real contract gap.

## Required Source Inventory

Before editing Visual Builder rules, inspect:

- `projects/praxis-visual-builder/AGENTS.md`
- `projects/praxis-visual-builder/src/public-api.ts`
- `projects/praxis-visual-builder/src/lib/praxis-visual-builder.ts`
- `projects/praxis-visual-builder/src/lib/praxis-visual-builder.metadata.ts`
- `projects/praxis-visual-builder/src/lib/models/rule-builder.model.ts`
- `projects/praxis-visual-builder/src/lib/models/field-schema.model.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-builder.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-node-registry.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-validation.service.ts`
- `projects/praxis-visual-builder/src/lib/services/field-schema.service.ts`
- `projects/praxis-visual-builder/src/lib/errors/visual-builder-errors.ts`
- `projects/praxis-visual-builder/src/lib/ai/praxis-visual-builder-authoring-manifest.ts`
- `projects/praxis-visual-builder/src/lib/ai/visual-builder-ai.adapter.ts`
- `projects/praxis-visual-builder/MINI-DSL-GUIDE.md` only for legacy migration context

Also inspect `README.md`, `src/lib/docs/collection-validators.md`, and `src/lib/docs/TEMPLATE-SYSTEM-GUIDE.md` when language, templates, validators, or public behavior changes.

## Rule And DSL Rules

Use JSON Logic for new persisted conditions and runtime expressions. Do not introduce new mini-DSL syntax, operators, or parsers for new configs. If legacy mini-DSL payloads must be supported, classify the work as migration compatibility and document the removal path.

Keep node identity stable:

- `RuleNode.id` is the identity key;
- `children` must remain string IDs, not embedded node objects;
- registry integrity must reject missing nodes, cycles where invalid, malformed child references, and orphaned edges;
- destructive node removal requires confirmation when conditions or effects can be lost.

For property effects, preserve canonical target semantics: `field`, `section`, `action`, `row`, `column`, or `visualBlock`. Do not encode target selection through labels, CSS selectors, or host-only aliases.

For field schemas and context variables, use governed `FieldSchema`, `FieldSchemaContext`, `ContextVariable`, and custom function metadata. Text search can rank fields after scope is known, but it must not decide primary authoring intent.

## AI Manifest Rules

The visual builder manifest should preserve editable targets for node, edge, variable, condition, effect, and DSL document. Operations should use deterministic handler contracts for node add/remove/configure, edge connect/remove, variable add, condition set, effect set, and DSL round-trip validation.

Every operation must validate graph integrity and JSON Logic round-trip where relevant. Broad config patches are incomplete unless they identify stable node/edge/field targets and failure modes.

`VisualBuilderAiAdapter` may apply governed `RuleBuilderConfig` patches, but it must not bypass the rule graph, registry integrity, or JSON Logic conversion checks for persisted rules.

When Visual Builder is embedded in Page Builder, Dynamic Form, Table, or another component editor, keep Visual Builder as the owner of graph/JSON Logic semantics and the host as owner of placement, persistence, and child editor lifecycle. Do not serialize host-specific labels, widget keys, or CSS selectors into rule conditions unless the canonical target schema defines them.

## Validation

Use focused local gates:

- visual rule editing: `rule-editor.component.spec.ts`, `rule-canvas.component.spec.ts`, `rule-definition.component.spec.ts`, and `rule-list.component.spec.ts`.
- field/property editors: `field-condition-editor.component.spec.ts`, `property-effect-editor.component.spec.ts`, and metadata editor specs.
- services: `rule-builder.service.spec.ts`, `rule-validation.service` coverage, `rule-node-registry` coverage, and field schema service coverage.
- AI: `praxis-visual-builder-authoring-manifest.spec.ts`, `visual-builder-ai.adapter.spec.ts`, and AI integration specs.
- round-trip: any `round-trip-*.spec.ts` or validator round-trip specs present in the workspace; add focused round-trip coverage if a conversion path changes.
- host integration: dynamic-form, table, page-builder, or manual-form focused specs only when the rule materialization path for that host changed.
- build: `npm run build:praxis-visual-builder` when public API, models, templates, or language behavior changes.

When validation is partial, state which visual, JSON Logic, service, AI, and build gates remain unexecuted.
