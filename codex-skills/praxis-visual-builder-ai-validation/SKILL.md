---
name: praxis-visual-builder-ai-validation
description: Use when Codex must implement, audit, or consume @praxisui/visual-builder AI authoring surfaces: PRAXIS_VISUAL_BUILDER_AUTHORING_MANIFEST, VisualBuilderAiAdapter, VISUAL_BUILDER_AI_CATALOG, editable targets, node.add, node.remove, node.configure, edge.connect, edge.remove, variable.add, condition.set, effect.set, dsl.roundTrip.validate, validators, failure modes, context packs, or AI registry ingestion.
---

# Praxis Visual Builder AI Validation

Use this skill for governed AI authoring of visual-builder rules. AI operations must resolve semantic intent into declared manifest operations and validators; they must not patch arbitrary JSON or route primary intent through keywords.

Pair it with:

- `praxis-ai-authoring-manifests` for component manifest structure, operation contracts, targets, validators, and examples.
- `praxis-ai-registry-ingestion` when manifest changes must be discovered by the AI registry.
- `praxis-ai-semantic-intent` when user intent resolution, grounding, or tool selection is involved.
- `praxis-visual-builder-graph-runtime` for graph state, node identity, edges, validation errors, and registry integrity.
- `praxis-visual-builder-jsonlogic-roundtrip` for `condition.set`, JSON Logic parsing, and `dsl.roundTrip.validate`.
- `praxis-visual-builder-schemas-templates` for `variable.add`, `effect.set`, target schemas, field schemas, and context variables.

## Source Audit

Before editing visual-builder AI behavior, inspect:

- `projects/praxis-visual-builder/AGENTS.md`
- `projects/praxis-visual-builder/README.md`
- `projects/praxis-visual-builder/src/lib/ai/praxis-visual-builder-authoring-manifest.ts`
- `projects/praxis-visual-builder/src/lib/ai/visual-builder-ai.adapter.ts`
- `projects/praxis-visual-builder/src/lib/ai/visual-builder-ai-capabilities.ts`
- `projects/praxis-visual-builder/src/lib/ai/visual-builder-ai.context.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-builder.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-node-registry.service.ts`
- `projects/praxis-visual-builder/src/lib/services/context/context-management.service.ts`
- manifest, adapter, AI wizard, and AI integration specs

Also inspect core AI manifest/registry contracts if operation schema, validator shape, or ingestion behavior changes.

## Canonical AI Boundary

`PRAXIS_VISUAL_BUILDER_AUTHORING_MANIFEST` owns the agentic contract for:

- editable targets: `node`, `edge`, `variable`, `condition`, `effect`, and `dslDocument`;
- operations: `node.add`, `node.remove`, `node.configure`, `edge.connect`, `edge.remove`, `variable.add`, `condition.set`, `effect.set`, and `dsl.roundTrip.validate`;
- input schemas, identity keys, affected paths, preconditions, destructive flags, failure modes, validators, and examples;
- round-trip requirements for graph identity, JSON Logic, target property schemas, and child component ownership.

`VisualBuilderAiAdapter` owns guarded `RuleBuilderConfig` patch application for the component. It must not become a bypass around graph operations, registry integrity, JSON Logic validation, or target-property validation for persisted rules.

## AI Authoring Rules

- Resolve user intent semantically into manifest operations. Do not decide intent through keyword lists, regexes, or local aliases.
- Use matching, labels, field search, and fuzzy ranking only after the semantic operation scope and canonical target kind are known.
- Every AI operation needs stable identity keys: `nodeId`, source/target node IDs, variable scope/name, effect target type/targets, or round-trip format/compare mode.
- Destructive `node.remove` and `edge.remove` require explicit confirmation when semantics can be lost.
- `condition.set` must provide JSON Logic objects within the supported visual subset, not JavaScript strings.
- `effect.set` must validate `targetType`, target IDs, governed properties, and property value types through target property schemas and `RULE_PROPERTY_SCHEMA`.
- `variable.add` governs contextual/template flows; visual field-condition references to context variables remain unsupported until the canonical JSON Logic shape is defined.
- `dsl.roundTrip.validate` must prove export/import stability and reject semantic drift or unstable identity.

## Inventory Before New Contract

Classify AI gaps before adding manifest operations:

- `ja-suportado-so-ux`: the operation, validator, failure mode, or example exists but the assistant/wizard does not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: broad config patches or host-local labels are being used where manifest targets and operation IDs already exist.
- `suportado-parcialmente`: the manifest operation exists but handler wiring, validator coverage, adapter behavior, examples, or registry ingestion is incomplete.
- `lacuna-real-de-contrato`: no declared target, operation, input schema, validator, handler contract, or canonical runtime path can express the AI authoring decision.

Only a real gap justifies new AI operations or public authoring contracts. When adding one, define source of truth, affected paths, failure modes, examples, registry ingestion impact, docs/examples, and local validation.

## Validation

Use focused local gates:

- `praxis-visual-builder-authoring-manifest.spec.ts` for manifest shape, operations, validators, examples, and round-trip requirements;
- `visual-builder-ai.adapter.spec.ts` for patch application, snapshot/restore, and failure behavior;
- AI wizard/integration specs when user-facing AI authoring changes;
- graph, JSON Logic, schema/template skills for operation-specific runtime validation;
- `praxis-ai-registry-ingestion` checks when generated registry assets or catalog ingestion changes;
- `npm run build:praxis-visual-builder` when public AI exports change.

Final audit should state whether manifest validation, adapter behavior, operation runtime effects, registry ingestion, and JSON Logic round-trip were tested locally.
