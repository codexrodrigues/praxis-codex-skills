---
name: praxis-config-ai-registry-manifests
description: Use when Codex must work on praxis-config-starter AI registry contracts: ai_registry, /api/praxis/config/ai-registry/**, component definitions, registry snapshot ingestion, templates, authoringManifest projection, editableTargets, operations, validators, effect compilers, presentation affordances, manifest validation, and compile-patch endpoints.
---

# Praxis Config AI Registry Manifests

Use this skill for the canonical backend registry that stores component definitions, templates, and executable authoring manifests in `praxis-config-starter`. The registry is a governed tool contract, not a documentation cache.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/config/controller/RegistryIngestionController.java`
- `src/main/java/org/praxisplatform/config/controller/AiRegistryTemplateController.java`
- `src/main/java/org/praxisplatform/config/controller/AgenticAuthoringManifestController.java`
- `src/main/java/org/praxisplatform/config/service/RegistryIngestionService.java`
- `src/main/java/org/praxisplatform/config/service/AiRegistryTemplateService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringManifestService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringManifestContractValidator.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringTargetResolverRegistry.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringValidatorRegistry.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringEffectCompilerRegistry.java`
- `src/main/resources/ai-registry/registry-snapshot.json`
- `src/main/resources/ai-authoring/**`
- focused registry, manifest, validator, compiler, and contract tests.

## Canonical Boundary

`/api/praxis/config/ai-registry/component-definitions` ingests component registry snapshots. `/api/praxis/config/ai-registry/templates/**` owns persisted AI templates. `/api/praxis/config/ai/authoring/manifests/{componentId}/**` projects executable manifests from `ai_registry`.

Executable manifests govern `editableTargets`, `operations`, validators, target resolvers, destructive confirmation, effect compilation, `compiledOperations`, `patchOperations`, and `proposedConfig`. They are public contracts, not hints.

## Decision Rules

- Do not expose arbitrary JSON patching when a component can declare governed operations.
- Keep registry ingestion, manifest projection, validators, effect compilers, and generated resources synchronized.
- If a component authoring operation is missing, add or correct the manifest/registry contract instead of adding a backend fast path.
- Do not let templates override component runtime contracts or backend resource semantics.
- Presentation affordance catalogs are grounding for authoring; they do not authorize business-rule materialization.
- Preserve tenant/environment headers when ingesting registry snapshots or templates.

## No Keyword Routing

Do not select manifest operations, targets, validators, or effect compilers through command words, labels, aliases, regexes, or local fuzzy matching as the primary decision. Use the manifest's declared operations, editable targets, resolver ids, validator ids, component registry keys, and governed tool contracts; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding registry fields, template fields, manifest operations, validator ids, compiler effects, endpoint variants, or generated artifacts, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real gaps justify new manifest or registry contracts. Identify the owning component, backend projection, Angular registry ingestion, public docs, generated artifacts, and validation.

## Validation

Use focused local gates:

- registry/template: `mvn "-Dtest=RegistryIngestionServiceTest,RegistryIngestionServiceIdentityTest,AiRegistryBootstrapServiceTest,AiRegistrySnapshotContractTest" test`
- manifests: `mvn "-Dtest=AgenticAuthoringManifestServiceTest,AgenticAuthoringManifestControllerTest,AgenticAuthoringManifestContractValidatorTest,AgenticAuthoringTargetResolverRegistryTest,AgenticAuthoringValidatorRegistryTest,AgenticAuthoringEffectCompilerRegistryTest" test`
- public AI contract changes: `mvn "-Dtest=AiApiContractOpenApiTest,AiContractSpecConsistencyTest,AiContractV11RetroCompatibilityTest" test`

Review `docs/ai/contracts/**`, `src/main/resources/ai-authoring/**`, Angular `praxis-ai-authoring-manifests`, registry ingestion outputs, and quickstart smokes when public manifest behavior changes.

## Companion Skills

- Use `praxis-config-agentic-authoring-streaming` when manifests are used by turn execution, preview, compile, apply, quick replies, or stream payloads.
- Use `praxis-config-runtime-persistence` when compiled patches persist to `/api/praxis/config/ui`.
- Use `praxis-ai-authoring-manifests` for Angular/component manifest authoring.
- Use `praxis-ai-registry-ingestion` for generated Angular registry assets.
