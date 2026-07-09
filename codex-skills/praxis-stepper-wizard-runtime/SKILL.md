---
name: praxis-stepper-wizard-runtime
description: Use when Codex must implement, audit, document, or author `@praxisui/stepper` or `PraxisWizardFormComponent` flows, including `stepperId` persistence, linear step validation, dynamic-form step integration, canonical `resourcePath`, rich step content, server validation, wizard config normalization, Settings Panel editors, widget events, AI authoring manifests, docs, examples, or host integration for Praxis multi-step experiences.
---

# Praxis Stepper Wizard Runtime

Use this skill for the canonical `@praxisui/stepper` runtime and the experimental wizard wrapper. Treat the stepper as a governed multi-step workflow surface, not as a local Material Stepper composition.

## Source Audit

Before editing code or guidance, inspect the relevant source:

- `projects/praxis-stepper/AGENTS.md`
- `projects/praxis-stepper/README.md`
- `projects/praxis-stepper/docs/host-stepper-integration.md`
- `projects/praxis-stepper/docs/stepper-api-reference.md`
- `projects/praxis-stepper/src/public-api.ts`
- `projects/praxis-stepper/src/lib/praxis-stepper.ts`
- `projects/praxis-stepper/src/lib/praxis-stepper.spec.ts`
- `projects/praxis-stepper/src/lib/praxis-stepper-config-editor*`
- `projects/praxis-stepper/src/lib/wizard/**`
- `projects/praxis-stepper/src/lib/ai/**`

If public docs, registry, playgrounds, or examples mention stepper or wizard flows, also audit those derived artifacts before declaring the issue complete.

## Canonical Boundary

`@praxisui/stepper` owns:

- `StepperMetadata`, `StepConfig`, orientation, header, linear, navigation, density, classes, appearance, and icons
- `stepperId`, `componentInstanceId`, and persistence through `ASYNC_CONFIG_STORAGE`
- step selection, `selectedIndexChange`, `selectionChange`, and Material animation events
- dynamic-form step embedding through `steps[].form`
- rich step content through `stepBlocksBeforeForm` and `stepBlocksAfterForm`
- advanced host-owned widgets through `steps[].widgets`
- `serverValidate`, `validateStep`, and `nextWithValidation`
- `widgetEvent` propagation from nested widgets with step-aware path context
- Settings Panel config editor, AI assistant integration, and `PRAXIS_STEPPER_AUTHORING_MANIFEST`
- `PraxisWizardFormComponent` as the higher-level wizard adapter that maps `WizardFormConfig` into `StepperMetadata`

Hosts consume these contracts. Do not move linear validation, form step mapping, wizard normalization, or canonical `resourcePath` handling into app-local steppers when the lib owns the workflow semantics.

## Runtime Rules

- Require a stable `stepperId` for persisted or customizable flows. Add `componentInstanceId` for repeated instances on one route.
- Keep `steps[].id` stable. Authoring, widget paths, validation, and wizard mapping should resolve by id before label or index.
- Pass dynamic-form `resourcePath` as a canonical base resource path, such as `domain/resource`; do not include `/api`, `/filter`, `/{id}`, schema endpoints, operation URLs, or query strings.
- Use `linear=true` plus form `FormGroup` validity for normal blocking behavior. Use `serverValidate` for remote validation instead of inventing a parallel validation DSL in stepper config.
- Prefer `stepBlocksBeforeForm` and `stepBlocksAfterForm` for editorial content. Use `steps[].widgets` only for advanced host-owned widgets after the canonical rich content path is unsuitable.
- Pair with `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters` when step rich content changes; new editorial content should prefer `RichContentDocument` over legacy wizard blocks.
- Keep navigation config as workflow chrome. Do not encode business approval rules as button labels, local command strings, or keyword-routed step actions.
- Forward nested widget events through `widgetEvent` instead of host-local event buses.

## Wizard Rules

- Use `PraxisWizardFormComponent` when the input is a higher-level wizard document rather than raw stepper config.
- Treat `buildStepperConfig`, wizard normalizers, migrations, validators, and form submission outputs as the canonical adapter path.
- Preserve the current `zones` precedence over legacy `blocks` when both exist, avoiding duplicate rendered content.
- Keep wizard output events such as submit/completed/custom action aligned with the wrapper contract. Do not force host code to reverse-engineer generated `StepperMetadata`.
- If the wizard cannot express a required flow, classify the gap before adding fields. Promote real contract gaps to the wizard/stepper owner, not a consuming app.

## Authoring Rules

- Use `PraxisStepperConfigEditor`, widget config editor, manifest capabilities, context packs, and `PRAXIS_STEPPER_AUTHORING_MANIFEST` for governed authoring.
- Keep Settings Panel apply/save/reset/reopen aligned with runtime config consumption.
- Keep i18n for authoring chrome and assistant labels in the package i18n path.
- When AI authors step changes, ensure operations target stable steps and preserve validation/persistence semantics.
- If a requested edit cannot be represented by the existing manifest or editor capability, classify it as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato` before adding a contract.

## Validation

Use the smallest reliable proof for the touched surface:

- `npm run build:praxis-stepper` or the repo's equivalent focal build
- focused specs for stepper runtime, config editor, wizard component, wizard adapter, normalizer, validator, and migrations
- dynamic-form integration validation when `steps[].form`, `resourcePath`, submit, or form events change
- Settings Panel round-trip validation when config editor behavior changes
- AI registry or authoring manifest validation when `ai/**`, capabilities, manifest refs, or registry docs change
- docs/playground validation when public examples or docs are updated

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-form-runtime-submit` for dynamic-form step integration, submit behavior, hooks, schema metadata, and resource path boundaries.
- Use `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters` for step rich content, wizard legacy block convergence, and `stepBlocksBeforeForm`/`stepBlocksAfterForm` semantics.
- Use `praxis-navigation-containers-ai-validation` for stepper AI manifests, registry projection, context packs, assistant turns, and cross-container validation.
- Use `praxis-authoring-editors` for Settings Panel editor round-trip.
- Use `praxis-core-composition-runtime` for nested widgets, widget events, composition links, and dynamic page materialization.
- Use `praxis-angular-i18n-governance`, `praxis-angular-public-api-governance`, `praxis-angular-docs-playgrounds`, and `praxis-angular-validation-gates` when the change touches their governed areas.
