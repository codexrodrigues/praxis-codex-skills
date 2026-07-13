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
- `projects/praxis-core/src/lib/logging/index.ts`
- `projects/praxis-core/src/lib/logging/logging.types.ts`
- `projects/praxis-core/src/lib/logging/logging.defaults.ts`
- `projects/praxis-core/src/lib/logging/logging.tokens.ts`
- `projects/praxis-core/src/lib/logging/logger.service.ts`
- `projects/praxis-core/src/lib/logging/provide-praxis-logging.ts`
- `projects/praxis-core/src/lib/logging/praxis-global-error-handler.ts`
- `projects/praxis-core/src/lib/logging/helpers/error-normalizer.helper.ts`
- `projects/praxis-core/src/lib/logging/helpers/throttle.helper.ts`
- `projects/praxis-core/src/lib/logging/helpers/warn-once.helper.ts`
- `projects/praxis-core/src/lib/logging/sinks/console-logger.sink.ts`
- `projects/praxis-core/src/lib/logging/sinks/telemetry-logger.sink.ts`
- `projects/praxis-core/src/lib/logging/observability/observability.types.ts`
- `projects/praxis-core/src/lib/logging/observability/observability.defaults.ts`
- `projects/praxis-core/src/lib/logging/observability/observability.tokens.ts`
- `projects/praxis-core/src/lib/logging/observability/observability-dashboard.service.ts`
- `projects/praxis-core/src/lib/services/telemetry.service.ts`
- `projects/praxis-core/src/lib/hooks/defaults/reportTelemetry.hook.ts`
- `projects/praxis-core/src/lib/hooks/defaults/logOnError.hook.ts`
- `projects/praxis-core/src/lib/providers/global-action-analytics.provider.ts`
- `projects/praxis-core/src/lib/providers/global-action-toast.provider.ts`
- `projects/praxis-core/src/lib/models/composition-diagnostics.model.ts`
- `tools/lint/no-console-runtime.js`
- `tools/lint/console-governance.js`
- `tools/lint/no-console-allowlist.json`
- focused `logger.service`, `provide-praxis-logging`, telemetry sink, global error handler, production contract, observability dashboard, and composition diagnostics specs
- direct consumers that emit logs, telemetry, or normalized errors

## Canonical Boundary

`@praxisui/core` owns `providePraxisLogging`, logger config tokens, logger levels, sinks, redaction policy, throttling, warn-once, normalized error shape, telemetry payload shape, global error handler integration, observability dashboard options, metrics snapshots, alert rules, console governance, telemetry hooks, and shared diagnostic model shapes.

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
- Treat direct runtime `console.*` as governed exception. Any residual console usage must be covered by `tools/lint/no-console-allowlist.json` and justified as compatibility, dev-only fallback, or intentionally host-facing output.
- Prefer `LoggerService` plus `TelemetryLoggerSink` for framework events that need auditability; use `TelemetryService` directly only for legacy hooks or explicit telemetry contracts.
- When moving an existing console diagnostic into logging, preserve the useful dimensions in `LoggerContext` instead of flattening them into message strings.

## Inventory Before New Contract

Classify requests before adding logging fields or sinks:

- `ja-suportado-so-ux`: logs/alerts exist but dashboards, docs, or messages do not surface them well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local log payloads should map to `LoggerEvent`, `LoggerTelemetryPayload`, or observability snapshots.
- `suportado-parcialmente`: core supports the event but redaction, throttling, alerting, docs, or consumer adoption is incomplete.
- `lacuna-real-de-contrato`: no logger config, context, sink, telemetry payload, alert rule, or observability metric can carry the fact.

For real gaps, update logging types, defaults, specs, public API, and direct consumers together.

## Validation

Use the smallest reliable proof:

- Core logger/provider/error/telemetry sink changes:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/logging/logger.service.spec.ts --include=projects/praxis-core/src/lib/logging/provide-praxis-logging.spec.ts --include=projects/praxis-core/src/lib/logging/praxis-global-error-handler.spec.ts --include=projects/praxis-core/src/lib/logging/sinks/telemetry-logger.sink.spec.ts --include=projects/praxis-core/src/lib/logging/logging-prod-contract.spec.ts`
- Observability dashboard, alert rules, metrics snapshots, or tokens/defaults:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/logging/observability/observability-dashboard.service.spec.ts --include=projects/praxis-core/src/lib/logging/observability/observability-dashboard.integration.spec.ts`
- Shared diagnostic model changes:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/models/composition-diagnostics.model.spec.ts`
- Runtime console cleanup or new console exception:
  - `npm run lint:no-console`
  - Review `tools/lint/no-console-allowlist.json` and keep entries tight to the residual runtime files.
- Direct consumer specs when a lib changes log/telemetry emission, for example:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts`
  - package-specific diagnostics specs such as `projects/praxis-dynamic-form/src/lib/utils/rule-authoring-diagnostics.spec.ts` or `projects/praxis-dynamic-fields/src/lib/utils/logger.spec.ts` when those packages adopt core logging.
- `npm run build:praxis-core` when exported contracts, tokens, defaults, sinks, or observability public API change.

Report whether redaction, throttling, global error handling, and telemetry sink behavior were validated or skipped.

## Companion Skills

- Use `praxis-core-providers-bootstrap` for logging provider wiring.
- Use `praxis-core-runtime-contracts` when logging types or public exports change.
- Use `praxis-angular-validation-gates` for scoped test/build selection.
- Use `praxis-angular-docs-playgrounds` when public logging/observability docs or examples change.
