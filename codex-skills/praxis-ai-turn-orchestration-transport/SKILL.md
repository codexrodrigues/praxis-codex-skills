---
name: praxis-ai-turn-orchestration-transport
description: Use when changing or reviewing `PraxisAssistantTurnOrchestratorService`, assistant turn models, flow controllers, session/client turn ids, runtime observation collection, apply/retry/cancel/edit/resend lifecycle, `AgenticAuthoringTurnClientService`, SSE/fetch streaming fallback, lifecycle events, terminal result handling, or agentic authoring turn transport.
---

# Praxis AI Turn Orchestration Transport

Use this skill for the bridge between assistant interaction state and backend turn streams. The orchestrator manages local lifecycle; transport services connect to governed backend contracts and materialize stream events.

## Canonical Boundary

- `PraxisAssistantTurnOrchestratorService` creates controllers and assembles `PraxisAssistantTurnRequest` from prompt, messages, attachments, context items, digests, pending clarification, pending patch, diagnostics, and runtime observations.
- `PraxisAssistantTurnFlow` implementations own submit/apply/cancel/retry behavior for a shell mode.
- `AgenticAuthoringTurnClientService` converts backend stream starts, lifecycle events, SSE/fetch envelopes, quick replies, clarifications, previews, diagnostics, and terminal results into `PraxisAssistantTurnResult`.
- `AiBackendApiService` owns HTTP endpoints, headers, stream connection mechanics, provider/config endpoints, and generated contract types.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `src/lib/core/models/assistant-turn.models.ts`
- `src/lib/core/services/assistant-turn-orchestrator.service.ts`
- `src/lib/core/services/agentic-authoring-turn-client.service.ts`
- `src/lib/core/services/ai-backend-api.service.ts`
- `src/lib/core/contracts/ai-contract.generated.ts`
- `src/lib/ui/assistant-shell/assistant-shell.types.ts`
- focused orchestrator, turn client, backend API, and shell specs

Use `praxis-ai-composer-attachments-quick-replies` for composer-originated actions. Use `praxis-ai-backend-config-contracts` for endpoint/header/token changes.

## Orchestration Rules

- Generate and preserve `sessionId` and `clientTurnId` so stale async results cannot overwrite newer turns.
- Keep phases explicit: capture, contextualize, clarify, plan, preview, review, apply, summarize.
- `submitPrompt`, clarification answers, edit/resend, retry, cancel, and apply must reset stale preview, pending patch, quick replies, clarification questions, diagnostics, and observation ids according to the branch being abandoned.
- Preserve `pendingClarification` into clarification submissions and carry semantic option payloads through `activeSemanticDecision` and `contextHints`.
- Collect runtime component observations only as optional evidence. When sent to backend contracts, mark the trust boundary as untrusted frontend observation.
- Intermediate stream/lifecycle events should update status, phase, diagnostics, or progress before a terminal result arrives.
- Terminal `result`, `error`, and `cancelled` envelopes must close or reset state deterministically and must not leave stale apply payloads active.

## Transport Rules

- Prefer EventSource when no explicit headers are needed; use fetch stream fallback when explicit headers require it or EventSource is unavailable.
- Probe streams before opening when the backend exposes probe endpoints, and surface lifecycle diagnostics without treating them as final decisions.
- Parse and validate stream envelopes against generated contract types; parse errors are transport/schema failures, not assistant semantic answers.
- Convert backend quick replies and pending clarifications without dropping `presentation`, `contextHints`, `canonicalAction`, `semanticDecision`, or diagnostics.
- Consultative catalog answers can end as success even when quick replies are present; edit flows require review/apply state and a governed pending patch.

## Validation

Use focused checks:

- local lifecycle: `assistant-turn-orchestrator.service.spec.ts`
- streaming and event conversion: `agentic-authoring-turn-client.service.spec.ts`
- endpoint stream mechanics: `ai-backend-api.service.spec.ts`
- shell state materialization: `assistant-shell.component.spec.ts` when UI is affected

For public type or `public-api.ts` changes, build `praxis-ai` and a direct consumer when feasible.
