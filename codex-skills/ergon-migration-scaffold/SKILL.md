---
name: ergon-migration-scaffold
description: Use when turning a closed Ergon/Archon screen-discovery package into a repeatable Praxis API-first implementation: operation inventory, manifest/profile/blueprint generation, read-only Java dry run, resource key, phase gates, evidence packet, and deterministic elapsed-time measurement.
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

## Prefer The API-First Factory

When `tools/migration-factory/export-api-first-manifest.ps1` exists and the
screen has its required Phase 1/2 factory inputs, it is the implementation path
for the smallest read slice. Run its checked chain in order:

```powershell
pwsh -File tools/migration-factory/export-api-first-manifest.ps1 -Screen <SCREEN>
pwsh -File tools/migration-factory/check-api-first-manifest.ps1 -ManifestPath docs/migracao/<SCREEN>/factory/api-first-manifest.json
pwsh -File tools/migration-factory/start-api-first-timing.ps1 -ManifestPath docs/migracao/<SCREEN>/factory/api-first-manifest.json
pwsh -File tools/migration-factory/new-api-first-read-profile.ps1 -ManifestPath docs/migracao/<SCREEN>/factory/api-first-manifest.json
pwsh -File tools/migration-factory/check-api-first-read-profile.ps1 -ProfilePath docs/migracao/<SCREEN>/factory/api-first-read-profile.prelim.json
pwsh -File tools/migration-factory/java-read-scaffold.ps1 -ProfilePath docs/migracao/<SCREEN>/factory/api-first-read-profile.prelim.json
```

The last command is a dry run by default. Fill every `REVIEW_REQUIRED` item
from confirmed screen/Oracle/host evidence, validate again, then permit output
files only in the canonical module. Read
[api-first-factory-integration.md](references/api-first-factory-integration.md)
before selecting this path.

## Measure The First Slice

When the API-first factory is available, its timing ledger is the canonical
prospective metric. Start it immediately after the checked manifest and before
the first Java edit:

```powershell
pwsh -File tools/migration-factory/record-api-first-timing-milestone.ps1 `
  -LedgerPath docs/migracao/<SCREEN>/factory/api-first-timing.json `
  -Milestone implementation-started `
  -Evidence docs/migracao/<SCREEN>/factory/evidence/implementation-started.md
```

Record the canonical milestones in order: `implementation-started`,
`first-endpoint-executed`, `schema-validated`, `focused-tests-passed`, and
`legacy-parity-assessed`. Each evidence path must already exist. The ledger is
bound to the source manifest hash; regenerate a changed manifest and restart an
unmeasured pilot rather than mixing two contracts in one duration. Audit it with
`check-api-first-timing.ps1`, adding `-RequireComplete` only at pilot closeout.

## Generic Packet Timing

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

The generic `create_api_scaffold.py` packet records entry evidence and elapsed
time only when the API-first factory is unavailable. It does not replace the
API-first manifest, profile, SQL blueprint, Java dry run, or factory timing
ledger when those official tools apply.

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
