---
name: praxis-charts-ai-validation
description: Use when Codex must implement, audit, or consume @praxisui/charts AI authoring from the Angular manifest through registry ingestion and praxis-config-starter execution, including edit plans, target resolution, capability-backed validators, domain compilers, canonical chart patches, and editor/runtime round-trip.
---

# Praxis Charts AI Validation

Use this skill for executable AI chart authoring. `PRAXIS_CHARTS_AUTHORING_MANIFEST` is the Angular declaration of governed semantic edits to `PraxisXUiChartContract`; it is not proof by itself that an edit is published, executable, capability-safe, or consumed correctly.

Pair it with:

- `praxis-ai-authoring-manifests` for shared manifest and edit-plan invariants.
- `praxis-ai-registry-ingestion` for generated registry projections and snapshot synchronization.
- `praxis-ai-semantic-intent` for semantic intent routing and consult/edit boundaries.
- `praxis-config-ai-registry-manifests` for `praxis-config-starter` ingestion and executable manifest projection.
- `praxis-charts-ai-handler-contracts` for operation schemas, handlers, validators, effects, and edit plans.
- `praxis-charts-authoring-settings` for visual editor parity.
- `praxis-charts-authoring-catalogs` for governed resources, fields, targets, and previews.
- `praxis-charts-runtime-data` and `praxis-charts-analytics-interactions` for data, stats, query context, and interaction behavior.
- `praxis-charts-echarts-engine-boundary` when a request appears to require raw ECharts options.

## Canonical Execution Chain

Treat these as distinct proofs:

1. **Declaration**: the Angular manifest declares targets, operations, schemas, validators, effects, examples, and handler contracts.
2. **Publication**: registry tooling projects that exact manifest into `praxis-component-registry-ingestion.json`, and `praxis-config-starter` ingests or snapshots it without semantic drift.
3. **Execution**: the backend resolves targets, validates grounded input, compiles canonical effects, rejects unsupported semantics, and produces a document that the editor and runtime can read back unchanged.

The canonical flow is:

`semantic request -> component manifest -> componentEditPlan -> target resolver -> input schema -> validators -> effect compiler -> canonical chartDocument/queryContext patch -> editor/runtime round-trip`

Do not call a chart operation executable because its TypeScript object passes a structural spec. A declared validator without backend implementation, an unknown domain compiler, a missing required target resolver, or unavailable grounding must fail the edit plan. Warnings are not sufficient for required semantics.

AI must resolve intent semantically from governed context and declared tools. Keywords such as "ranking", "trend", "pie", or "KPI" may help rank candidates only after semantic scope is resolved. Never use raw ECharts patches, generic JSON Patch, metric aliases, regex command routing, or host-only command strings as the primary authoring mechanism.

## Required Source Inventory

Before changing or certifying Charts AI authoring, inspect all three ownership layers.

Angular declaration and consumers:

- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.ts`
- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts`
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- `projects/praxis-charts/src/lib/services/chart-contract-validation.service.ts`
- `projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.ts`
- `projects/praxis-charts/src/public-api.ts`

Registry publication:

- `tools/ai-registry/generate-registry-ingestion.ts`
- `tools/ai-registry/validate-authoring-contracts-acceptance.js`
- generated `dist/praxis-component-registry-ingestion.json`
- `praxis-config-starter/src/main/resources/ai-registry/registry-snapshot.json`

Backend execution:

- `AgenticAuthoringManifestContractValidator`
- `AgenticAuthoringManifestService`
- `AgenticAuthoringTargetResolverRegistry`
- `AgenticAuthoringValidatorRegistry`
- `AgenticAuthoringEffectCompilerRegistry`
- focused tests for each registry and manifest service

Read the applicable `AGENTS.md` files in Charts, `tools/ai-registry`, and `praxis-config-starter`. Use `praxis-angular-agents-governance` when Angular governance is missing or stale.

## Adherence Inventory

Before adding a target, operation, validator, DTO, or handler, ask what the platform already knows but is not materializing correctly. Classify each requested improvement:

- `ja-suportado-so-ux`: canonical state and execution exist; only presentation is missing.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the contract exists but a validator, patch, registry projection, or consumer overclaims or distorts it.
- `suportado-parcialmente`: declaration, publication, execution, or runtime parity is incomplete.
- `lacuna-real-de-contrato`: required semantic data has no canonical owner.

Only the last classification justifies a new contract. Prefer fixing the canonical manifest, registry projection, backend executor, or chart consumer over creating a UI-local concept.

## Manifest Invariants

The manifest identity is `praxis-chart`, owner `@praxisui/charts`, schema `PraxisXUiChartContract`. Runtime inputs and editable paths must match actual public inputs and canonical chart models.

For every operation verify:

- its target kind exists and resolves deterministically with `ambiguityPolicy: "fail"`;
- its input schema is specific enough for the semantic operation;
- every referenced validator is implemented by the backend or a declared canonical tool;
- `affectedPaths` overlap the compiled effects;
- destructive edits require confirmation;
- `compile-domain-patch` names an implemented compiler;
- the compiler writes only canonical chart fields;
- examples pass the same schemas and validators as real plans;
- publication preserves operation IDs, target kinds, validators, examples, and handler contracts exactly.

Do not invent manifest coverage from model breadth. Maintain an explicit matrix of `AI-editable`, `editor-only`, `preserved-only`, and `unsupported` paths for chart type, series, axes, source, query context, events, legend, tooltip, labels, theme, sizing, motion, and state.

## Grounding And Capabilities

Validation names must describe behavior actually enforced.

- `remote-resource-in-api-metadata` must resolve the requested resource against governed API metadata or a canonical resource catalog. Checking that a string begins with `/` is only path-shape validation.
- `stats-operation-supported` must verify the selected resource's published stats capability, not only membership in a global operation enum.
- `series-field-aggregable` must verify the selected field and metric against the resource's stats field capabilities.
- field validators must use the correct source catalog for each field role. An absent required catalog must fail closed or produce an explicit unresolved-target result; it must not silently pass.
- event targets must resolve against governed target descriptors and action-specific constraints, including target kind, port/schema, required capability, and mapping compatibility.
- authorization-sensitive metrics and resources must come from backend capability decisions. Labels, menu visibility, examples, and prior successful plans are not authorization evidence.

If the platform lacks the necessary resource, stats, field, or target tool, register that as a canonical contract gap. Do not replace it with keyword matching or permissive validation.

## Operation Semantics

Series identity is `chartDocument.metrics[].field`; preserve deterministic add/remove behavior and reject ambiguous duplicate identities. Axis edits must enforce chart-family compatibility, including cartesian versus pie/donut behavior and combo-only secondary axes.

Data binding must validate `source.kind`, resource, operation, dimensions, metrics, filters, and sorting against the same governed metadata and capabilities used at runtime. `queryContext` must remain structured and support the canonical context fields, including filter expression when the runtime contract supports it; do not hide a missing contract behind opaque URL fragments.

For cross-filter, drilldown, and selection:

- compile event actions to the canonical `PraxisXUiChartEventAction` shape;
- derive the event key/path from the operation rather than persisting operation-only fields into the event action;
- treat mapping as `{ sourceField: targetField }` consistently in schema, validation, compiler, editor, and runtime;
- validate source-field keys against chart output fields and target-field values against the governed target input contract;
- do not advertise authoring support before the runtime emits and consumes that interaction correctly.

Structured actions such as `filter-widget`, `open-detail`, `navigate`, `update-context`, or `emit` must remain governed. Never translate them into Angular switch statements driven by user wording.

## Fail-Closed Backend Parity

`AgenticAuthoringManifestContractValidator` proving internal references is necessary but insufficient. The executable gate must also prove that required resolvers, validator IDs, and domain compiler IDs are registered.

Reject the plan before apply when:

- an operation validator has no backend implementation;
- a required target resolver cannot resolve exactly one governed target;
- a `compile-domain-patch` handler is unknown;
- required metadata, capabilities, fields, resources, or target catalogs are absent;
- compiled operations write outside declared affected paths or canonical chart models;
- the resulting chart document fails Angular contract validation or editor/runtime round-trip.

A validator named `editor-runtime-round-trip` must execute a real proof or be renamed/narrowed to what it checks. A no-op validator is not evidence.

## Synchronization Triggers

Re-run the full chain when any of these change:

- `PraxisXUiChartContract`, data source, query context, event, sizing, theme, motion, state, or stats models;
- chart editor editable paths, runtime inputs/outputs, mapper behavior, or public exports;
- manifest targets, operations, validators, examples, effects, or handler contracts;
- registry generation, component metadata, snapshot ingestion, context packs, quick replies, diagnostics, previews, or apply payloads;
- dashboard chart documents or backend payload adapters.

Compare generated registry content with the Angular source and backend snapshot. Update derived assets in the same cycle when public semantics change. If no update is required, state why.

## Validation Matrix

Use the smallest sufficient local gates, but cover every changed layer.

Angular declaration and round-trip:

```bash
npx ng test praxis-charts --watch=false --progress=false \
  --include='projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts' \
  --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' \
  --include='projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.spec.ts' \
  --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts' \
  --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts'
npm run build:praxis-charts
```

Registry publication:

```bash
npm run generate:registry:ingestion
npm run validate:authoring-contracts
```

Backend execution, from `praxis-config-starter`:

```bash
mvn -Dtest=AgenticAuthoringManifestServiceTest,AgenticAuthoringManifestContractValidatorTest,AgenticAuthoringTargetResolverRegistryTest,AgenticAuthoringValidatorRegistryTest,AgenticAuthoringEffectCompilerRegistryTest test
```

Add negative tests for unknown validator/compiler/resolver, absent catalogs, unsupported resource capability, invalid field metric, reversed mapping, noncanonical event fields, and round-trip loss. Run assistant/edit-plan E2E or a focused harness when consult/edit/apply behavior changes.

Acceptance requires all applicable layers to pass. Report separately what was proven structurally, what was published, what executed, and what runtime/editor behavior was exercised. Never present a skipped backend or consumer gate as complete AI validation.
