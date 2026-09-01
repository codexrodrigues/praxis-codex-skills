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
- `src/app/pages/dynamic-page-examples*`
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

## Companion Skills

- `praxis-core-component-runtime-profiles`: input/effect policy evidence.
- `praxis-core-composition-runtime` and `praxis-page-builder-composition`: canonical page materialization.
- `praxis-landing-registries-sitemap-playgrounds`: registry, route, sitemap, LLM and crawler publication.
- `praxis-landing-public-docs-contracts`: public contract claims.
- `praxis-angular-accessibility-governance` and `praxis-ui-product-design`: workstation accessibility and UX.
- `praxis-api-quickstart-cockpit-http-validation`: official remote-host evidence.

