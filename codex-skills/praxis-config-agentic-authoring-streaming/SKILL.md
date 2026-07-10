---
name: praxis-config-agentic-authoring-streaming
description: Use when Codex must work on praxis-config-starter agentic authoring backend: AiOrchestratorService, AgenticAuthoringController, AgenticAuthoringTurnStreamService, AgenticAuthoringTurnEngine, semantic intent resolution, declared tools, pre-intent tool planning, dry-run, plan, compile, preview, apply, SSE start/connect/probe/replay/cancel, AiTurnEventEnvelope, terminal events, quick replies, diagnostics, warnings, and observations.
---

# Praxis Config Agentic Authoring Streaming

Use this skill for the backend agentic authoring execution path in `praxis-config-starter`. This is the canonical backend boundary for semantic intent resolution, declared tools, validation, preview, apply, event streaming, replay, cancellation, and diagnostics.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `docs/ai/agentic-authoring-streaming.md`
- `docs/ai/contracts/README.md`
- `src/main/java/org/praxisplatform/config/controller/AgenticAuthoringController.java`
- `src/main/java/org/praxisplatform/config/controller/AiOrchestratorController.java`
- `src/main/java/org/praxisplatform/config/controller/AiPatchStreamController.java`
- `src/main/java/org/praxisplatform/config/service/AiOrchestratorService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringIntentResolverService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringLlmIntentResolverService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringTurnEngine.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringTurnStreamService.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringToolRegistry.java`
- `src/main/java/org/praxisplatform/config/ai/authoring/AgenticAuthoringPreIntentToolPlanningService.java`
- focused controller, intent, turn engine, stream, tool, and contract tests.

## Canonical Boundary

The preferred execution flow is:

`governed context + semantic catalogs + declared tools + LLM/tool resolution -> validated route -> plan/compile/preview -> reviewed apply -> persisted config/domain decision`

The stream family uses `AiTurnEventEnvelope`, `eventSchemaVersion`, `threadId`, `turnId`, `streamId`, `seq`, replay, heartbeat, ownership checks, cancellation, and terminal `result`, `error`, or `cancelled` events.

## Decision Rules

- Prefer semantic intent resolution and declared tools over deterministic fast paths.
- `intent.resolved` is replay-safe and non-terminal; clients finish only on terminal events.
- Provider failure, timeout, broad resource discovery, or missing grounding must fail closed with clarification/diagnostics, not promote lexical fallback to executable apply.
- Runtime observations are untrusted frontend evidence. Sanitize and ground them before using them; never promote them to permissions, capabilities, raw data, or action execution.
- Quick replies that represent semantic decisions must preserve `semanticDecision`, `contextHints`, canonical action, presentation, and diagnostics.
- Keep `start`, `probe`, stream connect, replay via `Last-Event-ID`, cancel, processing timeout, heartbeat, and event log aligned.
- If a needed tool is absent, model the canonical tool/contract. Do not replace it with text routing.

## No Keyword Routing

Do not route primary user intent through keywords, regexes, command words, aliases, normalized prompt strings, or deterministic fast paths. Local textual heuristics may only rank or disambiguate candidates after the semantic route is resolved by LLM/tooling, governed context, declared manifests, catalogs, capabilities, and active semantic decisions. Any fallback must be narrow, tested, fail-closed, and described as non-primary.

## Aderence Inventory

Before adding events, stream fields, DTOs, tools, validators, route classes, quick replies, diagnostics, preview/apply payloads, or contract docs, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real gaps justify a new public AI/stream contract. Name missing evidence, canonical owner, Angular consumers, generated contracts, docs, quickstart smoke impact, and validation.

## Validation

Use focused local gates:

- intent/tool/turn: `mvn "-Dtest=AgenticAuthoringIntentResolverServiceTest,AgenticAuthoringLlmIntentResolverServiceTest,AgenticAuthoringToolRegistryTest,AgenticAuthoringToolLoopExecutorTest,AgenticAuthoringTurnEngineTest" test`
- stream/controller: `mvn "-Dtest=AgenticAuthoringControllerTest,AgenticAuthoringTurnStreamServiceTest,AiPatchStreamControllerTest,AiPatchStreamHttpSseIntegrationTest,AiProviderStreamingFallbackAndCancelIntegrationTest" test`
- orchestrator legacy path: `mvn "-Dtest=AiOrchestratorControllerTest,AiOrchestratorService*Test" test`
- contract docs: `mvn "-Dtest=AiApiContractOpenApiTest,AiContractSpecConsistencyTest,AiContractV11RetroCompatibilityTest" test`

For release or end-to-end authoring changes, use the quickstart HTTP/SSE smoke from `RELEASING.md`; reserve GitHub Actions for phase/release gates after local proof.

## Companion Skills

- Use `praxis-config-ai-registry-manifests` for executable manifests, validators, compilers, and registry projections.
- Use `praxis-config-api-metadata-grounding` for API metadata, RAG, Project Knowledge, and resource candidate grounding.
- Use `praxis-config-domain-decisions` when route class or quick reply should move into shared-rule/domain-knowledge authoring.
- Use `praxis-api-quickstart-operational-proof`, `praxis-api-quickstart-security-config`, and `praxis-api-quickstart-cockpit-http-validation` for downstream HTTP/SSE proof in the reference host.
- Use `praxis-ai-turn-orchestration-transport` for Angular stream transport and assistant state.
- Use `praxis-page-builder-ai-agentic` for Page Builder cockpit consumption.
