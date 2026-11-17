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
6. Make validation guidance select evidence by changed behavior, dependency and
   direct consumer, with explicit delivery/completion criteria. Distinguish focal
   iteration from a required consolidated broad gate. A rerun needs relevant
   evidence invalidation, a demonstrated coverage gap or a gate requirement;
   a test-only change can still affect shared fixtures/harnesses. Keep required
   security, concurrency, SQL/HTTP/E2E, resource-completeness and release gates.
   Reject unconditional clean/build-all/test-all loops and arbitrary test-count
   ceilings. Require command, duration, result and candidate identity; a time
   limit with required work pending is a partial checkpoint, not completion.

## Publish Canonically

The versioned source is `<canonical-repo>/codex-skills/`, in the dedicated
`praxis-codex-skills` Git checkout (the `praxis-codex-skills` workspace checkout in this
environment). Resolve and verify that repository explicitly; a host workspace's
`codex-skills/` and `$CODEX_HOME/skills` are projections. Use the canonical
repository's scripts with explicit working directory or `-RepoRoot`/`--repo-root`;
never infer the owner from the caller's current directory or use workspace helpers
as the family authority. Never edit an installed copy as the authoritative fix.

1. Place the new skill in exactly one family manifest. Keep only real explicit
   dependencies; do not use the manifest as a broad related-skills catalog.
2. Update `skillMdSha256` and `treeSha256` with the canonical audit flow.
3. Run the skill-creator validator for changed skills when available, then run
   structure validation for those skills and both family audits as required by
   repository governance. Update generated issue drafts when the generator
   requires it. Guidance-only edits do not require Java/Angular/runtime suites;
   executable examples or tooling changes require their affected checks. After
   success, do not repeat unchanged gates merely to prepare the final report.
4. Sync only the affected skills after the source and manifest audit are clean.
   Derive a selected manifest from canonical entries and pass its path to the
   canonical sync script with explicit repository and destination roots. Do not
   force an entire family to overwrite unrelated local changes. Separate local
   validated source, remote integration/publication and installed candidate state.
   Re-audit the installed target. Investigate an existing destination drift
   instead of overwriting it casually.
   For a selective installation, traverse the selected entries' manifest
   dependencies transitively and inspect every required installed tree against
   the canonical manifest. Reconcile missing/outdated dependencies within the
   authorized scope, preserving unexplained local differences. Report entrypoint
   parity and dependency-closure parity separately; a clean selected entrypoint
   does not prove its companion guidance is current. Remaining family drift
   outside that closure is a separate inventory result.
5. Close with the classification, owner, evidence inspected, manifest change,
   validation run, installation result, and any platform follow-up still open.

Do not claim a local installation is current merely because its directory exists.
The canonical tree hash and an audit are the proof.

## Reviewing A Multi-Day Closure

Hash equality proves source/installation parity, not semantic coverage or runtime correctness.
For a retrospective, record the requested date range, repository/worktree heads, relevant committed
changes and uncommitted/untracked implementation evidence. Do not silently reduce several days to
the latest diff, or treat another task's later commit as part of an earlier validation.

Map each material behavior to its canonical source, public documentation, owner skill and focused
evidence. Separate guidance already adequate, guidance corrected, platform defects still open and
claims lacking proof. Retain links to tests or reproducible commands, not only ephemeral log paths
or historical passing counts. Distinguish documentation coverage, installation parity, fresh test
execution and remote integration in the closure. A documentation-only change may require no
generated artifacts itself while the underlying implementation still has publication or consumer
validation pending. Never turn that narrower conclusion into a full product certification.
