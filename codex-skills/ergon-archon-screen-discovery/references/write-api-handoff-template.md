# Write API Handoff Template

Use this file at the end of a read-first investigation or read-first API implementation when the legacy screen has write-like behavior.

The goal is to hand a future write-focused skill a precise starting point. This file should not make write APIs look ready unless the evidence actually supports that.

## Handoff Status

- Screen:
- Business resource:
- Current read state: `Ready for read API` / `Read-first API implemented` / `Blocked` / `Open`
- Write handoff decision: `Legacy-backed Write API candidate` / `Blocked` / `Not suitable`
- Last updated:
- Evidence sources:
  - `component-lineage-matrix.md`:
  - `closure-checklist.md`:
  - `write-risk.md`:
  - `write-risk-detail.sql`:
  - Oracle output:
  - API contract:
  - Implemented read endpoints:

## Read API Baseline

| Endpoint | Status | Implementation File(s) | Notes |
| --- | --- | --- | --- |
| `POST /filter` |  |  |  |
| `GET /{id}` |  |  |  |
| `GET /by-ids` |  |  |  |
| `POST /options/filter` |  |  |  |
| `GET /options/by-ids` |  |  |  |
| `/schemas` / `/schemas/filtered` |  |  |  |

Record only implemented or approved read endpoints. Candidate endpoints should remain candidates for the write skill too.

## Write Entry Points From Legacy UI

| UI Action | XML Component | Legacy Routine / Object | Operation | Current Decision | Notes |
| --- | --- | --- | --- | --- | --- |
| Novo |  |  | insert | Blocked / Candidate / Not present |  |
| Editar |  |  | update | Blocked / Candidate / Not present |  |
| Apagar |  |  | delete/anular | Blocked / Candidate / Not present |  |
| Duplicar |  |  | duplicate | Blocked / Candidate / Not present |  |
| Salvar |  |  | persist | Blocked / Candidate / Not present |  |
| Cancelar |  |  | cancel/no-op | Blocked / Candidate / Not present |  |

## Runtime Write Payload Capture

Capture this before Phase 3 write design. Do not infer payloads from PL/SQL signatures alone.

| UI Action | Runtime State Before | Hidden Keys / Row Locators | Operation Selector | Routine Args Observed | Side Fields Observed | Result / Message | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Novo |  |  | `P_OPER` / equivalent | `PB_*`, `PP_*`, `P_MENS` | publication/legal/pending/flex |  | Captured / Partial / Not captured / Blocked |
| Editar |  |  | `P_OPER` / equivalent | `PB_*`, `PP_*`, `P_ROWID_REG`, `P_MENS` | publication/legal/pending/flex |  | Captured / Partial / Not captured / Blocked |
| Apagar |  |  | `P_OPER` / equivalent | `P_ROWID_REG`, delete/anulation fields, `P_MENS` | pending/publication/legal |  | Captured / Partial / Not captured / Blocked |
| Duplicar |  |  | `P_OPER` / equivalent | source key, copied `PB_*`, copied/cleared `PP_*` | defaults changed by duplicate |  | Captured / Partial / Not captured / Blocked |
| Salvar |  |  | final operation mode | final routine payload | side-effect fields | success/validation | Captured / Partial / Not captured / Blocked |
| Cancelar |  |  | no-op / reset | no persisted routine expected unless proven otherwise | dirty form state | no mutation proof | Captured / Partial / Not captured / Blocked |

For every `Partial`, `Not captured`, or `Blocked`, list the exact next browser/debug/Oracle step in `Blockers For The Write Skill`. Do not use `Unknown` as a final status in this handoff; if evidence is missing, use `Not captured` or `Blocked` with the next check.

## Legacy-Backed Write Candidate

Use this section only when the likely strategy is to call existing PL/SQL/DML routines instead of reimplementing all business rules in Java.

If the Phase 1 execution gate is `Blocked`, this field must also be `Blocked`. Do not leave it as `Open` after a formal gate decision; `Open` is only for work in progress before a gate is closed.

- Primary routine:
- Package/procedure/function owner:
- Operation selector parameter:
- Selected-row key parameter:
- Requires `ROWID`: yes/no/not captured/blocked
- Requires stable public id mapping: yes/no/not captured/blocked
- Requires publication fields: yes/no/not captured/blocked
- Requires legal-document fields: yes/no/not captured/blocked
- Requires pending-record handling: yes/no/not captured/blocked
- Requires Oracle package session context: yes/no/not captured/blocked
- Same-connection Java strategy known: yes/no/not captured/blocked
- Cleanup/reset strategy known: yes/no/not captured/blocked

## Candidate Write Payload

| API Field | Legacy Field / XML Source | PL/SQL Argument | Type | Required | Validation | Notes |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Include hidden/internal fields only when they are necessary for calling the legacy routine. Do not expose `ROWID` as public API without explicit acceptance.

## Side Effects To Preserve

| Area | Legacy Evidence | Required Write Check | Status |
| --- | --- | --- | --- |
| Target table triggers |  | inspect trigger body and timing |  |
| Audit/history |  | inspect audit package/table behavior |  |
| Pending approval |  | inspect `_PND` package/table and approval path |  |
| Publication |  | inspect `PP_%` args and `HADadm_blk001` coupling |  |
| Legal documents |  | inspect `ERGadm_blk004` coupling |  |
| Authorization/profile |  | inspect flags/functions and browser button state |  |
| Session context |  | inspect `FLAG_PACK`/package dependencies |  |
| Autonomous transactions |  | search routine/trigger source |  |

## Error And Validation Mapping

| Legacy Error / Validation | Source | API Error Decision | Status |
| --- | --- | --- | --- |
| Required field |  | `400` field validation |  |
| Invalid date/quantity/code format |  | `400` field validation |  |
| No permission |  | `403` |  |
| Selected row missing |  | `404` |  |
| PL/SQL business error |  | project error envelope |  |
| Oracle/package failure |  | project error envelope with correlation id |  |

## Required Write Parity Cases

| Case | Legacy Action | API Request | Required Evidence | Status |
| --- | --- | --- | --- | --- |
| Insert valid record |  |  | row created and visible in legacy/read API |  |
| Update valid record |  |  | row updated and visible in legacy/read API |  |
| Delete/anular valid record |  |  | legacy delete/anulation semantics preserved |  |
| Duplicate valid record |  |  | duplicate semantics preserved |  |
| Invalid payload |  |  | same functional error class/message |  |
| No permission |  |  | write denied |  |
| Pending on/off |  |  | pending behavior preserved |  |
| Publication/legal fields |  |  | side effects preserved |  |
| Rollback/error |  |  | no partial business mutation |  |

## Blockers For The Write Skill

List exact missing checks. Avoid generic items such as "confirmar no banco".

- 

## Recommendation For Next Skill

Choose one:

- `Proceed with Legacy-backed Write API`: enough evidence exists to design a write contract that calls legacy routines.
- `Investigate write deeper`: routine/trigger/session/error behavior still needs confirmation.
- `Keep write blocked`: write behavior is too broad or unsafe for the next migration slice.
- `Not suitable for write API`: behavior should remain in legacy or move to a separate workflow.
