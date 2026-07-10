---
name: praxis-angular-validation-gates
description: Use when choosing, planning, or auditing local validation for Praxis Angular changes in `praxis-ui-angular`, including focused lib builds/tests, consumer builds, Playwright/screenshot QA, AI registry gates, docs validators, release preflight, and deciding when GitHub Actions are or are not appropriate.
---

# Praxis Angular Validation Gates

Use this skill to choose the smallest reliable validation that proves a Praxis Angular change. Validation is part of the platform contract: a green build alone is not enough when the behavior is semantic, authoring-driven, visual, published, or derived into AI/docs artifacts.

## Canonical Rule

Prefer local focused validation during development. Treat GitHub Actions as a phase, release, publication, or hosted-smoke gate, not as the default debugging tool.

Do not run broad suites reflexively. Pick the narrowest official command that proves the changed contract, then state exactly what remains unvalidated.

## Required Preflight

Before choosing commands:

1. Read `praxis-ui-angular/AGENTS.md` and any local `AGENTS.md` for the touched subarea. If the subarea lacks local guidance, use `praxis-angular-agents-governance` and derive gates from root AGENTS, `package.json`, README/docs, focused specs, and public API ownership instead of relying on memory.
2. Classify the change: `local-pequena`, `transversal`, `arquitetural`, `contrato-publico`, or `docs-apenas`.
3. Identify high-risk surfaces: `public-api`, `@praxisui/core`, `@praxisui/dynamic-form`, `@praxisui/table`, AI manifests, docs/playgrounds, i18n catalogs, release assets, or `/api/praxis/config/**` integrations.
4. Inspect `praxis-ui-angular/package.json` for current commands instead of relying on old docs.
5. If the task touches Angular/Node in a mixed OS workspace, verify whether `node_modules` belongs to Windows or Unix before running Node-sensitive commands.

## Validation Matrix

- Local code change in one lib: run the lib build script when present, such as `npm run build:praxis-table`, plus the focused spec or `ng test <project> --watch=false --progress=false --include=<spec>`.
- Public export, shared model, token, provider, or cross-lib contract: run the altered lib build, one direct consumer build/test, and use `praxis-angular-public-api-governance`.
- Authoring editor, Settings Panel, builder, or editable config: run the focused editor/round-trip spec when present and use `praxis-authoring-editors`; add browser validation for open/edit/apply/save/reopen when the behavior is visual or stateful.
- AI manifest or authoring contract: run the focused manifest spec when present, then `npm run generate:registry:ingestion` unless the change is demonstrably narrower; use `praxis-ai-registry-ingestion`.
- Internal UI text or authoring chrome: use `praxis-angular-i18n-governance` and validate catalog updates for both `pt-BR` and `en-US` where the lib has catalogs.
- Public docs, examples, recipes, playgrounds, or landing content: use `praxis-angular-docs-playgrounds` and run the relevant docs validators from the owning project.
- Visual/product UI: use `praxis-ui-product-design`; add screenshot/browser validation in desktop and narrow viewports when feasible.
- Release or npm publication preflight: do not publish locally. Use local preflight commands only as evidence; official publication is through the documented tag/workflow path.

## Common Commands

From `praxis-ui-angular`, prefer current scripts:

- `npm run build:<lib>` for lib-specific builds, for example `build:praxis-core`, `build:praxis-table`, `build:praxis-dynamic-form`, `build:praxis-settings-panel`, `build:praxis-charts`.
- `npm run build:libs` when package graph synchronization from `dist/` to `node_modules/@praxisui/*` matters.
- `npm run test:core`, `npm run test:table`, `npm run test:form`, `npm run test:settings-panel`, or `ng test <project> --watch=false --progress=false --include=<spec>`.
- `npm run generate:registry:ingestion`, `npm run validate:catalog`, and `npm run validate:authoring-contracts` for AI registry surfaces.
- `npm run docs:validate-frontmatter:changed` for changed Angular docs frontmatter.
- `npm run e2e:platform:list` to discover lanes before choosing an E2E lane.
- Use documented local E2E runners under `tools/local-e2e/` only for the matching semantic flow.

For `praxis-ui-landing-page`, use its `package.json` and `AGENTS.md`; common gates include `npm run validate:published-guides`, `npm run validate:sitemap`, `npm run validate:table-manifests`, and `npm run check:integration`.

## Release Boundary

For `@praxisui/*` publication:

- Do not use `npm publish` local or present `npm run release --publish` as the official path.
- Before release guidance, read `RELEASE.md`, `.github/workflows/build-libs.yml`, and `.github/workflows/publish-from-tag.yml`.
- Use local commands such as `release:preflight:npm`, tarball validation, docs validation, and registry ingestion as preflight evidence only.
- Use GitHub Actions only at the release/tag gate or for a hosted smoke that cannot be reproduced locally.

## Output Expectations

When reporting validation, include:

- why the selected validation is sufficient for the scope
- exact commands run and result
- commands intentionally skipped and why
- unvalidated risks, especially browser, docs, registry, direct consumer, and release gates

Never claim full validation when only structural checks or a focused subset ran.
