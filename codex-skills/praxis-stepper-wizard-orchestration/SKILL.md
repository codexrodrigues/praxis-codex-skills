---
name: praxis-stepper-wizard-orchestration
description: Use when Codex must implement, audit, or consume @praxisui/stepper workflow orchestration: dynamic-form steps, canonical resourcePath, linear navigation, serverValidate, validateStep, nextWithValidation, stepFormReady/value events, WizardFormConfig, PraxisWizardFormComponent, buildStepperConfig, wizard normalization/migrations/validation, submit/completed/customAction outputs, preferences, rich step content, and host submit boundaries.
---

# Praxis Stepper Wizard Orchestration

Use this skill for multi-step workflow execution and the wizard adapter layer. Stepper owns workflow navigation and step composition; dynamic-form owns form semantics; the host owns domain submit, remote validation implementation, authorization, and durable domain state.

Pair it with:

- `praxis-stepper-wizard-runtime` for the broad stepper/wizard runtime.
- `praxis-form-runtime-submit` for dynamic-form submission, hooks, schemas, and resource path boundaries.
- `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters` for rich step content and legacy wizard block convergence.
- `praxis-navigation-container-composition-events` for nested widgets and step-aware event paths.
- `praxis-navigation-agentic-registry` when AI operations author workflow, validation, or wizard content.

## Source Audit

Inspect:

- `projects/praxis-stepper/AGENTS.md`
- `projects/praxis-stepper/README.md`
- `projects/praxis-stepper/docs/host-stepper-integration.md`
- `projects/praxis-stepper/docs/stepper-api-reference.md`
- `projects/praxis-stepper/src/lib/praxis-stepper.ts`
- `projects/praxis-stepper/src/lib/praxis-stepper.spec.ts`
- `projects/praxis-stepper/src/lib/wizard/praxis-wizard-form.component.ts`
- `projects/praxis-stepper/src/lib/wizard/praxis-wizard-form.adapter.ts`
- `projects/praxis-stepper/src/lib/wizard/wizard-config.*`
- focused wizard component, adapter, normalizer, validator, migration, rich-content, and editor specs.

## Canonical Boundary

`StepperMetadata` is the runtime workflow document. `WizardFormConfig` is a higher-level adapter contract that compiles through `buildStepperConfig` into `StepperMetadata` and form config. Do not make hosts reverse-engineer generated stepper config or encode workflow rules in local button labels, command strings, or route guards when stepper/wizard contracts own them.

## Orchestration Rules

- `steps[].form.resourcePath` must remain a canonical resource path such as `domain/resource`; no `/api`, `/filter`, `/{id}`, operation URL, or query string.
- `linear=true` plus form validity is the normal client-side progression gate.
- `serverValidate` is the host-owned remote gate; stepper must not define a hidden validation DSL.
- `validateStep` and `nextWithValidation` must preserve async error handling and selected-step semantics.
- `stepFormReady` and `stepFormValueChange` are the canonical form bridge events.
- Wizard submit/completed/customAction outputs must include wizard id, selected step context, and collected values without forcing host introspection into child forms.
- Wizard preferences and local persistence must stay scoped by `wizardId` or explicit storage key.
- Rich content should flow through `stepBlocksBeforeForm`, `stepBlocksAfterForm`, and `RichContentDocument` where possible; legacy wizard blocks are adapter input, not the preferred new content model.

## Inventory Before New Contract

- `ja-suportado-so-ux`: orchestration exists but host wiring, docs, diagnostics, or UX affordance is weak.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host uses operation URLs, local validation labels, or direct child-form introspection where canonical resource paths, `serverValidate`, or step events already exist.
- `suportado-parcialmente`: stepper/wizard supports the flow but adapter, normalizer, validation, migration, rich-content mapping, AI manifest, or tests are incomplete.
- `lacuna-real-de-contrato`: no stepper, wizard, dynamic-form, rich-content, or host validation contract can express the workflow decision.

Only real gaps justify public contract changes.

## Validation

Use focused gates:

- `praxis-stepper.spec.ts` for linear validation, selection, form events, and widget events;
- `praxis-wizard-form.component.spec.ts` for submit/completed/customAction and preference behavior;
- `praxis-wizard-form.adapter.spec.ts` for `WizardFormConfig -> StepperMetadata`;
- wizard normalizer, validator, migration, and rich-content specs when those paths change;
- dynamic-form integration checks when resourcePath, submit, form events, or server validation change.

Report exactly which runtime, wizard, form, rich-content, and host-boundary checks ran.
