---
name: praxis-ai-composer-attachments-quick-replies
description: Use when changing or reviewing `@praxisui/ai` assistant composer actions, prompt submission, quick replies, recommended intents, clarification state, pasted/selected attachments, attachment summaries, safe forwarding, message edit/resend, feedback actions, or browser voice input.
---

# Praxis AI Composer Attachments Quick Replies

Use this skill for the interactive shell controls that capture user input and materialize backend-authored choices. Composer UI may carry semantic payloads returned by contracts, but it must not become a local command router.

## Canonical Boundary

- `PraxisAiAssistantShellComponent` owns input UX, actions, quick reply presentation, recommended intent presentation, attachment selection/paste events, message actions, and optional browser speech capture.
- `PraxisAssistantTurnOrchestratorService` owns turn lifecycle, pending clarification, edit/resend replay, apply/retry/cancel transitions, and request assembly.
- Backend/LLM contracts own semantic intent, clarification options, canonical actions, semantic decisions, and risk policies.
- Component or host adapters own file handling and safe attachment summaries. The shell does not upload, persist, or serialize raw files to backend contracts.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `projects/praxis-ai/README.md`
- `src/lib/ui/assistant-shell/assistant-shell.types.ts`
- `src/lib/ui/assistant-shell/assistant-shell.component.ts`
- `src/lib/ui/assistant-shell/assistant-shell.component.html`
- `src/lib/core/models/assistant-turn.models.ts`
- `src/lib/core/services/assistant-turn-orchestrator.service.ts`
- `src/lib/core/services/assistant-quick-reply.utils.ts`
- `src/lib/core/services/browser-speech-transcription.service.ts`
- focused shell and orchestrator specs

Use `praxis-ai-semantic-intent` when quick replies, recommended intents, or clarifications influence intent routing. Use `praxis-ai-shell-session-context` when the change depends on snapshot data or session identity.

## Interaction Rules

- Quick replies and clarification options must preserve full payloads: `value`, `contextHints`, `canonicalAction`, `semanticDecision`, presentation, and display prompt. Do not downcast them to labels or local command strings.
- Recommended intents are authored opportunities from governed evidence. They may submit prompts, start review, or open guidance, but must not bypass manifest validation or backend semantic resolution.
- In clarification state, preserve `pendingClarification` and attach it to the next submit action so backend contracts can continue the same semantic decision.
- Message edit/resend must replay from the selected user message and clear stale quick replies, previews, pending patches, and diagnostics from the abandoned branch.
- Attachment objects may include local `File` or `previewUrl` for UX, but backend requests must use serializable safe summaries or contract-owned upload references. Never forward bytes, base64, blob URLs, or raw file handles as governed context.
- Browser speech is opt-in and disabled by default. Treat it as local transcription convenience, not canonical voice intent. Promote backend-owned transcription only through explicit contracts.
- Feedback actions may attach assistant observation ids to assistant/status/error messages; they must not mutate canonical decisions without backend acknowledgement.

## Red Flags

Refactor or reject:

- quick replies implemented as `includes`, regex command parsing, localized label switches, or hidden command aliases
- clarification answers that discard `contextHints`, `canonicalAction`, or `semanticDecision`
- shell uploads or persists files directly without a platform contract
- composer state that applies stale `pendingPatch` or stale preview after edit, resend, retry, or cancel
- voice input treated as a separate intent authority

## Validation

Use focused checks:

- shell interaction/rendering: `assistant-shell.component.spec.ts`
- pending clarification, edit/resend, attachments, apply/retry/cancel: `assistant-turn-orchestrator.service.spec.ts`
- quick reply normalization: quick reply utility specs when touched
- browser speech: speech transcription service spec and shell voice tests

State whether docs/examples/registry artifacts are unaffected or update them when public behavior changes.
