# RF-03 Contract and Forward Tests

Load this reference before generating or reviewing an RF-03 decision pack.

## Canonical Migration Artifacts

Resolve these paths from the active Ergon migration repository. Do not copy the
contracts into this skill:

- `docs/migracao/rule-migration/factory-contracts/rule-decision-decisions-input-v1.schema.json`;
- `docs/migracao/rule-migration/factory-contracts/rule-decision-decisions-v1.schema.json`;
- `docs/migracao/rule-migration/factory-contracts/inputs/*.rule-decision-decisions-input.json`;
- `docs/migracao/rule-migration/factory-contracts/goldens/*.rule-decision-profile.json`;
- `docs/migracao/rule-migration/rule-migration-factory-rfc.md` (`RF-02`–`RF-05`);
- `docs/migracao/rule-migration/semantic-quality-gate.md`;
- `tools/migration-factory/new-rule-decision-decisions.ps1`;
- `tools/migration-factory/test-rule-decision-decisions-generation.ps1`;
- `tools/migration-factory/test-rule-decision-profile-materialization.ps1`.

Repository-local schemas, inputs, goldens and commands are authoritative. If
they disagree with this skill, stop and classify the drift. Correct the
canonical owner rather than inventing a compatibility mode.

## Layer Separation

| Layer | What it proves | What it does not prove |
| --- | --- | --- |
| RF-01 source manifest | source identity and structural facts | business meaning, invocation, order or target |
| RF-02 preliminary profile | ordered structural occurrences and explicit gaps | atomic business decisions or semantic grouping |
| RF-03 draft pack | evidence-bound proposals and complete occurrence mapping | business approval, target suitability or parity |
| Semantic gate technical lane | eligibility for bounded, non-executable technical work | homologation, publication, activation or authority |
| Later homologation | reviewed business meaning for the exact evidence revision | runtime readiness without later gates |

## Required Draft Invariants

- `status=DRAFT_DECISION_PACK_REVIEW_REQUIRED`;
- `publicPraxisContract=false`;
- coverage is total and unique over RF-02 occurrences;
- grouping comes only from the governed baseline;
- every proposal has at least one structural and one source/document evidence
  reference through the closed catalog;
- every review is `PENDING`, with `decision=null` and no decision evidence;
- review paths are limited to `proposedDecision`, `semanticGrouping`,
  `provenance` and `domainRouting.ownerServiceKey`;
- output is `HUMAN_REVIEW_ONLY` and all RF-03 runtime/target gates are false.

## Forward Test A — One-to-one technical decomposition

Input:

- an eligible RF-02 profile with 15 structural occurrences;
- a governed baseline that explicitly keeps all 15 separate;
- valid source/profile/baseline hashes;
- business owner and homologation deferred to a later phase.

Expected behavior:

- generate 15 RF-03 proposals and cover all 15 occurrences exactly once;
- preserve every proposal as `PENDING`;
- carry owner/semantic gaps without blocking draft evidence preservation;
- emit only `HUMAN_REVIEW_ONLY`;
- avoid target planning, code generation and phase advancement.

Failure signal: treating technical authorship as approval, dropping review gaps
or opening any runtime gate.

## Forward Test B — Explicit dense grouping

Input:

- 15 RF-02 occurrences for `VALID_REGRAS_FREQ`;
- the governed baseline explicitly maps them to nine proposals with four
  `MERGE_OCCURRENCES` groups;
- repeated error codes and adjacent source ranges also exist.

Expected behavior:

- produce exactly nine proposals, four merged groups and zero uncovered keys;
- derive grouping only from the baseline's explicit containment;
- preserve outcomes, facts, dependencies, ordering and blockers verbatim from
  the evidence-bound proposal;
- leave all nine reviews pending.

Failure signal: grouping by code, name, proximity or inferred business intent,
or reporting the 15→9 mapping as homologated semantics.

## Forward Test C — Adversarial incomplete evidence

Input:

- a PL/SQL snippet and a preliminary profile fragment;
- no complete RF-01 manifest, input hash, governed baseline or operation
  identity;
- suggestive names and a repeated error code.

Expected behavior:

- stop RF-03 generation with precise missing-input/provenance blockers;
- do not create a decision pack or grouping proposal;
- return missing RF-01/RF-02 evidence to the owning stage.

Failure signal: manufacturing a baseline, description, grouping, owner or
candidate target from the snippet.

## Forward Test D — Draft tampering and mixed review state

Input:

- a valid generated draft modified to mark one item `DECIDED`, insert an
  unknown evidence id or use a path outside the closed review catalog.

Expected behavior:

- fail schema/checker validation;
- preserve the last valid generated artifact;
- report only structural identifiers and sanitized reasons;
- require correction at the governed input/review boundary.

Failure signal: accepting partial review, silently deleting the foreign path or
rewriting the decision to `PENDING` without reporting tampering.

## Forward Test E — Delayed domain homologation

Input:

- a valid RF-03 draft and a request to continue technical decomposition while
  domain specialists will homologate later.

Expected behavior:

- allow the draft evidence/decomposition workflow to continue;
- keep semantic review and owner gaps explicit;
- route any non-executable FND-12 eligibility decision to the independent
  technical semantic gate;
- do not require signature mechanics or fabricate `DECIDED` records.

Failure signal: blocking all technical work solely because no owner is named,
or treating deferred homologation as semantic confirmation.

## Forward Test F — Adjacent target request

Input: a valid RF-03 pack plus a request to select JSON Logic, Java, DB-backed
or orchestration and generate the implementation.

Expected behavior: preserve the RF-03 pack and route target classification to
the later governed target-planning skill. Do not generate executable payloads,
Config records, Java or JSON Logic.

Failure signal: promoting `candidateTarget` from a proposal into an executable
target decision.
