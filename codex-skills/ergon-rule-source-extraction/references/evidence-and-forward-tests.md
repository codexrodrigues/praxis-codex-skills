# Evidence Contract and Forward Tests

Load this reference for Phase 10 source extraction or review.

## Canonical Migration Artifacts

Resolve paths from the active Ergon migration repository rather than copying these contracts into the skill:

- `docs/migracao/rule-migration/factory-contracts/rule-source-manifest-v1.schema.json`
- `docs/migracao/rule-migration/factory-contracts/goldens/*.rule-source-manifest.json`
- `docs/migracao/rule-migration/rule-migration-factory-rfc.md` (`RF-01`)
- `docs/migracao/rule-migration/templates/rule-inventory.md`
- `docs/migracao/rule-migration/templates/rule-traceability-matrix.md`
- `docs/migracao/rule-migration/templates/phase-10-execution-gate.md`
- `docs/migracao/rule-migration/part2-foundation-readiness-study.md`

Repository-local schemas, templates and goldens are canonical. If they disagree with this skill, stop, classify the drift and correct the canonical owner instead of inventing compatibility behavior.

## Evidence Strength

Prefer evidence in this order, without treating a lower item as proof of a higher one:

1. observed execution on the approved Parte 1 route with correlated input/output and source identity;
2. exact versioned source plus approved table-rule/runtime audit evidence;
3. exact versioned source declaration or static invocation reference;
4. historical output, XML/configuration reference or database registration;
5. name, keyword, label, regex or table association.

Items 4 and 5 can identify review candidates. They do not prove invocation, order, business ownership or parity.

## Status Decisions

| Evidence state | Manifest decision | Phase 10 consequence |
| --- | --- | --- |
| Canonical structural process passed; declared source scope is complete; schema/ranges/hashes reconcile | `SOURCE_MANIFEST_STRUCTURALLY_CONFIRMED` | Eligible for gate review; not automatically closed |
| Manually curated, RF-01 unavailable, ambiguous range, incomplete source, unresolved owner or review item | `SOURCE_MANIFEST_REVIEW_REQUIRED` | Useful evidence, but unresolved item remains explicit |
| Missing approved Parte 1 baseline or screen/operation identity | No advancing manifest | Return/block at intake |
| Only keyword, object existence, XML label or table-name association | Candidate evidence only | Unknown/defer; no classification upgrade |

## Forward Test A — Evidence-backed extraction

Input:

- an approved Parte 1 handoff for one operation;
- versioned package specification and body with exact hashes;
- the canonical `pck-regras-freq.rule-source-manifest.json` golden or an equivalent governed source set;
- table-rule audit evidence with unresolved ownership or invocation gaps;
- RF-01 is not yet implemented.

Expected behavior:

- preserve specification and body separately;
- inventory routines, ranges, calls, reads, mutations and unparsed blocks;
- cite the Parte 1 operation and audit evidence;
- classify unsupported business ownership as `unknown` and disposition as `defer`;
- produce `SOURCE_MANIFEST_REVIEW_REQUIRED` and record RF-01 as missing;
- update Phase 10 artifacts without declaring Phase 10 closed or selecting a Java target.

Failure signal: reporting `SOURCE_MANIFEST_STRUCTURALLY_CONFIRMED`, assigning business intent from routine names, or advancing to shadow/preflight.

## Forward Test B — Adversarial snippet

Input:

- a PL/SQL snippet containing suggestive validation names and a table name;
- no complete source, hash, approved Parte 1 handoff, operation identity or runtime evidence.

Expected behavior:

- stop with `Blocked - Missing Part 1 Evidence` plus missing-source provenance;
- do not manufacture a source manifest, rule classification or candidate Java decision;
- route the missing baseline to `$ergon-rule-migration-orchestration`.

Failure signal: using regex/keywords to call the snippet a product rule, inferring screen ownership, or writing implementation guidance.

## Forward Test C — Adjacent phase request

Input: a structurally complete Phase 10 manifest and a request to determine nested execution order, HADES activation or the Java target contract.

Expected behavior: preserve the manifest, then route execution-order work to Phase 11, HADES activation/order to Phase 12, and target/contract design to the later governed phase through `$ergon-rule-migration-orchestration`.

Failure signal: expanding this skill into dependency-graph closure, HADES activation claims or implementation.
