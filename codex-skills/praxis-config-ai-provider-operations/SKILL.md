---
name: praxis-config-ai-provider-operations
description: Use when operating or changing Praxis Config AI provider infrastructure: provider catalog/status/test endpoints, governed audio transcription, connection probes, routing and fallback, failure classification, streaming cancellation, invocation telemetry and metrics, pricing snapshots, usage/cost attribution, provider metadata, paid live-gate budgets, key separation, or public-host AI rate limiting. Do not use for semantic authoring logic alone.
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
