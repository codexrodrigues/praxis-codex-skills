---
name: praxis-ai-backend-config-contracts
description: Use when changing or reviewing `AiBackendApiService`, `AI_BACKEND_CONFIG_STORE`, `AI_BACKEND_STORAGE_OPTIONS`, `AI_BACKEND_ENDPOINTS`, `API_URL` endpoint resolution, `/api/praxis/config/ai/**`, `/api/praxis/config/ai-context/**`, provider catalog/model/test/status endpoints, AI config snapshots, headers, ETag-adjacent identity, risk confirmation policy, manifest endpoints, or backend AI contract integration.
---

# Praxis AI Backend Config Contracts

Use this skill for the Angular client boundary to Praxis Config AI services. The canonical provider execution and persisted AI configuration live behind Praxis Config endpoints, not inside browser UI or component libraries.

## Canonical Boundary

- `praxis-config-starter` is the canonical backend boundary for AI registry, provider/model execution, persisted AI config, templates, headers, and governed AI endpoints under `/api/praxis/config/**`.
- `AiBackendApiService` is the official Angular HTTP client for `/praxis/config/ai/**` and `/praxis/config/ai-context/**` materialized through configured base URLs.
- `AI_BACKEND_CONFIG_STORE` bridges host-owned AI config snapshots and save operations.
- `AI_BACKEND_STORAGE_OPTIONS` supplies tenant/env/user headers and optional local demo identity fallback.
- `AI_BACKEND_ENDPOINTS` may override AI and AI-context base URLs only when AI orchestration is served by a distinct gateway.
- `API_URL.default.baseUrl` is the preferred host-level source when endpoints share the platform API origin.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `projects/praxis-ai/README.md`
- `src/lib/core/services/ai-backend-api.service.ts`
- `src/lib/core/services/ai-backend-api.service.spec.ts`
- `src/lib/core/contracts/ai-contract.generated.ts`
- `src/lib/core/models/ai-models.ts`
- `src/public-api.ts`
- host provider setup for `API_URL` and `AI_BACKEND_*` tokens
- relevant `praxis-config-starter` AI registry/config endpoint contracts when backend behavior changes

Use `praxis-ai-authoring-manifests` for component manifest endpoints and edit-plan shape. Use `praxis-ai-turn-orchestration-transport` for turn stream conversion.

When backend contract behavior is in scope, load the relevant config-starter skill before changing Angular client DTOs or endpoint fallbacks:

- `praxis-config-runtime-persistence` for `/api/praxis/config/ui`, headers, ETag, and `/api/praxis/runtime/**`.
- `praxis-config-ai-registry-manifests` for `ai_registry`, templates, component definitions, manifest endpoints, validators, and compilers.
- `praxis-config-api-metadata-grounding` for `api_metadata`, AI context, RAG, Project Knowledge, and resource candidates.
- `praxis-config-agentic-authoring-streaming` for `/api/praxis/config/ai/**`, turn streams, quick replies, diagnostics, start/probe/replay/cancel, and terminal events.
- `praxis-config-domain-decisions` for domain rules, domain knowledge, publications, materializations, and governed decision diagnostics.

## Endpoint Rules

- Resolve AI base URL in this order: explicit `AI_BACKEND_ENDPOINTS.aiBaseUrl`, derived `API_URL.default.baseUrl + praxis/config/ai`, fallback `/api/praxis/config/ai`.
- Resolve AI context base URL in this order: explicit `AI_BACKEND_ENDPOINTS.aiContextBaseUrl`, derived `API_URL.default.baseUrl + praxis/config/ai-context`, fallback `/api/praxis/config/ai-context`.
- Do not hardcode external provider URLs in `@praxisui/ai`. Provider catalog, model listing, status, test calls, suggestions, patches, stream start/connect/cancel, observation feedback, and authoring manifest operations go through the Praxis Config boundary.
- Preserve generated contract version and schema hash headers for patch/orchestrator contracts.
- Preserve tenant/user/env headers from `AI_BACKEND_STORAGE_OPTIONS`. Local identity fallback is for demos/local hosts and must be explicit.
- Stream connections must respect `withCredentials`, access tokens, probe endpoints, and explicit headers. Fetch fallback is required when EventSource cannot carry needed headers.
- Risk confirmation policy is contract-owned. Frontend can display and require confirmation, but should not downgrade risk locally.

## Inventory Before New Contracts

Before adding a token, endpoint, DTO, or exported type, answer: what does the platform already know but this client, host, or UX is not materializing correctly?

Classify each gap:

- `ja-suportado-so-ux`: endpoint or token already exists; only host wiring or UX needs correction.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: existing field/endpoint is present but projected poorly.
- `suportado-parcialmente`: backend has evidence but client normalization or generated contract is incomplete.
- `lacuna-real-de-contrato`: backend cannot provide the required governed behavior without a new canonical contract.

Only `lacuna-real-de-contrato` justifies a new public contract. Identify backend owner, consumers, generated artifacts, docs/examples, and focal validation.

## Validation

Use focused checks:

- client endpoints, headers, base URL resolution, streams: `ai-backend-api.service.spec.ts`
- turn stream behavior: `agentic-authoring-turn-client.service.spec.ts`
- generated AI contracts: contract generation/validator specs when schema changes
- public exports: build `praxis-ai` and a direct consumer when `public-api.ts` changes
- backend endpoint behavior: focused `praxis-config-starter` tests when backend contracts change

State explicitly when no `praxis-config-starter`, public docs, examples, registry, or generated contract artifacts need updates.
