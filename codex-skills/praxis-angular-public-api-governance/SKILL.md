---
name: praxis-angular-public-api-governance
description: Use when changing, reviewing, or relying on `@praxisui/*` public APIs in `praxis-ui-angular`, including `src/public-api.ts`, exported types/services/tokens/components, cross-lib imports, barrel boundaries, packageable contracts, and direct-consumer validation.
---

# Praxis Angular Public API Governance

Use this skill for public API changes across `@praxisui/*`. A root `public-api.ts` export is a platform contract, not a convenience import.

## Canonical Rule

No public Angular lib should become a transitive facade for another public lib's root barrel without an explicit architectural reason. Keep root exports intentional, stable, packageable, and owned by the canonical lib.

Classify any changed `public-api.ts`, exported model, service, token, component, provider, AI contract, or package-facing type as at least `contrato-publico`.

## Required Inventory

Before editing:

1. Read `praxis-ui-angular/AGENTS.md` and the local `projects/<lib>/AGENTS.md`.
2. Identify the owner of the contract. Shared runtime contracts normally belong in `@praxisui/core`; vertical semantics belong in the owning component lib.
3. Search direct consumers in `projects/*`, examples, docs, recipes, tests, and landing docs.
4. Check whether the new export would reexport a type owned by another public lib.
5. Ask: what does Praxis already know, but the UX/runtime/consumer is not materializing well?
6. Classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.

Only `lacuna-real-de-contrato` justifies a new public contract. If the need is already represented by metadata, config, capabilities, AI manifest, component docs, or an owner lib export, improve that materialization instead of adding a parallel alias.

## Export Decision

Prefer, in order:

1. Use the canonical owner export directly.
2. Add a minimal stable export to the true owner.
3. Move a shared contract to the canonical shared owner when multiple libs truly need it.
4. Define a structurally compatible local contract in the consumer only when a root facade would create inappropriate coupling.

Avoid:

- root barrel reexports from another `@praxisui/*` root barrel
- exporting internals, implementation helpers, generated artifacts, adapters, or heavy runtime objects for convenience
- adding aliases that preserve legacy names during beta when a clean canonical migration is viable
- expanding `@praxisui/core` merely to hide poor ownership in a vertical lib

## Validation

Minimum validation for public API changes:

- build the altered lib, for example `npm run build:praxis-core`
- build or test at least one real direct consumer
- run focused specs for the exported service/model/provider when present
- review docs/examples/AI registry impact when the public behavior is documented or authorable

If the change touches `@praxisui/ai`, `@praxisui/core`, or public AI contracts, add the focal E2E or consumer gates named by `praxis-ui-angular/AGENTS.md` when applicable.

Use `praxis-angular-validation-gates` to pick the smallest reliable command set, and `praxis-ai-registry-ingestion` if the export affects AI manifests, component docs, or packaged AI assets.
For `@praxisui/core` exports, also use the focused core skill for the affected subdomain: `praxis-core-providers-bootstrap`, `praxis-core-widget-observations`, `praxis-core-logging-observability`, `praxis-core-i18n-resource-copy`, or `praxis-core-global-actions-metadata`.

## Derived Artifacts

After public API changes, review:

- `README.md`, package docs, `*.json-api.md`, and `docs/praxis-docs.manifest.json` for the owning lib
- `docs/ai/agentic-authoring/component-authoring-contracts` when AI-authorable behavior changes
- examples, recipes, playgrounds, and landing pages that publish the public surface
- generated registry/package assets when component metadata or authoring contracts changed

If none apply, say why.

## Output Expectations

Report:

- canonical owner
- consumers found
- whether the export creates a new cross-lib edge
- validation run for owner and consumer
- derived artifacts reviewed or intentionally skipped
