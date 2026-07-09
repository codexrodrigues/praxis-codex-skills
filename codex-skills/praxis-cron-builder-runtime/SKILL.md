---
name: praxis-cron-builder-runtime
description: Use when Codex must implement, audit, document, or consume `@praxisui/cron-builder` runtime surfaces, including `PdxCronBuilderComponent`, CRON editing, simple or advanced modes, presets, `CronBuilderMetadata`, `ControlValueAccessor`, validation errors, humanized descriptions, timezone-aware next-occurrence preview, locale handling, docs, examples, public API, or Angular host integration for Praxis schedule editing.
---

# Praxis Cron Builder Runtime

Use this skill for the canonical Angular CRON editor in `@praxisui/cron-builder`. Treat it as a governed schedule authoring runtime, not as a generic text field around a CRON string.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-cron-builder/AGENTS.md`
- `projects/praxis-cron-builder/README.md`
- `projects/praxis-cron-builder/src/public-api.ts`
- `projects/praxis-cron-builder/src/lib/pdx-cron-builder.component.ts`
- `projects/praxis-cron-builder/src/lib/pdx-cron-builder.component.html`
- `projects/praxis-cron-builder/src/lib/pdx-cron-builder.metadata.ts`
- `projects/praxis-cron-builder/src/lib/praxis-cron-builder.metadata.ts`
- `projects/praxis-cron-builder/src/lib/cron-runtime.ts`
- `projects/praxis-cron-builder/src/lib/schedule-authoring-runtime.ts`
- focused component, runtime, metadata, and docs manifest specs

## Canonical Boundary

`@praxisui/cron-builder` owns CRON expression editing, simple and advanced builder modes, presets, validation feedback, humanized description, next-occurrence preview, timezone and locale runtime behavior, `ControlValueAccessor`, component metadata, and the schedule authoring bridge.

Hosts own the business meaning of a schedule, persistence, authorization, scheduler execution, product-specific labels, and whether a field is editable. Do not move CRON parsing, humanization, preview, or field-count rules into hosts when the runtime package already owns them.

## Runtime Rules

- Use `PdxCronBuilderComponent` and `CronBuilderMetadata` for runtime configuration.
- Preserve `ControlValueAccessor` behavior: `writeValue`, `registerOnChange`, disabled state, touched state, and emitted compatibility value must remain form-safe.
- Support both legacy CRON strings and structured schedule configs through the package runtime. Do not make a host-local adapter the primary source of truth.
- Keep `metadata.mode` as `simple`, `advanced`, or `both`; do not fork component behavior in consumers.
- Keep presets in `metadata.presets[]` with stable label and cron values. Validate a preset before applying it.
- Use `metadata.timezone`, `metadata.locale`, `metadata.previewOccurrences`, and `metadata.previewFrom` as the preview inputs visible to the runtime.
- Generate humanized text and next occurrences from the same expression, timezone, locale, occurrence count, and from-date.
- Keep validation errors in the component/form control path. Do not hide invalid CRON values only because a preview cannot be generated.
- Treat default labels and component chrome as runtime/i18n text. Treat host domain schedule names, owners, tags, and descriptions as schedule governance data, not component labels.

## Inventory Before New Contract

Classify requested improvements before adding fields:

- `ja-suportado-so-ux`: preview, humanized text, invalid state, mode toggles, or preset display exists but is not surfaced well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: existing metadata, schedule config, dialect, timezone, or diagnostics cover the need but a consumer uses a local alias.
- `suportado-parcialmente`: the runtime supports CRON strings but the target flow needs structured schedule intent, field catalog projection, or richer form integration.
- `lacuna-real-de-contrato`: no existing metadata, schedule config, diagnostics, manifest operation, or public API can carry the behavior without losing semantic meaning.

Only introduce a public contract after identifying the canonical owner, affected consumers, docs/examples, and the smallest validation that proves the new behavior.

## Validation

Use the smallest reliable proof:

- `npm run build:praxis-cron-builder`
- `pdx-cron-builder.component.spec.ts` for CVA, modes, presets, disabled state, and form errors
- `cron-runtime.spec.ts` for parsing, validation, humanization, timezone preview, and occurrence generation
- metadata specs when component discovery changes
- docs/playground validation when public examples or manifests change
- focused consumer validation when dynamic forms, CRUD, or host projects embed the component

Report exact validation and skipped gates.

## Companion Skills

- Use `praxis-cron-schedule-authoring` for `ScheduleAuthoringConfig`, dialects, recurrence intent, normalization, compile, diagnostics, and preview contracts.
- Use `praxis-cron-builder-form-field` when the builder is registered or consumed as a metadata-driven form field.
- Use `praxis-cron-builder-ai-validation` for AI manifests, operations, read-only validation, preview generation, and registry ingestion.
- Use `praxis-angular-i18n-governance`, `praxis-angular-public-api-governance`, and `praxis-angular-docs-playgrounds` when locale, exports, docs, examples, or published guides change.
