---
name: praxis-angular-validation-gates
description: Use when selecting, running, auditing, or reporting local validation for Praxis Angular changes in praxis-ui-angular: lib/public API builds and consumers, focused specs, authoring round trips, AI registry artifacts, i18n/docs/playgrounds, Playwright and local E2E lanes, package/release preflight, Node environment ownership, derived artifacts, or the decision to use GitHub Actions.
---

# Praxis Angular Validation Gates

Use this skill to select the smallest reliable evidence for a Praxis Angular change. Validation proves a semantic, public, authoring, or visual contract; a green TypeScript build alone does not prove that a runtime, editor, metadata contract, or consumer remains coherent.

## Preflight Before Commands

Before choosing a gate:

1. Read `praxis-ui-angular/AGENTS.md`, `codex-rules.md`, and every applicable local `AGENTS.md` under the changed project or tool. Load the Angular MCP guidance when implementing Angular code, following the workspace's documented flow; do not claim framework guidance that was not retrieved.
2. Classify `docs-apenas`, `local-pequena`, `transversal`, `contrato-publico`, or `arquitetural`.
3. Identify the canonical owner and risk: `public-api`, shared core models/tokens/services, configuration/editor round trip, AI manifest/registry, i18n, metadata/schema/action/capability consumption, docs/playgrounds, visual UX, package/release, or cross-repository config integration.
4. Inspect the current root `package.json`, project package, local AGENTS, focused specs, and documented E2E lane. Do not invent scripts from memory.
5. Verify `node_modules` ownership before Node/Angular commands. On a Windows-owned install (Windows native packages or `.cmd` bins), invoke npm/npx/ng through `cmd.exe /c`; on a Unix install use its owning shell. Do not mix installations across environments.
6. Check whether a consumer may resolve stale `node_modules/@praxisui/*` rather than current `dist/*`. For cross-lib type/export failures, run the canonical `npm run build:libs` synchronization before changing a public contract.
7. List derived artifacts that may need review: `public-api.ts`, manifests, registry/corpus, docs, recipes/playgrounds, i18n catalogs, screenshots, landing content, package assets, and consumer builds.

## Evidence Selection

Start with the narrowest applicable row. Add a row only when the changed contract crosses that boundary.

| Changed surface | Minimum local evidence |
| --- | --- |
| one lib implementation, no public shape | focused `.spec.ts` then the owning lib build, such as `npm run build:praxis-table` |
| shared core model/token/service/schema/runtime contract | focused core spec or `npm run test:core`, `npm run build:praxis-core`, and a real direct-consumer build/test |
| public export or cross-lib contract | altered lib build, `public-api` audit with `praxis-angular-public-api-governance`, `npm run build:libs` if consumer packages need sync, and a direct consumer proof |
| table/form/list behavior | owning build plus `npm run test:table`, `npm run test:form`, or focused `ng test <project> --watch=false --progress=false --include=<spec>` |
| editable config, authoring editor, Settings Panel bridge | focused runtime/config/editor/round-trip specs; browser proof for open, edit, apply/save, reopen, and reset when visible/stateful |
| AI component manifest, docs metadata, catalog tool | focused manifest/tool spec, `npm run generate:registry:ingestion`, then `npm run validate:catalog` and `npm run validate:authoring-contracts` when not already part of ingestion |
| internal framework UI text | `praxis-angular-i18n-governance`, relevant specs, and both `pt-BR`/`en-US` catalog updates; preserve UTF-8 |
| docs, recipes, examples, playgrounds | `praxis-angular-docs-playgrounds` and the owning changed-doc validator, such as `npm run docs:validate-frontmatter:changed` |
| visual/product behavior | focused functional evidence plus browser/screenshot evidence at desktop and narrow viewport with `praxis-ui-product-design` |
| config-starter/quickstart integration or semantic decision materialization | matching focused local E2E lane or documented cross-repository smoke, only after unit/build proof |
| release/package/publication | documented local preflight from `RELEASE.md`; GitHub tag/workflows remain the only official publish path |
| skills-only change | skill structure, manifest hashes, generated issue draft, local sync, and audit only; do not run Angular suites without code/generated/runtime change |

Do not count a mock-only spec as browser, persistence, authoring, or cross-project proof. Conversely, do not run the complete workspace merely because a narrow contract is public; broaden based on actual consumers and risk.

## Core Commands And Their Meaning

Use exact current scripts from the workspace:

- `npm run build:praxis-core`, `build:praxis-table`, `build:praxis-dynamic-form`, `build:praxis-settings-panel`, or `build:praxis-charts`: focused packagable library builds.
- `npm run build:libs`: builds the package graph and synchronizes built packages into `node_modules/@praxisui/*`; use it before treating consumer compilation against stale local packages as a true regression.
- `npm run test:core`, `test:table`, `test:form`, `test:settings-panel`: focused project suites. For a precise spec, use the workspace Angular CLI form with `--include=<spec>`.
- `npm run generate:registry:ingestion`: extracts component docs, generates AI metadata/ingestion, validates catalog governance, and validates authoring contracts. Do not edit derived registry output as a shortcut.
- `npm run docs:validate-frontmatter:changed`: validates changed documentation frontmatter; use the owning docs/playground guidance for broader public claims.
- `npm run e2e:platform:list`: discover available deterministic platform lanes before choosing one. It is discovery only, not E2E proof.

For a new public component behavior, a manifest or registry check does not replace a lib build. For a public API change, a lib build does not replace a consumer proof. Keep these distinctions explicit.

## Public API And Consumer Proof

Changes to root `public-api.ts`, exported types, tokens, services, AI contracts, or shared models require a consumer map before edits. Validate the altered library and at least one direct real consumer. For `@praxisui/core` or `@praxisui/ai` public surfaces, include a focused consumer E2E lane where the contract is visually/runtime critical.

Never solve a stale consumer or circular dependency by reexporting another public library through a root barrel. First compare the dependency graph with `main`, confirm `dist`/`node_modules` synchronization, then correct the canonical owner or define a stable minimal contract.

## Authoring, Metadata, And AI Gates

An editable runtime/config change is incomplete until its canonical editor or builder can materialize and round-trip it. Validate runtime/config normalization plus the actual editor path. Include save/reopen behavior whenever persistence is part of the contract, and test invalid/no-result/blocked state where applicable.

For public functional components, inspect the AI authoring manifest, `ComponentDocMeta`, recipes, and registry surface. Run registry ingestion for functional, public, authoring, capability, operation, schema/path, or docs-meta changes; explain explicitly when no manifest/registry artifact applies.

Do not treat frontend observations, labels, or prompt text as authoring authority. AI E2E must prove that backend-governed semantic decisions, actions, schemas, and materializations are consumed rather than recreated in Angular.

## Browser And Local E2E Lanes

Choose an existing lane by its semantic contract and prerequisites:

- `e2e:platform:*` lanes cover deterministic persistence/connection labs; inspect the listed route/spec before execution.
- `tools/local-e2e/run-page-builder-agentic-*.sh` cover real browser, backend SSE, provider, and managed config-starter/quickstart integration.
- shared-rule, Domain Knowledge, and Dynamic Form domain-rules lanes prove governed decision materialization; they must not be replaced by frontend mocks or ad hoc Playwright commands.
- quickstart remote metadata lab uses the official origin `http://localhost:4003`; do not substitute another host/port because CORS/config behavior is part of the evidence.

Read `tools/local-e2e/README.md` first. Respect its required backend, database, stream-auth, provider credential, port, and cleanup rules. Do not run a live/mutating lane casually, against an unknown scope, or in parallel with another lane that shares ports or persistent fixtures. For visual changes, inspect desktop and narrow viewport screenshots; for lookup/search, test both a matching and no-result query.

## Docs, Release, And Actions

Review public docs, examples, recipes, playgrounds, landing claims, generated package assets, and i18n whenever a published surface changes. State why each reviewed artifact is unchanged when it was intentionally not updated.

For release preparation, read `RELEASE.md`, `build-libs.yml`, and `publish-from-tag.yml`. The documented preflight includes package/audit/link/build/peer/docs/registry/tarball checks. Local `release:preflight:npm`, packing, or dry-runs are evidence only. Do not run local `npm publish` or present it as the official release route.

GitHub Actions is for the final release/tag, publication, or hosted-only smoke. During development, prefer local focused tests, builds, local E2E, and package checks; do not spend remote runs to discover failures reproducible locally.

## Failure Triage

Classify a failure before broadening tests:

1. Environment/tooling mismatch: Node ownership, missing browser, ports, credentials, or stale `dist`/`node_modules`.
2. Focused implementation regression: fix the owning lib/spec.
3. Public boundary regression: identify export/consumer/dependency owner and add direct-consumer proof.
4. Editor/manifest/docs drift: correct the derived artifact or canonical materialization, not a local display workaround.
5. Cross-project contract issue: reproduce locally, route to metadata/config/quickstart owner, and keep Angular as downstream proof.

Never describe a skipped browser, consumer, registry, docs, release, or live E2E gate as validated.

## Reporting Template

Report:

- classification, canonical owner, and changed contract;
- commands executed with result and why they prove the scope;
- direct consumers, derived artifacts, and visual/live lanes reviewed or updated;
- gates intentionally skipped and why;
- remaining risks and whether a hosted/release gate is still required.

## Companion Skills

- Use `praxis-angular-agents-governance` to locate and apply local workspace rules.
- Use `praxis-angular-public-api-governance` for cross-lib exports and consumer maps.
- Use `praxis-angular-i18n-governance` and `praxis-angular-docs-playgrounds` for their derived artifacts.
- Use `praxis-authoring-editors` and `praxis-ui-product-design` for editable and visual surfaces.
- Use `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion` for AI component contracts and registry artifacts.
- Use functional component skills, `praxis-config-*`, and quickstart skills for the canonical source behind cross-project validation.
