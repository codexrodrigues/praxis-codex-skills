---
name: praxis-config-ai-provider-operations
description: Use when operating or changing Praxis Config AI provider infrastructure: provider catalog/status/test endpoints, connection probes, routing and fallback, failure classification, streaming cancellation, invocation telemetry and metrics, pricing snapshots, usage/cost attribution, provider metadata, paid live-gate budgets, key separation, or public-host AI rate limiting. Do not use for semantic authoring logic alone.
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
- Failure classification drives retry/fallback policy. Authentication, quota,
  rate-limit, timeout, cancellation, invalid request, schema failure, and
  provider outage are not interchangeable.
- Retries and fallbacks are bounded. Cancellation must reach the provider path
  and the turn lifecycle; do not start a replacement call after a terminal
  cancel or duplicate a paid call after an accepted result.
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

Public hosts apply a dedicated AI rate limit before broader config limits. The
reference in-memory limiter is not a substitute for production gateway/WAF
enforcement or provider project budgets.

## Proof

Use focused Config gates:

```bash
mvn "-Dtest=AiProviderManagementServiceTest,AiProviderRouterTest,AiProviderFailureClassifierTest,AiProviderInvocationMetricsTest,AiProviderStreamingFallbackAndCancelIntegrationTest,AgenticAuthoringProviderTelemetrySerializationTest,AgenticAuthoringProviderPricingSnapshotTest" test
```

Add controller/status tests for endpoint changes, Quickstart security tests for
rate limiting, and a real-provider probe only when credentials, model listing,
or external integration genuinely requires it. Real paid calls require explicit
scope, stopping conditions, cost expectation, and sanitized output.

Prove healthy probe/routing, classified provider failure with bounded fallback,
cancel/timeout without duplicate call, sanitized telemetry serialization,
pricing estimate reproducibility, and rate-limit denial. Review OpenAPI/docs,
workflows, environment examples, Quickstart security docs, and operational
receipts when public behavior changes.

## Companion Skills

- `praxis-config-agentic-authoring-streaming`: semantic turn/tool/stream lifecycle.
- `praxis-ai-turn-orchestration-transport`: Angular assistant transport and cancellation UX.
- `praxis-api-quickstart-security-config`: hosted endpoint protection and rate limiting.
- `praxis-api-quickstart-operational-proof`: deployed reference-host evidence.
- `praxis-core-logging-observability`: safe client/runtime diagnostics.

