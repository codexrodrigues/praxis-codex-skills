# Interpretation Notes

Use these notes only when deciding activation and order.

## Execution Order

For a normal Ergon table with generated packages, the usual order is:

1. `BEFORE STATEMENT` trigger initialization, if present.
2. `BEFORE EACH ROW` trigger source line order.
3. Product `PCK_<TABLE>.MAIN_PRE`.
4. Client trigger-before dispatch, usually `PCK_EXEC_EP_CERG.EXEC_EP_TRG_BEFORE('<TABLE>', ...)`.
5. Row capture into product package arrays for after processing.
6. Audit/history `AFTER EACH ROW` triggers, if present.
7. `AFTER STATEMENT` trigger source line order.
8. Product `PCK_<TABLE>.MAIN_POS`.
9. Client trigger-after dispatch, usually `PCK_EXEC_EP_CERG.EXEC_EP_TRG_AFTER('<TABLE>', ...)`.
10. Pending-record package calls such as `PCK_<TABLE>_PND.GRAVA_PEND`, when present.

Always confirm the order in `ALL_SOURCE`; generated packages and custom triggers can diverge.

Do not rely only on key-call excerpts. For migration, read complete trigger source because validations, pending-state checks, error normalization, and session side effects are often near the package calls rather than on the same line.

## Generated Table Infrastructure

The local Ergon table scripts (`aps/<table>.tab`) commonly call `ERG_GERA_OBJETOS_TABELA`. That generator is documented in `aps/fontes_ergon/erg_gera_objetos_tabela.prc` as the automatic generator for table infrastructure: DML triggers, Hades audit trigger, Ergon audit trigger, DML procedure, publication-aware DML, package, and multi-company view/INSTEAD OF trigger.

Use `.tab` flags as an expectation checklist:

- `P_GERA_TRG_DML`: expect generated DML triggers such as `T_BS_IUD_*`, `T_B_IUD_*`, `T_A_IUD_*`.
- `P_GERA_TRG_AUDHD`: expect Hades audit trigger, often `AUDHD_*`.
- `P_GERA_TRG_AUDIT`: expect Ergon audit trigger, often `AUDIT_*`.
- `P_GERA_PROC_DML`: expect generated DML procedure such as `ERG_DML_*`.
- `P_GERA_PROC_DML_PUBL`: expect DML publication behavior.
- `P_GERA_VIEW_MULT_EMP`: expect multi-company view and INSTEAD OF trigger.

Then confirm actual existence and status in Oracle. A `.tab` file may be older or newer than the current environment.

## Product Versus Client

Treat `PCK_<TABLE>` validations as product unless they delegate to `PCK_EXEC_EP_CERG` or `C_ERGON`.

Treat HADES metadata as dispatch configuration, not proof of execution by itself. Execution requires the active branch:

- Single EP branch: parent `HAD_CAD_SPROC.EXEC='S'` and parent `SINTAXE` not null.
- Multiple EP branch: parent `EXEC_MULT_EPS='S'`; then each child row needs `HAD_CAD_MULT_EPS.EXEC='S'` and child `SINTAXE` not null.

Object existence in `C_ERGON` is not enough to mark a rule active.

## Nested Dependencies

Use the nested dependency map to understand impact and missing-rule risk:

- `ALL_DEPENDENCIES` shows structural compile-time dependencies, not exact runtime order.
- `ALL_SOURCE` call candidates show likely helper calls, validation/error calls, session-context usage, and dynamic SQL.
- HADES `SINTAXE` and `EXECUTE IMMEDIATE` are dynamic dependencies. Treat them as incomplete until the called routine is separately inspected.
- A utility package dependency does not automatically mean business behavior must move to Java; first decide whether the Java path will keep that behavior DB-backed.

For migration decisions:

- If the write path calls the same legacy routine/table path, many nested dependencies may be preserved DB-backed.
- If Java reimplements the rule, every active nested dependency must be classified as reimplemented, replaced, kept DB-backed through a service call, or out of scope.
- If a dependency cannot be classified, mark the rule `Parcial` or keep the operation `Blocked/Deferred`.

## Migration Decision

Use these decisions in the final report:

- `Reimplementar em Java`: validation, derivation, defaulting, permission, or workflow behavior needed by the migrated endpoint.
- `Manter DB-backed`: behavior remains behind a stored procedure/trigger path that Java will still call in production.
- `Preservar como extensibility hook`: HADES/C_ERGON EP exists and may need a Java extension-point equivalent even when no active client row exists today.
- `Somente auditoria/publicacao`: side effect matters for writes but not for read-only parity.
- `Fora do escopo atual`: active legacy behavior exists but cannot be reached by the migrated functionality under review.

When uncertain, mark `Parcial` and state the missing evidence instead of upgrading to active or inactive.
