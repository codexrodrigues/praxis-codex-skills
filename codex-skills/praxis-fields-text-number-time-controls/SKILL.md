---
name: praxis-fields-text-number-time-controls
description: Use when Codex must implement, audit, or consume @praxisui/dynamic-fields or praxis-dynamic-fields package text, email, password, textarea, search, phone, URL, CPF/CNPJ, numericTextBox, currency, slider, rangeSlider, priceRange, rating, dateInput, date, dateRange, dateTimeLocal, month, week, year, time, timePicker, timeRange, inline text/number/currency/date/time/period controls, temporal bounds, masks, value shapes, formatting, and related AI profiles.
---

# Praxis Fields Text Number Time Controls

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

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
- `src/lib/ai/control-type-ai-catalog.ts` and spec
- `src/lib/catalog/dynamic-fields-playground.catalog.ts`
- `src/lib/catalog/catalog-derivation.spec.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.spec.ts`
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- relevant `src/lib/editorial/wave1/*.editorial.ts`
- `src/lib/services/date-utils.service.ts` and spec
- `src/lib/utils/format-display.util.ts` and spec
- `src/lib/utils/numeric-presentation.util.ts` and spec
- `src/lib/utils/inline-display-mask.util.ts` and spec
- `src/lib/utils/json-schema-mapper.ts` and spec when schema/type projection changes
- `src/lib/utils/field-state.util.ts`, `clear-button.util.ts`, and `error-state-matcher.ts` when control state UX changes
- `src/lib/examples/date-range-corporate-usage.example.ts` when date range shortcuts or business periods change
- wrapper-owner skills when the control delegates to another package, such as upload, rich content, or CRON/schedule fields
- focused component and profile specs

## Canonical Families

- Text: `input`, `email`, `password`, `textarea`, `search`, `phone`, `url`, `inlineInput`, and inline phone behavior.
- Regional document: `cpfCnpjInput`, with mask and checksum semantics.
- Numeric/currency: `numericTextBox`, `currency`, `slider`, `rangeSlider`, `priceRange`, `rating`, `inlineNumber`, `inlineCurrency`, `inlineCurrencyRange`, `inlineRange`, `inlineRating`, `inlineDistanceRadius`, and `inlineScorePriority`.
- Temporal: `dateInput`, `date`, `dateRange`, `dateTimeLocal`, `month`, `week`, `year`, `time`, `timePicker`, `timeRange`, `inlineDate`, `inlineDateRange`, `inlineTime`, `inlineTimeRange`, `inlinePeriodRange`, `inlineYearRange`, `inlineMonthRange`, and `inlineRelativePeriod`.
- Wrapper fields: upload, rich-content, and CRON/schedule controls may be registered or discovered through dynamic-fields, but their value shape, security, authoring model, and package runtime are owned by their specialized package skills.

## Runtime Rules

- Preserve canonical value shapes from docs/catalogs. Do not substitute display masks or labels as submitted values.
- Phone/document masks may change display, but raw submitted semantics must remain canonical.
- Currency/range components may have internal UI states; backend payload shape is governed by form/filter contracts and range normalizers.
- Time values should prefer `HH:mm`; compatible internal formats do not make those formats the recommended contract.
- Date/time range controls require distinct start/end semantics and ordered values.
- Date, month, week, year, and date-time controls must route shared parsing/default-format decisions through `DateUtilsService` or the owning component contract; do not fork host-local date parsing.
- Numeric and currency display decisions should use `numeric-presentation` or documented component metadata, not ad hoc pipes in consumers.
- Inline display-only masks should use `inline-display-mask` and preserve the submitted value shape.
- Visual numeric controls such as rating, score, and distance must keep text labels or accessible names; color/star/graphic affordance is never the only semantic channel.
- Inline temporal/numeric controls use `inlineOverlay` where draft state exists.
- Do not collapse wrapper field payloads into scalar text just because the host form submits through dynamic-form. Use the wrapper package contract and then verify dynamic-form payload projection.

## Inventory Before New Contract

- `ja-suportado-so-ux`: metadata exists but formatting, placeholder, validation message, preview, or docs are weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host uses local masks, aliases, range keys, or CSS where canonical `FieldMetadata`, value presentation, or inline contracts already exist.
- `suportado-parcialmente`: runtime renders but metadata-editor, catalog, JSON API, AI profile, submit, or inline overlay behavior is incomplete.
- `lacuna-real-de-contrato`: no current control type, metadata path, value shape, formatter, validator, profile, or docs can express the needed scalar/temporal decision.

Only real gaps justify new public metadata. Prefer completing the canonical control/editor/profile chain.

## Validation

Use focused gates:

- Text/document controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/text-input/text-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/text-input/text-input.transform.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/email-input/email-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/password-input/password-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-textarea/material-textarea.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/search-input/search-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/phone-input/phone-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/url-input/url-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-cpf-cnpj-input/material-cpf-cnpj-input.component.spec.ts`
- Numeric/currency/range controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/number-input/number-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-currency/material-currency.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-number/inline-number.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-currency/inline-currency.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-currency-range/inline-currency-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-slider/material-slider.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-range-slider/material-range-slider.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-price-range/material-price-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-rating/material-rating.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-rating/inline-rating.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-distance-radius/inline-distance-radius.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-score-priority/inline-score-priority.component.spec.ts`
- Temporal controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/services/date-utils.service.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/date-input/date-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-datepicker/material-datepicker.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-date-range/material-date-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/datetime-local-input/datetime-local-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/month-input/month-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/week-input/week-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/pdx-year-input/pdx-year-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/time-input/time-input.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-timepicker/material-timepicker.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/pdx-material-time-range/pdx-material-time-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-date/inline-date.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-date-range/inline-date-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-time/inline-time.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-time-range/inline-time-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-period-range/inline-period-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-year-range/inline-year-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-month-range/inline-month-range.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-relative-period/inline-relative-period.component.spec.ts`
- Shared formatting, masks, schema mapping, or state utilities:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/utils/format-display.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/numeric-presentation.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/inline-display-mask.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/json-schema-mapper.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/field-state.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/clear-button.util.spec.ts --include=projects/praxis-dynamic-fields/src/lib/utils/error-state-matcher.spec.ts`
- Registry/loader changes:
  - Run the focused gates from `praxis-fields-runtime-loader`.
- Metadata/editorial/catalog discovery changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts`
- AI profile changes:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts`
- Form submit or filter payload tests when value shape changes.
- Playwright for inline overlay/range/date/time visual interactions, especially `inline-number-real-usage.playwright.spec.ts`, `inline-date-range-visual.playwright.spec.ts`, `inline-date-range-business-shortcuts.playwright.spec.ts`, `inline-layout-overflow.playwright.spec.ts`, and `inline-all-components-smoke.playwright.spec.ts`.
- Wrapper package tests plus dynamic-fields registration/discovery tests when a wrapper control is involved.
- `npm run build:praxis-dynamic-fields` when public exports, metadata contracts, AI profiles, or package-owned control coverage changes.

State which runtime, metadata/editorial, value-shape, AI profile, and submit/filter checks were run.
