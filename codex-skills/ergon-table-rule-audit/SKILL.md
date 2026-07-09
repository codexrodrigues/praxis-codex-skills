---
name: ergon-table-rule-audit
description: Audit Ergon legacy Oracle table rules for Java/Spring migration. Use when Codex needs, given an Ergon table name, to identify product rules, generated triggers/DML/audit infrastructure, client custom rules, active/inactive status, execution order, and nested dependencies across ALL_TRIGGERS, ALL_SOURCE, ALL_DEPENDENCIES, generated PCK table packages, generated PND packages, PCK_EXEC_EP_CERG, HADES.PACK_EXEC_SPROC, HADES.HAD_CAD_SPROC, HADES.HAD_CAD_MULT_EPS, and C_ERGON POA_/EP__ functions.
---

# Ergon Table Rule Audit

## Goal

Given a table name, produce an evidence-backed map of table rules. In a multi-phase migration, this skill is phase 2.5 and should be invoked by `ergon-migration-orchestration` only after screen discovery identifies target write tables/routines, normally after the read API boundary is closed.

For the current migration process, this skill is used in Phase 4 as the Ergon write framework audit. When the workspace has `docs/migracao/phase-4-write-framework-checklist.md`, use it as the operation-facing checklist that sits above the table-specific audit.

Apply the root migration `AGENTS.md` when translating audit findings into API
or migration decisions. Audit artifacts may cite HADES, SQL, `ROWID`, package
names, empresa, usuario, perfil, and session context as internal evidence, but
those details must not become public DTO/schema/URL/x-ui/action/surface
contract. If audit reveals a Praxis contract gap, record a `Praxis Platform
Follow-up` instead of recommending an Ergon-local platform workaround.

- Product rules: trigger bodies, generated `PCK_<TABLE>` / `PCK_<TABLE>_PND` routines, direct package calls, constraints, and generated DML procedures.
- Client rules: `PCK_EXEC_EP_CERG` dispatch, `HAD_CAD_SPROC`, `HAD_CAD_MULT_EPS`, and executable `C_ERGON` functions/procedures such as `POA_*` or `EP__*`.
- Generated infrastructure: `.tab` generation flags, DML triggers, audit triggers, Hades audit triggers, multi-company views/triggers, and publication-aware DML procedures.
- Runtime support infrastructure: package-state controls such as `FLAG_PACK` and trigger-state controls such as `PACK_TRG_STAT`. Treat these as legacy mechanisms to understand, not as permission to bypass product rules in Java.
- Activation: `ALL_TRIGGERS.STATUS`, `HAD_CAD_SPROC.EXEC`, `HAD_CAD_SPROC.EXEC_MULT_EPS`, `HAD_CAD_MULT_EPS.EXEC`, object validity, and generation flags as expected-local evidence only.
- Order: trigger timing and source line order, package source line order, and `HAD_CAD_MULT_EPS.ORDEM`.
- Nested dependencies: structural object dependencies from `ALL_DEPENDENCIES`, explicit source call candidates from `ALL_SOURCE`, and dynamic HADES/`EXECUTE IMMEDIATE` risks.
- Migration decision: whether each behavior must be reimplemented in Java, left database-backed, preserved as extension hook, or marked outside the migrated endpoint.

Prefer Oracle metadata over documentation. Use repo source as secondary evidence and docs only as context.

## Mandatory Coverage Gate

Before any write API is marked ready, the table audit must explicitly cover each mandatory source or mark the migration `Blocked`/`Deferred` with the exact rerun command and missing access:

- `ALL_TRIGGERS`: trigger type, event, enabled status, and complete trigger source windows for every trigger on the target table.
- `ALL_SOURCE`: complete source windows for `PCK_<TABLE>`, `PCK_<TABLE>_PND`, generated `ERG_DML_*` procedures, trigger bodies, `PCK_EXEC_EP_CERG`, `HADES.PACK_EXEC_SPROC`, and C_ERGON targets reached from HADES syntax.
- `ALL_DEPENDENCIES`: structural dependencies for trigger/package/generated-DML seeds and nested dependency graph when Java may reimplement behavior.
- HADES dispatch metadata: `HADES.HAD_CAD_SPROC`, `HADES.HAD_CAD_MULT_EPS`, `EXEC`, `EXEC_MULT_EPS`, `ORDEM`, `SINTAXE`, and the active execution branch selected by `HADES.PACK_EXEC_SPROC`.
- Customer extension routines: `C_ERGON` `POA_*`, `TPOA_*`, `EP__*`, and routines referenced by active HADES syntax.
- Generated infrastructure evidence: `.tab` generation flags, generated DML procedures, audit/HADES triggers, publication-aware DML, pending packages, multi-company views/triggers, and `PACK_TRG_STAT`/`FLAG_PACK` usage when present.
- Side-effect tables: every table reached by active source DML candidates must be classified as `Audited`, `Deferred`, or `Rejected as not reached`.

The summary must distinguish `Produto`, `Cliente`, `Gerada`, and infrastructure/session mechanisms. It must also state execution order, active/inactive/invalid status, nested dependency risk, and Java decision for each rule: `Reimplementar em Java`, `Manter DB-backed`, `Preservar como extensibility hook`, `Somente auditoria/publicacao`, `Fora do escopo atual`, `Blocked`, or `Deferred`.

Do not treat object existence, `.tab` flags, source snippets, or a dependency graph as sufficient by themselves. A write migration remains blocked while activation, source windows, side-effect tables, or nested dependencies are only partially known.

## Workflow

1. Normalize the table name to uppercase. Default owner is `ERGON`; do not assume every object is in `ERGON`.
   - When the physical table ends with `_`, also search the logical base name without trailing `_`. Example: `TIPO_FREQ_` can have triggers/DML named with `TIPO_FREQ_`, but product package and EP hooks named `PCK_TIPO_FREQ`, `EPB__TIPO_FREQ`, and `EPA__TIPO_FREQ`.
2. Run `scripts/render_table_rule_audit_sql.ps1` to generate a table-specific SQL file from `scripts/table_rule_audit.sql.tpl`.
3. Execute the generated SQL using the same Oracle access contract as `ergon-archon-screen-discovery`: dot-source `secrets/ergon.env.ps1` when present, prefer `run_oracle_query.ps1`, and fall back to `run_oracle_query_jdbc.ps1` if SQLcl fails in non-interactive Windows execution. Do not print credentials or connect strings.
4. Run `scripts/find_table_generation_flags.ps1` against `docs-legado/v7x` when local legacy docs exist. The script resolves `aps` internally. Treat the `.tab` block as expected generated infrastructure, not proof of current DB state.
5. Inspect local source for the same objects under `docs-legado/v7x/aps/fontes_ergon` and `docs-legado/v7x/aps/fontes_c_ergon` when available.
6. Read complete trigger source, not only filtered key-call lines. Business rules may be adjacent to package calls or error handling and may not contain `EP`, `MAIN_PRE`, or `MAIN_POS`.
7. Read complete `PCK_<TABLE>` / `_PND` package body windows when producing parity cases, error maps, Java reimplementation decisions, or operation contracts. Keyword snippets are an index, not a proof that all validations were seen.
8. Read HADES execution semantics before deciding activation:
   - If `HAD_CAD_SPROC.EXEC_MULT_EPS = 'S'`, execution uses `HAD_CAD_MULT_EPS` rows ordered by `ORDEM`.
   - In `HADES.PACK_EXEC_SPROC`, a row executes only when `EXEC = 'S'` and `SINTAXE` is not null.
   - If a multiple-EP row has `EXEC = 'N'`, it does not execute and there is no fallback to the parent `HAD_CAD_SPROC.SINTAXE` for that row.
   - If `EXEC_MULT_EPS <> 'S'`, the parent `HAD_CAD_SPROC` executes only when `EXEC = 'S'` and `SINTAXE` is not null.
9. Build a mandatory product/client execution matrix for each write-relevant table phase:
   - For `PCK_<TABLE>.MAIN_PRE`, locate `EXEC_EP_PCK_BEFORE`, the logical EP name such as `EPB__<TABLE>`, the returned `v_ep`, the `P_MENS` check, and the exact `IF v_ep THEN` block.
   - For `PCK_<TABLE>.MAIN_POS`, locate `EXEC_EP_PCK_AFTER`, the logical EP name such as `EPA__<TABLE>`, the returned `v_ep`, the `P_MENS` check, and the exact `IF v_ep THEN` block.
   - Classify product rules as `Before EP`, `Inside v_ep gate`, `Outside v_ep gate`, or `After v_ep gate`.
   - For triggers, locate `EXEC_EP_TRG_BEFORE` and `EXEC_EP_TRG_AFTER`; record these as trigger-level client extensions that can block through `P_MENS` but do not return `v_ep` to skip `MAIN_PRE` or `MAIN_POS`.
   - If source does not use `v_ep`, state that explicitly instead of assuming product/client override behavior.
10. When Java may re-orchestrate or reimplement rules, run `scripts/render_nested_dependency_sql.ps1`, execute the generated SQL, then run `scripts/build_dependency_graph_md.ps1` to create a dependency graph summary.
11. Use source DML target candidates to expand side-effect tables. Audit or explicitly discard each pending, audit, publication, association, generated-detail, or package-written table that matters to the operation. Include tables reached transitively by triggers/packages, not only direct foreign-key children.
12. Produce a compact report with a table: order, layer, rule, product/client, active, migration decision, evidence, and dependency risk.

## Oracle Access

Use the same database access rules as `ergon-archon-screen-discovery`.

Codex should run read-only Oracle discovery directly when the workspace is provisioned. Do not ask the developer to run routine confirmation SQL manually. Keep credentials outside generated files and final reports.

Expected local variables:

- `ERGON_HADES_CONN`: SQLcl connection string or wallet alias.
- `ERGON_SQLCL`: path to `sql.exe`.
- `JAVA_HOME`: Java runtime used by SQLcl/JDBC fallback, when required.

For this migration workspace, dot-source the local bootstrap file when it exists:

```powershell
. .\secrets\ergon.env.ps1
```

Do not print that file or echo its variables. The skill may document variable names, but must not store Oracle usernames, passwords, hosts, service names, wallet passwords, or full connection strings.

Preferred SQLcl runner:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query.ps1 `
  -SqlFile $sql `
  -OutputPath $out
```

Fallback JDBC runner when SQLcl has Windows console issues:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile $sql `
  -OutputPath $out `
  -MaxRows 1000
```

If running SQLcl directly, use the SQLcl executable from `ERGON_SQLCL` and pass connection and script as separate arguments:

```powershell
& $env:ERGON_SQLCL @($env:ERGON_HADES_CONN, "@$sql")
```

Do not use `-nolog` before the connection string for this workspace pattern. On Oracle 11g avoid `FETCH FIRST`; use `ROWNUM` or client-side limits.

## SQL Execution

Example from a migration workspace. Use `tmp/` only while exploring; copy or write final SQL/output into the screen package before closing the audit gate:

```powershell
$table = 'FREQUENCIAS'
$screen = 'ERGadm00189'
$auditDir = "docs\migracao\$screen\oracle-results\table-rule-audit"
New-Item -ItemType Directory -Force -Path $auditDir | Out-Null
$sql = Join-Path $auditDir "${table}.audit.sql"
D:\CodexHome\skills\ergon-table-rule-audit\scripts\render_table_rule_audit_sql.ps1 `
  -TableName $table `
  -OutputPath $sql

D:\CodexHome\skills\ergon-table-rule-audit\scripts\find_table_generation_flags.ps1 `
  -TableName $table `
  -DocsRoot docs-legado\v7x

. .\secrets\ergon.env.ps1
& D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query.ps1 `
  -SqlFile $sql `
  -OutputPath (Join-Path $auditDir "${table}.audit.out.txt")
```

If SQLcl fails in non-interactive execution, rerun the same SQL with `run_oracle_query_jdbc.ps1 -MaxRows 1000`.

## Nested Dependency Map

Use the nested dependency map when the migration decision could be `Reimplementar em Java`, when a package has many helper calls, or when the write API needs to prove that the chosen legacy path covers all active rules.

Generate and execute the nested SQL:

```powershell
$table = 'FREQUENCIAS'
$screen = 'ERGadm00189'
$auditDir = "docs\migracao\$screen\oracle-results\table-rule-audit"
New-Item -ItemType Directory -Force -Path $auditDir | Out-Null
$sql = Join-Path $auditDir "${table}.nested-dependencies.sql"
$out = Join-Path $auditDir "${table}.nested-dependencies.out.txt"
$md = Join-Path $auditDir "${table}.dependency-graph.md"

D:\CodexHome\skills\ergon-table-rule-audit\scripts\render_nested_dependency_sql.ps1 `
  -TableName $table `
  -OutputPath $sql `
  -MaxDepth 3

. .\secrets\ergon.env.ps1
& D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile $sql `
  -OutputPath $out `
  -MaxRows 2000

D:\CodexHome\skills\ergon-table-rule-audit\scripts\build_dependency_graph_md.ps1 `
  -InputPath $out `
  -OutputPath $md `
  -TableName $table
```

Default `MaxDepth` is `3`. Increase it only with a concrete reason; broad legacy graphs can become noisy and slow. The generated Markdown contains a Mermaid graph and tables. Treat it as an impact map, not as a full PL/SQL parser.

## Classification

Use these labels:

- `Produto`: trigger code, `PCK_<TABLE>`, generated DML procedures, product package calls, constraints, and product-owned `EP__*` calls in `ERGON`.
- `Cliente`: `PCK_EXEC_EP_CERG`, HADES EP dispatch metadata, `C_ERGON` routines, `POA_*`, `TPOA_*`, customer-specific `EP__*`.
- `Gerada`: object produced by Ergon table-generation infrastructure, even if it still contains business-relevant behavior.
- `Ativa`: trigger enabled or metadata row has `EXEC='S'` in the branch that actually runs.
- `Inativa`: trigger disabled, `EXEC='N'`, missing syntax, or multiple-EP chain row skipped by `EXEC='N'`.
- `Ativa mas invalida/bloqueante`: the active execution path points to an invalid or unreadable object that would fail or block at runtime.
- `Parcial`: object exists but the agent cannot read source, owner differs, privileges are missing, or a synonym hides the effective object.
- `Esperado pelo .tab`: local `.tab` generation flags say an object should be generated; confirm existence/status in Oracle before marking active.
- `Dependencia dinamica`: call path uses `EXECUTE IMMEDIATE`, HADES `SINTAXE`, or source that cannot be resolved statically.
- `Produto gated por v_ep`: product rule inside an `IF v_ep THEN` block after `EXEC_EP_PCK_BEFORE` or `EXEC_EP_PCK_AFTER`; an active client EP returning `FALSE` can skip that block.
- `Produto fora do gate v_ep`: product rule before EP, after the gated block, or otherwise outside `IF v_ep THEN`; do not claim it is skipped by a client EP unless source proves it.
- `Cliente package EP`: `EPB__<TABLE>` or `EPA__<TABLE>` reached through `EXEC_EP_PCK_BEFORE/AFTER`; may return `v_ep` and `P_MENS`.
- `Cliente trigger EP`: `EP_TRG_B_<TABLE>` or `EP_TRG_A_<TABLE>` reached through `EXEC_EP_TRG_BEFORE/AFTER`; may block with `P_MENS` but does not return `v_ep` to the trigger.

## Legacy Documentation Checks

When `docs-legado/v7x` is available, verify these local documentation/source anchors:

- `aps/fontes_ergon/erg_gera_objetos_tabela.prc`: official generator for table infrastructure. It documents `P_GERA_TRG_DML`, `P_GERA_TRG_AUDHD`, `P_GERA_TRG_AUDIT`, `P_GERA_PROC_DML`, `P_GERA_PROC_DML_PUBL`, and `P_GERA_VIEW_MULT_EMP`.
- `aps/<table>.tab`: table-specific generation block. Use it to know whether DML triggers, audit triggers, DML procedures, publication support, or multi-company views were expected.
- `aps/fontes_c_ergon/pck_exec_ep_cerg.pks`: official explanation of package-level EPs (`EXEC_EP_PCK_BEFORE/AFTER`) and trigger-level EPs (`EXEC_EP_TRG_BEFORE/AFTER`).
- `aps/fontes_c_ergon/pck_exec_ep_cerg.pkb`: implementation that delegates to `C_HADES.PACK_EXEC_SPROC`.

For Java migration, include all write-side generated infrastructure in the parity map even if the current feature is initially read-only: generated DML procedure, publication DML, audit triggers, pending packages, workflow hooks, and session-package calls may affect behavior.

Also inspect `PACK_TRG_STAT` usage when triggers call it or when cleanup/parity tests encounter table-mutating errors. This package is a trigger-state flag mechanism used by generated infrastructure. Document where it appears and what it protects, but classify production use from Java as `Blocked` unless the screen route itself proves that bypass behavior.

## Migration Review Standard

For each candidate rule, answer three questions before reporting:

- What executes it: trigger, package, generated DML procedure, HADES dispatcher, direct package call, constraint, or synonym/view indirection?
- Is it active in this database: enabled trigger, valid object, HADES active branch, readable source, and no missing target routine?
- What does it depend on: product package, utility package, session state, client routine, table/view, dynamic SQL, or HADES syntax?
- What must Java preserve: validation/error behavior, audit/history side effect, pending/workflow side effect, publication side effect, data derivation, or no migrated behavior.
- What data can it create or delete indirectly: association rows, company rows, generated detail rows, pending/publication rows, or cleanup-sensitive rows that parity fixtures must remove.

## Output Shape

Write final audit evidence under:

```text
docs/migracao/<SCREEN>/oracle-results/table-rule-audit/
  <TABLE>.audit.sql
  <TABLE>.audit.out.txt
  <TABLE>.summary.md
  <TABLE>.nested-dependencies.sql
  <TABLE>.nested-dependencies.out.txt
  <TABLE>.dependency-graph.md
```

The summary must list every side-effect table as `Audited`, `Deferred`, or `Rejected as not reached`, with evidence. Do not close Phase 2.5 with final evidence only in `tmp/`.

Add a handoff decision section with:

- overall status: `Write API safe to design`, `DB-backed write path required`, `Blocked`, or `Deferred`;
- mandatory source coverage table for `ALL_TRIGGERS`, `ALL_SOURCE`, `ALL_DEPENDENCIES`, HADES dispatch, C_ERGON routines, generated infrastructure, and side-effect tables;
- active rule count by `Produto`, `Cliente`, `Gerada`, and infrastructure/session mechanism;
- rules that can change visible validation/error behavior, audit/history, pending/workflow, publication/legal side effects, derived/defaulted data, or fixture cleanup;
- exact blockers and rerun commands when Oracle, HADES, source, dependency graph, or local `.tab` evidence is missing.

Keep the final answer short and evidence-first:

```markdown
| Ordem | Camada | Regra | Tipo | Ativa? | Decisao Java | Dependencias | Evidencia |
|---:|---|---|---|---|---|---|---|
| 1 | BEFORE EACH ROW trigger | T_B_IUD_<TABLE> calls PCK_<TABLE>.MAIN_PRE | Produto | Sim | Reimplementar/confirmar regra | PCK_<TABLE>, FLAG_PACK | ALL_SOURCE line ... |
| 2 | Package MAIN_PRE | EXEC_EP_PCK_BEFORE('EPB__<TABLE>') | Cliente dispatch | Depende HADES | Preservar ponto de extensao ou manter DB-backed | HADES, C_ERGON | ALL_SOURCE line ...; HAD_CAD_SPROC ... |
| 3 | Generated DML procedure | ERG_DML_<TABLE> | Produto/write path | Sim/Parcial | Avaliar nos endpoints de escrita | triggers, audit, publication | ALL_OBJECTS status ...; .tab flags ... |
```

Also include a product/client execution matrix when the table participates in writes:

```markdown
| Phase | Source | EP/HADES | Client active? | Return path | Product rules in v_ep gate | Product rules outside v_ep gate | Java decision | Evidence |
|---|---|---|---|---|---|---|---|---|
| MAIN_PRE | PCK_<TABLE>.MAIN_PRE | EPB__<TABLE> | Yes/No/Partial | v_ep + P_MENS | rule names/lines | rule names/lines | DB-backed / reimplement / blocked | ALL_SOURCE lines ...; HADES rows ... |
| TRIGGER_BEFORE | T_B_IUD_<TABLE> | EP_TRG_B_<TABLE> | Yes/No/Partial | P_MENS only | n/a | trigger rules/lines | preserve hook / blocked | ALL_SOURCE lines ... |
| MAIN_POS | PCK_<TABLE>.MAIN_POS | EPA__<TABLE> | Yes/No/Partial | v_ep + P_MENS | rule names/lines | rule names/lines | DB-backed / reimplement / blocked | ALL_SOURCE lines ...; HADES rows ... |
| TRIGGER_AFTER | T_A_IUD_<TABLE> | EP_TRG_A_<TABLE> | Yes/No/Partial | P_MENS only | n/a | trigger rules/lines | preserve hook / blocked | ALL_SOURCE lines ... |
```

Then list discrepancies and gaps:

- Repo source diverges from DB trigger/package names.
- HADES metadata exists but source object is missing/inaccessible.
- Documentation states behavior not confirmed by XML/source/Oracle.

## Evidence Rules

- Cite `ALL_SOURCE` owner/name/type/line or local file path and line.
- Cite HADES metadata values as summarized rows, not full credential-bearing output.
- Do not paste hostnames, usernames, passwords, full connect strings, or broad data samples.
- Do not infer trigger order from docs; use `ALL_TRIGGERS.TRIGGER_TYPE` plus `ALL_SOURCE.LINE`.
- Do not infer active client rules from object existence alone; check the HADES `EXEC` flag in the actually selected execution branch.
- Do not treat package EPs and trigger EPs as equivalent. Package EPs can return `v_ep`; trigger EPs only expose `P_MENS` to the trigger caller.
- Do not claim an active client EP disables all product behavior. It only skips product code that source places behind the relevant `IF v_ep THEN` gate.
- Do not omit product code outside `IF v_ep THEN`; it remains part of the route unless another source-level condition proves otherwise.
- Do not infer current database objects from `.tab` flags alone; use them to detect expected objects and then confirm with Oracle metadata.
- Do not reduce the migration analysis to EPs. Generated triggers, DML procedures, constraints, audit, pending packages, and direct product package calls can be business behavior.
- Do not treat the dependency graph as execution order by itself. Use trigger/source line order for order; use dependency graph for impact and missing-rule risk.
- Do not claim Java can reimplement a rule until nested dependencies are classified or explicitly kept DB-backed.
- Do not treat a HADES dependency graph row as active until its `execution_status`/`EXEC` branch is checked. The graph may include inactive dynamic candidates for impact analysis.
- Do not close a write-rule audit with only the main table if source DML candidates identify side-effect tables that can change behavior.
- Do not assume fixture cleanup is simple direct DML. Generated triggers/packages may create transitive rows and may require the same legacy route or a documented technical cleanup path.
- For Spring migration, explicitly say whether each rule must be preserved in Java, remains database-backed, or is out of scope because the migrated endpoint is read-only.
- For Oracle 11g, `ALL_TRIGGERS` trigger owner column is `OWNER`, not `TRIGGER_OWNER`.
