---
name: praxis-list-ai-validation
description: Use when changing or validating `@praxisui/list` AI authoring: `PRAXIS_LIST_AUTHORING_MANIFEST`, list AI capabilities, context packs, AI adapter, agentic turn flow, component edit plans, declared-only warnings, registry ingestion, backend grounding, and assistant validation for list/card/tile configs.
---

# Praxis List AI Validation

Use this skill for assistant-driven and agentic authoring of `@praxisui/list`. The public AI contract is the list authoring manifest and its executable operations, not free-form JSON patches.

Use `praxis-ai-authoring-manifests` for shared manifest rules, `praxis-ai-registry-ingestion` for generated registry artifacts, `praxis-ai-semantic-intent` for intent boundaries, and `praxis-list-authoring-settings` for visual editor parity.

## Required Source Audit

Inspect:

- `projects/praxis-list/AGENTS.md`
- `src/lib/ai/praxis-list-authoring-manifest.ts`
- `src/lib/ai/list-ai-capabilities.ts`
- `src/lib/ai/list-ai.adapter.ts`
- `src/lib/ai/list-context-pack.ts`
- `src/lib/ai/list-agentic-authoring-turn-flow.ts`
- `src/lib/ai/README_CAPABILITIES.md`
- `src/lib/ai/*.spec.ts`
- `src/lib/praxis-list.metadata.ts`
- `docs/praxis-docs.manifest.json`

## Canonical AI Boundary

List AI authoring must compile intent into manifest-backed component edit plans. Do not route prompts through local keyword lists or emit arbitrary JSON patches.

Ground edit decisions in:

- active `PraxisListConfig`
- manifest operations and schemas
- list capability catalog
- safe context pack facts
- runtime/editor support status from README and json-api docs
- backend/domain metadata when the list is resource-bound

Treat `visual-only` list operations such as `item.primaryText.set`, `item.secondaryText.set`, `item.avatar.configure`, `item.badge.configure`, row layout, layout density, i18n, and a11y presentation as list rendering materialization only. They may bind fields, expressions, labels, badges, chips, avatars, spacing, density, and accessibility hints, but they must not classify records, synthesize status/eligibility patches, create `domain-rules`, infer `backend_validation`, or become item authorization/business policy. Treat `events.map` as declarative host event wiring, not as proof that an event handler, workflow, or backend side effect exists.

Treat `item.action.add` and `item.action.update` as list action configuration only. `actions[].globalAction.actionId`, `payload`, `payloadExpr`, `confirmation`, `showIf`, `emitLocal`, and `actionClick` may declare or delegate an interaction through the host/global action runtime, but they do not prove that a handler, workflow, permission, backend mutation, or authorization policy exists. Ground global action ids and payloads in the declared catalog/registry when available; otherwise keep the action declarative and open the owning integration/platform follow-up instead of encoding host-local command behavior in the list config.

Keep list data-source authoring explicit. `data.local.set` creates inline/local data for examples, previews, or intentionally local lists, and `dataSource.data` takes precedence over `dataSource.resourcePath` at runtime. `data.resource.bind` is the canonical remote binding operation and must account for local data via `clearLocalData`/`local-remote-precedence-safe`; do not leave sample rows in the config as proof of a remote API contract, and do not replace a requested remote resource with fabricated local rows unless the user explicitly asked for local example content.

## Declared-Only Protection

The manifest and context pack must not imply full authorability for fields that are only declared or partially runtime-proven. Maintain warnings for:

- `layout.virtualScroll`
- `layout.stickySectionHeader`
- `actions[].emitPayload`
- `events.*`
- `a11y.highContrast`
- `a11y.reduceMotion`

If AI needs to author one of these as active behavior, first implement the runtime/editor contract and update docs and tests.

## Capability Coverage

When adding or changing authorable paths, check:

- capability catalog paths and allowed values
- manifest operation input schema
- handler/adapter behavior
- context pack projection
- editor parity for the same path
- registry ingestion output
- focused specs proving path-level coverage

Do not rely on a broad parent path such as `templating` or `actions` as proof that every nested path can be safely edited.

## Validation

Minimum gates:

- manifest changes: `src/lib/ai/praxis-list-authoring-manifest.spec.ts`
- adapter changes: `src/lib/ai/list-ai.adapter.spec.ts`
- turn flow changes: `src/lib/ai/list-agentic-authoring-turn-flow.spec.ts`
- component metadata changes: `src/lib/praxis-list.metadata.spec.ts`
- registry projection: `npm run generate:registry:ingestion` when manifest, component docs, or metadata affects AI registry
- browser assistant proof: `test-dev/e2e/list-authoring-canonical.playwright.spec.ts` when the visible assistant/editor flow changes

Use `praxis-angular-validation-gates` to choose the smallest sufficient local proof and state if registry, browser, or backend sync was not run.
