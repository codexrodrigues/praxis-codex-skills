---
name: praxis-editorial-forms-journey-snapshot-runtime
description: Use when implementing or auditing `@praxisui/editorial-forms` journey resolution, `EditorialRuntimeInput`, `EditorialSolutionDefinition`, `EditorialTemplateInstance`, `EditorialRuntimeState`, `resolveEditorialRuntimeSnapshot()`, context merge, presets, block provenance, overrides, runtime snapshots, and `snapshotChange`.
---

# Praxis Editorial Forms Journey Snapshot Runtime

Use this skill when the work touches the canonical editorial runtime model: solution, instance, runtime context, journeys, steps, blocks, presets, overrides, resolved snapshot, and block provenance.

## Source Audit

Inspect before editing:

- `projects/praxis-editorial-forms/AGENTS.md`
- `projects/praxis-editorial-forms/README.md`
- `projects/praxis-editorial-forms/docs/architecture.md`
- `projects/praxis-editorial-forms/src/public-api.ts`
- `projects/praxis-editorial-forms/src/lib/editorial-runtime.contract.ts`
- `projects/praxis-editorial-forms/src/lib/editorial-form-runtime.component.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-state.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-preset-resolver.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-snapshot.model.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime.helpers.ts`
- focused runtime, preset resolver, technical harness, and E2E lab specs

## Canonical Boundary

`@praxisui/editorial-forms` owns the resolved editorial runtime. `@praxisui/core` owns shared domain types such as `EditorialSolutionDefinition` and `EditorialTemplateInstance`. The runtime resolves those inputs into an `EditorialRuntimeSnapshot`; hosts should consume `snapshotChange` rather than reconstructing journeys, presets, provenance, or fallback locally.

Do not reduce editorial experiences to `FormConfig.sections`, rows, columns, or dynamic-form config. Use `@praxisui/dynamic-form` only through explicit `dataCollection` adapters.

## Snapshot Rules

- Treat `solution`, `instance`, and `runtimeContext` as the runtime input document.
- Merge context from `instance.context`, `instance.overrides.contextPatch`, and host `runtimeContext` deterministically.
- Validate context contracts, compliance presets, compliance evidence, and required acceptances before rendering.
- Resolve journeys, active journey, active step, blocks, compliance preset blocks, instance journeys, and journey overrides before rendering.
- Preserve block provenance with source refs, primary source, composition trail, and deterministic override operations.
- Keep supported override operations canonical: `append`, `insertBefore`, `insertAfter`, `replace`, and `remove`.
- Invalid references and concurrent override conflicts should produce diagnostics; do not silently repair authored data.
- `snapshotChange` is host-facing evidence for audit trails, UX derivation, diagnostics, and product state.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: snapshot/provenance exists but the host, docs, or lab does not surface it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer calls journey state a page, wizard, or form state while `EditorialRuntimeSnapshot` already owns it.
- `suportado-parcialmente`: a solution/instance path exists but snapshot merge, provenance, override diagnostics, or E2E proof is incomplete.
- `lacuna-real-de-contrato`: no existing solution, instance, context, journey, block, provenance, or snapshot shape can express the requirement.

Only a real contract gap justifies new public domain fields or exported runtime types.

## Validation

Use focused local proof:

- snapshot/presets/provenance: `src/lib/runtime/editorial-preset-resolver.spec.ts`
- runtime component/state: `src/lib/editorial-form-runtime.component.spec.ts`
- harness fixtures: `src/lib/testing/editorial-runtime-technical-harness.component.spec.ts`
- public API: `src/public-api.ts` audit and `npm run build:praxis-editorial-forms` when exports or public runtime contracts change
- host/labs: `test-dev/e2e/editorial-runtime-lab.playwright.spec.ts` and `editorial-runtime-experiments.playwright.spec.ts` when real host behavior changes

Pair with `praxis-editorial-forms-presentation-diagnostics` for fallback/presentation, `praxis-editorial-forms-data-collection-adapters` for `dataCollection`, and `praxis-editorial-forms-agentic-authoring` for manifest-backed authoring.
