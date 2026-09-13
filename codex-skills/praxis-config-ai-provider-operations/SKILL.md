---
name: praxis-config-ai-provider-operations
description: Use when operating or changing Praxis Config AI provider infrastructure: provider catalog/status/test endpoints, governed audio transcription, connection probes, routing and fallback, failure classification, streaming cancellation, invocation telemetry and metrics, pricing snapshots, usage/cost attribution, provider metadata, managed Agents API session renewal, paid live-gate budgets, key separation, or public-host AI rate limiting. Do not use for semantic authoring logic alone.
---

# Praxis Config AI Provider Operations

Use this skill for the operational boundary around external AI providers.
`praxis-config-starter` owns provider routing, status, sanitized telemetry, and
invocation policy; semantic intent and authoring decisions remain in their
agentic/domain owner skills.

## Source Audit

Inspect:

- `praxis-config-starter/AGENTS.md`
- `AiProviderController`, `AiProviderStatusController`, catalog/status/test DTOs
- `AiProviderManagementService`, `AiProviderRouter`, `AiProviderStatusService`
- `AiProviderFailureClassifier`, invocation telemetry/metrics/trace
- provider streaming fallback/cancel and access-token services
- `OpenAiAgentsTableTurnPlanner`, `OpenAiAgentsSessionClient`, and their focused
  tests when changing managed-session authority, renewal, or cleanup
- `AiAudioTranscriptionController`, `AiAudioTranscriptionRequest`, `AiAudioTranscriptionResponse`, `AiProvider.supportsAudioTranscription/transcribeAudio`, provider management selection/configuration, and provider adapter implementation
- `docs/ai/openai-cost-attribution-and-live-gates.md`
- provider pricing schema/snapshot and provider telemetry evidence docs
- focused management, router, failure, metrics, telemetry, pricing, streaming,
  and real-provider integration tests

For hosted protection also inspect Quickstart security/rate-limit configuration,
deployment variables, and the exact live-gate workflow or script.

## Operational Boundary

- Connection/status probes should establish usable connectivity and model
  availability with the least cost possible. Do not perform an inference merely
  to test credentials when a provider-native non-generative probe exists.
- Provider routing is explicit and observable. Preserve selected provider/model,
  phase, attempt, response mode, latency, token usage, failure class, fallback,
  cancellation, and terminal outcome without storing prompts or responses in
  ordinary operational telemetry.
- Governed audio transcription is a provider operation, not an intent or turn.
  The canonical Config endpoint resolves principal scope, enforces the bounded
  multipart payload, chooses the configured transcription provider/model, checks
  provider capability, and returns transcript text for later user review. It
  must not initiate authoring, semantic routing, preview, apply, or persistence.
- Keep raw audio bytes, transcript text, file names, tenant/user identifiers,
  provider bodies, and credentials out of ordinary telemetry and errors. When
  operational evidence is required, retain only bounded safe metadata such as
  provider/model, MIME class, byte/duration units, outcome, latency, and failure
  class according to the canonical observability policy.
- Failure classification drives retry/fallback policy. Authentication, quota,
  rate-limit, timeout, cancellation, invalid request, schema failure, and
  provider outage are not interchangeable.
- Normalize provider failures on both unit and batch paths. Prefer structured
  status, error code, `Retry-After`, and `google.rpc.RetryInfo`; retain raw
  provider bodies/messages only as an unexposed cause when necessary, never in
  DTOs, ordinary logs, or canonical error messages.
- Retries and fallbacks are bounded. Cancellation must reach the provider path
  and the turn lifecycle; do not start a replacement call after a terminal
  cancel or duplicate a paid call after an accepted result.
- Provider retry guidance is a lower bound, not a polling hint. Do not retry
  before it. If the guided delay exceeds the bounded inline retry window,
  persist the typed terminal attempt with its safe `retryAfter` instead of
  sleeping for less or inventing a consumer-side retry.
- Pricing snapshots are versioned evidence for estimation, not billing truth.
  Record model/input/output/cache units and snapshot identity so estimates are
  reproducible; never hardcode prices in UI or prompts.
- Provider request metadata is bounded, non-content, and sanitized. Keep API
  keys, prompts, responses, tenant/user ids, business data, and raw exceptions
  out of metadata and logs.

## OpenAI Model And Managed Session Qualification

Before enabling a newly released model, inspect the current official model guide and
`SpringAiOpenAiService` request serialization. Availability in the model list does not
prove compatibility with temperature, reasoning effort, or output-token settings.
For the known `gpt-6-astra` identifier, the adapter omits temperature, uses supported
reasoning effort, and preserves explicit token limits; do not infer undocumented
snapshot identifiers or apply the same policy to every future model by prefix.
Prove the serialized request in `SpringAiOpenAiServiceTest`, including an unaffected
model, before a paid comparison.

For the experimental Agents API transport, inspect `OpenAiAgentsSessionClient`, its
focused tests, and `docs/ai/agents-api-pilot.md`. Keep one remotely managed session
bound to the server-owned principal, canonical thread, and credential scope.
A completed remote turn is not an approved Praxis preview. Accept session continuation
only after the canonical engine successfully appends an applicable terminal result;
UI persistence still requires the separate governed apply operation.

Before continuing a managed session, compare the server-reconciled target app,
component, route, selected widget, schema base URL, authoring manifest, declared
tools, skill catalog refs and hashes, required skill refs, and server-resolved
credential fingerprint with the authority captured when that session opened. The current
page draft may change after an accepted terminal and is not itself renewal drift.
On authority or credential drift, close the old remote session and open a new one
only after cleanup reports `deleted` or `already-absent`. Preserve the accepted
page draft as grounded input to the new session; it is not a persisted apply or a
preserved remote conversation. If deletion remains unconfirmed, block another
session for the same owner in this process with `managed-session-cleanup-required`.
The tombstone consumes bounded in-process owner capacity; reconcile remote cleanup
explicitly instead of restarting merely to bypass the block. Do not silently
retry creation or promise distributed recovery. After renewal or
loss of remote history, do not promise that anaphoric references to prior turns
will resolve unless the necessary context is explicitly available and verified.

Recover only read-only `GET` of the session and paginated turns after HTTP
`500`, `502`, `503`, or `504`. Share at most two retries across all those reads
in one user turn, with minimum waits of one then two seconds. Honor a valid
`Retry-After` in seconds or RFC 1123 date form, but stop if the delay cannot fit
within the five-second cumulative inline wait budget or remaining turn
deadline. Check cancellation throughout the wait. Preserve the first sanitized
HTTP failure diagnostic after a later successful read; its presence alone does
not prove a terminal turn failure. Prove the shared budget, first diagnostic,
cancellation, deadline, and no duplicate function execution with
`OpenAiAgentsSessionClientTest`.
Do not retry authentication/quota failures, unknown transport outcomes, or
`POST` creation/events under this read policy. Pending `tool_result` replay
with cached output is a separate idempotency path. Session cleanup separately
retries `DELETE` on HTTP `409` up to four attempts; neither path supplies a
durable journal or cross-process recovery.

Bound function calls, repair attempts, request/body deadlines, response size, and
session lifetime. Prove timeout when headers arrive but the body stalls, duplicate
function replay without re-execution, conflicting replay rejection, cancellation,
and cleanup. Never blindly repeat a session-creation mutation with an uncertain
network outcome. Record inability to recover a missing remote session ID as a limit.
Keep provider error codes allowlisted; syntactically safe arbitrary strings can still
contain secrets.

For managed-session changes, also run
`OpenAiAgentsTableTurnPlannerTest#renewsRemoteAuthorityWithoutLosingAcceptedDraft`, including
authority drift, accepted-draft handoff, and failed deletion, alongside the client
cleanup tests. Inspect the sanitized cleanup status and the absence of a second
session after an unconfirmed delete; do not use a paid call to establish this gate.

Hosted skill evidence has distinct levels: attachment/configuration, explicit file
reads through a governed application tool, and native provider skill execution.
Record the project, skill version, archive/file hashes and observed read mechanism
without copying raw files into telemetry. A skill attached to a session or returned
by an application function is not proof of native execution. When using reviewed
exports, preserve exact content and an allowlist; do not silently replace a missing
account skill with locally authored instructions.

Compare runtimes with equivalent prompts, model, context and skill availability.
Record successful first attempts, repairs, total journey latency, calls and token
units separately from billing. A single successful journey supports a pilot, not
reliability estimates or definitive adoption. Keep the production selection unchanged
until the explicit adoption criteria are met.

## Usage, Cost, And Live Gates

Separate provider credentials and budgets by runtime owner/environment, such as
CI live gate, local development, and public landing. Source control may document
the variables and verification; it must not create projects, rotate keys, change
budgets, or deploy secrets without explicit external authorization.

Paid gates must be deliberate, bounded journeys. Prefer one canonical
end-to-end authoring journey over repeated isolated classifications. Record
whether the gate was deterministic or external-provider, call/turn count,
bounded continuation, cancellation behavior, and sanitized receipt. GitHub
Actions is a release/final gate, not the normal development loop.

Provider-backed transcription is also a paid operation. Unit/controller tests
must use deterministic adapters or mocks; a live transcription probe requires
an explicit audio fixture, maximum call count, payload-size/cost expectation,
cleanup policy, and sanitized receipt. Do not submit a second assistant turn as
part of a transcription connectivity probe.

Public hosts apply a dedicated AI rate limit before broader config limits. The
reference in-memory limiter is not a substitute for production gateway/WAF
enforcement or provider project budgets.

## Proof

Use focused Config gates:

```bash
mvn "-Dtest=AiProviderManagementServiceTest,AiProviderRouterTest,AiProviderFailureClassifierTest,AiProviderInvocationMetricsTest,AiProviderStreamingFallbackAndCancelIntegrationTest,AgenticAuthoringProviderTelemetrySerializationTest,AgenticAuthoringProviderPricingSnapshotTest" test
```

Add controller/status tests for endpoint changes, focused provider management
and provider adapter tests for audio transcription, Quickstart security tests for
rate limiting, and a real-provider probe only when credentials, model listing,
or external integration genuinely requires it. Real paid calls require explicit
scope, stopping conditions, cost expectation, and sanitized output.

Prove healthy probe/routing, transcription capability rejection and scoped
bounded success without turn creation, classified provider failure with bounded fallback,
cancel/timeout without duplicate call, sanitized telemetry serialization,
unit and batch failure parity, provider-guided retry timing, pricing estimate
reproducibility, and rate-limit denial. Review OpenAPI/docs, workflows,
environment examples, Quickstart security docs, and operational receipts when
public behavior changes.

## Companion Skills

- `praxis-config-agentic-authoring-streaming`: semantic turn/tool/stream lifecycle.
- `praxis-ai-turn-orchestration-transport`: Angular assistant transport and cancellation UX.
- `praxis-api-quickstart-security-config`: hosted endpoint protection and rate limiting.
- `praxis-api-quickstart-operational-proof`: deployed reference-host evidence.
- `praxis-core-logging-observability`: safe client/runtime diagnostics.
