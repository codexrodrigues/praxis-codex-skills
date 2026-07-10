---
name: praxis-navigation-agentic-registry
description: Use when Codex must implement, audit, or validate agentic AI and registry flows for Praxis navigation containers: @praxisui/tabs, @praxisui/stepper, PraxisWizardFormComponent, @praxisui/expansion, authoring manifests, AI adapters, agentic turn flows, context packs, capabilities, quick replies, diagnostics, preview/apply, component metadata, registry ingestion, docs, examples, and cross-container consistency.
---

# Praxis Navigation Agentic Registry

Use this skill for executable AI authoring and registry projection across tabs, stepper/wizard, and expansion. AI must resolve semantic edits through governed manifests, context packs, adapters, validators, and apply plans; registry output is derived evidence, not the source of truth.

Pair it with:

- `praxis-navigation-containers-ai-validation` for the broader cross-container AI checklist.
- `praxis-ai-authoring-manifests` for manifest invariants, operation schemas, target resolution, confirmations, and edit plans.
- `praxis-ai-registry-ingestion` when generated component docs, package assets, catalogs, or backend sync change.
- `praxis-tabs-runtime-authoring`, `praxis-stepper-wizard-runtime`, and `praxis-expansion-runtime-panels` for component-owned runtime/editor semantics.
- `praxis-navigation-container-composition-events` when AI operations affect nested widgets, lazy content, or widget events.
- `praxis-stepper-wizard-orchestration` when AI operations affect step validation, dynamic-form steps, wizard submit, or workflow content.

## Source Audit

Inspect:

- `projects/praxis-tabs/src/lib/ai/**`, `tabs-editor-capability*`, quick setup, config editor, and runtime specs.
- `projects/praxis-stepper/src/lib/ai/**`, stepper config editor, wizard editor/adapter/component, and runtime specs.
- `projects/praxis-expansion/src/lib/ai/**`, widget config editor, metadata provider, and runtime specs.
- `projects/*/src/lib/*metadata.ts` and `src/public-api.ts` for manifest refs and exported AI assets.
- `tools/ai-registry/**`, generated registry outputs, docs manifests, public docs, playgrounds, and AI recipes when projection changes.

## Agentic Boundary

The primary route is:

`semantic request -> component scope -> editable target -> operation schema -> validator -> handler/apply contract -> config document -> editor/runtime round-trip -> registry/docs projection`

Do not route tabs, steps, panels, or wizard actions by keywords, regexes, label matching, or arbitrary JSON patches as the primary mechanism. Text matching may rank candidates only after the semantic operation and component scope are resolved.

## Cross-Container AI Rules

- Use stable ids for target identity: tabs/link ids, step ids, panel ids, wizard ids, and component instance ids.
- Destructive operations require confirmation and safe reselection/fallback state.
- Operations that touch nested widgets must preserve delegated child contracts and `WidgetEventEnvelope` path enrichment.
- Validation operations in stepper/wizard must compile into dynamic-form metadata or host `serverValidate`; do not create a parallel hidden validation DSL.
- Render/body ownership, lazy content, and external panels must remain explicit in the config and context pack.
- Context packs should expose governed component facts, not prompt-only classifiers.
- Registry ingestion must be regenerated or validated from source manifests/metadata; never edit generated assets as canonical truth.

## Inventory Before New Contract

- `ja-suportado-so-ux`: manifest/adapters already support the operation; assistant UI, quick replies, diagnostics, docs, or registry projection needs improvement.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local prompts, keyword handlers, or broad patches are used where manifest operations and target ids already exist.
- `suportado-parcialmente`: operation exists but context pack, agentic turn flow, validator, editor parity, runtime round-trip, registry, or docs evidence is incomplete.
- `lacuna-real-de-contrato`: no editable target, operation, validator, handler/apply path, runtime config, or registry source can express the authoring decision.

Only real gaps justify new AI operations or public exports.

## Validation

Use focused gates:

- component authoring manifest specs for tabs, stepper, or expansion;
- AI adapter and agentic turn-flow specs;
- editor/runtime specs for affected operation paths;
- `npm run validate:authoring-contracts` or narrower registry validation when manifests change;
- `npm run generate:registry:ingestion` when generated registry assets or component docs must update;
- docs/playground validation when public examples or recipes change.

Report exactly which manifest, adapter, turn flow, registry, editor/runtime, and docs checks ran.
