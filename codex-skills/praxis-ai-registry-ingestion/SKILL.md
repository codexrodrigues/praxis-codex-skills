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
Use `praxis-angular-public-api-governance` when the registry change is caused by package-facing
exports or public component contracts.
Use `praxis-list-ai-validation` for `@praxisui/list` manifest/capability/context-pack changes, and
`praxis-list-docs-evidence` when list docs or living examples feed the registry projection.
Use `praxis-metadata-editor-ai-validation` for `@praxisui/metadata-editor`
manifest/capability/context-pack changes. Pair it with
`praxis-metadata-editor-renderer-coverage` or `praxis-metadata-editor-cascade-normalization` when
registry docs derive from editor visual coverage, cascade behavior, option-source dependency
preservation, or schema normalization.
Use `praxis-manual-form-ai-authoring` for `@praxisui/manual-form` manifest, capability, context-pack,
config editor, formRules, toolbar, autosave, and metadata bridge projections. Use
`praxis-editorial-forms-adapters-ai` for `@praxisui/editorial-forms` manifest, adapter, dataCollection,
field binding, fallback, presentation, and registry projections.
Use `praxis-crud-ai-authoring` for `@praxisui/crud` manifest, capabilities, context packs, metadata
editor, and child-operation delegation. Use `praxis-dialog-global-actions-ai` for `@praxisui/dialog`
global actions, registries, authoring manifest, and registry projections.

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
