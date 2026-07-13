---
name: praxis-ai-composer-attachments-quick-replies
description: Use when implementing, auditing, or consuming `@praxisui/ai` composer submission, quick replies, recommended intents, clarification continuation, pasted/selected attachments, safe attachment forwarding, edit/resend/feedback actions, or optional browser speech input.
---

# Praxis AI Composer, Attachments, And Quick Replies

The composer captures local interaction and renders backend-authored choices. It must preserve structured evidence and turn state without becoming an intent router, uploader, persistence layer, or patch authority.

## Owner Flow

`PraxisAiAssistantShellComponent` owns accessible input, display, file/paste events, object-URL cleanup, optional voice UX, and emits typed actions. `assistant-quick-reply.utils` preserves a reply's canonical value and structured metadata. `AgenticAuthoringTurnClientService` maps backend stream quick replies, pending clarification, preview, patch, diagnostics, and consultative catalog answers into shell turn results. `PraxisAssistantTurnOrchestratorService` owns submit/clarification/edit/resend/retry/cancel state and stale-artifact reset. Backend contracts own semantic intent, canonical actions, decisions, risk, clarification authority, upload references, and apply authorization.

Read `projects/praxis-ai/AGENTS.md`, shell types/component, quick-reply utility, turn models/orchestrator, context snapshot models, speech service, and focused specs. Use `praxis-ai-turn-orchestration-transport` for turn/stream state and `praxis-ai-shell-session-context` for snapshots or serializable attachment summaries.

## Structured Continuations

- Streamed quick replies are accepted only when they have stable `id` and `label`, then mapped into shell types with `kind`, `prompt`, description, icon/tone, `presentation`, `contextHints`, `canonicalAction`, `semanticDecision`, and `value`. Do not fabricate missing identity or infer a route from display text.
- A quick reply preserves `id`, `value`, `rawValue`, `displayPrompt`, `contextHints`, `canonicalAction`, `semanticDecision`, description, and presentation. Clone structured objects before handing them between UI/turn state so later mutation cannot change a submitted continuation.
- Its canonical submitted prompt is the nonempty string `value`, falling back to `prompt`; the visible label is only display text. Never route by label, translated copy, regex, aliases, `includes`, resource-path fragments, or hidden commands.
- In clarification state call the canonical clarification path and preserve the pending clarification lineage. Outside it, submit a typed action carrying structured context. A free prompt must not inherit a quick reply's semantic decision.
- Recommended intents are governed opportunities, not local permissions. Their current action kinds are `submit-prompt`, `start-review`, `open-guidance`, or an explicit custom kind; preview/apply still requires backend semantic resolution and contract gates.
- Consultative catalog answers may include quick replies without forcing clarification. Preserve the backend's consultative/clarification distinction instead of treating every quick-reply list as a required user decision.
- Presentation helpers may format server-provided details, icons, tone, resource labels, and evidence. They cannot turn hints into authorization, canonical target selection, or a new semantic route.

## Attachments, Messages, And Voice

- Shell attachments may temporarily hold `File`, `source` (`paste`, `file-picker`, or `host`), `status`, and owned `previewUrl` for local UX. Emit them to a host adapter; do not upload, persist, or put raw handles, bytes, base64, blob URLs, or file payloads into assistant context or backend turns.
- Backend-facing context uses only serializable safe summaries or a contract-owned upload reference. A new upload requirement belongs to the canonical backend/files contract, not a composer workaround.
- Image attachments created by paste or file picker receive an owned object URL. Revoke owned preview URLs when attachments are removed, detached, or the shell is destroyed. Preserve host-owned URLs and do not revoke an URL still used by active attachments.
- Edit/resend branches from the selected user message and clears stale quick replies, preview, pending patch, diagnostics, clarification, and apply state before the replacement turn. Retry/cancel follow the orchestrator's same reset authority.
- Feedback is write-only evidence linked to assistant/status/error observation IDs; it cannot mutate a semantic decision or applied result without backend acknowledgement.
- Browser speech is explicit opt-in and local transcription convenience. Keep it disabled by default, append a valid transcript without auto-submitting, handle unsupported/permission/no-speech outcomes, and invalidate late captures through the capture sequence when mode changes or capture stops. Voice text still goes through normal backend semantic resolution.

## Contract Inventory And Impact

Before fields/events, inventory existing shell types, context snapshot, upload contract, manifests, actions, capabilities, clarification/turn contracts, diagnostics, and backend tools. Classify `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only a real gap permits a public payload, upload route, or local storage addition.

Public shell/type changes require the AI build, direct consumer and local-AGENTS E2E proof. For source/manifest/docs changes, review AI registry and public docs artifacts; state explicitly when they are unaffected.

## Validation

```sh
npm exec -- ng test praxis-ai --watch=false --progress=false \
  --include='projects/praxis-ai/src/lib/ui/assistant-shell/assistant-shell.component.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/models/assistant-context.models.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/services/assistant-turn-orchestrator.service.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/services/browser-speech-transcription.service.spec.ts'
```

`assistant-context.models.spec.ts` is the focused proof that attachment summaries remain serializable, redact unsafe text, and drop raw `File`, blob/preview URL, runtime state, config payload, diagnostics, or pending patch details before entering assistant context.

Exercise: structured clarification; direct prompt after clarification; edit/resend cleanup; pasted and selected attachment with preview cleanup; hostile label that must not route intent; stale speech transcript; serializable attachment summaries with no local file/blob leakage; and a requested upload with no contract that must be rejected/escalated.

Use `praxis-ai-semantic-intent` for routing, `praxis-files-upload-backend-contract` for uploads, `praxis-ai-backend-config-contracts` for endpoint changes, and `praxis-angular-i18n-governance` for framework copy.
