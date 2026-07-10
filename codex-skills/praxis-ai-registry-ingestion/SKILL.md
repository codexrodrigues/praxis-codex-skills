---
name: praxis-ai-registry-ingestion
description: Use when implementing, auditing, generating, packaging, or synchronizing Praxis AI registry artifacts: component docs extraction, AI metadata, ingestion corpus/chunks, catalog governance, authoring-contract acceptance, AI-ready docs, RAG/provider projections, package `ai/component-registry.json` assets, or official backend uploads.
---

# Praxis AI Registry Ingestion

`tools/ai-registry` is the canonical generator and governance boundary for AI-facing Angular artifacts. Registry output describes existing Praxis contracts for grounding; it does not invent component semantics, route intent, or replace source manifests, metadata, backend schemas, capabilities, actions, surfaces, or runtime code.

## Provenance Pipeline

```text
component source, metadata, README/docs, authoring manifests, capability/context packs
  -> extract-component-docs.js + generate:ai-metadata
  -> dist/praxis-component-registry.json
  -> generate-registry-ingestion.ts
  -> dist/praxis-component-registry-ingestion.json (canonical aggregate corpus)
  -> catalog + authoring-contract validation
  -> optional RAG/provider/AI-ready/package/upload projections
```

The ingestion corpus with `components[].chunks` is canonical for aggregate analysis. `praxis-component-registry-rag.json`, provider projections, AI-ready docs, reports, npm package assets, and backend uploads are derived read models. Never hand-edit `dist/**`, package assets, projections, or reports to repair a source/contract problem.

Read `tools/ai-registry/AGENTS.md`, its README, workspace AGENTS, and the affected library's AGENTS before editing. Inspect the actual owner source: public API, component metadata, docs manifest, authoring manifest, capabilities/context pack, focused specs, and consumer docs.

## Decide The Smallest Canonical Operation

| Change | Owner and minimum action |
| --- | --- |
| component docs extraction or AI metadata | source docs/metadata first, then `npm run generate:registry:ingestion` |
| ingestion generator/schema/chunks/governance | `generate:registry:ingestion`; validate catalog and authoring contracts |
| catalog validation only | `npm run validate:catalog` |
| completed authoring contract acceptance | `npm run validate:authoring-contracts` |
| AI planning/RAG/templates | `npm run validate:ai` |
| package-scoped asset after ingestion and library builds | `npm run package:ai-assets`, then package/tarball validation if release scope requires it |
| provider projection | regenerate from the canonical ingestion corpus for the explicit release; never upload secrets/external IDs into it |
| backend upload | use `tools/ai-registry/run-all.sh` or `npm run ai:sync-backend` only when a real backend state change is required |

`npm run generate:registry:ingestion` is the standard local pipeline: extract component docs, generate AI metadata, generate ingestion corpus, validate catalog governance, and validate authoring contracts. It is the correct response to a source/manifest/capability/context-pack change; it is not required merely to edit a derived report or inspect a package asset.

## Canonical Content Rules

- Keep component docs extractable from supported literal metadata/factories. If extraction cannot represent a semantic feature, improve the source metadata or official extractor, not a consumer-side registry patch.
- A manifest, capability, target, validator, effect, profile, context pack, and docs chunk must point to the source owner and remain mutually consistent. Do not make a generated registry the primary definition of an operation.
- Registry grounding is evidence for LLM semantic resolution. Do not encode primary intent as keyword, regex, alias, fuzzy match, display-label parsing, or a registry-only command dialect.
- Quick replies/actions must retain structured canonical action, semantic decision, target, context, risk, and presentation. Labels are not authority.
- Preserve the runtime observation contract chunk and its `untrusted_frontend_observation` boundary. Observations require backend grounding into canonical context before they influence an answer; registry text cannot grant read/tool/apply authority.
- Catalog governance must reject duplicate IDs/selectors, invalid paths, incomplete target/validator/effect evidence, unconfirmed destructive work, ambiguous targets without policy, inconsistent control profiles, and lost trust boundaries. Repair the source owner or validator, never weaken the gate to pass a local artifact.
- Use aggregate corpus for cross-package/release analysis and `@praxisui/<package>/ai/component-registry.json` only for source-less package consumers. Package assets remain filtered projections of their owning package.

## Before New Contracts Or Scripts

Inventory the existing metadata, `x-ui`, schemas, actions, surfaces, capabilities, option sources, manifests, registry chunks, diagnostics, context packs, docs, and backend API catalog. Classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.

Only a real contract gap justifies a schema, chunk, generator, endpoint, or script change. Map source owner, generated outputs, Angular/package consumers, backend ingestion, security/origin requirements, docs/playgrounds, compatibility, and focused validation first. Do not add ad hoc upload, extraction, or sync scripts outside this tool owner.

## Remote And Release Boundaries

- Local generation and validation come first. GitHub Actions are release/final gates, not discovery tooling.
- Backend uploads use the documented environment and official scripts: `BACKEND_URL`, `CONFIG_ORIGIN`, `APP_SECURITY_READ_OPEN`, and `APP_SECURITY_WRITE_OPEN`. Do not invent endpoints, origins, ports, or upload ordering.
- `run-all.sh --with-api-catalog` is the canonical combined registry/templates/API-catalog flow. Do not additionally invoke individual upload scripts in the same operation.
- `package:ai-assets` needs the generated ingestion corpus and built `dist/<package>` folders. It writes the scoped asset plus package export; validate local tarballs when package publication is in scope.

## Evidence And Companion Skills

Run the smallest compatible command and report it exactly. For changes to tooling itself, add its focused Node self-test; for a source component, add that component's build/spec/authoring proof. State whether docs, recipes, manifests, landing, package assets, RAG/provider projections, backend sync, and release validation were affected.

Use `praxis-ai-authoring-manifests` for executable authoring contracts; `praxis-angular-docs-playgrounds` for public documentation; `praxis-angular-public-api-governance` for exports; `praxis-angular-validation-gates` for local proof; and the functional component skill for the changed source. Use `praxis-config-agentic-authoring-streaming` or `praxis-ai-turn-orchestration-transport` when registry chunks derive from governed turns, tools, observations, quick replies, or backend transport.
