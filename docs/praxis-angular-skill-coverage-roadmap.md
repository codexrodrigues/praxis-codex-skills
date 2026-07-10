# Praxis Angular Skill Coverage Roadmap

## Purpose

This document records a first-pass coverage estimate for Codex skills that would be needed to cover the Angular side of Praxis with meaningful platform knowledge.

The goal is not to create one skill per file, export, or component. The goal is to size a skill roadmap that helps Codex make canonical Praxis decisions across `@praxisui/*` runtimes, authoring surfaces, metadata-driven UX, AI manifests, validation, examples, and derived artifacts.

## Scope

Source audited:

```text
/Users/rodrigo/Dev/pessoal/praxis-plataform/praxis-ui-angular
```

Angular is only one of the three main Praxis platform fronts:

- `praxis-config-starter`
- `praxis-metadata-starter`
- `praxis-ui-angular`

This estimate covers `praxis-ui-angular` only. A full-platform skill program that also covers config and metadata starters would need a larger number.

## Current Repository Coverage

Status after Wave 6, with `codex-skills/praxis-skills.manifest.json` at 146 skills:

| Metric | Count |
| --- | ---: |
| Praxis skills in manifest | 146 |
| Active Praxis skills | 145 |
| Active skills needing curation | 1 |
| Open roadmap issues | 0 |

The entry still marked `active-needs-curation` is:

- `praxis-java-host-project`

The repository has moved past the minimum useful coverage tier and is now inside the strong canonical coverage band for the Angular side. The current 146-skill set is no longer just an initial foundation: it encodes substantial platform knowledge across runtime, authoring, AI, validation, docs, metadata, config, quickstart proof, HTTP examples, and landing/public docs.

It should still not be treated as exhaustive coverage. The largest remaining risk is not raw skill count, but whether each high-complexity Praxis surface has enough canonical guidance to prevent local workarounds, keyword-based routing, duplicated contracts, or weak validation choices during future implementation.

### Current Coverage By Area

This distribution is based on skill names in the manifest and is meant as planning evidence, not as a strict ownership taxonomy.

| Area | Skills |
| --- | ---: |
| `praxis-core*` | 12 |
| `praxis-table*` | 12 |
| `praxis-form*` | 8 |
| `praxis-fields*` plus `praxis-dynamic-fields-editorial` | 9 |
| `praxis-ai*` | 8 |
| `praxis-metadata*` including metadata editor | 8 |
| `praxis-config*` | 5 |
| `praxis-charts*` | 7 |
| `praxis-page-builder*` | 3 |
| `praxis-visual-builder*` | 5 |
| `praxis-settings*` | 4 |
| `praxis-crud*` | 4 |
| `praxis-list*` | 4 |
| `praxis-api-quickstart*` | 4 |
| `praxis-http-examples*` | 3 |
| `praxis-landing*` | 2 |

Coverage added through the completed roadmap waves now includes:

- Angular runtime and host integration, public API, validation, i18n, docs/playgrounds, and design guidance.
- Core metadata/resource/action/surface materialization, global actions, widget observations, providers, logging, and component registry contracts.
- Table, dynamic form, dynamic fields, charts, CRUD, list, settings, navigation, files upload, rich content, cron, table rule builder, metadata editor, manual form, editorial forms, page builder, visual builder, and AI authoring families.
- Backend-adjacent platform skills for `praxis-metadata-starter`, `praxis-config-starter`, `praxis-api-quickstart`, `praxisui-http-examples`, and `praxis-ui-landing-page`.

## Angular Workspace Inventory

The Angular workspace currently exposes 22 `projects/*` packages.

| Metric | Count |
| --- | ---: |
| Public Angular packages | 22 |
| Public exports from `public-api.ts` | 798 |
| Angular components | 280 |
| Services | 134 |
| Directives | 13 |
| Injection token files/usages | 46 |
| Exported interfaces | 1630 |
| Exported classes | 486 |
| Specs | 599 |
| Top-level `src/lib` directories | 164 |
| Domain top-level directories, excluding common folders | 96 |
| Authoring/config/editor/builder-related files | 460 |
| AI/manifest-related files | 132 |

These numbers are intentionally not used as direct skill counts. They are evidence that the Angular surface is too large to be covered by the current skill set or by a handful of generic skills.

## Library Inventory

| Library | Exports | Components | Services | Specs | Domain dirs |
| --- | ---: | ---: | ---: | ---: | ---: |
| `praxis-ai` | 24 | 7 | 12 | 19 | 3 |
| `praxis-charts` | 37 | 8 | 14 | 19 | 5 |
| `praxis-core` | 227 | 16 | 50 | 126 | 15 |
| `praxis-cron-builder` | 7 | 1 | 0 | 6 | 0 |
| `praxis-crud` | 14 | 5 | 2 | 12 | 0 |
| `praxis-dialog` | 15 | 3 | 2 | 7 | 2 |
| `praxis-dynamic-fields` | 191 | 78 | 6 | 104 | 8 |
| `praxis-dynamic-form` | 42 | 25 | 9 | 58 | 14 |
| `praxis-editorial-forms` | 28 | 10 | 0 | 15 | 3 |
| `praxis-expansion` | 5 | 2 | 0 | 5 | 0 |
| `praxis-files-upload` | 2 | 4 | 5 | 12 | 4 |
| `praxis-list` | 23 | 22 | 2 | 18 | 3 |
| `praxis-manual-form` | 17 | 7 | 3 | 8 | 5 |
| `praxis-metadata-editor` | 13 | 7 | 6 | 14 | 6 |
| `praxis-page-builder` | 20 | 11 | 1 | 21 | 3 |
| `praxis-rich-content` | 8 | 2 | 1 | 8 | 0 |
| `praxis-settings-panel` | 23 | 4 | 3 | 12 | 1 |
| `praxis-stepper` | 9 | 16 | 0 | 9 | 1 |
| `praxis-table` | 39 | 23 | 9 | 98 | 18 |
| `praxis-table-rule-builder` | 14 | 7 | 1 | 5 | 1 |
| `praxis-tabs` | 9 | 4 | 0 | 10 | 1 |
| `praxis-visual-builder` | 31 | 18 | 8 | 13 | 3 |

## Coverage Interpretation

### Minimum useful coverage: 55-70 skills

This tier gives Codex reliable behavior for common Praxis work:

- one skill per major library or component family;
- shared skills for Angular host setup, authoring editors, metadata contracts, visual product design, validation, i18n, public API, and AI manifests;
- enough guidance to avoid common local workarounds.

This tier is now complete and should be treated as surpassed.

### Strong canonical Angular coverage: 140-170 skills

This is the recommended planning target. The current 146-skill manifest is inside this band.

It allows each complex library to have several focused skills for:

- runtime usage;
- canonical config;
- visual authoring;
- Settings Panel round-trip;
- AI authoring manifests;
- metadata/schema/capabilities integration;
- derived docs/examples/playgrounds;
- validation and E2E gates;
- public API and cross-lib dependency rules.

At this tier, Codex can encode Praxis platform knowledge instead of merely remembering docs. The current repository is now in this tier, with the caveat that some areas still need deeper audit against the live monorepo before being called exhaustive.

### Exhaustive Angular coverage: 180-200 skills

This tier covers:

- each major subdomain in table, dynamic form, dynamic fields, core, page builder, visual builder, AI, charts, metadata editor, and settings panel;
- advanced recipes and migrations;
- component-specific authoring/E2E/manifest/playground guidance;
- specialist skills for uncommon but high-risk surfaces.

198 skills is enough for this Angular-only exhaustive tier, but it should be treated as an upper bound, not an automatic target. The next decisions should be driven by source audit and implementation failures, not by filling a number.

## Recommended Target

Recommended Angular-only planning number:

```text
160 canonical skills
```

Recommended capacity range:

```text
140-170 skills for strong coverage
180-200 skills for exhaustive coverage
```

Therefore:

- 198 skills is enough for `praxis-ui-angular` if the goal is exhaustive Angular coverage.
- 198 skills is probably higher than necessary for a strong first canonical roadmap.
- 198 skills is not enough for the entire Praxis platform if config and metadata starters are included with the same depth.
- 146 skills is enough to operate as strong canonical Angular coverage, but not enough to declare the whole Praxis platform exhaustively covered.

## Proposed Waves

The waves below are retained as the original sizing model. Waves 1-6 have effectively been executed through the closed roadmap issues. Future waves should now be smaller, evidence-driven refinement cycles.

### Wave 1 - Foundation

Target: 25-35 skills.

- Angular host integration
- Core metadata/schema/actions/surfaces/capabilities
- Component minimums
- UI product design
- Authoring editors
- Settings Panel
- Dynamic fields editorial chain
- Dynamic form runtime
- Table runtime
- CRUD runtime
- Dashboard/charts analytics
- AI manifest and registry basics
- Public API and cross-lib dependency guardrails

### Wave 2 - Complex Library Depth

Target: 55-75 additional skills.

- `praxis-table`: filters, rules, formatting, toolbar actions, local/remote data, config editors, inline authoring, CRUD integration, analytics, visual formula builder.
- `praxis-dynamic-form`: config editor, layout editor, rules, hooks, messages, actions, canvas, filter form, submit payload semantics.
- `praxis-dynamic-fields`: registry, loaders, descriptors, entity lookup, async select, inline filters, catalog, canvas integration.
- `praxis-core`: action/surface adapters, schema, logging, i18n, widgets, providers, metadata services.
- `praxis-page-builder` and `praxis-visual-builder`: builder graph, shell, editor contracts, AI integration, round-trip.

### Wave 3 - Authoring And AI Completeness

Target: 35-45 additional skills.

- One focused skill family per authoring manifest.
- AI registry ingestion and validation.
- Component authoring contracts.
- Settings Panel round-trip per major component family.
- Visual QA and accessibility gates.
- i18n/editor text governance.

### Wave 4 - Recipes, Edge Cases, And Published Surfaces

Target: 25-35 additional skills.

- Examples and playgrounds.
- Landing/documentation synchronization.
- Migration recipes.
- E2E focal suites.
- Release/publication preflight.
- High-risk package-specific edge cases.

## Immediate Backlog Recommendation

Do not create another batch of broad skill-generation issues just to increase the count. The next backlog should be driven by audit findings, curation gaps, and observed implementation misses.

Recommended next issues:

1. Curate `praxis-java-host-project` against current `praxis-metadata-starter`, `praxis-config-starter`, and `praxis-api-quickstart` guidance.
2. Run a live monorepo coverage audit for the most complex Angular packages: `praxis-core`, `praxis-table`, `praxis-dynamic-form`, `praxis-dynamic-fields`, `praxis-page-builder`, `praxis-visual-builder`, `praxis-ai`, and `praxis-charts`.
3. Verify whether the 146 current skills still match source reality after recent platform changes, especially public APIs, authoring manifests, AI contracts, docs registries, quickstart scripts, and HTTP examples.
4. Create only focused follow-up issues where the audit finds one of these signals:
   - recurring missing canonical guidance;
   - skill guidance drifting from source;
   - high-risk runtime/API surface not covered by a focused skill;
   - validation gates missing or too broad;
   - a public docs/example/playground projection that can mislead future implementation;
   - any guidance that still encourages local adapters, keyword routing, duplicate contracts, or frontend-only semantics.

Recommended near-term target:

```text
146 -> 150-160 curated skills
```

That range leaves room for real gaps without turning the roadmap into a count-driven exercise. A move toward 180-200 skills should happen only after a new source audit proves that exhaustive Angular coverage is worth the maintenance cost.
