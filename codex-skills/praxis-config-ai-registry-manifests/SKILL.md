---
name: praxis-config-ai-registry-manifests
description: Use when implementing, reviewing, debugging, or validating praxis-config-starter AI registry persistence, component registry ingestion, bootstrap snapshots, templates, semantic search, RAG publication, executable authoring manifest projection, target resolution, validators, effect compilers, presentation affordances, or /api/praxis/config/ai-registry/** and /api/praxis/config/ai/authoring/manifests/** contracts.
---

# Praxis Config AI Registry Manifests

Use this skill for the canonical backend registry that persists component definitions, templates,
snapshot metadata, and their executable authoring projection in `praxis-config-starter`.
`ai_registry` is governed persistence. It is not a documentation cache, an Angular runtime registry,
or permission to execute whatever appears in a generated JSON document.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/config/domain/AiRegistry.java`
- `src/main/java/org/praxisplatform/config/repository/AiRegistryRepository.java`
- `src/main/java/org/praxisplatform/config/controller/RegistryIngestionController.java`
- `src/main/java/org/praxisplatform/config/service/RegistryIngestionService.java`
- `src/main/java/org/praxisplatform/config/registry/AiRegistryBootstrapService.java`
- `src/main/java/org/praxisplatform/config/registry/AiRegistryStatusService.java`
- `src/main/java/org/praxisplatform/config/controller/AiRegistryTemplateController.java`
- `src/main/java/org/praxisplatform/config/service/AiRegistryTemplateService.java`
- `src/main/java/org/praxisplatform/config/controller/AgenticAuthoringManifestController.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringManifestService.java`
- manifest contract validator, target resolver, validator, effect compiler, capability catalog, and
  presentation-affordance services under `src/main/java/org/praxisplatform/config/ai/authoring/`
- `src/main/resources/ai-registry/registry-snapshot.json`
- `docs/ai/contracts/**` and focused registry, bootstrap, manifest, compiler, controller, and OpenAPI tests.

Inspect the Angular producer with `praxis-ai-registry-ingestion` before changing ingestion shape:

- `praxis-ui-angular/tools/ai-registry/AGENTS.md`
- `generate-registry-ingestion.ts`, its JSON schema, catalog governance, authoring acceptance,
  upload, package-assets, RAG/provider projection, and backend-sync tools
- the owning component manifest and spec with `praxis-ai-authoring-manifests`.

## Canonical Flow

Preserve this ownership chain:

`Angular public API + component metadata + authoring manifest + recipes`
`-> canonical aggregate ingestion registry`
`-> POST /api/praxis/config/ai-registry/component-definitions`
`-> SYSTEM/GLOBAL component_definition records in ai_registry`
`-> release-scoped RAG documents as a derived index`
`-> executable /api/praxis/config/ai/authoring/manifests/{componentId}/** projection`

The Angular aggregate `dist/praxis-component-registry-ingestion.json` is the canonical generated
publication input. Package `ai/component-registry.json`, provider projections, compact registry RAG,
and the backend classpath snapshot are derived artifacts. Regenerate or synchronize them; do not
edit them as independent sources of truth.

The classpath snapshot is an operational fallback/bootstrap artifact. Compare its component count,
manifest coverage, chunks, hash, version, and `generatedAt` with the current Angular ingestion corpus
before claiming that the backend represents current platform capabilities. Registry health proves
configured minimum counts and required IDs, not semantic completeness or release parity.

## Persistence And Scope

`AiRegistry` identity is the tuple:

`registryType + registryKey + componentType + scope + scopeKey`

Current component definitions and templates are persisted as `Scope.SYSTEM` / `GLOBAL`. Ingestion
headers `X-Tenant-ID` and `X-Env` scope the derived RAG publication identity; they do not silently
turn the canonical component definition into tenant-owned registry state. Do not invent tenant or
environment persistence semantics without an explicit public-contract decision.

Keep these record families distinct:

- `component_definition`: generated component contract, including `componentDefinition.jsonSchema`
  and optional `authoringManifest`;
- `template`: reusable component config plus `aiDescription` and `templateMeta`, with semantic search;
- `registry_snapshot_metadata`: bootstrap hash, source, location, release identity, count, and time;
- release-scoped RAG documents: derived retrieval copies, never the persistence source of truth.

Upsert behavior must preserve stable identity and explicitly govern payload, embedding, source,
status, version, ETag, and timestamps. Do not claim optimistic concurrency or incremental versioning
unless update tests prove that `version` and `etag` actually change under the documented policy.

## Executable Manifest Boundary

The backend reads an executable manifest only from:

`component_definition.payload.componentDefinition.jsonSchema.authoringManifest`

A missing manifest is valid for a consult-only/non-authorable component. It must produce a clear
not-found/configuration outcome when an executable manifest endpoint is requested; it must not fall
back to arbitrary JSON patching.

For an authorable component, preserve the complete chain:

`editableTargets -> operationId -> target resolver -> input schema -> validators -> effects/handler`
`-> affected paths -> destructive confirmation -> compiledOperations/patchOperations/proposedConfig`

Apply these rules:

- Resolve only operations declared by the selected component manifest.
- Require deterministic target resolution and fail on missing or ambiguous required targets.
- Require explicit confirmation for destructive operations.
- Treat `presentationAffordances` as semantic grounding for compatible presentation choices, not as
  business authorization or an effect compiler.
- Treat runtime observations, chunks, examples, labels, aliases, and templates as grounding evidence,
  never as permissions.
- Fail closed when a referenced validator, target resolver, or domain effect handler has no backend
  implementation. A warning is not sufficient evidence for executable compile/apply.
- Keep `compiledOperations` as normalized audit output, `patchOperations` as applicable materialization,
  and `proposedConfig` as preview. None of them bypasses persistence ETag, authorization, or domain
  decision governance.
- Templates may seed or rank a configuration candidate; they cannot override component manifests,
  backend resource semantics, metadata capabilities, or domain decisions.

## Semantic Routing

Do not select component, operation, target, validator, compiler, or template through command words,
regexes, aliases, labels, or fuzzy matching as the primary decision. Use governed context, component
registry keys, declared manifests/tools, metadata and capability catalogs, and LLM semantic intent.
Vector search or textual matching may rank templates or candidates only after semantic scope is known.

If an operation or tool is absent, add it to the canonical owner and synchronize the publication
pipeline. Do not replace the missing contract with a backend fast path or frontend-only patch.

## Aderence Inventory

Before adding registry fields/types, scope variants, endpoint variants, template metadata, manifest
operations, validator IDs, resolver IDs, compiler handlers, health signals, or generated artifacts,
ask what the platform already knows and classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public contract. Name the missing evidence, canonical
owner, persistence and migration impact, Angular producer, assistant/quickstart consumers, generated
artifacts, docs/OpenAPI impact, compatibility risk, and minimum proof before editing.

## Validation

Run the smallest local gate that proves the changed boundary:

- ingestion identity, invalid manifests, chunk/RAG publication, bootstrap refresh/prune, and snapshot:
  `mvn "-Dtest=RegistryIngestionServiceIdentityTest,AiRegistryBootstrapServiceTest,AiRegistrySnapshotContractTest" test`
- executable manifests, target resolution, validators, compilers, and HTTP projection:
  `mvn "-Dtest=AgenticAuthoringManifestServiceTest,AgenticAuthoringManifestControllerTest,AgenticAuthoringManifestContractValidatorTest,AgenticAuthoringTargetResolverRegistryTest,AgenticAuthoringValidatorRegistryTest,AgenticAuthoringEffectCompilerRegistryTest" test`
- public AI contract changes:
  `mvn "-Dtest=AiApiContractOpenApiTest,AiContractSpecConsistencyTest,AiContractV11RetroCompatibilityTest" test`
- Angular producer changes: focused tool specs, then `npm run validate:catalog` and
  `npm run validate:authoring-contracts`; use `npm run generate:registry:ingestion` when aggregate
  publication must be regenerated.

For templates, prove object validation, default description, identity-preserving upsert, semantic
search scoping/limits, payload mapping, bulk partial failure, delete/not-found, and HTTP/security
behavior. If the owner has no focal template tests, record that as a platform test gap instead of
presenting unrelated registry tests as proof.

Audit one happy path and these adversarial paths:

- invalid or missing manifest, undeclared operation, unresolved/ambiguous target;
- destructive edit without confirmation;
- validator/resolver/compiler declared but not implemented;
- stale classpath snapshot versus current Angular aggregate;
- component removal and release-scoped RAG cleanup;
- malformed template config and cross-component template search;
- tenant/environment headers incorrectly assumed to change persisted registry scope.

Use the quickstart HTTP/SSE smoke only when registry behavior changes downstream authoring execution.
Reserve GitHub Actions for the final phase/release gate after local proof.

## Derived Artifacts

After public registry or manifest changes, review and synchronize as applicable:

- Angular aggregate ingestion registry and package-scoped AI assets;
- backend classpath snapshot and snapshot contract tests;
- compact RAG compatibility and provider projections;
- template plans/uploads and registry sync scripts;
- `docs/ai/contracts/**`, OpenAPI consistency, public docs/examples, and quickstart smokes.

State explicitly when an artifact does not need an update and why.

## Companion Skills

- Use `praxis-ai-authoring-manifests` for the owning Angular component manifest.
- Use `praxis-ai-registry-ingestion` for generation, governance, packaging, and upload tooling.
- Use `praxis-config-agentic-authoring-streaming` for semantic turn resolution, preview/apply, SSE,
  quick replies, diagnostics, and replay.
- Use `praxis-config-runtime-persistence` for applying a compiled component config with scope and ETag.
- Use `praxis-config-api-metadata-grounding` for API/resource RAG and metadata grounding; do not store
  resource-domain truth in component registry records.
- Use `praxis-config-domain-decisions` when an authoring operation materializes a governed business
  decision rather than component configuration.
