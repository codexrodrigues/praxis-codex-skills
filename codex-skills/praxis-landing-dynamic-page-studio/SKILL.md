---
name: praxis-landing-dynamic-page-studio
description: Use when implementing or auditing the public Praxis Dynamic Page Studio and its learning journey: safe operational JSON, runtime-profile execution policy, sandbox/network fail-closed behavior, JSON/Visual modes, preview/materialization state, curated recipe families, guided outcomes/progress, accessible workspace, Quickstart integration, or hosted Studio E2E. Do not use for Page Builder runtime internals alone.
---

# Praxis Landing Dynamic Page Studio

Use this skill for the official public Studio in `praxis-ui-landing-page`. The
Studio teaches and proves governed Praxis materialization; it must not become a
second Page Builder, component registry, execution policy language, or source of
business semantics.

## Canonical Boundary And Sources

The Landing project owns the public learning/workstation experience. It consumes
published `@praxisui/*`, runtime profiles, official recipes, Quickstart HTTP, and
canonical documentation.

Inspect:

- landing root `AGENTS.md`
- `src/app/pages/dynamic-page-studio/**`
- execution, sandbox, network-policy, document-store, analytics, i18n, and page specs
- `src/app/pages/dynamic-page-examples*`, especially the component and specs for
  the public visual-editor opener
- Core `ComponentConfigEditorDefinition` and the component owner's published
  `configEditor` metadata before assuming an eager editor implementation
- `src/app/data/ai-recipes/**` and example metadata/catalog sync tool
- `e2e/dynamic-page-studio.spec.ts` plus the affected recipe/remote E2E
- package versions, runtime providers, official Quickstart origin, sitemap,
  LLM indexes, crawler/publication gates, and hosted smoke

Use `praxis-core-component-runtime-profiles` for execution-profile semantics and
Page Builder/Core composition skills for runtime documents. Landing may explain
and project those contracts but must not redefine them.

## Studio Rules

- Keep authored source and runtime materialization distinct. JSON/Visual edits
  produce a canonical page document; derived runtime state, capability results,
  diagnostics, receipts, and selected examples do not leak back into authored
  JSON unless an explicit owner operation applies them.
- Validate the complete document before preview. Unknown components, unmatched
  runtime profiles, undeclared effects, unsafe URLs/renderers/hooks, invalid
  composition, or missing required policy evidence fail closed with actionable
  diagnostics.
- Network policy derives from matched owner profiles and the official runtime
  origin. Component ids, prompts, example labels, or visible buttons never grant
  network access. Block unexpected `/api/**`, cross-origin, unresolved, or
  undeclared operations.
- Preserve user input across JSON/Visual mode changes without maintaining two
  divergent documents. Monaco paste/import is an explicit action with parse,
  validation, and recovery feedback.
- Preview scope must be visible: local-only, governed remote, degraded, blocked,
  or unsupported. A rendered widget is not proof that its actions or remote data
  are executable.
- Curated examples are versioned evidence with family/variant identity, learning
  objective, runtime requirements, guide, and validation. Do not copy stale
  vendor docs or synthetic endpoints into the catalog.
- Guided journeys expose the current step, outcome, next safe action, and
  progress without hiding the actual JSON/runtime surface. They may suggest
  canonical operations but never keyword-route intent or fabricate success.
- Preserve accessible splitter/editor/preview behavior, keyboard access, focus,
  narrow/mobile containment, localization, and reduced-motion/high-contrast
  behavior.

## Workflow

1. Inventory the existing page document, matched profiles, network decision,
   materialization state, recipe metadata, guide, and hosted dependency.
2. Classify whether the need is Studio UX, missing published recipe evidence,
   under-projected component metadata, or a real owner-contract gap.
3. Fix the canonical owner first when profiles, component runtime, schemas,
   actions, surfaces, or composition are wrong; then update the Landing
   projection and official example.
4. Keep package/version and Quickstart origin aligned with the documented
   integration path. Do not add local aliases or ad hoc origins.
5. Update sitemap/LLM/crawler/public artifacts only when the route, guide,
   catalog, or published claim changes.

## Public Visual Editor Resolution And Custody

Consume the existing owner `configEditor` definition: resolve
`editor.component ?? await editor.loadComponent?.()` before opening the Settings
Panel. A lazy definition is supported metadata, not a missing editor. While the
loader is pending, or if it fails, do not substitute the JSON inspector or claim
the visual editor opened; report a safe diagnostic without exposing loader details.

Capture the selected example, authored page and widget inputs from one snapshot.
Use the latest request generation plus selection and destroy guards after the
await and for the opened panel's events. Selection A→B→A must invalidate the old
request even when the final selected ID matches. Before opening, also reject a
pending resolution if the authored page changed or its draft was reset without
a selection change. The page-snapshot check belongs to pending resolution:
a legitimate Apply replaces the authored page, so a subsequent Save in that same
owned panel must still succeed. Do not reject the panel's own revision with a
permanent comparison against the pre-open page.

On replacement, selection change or destroy, close the owned panel and release
its subscriptions; on normal close, remove the owned reference/subscriptions.
Late loader results or Apply/Save events must not open or mutate a new selection.
Keep updates in the existing canonical page/envelope through the owner outputs;
do not add a parallel draft or editor contract in Landing.

## Proof

Minimum local gates:

- execution/network/sandbox/document-store focused specs;
- Dynamic Page Studio component spec;
- example metadata/catalog synchronization and validation;
- landing build;
- `e2e/dynamic-page-studio.spec.ts` for visible workflow changes;
- affected recipe/remote E2E when a public example or Quickstart integration changes.

Prove local safe JSON, governed remote execution, unmatched/unsafe profile
rejection, blocked unexpected network, JSON/Visual round-trip, invalid paste
recovery, accessible keyboard/narrow journey, and direct route reload. Hosted
claims require the hosted smoke; local mocks do not prove public integration.
For a visual-editor opener, cover eager/lazy definitions, reverse completion,
A→B→A, pending page replacement/reset, load rejection, destroy, late events and
Apply→Save in focused specs. Then use the public button in a real browser with
the target published SDK, resolve its actual editor and exercise Apply/Save in
the canonical page. Mocked metadata/Settings Panel on an installed older SDK
train does not prove the next SDK train's lazy chunk, rendering or public flow;
keep that browser/adoption gate explicitly pending until it runs.

## Companion Skills

- `praxis-core-component-runtime-profiles`: input/effect policy evidence.
- `praxis-core-composition-runtime` and `praxis-page-builder-composition`: canonical page materialization.
- `praxis-landing-registries-sitemap-playgrounds`: registry, route, sitemap, LLM and crawler publication.
- `praxis-landing-public-docs-contracts`: public contract claims.
- `praxis-angular-accessibility-governance` and `praxis-ui-product-design`: workstation accessibility and UX.
- `praxis-api-quickstart-cockpit-http-validation`: official remote-host evidence.

