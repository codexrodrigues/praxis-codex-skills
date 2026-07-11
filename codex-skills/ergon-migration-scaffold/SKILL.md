---
name: ergon-migration-scaffold
description: Use when turning a closed Ergon/Archon screen-discovery package into a repeatable Praxis API implementation packet: operation inventory, resource key, read/options/write route decisions, metadata contract outline, phase gates, code-ready tasks, and a deterministic migration scaffold.
---

# Ergon Migration Scaffold

Use this skill after a screen has enough discovery evidence to start Parte 1.
It turns that evidence into a small, deterministic implementation packet so the
agent can author the Praxis API in minutes rather than reconstructing the same
decisions across discovery, Java, and handoff phases.

## Entry Gate

Require the closed screen package, especially `closure-checklist.md`, lineage,
operation inventory or XML evidence, `api-contract.md`, platform-reuse
inventory, and any existing read/write handoff. Do not use the scaffold to
invent fields, IDs, routes, permissions, option semantics, Oracle behavior, or
write safety.

Classify missing information as `Blocked` or `Deferred`; do not fill it with a
generic CRUD assumption. For a closed read-only slice, the scaffold may proceed
without Oracle access. For writes, unknown rule, side effect, session context,
or cleanup means `WRITE_DB_BACKED_REQUIRED` or `WRITE_BLOCKED`.

## Generate The Packet

Run:

```bash
python3 codex-skills/ergon-migration-scaffold/scripts/create_api_scaffold.py \
  --screen ERGadm00033 \
  --resource-key tipo-frequencia \
  --base-path /api/administracao-pessoal/tipos-frequencia \
  --output docs/migracao/ERGadm00033/api-scaffold \
  --operations list,detail,options,create,update,delete
```

`resourceKey` is semantic identity; `base-path` is the host's HTTP route. The
script writes a bounded implementation packet and refuses to overwrite an
existing packet without `--force`. Read
[scaffold-contract.md](references/scaffold-contract.md) when choosing
operations or interpreting generated states.

## Measure The First Slice

The generated `factory-timing.json` starts the prospective clock. Record an
event only after its evidence exists:

```bash
python3 codex-skills/ergon-migration-scaffold/scripts/record_factory_milestone.py \
  --packet docs/migracao/ERGadm00033/api-scaffold \
  --milestone first-endpoint-executed \
  --outcome passed \
  --evidence docs/migracao/ERGadm00033/api-results/filter-smoke.json
```

Use `first-endpoint-executed`, `schema-validated`, `focused-tests-passed`, and
`legacy-parity-assessed` to measure actual elapsed minutes from scaffold
creation. A blocked or deferred event is valid only with its evidence path. Do
not backfill a historical timestamp from memory; mark retrospective packets as
unmeasured instead.

## Use The Packet Correctly

1. Fill the generated evidence placeholders from the discovery artifacts; retain
   the source path and confidence for each decision.
2. Run `praxis-dto-annotations` and `praxis-java-resource-authoring` to design
   DTOs, FilterDTOs, options, schemas, actions, surfaces, and capabilities.
3. Use `ergon-archon-read-api-migration` for list/detail/options. Reuse the
   platform resource baseline; no Ergon-local metadata or capability model.
4. Route each write operation to `ergon-table-rule-audit` and
   `ergon-archon-write-api-migration`. Only the exact route marked
   `WRITE_TABLE_DIRECT_SAFE` may use direct persistence; otherwise preserve the
   validated legacy-backed route.
5. Implement in the canonical module after the duplicate-root guard, then prove
   endpoint execution and legacy/API/database parity. A generated packet is a
   plan, never proof or a phase closeout.

The scaffold may prefill standard operation states and Praxis endpoint shapes,
but a resource contract is not complete until its real DTO and host conventions
are inspected. Keep `ROWID`, Oracle session/HADES state, company/user context,
and SQL private to the legacy bridge.

## Mutation And Evidence

When the migration's development database policy preauthorizes mutations,
perform needed setup, mutation, verification, and cleanup without requesting
another confirmation. Record fixture identity, before/after evidence, and final
cleanup. Never convert that authorization into permission for production or
unknown environments.

## Handoff

Close the scaffold phase with the selected resource key, operation states,
canonical Praxis surfaces, write-route state, implementation owner, evidence
gaps, and exact next skill. The next agent should be able to start the narrow
API slice directly from the packet.

## Companion Skills

- `ergon-migration-orchestration`: phase ownership and gates.
- `ergon-archon-screen-discovery`: source evidence and screen closure.
- `ergon-archon-read-api-migration`: read/options implementation and parity.
- `ergon-table-rule-audit`: table rule and side-effect evidence.
- `ergon-archon-write-api-migration`: safe write routes and parity.
- `praxis-java-resource-authoring`: canonical resource implementation.
- `praxis-dto-annotations`: metadata contract authoring.
