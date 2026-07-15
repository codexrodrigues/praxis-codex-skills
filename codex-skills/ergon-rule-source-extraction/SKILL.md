---
name: ergon-rule-source-extraction
description: Extract a conservative, evidence-backed Phase 10 inventory of legacy Ergon rule sources. Use after an approved Parte 1 handoff when Codex must catalog package specs/bodies, procedures, functions and triggers; correlate XML/client or historical evidence; record hashes, source ranges, routines, calls, reads, mutations and unresolved blocks; produce RULE_SOURCE_MANIFEST, rule-inventory.md and rule-traceability-matrix.md inputs without interpreting business intent, selecting a Java target, or claiming HADES activation.
---

# Ergon Rule Source Extraction

Build the structural evidence package that lets Parte 2 answer which rule sources exist for one exact screen and operation. This skill owns Phase 10 extraction and inventory; `$ergon-rule-migration-orchestration` owns phase advancement and cross-artifact governance.

## Boundary

Treat source extraction as evidence preservation, not rule interpretation. Record what a source declares and does structurally, with exact provenance. Do not:

- translate PL/SQL, trigger, XML or client code mechanically to Java;
- infer business meaning from names, labels, keywords, regex matches or table names;
- choose a target rule contract, DSL, runtime service or canonical platform owner;
- claim dependency order, HADES activation, EP precedence or client behavior that the evidence does not prove;
- close Phase 11, 12 or later gates;
- expose Oracle, HADES, package or session details as public API metadata.

Use `$ergon-table-rule-audit` for detailed table-write, trigger, package and HADES evidence. Preserve its findings and confidence; do not silently upgrade them.

## Required Inputs

Before extracting, identify all of the following:

1. the exact screen/transaction and operation;
2. the approved Parte 1 handoff and parity route for that operation;
3. the Phase 9 intake and canonical decision inventory;
4. the legacy source roots and available source artifacts;
5. the canonical `rule-source-manifest-v1` schema, Phase 10 templates and any approved goldens;
6. relevant table-rule audit evidence when the operation reads or writes Oracle tables.

If the screen/operation identity, approved Parte 1 baseline or source provenance is missing, stop extraction advancement. Record `Blocked - Missing Part 1 Evidence` or the precise missing-source blocker and return to the orchestrator. A source snippet or table name alone is not an eligible Phase 10 intake.

Read `references/evidence-and-forward-tests.md` before producing or reviewing a manifest.

## Workflow

### 1. Freeze scope and provenance

Create one extraction scope per screen/operation. For every candidate source supported by the canonical schema, record the stable source key, kind, repository-relative or governed absolute path, encoding, line count, byte count, SHA-256 and acquisition evidence. Keep package specification and body as distinct sources. Include triggers, standalone routines, Parte 1 artifacts and approved historical outputs when they are relevant.

Correlate XML/client evidence through governed Parte 1 artifacts, invocation evidence or the review queue. The v1 schema has no first-class XML/client `sourceType`; do not mislabel a raw XML/client file as another type merely to pass validation. If first-class preservation is required, record a contract gap and return it to the canonical factory/schema owner.

Never normalize away source text before hashing. If encoding, file completeness or source version is uncertain, preserve the source as unresolved and add it to the review queue.

### 2. Produce the structural manifest

Use the canonical RF-01 exporter/parser when it exists and is approved for the repository. Validate its output against `rule-source-manifest-v1.schema.json`.

When RF-01 is absent, do not create an ad hoc regex parser inside this skill. A manually curated manifest may be used as a review artifact only when every fact cites exact source evidence. Set status to `SOURCE_MANIFEST_REVIEW_REQUIRED`, record the missing RF-01 capability, and never report structural confirmation.

For each routine or block, preserve as available:

- declared name, kind, visibility, owner source and exact line range;
- parameters and direction/type declarations supported by the schema;
- calls, reads, mutations and emitted outcomes;
- structural control-flow facts such as guarded branches and loops;
- invocation evidence and its source;
- unparsed or ambiguous blocks without summarizing them away.

Use `SOURCE_MANIFEST_STRUCTURALLY_CONFIRMED` only when the canonical structural process ran successfully, schema validation passed, source coverage is complete for the declared scope, and every unresolved block or review item allowed by the gate is explicitly accounted for.

### 3. Reconcile invocation evidence

Cross-reference Parte 1 evidence and `$ergon-table-rule-audit` findings. Distinguish:

- declaration or object existence;
- observed invocation on the approved baseline route;
- configured activation;
- inferred candidate relationship;
- unknown.

An Oracle object, HADES registration, XML reference or call name does not prove activation or execution order. Carry unknown activation/order into Phase 11 or 12 as a blocker or deferred item.

### 4. Materialize Phase 10 artifacts

Update `rule-inventory.md` and `rule-traceability-matrix.md` from the manifest and approved Parte 1 evidence. Each inventory row must contain:

- stable rule/source identifier;
- exact legacy origin and operation;
- cited Parte 1 artifact;
- structural source/routine range;
- classification as product, client, security, side effect, dependency blocker, edge validation or unknown;
- evidence strength and unresolved questions;
- initial disposition: keep, candidate, defer or reject.

Classification describes the evidence-backed role in the current operation; it is not a Java target decision. If evidence does not support a class or disposition, use `unknown` and `defer`. Never let a plausible name become a business classification.

### 5. Hand off without overclaiming

Return the manifest, inventory, traceability changes, review queue, unparsed blocks and missing-evidence list to `$ergon-rule-migration-orchestration`. The orchestrator decides whether Phase 10 can close and whether work proceeds to dependency graph or HADES analysis.

Phase 10 remains blocked when required sources are missing, scope identities disagree, origin/operation cannot be tied to Parte 1, facts depend on unsupported inference, or the required review queue has no owner. A review-required manifest can document useful progress without authorizing shadow, preflight or implementation.

## Validation

Use the smallest reliable validation set:

1. validate manifest JSON with the canonical schema;
2. run the migration repository's RF-01/golden contract test when available;
3. compare hashes, ranges and routine ownership against the original sources;
4. check that every inventory classification and disposition cites evidence;
5. execute the success and adversarial forward tests in `references/evidence-and-forward-tests.md`;
6. keep unresolved evidence visible in the manifest, matrix and phase gate.

Report exactly which checks ran. Schema validity proves shape only; it does not prove semantic completeness, activation, order or parity.
