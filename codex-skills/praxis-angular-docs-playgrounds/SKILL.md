---
name: praxis-angular-docs-playgrounds
description: Use when implementing, auditing, synchronizing, or validating Praxis Angular public documentation and derived experiences: library README/json-api/host/editor docs, docs/praxis-docs.manifest.json, docs shell and vendor sync, component/published-guide registries, examples, AI recipes, playground/demo routes, screenshots, landing pages, sitemap, LLM/public guide artifacts, or documentation-contract drift.
---

# Praxis Angular Docs And Playgrounds

Use this skill when a Praxis contract must be published as documentation, recipe, example, playground, or landing experience. These are derived evidence surfaces. They explain and demonstrate what the canonical owner already publishes; they do not invent runtime semantics, backend rules, AI routes, or business behavior.

## Classify The Publication Change

Classify before editing:

- `docs-apenas`: editorial or explanatory change with no public runtime/config/metadata contract change.
- `local-pequena`: one library document, manifest item, recipe, or demo with no cross-project projection.
- `transversal`: source library plus AI registry, docs shell, landing, public guide, recipe, or example consumer.
- `contrato-publico`: public API/config/schema/action/capability/manifest/host integration claim or published route changes.
- `arquitetural`: documentation exposes an unclear owner or a contradiction between Angular, metadata starter, config starter, Quickstart, or landing.

For every non-editorial claim, identify the canonical source, executable evidence, affected projection chain, intended audience, and minimum validation before writing copy.

## Canonical Sources And Projection Chain

Keep these roles distinct:

- `praxis-ui-angular` owns component runtime, public APIs, component docs, manifests, examples, recipes, playground source, and AI registry extraction.
- `praxis-metadata-starter` owns backend `x-ui`, filtered schemas, actions, surfaces, capabilities, option sources, and discovery semantics.
- `praxis-config-starter` owns persisted config, AI/context/authoring, domain decisions, ETag, and governed materialization lifecycle.
- `praxis-api-quickstart` proves those contracts in a real host.
- `praxis-ui-landing-page` projects library documentation into public routes; it never overrides the owning library.

The canonical docs flow is:

`library source/runtime/spec -> README/API/host/editor docs -> docs manifest -> landing vendor sync -> generated component docs/published-guide registries -> route links and sitemap`.

When any step disagrees, repair the canonical owner or record the drift. Do not alter a landing sentence, generated vendor file, screenshot, or recipe merely to conceal an incorrect contract.

## Required Inventory

Read `praxis-ui-angular/AGENTS.md`, `codex-rules.md`, the owning library `AGENTS.md`, `README.md`, `src/public-api.ts`, relevant component/manifest/spec, and `docs/praxis-docs.manifest.json`. For component landing work, read:

- `docs/component-documentation-contract.md` and `docs/component-documentation-matrix.md`;
- `docs/templates/component-landing-template.md` and `docs/templates/README.md`;
- `praxis-ui-landing-page/AGENTS.md`, `component-docs.registry.ts`, and `landing-docs.registry.ts`.

For AI-authorable behavior, inspect the manifest, `ComponentDocMeta`, registry tooling, and the component's recipe specs. For a backend-derived claim, inspect the corresponding metadata/config/Quickstart owner and its HTTP or focused test evidence before documenting it.

## Documentation Contract

Every public component surface has a deliberate role:

| Surface | Must establish |
| --- | --- |
| overview | what Praxis materializes, why it differs from a basic widget, host boundary, and real value |
| API | public inputs/outputs/events/config, precedence, defaults, constraints, and breaking behavior |
| examples | executable or copyable proof of a valuable scenario, not decorative rendering |
| host integration | required providers, persistence, authorization, backend/metadata/config responsibilities |
| editor | runtime/config to visual-authoring parity, supported fields, apply/save/reset/reopen limits |
| AI | capabilities, context, grounding, safety limits, authoring/apply boundary, and evidence |
| styles | tokens, theming, density, and safe customization limits |
| architecture/troubleshooting | owner decisions, failure signatures, and canonical correction path |

`docs/praxis-docs.manifest.json` records the owner, source paths, publication type, canonicality, routes, and automation. Only `docs-shell` or `component-route` content becomes a docs-shell surface. `published-guide` remains a supplemental public guide; `source-only` is evidence, not a promise to render a public tab. Never promote an empty, unverified, or source-only artifact to a public component claim.

## Writing And Claim Rules

Write for a technical buyer, product decision maker, or implementer: value, contract, host responsibility, evidence, and limit. Do not write production instructions, private implementation checklists, or marketing claims unsupported by code, manifest, runtime, metadata, spec, or host proof.

Describe Angular components as governed, metadata-driven runtime surfaces. Preserve these boundaries:

- schemas, `x-ui`, actions, surfaces, capabilities, option sources, and resource identity come from metadata contracts;
- config/AI/domain decisions are authored and persisted at the config boundary;
- Angular materializes those contracts and does not become a primary business-rule or intent-routing owner;
- host business labels/content remain metadata/config values, not library prose or i18n defaults.

Do not route user intent through labels, route fragments, aliases, regexes, or prompt phrases in examples or recipes. Use canonical component/resource/action/capability identifiers and backend-governed semantics. A recipe demonstrates declared capabilities; it does not authorize arbitrary JSON or a local frontend command parser.

## Examples, Recipes, And Playgrounds

An example or recipe must be tied to a canonical source and focused spec. It should declare setup, required host/backend context, expected materialized outcome, limitations, and the smallest reproducible flow. Update its importing recipe spec when its payload/contract changes.

For visual or interactive playgrounds, prove the actual behavior in the owning runtime and, when relevant, the editor round trip. Use official routes/origins/ports and existing E2E lanes; do not create a parallel demo server or mock away a metadata/config/AI contract that the public example claims to exercise. Validate desktop and narrow viewports when the change affects visible composition, content fit, accessibility, or authoring.

Generated artifacts under `dist/`, vendored landing copies, generated registry output, and package assets are never hand-edited. Regenerate/synchronize through the owning script.

## Derived Artifact Decision Matrix

| Changed canonical surface | Review/update |
| --- | --- |
| public API, config shape, default, event, provider | README/API, manifest, examples, host/editor docs, consumer/landing claims |
| `ComponentDocMeta`, authoring manifest, AI capability/operation/context | manifest specs, `examples/ai-recipes`, registry ingestion, AI docs, playground/assistant evidence |
| metadata/schema/action/surface/capability/option source | owner docs/HTTP evidence first, then Angular guides/examples that consume it |
| runtime/editor persistence or visible authoring | editor docs, screenshots/playground, apply/save/reset/reopen proof |
| docs manifest/source path/publication/route | landing vendor sync, component/published-guide registries, links, sitemap |
| i18n or visible copy | docs/screenshots/examples that quote it plus i18n coverage |
| package/release claim | package docs, public links, npm/landing claims, release validation |

When nothing changes, record negative evidence: no public behavior/manifest/metadata/config changed, no example or public claim references it, no recipe/registry source changed, no visible copy changed, and no landing/sitemap/package surface is affected.

## Validation

Run the smallest official gate that proves the affected projection:

| Scope | Minimum validation |
| --- | --- |
| changed governed Angular docs | `npm run docs:validate-frontmatter:changed` |
| changed publishable docs/assets | `npm run validate:published-doc-assets` |
| component docs/metadata/AI registry projection | focused manifest/recipe specs plus `npm run generate:registry:ingestion` |
| changed library example/playground | owning lib build/spec and focused browser/E2E proof when interactive |
| docs manifest intended for landing | in landing: `npm run vendor-docs:sync`, then `npm run validate:vendor-docs` and `npm run docs:validate` |
| landing guide/route publication | `npm run validate:published-guides` and `npm run validate:sitemap`; run `npm run sitemap:sync` only when intentional route drift requires it |
| landing `site.data.ts` table manifests/examples | `npm run validate:table-manifests` |
| broad landing projection | `npm run check:integration` after focused validation is green |

Use `praxis-angular-validation-gates` for Node environment and build/test selection. For landing-to-Quickstart validation, use the documented `4301` origin (`localhost` or `127.0.0.1`), not an improvised port. State exactly what browser, registry, vendor sync, landing, or hosted proof did not run.

## Follow-up And Reporting

If docs reveal behavior that has no canonical source or executable evidence, classify it. Improve an existing projection for `ja-suportado-*`; record a platform issue only for `lacuna-real-de-contrato`, naming owner, consumers, public artifacts, and proof. Do not create a new component/package solely because documentation needs a category: Filters and Timeline are existing capabilities, not pretexts for parallel packages.

Report canonical owner/evidence, source documents/manifests, derived artifacts updated or reviewed, commands run, generated artifacts not hand-edited, publication status, and remaining drift or unvalidated visual/host risk.

## Companion Skills

- Use `praxis-landing-public-docs-contracts` and `praxis-landing-registries-sitemap-playgrounds` for public landing projection.
- Use `praxis-angular-validation-gates`, `praxis-angular-public-api-governance`, and `praxis-angular-i18n-governance` for underlying contract gates.
- Use `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion` for AI-derived docs and recipes.
- Use `praxis-authoring-editors`, `praxis-ui-product-design`, and the functional component skill for runtime/editor/visual proof.
- Use metadata/config/quickstart skills when the documentation claim derives from those canonical owners.
