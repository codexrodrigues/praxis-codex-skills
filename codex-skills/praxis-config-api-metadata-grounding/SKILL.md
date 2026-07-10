---
name: praxis-config-api-metadata-grounding
description: Use when Codex must work on praxis-config-starter API metadata and grounding: api_metadata, /api/praxis/config/api-catalog/ingest, /api/praxis/config/ai-context/**, ApiMetadataIngestionService, schema/context retrieval, RAG vector store, project knowledge, component corpus retrieval, candidate resources, API Catalog Q&A, and grounding diagnostics.
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
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringApiMetadataCandidateCatalog.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringResourceDiscoveryService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringProjectKnowledgeService.java`
- `src/main/java/org/praxisplatform/config/rag/**`
- `src/main/resources/db/migration/V4__create_api_metadata.sql`, `V8__create_api_metadata_embedding_index.sql`, and vector-store migrations.
- focused API metadata, context, RAG, project knowledge, and resource discovery tests.

## Canonical Boundary

`/api/praxis/config/api-catalog/ingest` stores normalized API metadata and publishes derived vector-store documents for retrieval. `/api/praxis/config/ai-context/**` composes component state, templates, schema hints, runtime config, and grounding context for AI authoring.

API Catalog Q&A should be an informative grounded answer path. It should not start `page-preview`, require executable resource clarification, or apply configuration until a later turn chooses an executable authoring route.

## Decision Rules

- Treat `api_metadata`, vector documents, project knowledge, domain catalog hints, schemas, and runtime state as evidence for AI/tool grounding.
- Do not answer API catalog questions with hardcoded deterministic prose when LLM/RAG grounding is available.
- Do not use local text search as the primary decision for business resource selection.
- Preserve tenant, environment, release id, version, generatedAt, operationId, schemas, params, tags, and raw JSON enough for replayable grounding.
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

- ingestion/context: `mvn "-Dtest=ApiMetadataIngestionServiceTest,AiContextControllerTest,AiContextServiceTest,ContextRetrievalServiceTest,SchemaRetrievalServiceTest" test`
- resource/project knowledge grounding: `mvn "-Dtest=AgenticAuthoringApiMetadataCandidateCatalogTest,AgenticAuthoringResourceDiscoveryServiceTest,AgenticAuthoringProjectKnowledgeServiceTest,VectorRankedProjectKnowledgeCandidateRetrieverTest" test`
- RAG/vector changes: `mvn "-Dtest=RagVectorStoreServiceTest,RagVectorStoreConfigurationTest,RagProjectKnowledgeMetadataTest,RagProjectKnowledgeDerivedIndexServiceTest" test`

Review `docs/ai/**`, `docs/domain-catalog/**`, API contract docs, quickstart ingestion/smoke scripts, and Angular AI context consumers when public grounding changes.

## Companion Skills

- Use `praxis-metadata-schema-contracts` when grounding depends on backend resource schema semantics.
- Use `praxis-config-agentic-authoring-streaming` when candidates feed intent resolution, turn stream, quick replies, or terminal diagnostics.
- Use `praxis-config-domain-decisions` when grounding should route to shared rule/knowledge authoring.
- Use `praxis-api-quickstart-cockpit-http-validation` for downstream proof of domain catalog ingest, API catalog grounding, Project Knowledge, and HTTP examples.
- Use `praxis-ai-semantic-intent` for Angular assistant consult/edit boundaries.
