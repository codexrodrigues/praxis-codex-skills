# <SCREEN> - Write Route Decision

## Status

`Blocked - needs runtime trace`

Use one route-decision status per operation:

- `Chosen`
- `Blocked - needs runtime trace`
- `Blocked - unsafe transaction`
- `Rejected`
- `Deferred`

Use one route safety state per operation:

- `WRITE_TABLE_DIRECT_CANDIDATE`
- `WRITE_TABLE_DIRECT_SAFE`
- `WRITE_DB_BACKED_REQUIRED`
- `WRITE_BLOCKED`
- `WRITE_DEFERRED`

## Operation

| Field | Value |
| --- | --- |
| Screen | `<SCREEN>` |
| Operation | `<insert/update/delete/duplicate/business-action>` |
| Endpoint candidate | `<method path>` |
| Public key | `<public id/key>` |
| Target object from UI | `<recordPanelEdit dataTable/db routine/etc>` |
| Route safety state | `<WRITE_TABLE_DIRECT_CANDIDATE/WRITE_TABLE_DIRECT_SAFE/WRITE_DB_BACKED_REQUIRED/WRITE_BLOCKED/WRITE_DEFERRED>` |
| Table-rule handoff | `<Write API safe to design/DB-backed write path required/Blocked/Deferred>` |
| Entry gate status | `<Ready for design/Ready for implementation/Blocked/Deferred>` |

## Candidate Routes

| Route | Status | Evidence | Why it is or is not safe |
| --- | --- | --- | --- |
| Generated DML procedure | `<Chosen/Rejected/Blocked>` | `<ALL_OBJECTS/ALL_ARGUMENTS/ALL_SOURCE/runtime trace>` | `<transaction, rules, side effects>` |
| Direct table DML with triggers | `<Chosen/Rejected/Blocked>` | `<XML dataTable, ALL_TRIGGERS, table audit>` | `<rule coverage>` |
| Writable view / instead-of trigger | `<Chosen/Rejected/Blocked>` | `<ALL_TRIGGERS/ALL_SOURCE for view trigger>` | `<multi-company or key semantics>` |
| Package or HADES action | `<Chosen/Rejected/Blocked>` | `<XML db:* / HADES metadata / source>` | `<rule coverage>` |
| Shared legacy bridge adapter | `<Chosen/Rejected/Blocked>` | `<project convention / same-connection need / reusable runtime>` | `<context, transaction, error translation>` |

## Rule Coverage Matrix

| Rule or behavior | Required by legacy | Generated DML | Direct table DML | Writable view | Package/HADES | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| BEFORE trigger / `MAIN_PRE` | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| AFTER trigger / `MAIN_POS` | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| Side-effect tables | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| Transitive dependency blockers | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| Fixture cleanup route | `<yes/no>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<file or SQL output>` |
| Client EP / HADES | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| Audit/session context | `<yes/no>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<covers/does not cover/unknown>` | `<file or SQL output>` |
| Transaction/rollback | `<yes/no>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<file or SQL output>` |
| Retry/idempotency | `<yes/no>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<safe/unsafe/unknown>` | `<file or SQL output>` |

## Decision Rule

Choose a route only when:

1. Runtime evidence proves the legacy UI uses it, or product documentation/source proves the Archon resolver maps the UI action to it.
2. The route covers all active product and client rules for target and side-effect tables.
3. Transaction behavior is acceptable for the Java API contract.
4. Required session context can be initialized on the same physical Oracle connection.
5. Controlled fixtures can be cleaned without leaving target or side-effect rows behind.

If these conditions are not met, keep the operation blocked.
Do not choose a route just to unblock Java coding. A missing shared legacy bridge, missing session-context setup, missing HADES/client-rule audit, or unknown rollback behavior is a route blocker, not an implementation detail.

Mark `WRITE_TABLE_DIRECT_SAFE` only when direct table/platform persistence is the chosen route and evidence proves:

1. No required product/client/HADES/package-only rule is skipped.
2. Triggers, constraints, defaults, and direct persistence cover the required behavior for the exact operation.
3. Required session context is absent, already provided safely, or not needed.
4. Side effects are absent, covered, or explicitly out of scope with acceptance.
5. Error mapping and error precedence are accepted.
6. Cleanup and rollback are proven for controlled fixtures.
7. API parity proves success and representative negative cases.

If any item is unknown, use `WRITE_TABLE_DIRECT_CANDIDATE`, `WRITE_DB_BACKED_REQUIRED`, or `WRITE_BLOCKED`.

## Next Experiment

Describe the smallest experiment that closes the decision, for example:

- capture Archon debug SQL while saving the screen;
- trace database session for one insert/update/delete;
- run a rollback-safe transaction probe in a disposable record;
- inspect the Archon/Hades resolver source for `recordPanelEdit dataTable`;
- compare side effects produced by each candidate route in a controlled test.
- prove dependency cleanup for a disposable fixture, including generated-detail tables and association tables.

## Developer Instruction

`Do not implement yet. Run the next experiment above.`

When closed, replace with:

`Implement using <chosen route>. Do not use the rejected routes unless this artifact is reopened.`

For `WRITE_TABLE_DIRECT_SAFE`, replace with:

`Implement using direct platform/table persistence for this operation only. Do not generalize to other operations without their own route decision.`
