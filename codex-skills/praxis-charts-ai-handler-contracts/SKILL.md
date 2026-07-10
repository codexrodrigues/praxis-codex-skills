---
name: praxis-charts-ai-handler-contracts
description: Use when Codex must implement, audit, or consume executable @praxisui/charts authoring operations across PRAXIS_CHARTS_AUTHORING_MANIFEST, target resolution, validators, compile-domain-patch handlers, compiled patch evidence, canonical chartDocument/queryContext/event writes, registry projection, and editor/runtime round-trip.
---

# Praxis Charts AI Handler Contracts

Use this skill for the operation-to-patch boundary of executable Chart authoring. It governs how a semantically resolved Chart decision becomes a deterministic canonical configuration change; it does not authorize raw chart JSON, ECharts options, JSON Patch, or keyword-routed host commands.

Use `praxis-charts-ai-validation` for the broader declaration, publication, grounding, and end-to-end validation chain. This skill is narrower: it makes each handler's reads, identity, writes, compiled evidence, failure behavior, and consumer round-trip explicit.

Pair it with:

- `praxis-ai-authoring-manifests` for shared operation/effect invariants.
- `praxis-config-ai-registry-manifests` when backend manifest projection, executable registries, or compile/apply semantics are involved.
- `praxis-ai-registry-ingestion` for generated Angular registry assets and snapshot comparison.
- `praxis-charts-authoring-catalogs` for governed resource, field, and target descriptors.
- `praxis-charts-analytics-interactions` for stats, query context, cross-filter, drilldown, and selection runtime behavior.
- `praxis-charts-authoring-settings` and `praxis-charts-runtime-data` when a compiled path is consumed by the editor or runtime.
- `praxis-charts-echarts-engine-boundary` when a request attempts to cross the renderer-neutral boundary.

## Canonical Boundary

The canonical execution sequence is:

`semantic decision -> manifest operation -> target resolution -> input schema and grounded validators -> effect/handler -> compiled operation evidence -> proposed canonical config -> editor/runtime read-back`

Ownership is intentional:

- `@praxisui/charts` owns `PraxisXUiChartContract`, the Chart manifest, editor paths, runtime model, and public component surface.
- `praxis-config-starter` owns executable manifest projection, target resolvers, validator registry, domain compiler registry, diagnostics, and compile/apply policy.
- metadata/resource capability owners provide resource, field, stats, action, and target authority; a handler consumes those decisions and does not recreate them locally.
- the AI registry projects the manifest. Generated `dist/` files and backend snapshots are derived evidence, never the source to patch by hand.

Do not decide intent from words such as "trend" or "ranking". Semantic resolution selects the operation first; aliases or fuzzy matching may only rank candidates within that governed operation.

## Required Source Inventory

Inspect the Angular declaration and consumers:

- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.ts`
- `projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts`
- `projects/praxis-charts/src/lib/models/x-ui-chart.model.ts`
- `projects/praxis-charts/src/lib/services/chart-contract-validation.service.ts`
- `projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.ts`
- `projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.ts`
- `projects/praxis-charts/src/lib/praxis-chart.metadata.ts`

Inspect the executable backend, not only the manifest:

- `AgenticAuthoringManifestService`
- `AgenticAuthoringTargetResolverRegistry`
- `AgenticAuthoringValidatorRegistry`
- `AgenticAuthoringEffectCompilerRegistry`
- their focused tests and `registry-snapshot.json`

Read `projects/praxis-charts/AGENTS.md`, `tools/ai-registry/AGENTS.md`, and `praxis-config-starter/AGENTS.md` before code changes. Use `praxis-angular-agents-governance` if local Angular governance is absent or stale.

## Inventory Before A New Operation

Ask first what already exists but is inadequately materialized:

- `ja-suportado-so-ux`: an operation and handler work, but assistant UI, preview, examples, or diagnostics do not expose them well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a manifest operation already expresses the decision, but its handler, compiled evidence, or consumer path is misleading.
- `suportado-parcialmente`: the operation exists but lacks an executable resolver, grounded validator, compiler, exact registry projection, or editor/runtime parity.
- `lacuna-real-de-contrato`: no canonical target, operation, handler, or consumer path can represent the decision.

Only the last classification justifies a new operation or type. Do not add a frontend-only handler or an alternate chart dialect to cover an executor, metadata, or runtime gap.

## Operation And Effect Selection

Use a built-in manifest effect only when it is a lossless, path-local canonical transformation:

- `set-value` for a whole canonical value such as `chartDocument`, `queryContext`, `legend`, or `tooltip`.
- `merge-object` only when every accepted input key belongs to the exact target object and no domain rule, identity, or capability decision is hidden in the merge.
- `remove-by-key` only with the canonical collection identity and confirmation for destructive removal.

Use `compile-domain-patch` when an operation has semantic identity, placement, multiple writes, cross-field constraints, catalog/capability grounding, or a specialized audit operation. A `handlerContract` is executable metadata, not prose: it must declare accurate `reads`, `writes`, stable `identityKeys`, input schema, failure modes, and a semantic description.

Every domain handler must be registered by the backend before a plan is accepted. Unknown handlers, unimplemented validators, unresolved required targets, and absent required grounding must fail closed with structured diagnostics; a warning cannot certify an executable edit.

## Compiled Operation Invariants

For each `compile-domain-patch`, prove all of the following:

- The compiler receives the resolved target, plan input, and isolated proposed configuration; it never mutates the user's persisted config directly.
- The compiled record identifies `componentId`, `operationId`, `effectKind`, `domainHandler`, semantic `op`, `target`, `input`, `affectedPaths`, and `submissionImpact`; include resolved target evidence when resolution occurred.
- `path` and `value` describe the same canonical subtree. If an operation changes multiple paths, emit path-accurate deltas or explicitly emit a root-document operation whose value is the root document. Never label a nested path while supplying an unrelated larger document.
- The compiler's actual writes are covered by both `handlerContract.writes` and operation `affectedPaths`; no silent mutation may escape audit, authorization, preview, or apply.
- Collection operations expose stable canonical identity, such as `chartDocument.metrics[].field`, plus insertion/removal/reorder facts when relevant.
- Failure leaves no applicable compiled patch. A failed multi-write operation must not be exposed as a partial success.
- The proposed result preserves `PraxisXUiChartContract` and can be read by the editor and runtime without loss, raw engine options, or operation-only fields.

Treat a `handlerContract` whose reads/writes or failure modes do not match the compiler as `ja-suportado-mal-nomeado-ou-mal-materializado`. Correct the canonical manifest or executor; do not document the mismatch away.

## Chart Operation Contracts

`chart.document.set` may set the complete `PraxisXUiChartContract` only after version, kind, source, and chart-family validation. It must never accept an ECharts-shaped document.

`chart.type.set` may use a path-local merge only for canonical `kind` and orientation fields. It must still preserve pie/donut, cartesian, combo, metric, and dimension constraints. If a type change requires structural migration, promote it to a domain handler.

`series.add` uses `metrics[].field` as its only stable identity. The handler must validate the governed field and aggregation, reject duplicates, preserve requested placement through a known `afterField`, and report the inserted index and canonical metric value.

`series.remove` must resolve the selected series deterministically, require confirmation, preserve any required minimum metric invariant, and ensure target identity and input field cannot disagree silently.

`axis.configure` must declare exactly whether it changes orientation, `dimensions[].role`, and/or `metrics[].axis`. It may add a canonical dimension by field but must not invent a metric. Combo-only secondary axes and chart-family dimension requirements are handler preconditions, not editor conventions.

`data.resource.bind` is a multi-write semantic operation. Its handler must ground resource, stats operation, dimensions, and metrics in canonical metadata/capabilities, then emit path-accurate evidence for `source`, `dimensions`, and `metrics` or an explicit root-document result. Relative path syntax alone is not resource validation.

`queryContext.set` uses a structured, serializable canonical context. Keep it distinct from the chart document and from ad hoc query strings; validate field references, safe values, and every canonical context field supported by runtime.

For `crossFilter.configure`, `drilldown.configure`, and `selection.configure`:

- operation-specific handler choice determines the event key; do not persist an input-only `event` discriminator into `PraxisXUiChartEventAction`;
- persist only canonical event fields: `action`, optional `target`, and optional `{ sourceField: targetField }` mapping;
- validate mapping keys against Chart output fields and values against the governed target input contract;
- apply the same compiler policy to selection as to cross-filter and drilldown; generic merge is acceptable only when it proves the identical canonical shape and diagnostics;
- do not claim an operation is executable until the runtime emits and consumes that interaction.

`legend.configure` and `tooltip.configure` remain visual-only path-local effects unless their implementation changes data behavior.

## Registry And Consumer Parity

The Angular manifest, generated ingestion registry, and `praxis-config-starter` classpath snapshot must agree exactly on operation IDs, targets, schemas, validators, effects, handler contracts, `affectedPaths`, and `submissionImpact`. Count equality is insufficient.

When source changes cross Angular and backend, do not compensate for a stale snapshot by weakening an Angular handler contract. Update the canonical owner and derived projection in the same cycle, or record the exact drift as a backend follow-up.

Revisit editor/config/runtime pairing whenever a handler writes `chartDocument`, `queryContext`, resource binding, metrics, axes, or events. A compiled document that renders but is lost on apply/save/reopen is not a successful handler.

## Validation

Run the smallest set that covers the changed boundary.

Angular declaration and consumers:

```bash
npx ng test praxis-charts --watch=false --progress=false \
  --include='projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts' \
  --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' \
  --include='projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.spec.ts' \
  --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts' \
  --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts'
```

Registry publication:

```bash
npm run generate:registry:ingestion
npm run validate:authoring-contracts
```

Backend execution, from `praxis-config-starter`:

```bash
mvn -Dtest=AgenticAuthoringManifestServiceTest,AgenticAuthoringTargetResolverRegistryTest,AgenticAuthoringValidatorRegistryTest,AgenticAuthoringEffectCompilerRegistryTest test
```

Add focused negative coverage for duplicate/missing series identity, missing insertion target, non-combo secondary axis, absent metadata/capability, unknown validator or handler, compiled path/value mismatch, noncanonical event fields, reversed mapping, partial mutation after failure, and editor/runtime round-trip loss.

Report declaration, backend execution, registry publication, and consumer round-trip separately. Passing structural manifest validation does not prove a handler can safely compile or apply a Chart decision.
