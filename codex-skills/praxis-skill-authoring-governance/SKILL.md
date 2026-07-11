---
name: praxis-skill-authoring-governance
description: Use when creating, splitting, reviewing, retiring, or publishing a canonical Praxis Codex skill; when deciding whether recurring friction is a skill gap or a platform gap; or when reconciling skill scope, canonical owner, manifest dependencies, validation, and local-installation drift.
---

# Praxis Skill Authoring Governance

Treat a Praxis skill as executable platform guidance, not as generic documentation.
It must make a future implementation faster and more canonical by directing Codex to
the real owner, contracts, evidence, decisions, and focused proof.

## Start From The Real Friction

1. Capture the concrete repeated task, the decision that consumes time, and the
   observable failure or rework it causes.
2. Inspect the affected platform source, local `AGENTS.md`, public contracts,
   focused tests, operational examples, and direct consumers. Do not author from
   a remembered API or only a ticket description.
3. Classify the finding:
   - `migration-skill-gap`: the platform already supports the outcome but the
     repeatable native route is absent or unclear;
   - `ja-suportado-so-ux` or `ja-suportado-mal-nomeado-ou-mal-materializado`:
     improve adoption or materialization, not the contract;
   - `suportado-parcialmente`: identify the owning follow-up and the temporary
     limit precisely;
   - `lacuna-real-de-contrato`: stop skill authoring as the primary remedy and
     open an owner-specific platform RFC or implementation follow-up.
4. State the canonical owner. `praxis-metadata-starter` owns backend metadata,
   schemas, resources, surfaces, actions, capabilities, and `x-ui`.
   `praxis-config-starter` owns governed config and authoring persistence.
   `praxis-ui-angular` owns public runtime libraries. Quickstarts prove contracts;
   they do not redefine them.

Do not turn a missing tool, contract, or semantic capability into prose that
teaches a consumer-local workaround. Do not route primary intent with keywords,
regexes, labels, or aliases.

## Choose The Smallest Useful Skill

Use one task-oriented skill when its workflow, evidence, owner, and validation
are coherent. Split only when a user can complete one task without loading the
other skill's detailed guidance. Keep `praxis-*` independent of Ergon/Archon;
put legacy discovery, Oracle behavior, migration gates, and Ergon evidence in
`ergon-*` skills.

Read [portfolio-and-review.md](references/portfolio-and-review.md) when sizing a
new skill, reviewing overlap, or planning a delivery wave.

Each skill must contain:

- a trigger-rich frontmatter description;
- the canonical owner and the source paths/contracts that must be inspected;
- an evidence-first workflow with explicit decision points;
- prohibited local shortcuts and any required companion skills;
- the smallest validation that proves the promised outcome and derived-artifact
  decision.

Keep `SKILL.md` procedural and concise. Put detailed matrices, examples, or
taxonomy in `references/`; add a script only for deterministic repeated work.

## Author And Review

1. Create the skill with the standard initializer, then replace all template
   text. Keep its directory name and frontmatter `name` identical.
2. Test the description against at least two realistic prompts: one that should
   trigger and one adjacent task that should not. Check that the workflow can
   lead to `already supported` as well as to an evidence-backed gap.
3. For Java/Praxis guidance, inspect the actual starter annotations, base
   controllers/services, schema or discovery projection, focused tests, and a
   real host/consumer before asserting a canonical path. For Angular handoff,
   prove that the backend contract can materialize in the relevant runtime,
   including options, surfaces, actions, capabilities, errors, and applicable
   stats/export.
4. Record expected side effects for commands and mutations. Development-database
   mutation authority may be pre-approved by the migration process, but the
   skill must still require scoped probes, evidence, and cleanup or rollback
   where the workflow creates test data.
5. Reject a skill that repeats broad architecture without changing a concrete
   future decision, hides uncertainty as fact, duplicates a neighboring skill,
   or substitutes instructions for a missing platform contract.

## Publish Canonically

The versioned source is this repository's `codex-skills/`; `$CODEX_HOME/skills`
is an installed projection. Never edit an installed copy as the authoritative
fix.

1. Place the new skill in exactly one family manifest. Keep only real explicit
   dependencies; do not use the manifest as a broad related-skills catalog.
2. Update `skillMdSha256` and `treeSha256` with the canonical audit flow.
3. Run the skill-creator validator when available, then run the repository
   structure validation and both family audits. Update generated issue drafts
   when the repository's generator requires it.
4. Sync the smallest family only after the source and manifest audit are clean.
   Re-audit the installed target. Investigate an existing destination drift
   instead of overwriting it casually.
5. Close with the classification, owner, evidence inspected, manifest change,
   validation run, installation result, and any platform follow-up still open.

Do not claim a local installation is current merely because its directory exists.
The canonical tree hash and an audit are the proof.
