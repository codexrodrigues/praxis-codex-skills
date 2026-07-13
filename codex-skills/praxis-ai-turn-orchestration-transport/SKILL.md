---
name: praxis-ai-turn-orchestration-transport
description: Use when implementing, auditing, or debugging Praxis Angular assistant turn orchestration, `PraxisAssistantTurnOrchestratorService`, flow controllers, session/client turn identity, runtime observation evidence, clarifications, review/apply/cancel/retry/edit/resend state, `AgenticAuthoringTurnClientService`, generated authoring-turn contracts, or SSE/fetch stream lifecycle and terminal handling.
---

# Praxis AI Turn Orchestration And Transport

Use this skill for the Angular boundary that materializes a backend-governed assistant turn. `@praxisui/ai` owns interaction state, safe request assembly, HTTP/SSE transport, and rendering of the resolved result. It does not infer primary intent, authorize a patch, or recreate backend policy in the browser.

## Canonical Flow And Owners

```text
shell/composer action
  -> PraxisAssistantTurnOrchestratorService / PraxisAssistantTurnFlow
  -> AgenticAuthoringTurnClientService
  -> AiBackendApiService + generated contract
  -> Praxis Config authoring-turn start, stream, probe, cancel
  -> validated event envelopes
  -> turn result and shell state
```

| Owner | Responsibility |
| --- | --- |
| `PraxisAssistantTurnOrchestratorService` | creates/forks local turn state; assembles request; guards against stale flow results; resets abandoned review/clarification state |
| `PraxisAssistantTurnFlow` | mode-specific submit, apply, cancel, and retry behavior; no duplicate semantic routing |
| `AgenticAuthoringTurnClientService` | starts the canonical stream, collects optional observations, converts lifecycle/events to `PraxisAssistantTurnResult`, and enforces client timeouts |
| `AiBackendApiService` | authenticated headers, normalized IDs, start/probe/connect/cancel endpoints, EventSource/fetch selection, runtime envelope validation, and stream cleanup |
| `praxis-config-starter` | semantic intent, tools, eligibility, preview/apply policy, persisted event lineage, auth, replay, and terminal authority |

Read `projects/praxis-ai/AGENTS.md`, workspace `AGENTS.md`, and `codex-rules.md` before Angular edits. Inspect `praxis-config-starter/AGENTS.md` and use `praxis-config-agentic-authoring-streaming` whenever server event semantics, authorization, replay, tools, or materialization change.

## Required Inventory

Inspect the source and its focused specs together:

- `core/models/assistant-turn.models.ts` and `core/contracts/ai-contract.generated.ts`;
- `assistant-turn-orchestrator.service.ts` and `.spec.ts`;
- `agentic-authoring-turn-client.service.ts` and `.spec.ts`;
- `ai-backend-api.service.ts` and `.spec.ts`;
- affected flow/controller, `assistant-shell` types/spec, and `ai-assistant` stream consumer when the older surface is involved;
- when backend turn transport, event lineage, replay, security, or terminal semantics are involved, inspect `praxis-config-starter/AGENTS.md`, `AiTurn`, `AiTurnEvent`, `AiTurnStatus`, `AiTurnService`, `AiTurnEventService`, `AiStreamService`, `AiStreamExecutionContextHolder`, `AiStreamAccessTokenService`, `AiTurnEventEnvelope`, `AgenticAuthoringTurnStreamStartResponse`, `AgenticAuthoringTurnStreamService`, `AgenticAuthoringTurnStreamRequest`, `AgenticAuthoringTurnEngine`, `AgenticAuthoringTurnEventSink`, `AgenticAuthoringConversationTurnOrchestrator`, and the relevant tool-loop classes;
- `README.md`, `docs/ai-deployment-flow.md`, `src/public-api.ts`, manifests, recipes, and direct consumers when the change is public.

Before proposing a field, event, endpoint, local state, or fallback, inventory the existing request, generated contract, backend event, diagnostics, preview, pending clarification, quick reply, runtime observation, and flow state. Classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only the last can justify a cross-boundary contract change.

## Turn Identity And Local State

- Create a fresh `clientTurnId` for each submitted, retried, edited, or resent turn; preserve `sessionId` until cancel/reset deliberately starts a new conversation.
- Apply an async result only when its client turn identity still matches the active local turn. A late response must never overwrite a newer prompt, review, or clarification.
- Build requests from the current messages, attachments, context items, state/digests, schema/data evidence, diagnostics, preview, pending patch, pending clarification, and the action-specific structured continuation. Do not reconstruct lost state from display text.
- A new submit/edit/resend must clear abandoned quick replies, clarification questions, review authorization, preview, pending patch, pending clarification, errors, diagnostics, and observation ID before the next result materializes.
- Cancel resets the conversation/session according to the flow and leaves no applicable patch or clarification. A missing cancel handler is still required to clear local review artifacts safely.
- Runtime component observations are optional, best-effort evidence. Filter empty/unavailable collection, send only the supported envelope shape, mark it `untrusted_frontend_observation`, and never let frontend evidence elevate permissions, tool budgets, target eligibility, or apply authority.

## Semantic Continuations And Result Materialization

- Quick-reply labels and display prompts are presentation, never authority. Carry structured `value`, `canonicalAction`, `semanticDecision`, `contextHints`, presentation, and diagnostics without parsing labels back into intent.
- Promote only a backend-issued quick-reply semantic decision to `activeSemanticDecision`. Do not inherit context-hint decisions into free user input.
- Preserve `pendingClarification` source prompt, questions, diagnostics, and client turn identity into a clarification answer. Direct user input remains a submit action while carrying the pending clarification context.
- A result with structured clarification becomes `clarification` and cannot apply. A review requires backend `canApply === true` and the governed preview/patch. Consultative catalog answers may succeed with quick replies but no patch or apply authority.
- Keep `assistantContent`, diagnostics, quick replies, and related-surface evidence structured. The shell may render them but cannot reinterpret them into a new route, action, or permission.

## Stream Contract And Transport

The canonical authoring-turn API is start, stream, probe, and cancel beneath `/api/praxis/config/ai/authoring/turn/stream/**`. Generated contracts define the envelope identity: stream, thread, turn, finite sequence, schema version, timestamp, allowed type, and JSON-object payload.

- Validate received payloads at runtime before materializing them. Invalid JSON, wrong schema version/type, malformed envelope, and transport failures are transport/schema failures, not semantic assistant answers.
- Only `result`, `error`, and `cancelled` are terminal. `status`, `thought.step`, `heartbeat`, and `intent.resolved` are progress/evidence; they can update phase, status, or diagnostics but cannot authorize apply or complete the turn.
- On a terminal event, complete the observable and close EventSource or abort fetch. Never append a late event after terminal completion.
- Use EventSource with credentialed cookies when no explicit headers are required. Its stream path performs the canonical probe before connecting. Use the fetch SSE fallback when explicit headers are required or EventSource is unavailable; preserve cancellation through `AbortController` and do not claim that the EventSource probe ran on that fallback path.
- Surface lifecycle evidence such as probe readiness, transport opening, and first event as non-terminal diagnostics. Apply silence, result, and whole-turn timeouts as recoverable transport failures; do not fabricate a backend result.
- `Last-Event-ID`, access token, tenant/user/environment headers, and normalized session/client IDs are backend contract/security inputs. Do not invent alternate query parameters, origins, or unauthenticated reconnect paths.

## Prohibited Shortcuts

- Do not route prompts, quick-reply labels, error text, or stream content using keyword, regex, alias, or `includes` matching.
- Do not call an external LLM provider from Angular or turn a backend tool/policy gap into a browser-side heuristic.
- Do not make stream lifecycle, a thought step, a frontend observation, a cached diagnostic, or a quick-reply label equivalent to a semantic decision or apply permission.
- Do not add a second envelope, parallel patch stream, untyped event parser, or consumer-specific SSE client when the authoring-turn contract covers the need.
- Do not hand-edit generated contracts or let `@praxisui/ai` root exports become a facade for `@praxisui/core`.

## Impact And Validation

For endpoint, model, generated-contract, public API, or cross-lib changes, map backend owner, Angular consumers, OpenAPI/generated types, docs/recipes/registry, quickstart/HTTP examples, auth/replay impact, and breaking risk before editing.

Use the smallest proof that covers the changed layer:

```sh
npm exec -- ng test praxis-ai --watch=false --progress=false \
  --include='projects/praxis-ai/src/lib/core/services/assistant-turn-orchestrator.service.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/services/agentic-authoring-turn-client.service.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/services/ai-backend-api.service.spec.ts'
```

Add `assistant-shell.component.spec.ts` for shell state; use `npm run test:praxis-ai:assistant` for the legacy assistant view. Public `@praxisui/ai` changes require the library build, a direct consumer, and the focused E2E evidence required by local AGENTS. Backend semantics require the focused config-starter gates; cross-project/release proof may add quickstart HTTP/SSE, Page Builder, registry, and public docs checks.

For backend authoring-turn transport, persisted event lineage, transaction, signed-token, access-token, or security-chain changes, prefer the focused config-starter gate:

```sh
mvn "-Dtest=AiTurnEventServiceTest,AiTurnRepositoryContractTest,AiStreamTransactionContractTest,AiStreamRuntimeTransactionManagerIntegrationTest,AgenticAuthoringTurnStreamServiceTest,AgenticAuthoringTurnStreamHttpSseIntegrationTest,AgenticAuthoringTurnStreamSignedTokenIntegrationTest,AgenticAuthoringTurnStreamSecurityChainIntegrationTest,AiStreamAccessTokenServiceTest" test
```

For changes that alter tool progress, engine continuation, or conversation orchestration carried by the turn stream, add:

```sh
mvn "-Dtest=AgenticAuthoringTurnEngineTest,AgenticAuthoringConversationTurnOrchestratorTest,AgenticAuthoringToolLoopExecutorTest,AgenticAuthoringToolRegistryTest,AgenticAuthoringLlmPreIntentToolPlanningServiceTest" test
```

Treat `AiPatchStream*` tests as legacy compatibility evidence only when the older patch stream is intentionally touched. The canonical authoring-turn transport remains `/api/praxis/config/ai/authoring/turn/stream/**`.

Exercise: normal clarification-to-review/apply; stale result after a newer turn; cancel/reset; malformed envelope; EventSource unavailable or explicit headers; silent/no-terminal stream; timeout/result and cancel/result race; untrusted observation; structured quick reply; and a consultative answer with no apply authorization.

## Companion Skills

- `praxis-ai-composer-attachments-quick-replies` for composer inputs and structured continuations.
- `praxis-ai-shell-session-context` for session/context ownership and shell state.
- `praxis-core-widget-observations` for observation registry contracts.
- `praxis-ai-backend-config-contracts` for endpoint/header/generated-contract ownership.
- `praxis-ai-semantic-intent` for semantic routing constraints.
- `praxis-config-agentic-authoring-streaming` for backend stream, replay, semantic intent, tools, and apply governance.
- `praxis-angular-public-api-governance`, `praxis-angular-validation-gates`, and `praxis-angular-docs-playgrounds` for their respective cross-cutting surfaces.
