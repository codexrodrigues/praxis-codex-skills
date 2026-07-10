---
name: praxis-angular-public-api-governance
description: Use when designing, changing, auditing, or consuming @praxisui Angular package APIs: root public-api.ts, exported components/types/services/tokens/providers, package entrypoints, cross-library imports and dependency edges, beta migrations, packageable barrels, direct-consumer proofs, public docs/manifests, or release compatibility assessment.
---

# Praxis Angular Public API Governance

Use this skill for the intentional package surface of `@praxisui/*`. A root `public-api.ts` creates a stable, packageable platform contract. It is not a convenience barrel, a shortcut around an import, or a place to conceal an ownership problem.

## Classify And Map Impact

Treat a changed root `public-api.ts`, exported model/service/token/provider/component, package entrypoint, public AI contract, or new cross-lib import as `contrato-publico`. Escalate to `transversal` when another library, app, docs, manifest, or external package consumer is affected; escalate to `arquitetural` when ownership or dependency direction changes.

Before editing, map:

- canonical symbol owner and intended package entrypoint;
- current imports, direct consumers, docs/examples/recipes/playgrounds, manifests, and test fixtures;
- new or removed library dependency edges and whether it crosses another root barrel;
- package/build/consumer proof, derived artifacts, beta migration path, and breaking-change risk.

## Required Inventory

Read `praxis-ui-angular/AGENTS.md`, `codex-rules.md`, and applicable `projects/<lib>/AGENTS.md`. When implementing Angular code, follow the workspace Angular MCP requirements before changing code.

Inspect the exact surface rather than reasoning from imports alone:

- owning `src/public-api.ts`, its `ng-package.json`, project `package.json`, README, and package docs;
- source declaration and its intended public owner;
- consumer imports under `projects/**`, `src/**`, `examples/**`, docs, recipes, tests, and landing content;
- direct dependencies in project/package configuration and the local package graph;
- focused export/package specs and `main` diff when a new edge or circular-packaging risk is suspected.

Useful audit queries include searching root barrels for `from '@praxisui/` and consumers for the candidate package/symbol. A type-only import is still not permission to reexport another package's root API.

## Canonical Ownership Rules

Use this order of decisions:

1. Import the existing symbol directly from its canonical owner.
2. If the symbol is required publicly but missing, add a minimal stable export to its true owner.
3. When multiple independent libraries need a genuinely shared contract, move that contract to the correct shared owner, normally `@praxisui/core`, with an explicit dependency map.
4. Define a structurally compatible local contract only when sharing the owner contract would create inappropriate public coupling and the consumer owns a distinct semantic boundary.

Never make a root `@praxisui/*` barrel a transitive facade for another public library's root barrel. Do not root-reexport another library's component, token, service, type, adapter, helper, or generated contract merely because a consumer currently imports through the wrong package.

Keep vertical semantic contracts in their owning library. Keep shared runtime/schema/registry/i18n/CRUD/global-action infrastructure in the real shared owner. Do not expand `@praxisui/core` as a dumping ground, and do not let a vertical package publish core internals under a new alias.

## Export Decision Checklist

For each proposed export, answer all of these before adding it:

1. Who declares and owns the symbol's semantics and lifecycle?
2. Is the declaration already public from that owner, and can the consumer import it directly?
3. Does the export add a package dependency edge or reexport a symbol from a different root package?
4. Is it a minimal stable contract, or an internal helper/generated artifact/heavy runtime/implementation detail?
5. Which exact consumers need it today? A hypothetical future consumer is not enough.
6. Does it change config, metadata, schema, action, capability, manifest, persistence, or editor behavior that needs derived evidence?
7. In beta, can all in-workspace consumers migrate cleanly in this same change instead of carrying a compatibility alias?

If the answer reveals an existing contract that a runtime/UX simply does not materialize well, classify it as `ja-suportado-so-ux` or `ja-suportado-mal-nomeado-ou-mal-materializado`, not as a reason for a new export. Only `lacuna-real-de-contrato` justifies a new public API.

## Beta Migration Protocol

While Praxis libraries are beta, prefer a clean canonical migration:

1. Add or correct the export at the canonical owner if necessary.
2. Search and migrate all workspace consumers, docs, examples, recipes, manifests, and tests.
3. Remove the obsolete alias/reexport instead of preserving parallel names or package facades.
4. Update direct-consumer and public-boundary proof.
5. Document a real operational exception only when coexistence is unavoidable, including owner, debt, affected consumers, and removal plan.

Do not retain `v1`/`v2`, aliases, deprecated root barrels, or duplicate type definitions merely because a migration requires a search. Avoid a new major version unless the public compatibility assessment demonstrates a governed breaking change beyond the beta cleanup policy.

## AI, Metadata, And Authoring Contracts

An exported Angular API must not duplicate canonical backend semantics. Schemas, `x-ui`, resource keys, actions, capabilities, option sources, domain decisions, and config persistence remain owned by Praxis starters. Angular public APIs consume and materialize those contracts.

For an export that affects authoring, `ComponentDocMeta`, manifests, runtime observations, config shapes, schemas, accepted paths, actions, capabilities, or settings/editor round trips:

- inspect the owning AI manifest and component docs;
- run the canonical registry ingestion/validation path;
- validate runtime/editor parity and persistence where applicable;
- ensure the export does not turn prompt text, labels, aliases, or frontend context into primary semantic routing.

Use structured backend-issued semantic decisions, metadata, catalogs, declared tools, and canonical identifiers. Never introduce keyword or fuzzy routing in a public Angular facade to compensate for a missing backend contract.

## Validation Matrix

Use `praxis-angular-validation-gates` to select exact commands, then satisfy these minimums:

| Public change | Minimum proof |
| --- | --- |
| owner-local public symbol | focused export/spec plus owning library build |
| shared core model/token/service/schema | focused core spec, `npm run build:praxis-core`, and one direct consumer build/test |
| vertical lib export | owning lib build and one direct consumer build/test |
| root barrel or package dependency edge | owner build, direct consumer proof, `npm run build:libs` when local packages may be stale, and `main` dependency-delta review |
| `@praxisui/core` or `@praxisui/ai` public contract | above evidence plus applicable critical-consumer E2E from workspace AGENTS |
| authorable/AI-visible public behavior | focused manifest spec, `npm run generate:registry:ingestion`, and relevant docs/consumer proof |
| release-facing package contract | documented `RELEASE.md` preflight; tarball/package validation is release evidence, not a substitute for consumer proof |

For public AI surfaces, prioritize the focused Dynamic Form, Table, List, and Charts consumer E2E named by the workspace AGENTS. If one does not exercise the changed contract, name the replacement existing lane and why it is equivalent. Do not invent an ad hoc browser flow.

## Derived Artifacts

Review the owning README, package docs, `*.json-api.md`, `docs/praxis-docs.manifest.json`, AI authoring contracts, manifests, registry assets, examples, recipes, playgrounds, landing claims, and i18n-visible copy when relevant.

A valid no-change conclusion must name what was reviewed and why it is unaffected. For example: the symbol remained owner-local, no component metadata/config/authoring contract changed, no docs or examples claim the symbol, no AI registry artifact references it, and no visible text changed.

## Failure Triage

Before altering a contract after a build failure, exclude:

1. stale `dist` versus `node_modules/@praxisui/*` packages;
2. a newly introduced root-barrel dependency edge or circular packaging relationship;
3. an internal symbol exported accidentally rather than a missing public contract;
4. a missing consumer import migration; and
5. metadata/config/runtime behavior that belongs to another canonical owner.

If an audit finds a current cross-root reexport with no accepted migration plan, record it as a `contrato-publico` platform issue in `praxis-ui-angular`, including owner, consumers, clean beta migration, and validation plan. Do not normalize the violation by adding more facades.

## Reporting

Report canonical owner, public entrypoint, consumer map, new/removed dependency edge, classification, exact validation, derived artifacts, beta migration decision, and remaining compatibility risk. State plainly when browser, direct-consumer, registry, docs, or release evidence has not run.

## Companion Skills

- Use `praxis-angular-validation-gates` for focused builds/tests/E2E and Node environment checks.
- Use `praxis-angular-agents-governance` to locate applicable local rules.
- Use `praxis-core-*` skills when the true owner is shared core infrastructure.
- Use `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, and `praxis-ai-turn-orchestration-transport` for AI public contracts.
- Use `praxis-angular-docs-playgrounds`, `praxis-angular-i18n-governance`, `praxis-authoring-editors`, and the functional component skill for derived artifacts and runtime/editor behavior.
