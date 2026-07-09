---
name: praxis-visual-builder-graph-runtime
description: Use when Codex must implement, audit, or consume @praxisui/visual-builder graph runtime state: RuleBuilderState, RuleNode, RuleNodeType, RuleBuilderService node add/update/remove/select, undo/redo snapshots, rootNodes, children edge IDs, RuleNodeRegistryService, RuleValidationService, graph integrity, cycles, orphaned nodes, validationErrors, or visual rule editor state.
---

# Praxis Visual Builder Graph Runtime

Use this skill for the canonical visual rule graph in `@praxisui/visual-builder`. Treat `RuleBuilderState` as the visual source of truth for authoring sessions; JSON Logic and form-rule payloads are projections that must be validated against this graph.

Pair it with:

- `praxis-visual-builder-jsonlogic-roundtrip` when import/export, `currentJSON`, JSON Logic parsing, or `dsl.roundTrip.validate` is involved.
- `praxis-visual-builder-schemas-templates` when node configs depend on field schemas, target schemas, property schemas, collection validators, context variables, or templates.
- `praxis-visual-builder-ai-validation` when an AI manifest operation edits nodes, edges, variables, conditions, effects, or validates round-trip.
- `praxis-core-runtime-contracts` when shared `JsonLogicExpression`, `FormLayoutRule`, `RULE_PROPERTY_SCHEMA`, or exported public model contracts change.

## Source Audit

Before editing graph runtime behavior, inspect:

- `projects/praxis-visual-builder/AGENTS.md`
- `projects/praxis-visual-builder/README.md`
- `projects/praxis-visual-builder/src/public-api.ts`
- `projects/praxis-visual-builder/src/lib/models/rule-builder.model.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-builder.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-node-registry.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-validation.service.ts`
- focused specs for rule editor, rule canvas, rule definition, rule list, rule builder service, registry, and validation service

Also inspect component hosts such as `rule-editor.component.ts`, `rule-canvas.component.ts`, `rule-node.component.ts`, and `visual-rule-builder.component.ts` when UI events or selection state change.

## Canonical Boundary

`@praxisui/visual-builder` owns:

- `RuleBuilderState.nodes` and `RuleBuilderState.rootNodes`;
- `RuleNode.id` as stable node identity;
- `RuleNode.children` as string node IDs only;
- `RuleNode.parentId` for graph hierarchy;
- selection, dirty state, validation errors, and history snapshots;
- `RuleBuilderService` state transitions for add, update, remove, select, clear, undo, redo, import, export, and validation;
- `RuleNodeRegistryService` node resolution, child resolution, orphan cleanup, cycle detection, and integrity checks;
- `RuleValidationService` tree validation for structure, dependency, business logic, performance, and custom rules.

Consumers must not embed child node objects in `children`, derive node identity from labels, or keep a parallel local graph model. If a host needs visual rule authoring, it should host the visual builder or delegate to this graph contract.

## Inventory Before New Contract

Before adding fields or services, classify the need:

- `ja-suportado-so-ux`: selection, validation errors, root nodes, history, or registry state exists but the editor does not surface it clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host uses labels, array indexes, embedded child objects, or local aliases where `RuleNode.id`, `rootNodes`, `children`, or `parentId` already carry the identity.
- `suportado-parcialmente`: the graph can represent the decision, but a specific node type lacks complete validation, UI editing, or JSON Logic round-trip.
- `lacuna-real-de-contrato`: no current node model, graph relation, registry check, validation error, or projection path can represent the visual decision.

Only a real contract gap justifies public model changes. Name the canonical owner, impacted consumers, docs/examples, AI manifest impact, derived artifacts, and minimum validation before editing.

## Graph Rules

- Preserve `RuleNode.id` during updates. `RuleBuilderService.updateNode(...)` must not allow identity mutation.
- Keep `children` as string IDs. `RuleNodeRegistryService.resolveChildren(...)` intentionally fails on embedded objects because that state violates the graph model.
- Keep `rootNodes` limited to top-level rules. A node should not be both root and referenced as a child unless the graph semantics explicitly allow it and validation is updated.
- Reject missing roots, missing children, cycles, and invalid parent references through service-level validation.
- Treat orphan warnings as authoring diagnostics, not as permission to persist disconnected semantics.
- Use `saveSnapshot(...)`-driven history for undo/redo rather than ad hoc local copies in hosts.
- Keep destructive node or edge operations explicit when conditions, effects, or descendants can be lost.

## Validation

Use the smallest reliable proof:

- graph service changes: `rule-builder.service.spec.ts`, registry specs, and validation service specs;
- editor state changes: `rule-editor.component.spec.ts`, `rule-canvas.component.spec.ts`, `rule-node.component.spec.ts`, and `rule-list.component.spec.ts`;
- graph serialization side effects: add `praxis-visual-builder-jsonlogic-roundtrip` validation;
- public API or model changes: `npm run build:praxis-visual-builder` plus one focused consumer when exported contracts are touched.

Report exactly which graph, UI, registry, round-trip, and build gates were executed or skipped.
