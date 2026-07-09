---
name: praxis-cron-builder-form-field
description: Use when Codex must wire, audit, document, or author `@praxisui/cron-builder` as a Praxis form or metadata-driven field, including `ControlValueAccessor` integration, dynamic-form or dynamic-fields catalog registration, field metadata, submit payload shape, legacy CRON string versus `ScheduleAuthoringConfig` values, validation errors, locale/timezone inputs, CRUD forms, docs, examples, or host form integration.
---

# Praxis Cron Builder Form Field

Use this skill when the CRON builder participates in forms, CRUD screens, metadata-driven UI, or field catalogs. Treat the form field as a projection of canonical schedule authoring semantics, not as a host-specific text input.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-cron-builder/AGENTS.md`
- `projects/praxis-cron-builder/README.md`
- `projects/praxis-cron-builder/src/public-api.ts`
- `projects/praxis-cron-builder/src/lib/pdx-cron-builder.component.ts`
- `projects/praxis-cron-builder/src/lib/pdx-cron-builder.metadata.ts`
- `projects/praxis-cron-builder/src/lib/praxis-cron-builder.metadata.ts`
- `projects/praxis-cron-builder/src/lib/schedule-contract.ts`
- `projects/praxis-dynamic-fields/**` when catalog or field discovery changes
- `projects/praxis-dynamic-form/**`, CRUD examples, docs, and playground consumers that submit schedule values

## Canonical Boundary

`@praxisui/cron-builder` owns the field runtime, CVA behavior, CRON validation, schedule preview, and component metadata. Dynamic Fields and Dynamic Form own field discovery, form rendering, layout, validation aggregation, and submit orchestration. Backend metadata owns whether the field stores a legacy CRON string or a structured schedule config.

Do not invent a local form adapter that reinterprets schedule semantics. If a metadata-driven form needs richer schedule values, project the canonical `ScheduleAuthoringConfig` or explicitly preserve legacy CRON string compatibility.

## Form Rules

- Choose the value shape from the backend/form contract before wiring the field.
- Use legacy CRON string values when the public API or existing backend contract still expects a string.
- Use `ScheduleAuthoringConfig` when the flow needs schedule kind, recurrence, dialect, timezone, preview, window, execution policy, or governance metadata.
- Keep `ControlValueAccessor` as the integration point for Angular forms; do not bypass it with host-local event plumbing.
- Propagate disabled state, touched state, validation errors, and form control status.
- Feed timezone, locale, preview count, presets, and mode through `CronBuilderMetadata`.
- Keep user-facing internal editor labels on the i18n path. Keep domain schedule labels, owners, and tags in schedule governance or host data.
- Preserve form submit payload shape when introducing structured schedule authoring. Update examples/docs in the same cycle when the public shape changes.

## Metadata Rules

- Register the component through the package metadata provider when dynamic widget loaders, Page Builder, or field catalogs need discovery.
- Do not encode CRON parsing or next-run preview as field catalog heuristics. The catalog should identify the component and config; the package runtime should evaluate the expression.
- When metadata lacks a required value shape, classify the gap before adding a new field:
  - `ja-suportado-so-ux`
  - `ja-suportado-mal-nomeado-ou-mal-materializado`
  - `suportado-parcialmente`
  - `lacuna-real-de-contrato`
- For `lacuna-real-de-contrato`, name the canonical metadata source, consumers, docs/examples, generated artifacts, and validation proof.

## Validation

Use the smallest reliable proof:

- `pdx-cron-builder.component.spec.ts` for CVA round-trip, disabled state, validation errors, mode behavior, and metadata inputs
- metadata provider specs when registration or catalog data changes
- dynamic-fields or dynamic-form focused specs when discovery, rendering, or submit payload changes
- CRUD or host screen validation when schedule values are persisted through a real form
- docs/playground validation when examples or public recipes change

Report exact value-shape assumptions and skipped consumers.

## Companion Skills

- Use `praxis-cron-builder-runtime` for the underlying component, preview, presets, locale, and timezone behavior.
- Use `praxis-cron-schedule-authoring` for canonical schedule config, recurrence, dialects, compile, and diagnostics.
- Use `praxis-form-runtime-submit`, `praxis-dynamic-fields-editorial`, and `praxis-crud-runtime-openmodes` when form metadata, field catalog, submit payload, or CRUD flows are affected.
- Use `praxis-cron-builder-ai-validation` when AI-authored schedule values are applied through a form.
