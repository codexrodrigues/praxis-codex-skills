---
name: praxis-angular-agents-governance
description: Use when Codex must audit or act on Praxis Angular local AGENTS.md governance: inventory projects/*/AGENTS.md coverage, handle absent subarea instructions, classify governance gaps, decide whether the fix belongs in praxis-ui-angular versus codex-skills, reconcile skill guidance with local platform source, and avoid relying on memory when component-local AGENTS files are missing.
---

# Praxis Angular AGENTS Governance

Use this skill for governance around `praxis-ui-angular` local `AGENTS.md` files and drift between Codex skills and the Angular platform. A local AGENTS file is durable platform guidance; a skill should encode how to use that guidance, not replace it as the source of truth for a component subarea.

## Current Audited Inventory

In the audited checkout, `praxis-ui-angular/projects` contains 23 top-level directories.

Local `AGENTS.md` exists for:

- `praxis-ai`
- `praxis-charts`
- `praxis-core`
- `praxis-cron-builder`
- `praxis-crud`
- `praxis-dialog`
- `praxis-dynamic-fields`
- `praxis-dynamic-form`
- `praxis-editorial-forms`
- `praxis-expansion`
- `praxis-files-upload`
- `praxis-list`
- `praxis-manual-form`
- `praxis-metadata-editor`
- `praxis-page-builder`
- `praxis-rich-content`
- `praxis-settings-panel`
- `praxis-stepper`
- `praxis-table`
- `praxis-table-rule-builder`
- `praxis-tabs`
- `praxis-visual-builder`

Local `AGENTS.md` is absent for:

- `projects/tools`: `docs/guidance`; tooling guidance exists under `tools/ai-registry/AGENTS.md`, not at `projects/tools/AGENTS.md`

Re-audit this inventory before using it as evidence. If the source changed, update this skill and the affected component skills in the same cycle.

## Source Audit

Before changing guidance or planning implementation:

- inspect `praxis-ui-angular/AGENTS.md`;
- list `projects/*/AGENTS.md` coverage;
- read the local AGENTS for each touched lib when it exists;
- when absent, inspect the owning lib `README.md`, `src/public-api.ts`, docs manifests, AI manifests, focused specs, and package scripts;
- inspect `tools/ai-registry/AGENTS.md` for AI registry work;
- search Codex skills for stale statements about missing or existing AGENTS files.

## Classification

Classify each gap:

- `docs/guidance`: the component has enough local governance, but a skill routes poorly or omits the right source/validation/doc artifact.
- `governança-local-ausente`: a component lib lacks `projects/<lib>/AGENTS.md`; create a follow-up in `praxis-ui-angular`, not in this skills repo.
- `contrato-canônico-ambíguo`: the absence or drift hides uncertainty about owner, public API, validation gate, or derived artifact; pause local patches and identify the canonical platform owner.

Also classify implementation need with the standard Praxis categories:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Missing AGENTS guidance alone is not a runtime contract gap.

## Decision Rules

- Do not invent component-local AGENTS content inside `praxis-codex-skills`.
- If the gap is local governance, open or record a follow-up against `praxis-ui-angular` with the missing lib, owner boundary, validation gates, public artifacts, and observed evidence.
- Update skills when the evidence is already verifiable and the correction is small, objective, and directly useful for future Codex work.
- When a skill and local AGENTS disagree, prefer the local platform source and update the skill.
- When local AGENTS is absent, avoid memory-based commands; derive validation from root AGENTS, `package.json`, README/docs, focused specs, and public API ownership.
- Treat docs, examples, public API, AI registry, i18n, and playgrounds as derived artifacts that must be reviewed when the missing AGENTS would normally name them.
- For skills-only updates, prefer changing the versioned source under `codex-skills/`, updating the manifest hashes, and running the smallest available audit/sync path. If PowerShell is unavailable, record that `scripts/sync-praxis-skills.ps1` could not run instead of silently skipping local installation sync.

## Known Follow-Ups

- `praxis-charts` now has local AGENTS guidance for ECharts adapter boundaries, analytics/stats contracts, config editors, AI manifest/registry gates, public API, docs/playgrounds, and focused build/spec commands. Re-audit if source guidance changes.
- `praxis-rich-content` now has local AGENTS guidance for core-owned `RichContentDocument`, renderer/editor/preset boundaries, safe URL/style policy, JsonLogic fail-safe behavior, AI manifest/registry gates, public API, docs/playgrounds, and focused build/spec commands. Re-audit if source guidance changes.
- `projects/tools` should not be treated as a missing component-lib AGENTS gap while `tools/ai-registry/AGENTS.md` governs the actual AI registry tooling.

## Validation

For skills-only governance updates:

- re-run the project AGENTS inventory script;
- search touched skills for stale AGENTS claims;
- validate manifest count, hashes, frontmatter, `$skill` prompts, dependencies, and cycles;
- run `git diff --check`;
- run `skill-creator` validation when the environment has PyYAML;
- run skill sync when PowerShell is available, or state why sync was skipped.
- if `quick_validate.py` is absent, state that absence and use the repo's manifest/hash audit as the local substitute.

For monorepo follow-ups, validate in `praxis-ui-angular` according to the affected local AGENTS, root AGENTS, and the smallest reliable package/docs/registry gates.
