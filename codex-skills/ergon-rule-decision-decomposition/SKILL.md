---
name: ergon-rule-decision-decomposition
description: Build and review evidence-bound RF-03 decision-pack drafts for Ergon rule migration. Use after RF-01 source extraction and an RF-02 preliminary profile when Codex must map every structural occurrence exactly once into explicit atomic decision proposals, preserve source provenance, outcomes, facts, order, dependencies and unknowns, run the canonical RF-03 generator and tests, or prepare a governed review queue without inventing business semantics, recording human approval, selecting a runtime target, or generating code.
---

# Ergon Rule Decision Decomposition

Produce the governed RF-03 boundary between structural evidence and later
semantic homologation. Treat every generated decision as a proposal, never as
confirmed business truth. Let `$ergon-rule-migration-orchestration` decide phase
advancement and cross-artifact status.

## Boundary

Use the canonical factory contracts and commands from the active migration
repository. Do not reimplement RF-03 inside this skill.

Do not:

- infer an atomic decision, grouping, description, fact meaning, owner, order,
  outcome consequence or target from names, labels, camelCase, proximity,
  repeated error codes or plausible policy;
- silently repair RF-01/RF-02 evidence, source ranges, hashes or the governed
  semantic baseline;
- turn a `candidateTarget` copied from a reviewed baseline into a target
  decision or implementation authorization;
- mark a draft review `DECIDED`, manufacture review evidence or treat technical
  authorship as business homologation;
- generate JSON Logic, Java, Config materialization, snapshots, shadow code or
  production changes;
- close Phase 11 or later gates, disable legacy behavior, or change runtime
  authority;
- expose package, Oracle, HADES or session details as public API metadata.

The technical factory may continue decomposition, parity work, offline
simulation and non-executable FND-12 planning while business owner and
homologation remain deferred. Preserve those gaps as `PENDING`, `UNKNOWN`,
`REVIEW_REQUIRED` or `BUSINESS_REVIEW_PENDING`; never convert deferral into
approval.

## Required Inputs

Identify all of the following before generating a pack:

1. exact screen/operation and current migration phase;
2. approved Parte 1 route and Phase 9/10 evidence for that operation;
3. RF-01 source manifest and RF-02 decision-profile input with verified hashes;
4. generated RF-02 preliminary profile;
5. governed RF-03 input plan and semantic baseline, both hash-bound;
6. canonical input/output schemas and `new-rule-decision-decisions.ps1` from
   the active migration repository;
7. current readiness and any blockers carried by RF-01/RF-02.

If identity, source provenance, RF-02 coverage, input hashes or the semantic
baseline is missing, stop RF-03 generation. Preserve the precise blocker and
return it to the owning earlier stage. A source snippet, observed error code or
technical description is not a substitute.

Read `references/contract-and-forward-tests.md` before producing or reviewing
a decision pack.

## Workflow

### 1. Freeze scope and lineage

Resolve every path relative to the active migration workspace. Verify the
declared SHA-256 values before reopening source manifest, RF-02 input or review
baseline. Reject path traversal, absolute paths where the schema forbids them,
source drift and scope disagreement.

Keep source manifest, RF-02 structural occurrences and RF-03 semantic proposals
as distinct layers. Do not copy a proposal back into structural evidence.

### 2. Reconcile occurrences without heuristics

Require every RF-02 structural occurrence to appear in exactly one RF-03
proposal:

- use `KEEP_SEPARATE` for one occurrence;
- use `MERGE_OCCURRENCES` only when the governed baseline explicitly lists two
  or more contained occurrences;
- reject uncovered, duplicate or foreign structural keys;
- preserve explicit source containment when multiple occurrences form one
  proposal.

Repeated outcomes, adjacent lines or similar conditions may identify a review
question. They never authorize grouping.

### 3. Generate through the canonical factory

Run the repository-local wrapper with the exact governed input:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools\migration-factory\new-rule-decision-decisions.ps1 `
  -InputPath <rf03-input.json> `
  -OutputPath <decision-pack.draft.json> `
  -EvidenceRoot <migration-root>
```

Require output `kind=RULE_DECISION_DECISIONS`,
`status=DRAFT_DECISION_PACK_REVIEW_REQUIRED` and
`publicPraxisContract=false`. Do not hand-edit generated output to make a gate
pass; correct the canonical input or evidence owner.

### 4. Validate the draft invariants

Confirm all of the following:

- each structural occurrence is covered exactly once;
- every evidence reference exists in the closed catalog and is authorized for
  the proposal that cites it;
- every review path belongs to the four-value closed catalog;
- every proposal is `PENDING`, has no recorded decision evidence and exposes
  only the three allowed future review actions;
- all facts, reads, mutations, side effects, dependencies and ordering states
  remain exactly as evidenced, including `UNKNOWN`;
- `allowedOutputs` is exactly `HUMAN_REVIEW_ONLY`;
- target planning, shadow, runtime snapshot and code generation remain false in
  the RF-03 ownership gate;
- the review queue keeps every unresolved semantic, ownership, order,
  provenance and dependency question blocking at its proper stage.

Schema validity proves shape only. It does not confirm business meaning,
execution order, target suitability or parity.

### 5. Separate technical progress from homologation

For the current technical migration cycle, keep reviews pending and record the
missing evidence needed by future domain homologation. Do not require a named
business owner merely to preserve evidence or generate the draft.

Only record `DECISION_PACK_HUMAN_REVIEW_RECORDED` in a later homologation flow
when an authorized reviewer provides an explicit action and evidence for every
proposal. Partial review, an agent-generated rationale or a status flip without
evidence must fail closed.

### 6. Hand off without expanding scope

Return the decision pack, coverage summary, grouping map, evidence catalog,
review queue and blockers to `$ergon-rule-migration-orchestration`.

RF-04 may materialize a reviewed profile only through its own contract. The
technical semantic gate may independently allow a non-executable draft with
`BUSINESS_REVIEW_PENDING`; this skill must not declare that gate passed.
Requests for target classification, JSON Logic, Java, parity/shadow or trigger
containment belong to later specialized skills.

## Validation

Use the smallest reliable set:

1. validate the RF-03 input and pack against their canonical schemas;
2. run `test-rule-decision-decisions-generation.ps1` against the active
   migration repository;
3. when downstream profile behavior is affected, also run
   `test-rule-decision-profile-materialization.ps1`;
4. execute the success, adversarial and boundary forward tests in
   `references/contract-and-forward-tests.md`;
5. audit this skill and the `ergon-migration` manifest after any guidance
   change.

Report the exact checks executed and any deferred review. Never summarize a
green RF-03 test as business approval or runtime readiness.
