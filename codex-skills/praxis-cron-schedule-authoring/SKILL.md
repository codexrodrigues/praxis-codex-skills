---
name: praxis-cron-schedule-authoring
description: Use when Codex must model, change, audit, or validate Praxis schedule semantics around `@praxisui/cron-builder`, including `ScheduleAuthoringConfig`, `CronDialect`, `CRON_DIALECTS`, recurrence intent, `normalizeScheduleValue`, `compileScheduleExpression`, `validateScheduleAuthoringConfig`, `createSchedulePreview`, legacy CRON string compatibility, timezone, locale, diagnostics, or canonical schedule authoring decisions.
---

# Praxis Cron Schedule Authoring

Use this skill when the task is about schedule meaning, not just widget rendering. Treat `ScheduleAuthoringConfig` as the canonical Praxis schedule intent model inside `@praxisui/cron-builder`.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-cron-builder/AGENTS.md`
- `projects/praxis-cron-builder/README.md`
- `projects/praxis-cron-builder/src/lib/schedule-contract.ts`
- `projects/praxis-cron-builder/src/lib/schedule-normalizer.ts`
- `projects/praxis-cron-builder/src/lib/schedule-authoring-runtime.ts`
- `projects/praxis-cron-builder/src/lib/cron-runtime.ts`
- `projects/praxis-cron-builder/src/lib/ai/praxis-cron-builder-authoring-manifest.ts`
- focused `schedule-*`, `cron-runtime`, and AI manifest specs

## Canonical Boundary

`schedule-contract.ts` owns the public schedule vocabulary:

- `ScheduleAuthoringConfig`
- `ScheduleKind`
- `ScheduleRecurrence`
- `ScheduleWindow`
- `ScheduleExecutionPolicy`
- `ScheduleGovernance`
- `ScheduleDiagnostic`
- `CronDialect`
- `CRON_DIALECTS`

`schedule-normalizer.ts` owns compatibility from legacy CRON strings to canonical schedule config. `schedule-authoring-runtime.ts` owns compile, validation, and preview orchestration. `cron-runtime.ts` owns expression parsing, humanization, and occurrence generation.

Do not create parallel host DTOs for schedule kind, dialect, timezone, preview, diagnostics, or execution policy when these contracts already carry the semantics.

## Authoring Rules

- Model business schedule intent as `kind` plus `recurrence` whenever possible.
- Use `kind='customCron'` and `expression.cron` only when the user explicitly requires a raw expression or an unsupported recurrence.
- Preserve legacy string compatibility through `normalizeScheduleValue`; do not delete the compatibility path unless the public contract is intentionally migrated.
- Compile structured recurrence with `compileScheduleExpression` before writing a canonical expression or compatibility value.
- Run `validateScheduleAuthoringConfig` before accepting recurrence, expression, window, timezone, or execution policy changes.
- Use `createSchedulePreview` for preview and diagnostics; do not manually recompute next occurrences in consumers.
- Use `CRON_DIALECTS` for field count, seconds/year support, named months/weekdays, question mark, last/nth weekday support, timezone mode, and day-of-month/day-of-week rules.
- Preserve dialect differences between Unix, Quartz, AWS EventBridge, Kubernetes CronJob, GitHub Actions schedule, and Google Cloud Scheduler.
- Keep one-time schedules explicit. Do not pretend `kind='once'` has a portable CRON representation when diagnostics say it does not.
- Keep timezone as IANA timezone metadata unless the selected dialect has fixed UTC or host-local semantics.

## Inventory Before New Contract

Classify requested behavior before adding fields:

- `ja-suportado-so-ux`: existing diagnostics, preview, recurrence, window, or governance data is not surfaced clearly.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a consumer stores CRON strings or local fields that should normalize to `ScheduleAuthoringConfig`.
- `suportado-parcialmente`: existing config carries the intent but compile, preview, i18n, docs, or form projection needs completion.
- `lacuna-real-de-contrato`: no current schedule config, dialect definition, execution policy, governance, diagnostics, or manifest operation can represent the required semantic decision.

For real contract gaps, name the canonical owner, affected package exports, consumers, docs/examples, AI manifest changes, and minimum proof before editing.

## Validation

Use the smallest reliable proof:

- `schedule-normalizer.spec.ts`
- `schedule-authoring-runtime.spec.ts`
- `cron-runtime.spec.ts`
- `pdx-cron-builder.component.spec.ts` when compile/preview affects CVA round-trip
- AI manifest/adapter specs when operations or diagnostics change
- `npm run build:praxis-cron-builder` when public types or exports change

Report exactly which dialects, schedule kinds, and invalid cases were covered.

## Companion Skills

- Use `praxis-cron-builder-runtime` for component UI, CVA, metadata, and preview rendering.
- Use `praxis-cron-builder-form-field` for metadata-driven form integration and submit payload shape.
- Use `praxis-cron-builder-ai-validation` for agentic operations, read-only validate/preview behavior, and registry contracts.
- Use `praxis-core-runtime-contracts` only if schedule semantics are intentionally promoted from the package to shared core.
