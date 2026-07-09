---
name: praxis-ai-assistant-runtime
description: Use when changing or reviewing `@praxisui/ai` assistant runtime, AI backend client, assistant shell/dock/session host, turn streaming, quick replies, clarifications, diagnostics, previews, apply payloads, history, runtime observations, `/api/praxis/config/ai/**` integration, or AI UX state materialization.
---

# Praxis AI Assistant Runtime

Use this skill for `@praxisui/ai` as shell, UX, HTTP client, history, and materializer of governed backend/LLM decisions. Do not turn browser UI into the primary intent router.

## Canonical Boundary

- `@praxisui/ai` sends prompt, messages, context, runtime state, capabilities, manifests, observations, and metadata to backend/LLM contracts.
- Praxis Config backend endpoints under `/api/praxis/config/ai/**` own provider calls, model execution, streams, and persisted AI config.
- Frontend logic may manage interaction state, accessibility, history, replay, confirmations, quick replies, clarifications, diagnostics, preview rendering, and apply of already resolved operations.
- Runtime component observations are untrusted frontend evidence and must be marked with the trust boundary before backend grounding.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `src/public-api.ts`
- `src/lib/core/services/ai-backend-api.service.ts`
- `src/lib/core/services/agentic-authoring-turn-client.service.ts`
- `src/lib/core/services/assistant-turn-orchestrator.service.ts`
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
- Public exports in `@praxisui/ai` must not become a transitive facade for `@praxisui/core`.

## Validation

Use focused checks:

- backend payload/endpoints: `ai-backend-api.service.spec.ts`
- streaming/turns: `agentic-authoring-turn-client.service.spec.ts` and orchestrator specs
- assistant UX: `assistant-shell.component.spec.ts`, `ai-assistant.component.spec.ts`, session host/dock specs
- contracts: generated contract specs and response validator specs
- public API changes: build `praxis-ai` and at least one direct consumer when feasible

Review README and `docs/ai-deployment-flow.md` when endpoints, deployment, provider routing, or public behavior change.
