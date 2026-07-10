---
name: praxis-page-builder-ai-agentic
description: Use when Codex must create, update, or audit @praxisui/page-builder AI and agentic authoring: PRAXIS_PAGE_BUILDER_AUTHORING_MANIFEST, PageBuilderAiAdapter, PageBuilderAgenticAuthoringService, streaming turn flow, UI composition plans, component capability catalogs, context packs, runtime observations, project knowledge/domain rule handoff, quick replies, preview/apply, AI registry ingestion, or Page Builder E2E gates.
---

# Praxis Page Builder AI Agentic

Use this skill for executable AI/agentic Page Builder flows. Page Builder AI is an authoring cockpit for governed page decisions; it is not a shortcut for arbitrary JSON patches, keyword-routed intent, or business-rule materialization inside a page preview.

Pair it with:

- `praxis-ai-authoring-manifests` for shared manifest invariants, validators, and edit-plan rules.
- `praxis-ai-registry-ingestion` for generated registry/catalog/package AI assets.
- `praxis-ai-semantic-intent` for consult/edit boundaries and no keyword-based intent routing.
- `praxis-ai-turn-orchestration-transport` for assistant turn stream lifecycle, runtime observation trust boundary, and terminal result handling.
- `praxis-ai-composer-attachments-quick-replies` for quick replies, clarifications, and composer actions that select Page Builder targets or operations.
- `praxis-page-builder-composition` for `WidgetPageDefinition`, `UiCompositionPlan`, composition links, and runtime page materialization.
- `praxis-page-builder-authoring` for Settings Panel and visual editor round-trip.

## Canonical AI Boundary

AI must operate through governed contracts:

`user semantic intent -> backend/tool grounding -> component/page capabilities -> UiCompositionPlan or manifest operation -> preview -> reviewed apply -> persistence`

Do not route Page Builder intent by local keyword lists in Angular. `intentExamples` and trigger terms may help catalogs describe capabilities, but final routing must be governed by backend/LLM semantic resolution, component manifests, declared tools, metadata, runtime observations, and validated candidates.

Do not call Page Builder preview/apply for shared business-decision materialization such as Domain Rules or Project Knowledge. Route those through canonical `@praxisui/core` Domain Rule and Domain Knowledge services and keep cockpit evidence safe.

## Required Source Inventory

Before editing Page Builder AI, inspect:

- `projects/praxis-page-builder/AGENTS.md`
- `projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.ts`
- `projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.spec.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-ai.adapter.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-ai-catalog.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-context-pack.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-ui-composition-plan.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-agentic-authoring.service.ts`
- `projects/praxis-page-builder/src/lib/ai/page-builder-agentic-authoring-turn-flow.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-builder.component.ts`
- `projects/praxis-page-builder/docs/page-builder-governed-continuity-inventory.md`
- `projects/praxis-page-builder/docs/component-palette-browser-validation-roadmap.md`

If the change affects generated AI assets, inspect `tools/ai-registry` through `praxis-ai-registry-ingestion`.

## Manifest And Plan Rules

Keep `WidgetPageDefinition` as the canonical persisted page shape. `UiCompositionPlan` is an intermediate agentic plan that must compile before runtime apply. Do not persist preview envelopes, compiled patch wrappers, or plan documents as if they were runtime pages.

The Page Builder manifest should preserve operations for page config, canvas config, widget add/remove/move, widget shell, composition links, state, preview apply, persistence save, and child operation delegation. Every child widget input edit must delegate to the child component `ComponentDocMeta.configEditor` or child `ComponentAuthoringManifest`.

For composition links, require stable ids, resolvable endpoints, valid nested paths, valid JSON Logic conditions, and no legacy connection writes.

For page persistence, keep `pageIdentity`, scope, and ETag policy out of the page document itself. Persist through the canonical config surface; do not create Page Builder-local persistence routes.

## Agentic Turn Rules

Streaming turn behavior must show intermediate reasoning/state in the assistant UI before the terminal preview/result. Clarifications, quick replies, diagnostics, attachments, component capabilities, runtime observations, and selected widget context must remain visible enough for enterprise users to understand why the assistant is blocked or proposing a change.

Runtime observations are untrusted frontend evidence. Use them as grounding signals, not as backend truth. When sent to the backend, preserve the trust-boundary marker.

For shared-rule or project-knowledge continuation:

- use canonical Domain Rule and Domain Knowledge services from `@praxisui/core`;
- do not invent `/api/praxis/config/**` routes;
- do not render raw prompt, patch, source pointer, materialized payload, assistant message, or sensitive evidence in common cockpit state;
- keep route-required handoffs as clarification/continuation states, not successful page previews.

## Validation

Use local-first gates:

- manifest changes: `praxis-page-builder-authoring-manifest.spec.ts`.
- adapter or composition plan changes: `page-builder-ai.adapter.spec.ts`, `page-builder-ui-composition-plan.spec.ts`, and runtime normalization specs.
- capability catalogs: `page-builder-ai-catalog.spec.ts` and AI registry validation when generated assets change.
- turn flow: `page-builder-agentic-authoring-turn-flow.spec.ts`, agentic authoring service specs, and dynamic page builder component specs.
- full agentic/page-builder contract changes: the local Playwright gates named in `projects/praxis-page-builder/AGENTS.md`, using the official backend/UI origins and real provider configuration.

Report whether only the quick smoke ran or the complete agentic validation gate ran. Do not use GitHub Actions as the normal exploratory loop when local gates can prove the change.
