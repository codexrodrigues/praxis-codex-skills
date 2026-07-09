# Screen Write-Risk Template

Use this file when a screen has create, edit, delete, duplicate, approve, publish, legal-document, or pending-record behavior.

## Status

- Screen:
- Status: `In scope` / `Blocked for write API` / `Deferred`
- Evidence query:
- Oracle output:
- Confidence:

## Main Finding

State whether the screen writes directly to a table/view, calls a DML routine, uses generated Archon hooks, or only opens related write flows.

Before concluding direct CRUD, compare the screen with the skill reference `references/archon-write-patterns.md`. In many Ergon/Archon screens the visible form is only the entry point into generated DML, triggers, audit, pending records, publication, and legal-document side effects.

## Write Entry Points

| UI Action | XML Component | Routine / Object | Operation | Runtime Status | Notes |
| --- | --- | --- | --- | --- | --- |
| Novo |  |  | insert | pending |  |
| Editar |  |  | update | pending |  |
| Apagar |  |  | delete | pending |  |
| Duplicar |  |  | duplicate | pending |  |
| Salvar |  |  | persist | pending |  |
| Cancelar |  |  | cancel | pending |  |

## Procedure Or DML Contract

List inputs and outputs only at the level needed for migration decisions:

- operation parameter:
- selected-row key or `ROWID` parameter:
- domain fields:
- publication/legal-document fields:
- pending-record fields:
- output message/error parameter:
- `PP_%` publication arguments present: yes/no/unknown
- generated DML evidence: `HAD_GERA_PROC_DML` / `dbms_sql.bind_variable_rowid` / unknown

## Architecture Pattern Checks

| Check | Evidence | Status | Notes |
| --- | --- | --- | --- |
| XML `recordPanelEdit` / reusable block found |  | pending |  |
| `db:*` write routine found |  | pending |  |
| `ERG_DML_*` or generated DML pattern found |  | pending |  |
| `PP_%` publication args checked |  | pending |  |
| Target table triggers checked |  | pending |  |
| `PCK_<TABELA>` checked |  | pending |  |
| Audit/session context checked |  | pending |  |
| `_PND` table/package checked |  | pending |  |
| `PACK_ERG_PEND` / `PACK_HAD_PEND` involvement checked |  | pending |  |
| `HADadm_blk001` publication block checked |  | pending |  |
| `ERGadm_blk004` legal-document block checked |  | pending |  |

## Validations

Summarize legacy validations and where they live:

- required fields:
- lookup/code validity:
- quantity/date/time formatting:
- authorization/profile checks:
- business rules:
- legacy error messages:

## Trigger And Side Effects

| Object | Timing | Side Effect | Migration Risk |
| --- | --- | --- | --- |
|  |  |  |  |

Include audit, generated history, pending approval, publication/legal pointers, process pointers, autonomous transactions, and extension hooks.

## Required Write Parity Topics

- browser behavior for write buttons, save/cancel, confirmations, and validation messages;
- exact payload fields supplied by the legacy UI;
- same-connection session context required by triggers/packages;
- rollback/commit behavior, including autonomous transactions;
- pending approval on/off behavior;
- publication/legal-document coupling;
- permission denied cases;
- invalid input cases;
- duplicate/update/delete cases.

## Decision

State the phase boundary:

- `Write API ready`: only when browser, XML, Oracle, triggers, package state, and parity cases are closed.
- `Blocked for write API`: when write is real but too risky for the current phase.
- `Deferred`: when write is intentionally out of scope and the read API can proceed without it.
