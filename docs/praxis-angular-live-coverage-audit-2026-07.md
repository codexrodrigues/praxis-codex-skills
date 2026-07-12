# Praxis Angular Live Coverage Audit - July 2026

## Purpose

This audit checks whether the current Praxis Codex skill set is enough to cover the Angular side of Praxis after the latest roadmap waves.

The question is not whether every Angular export has its own skill. The question is whether Codex has enough canonical Praxis knowledge to accelerate future implementation with fewer local guesses, fewer tactical adapters, and more platform-correct decisions.

## Scope

Source audited:

```text
/Users/rodrigo/Dev/pessoal/praxis-plataform/praxis-ui-angular
```

Skill source audited:

```text
/Users/rodrigo/Dev/pessoal/praxis-codex-skills/codex-skills
```

This audit covers `praxis-ui-angular` only. It does not claim exhaustive coverage for `praxis-config-starter`, `praxis-metadata-starter`, `praxis-api-quickstart`, `praxisui-http-examples`, or `praxis-ui-landing-page`, although the current skill repository already includes important coverage for those projects.

## Current Answer

### Reconciliation - 2026-07-11

At this audit point, the skill source contained 147 `praxis-*` skills. The Angular workspace
contains 22 package roots and 24 `public-api.ts` surfaces when the public CRUD
and Table adapters are counted separately. This does not change the coverage
conclusion below: package roots remain the useful ownership measure, while
adapter APIs are separate public contracts to include in validation and routing
guidance.

### Reconciliation - 2026-07-12

After the retrospective review and Wave 3 backend/HTTP proof work, the canonical
`codex-skills/praxis-skills.manifest.json` contains 161 active Praxis skills.
The conclusion remains the same: this is strong canonical coverage, not a reason
to chase the 180-200 exhaustive Angular-only upper band without new source
evidence.

The live recommendation remains evidence-driven curation, not creating skills
to reach a numeric target. As of the follow-up ledger #254, real misses should
be recorded there first and promoted to focused PRs only when source drift,
missing proof, or repeated implementation friction is material. The next formal
audit should regenerate the package metrics and check source drift against this
reconciliation.

The current 161 active Praxis skills are sufficient for strong canonical
coverage of the Angular platform, but not for exhaustive Angular coverage.

The earlier 198-skill estimate remains a reasonable upper bound for exhaustive Angular-only coverage. It is not the next recommended target. The live source audit indicates that the next work should refine discoverability, routing, validation gates, and source-aligned guidance in existing skill families before creating another broad wave of new skills.

Recommended position:

| Coverage goal | Skill count interpretation |
| --- | --- |
| Strong Angular coverage | Current 161 skills are enough to operate effectively. |
| Exhaustive Angular coverage | 180-200 skills remains a reasonable upper band. |
| Whole Praxis platform coverage | 198 skills is not enough if config, metadata, quickstart, examples, and landing are covered with the same depth. |

## Live Angular Inventory

The current Angular workspace exposes 22 public packages under `projects/*`.

| Metric | Count |
| --- | ---: |
| Public packages | 22 |
| `public-api.ts` exports | 800 |
| Components | 249 |
| Services | 125 |
| Directives | 8 |
| Specs | 599 |
| Markdown docs under package `docs/` | 149 |
| `*.json-api.md` files | 85 |
| AI/authoring/manifest/context signal files | 361 |
| Authoring manifest files | 20 |

The inventory confirms that the Angular surface is too large to reason about by raw component count. A skill-per-component model would produce noisy guidance. The better model is canonical skill families for runtime, authoring, AI manifests, Settings Panel round-trip, docs/examples, validation, and cross-lib public API boundaries.

## Package Signals

| Package | Exports | Components | Specs | Docs | JSON API docs | AI signal files | Authoring manifest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `praxis-core` | 227 | 15 | 126 | 46 | 0 | 60 | 0 |
| `praxis-dynamic-fields` | 191 | 79 | 104 | 14 | 72 | 31 | 1 |
| `praxis-dynamic-form` | 42 | 20 | 58 | 7 | 6 | 29 | 1 |
| `praxis-table` | 40 | 18 | 98 | 32 | 1 | 34 | 1 |
| `praxis-charts` | 37 | 6 | 19 | 0 | 0 | 9 | 1 |
| `praxis-visual-builder` | 31 | 17 | 13 | 0 | 0 | 10 | 1 |
| `praxis-ai` | 24 | 6 | 19 | 4 | 0 | 53 | 0 |
| `praxis-settings-panel` | 23 | 4 | 12 | 1 | 0 | 6 | 1 |
| `praxis-page-builder` | 20 | 11 | 21 | 2 | 0 | 21 | 1 |

These are the highest-risk packages for future skill drift because they combine public APIs, authoring flows, AI manifests, and cross-lib runtime behavior.

## Current Skill Coverage By High-Risk Area

| Area | Current skill family | Count | Coverage reading |
| --- | --- | ---: | --- |
| Core runtime and contracts | `praxis-core-*` | 12 | Strong. Matches public API, resource runtime, providers, i18n, observations, global actions, registry, and materialization. |
| Table | `praxis-table-*` | 12 | Strong. Covers runtime data, filters, authoring settings, rules, selection/export, analytics, diagnostics, and data precedence. |
| Dynamic form | `praxis-form-*` | 8 | Substantively strong, but naming is weaker than the package boundary because the package is `praxis-dynamic-form`. |
| Dynamic fields | `praxis-fields-*` plus `praxis-dynamic-fields-editorial` | 9 | Substantively strong, but naming is weaker than the package boundary because most skills omit `dynamic-fields`. |
| AI | `praxis-ai-*` | 8 | Strong. Covers assistant runtime, session context, transport, backend config contracts, manifests, registry ingestion, and semantic intent. |
| Charts | `praxis-charts-*` | 7 | Strong for runtime, authoring, ECharts boundary, analytics interactions, catalogs, and handlers. |
| Visual builder | `praxis-visual-builder-*` | 5 | Good. Covers graph runtime, JSON Logic round-trip, schemas/templates, rules, and validation. |
| Page builder | `praxis-page-builder-*` | 3 | Adequate but should be watched because the local `AGENTS.md` now documents heavier validation gates for agentic authoring. |
| Settings Panel | `praxis-settings-*` | 4 | Adequate. Covers shell, global config, round-trip authoring, AI/i18n validation. |
| Table rule builder | Mostly `praxis-table-rule-*` | 4 | Adequate by ownership, but no direct `praxis-table-rule-builder-*` name. |

## Aderencia Classification

| Finding | Classification | Interpretation |
| --- | --- | --- |
| 161 active skills cover the major Angular semantic boundaries and backend-adjacent Praxis surfaces. | `ja-suportado-so-ux` | The repository already has enough skill families to guide normal Angular implementation and current platform proof work. The user-facing planning question needs this evidence projected clearly. |
| `praxis-dynamic-form` has 42 exports, 20 components, 58 specs, 7 docs, an authoring manifest, and 8 relevant `praxis-form-*` skills, but no direct `praxis-dynamic-form-*` skill names. | `ja-suportado-mal-nomeado-ou-mal-materializado` | Coverage exists, but skill discovery can under-route tasks that mention the package name exactly. |
| `praxis-dynamic-fields` has 191 exports, 79 components, 104 specs, 72 JSON API docs, and 9 relevant skills, but most use `praxis-fields-*` rather than `praxis-dynamic-fields-*`. | `ja-suportado-mal-nomeado-ou-mal-materializado` | Coverage exists, but naming creates the same discovery risk in the largest Angular field surface. |
| `praxis-page-builder` local guidance now includes heavy agentic validation gates and environment assumptions. | `suportado-parcialmente` | Existing skills cover authoring/composition/AI, but should be checked for parity with the current `AGENTS.md` validation model. |
| `praxis-table-rule-builder` is covered through table-rule skills, but direct package-name discovery returns no skill names. | `ja-suportado-mal-nomeado-ou-mal-materializado` | Coverage exists by domain, but exact package routing is less obvious. |
| No evidence requires a new Angular public contract or new platform abstraction. | Not `lacuna-real-de-contrato` | The next work belongs in skill curation and routing, not Angular runtime contract creation. |

## Recommended Follow-Up Issues

Create a small, evidence-driven backlog instead of a broad skill-count wave.

Status as of the post-audit curation pass: all four follow-up issues below were completed and merged.

1. Curate dynamic-form skill discoverability and source parity.

   Scope: review `praxis-form-*` skills against `projects/praxis-dynamic-form/AGENTS.md`, `README.md`, docs, authoring manifest, config editors, layout/rules/messages/hooks/actions editors, and focal validation commands.

   Expected outcome: either rename or add explicit routing language so tasks mentioning `@praxisui/dynamic-form` reliably load the correct skill family.

   Status: completed in PR #110.

2. Curate dynamic-fields skill discoverability and editorial chain parity.

   Scope: review `praxis-fields-*` and `praxis-dynamic-fields-editorial` against `projects/praxis-dynamic-fields/AGENTS.md`, field catalog docs, inline filter contracts, component registry, descriptors, loader specs, JSON API docs, and host custom field guides.

   Expected outcome: make the skill family unmistakably canonical for `@praxisui/dynamic-fields`, especially runtime coverage versus editor/tooling coverage.

   Status: completed in PR #111.

3. Curate page-builder agentic validation gates.

   Scope: compare `praxis-page-builder-*` skills with the current local `AGENTS.md`, especially agentic authoring, SSE/backend gates, Settings Panel bridge, catalog AI, graph editor, shell editor, and environment assumptions for the full validation gate.

   Expected outcome: prevent future implementations from closing page-builder AI work with only a build or smoke when the local source requires the heavier gate.

   Status: completed in PR #112.

4. Curate package-name aliases for table-rule-builder and settings-related routing.

   Scope: ensure tasks mentioning exact package names such as `praxis-table-rule-builder` and `praxis-settings-panel` route to the correct canonical skill family without encouraging duplicate concepts or convenience wrappers.

   Expected outcome: better task-to-skill routing without creating parallel semantic layers.

   Status: completed in PR #113.

## Post-Curation Recommendation

Do not create new Angular skill-count issues immediately. The current next step
is to use the curated 161 active skills during real Praxis implementation and
record only evidence-backed misses in #254:

- a skill routes to the wrong canonical owner;
- a skill misses a validation gate that the source requires;
- a package changes public API, authoring manifest, docs registry, or AI registry behavior;
- a recurring implementation task needs new canonical guidance rather than local adaptation.

## What Not To Do Next

Do not create 52 new skills merely to move from 146 to 198.

Do not treat `198` as a platform-wide answer. It is only an Angular exhaustive upper-band estimate.

Do not generate one skill per component or per public export. The current platform evidence supports canonical family skills with strong routing and validation gates.

Do not solve package-name discovery by creating duplicated parallel skills unless the existing families cannot be safely renamed or routed.

## Validation Performed

This audit used local source inspection only:

- GitHub issues check: no open roadmap/review issues at the original audit
  point; #254 is now the active evidence ledger, not a broad backlog issue.
- Skill manifest check: 161 Praxis skills, all active, after the 2026-07-12 reconciliation.
- Angular source inventory across `praxis-ui-angular/projects/*`.
- Local `AGENTS.md` review for `praxis-ui-angular`, `praxis-dynamic-form`, `praxis-dynamic-fields`, `praxis-table`, `praxis-page-builder`, and `praxis-ai`.
- Package scripts review for focal Angular build/test/e2e gates.

No PowerShell sync script was executed because this audit did not change canonical skill files.
