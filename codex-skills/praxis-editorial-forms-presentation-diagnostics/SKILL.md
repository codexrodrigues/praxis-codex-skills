---
name: praxis-editorial-forms-presentation-diagnostics
description: Use when implementing or auditing `@praxisui/editorial-forms` fallback states, diagnostics, operational events, `solution.presentation`, layout/theme/stepper helpers, unsupported presentation keys, runtime CSS variables, stepper behavior, i18n, and visual/runtime health reporting.
---

# Praxis Editorial Forms Presentation Diagnostics

Use this skill when editorial runtime health or presentation is in scope. Presentation is a constrained `solution.presentation` projection; fallback and operational events are technical runtime evidence, not domain shortcuts.

## Source Audit

Inspect before editing:

- `projects/praxis-editorial-forms/AGENTS.md`
- `projects/praxis-editorial-forms/README.md`
- `projects/praxis-editorial-forms/docs/architecture.md`
- `projects/praxis-editorial-forms/docs/recovery-playbook.md`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-fallback.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-diagnostics.model.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-events.model.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-presentation.helpers.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-runtime-theme.helpers.ts`
- `projects/praxis-editorial-forms/src/lib/runtime/editorial-preset-resolver.ts`
- `projects/praxis-editorial-forms/src/lib/renderers/editorial-stepper.component.ts`
- `projects/praxis-editorial-forms/src/lib/i18n/*`
- fallback, theme helper, runtime component, renderer, and E2E specs

## Canonical Boundary

`solution.presentation` owns visual runtime intent. `deriveRuntimeFallbackState()` owns fallback derivation from snapshot diagnostics. `operationalEvent` owns technical telemetry for diagnostics, blocking errors, override conflicts, and adapter states.

Do not persist fallback as hidden business truth. Do not move presentation flags into host CSS, dynamic-form layout, journey blocks, `FieldMetadata`, or collected data.

## Presentation Rules

- Supported runtime layout keys include orientation, density, max width, spacing, shell variant, mobile orientation, and collapse breakpoint behavior.
- Supported stepper keys include visibility, orientation, labels/descriptions/connectors, connector style, and step jump policy.
- Theme tokens must flow through `buildRuntimeCssVars()` and valid CSS variable inputs.
- Unsupported accepted model keys must emit `presentation-config-unsupported` diagnostics instead of pretending support.
- Known diagnosed keys include `presentation.layout.contentAlign`, `presentation.layout.responsive.tabletOrientation`, `presentation.stepper.size`, `presentation.stepper.align`, and stepper variants without distinct renderer behavior.
- Presentation changes must not mutate journeys, blocks, `FormConfig`, `FieldMetadata`, or `runtimeContext.formData`.

## Fallback And Event Rules

- Fallback modes are `normal`, `warning`, `degraded`, and `blocked`.
- Blocking diagnostics are global errors or active-step errors in the current scope.
- Missing data-collection adapters require engine attention and may degrade or block based on explicit policy.
- `snapshotChange`, `fallbackChange`, and `operationalEvent` remain separate host outputs.
- `operationalEvent` is technical telemetry for logs, monitoring, and runbooks; it must not become the primary host UI contract.
- Respect `hostConfig.emitOperationalEvents` and `hostConfig.forwardAdapterOperationalEvents`.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: diagnostics/fallback exist but badges, docs, lab, or host display is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host calls a presentation token local CSS while `solution.presentation` or theme tokens already own it.
- `suportado-parcialmente`: a key exists in the model but renderer support, diagnostics, theme mapping, or validation is incomplete.
- `lacuna-real-de-contrato`: no existing presentation key, diagnostic code, fallback mode, event payload, or helper can express the requirement.

Only a real gap justifies adding public presentation keys, diagnostic codes, or event types.

## Validation

Use focused local proof:

- fallback: `src/lib/runtime/editorial-runtime-fallback.spec.ts`
- presentation/theme: `src/lib/runtime/editorial-runtime-theme.helpers.spec.ts` and presentation helper specs when present
- runtime UI diagnostics: `src/lib/editorial-form-runtime.component.spec.ts`
- stepper behavior: `src/lib/renderers/editorial-stepper.component.spec.ts`
- i18n: package i18n specs or catalog audit when text changes
- build: `npm run build:praxis-editorial-forms` when public presentation/fallback contracts change
- host/lab: E2E labs when operational events or visual runtime behavior changes

Pair with `praxis-editorial-forms-journey-snapshot-runtime` for snapshot scope and with `praxis-editorial-forms-data-collection-adapters` for adapter diagnostics.
