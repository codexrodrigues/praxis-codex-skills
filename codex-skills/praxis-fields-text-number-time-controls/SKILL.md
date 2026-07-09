---
name: praxis-fields-text-number-time-controls
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields text, email, password, textarea, search, phone, URL, CPF/CNPJ, numericTextBox, currency, slider, rangeSlider, priceRange, rating, dateInput, date, dateRange, dateTimeLocal, month, week, year, time, timePicker, timeRange, inline text/number/currency/date/time/period controls, temporal bounds, masks, value shapes, formatting, and related AI profiles.
---

# Praxis Fields Text Number Time Controls

Use this skill for scalar and temporal control families in `@praxisui/dynamic-fields`: text-like inputs, regional documents, numbers, currency, sliders/ranges, dates, times, periods, and their inline variants.

Pair it with:

- `praxis-fields-runtime-loader` for component registration and loader behavior.
- `praxis-fields-editorial-discovery` for metadata, catalog, JSON API docs, and field selection guidance.
- `praxis-fields-inline-overlay-runtime` for inline compact/pill behavior, draft state, and Apply/Cancel/Clear.
- `praxis-fields-control-profile-ai` for AI profile operations such as `field.text.configure`, `field.numeric.configure`, `field.currency.configure`, `field.date.configure`, `field.dateRange.configure`, and `field.timeRange.configure`.
- `praxis-form-runtime-submit` when value shape affects submit payloads.

## Source Audit

Inspect:

- `projects/praxis-dynamic-fields/AGENTS.md`
- `README.md`
- `docs/dynamic-fields-field-catalog.md`
- `docs/dynamic-fields-field-selection-guide.md`
- `docs/dynamic-fields-inline-filter-runtime-contract.md`
- relevant component folder under `src/lib/components/**`
- relevant `*.metadata.ts` and `*.json-api.md`
- `src/lib/ai/text-inputs-ai-capabilities.ts`
- `src/lib/ai/numeric-inputs-ai-capabilities.ts`
- `src/lib/ai/date-controls-ai-capabilities.ts`
- `src/lib/ai/time-range-ai-capabilities.ts`
- `src/lib/ai/price-range-ai-capabilities.ts`
- `src/lib/ai/brazil-inputs-ai-capabilities.ts`
- focused component and profile specs

## Canonical Families

- Text: `input`, `email`, `password`, `textarea`, `search`, `phone`, `url`, `inlineInput`, and inline phone behavior.
- Regional document: `cpfCnpjInput`, with mask and checksum semantics.
- Numeric/currency: `numericTextBox`, `currency`, `slider`, `rangeSlider`, `priceRange`, `rating`, `inlineNumber`, `inlineCurrency`, `inlineCurrencyRange`, `inlineRange`, `inlineRating`, `inlineDistanceRadius`, and `inlineScorePriority`.
- Temporal: `dateInput`, `date`, `dateRange`, `dateTimeLocal`, `month`, `week`, `year`, `time`, `timePicker`, `timeRange`, `inlineDate`, `inlineDateRange`, `inlineTime`, `inlineTimeRange`, `inlinePeriodRange`, `inlineYearRange`, `inlineMonthRange`, and `inlineRelativePeriod`.

## Runtime Rules

- Preserve canonical value shapes from docs/catalogs. Do not substitute display masks or labels as submitted values.
- Phone/document masks may change display, but raw submitted semantics must remain canonical.
- Currency/range components may have internal UI states; backend payload shape is governed by form/filter contracts and range normalizers.
- Time values should prefer `HH:mm`; compatible internal formats do not make those formats the recommended contract.
- Date/time range controls require distinct start/end semantics and ordered values.
- Visual numeric controls such as rating, score, and distance must keep text labels or accessible names; color/star/graphic affordance is never the only semantic channel.
- Inline temporal/numeric controls use `inlineOverlay` where draft state exists.

## Inventory Before New Contract

- `ja-suportado-so-ux`: metadata exists but formatting, placeholder, validation message, preview, or docs are weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host uses local masks, aliases, range keys, or CSS where canonical `FieldMetadata`, value presentation, or inline contracts already exist.
- `suportado-parcialmente`: runtime renders but metadata-editor, catalog, JSON API, AI profile, submit, or inline overlay behavior is incomplete.
- `lacuna-real-de-contrato`: no current control type, metadata path, value shape, formatter, validator, profile, or docs can express the needed scalar/temporal decision.

Only real gaps justify new public metadata. Prefer completing the canonical control/editor/profile chain.

## Validation

Use focused gates:

- component specs for the affected control;
- `ComponentRegistryService` and loader specs when control resolution changes;
- metadata/editorial/catalog specs when discovery changes;
- profile/catalog specs when AI guidance changes;
- form submit or filter payload tests when value shape changes;
- Playwright for inline overlay/range/date/time visual interactions.

State which runtime, metadata/editorial, value-shape, AI profile, and submit/filter checks were run.
