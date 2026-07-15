---
name: praxis-ai-authoring-manifests
description: Use when creating, updating, reviewing, or validating Praxis component authoring manifests, `ComponentAuthoringManifest`, editableTargets, operations, validators, effects, handler contracts, consult/edit response modes, component edit plans, authoring context packs, AI adapters, or manifest synchronization after public component API/editor/runtime changes.
---

# Praxis AI Authoring Manifests

Use this skill for executable AI authoring contracts. A manifest is not decorative documentation; it is the contract that tells backend tools how to ground, validate, compile, and reject component edits.

Pair with `praxis-ai-backend-config-contracts` when manifest operations are exposed through `/api/praxis/config/ai/**`; pair with `praxis-ai-turn-orchestration-transport` when component edit plans are transported through assistant turns; pair with `praxis-ai-composer-attachments-quick-replies` when quick replies or clarifications select manifest targets or operations.

Use `praxis-config-ai-registry-manifests` when the backend `ai_registry`, registry snapshot ingestion, manifest projection, validators, compilers, or `/api/praxis/config/ai/authoring/manifests/**` behavior is the source of truth. Do not patch Angular manifests to compensate for stale backend registry projection.

## Canonical Model

Every manifest change must preserve:

`public component surface -> editable targets -> operation schema -> validators -> effects/handler contract -> affected paths -> editor/runtime round-trip -> registry ingestion`

Do not expose arbitrary JSON patching when a component requires governed semantic decisions. Use component-specific operations with deterministic targets, schemas, validators, and effects.

## Required Inventory

Inspect the owning component:

- `projects/<lib>/src/lib/ai/*authoring-manifest.ts`
- focused manifest spec
- AI adapter and context pack when present
- component `public-api.ts`
- component metadata / `ComponentDocMeta` / `configEditor`
- visual editor and runtime specs for the edited paths
- related docs, examples, recipes, and registry ingestion outputs when public behavior changes

Also inspect `projects/praxis-core/src/lib/ai/authoring-manifest.types.ts` when changing manifest shape.

When backend registry projection, validation, compilation, or `/api/praxis/config/ai/authoring/manifests/**` endpoints are in scope, inspect `praxis-config-starter/AGENTS.md`, `AgenticAuthoringManifestController`, `AgenticAuthoringManifestService`, `AgenticAuthoringManifestContractValidator`, `AgenticAuthoringManifestEditPlanRequest`, `AgenticAuthoringManifestValidationResult`, `AgenticAuthoringManifestCompileResult`, and their focused tests. The backend is the runtime authority for resolving registry manifests, validating edit plans, compiling patches, and returning controlled configuration errors.

When ingestion/projection is in scope, inspect `praxis-ai-registry-ingestion`: `extract-component-docs.js` preserves `authoringManifestRef`, `generate-registry-ingestion.ts` projects `authoringManifest`, `authoringManifestProfiles`, and authoring-only entries, and `validate-authoring-contracts-acceptance.js` verifies the generated registry entry. Do not treat a source manifest as public until its registry projection is proven.

For component-specific manifest work, use the focused skill when available: `praxis-page-builder-ai-agentic` for `PRAXIS_PAGE_BUILDER_AUTHORING_MANIFEST`, `UiCompositionPlan`, child operation delegation, streaming authoring, and Page Builder registry gates; `praxis-visual-builder-rules` for `PRAXIS_VISUAL_BUILDER_AUTHORING_MANIFEST`, rule graph operations, JSON Logic round-trip, and visual-builder AI adapter behavior.

## Manifest Rules

- Separate `consult/answer` from `edit/componentEditPlan`; factual questions must not fabricate patches.
- Every operation target must resolve through an editable target with explicit ambiguity policy.
- `scope=global` operations must use `target.required=false`; all non-global operations must provide a structured `target` with `kind`, `resolver`, `ambiguityPolicy`, and `required=true` unless the type or source owner documents a safe exception. Do not use the reserved `scope='target'`.
- Operation input schemas must be concrete enough for backend tooling; broad objects require a resolvable downstream schema or explicit blocker.
- `compile-domain-patch` effects need deterministic handler contracts: reads, writes, stable identity keys, input schema, failure modes, and operational description.
- A new `compile-domain-patch.handler` is only an Angular declaration until `AgenticAuthoringEffectCompilerRegistry.supportsDomainPatchHandler(handler)` and focused backend compiler tests prove it. Classify it as `suportado-parcialmente` until then.
- Effects must overlap affected paths and validators must be used by pertinent operations.
- Destructive operations require confirmation.
- Family-level manifests need an aggregate registry entry addressable by `componentId`, not only child copies.
- Declared-only fields may be authorable for round-trip, but docs/validators must not imply active runtime behavior.
- Every non-global operation declares `target.kind`, resolver, ambiguity policy, preconditions, supported string `submissionImpact`, validators, effects, and affected paths. The deprecated `targetKind`, when retained, must equal `target.kind`; boolean `submissionImpact` is legacy only and should not be introduced in semantically validated manifests.
- Every global validator is used by an operation. Effect paths must overlap affected paths; collection effects declare identity keys; `compile-domain-patch` declares reads, writes, identity keys, input schema, failure modes, and a meaningful handler description.
- Manifest examples are executable grounding/eval evidence: include positive examples and at least one explicit negative example. Do not encode lexical routing as an example substitute.
- Remote-binding operations must prove input-schema and path/effect evidence, use a pertinent binding validator, and declare `affects-remote-binding`; do not label an unrelated operation as remote merely to satisfy a gate.
- Family `controlProfiles` repeat the same operation metadata and applicability evidence. The generated registry must expose the aggregate family entry, `projectedComponentIds`, child `authoringManifestProfiles`, and preserved operation metadata.
- For family manifests, edit profile semantics only in the aggregate source manifest. Child
  `authoringManifestProfiles` in generated registry entries are applicability projections, not a
  second manifest source. If a child component lacks a projected profile, audit the family
  `controlProfiles.appliesTo` rules, component docs extraction, and registry ingestion before adding
  a new operation, patching the corpus, or treating a capability alias as a component identity.
- Presentation affordances must identify their source, default target, and compatible options; they are consultative constraints, not edit permission.
- Quick replies, clarification options, feedback, stream diagnostics, and transport lifecycle events may select or carry
  a backend-issued semantic decision, but they cannot invent `operationId`, target resolver, validator, effect, handler,
  affected path, `submissionImpact`, or apply permission. Those must resolve back to the projected manifest and backend
  validation/compilation contract.
- A `semanticDecision` or `componentEditPlan` is only executable when every referenced operation, target, validator,
  effect, and presentation affordance can be traced to the current registry-projected manifest for the component/profile.
  Treat untraceable references as contract drift or clarification, not as a reason to patch UI state locally.

## Synchronization Triggers

Review manifests when a public component change touches:

- inputs, outputs, events, config paths, editor fields, defaults, capabilities, actions, surfaces
- apply/save/reset/reopen behavior
- runtime/editor parity
- `ComponentDocMeta`, `configEditor`, public README, examples, recipes, playgrounds
- AI assistant context, quick replies, diagnostics, preview, apply payload, or component edit plan
- backend AI manifest endpoints, turn stream payloads, quick reply semantic decisions, or clarification options that reference manifest targets/operations

If no manifest update is required after a public change, state why.

## Validation

Run the focused manifest spec first. Use `npm run validate:authoring-contracts` or the direct validator when the manifest is complete/public. Use `praxis-ai-registry-ingestion` when generated registry/catalog artifacts must be updated or verified.

For backend registry projection, manifest endpoint, edit-plan validation, compile-patch, presentation affordance, or configuration-error behavior, run the focused config-starter gate:

```sh
mvn "-Dtest=AgenticAuthoringManifestContractValidatorTest,AgenticAuthoringManifestServiceTest,AgenticAuthoringManifestControllerTest" test
```

For Angular public manifest corpus changes, run:

```sh
npm run validate:authoring-contracts
```

For manifest changes that add or rename operation ids, target resolvers, validator ids, effect kinds, `compile-domain-patch` handlers, presentation affordance catalogs, or family profiles consumed by the config backend, pair Angular and backend proof:

```sh
npm run generate:registry:ingestion
mvn "-Dtest=AgenticAuthoringManifestServiceTest,AgenticAuthoringManifestControllerTest,AgenticAuthoringManifestContractValidatorTest,AgenticAuthoringTargetResolverRegistryTest,AgenticAuthoringValidatorRegistryTest,AgenticAuthoringEffectCompilerRegistryTest" test
```

For a public manifest, prove the owning runtime/editor round-trip and inspect the generated registry entry, public export, README claim, and required implementation/semantic reports. A passing TypeScript literal is insufficient when targets, effects, validators, profile projection, or runtime coverage disagree.
