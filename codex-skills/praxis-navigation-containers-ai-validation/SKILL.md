---
name: praxis-navigation-containers-ai-validation
description: Use when Codex must change, audit, or validate AI-assisted authoring for Praxis navigation and disclosure containers such as `@praxisui/tabs`, `@praxisui/stepper`, `PraxisWizardFormComponent`, and `@praxisui/expansion`, including authoring manifests, AI adapters, agentic turn flows, capabilities, context packs, component registry ingestion, widget events, Settings Panel round-trip, i18n, docs, examples, or cross-container authoring consistency.
---

# Praxis Navigation Containers AI Validation

Use this skill for AI authoring and registry validation across tabs, stepper/wizard, and expansion. It does not replace the owning runtime skill; pair it with the specific component skill.

## Source Audit

Audit the component owner first:

- Tabs: `projects/praxis-tabs/AGENTS.md`, `README.md`, `src/public-api.ts`, `src/lib/praxis-tabs.ts`, `src/lib/ai/**`, editor capability, quick setup, and focused specs.
- Stepper: `projects/praxis-stepper/AGENTS.md`, `README.md`, `docs/**`, `src/public-api.ts`, `src/lib/praxis-stepper.ts`, `src/lib/wizard/**`, `src/lib/ai/**`, and focused specs.
- Expansion: `projects/praxis-expansion/AGENTS.md`, `README.md`, `src/public-api.ts`, `src/lib/praxis-expansion.ts`, `src/lib/praxis-expansion.metadata.ts`, `src/lib/ai/**`, and focused specs.

Then audit shared or derived surfaces when touched:

- `tools/ai-registry/**`
- generated or packaged `ai/component-registry.json` assets
- docs manifests, public docs, playgrounds, recipes, and AI examples
- Settings Panel editor hosts and widget config editor metadata
- i18n catalogs for assistant and authoring chrome

## Canonical Decision Boundary

AI authoring for these containers must operate through governed manifests, adapters, capabilities, and semantic context. Do not route intent through keywords, regexes, label matching, command strings, or free JSON patch generation as the primary decision mechanism.

Text matching may rank a tab, step, link, or panel only after the semantic operation and component scope are resolved by the manifest, context pack, or declared tool contract.

## Cross-Container Invariants

- Stable ids are mandatory authoring anchors: `tabs[].id`, `nav.links[].id`, `steps[].id`, and `panels[].id`.
- The component id is mandatory for persistence scopes: `tabsId`, `stepperId`, and `expansionId`.
- Nested widget events must remain `WidgetEventEnvelope` events with container-aware path segments; do not flatten them into app-local callback names.
- Settings Panel editors must emit the owning component's canonical input patch or config document, not a host wrapper.
- AI manifests must describe executable operations, targets, validators, affected paths, destructive confirmation, and submission impact. They are contracts, not prose-only docs.
- Context packs and assistant adapters should expose safe component facts, not local prompt classifiers.
- Registry ingestion is a derived artifact. Update source metadata/manifests first, then regenerate or validate the registry path.

## Component Routing

- Use `praxis-tabs-runtime-authoring` for group/nav mode, `renderBody`, quick setup, tab/link selection, and tabs persistence.
- Use `praxis-stepper-wizard-runtime` for workflow validation, dynamic-form steps, wizard config normalization, and submit/completed/custom action flows.
- Use `praxis-expansion-runtime-panels` for accordion defaults, provider registration, panel events, lazy panel content, and imperative panel methods.
- Use `praxis-navigation-container-composition-events` when AI operations affect nested widgets, lazy content, dynamic page embedding, widget events, external body ownership, or composition links.
- Use `praxis-stepper-wizard-orchestration` when AI operations affect dynamic-form steps, resource paths, validation, wizard adapter behavior, submit/completed/customAction, or host workflow boundaries.
- Use `praxis-navigation-agentic-registry` for AI adapters, agentic turn flows, context packs, registry projection, generated docs, and cross-container authoring consistency.
- Use `praxis-ai-authoring-manifests` for manifest schema, operation safety, target resolution, apply plans, and declared authoring contracts.
- Use `praxis-ai-registry-ingestion` when component docs, manifests, capabilities, context packs, or registry assets change.

## AI Authoring Checks

Before considering an AI authoring change complete, verify:

- The operation is represented in the owning manifest or explicitly classified as a real contract gap.
- Target resolution uses stable canonical ids and handles ambiguity without guessing.
- Destructive operations require confirmation and preserve safe reselection or fallback state.
- Runtime/editor/apply/persistence semantics remain aligned after assistant application.
- The assistant UI receives meaningful turn state, quick replies, diagnostics, preview, and apply outcome where that flow exists.
- Public API exports expose only intentional package-owned symbols.
- Registry, docs, examples, and playgrounds are either updated or explicitly ruled out as unaffected.

## Validation

Use the smallest reliable proof for the changed surface:

- focused component specs for AI adapters, agentic turn flows, editor capability, widget events, and runtime operation effects
- `npm run validate:authoring-contracts` when authoring contracts change
- `npm run generate:registry:ingestion` or narrower registry validation when extracted metadata, capabilities, or registry assets change
- focal package build for the owning lib
- Settings Panel round-trip validation when apply/save/reset behavior changes
- docs/playground validation when public docs or examples change

If local Node dependencies or platform binaries cannot run, perform a structural audit and state the unvalidated gate clearly.

## Anti-Patterns

- Do not create a second AI operation language for tabs, stepper, wizard, or expansion.
- Do not use label text as the primary target identity when ids exist.
- Do not let a host app bypass manifest operations with arbitrary JSON patches.
- Do not treat registry output as source of truth.
- Do not encode business rules in visual container chrome when metadata, form validation, workflow, actions, or semantic decisions own them.
