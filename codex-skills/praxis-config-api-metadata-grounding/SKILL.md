---
name: praxis-config-api-metadata-grounding
description: Use when Codex must implement, audit, or consume Praxis API grounding: api_metadata ingestion and search, release-scoped RAG documents, /api/praxis/config/ai-context/**, /schemas/filtered resolution, Project Knowledge retrieval, component corpus evidence, resource candidates, consultative API Catalog answers, or grounding provenance and diagnostics.
---

# Praxis Config API Metadata Grounding

Use this skill for API catalog ingestion, AI context composition, RAG/project-knowledge retrieval, and resource candidate grounding in `praxis-config-starter`. `api_metadata` is evidence for semantic grounding; it must not become a hardcoded conversational router.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/config/controller/ApiMetadataController.java`
- `src/main/java/org/praxisplatform/config/controller/AiContextController.java`
- `src/main/java/org/praxisplatform/config/controller/ContextRetrievalController.java`
- `src/main/java/org/praxisplatform/config/service/ApiMetadataIngestionService.java`
- `src/main/java/org/praxisplatform/config/service/AiContextService.java`
- `src/main/java/org/praxisplatform/config/service/ContextRetrievalService.java`
- `src/main/java/org/praxisplatform/config/service/SchemaRetrievalService.java`
- `src/main/java/org/praxisplatform/config/domain/ApiMetadata.java`
- `src/main/java/org/praxisplatform/config/repository/ApiMetadataRepository.java`
- `src/main/java/org/praxisplatform/config/dto/ApiCatalogRequest.java`
- `src/main/java/org/praxisplatform/config/dto/ApiSearchResult.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringApiMetadataCandidateCatalog.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringResourceDiscoveryService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringProjectKnowledgeService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/VectorRankedProjectKnowledgeCandidateRetriever.java`
- `src/main/java/org/praxisplatform/config/service/RagProjectKnowledgeDerivedIndexService.java`
- `src/main/java/org/praxisplatform/config/rag/RagDocumentIdentity.java`
- `src/main/java/org/praxisplatform/config/rag/RagFilters.java`
- `src/main/java/org/praxisplatform/config/rag/**`
- `src/main/resources/db/migration/V4__create_api_metadata.sql`, `V28__scope_api_metadata_identity.sql`, `V8__create_api_metadata_embedding_index.sql`, and vector-store migrations.
- `praxis-ui-angular/projects/praxis-ai/src/lib/core/services/ai-backend-api.service.ts`
- focused API metadata, context, RAG, project knowledge, and resource discovery tests.

## Canonical Boundary

`/api/praxis/config/api-catalog/ingest` stores normalized API metadata and publishes derived vector-store documents for retrieval. `/api/praxis/config/ai-context/**` composes component state, templates, schema hints, runtime config, and grounding context for AI authoring.

API Catalog Q&A should be an informative grounded answer path. It should not start `page-preview`, require executable resource clarification, or apply configuration until a later turn chooses an executable authoring route.

Keep the sources distinct: `praxis-metadata-starter` owns current resource structure and semantics through `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, and capabilities. `praxis-config-starter` persists an ingested operational API search corpus and governs how that evidence is retrieved for AI. RAG documents, caches, candidate rankings, context packs, and answers are derived projections.

## Ingestion Contract

- `POST /api/praxis/config/api-catalog/ingest` accepts endpoint snapshots with path, method, tags, summary, description, operation id, request/response schemas, parameters, release id, version, and generated timestamp. An empty endpoint list is a no-op.
- The structured `api_metadata` row currently stores tenant, environment, service key, release id/version, generated time, full schemas, parameters, raw endpoint JSON, and embedding.
- Current scoped identity is canonical: V28 adds `tenant_id`, `environment`, `service_key`, and `release_id`, replaces the legacy global `path + method` unique key, and enforces `tenant_id + environment + service_key + release_id + path + method`.
- Upsert first by scoped `path + method`, then by scoped stable `operationId + method` to reconcile a moved endpoint without crossing tenant, environment, service, or release boundaries.
- Release identity resolves from `releaseId`, then version/generated time according to `RagDocumentIdentity`. Preserve that identity and the content hash; do not publish anonymous chunks that cannot be replayed or purged by scope.
- The controller returns `202 Accepted`, but the current service performs structured upsert and attempted vector publication during the request. `202` is not proof that an optional vector store exists or that the derived corpus is reconciled.
- Vector publication is derived and optional. A disabled/unavailable vector store must not invalidate the canonical structured metadata, and a vector row must never become authority over a later canonical schema response.

## Retrieval Precedence

For API and component-definition search, preserve this order and diagnostics:

1. Resolve a release id and query the vector store with `resourceType`, tenant/environment when provided, release, and method filters.
2. Apply default-release fallback only when `praxis.ai.rag.release.fallback.default-enabled=true`; legacy `version` metadata fallback is a separate compatibility setting.
3. When the vector store is available but the scoped release has no result, return no candidates instead of silently using the global structured table.
4. When vector search is unavailable, legacy pgvector repository retrieval is allowed only for an unscoped request. Tenant/environment-scoped requests fail closed.

`tags` filtering is supported by the legacy repository query but not by the current vector path. Treat tag-filtered retrieval with RAG enabled as `suportado-parcialmente`; do not promise it works until the vector metadata/filter contract is implemented and tested.

Semantic retrieval is candidate grounding, not primary intent resolution. `AgenticAuthoringApiMetadataCandidateCatalog` prefers semantic evidence, may supplement it with explicit or weak lexical evidence, and marks provenance such as `semantic-retrieval`, `lexical-fallback`, `weak-evidence`, and semantic role. Weak candidates may explain search but must not become executable selection or strong quick replies without governed confirmation.

The current candidate catalog retries a failed scoped semantic search with an unscoped vector query. Do not interpret unscoped as “global-only”: without an explicit global-scope filter it can include documents from other tenants. Treat this as a platform gap and never reproduce it in new retrieval code.

## Context And Schema

- `GET /api/praxis/config/ai-context/{componentId}` resolves current state through `ui_user_config` user-to-tenant fallback. `POST` uses transient caller state and does not persist it.
- Both paths compose the system component definition, optional template, component state, mode, resource path, and `AiSchemaContext`. Default mode is `edit`; `requireSchema` defaults true only for `create`.
- `/ai-context` does not fetch or populate the schema itself. `schemaContext` is a pointer. Executable authoring resolves the actual structure just in time through `SchemaRetrievalService` and canonical `/schemas/filtered?path=...&operation=...&schemaType=...`.
- Schema retrieval returns typed failures for invalid context, missing base URL, access denial, not found, invalid payload, and transport/unavailable states. Do not replace a failed canonical schema request with `/schemas/catalog`, `api_metadata`, or an inferred local schema.
- The Angular `AiBackendApiService` derives the AI-context base URL from `API_URL.default` unless an explicit gateway override exists. Hosts must supply governed identity headers; demo/local header defaults are not corporate authorization.

## Project Knowledge And Corpus

- Project Knowledge vector publication and retrieval are opt-in derived accelerators. Publish only active, approved, AI-visible concepts backed by active evidence; mask or redact content before indexing.
- Vector hits only rank canonical concept keys. Reload Domain Knowledge rows by tenant/environment, then recheck lifecycle, curation, AI visibility, requested context/resource/kind, and active evidence before projecting influence into a turn.
- Reverted or superseded evidence must be removed from the derived index and must not influence new turns. A stale vector hit without a matching canonical concept/evidence row is discarded.
- Component corpus retrieval requires release/scoped metadata and `aiVisibility=allow`; preserve source id/kind, chunk kind, source pointer, content hash, corpus version, score, and release provenance in diagnostics.

## Consultative Answers

- `artifactKind=api_catalog` is a read-only consultative path. It may combine API candidates with a compact Domain Catalog projection and LLM-authored response, but it must not trigger preview/apply or pretend an unconfirmed domain exists.
- Preserve the structured grounding envelope, candidate APIs, consultative projection, warnings, evidence bundles, retrieval source, scores, scope, release, and elapsed/count diagnostics. Caches are bounded performance aids and must be invalidatable during ingestion verification.
- Resource candidates identify possible operations. Verify the chosen operation through `/schemas/filtered`, actions, surfaces, and capabilities before generating executable configuration.

## Decision Rules

- Treat `api_metadata`, vector documents, project knowledge, domain catalog hints, schemas, and runtime state as evidence for AI/tool grounding.
- Do not answer API catalog questions with hardcoded deterministic prose when LLM/RAG grounding is available.
- Do not use local text search as the primary decision for business resource selection.
- Preserve tenant, environment, release id, version, generatedAt, operationId, schemas, params, tags, scores, content hashes, source pointers, retrieval source, and raw JSON enough for replayable grounding.
- Fail closed when scoped or required grounding is unavailable; do not launder lexical fallback into a selected resource or successful materialization.
- Keep caches performance-only; `api_metadata`, `ai_registry`, runtime metadata, and persisted turn events remain canonical.
- If schema or resource semantics are missing, inspect `praxis-metadata-starter` contracts before inventing config-starter API metadata fields.

## No Keyword Routing

Do not resolve intent, resource, endpoint, schema, field, or API recommendation through labels, aliases, regexes, or local fuzzy matching as the primary decision. Use governed LLM/tool resolution, `api_metadata`, schema contracts, Project Knowledge, Domain Catalog, declared tools, and candidate provenance for grounding; textual matching may only rank candidates after semantic scope is established.

## Aderence Inventory

Before adding API metadata fields, context blocks, RAG metadata keys, candidate diagnostics, cache semantics, or context endpoints, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real gaps justify new public grounding contracts. Identify source owner, downstream assistant/runtime consumers, generated AI contracts, docs, quickstart smokes, and minimum validation.

## Validation

Use focused local gates:

- ingestion/context: `mvn "-Dtest=ApiMetadataIngestionServiceTest,AiContextControllerTest,ContextRetrievalServiceTest,SchemaRetrievalServiceTest" test`
- resource/project knowledge grounding: `mvn "-Dtest=AgenticAuthoringApiMetadataCandidateCatalogTest,AgenticAuthoringResourceDiscoveryServiceTest,AgenticAuthoringProjectKnowledgeServiceTest,VectorRankedProjectKnowledgeCandidateRetrieverTest" test`
- RAG/vector changes: `mvn "-Dtest=RagVectorStoreServiceTest,RagVectorStoreConfigurationTest,RagProjectKnowledgeMetadataTest,RagProjectKnowledgeDerivedIndexServiceTest" test`
- Angular AI-context consumer: `npm run test:praxis-ai:backend-api`

Review `docs/ai/**`, `docs/domain-catalog/**`, API contract docs, quickstart ingestion/smoke scripts, and Angular AI context consumers when public grounding changes.

## Companion Skills

- Use `praxis-metadata-schema-contracts` when grounding depends on backend resource schema semantics.
- Use `praxis-config-runtime-persistence` when `/ai-context` GET state resolution or tenant/user/environment config behavior changes.
- Use `praxis-ai-backend-config-contracts` when Angular endpoint resolution or identity headers change.
- Use `praxis-config-agentic-authoring-streaming` when candidates feed intent resolution, turn stream, quick replies, or terminal diagnostics.
- Use `praxis-config-domain-decisions` when grounding should route to shared rule/knowledge authoring.
- Use `praxis-api-quickstart-cockpit-http-validation` for downstream proof of domain catalog ingest, API catalog grounding, Project Knowledge, and HTTP examples.
- Use `praxis-ai-semantic-intent` for Angular assistant consult/edit boundaries.
