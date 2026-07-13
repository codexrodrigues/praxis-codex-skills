---
name: praxis-ai-assistant-runtime
description: Use when changing or reviewing `@praxisui/ai` assistant runtime, AI backend client, assistant shell/dock/session host, turn streaming, quick replies, clarifications, diagnostics, previews, apply payloads, history, runtime observations, `/api/praxis/config/ai/**` integration, or AI UX state materialization.
---

# Praxis AI Assistant Runtime

Use this skill for `@praxisui/ai` as shell, UX, HTTP client, history, and materializer of governed backend/LLM decisions. Do not turn browser UI into the primary intent router.

For deeper work, pair this umbrella skill with:

- `praxis-ai-shell-session-context` for shell, dock, session host, session registry, and safe context snapshots.
- `praxis-ai-composer-attachments-quick-replies` for composer actions, quick replies, clarifications, attachments, message replay, and voice input.
- `praxis-ai-turn-orchestration-transport` for turn controllers, lifecycle phases, runtime observations, stream events, and terminal result handling.
- `praxis-ai-backend-config-contracts` for endpoint resolution, AI config tokens, headers, provider/model endpoints, manifest endpoints, and Praxis Config boundary.

## Canonical Boundary

- `@praxisui/ai` sends prompt, messages, context, runtime state, capabilities, manifests, observations, and metadata to backend/LLM contracts.
- Praxis Config backend endpoints under `/api/praxis/config/ai/**` own provider calls, model execution, streams, and persisted AI config.
- Frontend logic may manage interaction state, accessibility, history, replay, confirmations, quick replies, clarifications, diagnostics, preview rendering, and apply of already resolved operations.
- Runtime component observations are untrusted frontend evidence and must be marked with the trust boundary before backend grounding.
- `PraxisAssistantContextSnapshot` carries safe summaries and digests; shell/session code should not invent component semantics or transport raw runtime payloads.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `src/public-api.ts`
- `src/lib/core/services/ai-backend-api.service.ts`
- `src/lib/core/services/agentic-authoring-turn-client.service.ts`
- `src/lib/core/services/assistant-turn-orchestrator.service.ts`
- `src/lib/core/services/assistant-history.service.ts`
- `src/lib/core/models/assistant-context.models.ts`
- `src/lib/core/models/assistant-turn.models.ts`
- `src/lib/ui/assistant-shell/**`
- `src/lib/ui/ai-assistant/**`
- `src/lib/ui/assistant-session-host/**`
- `src/lib/ui/assistant-dock/**`
- relevant specs for backend API, assistant shell, session host, history, validator, and turn client

## Runtime Rules

- Do not call external providers directly from the Angular lib when the canonical Praxis Config backend contract exists.
- Preserve `currentState`, `dataProfile`, `schemaFields`, `runtimeState`, `contextHints`, `runtimeComponentObservations`, pending clarification, preview, diagnostics, and apply payload shapes.
- Stream/lifecycle events must update visible assistant state before terminal result when the backend emits intermediate reasoning, status, clarification, diagnostics, or quick replies.
- Manual confirmation is required for risky or destructive patches when the contract marks them as such.
- History persistence must respect tenant, env, userId, redaction, and local storage boundaries.
- `AssistantHistoryService` is the canonical local-history owner. It keys the index by `tenantId/env/userId`, rejects cross-scope restore/delete/touch, honors storage unavailability, prunes old sessions, caps session count, and redacts API keys, tokens, bearer credentials, JWTs, `sk-*` secrets, passwords, and similar values before writing. Do not persist assistant history through ad hoc component localStorage keys.
- Public exports in `@praxisui/ai` must not become a transitive facade for `@praxisui/core`.
- Treat the local runtime as a state machine: a clarification cannot expose apply, a review cannot apply without a pending governed patch, and retry/edit/resend/cancel must clear abandoned preview, diagnostics, quick replies, and clarification state before a new branch materializes.
- `PraxisAssistantTurnOrchestratorService` protects async materialization with `clientTurnId` and clears replay/active-turn state. Preserve stale-result rejection and reset behavior when changing submit, edit, resend, retry, cancel, or apply.
- Persist history only through `AssistantHistoryService` under the tenant/env/user scope. Respect storage unavailability, 30-day/session-count retention, redaction on write and legacy read, and never reuse a session across scopes.
- Local confirmation may enforce stricter UI policy, but cannot downgrade backend risk or make a patch applicable. Manual patch editing/reapply in the legacy assistant remains an explicitly confirmed, auditable compatibility flow gated by `allowManualPatchEdit`; do not present it as the canonical route for governed decisions or manifest-backed edits.
- Intermediate SSE status/thought/diagnostic events are progress evidence. Terminal result/error/cancelled transitions determine final materialized state; raw errors and diagnostics remain redacted and are never promoted to business semantics.

## Validation

Use focused checks:

- backend payload/endpoints: `ai-backend-api.service.spec.ts`
- streaming/turns: `agentic-authoring-turn-client.service.spec.ts` and orchestrator specs
- history scope/redaction: `assistant-history.service.spec.ts`
- assistant UX: `assistant-shell.component.spec.ts`, `ai-assistant.component.spec.ts`, session host/dock specs
- contracts: generated contract specs and response validator specs
- public API changes: build `praxis-ai` and at least one direct consumer when feasible

Review README and `docs/ai-deployment-flow.md` when endpoints, deployment, provider routing, or public behavior change.

For a runtime-wide change, map the affected specialist surfaces first and run their focused gate rather than relying on an umbrella build: context/session, composer, turn/transport, backend contract, history, and legacy assistant UI. State why each unaffected surface is outside the change.
