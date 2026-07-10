---
name: praxis-angular-docs-playgrounds
description: Use when updating or auditing Praxis Angular public documentation, component docs, `docs/praxis-docs.manifest.json`, `*.json-api.md`, examples, `examples/ai-recipes`, landing pages, playgrounds, published guides, sitemap entries, AI registry derived docs, or other public derived artifacts.
---

# Praxis Angular Docs Playgrounds

Use this skill when a Praxis Angular change must be reflected in public docs, examples, playgrounds, landing pages, recipes, or AI-derived documentation.

Docs and playgrounds are projections of canonical platform contracts. They must not invent semantics, capabilities, AI flows, statuses, or business rules that the canonical owner does not publish.

## Canonical Sources

- `praxis-ui-angular` owns Angular runtime packages, component docs, manifests, AI registry extraction, examples, and playground source behavior.
- `praxis-metadata-starter` owns backend metadata semantics such as `x-ui`, `/schemas/filtered`, surfaces, actions, capabilities, and option-source contracts.
- `praxis-config-starter` owns governed config persistence and `/api/praxis/config/**`.
- `praxis-ui-landing-page` publishes official site pages and guides, but does not override the owning lib.

When docs disagree with code or backend contracts, fix the canonical owner or explicitly record drift; do not normalize the docs as if they were the source of truth.

## Required Inventory

Before editing docs or examples:

1. Read `praxis-ui-angular/AGENTS.md`; for landing work also read `praxis-ui-landing-page/AGENTS.md`.
2. Read the local `projects/<lib>/AGENTS.md` for the component family when present. If it is absent, use `praxis-angular-agents-governance`, record the local governance gap, and derive docs/validation impact from README, docs manifests, public API, metadata, examples, focused specs, and package scripts.
3. Inspect the owning lib docs: `README.md`, `*.json-api.md`, host integration docs, patterns/editor docs, and `docs/praxis-docs.manifest.json`.
4. For landing component pages, read `praxis-ui-angular/docs/templates/component-landing-template.md`, `docs/templates/README.md`, and landing registries such as `src/app/data/guides/component-docs.registry.ts`.
5. For AI-authorable components, inspect manifests and registry tooling through `praxis-ai-registry-ingestion`.
6. Classify whether the requested narrative is `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.

## Update Triggers

Review derived artifacts when a change touches:

- public component inputs, outputs, events, config shape, `public-api`, or default behavior
- `ComponentDocMeta`, config editor metadata, authoring manifests, capabilities, actions, schemas, or runtime observations
- examples, recipes, playgrounds, or demo routes used as reference behavior
- i18n or visible authoring chrome that appears in docs/screenshots
- package publication, npm docs, public links, or search surfaces

Do not update generated `dist/` artifacts by hand. Regenerate through the owning command when the task requires it.

## Validation

For `praxis-ui-angular` docs:

- `npm run docs:validate-frontmatter:changed` for changed docs frontmatter
- `npm run generate:registry:ingestion` when component docs or AI registry projections must update
- `npm run validate:published-doc-assets` for publishable docs/assets when relevant
- focused examples/playground build or E2E when the example behavior changed

For `praxis-ui-landing-page`:

- `npm run validate:published-guides`
- `npm run validate:sitemap`
- `npm run validate:table-manifests` when `site.data.ts` manifests/examples change
- `npm run check:integration` for sitemap plus dev/prod integration checks when the publication surface changed broadly

Use official local origins documented in AGENTS files. Do not invent ports for published quickstart or landing validation.

Use component-specific docs skills when they exist. For `@praxisui/list`, use
`praxis-list-docs-evidence` to preserve the Active/Partial/Declared-only status matrix, living
examples, executive evidence, and list-specific docs manifest before editing landing or playground
content.
For `@praxisui/metadata-editor`, use `praxis-metadata-editor-renderer-coverage`,
`praxis-metadata-editor-cascade-normalization`, `praxis-metadata-editor-consumer-bridges`, or
`praxis-metadata-editor-ai-validation` before updating docs manifests, architecture docs, coverage
checklists, AI registry docs, or public examples that describe metadata-editor authoring behavior.
For `@praxisui/manual-form`, use `praxis-manual-form-runtime-bridge` and
`praxis-manual-form-ai-authoring` before updating integration guides, API references, toolbar docs,
examples, docs manifests, or AI registry docs. For `@praxisui/editorial-forms`, use
`praxis-editorial-forms-runtime` and `praxis-editorial-forms-adapters-ai` before updating
architecture docs, authoring playbooks, labs, examples, docs manifests, or registry projections.
For `@praxisui/crud`, use `praxis-crud-runtime-openmodes` and `praxis-crud-ai-authoring` before
updating open-mode docs, drawer adapter ADRs, CRUD authoring docs, examples, docs manifests, or AI
registry docs. For `@praxisui/dialog`, use `praxis-dialog-overlay-runtime` and
`praxis-dialog-global-actions-ai` before updating dialog integration guides, examples, presets,
global actions, docs manifests, or registry projections.
For `@praxisui/tabs`, `@praxisui/stepper`, `PraxisWizardFormComponent`, or `@praxisui/expansion`,
use `praxis-tabs-runtime-authoring`, `praxis-stepper-wizard-runtime`,
`praxis-expansion-runtime-panels`, `praxis-navigation-containers-ai-validation`,
`praxis-navigation-container-composition-events`, `praxis-stepper-wizard-orchestration`, and
`praxis-navigation-agentic-registry` as applicable
before updating component guides, API references, examples, docs manifests, playgrounds, or AI
registry docs for navigation and disclosure containers.
For `@praxisui/files-upload`, use `praxis-files-upload-runtime`,
`praxis-files-upload-backend-contract`, `praxis-files-upload-form-field`, and
`praxis-files-upload-ai-validation` as applicable before updating component guides, host
integration docs, API references, examples, docs manifests, playgrounds, or AI registry docs.
For `@praxisui/rich-content`, use `praxis-rich-content-runtime`,
`praxis-rich-content-authoring-settings`, `praxis-rich-content-integration-adapters`, and
`praxis-rich-content-ai-security-validation` as applicable before updating component guides, docs
manifests, examples, playgrounds, AI recipes, or registry docs.
For `@praxisui/cron-builder`, use `praxis-cron-builder-runtime`,
`praxis-cron-schedule-authoring`, `praxis-cron-builder-form-field`, and
`praxis-cron-builder-ai-validation` as applicable before updating component guides, API references,
docs manifests, examples, playgrounds, AI recipes, or registry docs.
For `@praxisui/table-rule-builder`, use `praxis-table-rule-effects-runtime`,
`praxis-table-rule-animation-presets`, `praxis-table-rule-table-integration`, and
`praxis-table-rule-ai-validation` as applicable before updating component guides, API references,
docs manifests, examples, playgrounds, AI recipes, or registry docs.
For `@praxisui/charts`, use `praxis-charts-runtime-data`, `praxis-charts-authoring-settings`,
`praxis-charts-ai-validation`, `praxis-charts-echarts-engine-boundary`,
`praxis-charts-analytics-interactions`, `praxis-charts-authoring-catalogs`, and
`praxis-charts-ai-handler-contracts` as applicable before updating chart docs, API references,
examples, playgrounds, dashboard analytics evidence, AI recipes, or registry docs.
For `@praxisui/dynamic-fields`, use `praxis-dynamic-fields-editorial`, `praxis-fields-runtime-loader`,
`praxis-fields-editorial-discovery`, `praxis-fields-option-sources`,
`praxis-fields-inline-overlay-runtime`, `praxis-fields-text-number-time-controls`,
`praxis-fields-selection-lookup-controls`, and `praxis-fields-control-profile-ai` as applicable
before updating field catalogs, inline filter docs, examples, playgrounds, AI recipes, or registry
docs.
For `@praxisui/visual-builder`, use `praxis-visual-builder-rules` as the umbrella and then the
focused skills `praxis-visual-builder-graph-runtime`, `praxis-visual-builder-jsonlogic-roundtrip`,
`praxis-visual-builder-schemas-templates`, and `praxis-visual-builder-ai-validation` before updating
component guides, API references, docs manifests, examples, playgrounds, AI recipes, or registry
docs.

## Editorial Guidance

- Explain Praxis components as configurable, metadata-driven, governed runtime surfaces, not generic UI widgets.
- Public copy should explain value, evidence, host responsibility, and canonical contract.
- Avoid internal production instructions such as "show", "start", or "the ideal video should" in public editorial pages unless the page is an explicit tutorial.
- Keep `slug`, `related_docs`, markdown links, manifests, and sitemap entries valid.

## Output Expectations

Report:

- canonical owner consulted
- docs/examples/playgrounds updated or reviewed
- validation commands run
- generated artifacts intentionally not edited by hand
- any public surface still out of sync and why
