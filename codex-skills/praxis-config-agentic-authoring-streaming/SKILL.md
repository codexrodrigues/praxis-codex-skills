---
name: praxis-config-agentic-authoring-streaming
description: Use when implementing, reviewing, debugging, or validating praxis-config-starter semantic intent resolution, pre-intent planning, declared tools and tool loops, consult/edit routing, preview/repair/apply governance, runtime observation grounding, quick replies and active semantic decisions, authoring turn SSE, event-log replay, heartbeat, timeout, cancellation, stream identity/security, or legacy AI orchestrator and patch-stream migration.
---

# Praxis Config Agentic Authoring Streaming

Use this skill for the canonical backend execution path from a governed assistant turn to a
consultative answer or reviewed semantic materialization. This boundary resolves intent, gathers
backend-owned evidence, declares tools, validates preview/apply, and transports the result. It must
not convert prompt text directly into executable component or domain changes.

## Source Audit

Inspect `praxis-config-starter/AGENTS.md`, then the boundary being changed:

- public surface: `AgenticAuthoringController`, `AiPatchStreamController`,
  `docs/ai/agentic-authoring-streaming.md`, `docs/ai/contracts/**`;
- turn lifecycle: `AgenticAuthoringTurnStreamService`, `AgenticAuthoringTurnEngine`,
  `AiTurnEventService`, `AiTurnEvent`, `AiTurnEventRepository`, `AiThreadService`, `AiTurnService`,
  `AiStreamAccessTokenService`, and `AiTurnEventEnvelope`;
- semantic resolution: `AgenticAuthoringIntentResolverService`,
  `AgenticAuthoringLlmIntentResolverService`, candidate eligibility/provenance, semantic decision,
  route classification, conversation continuation, and materialization policy;
- tools and evidence: `AgenticAuthoringLlmPreIntentToolPlanningService`,
  `AgenticAuthoringToolRegistry`, `AgenticAuthoringToolLoopExecutor`, API metadata/domain catalogs,
  Project Knowledge, manifest slices, presentation affordances, runtime component grounding, and
  `AgenticAuthoringConsultativeAnswerService` runtime-related surface planning;
- materialization: plan, preview, repair classification, compiler, apply service, and ETag-backed
  `UserConfigService` persistence;
- legacy paths: `AiOrchestratorService`, `AiOrchestratorController`, `AiStreamService`, and patch SSE.

Inspect the Angular consumer with `praxis-ai-turn-orchestration-transport`:

- `projects/praxis-ai/src/lib/core/services/agentic-authoring-turn-client.service.ts`;
- backend API transport, generated contracts, assistant turn models, quick-reply utilities;
- Page Builder turn flow and focused specs when preview/apply behavior changes.

## Canonical Turn Flow

Preserve this sequence:

`principal + session/clientTurn identity + conversation + safe context`
`-> ground runtime observations as untrusted evidence`
`-> optional LLM-authored pre-intent tool plan`
`-> governed read-only evidence tools`
`-> LLM semantic intent + backend candidate eligibility/provenance`
`-> explicit route: consult | clarify | preview | governed handoff`
`-> plan -> compile -> preview -> optional bounded repair -> reviewed result`
`-> separate apply with semantic materialization validation + If-Match`

The backend may use deterministic policy after semantic scope is resolved to validate candidates,
reconcile canonical IDs, rank evidence, enforce route classes, compile declared effects, or block a
turn. That policy is not permission to infer primary intent from words.

Keep consult and edit distinct:

- consult returns grounded `assistantContent`/message and no executable patch;
- clarification returns structured questions or quick replies and no apply authorization;
- preview returns a governed materialization plus diagnostics and `canApply` only after all gates;
- apply revalidates the semantic decision against the compiled materialization, persists through the
  canonical config service, and respects scope, tenant/user/environment, ETag, and sanitization;
- shared-rule/domain-decision intent hands off to `praxis-config-domain-decisions`; it must not be
  flattened into component configuration.

## Semantic Intent Rules

Primary intent must be resolved by LLM/tooling over governed context, manifests, metadata schemas,
surfaces, actions, capabilities, domain catalogs, active semantic decisions, and declared tools.

- Do not add keyword, regex, alias, normalized-prompt, localized-label, fuzzy, or command-string
  routing for consult/edit, operation kind, artifact kind, route class, target, or tool execution.
- `AgenticAuthoringKeywordFallbackResolver` and deterministic fast paths are migration debt. Do not
  extend them. A provider failure or unresolved LLM result must clarify or fail closed; lexical output
  may provide non-executable diagnostics, never `canMaterialize`, preview authorization, or apply.
- Candidate matching is allowed only after semantic scope. Preserve provenance such as semantic
  retrieval, domain catalog, tool result, explicit canonical path, context hint, or lexical fallback.
  Weak/lexical candidates remain under review even if a technical preview happens to compile.
- Frontend `contextHints`, runtime observations, conversation text, quick-reply labels, and historical
  diagnostics are evidence, not permissions or semantic decisions.
- An `activeSemanticDecision` is accepted only as a structured backend-issued continuation and must
  be reconciled against current principal, thread, context, candidates, policy, and expiry.
- Missing tool or operation means model the canonical tool/manifest/decision contract. Do not add a
  text fast path.

## Tool Governance

Tools are explicit backend contracts with schemas, principal context, safe diagnostics, bounded
results, and deterministic failure codes. A tool result grounds a decision; it does not decide the
primary intent by itself.

- Pre-intent planning is LLM-authored and optional. Provider failure skips/fails the plan safely; it
  must not trigger keyword-selected tools.
- Enforce tool allowlists, phase eligibility, step budgets, maximum calls, projection/redaction
  policies, and fail-closed aggregation.
- Runtime component observations must declare
  `untrusted_frontend_observation`; copy only allowlisted identities/digests and reconcile reads with
  backend schemas, resource paths, actions, surfaces, relation mappings, and principal scope.
- Backend policy alone may enable runtime read tools or multi-tool execution. Frontend policy hints
  cannot increase budgets or authorize reads.
- If any multi-read step fails, do not publish partial aggregate evidence as a successful result.
- Keep tool traces and evidence bundles sanitized: no API keys, raw rows, secrets, unrestricted
  payloads, internal prompts, or unbounded provider output.

## Stream Contract

The canonical authoring family is:

- `POST /api/praxis/config/ai/authoring/turn/stream/start`;
- `GET /api/praxis/config/ai/authoring/turn/stream/{streamId}`;
- `GET /api/praxis/config/ai/authoring/turn/stream/{streamId}/probe`;
- `POST /api/praxis/config/ai/authoring/turn/stream/{streamId}/cancel`.

It reuses `AiTurnEventEnvelope`: `eventId`, `eventSchemaVersion`, `threadId`, `turnId`, `streamId`,
monotonic persisted `seq`, timestamp, type, and payload. Payloads may differ from legacy patch SSE;
do not create another envelope.

Preserve these invariants:

- `clientTurnId` provides idempotent start identity. Reuse is valid only when the canonical request
  fingerprint matches; a different request with the same ID must conflict rather than replay stale work.
- The request fingerprint is a backend hash over material authoring inputs: prompt, target, route,
  current page, conversation/clarification/attachments, context hints, capabilities, safe diagnostics,
  and active semantic decision. It must exclude `apiKey`, raw runtime observations, and
  `requestBaseUrl`; runtime observations influence the hash only after backend grounding into safe
  `contextHints.groundedRuntimeComponentContext`.
- On start, the backend may reuse an explicit `activeSemanticDecision` from the request or the latest
  authorized result event on the same thread. Reconcile that decision into the effective request before
  hashing and processing; do not trust a frontend-only continuation without backend lineage.
- New starts reserve capacity before processing and append the first persisted `status` event with
  phase `context.bundle`, `requestHash`, `expiresAt`, and the active semantic decision id when present.
- `status`, `thought.step`, tool progress, and `intent.resolved` are non-terminal and replay-safe.
- Only persisted `result`, `error`, or `cancelled` events terminate the turn. Heartbeats are transient
  liveness signals and cannot advance the persisted cursor.
- `heartbeat` is out-of-band keep-alive: it may use `seq=-1` and no `eventId`, derives `phase` and
  user-facing `summary` from the latest known event, and must not be counted as execution evidence.
- Long-running progress is persisted as `status` from the backend processing watchdog only when the
  observed tail is still latest. Preserve `streamEventDiagnostics` (`schemaVersion`,
  `dedupeKey`, `eventUniquenessKey`, `technicalDuplicate`, `replaySafe`,
  `duplicatesDoNotIndicateExecution`) so clients can group technical duplicates without inferring
  extra tool calls or semantic phases.
- `Last-Event-ID` replays only later events from the same stream and authorized principal scope.
- Ownership includes tenant, user, environment, thread, and turn. Cookie and signed-URL token modes
  must enforce the same scope on connect, probe, cancel, and replay.
- Timeout/cancel wins races against late preview or result; no event may append after a terminal event.
- Start reservation and event sequence allocation must remain safe across instances, not only inside
  one JVM.
- Bound active streams globally and per tenant/user, executor queues, emitter lifetime, replay polling,
  heartbeat tasks, processing timeout, payload size, and event retention.
- Error/timeout payloads expose stable public codes and safe user-facing text, not stack traces,
  provider secrets, prompts, or unsanitized exception content.
- Signed URL stream mode issues encrypted `enc1.*` tokens scoped to stream id, tenant, user,
  optional environment, and effective expiry. The token secret must be at least 32 bytes, legacy
  signed token parsing stays disabled unless explicitly enabled, and connect/probe/cancel must enforce
  the same scope as cookie mode.
- `fallbackAuthoringUrl` and legacy synchronous authoring fallbacks are migration bridges for clients
  that do not yet consume SSE. They are not alternate authorization paths: they must preserve the same
  tenant/user/environment scope, semantic decision governance, preview/apply gates, and fail-closed
  behavior for auth, probe, expiry, terminal, and stale-turn failures.

Treat `/ai/patch/stream/**` and `AiOrchestratorService` as legacy migration surfaces. Preserve
contract compatibility while consumers move to authoring turns, but do not add new agentic semantics
there or make one legacy barrel define the canonical behavior.

## Runtime Related Surface Grounding

Runtime related surface features are consultative grounding over backend-reconciled runtime context,
not a shortcut around semantic intent or authorization.

- `runtimeComponentObservations` are accepted only through the
  `untrusted_frontend_observation` boundary and become safe
  `groundedRuntimeComponentContext`; raw rows, sample rows, data sources, secrets, and frontend
  action decisions must not be copied into turn authority.
- `runtimeToolPlan` must publish `schemaVersion=praxis-runtime-tool-plan.v1`, backend-owned planner
  metadata, step budget, projection/redaction policy refs, and
  `multiToolAuthorization.source=backend_policy`.
- Treat `runtime.tool-plan.*` stream phases as replay-safe technical projections, not execution
  counters. Do not count repeated SSE phases, heartbeats, or `technicalDuplicate` diagnostics as
  extra reads or tools; audit execution through `runtimeToolPlan.steps[]`,
  `runtimeToolPlan.budget.usedToolCalls`, `runtimeRelatedSurfaceReads[]`, aggregate status, and
  `streamEventDiagnostics.dedupeKey`/`eventUniquenessKey`.
- Keep `steps[]`, `candidateSteps[]`, and `blockedSteps[]` as sibling arrays. `candidateSteps[]`
  ranks possible reads without authorizing execution; `blockedSteps[]` explains fail-closed cases.
- Default beta policy is conservative: read-free availability/disambiguation, or a single governed
  read only when backend policy and target reconciliation allow it. Multi-read execution requires an
  explicit backend policy such as `runtime-tool-policy:multi-tool-readonly-beta`.
- `runtime-tool-policy:multi-tool-dry-run-beta` is planning authority only. It may publish multiple
  `candidateSteps[]`, dry-run aggregation policy, and execution diagnostics, but must keep
  `budget.maxToolCalls=0`, `steps[]=[]`, `runtimeRelatedSurfaceReads[]=[]`,
  `backendReadsPerformed=false`, and no real aggregate summary/detail/compare evidence.
- Targeted detail/list/summary must be driven by semantic decision fields
  `DETAIL_TARGET_SURFACE_REF`, `LIST_TARGET_SURFACE_REF`, or `SUMMARY_TARGET_SURFACE_REF`, then
  reconciled against accepted runtime candidates before any HTTP read.
- `runtimeRelatedSurfaceResolution.*Target` should declare `source=semantic_decision`,
  `provenance=backend_reconciled`, read mode, aggregation policy, candidate refs, and failure
  diagnostics. Forged, missing, ambiguous, stale, or divergent targets block before backend reads.
- `resourcePath` alone is not runtime surface identity when multiple accepted surfaces can share it.
  If composition publishes `runtimeSurfaceInstanceRef` or `targetRuntimeSurfaceInstanceRef`, that ref
  governs target selection. Without it, a reconciled `targetWidget` may disambiguate; without either,
  block with ambiguity diagnostics instead of choosing the first matching resource.
- Backend target-candidate resolution may rank sanitized `surfaceRef`, `candidateRef`,
  `runtimeSurfaceInstanceRef`, labels, and semantic aliases only after a targetable intent has been
  semantically resolved. It must not decide the primary intent from prompt text.
- Disambiguation quick replies must carry a backend-issued `semanticDecision.constraints`
  `runtimeRelatedSurfaceDisambiguationSelection` with `optionRef`, `candidateRef`, and `surfaceRef`.
  Clients resend that decision as `activeSemanticDecision`; they must not reconstruct refs from labels
  or treat diagnostic context as authority.
- Historical `runtimeRelatedSurfaceDisambiguationContext` is read-free grounding only. It must carry
  session/page/source turn/TTL metadata and be discarded when expired, cross-session, same-client-turn,
  or no longer reconcilable against current candidates.
- Terminal evidence may include sanitized `runtimeConsultableContext`,
  `runtimeRelatedSurfaceReads[]`, runtime summary/detail/list resolution, and runtime tool diagnostics.
  It must preserve `rawRuntimeValuesCopied=false` when records are projected by allowlist.
- Runtime summary, detail, list, and compare evidence must derive only from sanitized
  `runtimeRelatedSurfaceReads[]` and their projection/redaction metadata. Do not copy
  `sampleRows`, `rawRows`, `dataSource`, hidden values, sensitive scalars, or raw frontend
  observation payloads into tool-plan events, terminal evidence, assistant text, or aggregate facts.
- Runtime compare must stay `compare_planning_only` until a comparison dimension is accepted. The
  accepted dimension must come from `COMPARISON_DIMENSION_FIELD` in the semantic decision or from
  backend-owned unique-dimension inference over reconciled surface contracts, with
  `provenance=backend_reconciled` and non-sensitive/common field coverage. Frontend hints,
  prompt labels, omitted/redacted fields, ambiguous common fields, or sensitive dimensions block
  before reads and must not emit `runtimeRelatedSurfaceCompare`.

## Quick Replies And Diagnostics

- Quick replies that choose an operation, resource, surface, or clarification must carry structured
  `semanticDecision`, `canonicalAction`, `contextHints`, `value`, presentation, and diagnostics.
- Labels/prompts are display copy and cannot be parsed back into authority.
- Persist semantic decisions only in the authorized event/thread lineage; stale choices must not leak
  into a new session, page, principal, or incompatible runtime context.
- `intent.resolved` exposes safe understanding, route, evidence refs, required tools, confidence, and
  fallback status. It does not authorize apply and must not be treated as terminal by clients.
- Keep `llmDiagnostics`, thought steps, tool traces, observations, and replay audit opt-in, bounded,
  sanitized, and clearly separate from public assistant content.

## Aderence Inventory

Before adding event types, stream fields, routes, tools, policies, diagnostics, context hints, quick
replies, decision fields, preview/apply payloads, or endpoint variants, ask what the platform already
knows and classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` permits a public contract change. Name the missing evidence, canonical
owner, security/storage impact, Angular consumers, generated OpenAPI/types, docs/examples, quickstart
smoke, backward compatibility, and minimum proof.

## Validation

Use the smallest local gate that proves the boundary:

- semantic intent, pre-intent planning, tools, candidates, and decision policy:
  `mvn "-Dtest=AgenticAuthoringIntentResolverServiceTest,AgenticAuthoringLlmIntentResolverServiceTest,AgenticAuthoringLlmPreIntentToolPlanningServiceTest,AgenticAuthoringToolRegistryTest,AgenticAuthoringToolLoopExecutorTest,AgenticAuthoringCandidateProvenancePolicyTest,AgenticAuthoringSemanticDecisionPolicyTest" test`
- turn engine, runtime grounding, preview/repair/apply, and stream lifecycle:
  `mvn "-Dtest=AgenticAuthoringTurnEngineTest,AgenticAuthoringTurnStreamServiceTest,AgenticAuthoringRuntimeComponentGroundingServiceTest,AgenticAuthoringPreviewServiceTest,AgenticAuthoringApplyServiceTest,AiTurnEventServiceTest" test`
- HTTP/SSE/security and legacy compatibility:
  `mvn "-Dtest=AgenticAuthoringControllerTest,AgenticAuthoringTurnStreamHttpSseIntegrationTest,AgenticAuthoringTurnStreamSecurityChainIntegrationTest,AgenticAuthoringTurnStreamSignedTokenIntegrationTest,AiStreamAccessTokenServiceTest,AiPatchStreamControllerTest,AiProviderStreamingFallbackAndCancelIntegrationTest,AiOrchestratorControllerTest,AiOrchestratorService*Test" test`
- persisted HTTP/SSE and security-chain integration, when the owner context is healthy:
  `mvn "-Dtest=AgenticAuthoringTurnStreamHttpSseIntegrationTest,AgenticAuthoringTurnStreamSecurityChainIntegrationTest,AgenticAuthoringTurnStreamSignedTokenIntegrationTest,AiPatchStreamHttpSseIntegrationTest,AiPatchStreamSecurityChainIntegrationTest" test`;
  if unrelated auto-configuration prevents startup, record the owner test-infrastructure gap instead
  of presenting controller/unit tests as end-to-end security proof;
- public contract changes:
  `mvn "-Dtest=AiApiContractOpenApiTest,AiContractSpecConsistencyTest,AiContractV11RetroCompatibilityTest" test`
- Angular consumer changes: focused authoring turn client, backend API, orchestrator, shell, and Page
  Builder turn-flow specs with `praxis-ai-turn-orchestration-transport`.

Audit happy paths plus provider failure, unresolved/ambiguous intent, forged/stale semantic decision,
keyword-only prompt, unsupported tool, tool budget exhaustion, partial multi-tool failure, untrusted
observation escalation, duplicate `clientTurnId` with changed payload, cross-principal replay,
invalid/foreign `Last-Event-ID`, reconnect after terminal, timeout/result race, cancel/result race,
stale ETag, and semantic materialization mismatch.

Do not count disabled host-specific tests as starter coverage. Move retained domain scenarios to the
quickstart/domain catalog owner, rewrite generic invariants without host vocabulary, and delete
obsolete lexical-fallback expectations with traceable replacement evidence.

Use quickstart HTTP/SSE and Page Builder E2E only for cross-project or release proof. Run local gates
first and reserve GitHub Actions for the final phase/release gate.

## Derived Artifacts

After a public change, review OpenAPI and generated Angular contracts, `docs/ai/**`, quickstart HTTP/SSE
smokes, `praxisui-http-examples`, Page Builder recipes/E2E, public landing examples, and stream auth
configuration. State explicitly when each family is unaffected.

## Companion Skills

- `praxis-ai-semantic-intent`: shared semantic-routing rules and frontend red flags.
- `praxis-config-ai-registry-manifests`: executable component operations, validators, and compilers.
- `praxis-config-api-metadata-grounding`: API metadata, schemas, RAG, Project Knowledge, and candidates.
- `praxis-config-domain-decisions`: governed business-rule authoring and materialization.
- `praxis-config-runtime-persistence`: config scope, ETag, and persisted apply behavior.
- `praxis-ai-turn-orchestration-transport`: Angular stream/event/lifecycle consumption.
- `praxis-ai-composer-attachments-quick-replies`: structured clarification and quick-reply semantics.
- quickstart, HTTP examples, Page Builder, and landing skills for downstream operational/public proof.
