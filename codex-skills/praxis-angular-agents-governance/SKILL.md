---
name: praxis-angular-agents-governance
description: Use when Codex must discover, apply, audit, or repair Praxis Angular governance across repository AGENTS.md files, codex-rules.md, component-local instructions, tools/ai-registry, skills, or a suspected instruction/owner/validation/derived-artifact drift.
---

# Praxis Angular AGENTS Governance

Use this skill to turn a concrete Angular path or planned change into the applicable Praxis governance. `AGENTS.md` files are versioned platform instructions. Skills help locate and apply them; they never replace their canonical guidance.

## When To Use

Use for a missing, stale, contradictory, or uncertain local rule; before changing a cross-lib surface; or when an implementation needs to determine its owner, allowed files, validation, publication artifacts, and follow-up repository.

Do not use this as a substitute for the functional skill of the affected component. Once the governing sources are resolved, load the functional skill and local guidance for the actual runtime, authoring, metadata, chart, table, form, AI, or tool change.

## Resolve The Governance Stack

Start from the exact file or area to change, not from a remembered inventory. Apply every file whose declared scope contains that path, from broad to narrow:

1. monorepo root `AGENTS.md`;
2. `praxis-ui-angular/AGENTS.md`;
3. `praxis-ui-angular/codex-rules.md` before any Angular task;
4. the nearest applicable `AGENTS.md` below the workspace, such as `projects/<lib>/AGENTS.md` or `tools/ai-registry/AGENTS.md`;
5. the component's `README.md`, `src/public-api.ts`, docs manifest, AI manifest, focused specs, and package scripts when the local instructions name them or are absent.

Confirm the workspace rule from `codex-rules.md` before editing Angular code: `Regras do codex-rules.md carregadas. Configurações do workspace NÃO serão modificadas.` Its build configuration, `tsconfig`, path mappings, package manifests, and dependency boundaries are protected unless the user explicitly authorizes a change.

Local instructions complement broader ones. A narrow file may supply owner-specific commands and artifacts; it cannot silently weaken a root platform rule. When instructions appear to conflict, preserve the stricter canonical rule, inspect the source contract, and record the ambiguity rather than choosing a convenient interpretation.

## Inventory, Do Not Assume

For the current checkout, enumerate only real source paths. Ignore generated or mirrored trees such as `.linux/**` unless the task explicitly targets them.

```sh
find praxis-ui-angular/projects -mindepth 1 -maxdepth 1 -type d -print | sort
find praxis-ui-angular/projects -mindepth 2 -maxdepth 2 -name AGENTS.md -print | sort
find praxis-ui-angular/tools -name AGENTS.md -print | sort
```

The audited baseline has local `AGENTS.md` coverage for all 22 public component libraries under `projects/`; `projects/tools` is a tooling container, not an uncovered public library. AI registry work is governed by `tools/ai-registry/AGENTS.md`. Re-run the inventory before claiming this remains true.

For every affected path, capture:

| Evidence | What it establishes |
| --- | --- |
| nearest `AGENTS.md` | owner boundary, paired files, focused gates, recurring risks |
| `codex-rules.md` | protected workspace configuration and edit constraints |
| `README.md` and `src/public-api.ts` | user-facing contract and package owner |
| docs/AI manifests, recipes, landing data | derived documentation, registry, and authoring obligations |
| specs, package scripts, root workspace guidance | smallest executable proof and environment constraints |

Do not infer a contract merely because a local file is absent. Inspect the established sources above and classify what is actually missing.

## Classify And Route The Gap

First classify the implementation using the platform categories: `local-pequena`, `transversal`, `arquitetural`, `contrato-publico`, or `docs-apenas`. For any proposed new surface, also classify adherence as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.

Then classify the governance result:

| Finding | Correct action |
| --- | --- |
| guidance exists but a skill omits, duplicates, or misroutes it | update the canonical skill in `codex-skills/`; do not copy local instructions into consumer code |
| a component library lacks local instructions and broader evidence cannot safely define owner/gates | create a `praxis-ui-angular` governance issue with the path, owner, paired artifacts, focused validation, and risk |
| local instructions are stale, mutually inconsistent, or contradict source behavior | fix the owning `AGENTS.md` in `praxis-ui-angular`; update affected skills in the same cycle when evidence is stable |
| ambiguity is actually about metadata, config, public API, runtime, or backend semantics | stop treating it as a documentation gap; map the canonical owner and solve it at platform level |
| generated registry/docs output differs from its source | repair the official generator flow, manifest, or source docs; never hand-edit generated output as a shortcut |

A missing `AGENTS.md` is a governance gap, not automatically a new runtime or metadata contract. Do not create inputs, exports, aliases, local services, words-based intent routing, or consumer-side parallel semantics to compensate for unclear instructions.

## Platform Decisions That Governance Must Preserve

- Praxis Angular is a runtime and cockpit for AI-authored semantic decisions; it does not become the primary source of business rules.
- Before proposing a contract, inventory existing metadata, schemas, `x-ui`, surfaces, actions, capabilities, option sources, registries, manifests, editor state, diagnostics, previews, and runtime adapters. Correct canonical materialization before adding parallel UI state.
- User intent is semantically resolved by AI/LLM with governed grounding. Keyword or regex matching can only assist after a canonical scope has been resolved; it cannot decide primary intent.
- Keep root `public-api.ts` intentional. Do not create a transitively exported facade for another public library; use `praxis-angular-public-api-governance` for cross-lib edges and direct-consumer proof.
- Framework-owned text follows `PraxisI18nService` and the owning locale catalogs; schema and host business copy remain external. Use `praxis-angular-i18n-governance` for catalog and hardcoded-chrome work.
- Runtime/config changes must be checked against their canonical visual authoring round-trip. For fields, include editorial discovery and tooling coverage, not just runtime rendering.
- AI registry, generated docs, manifests, recipes, and backend synchronization belong to `tools/ai-registry` and its official scripts, not ad hoc scripts or manually changed derived assets.
- In beta, prefer a clean canonical migration with updated consumers and artifacts over feature flags, aliases, or parallel v1/v2 contracts unless an operational exception is explicit.

## Required Impact Map

For `transversal`, `arquitetural`, or `contrato-publico` work, produce this before editing:

| Item | Record |
| --- | --- |
| canonical owner | library, starter, registry tool, or backend source that owns the semantics |
| affected consumers | direct libraries, host demos, editors, and backend/landing consumers |
| public/derived artifacts | `public-api`, README/docs manifest, AI manifest/registry, recipes, playground, landing, sitemap, corpus |
| validation | smallest focused build/spec/browser/registry/doc proof that covers the changed behavior |
| compatibility | breaking risk, clean beta migration, and any authorized operational exception |

For a local change, still name why no adjacent owner or derived artifact applies. This prevents a local patch from silently creating platform drift.

## Validation And Completion

Use the affected local `AGENTS.md` first, then select the narrowest command with `praxis-angular-validation-gates`. Typical coupled surfaces require these companions:

- public exports or cross-lib contracts: `praxis-angular-public-api-governance` plus altered-library and direct-consumer proof;
- internal framework copy: `praxis-angular-i18n-governance` plus `pt-BR` and `en-US` evidence;
- config, editors, Settings Panel, or field discovery: `praxis-authoring-editors` and the actual runtime-to-editor round trip;
- docs, examples, playgrounds, registries, or site routes: `praxis-angular-docs-playgrounds`;
- AI manifest, catalog, ingestion, generated AI docs, or backend sync: `praxis-ai-registry-ingestion` and `tools/ai-registry/AGENTS.md`.

For a skills-only change, update `codex-skills/`, its manifest hashes/dependencies, and generated issue draft; run `python3 scripts/preflight-python-fallbacks.py`, `python3 scripts/audit-praxis-skills.py --family praxis`, `git diff --check`, then `python3 scripts/sync-praxis-skills.py --family praxis --force` and re-audit. State exact validation and omissions.

Close with the resolved stack, classification, canonical owner, applied gates, derived-artifact decision, and any issue opened for a true governance or platform gap.
