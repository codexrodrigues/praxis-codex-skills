---
name: praxis-reactive-determinations
description: Use when implementing, auditing, or proving Praxis Reactive Determinations across metadata, governed rule snapshots, Java hosts, Angular Dynamic Form/CRUD/Stepper, diagnostics, and HTTP corpus: definition registries, trigger/form modes, input/output bindings, provenance, execution ordering, stale/cancel handling, last-known-good snapshot consumption, or migration away from legacy Form Effects.
---

# Praxis Reactive Determinations

Use this skill for the end-to-end handoff from a governed semantic decision to
reactive form behavior. Reactive Determinations replaced the former Form Effect
contract; do not reintroduce removed `@FormEffect` annotations, `formEffects`
schema blocks, or frontend-authored business formulas.

## Canonical Owners

- `praxis-config-starter` owns governed domain-rule authoring, approvals,
  publication, immutable snapshots, active heads, rollback, and materialization.
- `praxis-metadata-starter` owns the public metadata vocabulary and compiles
  registered determination definitions into operation-specific `x-ui` schema.
- The Java host owns facts, executable provider/registry implementations,
  authorization, transactions, and business effects.
- `praxis-ui-angular` owns the generic runtime materialization and diagnostics.
  It does not become the business-rule owner.
- Quickstart and HTTP Examples prove the chain; they do not redefine it.

## Required Source Audit

Inspect the affected owner and direct consumers:

- Metadata `docs/spec/reactive-determinations.md`,
  `uischema/determination/**`, compiler and contract specs
- Config `DomainRuleReactiveDeterminationSpec`, snapshot/control-plane services,
  materialization migration, rule tests, and active-head rules
- Quickstart `ReactiveDeterminationPilotConfiguration`, applied resolver,
  provider/ruleset, tenant-scope and resolver tests
- Angular Core reactive-determination model, Dynamic Form runtime service/spec,
  CRUD dialog/drawer handoff, Stepper adapter, Metadata Editor diagnostics, and
  component metadata/registry projection
- HTTP examples, payloads, manifest, corpus verifier, and smoke

## Contract Rules

- A definition has stable identity, scope, applicable form modes, trigger mode,
  typed input bindings, typed output bindings, and provenance.
- Resolve operation-specific metadata for the actual create/edit/action surface.
  A definition present on another operation is not applicable evidence.
- Input bindings read the current governed form snapshot. Output bindings write
  only declared targets under their documented write policy; do not patch
  arbitrary config or component state.
- Preserve definition/snapshot provenance through metadata, runtime diagnostics,
  HTTP evidence, and authoring explanations. Labels and prompts cannot select a
  determination.
- Order executions deterministically. When inputs change again, stale results
  must not overwrite a newer form state. Cancellation, debounce, concurrency,
  and partial output behavior must be explicit and tested.
- Fail closed for unknown definitions, invalid bindings, missing provider,
  incompatible snapshot, denied scope, malformed result, or unresolved output.
  Do not fall back to a local formula or legacy Form Effect.
- A host consuming governed snapshots validates scope, compatibility, content
  hash, head identity, and monotonic activation before an atomic last-known-good
  swap. A failed candidate leaves the last valid runtime active and visible in
  health/diagnostics without leaking snapshot payloads.
- Dynamic Form owns generic execution and form-state application. CRUD and
  Stepper pass the correct operation/form context; they do not duplicate the
  determination engine.

## Implementation Workflow

1. Inventory what the platform already publishes: active decision/snapshot,
   registered definition, operation schema, bindings, runtime service,
   diagnostics, and HTTP proof.
2. Classify the gap. Missing UI diagnostics or adapter propagation is not a new
   metadata contract. Missing business logic belongs to Config/host, not Angular.
3. Implement at the canonical owner and update the complete handoff only where
   its public projection changed.
4. Preserve beta cleanup: migrate consumers and derived docs in the same cycle;
   do not keep parallel Form Effect and Reactive Determination paths without an
   explicit operational requirement.
5. Prove tenant/operation/form-mode isolation and sanitized diagnostics.

## Proof Matrix

Minimum focused gates:

```bash
# metadata owner
mvn "-Dtest=ReactiveDeterminationMetadataCompilerTest,ReactiveDeterminationSpecContractTest" test

# Angular runtime
npm run test:core -- --include=projects/praxis-core/src/lib/models/form/reactive-determination.model.spec.ts
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/services/reactive-determination-runtime.service.spec.ts

# quickstart host
mvn "-Dtest=AppliedReactiveDeterminationResolverTest,ReactiveDeterminationTenantScopeHttpTest" test

# HTTP corpus
node smoke/verify-reactive-determination-corpus.mjs
node smoke/smoke-reactive-determinations.mjs
```

Run each command from its owning repository and add Config snapshot/rule tests
when authoring, publication, head, or materialization changes.

Prove happy execution, invalid inputs/business rejection, stale/cancel race,
tenant or operation mismatch, incompatible snapshot/LKG behavior, and absence
of legacy Form Effect output. Review Metadata docs, Angular JSON API/registry,
Quickstart pilot docs, HTTP manifest/LLM surface, and public examples whenever
the mirrored contract changes.

## Companion Skills

- `praxis-config-domain-decisions` and `praxis-rules-engine-runtime`: governed rule/snapshot lifecycle.
- `praxis-metadata-schema-contracts`: operation-specific schema and `x-ui` publication.
- `praxis-form-schema-runtime-modes` and `praxis-form-actions-hooks-runtime`: Angular form context and lifecycle.
- `praxis-crud-dialog-form-host-lifecycle` and `praxis-stepper-wizard-runtime`: host adapters.
- `praxis-api-quickstart-domain-pilots` and `praxis-http-examples-contract-surfaces`: operational/public proof.

