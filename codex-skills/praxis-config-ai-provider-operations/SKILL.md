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
- `OpenAiAgentsTableTurnPlanner`, `OpenAiAgentsSessionClient`,
  `OpenAiAgentsSessionJournalService`, `AgenticAuthoringTurnEventSink`,
  `AgenticAuthoringTurnStreamService`, `AiThread`, its migration, and focused
  tests when changing managed-session authority, renewal, cleanup, or terminal publication
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
Before returning a completed root turn, inspect its session items through bounded
pagination and the same per-turn GET retry/deadline budget. A `function_call` or
`function_call_output` with `status=failed` and the current root `turn_id` must
veto success with the fixed sanitized code `remote-function-failed`. Do not infer
success from session `idle` or root `completed`, classify raw error text, copy
provider output into telemetry, retry mutations, or attribute an older turn's
failure to the current turn. An incomplete item list cannot prove success. Test
current versus historical failures, later pages, malformed/incomplete pagination,
shared read retries, and no local function re-execution. This veto diagnoses a
remote tool failure; it does not establish the provider's internal root cause.

A completed remote turn is not an approved Praxis preview. Accept session continuation
only after the canonical engine successfully appends an applicable terminal result;
UI persistence still requires the separate governed apply operation.

Before continuing a managed session, compare the server-reconciled target app,
component, route, selected widget, schema base URL, authoring manifest, declared
tools, skill catalog refs and hashes, required skill refs, and server-resolved
credential fingerprint with the authority captured when that session opened. The current
page draft may change after an accepted terminal and is not itself renewal drift.
On authority or credential drift, close the old remote session and open a new one
only after cleanup reports `deleted` or `already-absent`. During in-process renewal,
preserve the accepted page draft as grounded input to the new session; it is not a
persisted apply or a preserved remote conversation. The experimental journal on
`ai_thread` reserves a random generation and 30-minute lease before one creation
POST, then records the remote ID synchronously under the same fence. The POST
metadata carries only the generation nonce. Resolve the real `proj_...` ID on
the server; send `OpenAI-Project` on every request and journal the credential
reference, project ID,
and SHA-256 credential fingerprint, never the key. Check the lease/fence before
provider requests, function execution, returning a result, and accepting a turn.
Do not treat an in-memory client or a successful HTTP response as a substitute
for the durable transition.

For a managed terminal, inspect the real event sink and stream service. Keep
lock order stream monitor then database; `journal.withLease` wraps only the
persisted append through `appendGuarded`. The transaction must commit before
updating stream cache/cursor, sending SSE, or completing stream resources. On
rollback, release the local terminal claim so a valid append can retry; do not
emit or accept the uncommitted result. Never include emitter I/O in that database
transaction. Prove the ordering with `AgenticAuthoringGuardedStreamCommitTest`
and journal PostgreSQL tests.

After restart or lease expiry, recovery is driven by the next eligible request;
there is no autonomous sweeper. Use the original credential and project scope.
For a known ID, verify it by scoped GET before cleanup. For an unknown ID, scan
the paginated `GET /agents/sessions` list within the client page cap and require
exactly one session whose metadata nonce matches; the API does not filter by
metadata or guarantee immediate list visibility. Record the unique ID under the
fence, persist `DELETE_PENDING` before DELETE, and clear only after DELETE 2xx
or scoped GET/DELETE 404. Zero or multiple matches, an incomplete list, unavailable
credential/project, or unconfirmed deletion keep the journal blocked with the
generation intact. Do not open a replacement session or blindly retry POST.
Recovery deletes the old remote session; after process restart the host must
reconcile the canonical page and must not claim to restore a preview draft or
remote conversation. Anaphoric references to prior turns are not guaranteed.
A missing historical ID from a session created without the nonce still needs
operational reconciliation.

Recover only read-only `GET` of the session and paginated turns/items after HTTP
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
retries `DELETE` on HTTP `409` up to four attempts. Reconciliation GETs use
the same bounded retry policy without creating a session or sending input.
The journal records remote identity and cleanup state, not function outputs or
the remote conversation.

Bound function calls, repair attempts, request/body deadlines, response size, and
session lifetime. Prove timeout when headers arrive but the body stalls, duplicate
function replay without re-execution, conflicting replay rejection, cancellation,
and cleanup. Never blindly repeat a session-creation mutation with an uncertain
network outcome. An unknown ID may remain blocked when exact, complete list
evidence is unavailable; do not describe the nonce as guaranteed recovery.
Keep provider error codes allowlisted; syntactically safe arbitrary strings can still
contain secrets.

For managed-session changes, run focused planner, client, journal and host tests.
Prove authority drift and accepted-draft handoff, single POST under concurrent
claims, the known/unknown-ID recovery paths, zero/multiple/incomplete list veto,
lost-fence veto before provider mutation, and DELETE 2xx/404/409/timeout. Inspect
the sanitized cleanup status and absence of a second session after unconfirmed
cleanup; use a fake provider and isolated database, not a paid call, for these gates.

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
