---
name: praxis-core-runtime-contracts
description: Use when Codex must inspect, change, or rely on @praxisui/core shared runtime contracts: public-api exports, tokens, providers, i18n, logging, common services, registries, shared models, schema infrastructure, global actions, config storage, CRUD/discovery services, or cross-lib contracts consumed by other @praxisui/* packages.
---

# Praxis Core Runtime Contracts

Use this skill for `@praxisui/core`, the canonical Angular owner of shared contracts, tokens, services, registries, models, providers, logging, i18n, schema infrastructure, global actions, and runtime utilities used by the other `@praxisui/*` libraries.

This skill is about the Angular runtime contract. It does not make Angular the source of backend business semantics. `praxis-metadata-starter` owns `x-ui`, schemas, actions, surfaces, capabilities, option-source semantics, and metadata emission. `praxis-config-starter` owns governed config/registry/template persistence. `@praxisui/core` consumes, normalizes, materializes, and exposes stable Angular contracts for those projections.

## Source Audit

Before changing a core-facing skill or implementation, inspect the real source for the affected area:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/docs/schema-flow.md` when schema or metadata flow changes
- `projects/praxis-core/docs/connection-editor.md` when connection, widget wiring, or actions change
- `projects/praxis-core/src/lib/models/**`
- `projects/praxis-core/src/lib/services/**`
- `projects/praxis-core/src/lib/tokens/**`
- `projects/praxis-core/src/lib/providers/**`
- `projects/praxis-core/src/lib/i18n/**`
- `projects/praxis-core/src/lib/logging/**`
- `projects/praxis-core/src/lib/reconcilers/**`

Do not rely on memory of the package. The core public API changes often and is the upstream owner for many runtime behaviors that vertical libs consume.

## Canonical Owner Decision

Put the fix in `@praxisui/core` when the concern is shared across libraries or affects one of these contracts:

- `GenericCrudService`, schema metadata clients, resource discovery, config storage, global config, and common CRUD/data access helpers
- global actions, global surfaces, action refs, action UI schema, action catalogs, and shared action providers
- tokens such as `API_URL`, `PAX_FETCH_HEADERS`, global config, loading, overlay decisions, export, external editors, field selectors, or surface/drawer bridges
- common models: table config, field metadata, option sources, resource discovery, domain catalog, domain knowledge/rules, query context, analytics presentation, loading state, collection export, surface actions, runtime observations
- logging, observability, error normalization, telemetry sinks, and global error handling
- i18n service, providers, resource-discovery copy, value presentation, and shared internal framework text
- reconcilers and config normalization shared by multiple libs

Do not move shared semantics into `praxis-table`, `praxis-dynamic-form`, `praxis-list`, host apps, examples, or migration code when the contract belongs in core.

## Public API Guardrails

Any change to `src/public-api.ts`, exported models, exported services, exported tokens, root providers, or shared AI contracts is at least `contrato-publico`.

Before editing:

1. Identify the canonical owner of the contract.
2. Search for direct consumers in `projects/*`, examples, docs, and recipes.
3. Check whether another public lib is using the core root barrel as a transitively convenient facade.
4. Prefer a minimal stable export from the true owner over reexporting another lib's root API.
5. Plan at least a focal build/test for `praxis-core` and one direct consumer when the export is used outside core.

Do not add a root export merely to make a local import easier. `public-api.ts` must remain an intentional, packageable contract.

## Platform Aderence Inventory

Before creating a new model, token, provider, service, config field, event, adapter, or export, answer:

`What does Praxis already know, but the Angular runtime or consumer is not materializing well?`

Classify each need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public core contract. If the data already exists in backend metadata, config starter state, action/surface/capability discovery, AI manifests, config storage, diagnostics, or runtime registries, fix the owner or materialization instead of adding a parallel Angular concept.

## Validation Guidance

Prefer the smallest reliable validation:

- localized shared service/model/reconciler change: focused `.spec.ts` for the area
- exported contract or public API change: `npm run build:praxis-core` plus at least one consumer build/test
- schema flow, `GenericCrudService`, resource discovery, global actions, i18n, logging, or widgets: treat as transversal and include focused consumer specs
- AI contract/manifest change: validate the relevant manifest spec and registry ingestion when applicable

If PowerShell audit scripts are unavailable, run an equivalent local manifest/hash/frontmatter audit and state the limitation.

Use `praxis-angular-validation-gates` for command selection and `praxis-angular-public-api-governance`
before changing root exports or cross-lib public contracts. Use `praxis-angular-i18n-governance` when
core text, logging UX, resource-discovery copy, or shared localization changes. Use
`praxis-angular-docs-playgrounds` when public docs, examples, or package docs reflect the contract.

## Companion Skills

- Use `praxis-core-resource-runtime` for resource discovery, schema, actions, surfaces, capabilities, HATEOAS, option sources, CRUD operation resolution, and analytics request contracts.
- Use `praxis-core-composition-runtime` for composition runtime, widgets, dynamic widget pages, nested ports, connection/link execution, and surface hosts.
- Use `praxis-angular-host-project` when applying core contracts in a consuming host.
- Use `praxis-component-minimums` when the question is the smallest runtime setup for a component.
- Use `praxis-ui-product-design` for visual/product UX and screenshot validation.
- Use `praxis-angular-public-api-governance` for public API boundaries and cross-lib export decisions.
- Use `praxis-angular-validation-gates` for focused local validation and release/preflight boundaries.
