---
name: ergon-forms-target-handoff
description: Validate an admitted Oracle Forms F7 capability and emit an origin-neutral intake for its real Ergon/Praxis target owner. Use only after F6 semantics and F7 admission are closed; do not use for Forms discovery, Cronos/Archon discovery, public API design, Java/Angular implementation or rule migration.
---

# Ergon Forms Target Handoff

Use this skill only at the convergence boundary defined by
`docs/architecture/ADR-0001-separacao-das-fontes-legadas.md`. The Forms
repository owns the source dossier; the target application owns later public
contracts and implementation.

## Entry gate

Require all of the following before emitting a handoff:

1. F6 classifies a functional capability without source UI/object names.
2. F7 admits that same `functionalityId`, resolves a real canonical owner and
   consumer, and keeps implementation unauthorized.
3. Every target incompatibility has a residual code and a return condition.
4. The evidence files referenced by F6/F7 exist and their current hashes can be
   calculated.

Fail closed if any condition is missing. Return to F4/F5/F6/F7 rather than
inventing target semantics.

## Workflow

1. Read the F6 semantic candidate and F7 admission.
2. Classify target reuse as `REUSE`, `EXTEND`, `CREATE`, `BLOCK` or `DEFER`.
3. Run `scripts/Export-FormsTargetHandoff.ps1` with the admitted inputs.
4. Run `scripts/Test-FormsTargetHandoff.ps1`; a generated file that differs
   from the versioned artifact is stale and cannot be consumed.
5. Route the accepted intake to the canonical target owner for contract
   discovery. Apply target API/UI skills only there and only after their entry
   gates pass.

## Handoff boundary

The intake may contain functional concepts, owner, consumer, reuse decisions,
invariants, residual codes, authority limits and opaque dossier hashes. It must
not contain or require:

- FMB/FMX, block, item, trigger, HWND or desktop-control identity;
- `.tp`, XML, Cronos, Archon or browser-discovery artifacts;
- `sourceOrigin`, V1/V2, aliases, origin modes or parallel target resources;
- SQL, schema, package, `ROWID` or private session/credential values;
- authorization to change public contracts, Java, Angular, rules, DML,
  publication, shadow, cutover or legacy authority.

The screen/functionality identifier may remain as opaque traceability. Source
paths stay in the origin dossier; the handoff carries only role, identifier and
SHA-256.

## Completion

Completion requires a schema-valid, deterministic handoff, a passing boundary
checker and a gate that names the next target-owned contract step. Do not call
the target API implemented or verified from the handoff alone.
