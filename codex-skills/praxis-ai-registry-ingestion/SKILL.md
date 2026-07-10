---
name: praxis-ai-registry-ingestion
description: Use when changing or validating Praxis AI registry tooling, `tools/ai-registry`, component docs extraction, registry ingestion generation, catalog governance, RAG/provider projections, packaged `ai/component-registry.json` assets, AI-ready docs, backend sync/upload scripts, or generated registry artifacts after component authoring manifest or metadata changes.
---

# Praxis AI Registry Ingestion

Use this skill for the canonical AI registry pipeline in `tools/ai-registry`. Do not create ad hoc scripts or edit generated `dist/` artifacts as source of truth.

## Canonical Pipeline

The standard ingestion command is:

```bash
npm run generate:registry:ingestion
```

It includes component docs extraction, AI metadata generation, ingestion registry generation, catalog governance validation, and authoring contract validation where configured.

Use narrower commands only when the change scope is narrower:

- `npm run validate:catalog` for catalog governance only
- `npm run validate:authoring-contracts` for completed authoring contracts
- focused Node specs for registry tooling self-tests
- `npm run validate:ai` when planning/RAG/template artifacts must be checked
- `npm run package:ai-assets` when package-scoped `ai/component-registry.json` assets must be refreshed
- `npm run ai:sync-backend` only when backend synchronization is explicitly required

Use `praxis-angular-docs-playgrounds` when registry extraction changes public component docs,
examples, landing pages, or playground evidence. Use `praxis-angular-validation-gates` to decide
whether full ingestion is required or a narrower registry validator is enough for the current scope.
Use `praxis-angular-agents-governance` when registry work touches a component whose local
`projects/<lib>/AGENTS.md` is absent or when a skill's governance claim may have drifted from the
Angular platform source.
Use `praxis-angular-public-api-governance` when the registry change is caused by package-facing
exports or public component contracts.
Use `praxis-list-ai-validation` for `@praxisui/list` manifest/capability/context-pack changes, and
`praxis-list-docs-evidence` when list docs or living examples feed the registry projection.
Use `praxis-metadata-editor-ai-validation` for `@praxisui/metadata-editor`
manifest/capability/context-pack changes. Pair it with
`praxis-metadata-editor-renderer-coverage` or `praxis-metadata-editor-cascade-normalization` when
registry docs derive from editor visual coverage, cascade behavior, option-source dependency
preservation, or schema normalization.
Use `praxis-manual-form-ai-authoring` and `praxis-manual-form-rules-agentic` for
`@praxisui/manual-form` manifest, capability, context-pack, config editor, formRules, JSON Logic,
agentic turn flow, and registry projections. Pair with
`praxis-manual-form-field-detection-instance`, `praxis-manual-form-autosave-persistence`, or
`praxis-manual-form-toolbar-metadata-bridge` when generated docs derive from field detection,
autosave/storage, toolbar, or metadata bridge behavior. Use
`praxis-editorial-forms-adapters-ai` and `praxis-editorial-forms-agentic-authoring` for
`@praxisui/editorial-forms` manifest, component metadata, adapter, dataCollection, field binding,
fallback, presentation, and registry projections. Pair with
`praxis-editorial-forms-journey-snapshot-runtime`, `praxis-editorial-forms-presentation-diagnostics`,
or `praxis-editorial-forms-data-collection-adapters` when generated docs derive from snapshot,
diagnostics/presentation, or adapter behavior.
Use `praxis-crud-ai-authoring` for `@praxisui/crud` manifest, capabilities, context packs, metadata
editor, and child-operation delegation. Use `praxis-dialog-global-actions-ai` for `@praxisui/dialog`
global actions, registries, authoring manifest, and registry projections.
Use `praxis-navigation-containers-ai-validation` for `@praxisui/tabs`, `@praxisui/stepper`,
`PraxisWizardFormComponent`, and `@praxisui/expansion` manifests, capabilities, context packs,
AI adapters, component docs, and registry projection.
Pair it with `praxis-navigation-agentic-registry`,
`praxis-navigation-container-composition-events`, or `praxis-stepper-wizard-orchestration` when
generated docs derive from agentic turn flows, nested widget composition, dynamic page events,
wizard submit/validation, or cross-container authoring consistency.
Use `praxis-files-upload-ai-validation` for `@praxisui/files-upload` manifests, capabilities,
context packs, AI adapters, component docs, backend endpoint/security operations, and registry
projection.
Use `praxis-rich-content-ai-security-validation` for `@praxisui/rich-content` manifests,
capabilities, recipes, document validator, sanitization policy, component docs, and registry
projection.
Use `praxis-cron-builder-ai-validation` for `@praxisui/cron-builder` manifests, capabilities,
context packs, AI adapters, component docs, schedule operation validators, preview/diagnostics, and
registry projection.
Use `praxis-table-rule-ai-validation` for `@praxisui/table-rule-builder` manifests, capabilities,
context packs, AI adapters, component docs, effect registry operations, semantic animation
validators, table delegation, and registry projection.
Use `praxis-fields-control-profile-ai` for `@praxisui/dynamic-fields` per-control AI profiles,
capability catalogs, registry component docs, and family-specific profile validation. Pair it with
`praxis-fields-inline-overlay-runtime`, `praxis-fields-text-number-time-controls`, or
`praxis-fields-selection-lookup-controls` when generated docs derive from inline overlay behavior or
specific control-family semantics.
Use `praxis-visual-builder-ai-validation` for `@praxisui/visual-builder` authoring manifest,
capabilities, context packs, AI adapter, editable targets, operation validators, JSON Logic
round-trip validation, and registry projection. Pair it with
`praxis-visual-builder-graph-runtime`, `praxis-visual-builder-jsonlogic-roundtrip`, or
`praxis-visual-builder-schemas-templates` when generated docs derive from graph, JSON Logic, schema,
context, property-effect, collection-validator, or template behavior.
Use `praxis-charts-ai-validation` for `@praxisui/charts` authoring manifest, editable targets,
validators, handler contracts, component metadata, and generated AI assets. Pair it with
`praxis-charts-ai-handler-contracts`, `praxis-charts-authoring-catalogs`,
`praxis-charts-analytics-interactions`, or `praxis-charts-echarts-engine-boundary` when registry docs
derive from handler contracts, resource/field/target catalogs, analytics interactions, or
engine-boundary behavior.

## Required Inventory

Inspect:

- `tools/ai-registry/AGENTS.md`
- `tools/ai-registry/README.md`
- `extract-component-docs.js`
- `generate-registry-ingestion.ts`
- `generate-registry-rag.ts`
- `validate-catalog-governance.js`
- `validate-authoring-contracts-acceptance.js`
- `package-ai-assets.mjs`
- `config.ts`
- relevant schemas under `tools/ai-registry/schemas`

## Registry Rules

- Canonical aggregate corpus: `dist/praxis-component-registry-ingestion.json`.
- Deprecated compatibility projection: `dist/praxis-component-registry-rag.json`.
- Package consumers without source should use `@praxisui/<package>/ai/component-registry.json`.
- Component docs must remain extractable from literal metadata or supported factories.
- Runtime observation contract chunks must preserve the untrusted frontend observation boundary and backend grounding requirement.
- Provider projections are derived read models; delete and regenerate them from the ingestion registry.
- Respect official env/origins for backend upload flows: `BACKEND_URL`, `CONFIG_ORIGIN`, `APP_SECURITY_READ_OPEN`, `APP_SECURITY_WRITE_OPEN`.

## Validation

Run the smallest official command compatible with the change and report exactly what was run. If tooling cannot run because Node modules or platform binaries are unavailable, still perform a structural audit and say what remains unvalidated.
