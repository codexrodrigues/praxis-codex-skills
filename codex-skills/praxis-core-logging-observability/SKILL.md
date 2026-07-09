---
name: praxis-core-logging-observability
description: Use when Codex must implement, audit, document, or consume `@praxisui/core` logging and observability infrastructure, including `providePraxisLogging`, `LoggerService`, logger sinks, telemetry sink, console sink, global error handler, error normalization, PII redaction, throttle/warn-once, logger config tokens, observability dashboard, alert rules, telemetry payloads, public API, or cross-lib logging guidance.
---

# Praxis Core Logging Observability

Use this skill for shared Praxis logging, telemetry, error normalization, and observability. Treat logging as governed platform infrastructure, not scattered `console.log` or host-only error handling.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/src/lib/logging/**`
- `projects/praxis-core/src/lib/services/telemetry.service.ts`
- focused `logger.service`, `provide-praxis-logging`, telemetry sink, global error handler, production contract, and observability specs
- direct consumers that emit logs, telemetry, or normalized errors

## Canonical Boundary

`@praxisui/core` owns `providePraxisLogging`, logger config tokens, logger levels, sinks, redaction policy, throttling, warn-once, normalized error shape, telemetry payload shape, global error handler integration, observability dashboard options, metrics snapshots, and alert rules.

Vertical packages own their domain context fields and event timing, but should emit through core logger/telemetry contracts. Hosts own environment-level provider choices and whether console, telemetry, global error handler, or custom sinks are enabled.

## Logging Rules

- Use `providePraxisLogging(...)` for bootstrap; do not hand-wire sinks and error handlers in each lib.
- Use `LoggerContext` fields such as `lib`, `component`, `actionId`, `correlationId`, and `feature` consistently.
- Preserve PII redaction before telemetry sink output.
- Use throttle/warn-once for noisy repeated diagnostics.
- Normalize errors before emitting telemetry. Do not expose raw thrown values or backend payloads as user-facing diagnostics.
- Keep production defaults aligned with `logging-prod-contract.spec.ts`.
- Add custom sinks through `PraxisLoggingOptions.sinks` only when they preserve `LoggerEvent` semantics.
- Observability alerts should group by declared dimensions: `global`, `lib`, `component`, or `actionId`.

## Inventory Before New Contract

Classify requests before adding logging fields or sinks:

- `ja-suportado-so-ux`: logs/alerts exist but dashboards, docs, or messages do not surface them well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local log payloads should map to `LoggerEvent`, `LoggerTelemetryPayload`, or observability snapshots.
- `suportado-parcialmente`: core supports the event but redaction, throttling, alerting, docs, or consumer adoption is incomplete.
- `lacuna-real-de-contrato`: no logger config, context, sink, telemetry payload, alert rule, or observability metric can carry the fact.

For real gaps, update logging types, defaults, specs, public API, and direct consumers together.

## Validation

Use the smallest reliable proof:

- `logger.service.spec.ts`
- `provide-praxis-logging.spec.ts`
- `praxis-global-error-handler.spec.ts`
- `telemetry-logger.sink.spec.ts`
- `logging-prod-contract.spec.ts`
- observability dashboard service/integration specs
- direct consumer specs when a lib changes log emission
- `npm run build:praxis-core` when exported contracts change

Report whether redaction, throttling, global error handling, and telemetry sink behavior were validated or skipped.

## Companion Skills

- Use `praxis-core-providers-bootstrap` for logging provider wiring.
- Use `praxis-core-runtime-contracts` when logging types or public exports change.
- Use `praxis-angular-validation-gates` for scoped test/build selection.
- Use `praxis-angular-docs-playgrounds` when public logging/observability docs or examples change.
