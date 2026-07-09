---
name: ergon-archon-write-api-migration
description: Design and implement legacy-backed write APIs for Ergon/Archon screens after screen discovery, read API migration, and table-rule audit gates are closed. Use when Codex must turn write-api-handoff.md, write-risk.md, table-rule audit summaries, and read API artifacts into write contracts, PL/SQL-backed Java endpoints, session-context handling, error mapping, and write parity tests for resources such as ERGadm00033 or ERGadm00189.
---

# Ergon Archon Write API Migration

Use this skill only after screen discovery, read API migration, and required table-rule audits are closed or explicitly deferred. In the current orchestration taxonomy, use `ergon-migration-orchestration` first to confirm the relevant Phase 4/5/6 gate.

This skill does not rediscover the screen from scratch. It starts from discovery, read API, and table-rule audit artifacts and decides whether write can be implemented safely, preferably by calling existing legacy routines or preserving generated trigger/package behavior instead of reimplementing all business rules in Java.

This skill must also classify whether a write operation is safe for direct table/platform persistence. Direct Praxis resource persistence is allowed only when the operation reaches `WRITE_TABLE_DIRECT_SAFE`; otherwise use `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`.

When this skill designs or changes command DTOs, request/response DTOs, `@Schema`, `@UISchema`, `@Filterable`, `x-ui`, OpenAPI schemas, `/schemas/filtered`, HATEOAS/action metadata, or capabilities, also use `praxis-dto-annotations` and `ergon-fieldspec-ui-contract`. Use `praxis-java-host-project` when creating or changing a Java/Spring resource. Use `praxis-resource-entity-lookup-backend` when write payloads, actions, or related flows consume `RESOURCE_ENTITY`, `OptionSourceRegistry`, `OptionSourceDescriptor`, or `/option-sources/{sourceKey}`.

## Platform Governance

Before designing, exposing, or implementing write metadata, apply the root
migration `AGENTS.md`. Classify the change as `docs-apenas`, `local-pequena`,
`transversal`, `contrato-publico`, or `arquitetural`, and record the canonical
owner in the phase plan/gate.

Do not patch Praxis platform limitations inside the Ergon write endpoint or UI
contract. Before introducing `@WorkflowAction`, `@UiSurface`, capabilities,
availability rules, custom action models, or Angular workarounds, inventory the
native Praxis support and classify the need as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`.

HADES-backed permission and state decisions must remain server-side through
the approved Ergon bridge/starter and canonical Praxis availability extension
points. Public write metadata may expose only availability and public payload,
never HADES, SQL, `ROWID`, empresa, usuario, perfil, package flags, or session
context. Real Praxis gaps must be recorded as `Praxis Platform Follow-up`.

## Phase Boundary

Use this as the write API migration skill for the current Phase 4/5/6 sequence: Phase 4 audits write behavior, Phase 5 closes the write contract, and Phase 6 implements approved operations. Older references may call this "Phase 3 - Write API Design"; map that wording to the current taxonomy before deciding gates.

1. `ergon-archon-screen-discovery` anchors the user workflow, XML/runtime SQL, read candidates, and write risk/handoff. It identifies candidate write actions and target routines/tables, but should not guess write parity from names alone.
2. `ergon-archon-read-api-migration` closes or implements read/query APIs before write API design. For read-first resources, require backend implementation evidence before write: service/controller tests for the read boundary, explicit blocked-write behavior for inherited generic CRUD, and at least one recorded smoke/parity result or a documented fixture blocker.
3. `ergon-archon-write-api-migration` consumes discovery, read API, and table-rule artifacts and closes one write operation at a time. It may implement Java only after target tables, routines, session context, permissions, rules, side effects, and parity cases are closed.
4. `ergon-table-rule-audit` is a required Phase 4 input for operations that can write data. Run it after write target tables are known from XML/runtime/handoff evidence and before this skill designs a write contract. Do not use it to replace screen discovery.

If the handoff does not identify write actions, target tables/routines, public key strategy, payload evidence, session context, operation status, or write blockers, stop and return to `ergon-archon-screen-discovery`. If table-rule audit summaries are missing for any target or side-effect table, return to `ergon-table-rule-audit` unless the operation is explicitly `Blocked`, `Deferred`, or `Not API`.

## Phase Entry Gate

Before changing Java, command DTOs, public metadata, or API behavior, create or update the write package with an explicit entry-gate decision:

- Phase 1/2 discovery artifacts are closed for the operation, including component lineage, operation inventory, API contract, public key strategy, and read/write handoff.
- Phase 3 read API is implemented or explicitly not required for this operation; read-first resources have backend tests, blocked write behavior for unsupported operations, and read smoke/parity evidence.
- Phase 4 table-rule audit is complete for every target and known side-effect table, including HADES `HAD_CAD_SPROC`, `HAD_CAD_MULT_EPS`, `PACK_EXEC_SPROC`, `C_ERGON` routines, generated trigger/package phases, nested dependencies, session context, and cleanup risks.
- The latest `ergon-table-rule-audit` handoff decision is recorded as `Write API safe to design`, `DB-backed write path required`, `Blocked`, or `Deferred`. Only the first two may enter Phase 5 design.
- `praxis-dto-annotations`, `ergon-fieldspec-ui-contract`, and `praxis-java-host-project` reviews are recorded before declaring `Ready for implementation`; `praxis-resource-entity-lookup-backend` is recorded when option sources participate in payloads, duplicate drafts, related resources, or action metadata.
- The operation has a named state: `Required Now`, `Ready for design`, `Ready for implementation`, `Implemented`, `Blocked`, `Deferred`, `Not API`, or `Not present`.

If any required evidence is missing, do not design a compensating shortcut. Route the work back to the owning phase and record the exact blocker in `write-api-handoff.md` or `write-contract.md`.

Payload closure is a hard Phase 4/5 input. For standard Cronos
`recordPanelEdit + dataTable`, accept parser-valid XML plus local Cronos
framework source as payload evidence when it proves the route, `_op`, `_p_`,
`_o_`, `_q_p_`, editable fields, table metadata SQL generation, and
same-connection Oracle execution. When
`tools/migration-factory/new-cronos-recordpanel-write-payload.ps1` exists,
require a passing `-Strict` run and generated Markdown/JSON under
`docs/migracao/<SCREEN>/factory/`.

For rotina/object-method/custom actions, or when XML/source does not prove the
route, the handoff must include browser/debug evidence for the actual payload
produced by the legacy UI, including operation selector, hidden locators,
business fields, publication fields, `P_MENS`, pending/legal/flex fields,
visible confirmation/validation messages, and cancel/no-op behavior. Do not
design command DTOs by copying all PL/SQL arguments when the screen only sends
or derives a subset.

## Standard Write Operation Set

For Ergon framework screens, design writes by operation, not by generic CRUD alone. Start with this set and mark each operation as `Implemented`, `Ready`, `Blocked`, `Deferred`, or `Not present`:

- `Novo/Salvar`: create command, defaults, required fields, legacy route, validation and cleanup.
- `Editar/Salvar`: update command, immutable keys, changed fields, validation and side effects.
- `Apagar`: delete/anulation command, confirmation, permission/dependency blockers, row preservation proof.
- `Duplicar`: copied/defaulted fields, generated key strategy, usually create-route parity but not assumed.
- `Cancelar`: no-mutation proof for create/edit/duplicate modes.
- `Documentos legais`: legal-document read/write route, link key such as `PONTLEI`, component ownership, and whether it is a separate resource.
- `Publicacoes/atos` and `Pendencias`: include when visible or reached by triggers/packages.

Do not declare a screen's backend "complete" while any visible operation from this set is merely absent from the contract. Either implement it, block it deliberately in the API/UI contract, or defer it with the exact missing evidence and risk.

## Praxis Write Mapping

Use the standard Praxis metadata/API resource surface as the API contract, but choose the implementation route by legacy evidence:

- `Novo/Salvar`: expose `POST /<resource>` and implement through `BaseResourceCommandService.create` only when direct platform persistence is safe. For legacy-generated DML, keep the endpoint but delegate to a screen-specific legacy write service using `ErgonLegacyExecutor`.
- `Editar/Salvar`: expose `PUT /<resource>/{id}` and implement through `BaseResourceCommandService.update`; prefer a command DTO when the read DTO contains derived, hidden, or view-only fields.
- `Apagar`: expose `DELETE /<resource>/{id}` and implement through `BaseResourceCommandService.deleteById`; enable `DELETE /batch` only after separate parity closure.
- `Duplicar`: expose `POST /<resource>/{id}/duplicate-draft` only when the service implements `DuplicateDraftResourceService.duplicateDraft`; use `DuplicateDraftUtils` and `@UISchema(copyOnDuplicate)` for draft behavior, then persist with `POST`. Do not classify duplicate as `@WorkflowAction` merely because the legacy UI has a duplicate button.
- `Cancelar`: do not create a backend mutation; prove no database change from create/edit/duplicate cancellation.
- `Documentos legais`, `Publicacoes/atos`, and `Pendencias`: model as separate related resources/workflows unless the legacy XML/runtime route proves they are part of the main command.

When writes must preserve Ergon behavior, the Praxis resource method is only the HTTP/resource contract. The implementation must run same-connection `FLAG_PACK` setup/cleanup, call the chosen route (`ERG_DML_*`, screen procedure, direct table with triggers, or writable view), translate Oracle/Ergon errors, reload read DTOs through the public key, and record parity evidence.

Never create a parallel write contract because the canonical Praxis action/capability model or Ergon legacy bridge is inconvenient. If Praxis lacks an action, availability, schema, option-source, or error-envelope capability needed for a safe Ergon write, classify the platform gap and keep the operation blocked or deferred until the canonical contract is extended.

Classify every write-like operation against the Praxis semantic contract before exposing metadata:

- Simple create, update, and delete remain resource operations when Phase 4/5 proves the route is safe.
- Partial same-resource maintenance may use `@ResourceIntent` when it needs a named intent but still belongs to the resource contract.
- Related tabs, read projections, embedded maintenance, legal documents, publications, and pending work are `@UiSurface` or separate related resources unless runtime evidence proves they are part of the same command.
- Business commands such as approve, cancel business state, reopen, publish, generate pending work, or other non-CRUD side-effect operations are `@WorkflowAction`. Duplicate is `@WorkflowAction` only when runtime evidence proves a business command with its own immediate effect, dedicated routine, pending/publication side effect, or semantics beyond preparing an editable create draft; otherwise use `duplicate-draft + POST`.
- Availability should use canonical Praxis capabilities/actions/surfaces. For HADES-backed permission or state decisions, use the existing HADES starter/`HadesLegacyAccessGuard`/legacy bridge plus optional Praxis rules such as `ActionAvailabilityRule`, `SurfaceAvailabilityRule`, and `ResourceStateSnapshotProvider`; do not expose HADES, SQL, `ROWID`, empresa, usuario, or raw session context in public metadata.

Route safety states:

- `WRITE_TABLE_DIRECT_CANDIDATE`: direct table/platform persistence may be viable, but evidence is not closed.
- `WRITE_TABLE_DIRECT_SAFE`: direct table/platform persistence is approved for the exact operation. This requires proof that it covers or safely excludes active product/client rules, HADES/EP behavior, package-only logic, side effects, session context, error mapping, transaction behavior, cleanup, and parity.
- `WRITE_DB_BACKED_REQUIRED`: use the validated DB-backed route because direct table persistence would skip or might skip required behavior.
- `WRITE_BLOCKED`: missing or contradictory evidence prevents implementation.
- `WRITE_DEFERRED`: explicitly out of scope.

Unknown means not safe. If any route coverage, side effect, HADES/client behavior, session context, error precedence, or cleanup path is unknown, do not mark `WRITE_TABLE_DIRECT_SAFE`.

## Supporting Skills

Use `ergon-table-rule-audit` before this skill after the write target tables are known. This skill may request additional table audits when operation design reveals side-effect tables not covered in Phase 4.

Use `praxis-dto-annotations` during Phase 5 contract work before marking command DTOs, request/response DTOs, `@Schema`, `@UISchema`, `@Filterable`, `x-ui`, or `/schemas/filtered` as closed. Use `ergon-fieldspec-ui-contract` to validate schema/action/capability metadata consumed by FieldSpec/Angular. Use `praxis-java-host-project` during Phase 6 implementation before changing resources/controllers/services. Use `praxis-resource-entity-lookup-backend` when governed option sources participate in write payloads, duplicate drafts, related resources, or action metadata.

It is not a replacement for screen discovery or XML analysis. It is the table-level rule audit used before choosing a write path. Run it for every base table that can be changed by the operation, including association/publication tables reached by triggers or packages.

Typical examples:

- `TIPO_FREQ_` and `TIPO_FREQ_EMPRESA` for ERGadm00033 type writes;
- `FREQUENCIAS` and related publication/pending tables for ERGadm00189 frequency writes;
- any table named by `recordPanelEdit dataTable`, generated DML procedure arguments, `INSTEAD OF` view triggers, or package side effects.

The audit must feed `write-contract.md`, `plsql-error-map.md`, and `write-parity-matrix.md` with:

- product rules from generated triggers, `PCK_<TABLE>`, `PCK_<TABLE>_PND`, constraints, defaults, and generated DML procedures;
- client rules from `PCK_EXEC_EP_CERG`, HADES `HAD_CAD_SPROC` / `HAD_CAD_MULT_EPS`, and `C_ERGON` routines;
- active/inactive status and execution order;
- the product/client execution matrix for package and trigger phases: `MAIN_PRE`, trigger before, DML/AUX/audit, `MAIN_POS`, and trigger after;
- package EP semantics: `EPB__<TABLE>` and `EPA__<TABLE>` can return `v_ep` plus `P_MENS`; `v_ep = FALSE` can skip only product code inside the relevant `IF v_ep THEN` block;
- trigger EP semantics: `EP_TRG_B_<TABLE>` and `EP_TRG_A_<TABLE>` can block through `P_MENS` but do not return `v_ep` to skip `MAIN_PRE` or `MAIN_POS`;
- product rules explicitly classified as inside or outside the `IF v_ep THEN` gate;
- nested dependency graph when Java may re-orchestrate or reimplement a rule;
- the migration decision for each rule: `Reimplement in Java`, `Keep DB-backed`, `Preserve extension hook`, `Audit/publication only`, or `Out of scope`.

Save table-rule audit SQL and output under the screen package, preferably:

```text
docs/migracao/<SCREEN>/oracle-results/table-rule-audit/
  <TABLE>.sql
  <TABLE>.out.txt
  <TABLE>.summary.md
  <TABLE>.nested-dependencies.sql
  <TABLE>.nested-dependencies.out.txt
  <TABLE>.dependency-graph.md
```

The canonical summary path is `docs/migracao/<SCREEN>/oracle-results/table-rule-audit/<TABLE>.summary.md`. The summary should be short and should contain only findings needed by the write decision, not full trigger/package source dumps. If a root-level `table-rule-audit-<table>.md` exists from exploratory work, link or migrate it into the canonical folder before closing the gate.

## Required Inputs

Before using this skill, verify the screen package has:

- `closure-checklist.md` with screen discovery closed for the intended slice;
- `component-lineage-matrix.md`;
- `api-contract.md`;
- `read-parity-matrix.md` and read implementation/test evidence when reads were implemented;
- `read-parity-results.md` when a read endpoint already exists, including commands/results, smoke fixture, remaining backend parity gaps, and any reason OpenAPI/x-ui checks are still planned;
- `write-risk.md`;
- `write-risk-detail.sql` and Oracle output when database access is available;
- `write-api-handoff.md`;
- `operation-inventory.md` or equivalent operation table listing list/detail/create/update/delete/duplicate/cancel/legal/publication/pending states;
- `platform-reuse-inventory.md` or an equivalent explicit decision showing whether each write/related resource will reuse, extend, create, block, defer, or stay out of the API;
- runtime or source-derived write payload evidence for every operation being designed: for standard Cronos `recordPanelEdit + dataTable`, a passing source-derived payload artifact is acceptable; for other actions use browser/debug payload evidence for `Novo`, `Editar`, `Apagar`, `Duplicar`, `Salvar`, `Cancelar`, or an explicit `Not present` / `Blocked` row;
- for `Duplicar`, a decision proving whether the flow is `duplicate-draft + POST`, a dedicated legacy route, a real `@WorkflowAction`, `Blocked`, or `Not present`; `duplicateEnabled=true` alone is not enough;
- table-rule audit summaries for each target and known side-effect table, unless the operation is not proceeding beyond `Blocked`/`Deferred`;
- implemented read API files when the current state is `Read API implemented`.

If these are missing, return to the owning earlier phase instead of guessing write behavior: use `ergon-archon-screen-discovery` for missing lineage/handoff, `ergon-archon-read-api-migration` for missing read implementation or read parity evidence, and `ergon-table-rule-audit` for missing table-rule evidence.

## Core Strategy

Prefer `Legacy-backed Write API` when possible:

- Java owns REST contract, authentication, authorization checks, payload validation, session context setup, transaction boundary, and error mapping.
- Oracle legacy routines, generated DML, triggers, and packages preserve business behavior.
- Java reimplementation is allowed only when the legacy routine is unsuitable and all validations, side effects, and parity cases are fully understood.

Do not expose generic CRUD merely because `AbstractResourceController` has create/update/delete hooks.

Do expose direct platform/table CRUD when, and only when, `write-route-decision.md` marks the operation `WRITE_TABLE_DIRECT_SAFE` and parity evidence supports it. This is a speed path, not a shortcut around rule audit.

## Legacy Bridge Pattern

When a migrated service must talk to legacy write behavior for years while the full flow remains split between Java and Oracle, prefer a small shared bridge over ad hoc database calls in each resource.

The bridge should centralize:

- same-connection legacy context setup such as `HADES.FLAG_PACK.SET_USUARIO`, `SET_TRANSACAO`, `SET_EMPRESA`, and optional `SET_SIS`/`SET_ROLE`;
- legacy user and company mapping through shared application hooks, such as `ErgonLegacyContextProvider`, `ErgonLegacyUserMapper`, and `ErgonLegacyCompanyResolver` in `ms-administracao-pessoal`, so production IdP/company-session differences are not reimplemented per write service;
- transaction participation and cleanup/reset for pooled connections;
- invocation of the chosen route: generated `ERG_DML_*`, direct table DML with generated triggers, writable view, or specific PL/SQL package;
- translation of `ORA-20xxx`, HADES/Ergon validation messages, unique violations, dependency violations, and setup failures into stable API errors;
- operation metadata: screen/transaction, company, user, route name, and evidence links.

If no existing Praxis host/shared module already provides this capability, create or extend a runtime-neutral legacy bridge only when it stays independent of UI/editor code and does not import a business module. Keep screen-specific DML, SQL text, DTO mapping, and policy decisions in the application module.

Do not make `JdbcTemplate` the declared project standard just because the bridge uses JDBC internally. First inspect the target module and starter conventions. If the module uses Spring Data/JPA plus a starter, keep resource/service/repository code aligned with that convention and confine low-level JDBC to a shared executor only when same-connection package state or callable PL/SQL requires it. Document the deviation in `write-route-decision.md`.

## Workflow

1. Read `write-api-handoff.md`, `write-risk.md`, `api-contract.md`, `platform-reuse-inventory.md`, and the read implementation files.
2. Identify the write resource, operations, public key strategy, current read DTO, and UI write buttons using the Standard Write Operation Set.
3. Inspect the Java project convention before selecting a persistence mechanism: existing write resources, starter-provided services/repositories, Spring Data/JPA repositories, `EntityManager`, transaction/session helpers, and any project abstraction for calling PL/SQL or generated DML. If Phase 1.5 found an existing resource, prefer reusing/extending it over creating a parallel endpoint. Do not assume `JdbcTemplate` is the default merely because direct Oracle calls are needed. If no shared helper exists and same-connection package state is required, propose or implement a legacy bridge abstraction instead of scattering low-level JDBC.
4. Inspect the Archon XML write component: `recordPanelEdit`, `dataTable`, `db:*` routine, duplicate behavior, delete/anulacao behavior, linked publication/legal blocks, and hidden row keys.
5. Inspect Oracle metadata for target tables, generated DML routines, triggers, grants, constraints, defaults, packages, package arguments, and source references.
6. Run `ergon-table-rule-audit` for each write target base table and each side-effect table that can be reached by triggers/packages.
7. Convert table-rule audit findings into an operation-level product/client decision matrix. For each phase (`MAIN_PRE`, trigger before, DML/AUX/audit, `MAIN_POS`, trigger after), classify the result as `product only`, `client + product`, `client replaces gated product block`, `client blocks by P_MENS`, `inactive`, or `unknown/blocked`. Identify product rules inside and outside `IF v_ep THEN`.
8. Convert the matrix into operation-level decisions: which rules are covered by the chosen legacy write path, which require Java behavior, which are audit/publication only, which preserve a customer extension hook, and which are out of scope for this operation.
9. If more than one persistence route exists, produce `write-route-decision.md` from [write-route-decision-template.md](references/write-route-decision-template.md). Do not ask the developer to choose manually. Compare generated `ERG_DML_*`, direct base-table DML, writable view triggers, and screen-specific PL/SQL packages against the same fixture whenever possible.
10. Decide the write strategy for each operation: `legacy-routine`, `direct-table-with-triggers`, `writable-view`, `java-reimplementation`, `blocked`, or `not-api`.
   Also record route safety state: `WRITE_TABLE_DIRECT_SAFE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`.
11. Produce `write-contract.md` from [write-contract-template.md](references/write-contract-template.md). Include the product/client decision matrix in the contract or link to the canonical table-rule audit summary that contains it. Record the applied `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` review before marking Phase 5 ready.
12. Produce `plsql-error-map.md` from [plsql-error-map-template.md](references/plsql-error-map-template.md).
13. Produce `write-parity-matrix.md` from [write-parity-template.md](references/write-parity-template.md). Include one row per standard operation, even when the current slice implements only create/delete.
14. Before Java implementation, close focused write probes for the smallest operation slice: valid fixture, invalid payload, missing required fields, duplicate/collision, no permission, missing row, and cleanup/final-count behavior. Store each SQL and output under `oracle-results/`.
15. Only implement Java write endpoints when all gates for the operation are closed or explicitly deferred for out-of-scope behavior.
16. After implementation, run API, OpenAPI/schema, database, and parity checks. For write pilots, run API-level success and negative smokes against Oracle, record request/response JSON, read-after-write behavior, target/side-effect table counts, rollback/no-partial-mutation proof for failed cases, and final zero-count cleanup proof. Keep unsafe operations blocked with explicit HTTP behavior. Include dependency and cleanup parity when delete/update can touch association or generated side-effect tables. Record the applied `praxis-dto-annotations`, `praxis-java-host-project`, and `ergon-fieldspec-ui-contract` reviews in implementation evidence.
17. Before declaring a pilot slice closed, update the parity matrix with exact cases closed by API smoke and exact cases deferred from the pilot. Deferrals must name the operation and reason, such as delete permission requiring a two-user fixture, dependency delete requiring approved dependent-row setup, pending requiring an environment/profile that generates `*_PND`, or publication/legal requiring related-component payload capture.

## Write Gates

An operation can move to implementation only when all required gates are closed:

- Public key maps to the legacy row or routine input without exposing `ROWID` unless explicitly accepted.
- Payload fields map to legacy UI fields and routine/table columns.
- Runtime or source-derived payload evidence proves which fields the legacy UI sends, derives, defaults, or omits for the operation. For standard Cronos `recordPanelEdit + dataTable`, XML + Cronos source can close this gate before the DB probe.
- Oracle same-connection session context is implemented when `FLAG_PACK` or package state is involved.
- Legacy user/company mapping is centralized and testable; fallback user/company values are explicit and production mapper/resolver hooks are available.
- Permission source is known: HADES access flags, UI capability, Oracle function/package, Java policy, or a combination.
- Trigger/package side effects are known.
- Generated DML procedure behavior is known when the procedure exists, including whether it commits/rolls back internally and whether it matches the screen's route.
- Product and client table rules were audited with `ergon-table-rule-audit` for every changed table and side-effect table discovered so far.
- The chosen write path explicitly covers or rejects each active table rule from the audit.
- The table-rule audit includes a product/client execution matrix for each target table phase, including package EPs, trigger EPs, HADES active/inactive branch, `P_MENS`, `v_ep`, and product rules inside/outside `IF v_ep THEN`.
- `write-contract.md` states whether each phase is `product only`, `client + product`, `client replaces gated product block`, `client blocks by P_MENS`, `inactive`, or `blocked`.
- If Java reimplements behavior, the contract states whether it replaces only the gated product block or also product behavior outside the `v_ep` gate.
- If multiple persistence routes exist, `write-route-decision.md` marks exactly one route as `Chosen`, or the operation remains `Blocked` with the next experiment.
- Direct table/platform persistence is marked `WRITE_TABLE_DIRECT_SAFE` only with route coverage, side-effect coverage, HADES/client classification, session context, error mapping, cleanup, and parity evidence.
- Nested dependencies are classified when a rule is reimplemented or orchestrated in Java instead of preserved DB-backed.
- PL/SQL errors and validation messages are mapped to API errors.
- Raw Oracle errors raised by legacy routines are still contract evidence. If probes surface `ORA-06502`, `ORA-01422`, `ORA-00001`, or similar low-level failures for business-invalid input, map them to stable API errors and add Java pre-validation where appropriate instead of leaking Oracle internals.
- Transaction, rollback, and autonomous transaction behavior are understood.
- The API contract states the transaction boundary, rollback expectation, self-commit/autonomous-transaction risk, cleanup route, and how partial side effects are detected and normalized.
- Parity cases exist for success, invalid input, missing row, duplicate, delete/anulation, pending, and side effects in scope. Permission denial is executed only when a real denied user/profile fixture exists; otherwise record waiver/accepted risk without blocking the screen.
- Controlled fixtures have a cleanup plan that respects legacy-generated dependencies; do not create database test data whose rollback/removal route is unknown.
- For resources migrated read-first, the read resource has backend automated tests and recorded smoke/parity evidence before write endpoints are opened.
- Phase 1.5 has checked whether the write/related operation already exists in the new Java/OMS platform and has chosen reuse, extension, creation, blocking, deferral, or not-api.
- Pilot closure must be evidence-backed: at minimum, record one successful API write/readback/delete cycle, one validation failure with no mutation, one duplicate/collision or equivalent conflict when applicable, one permission denial when a user fixture exists, and explicit deferral rows for everything not in the pilot surface.
- A backend slice can be accepted as partial only when all unimplemented visible operations from the standard set are deliberately blocked or deferred in the contract and parity matrix.

If any gate is open, keep the operation `Blocked` or `Deferred`.

Treat payload inferred only from PL/SQL arguments as an open gate. The next action is to return to screen discovery and close payload either through the Cronos source-derived path for standard `recordPanelEdit + dataTable`, or through browser/debug runtime capture for rotina/object-method/custom actions.

## Controlled Probe Discipline

Use disposable fixtures and negative probes before opening write endpoints. For each probe:

- choose a fixture key/date/marker that has zero baseline rows in the target and known side-effect tables;
- before any mutating run, execute a read-only context preflight that proves the selected legacy user, transaction, and empresa context are non-null/valid for side effects reached by the route; if the environment does not provide empresa, discover a valid fixture empresa through the referenced legacy FK/table and record that evidence;
- set `FLAG_PACK` on the same connection before invoking the routine, including explicit empresa context when generated triggers/packages call `FLAG_PACK.GET_EMPRESA`;
- execute the exact candidate route, such as `ERG_DML_*`, wrapper routine, or screen-specific package;
- print `call_status`, `sqlcode`, `sqlerrm`, `P_ROWID_REG`, `P_MENS`, and before/after counts;
- include a defensive cleanup path through the same legacy route if the probe unexpectedly creates data;
- commit cleanup explicitly when the legacy route persists beyond caller rollback;
- store both SQL and output under the screen package, using names like `write-invalid-quantity-probe.sql` and `.out.txt`;
- update `plsql-error-map.md` and `write-parity-matrix.md` immediately after each probe.

Do not discard probes that produce raw Oracle errors. A raw `ORA-06502` for invalid quantity or `ORA-01422` for missing code is a migration finding: the API should pre-validate or translate it into a stable business response while preserving the DB-backed route for valid writes.

For duplicate/collision probes, create the first disposable row through the chosen legacy route, attempt the second row with the same key, record the legacy constraint/message, then delete every marker row through the legacy route and prove final counts are zero.

For permission probes, use a real legacy user/profile fixture when one exists.
A read-denied user can be useful, but write permission must be proven by the
write routine before claiming `403` parity. If no valid denied principal exists,
record a waiver/accepted risk and continue; lack of such fixture must not block
the migrated screen. Do not infer write authorization from UI button state or
read `MOSTRA_*` alone.

If SQLcl is unreliable in the local environment, use a JDBC PL/SQL runner that enables `DBMS_OUTPUT`, runs the block on one connection, and writes output to `.out.txt`. The runner is a test/discovery tool only; production code should use the shared legacy bridge pattern.

## API Smoke Discipline

For each implemented write slice, create API result artifacts under `docs/migracao/<SCREEN>/api-results/` and Oracle count artifacts under `docs/migracao/<SCREEN>/oracle-results/`.

Before any mutating API call, run an API smoke preflight and record it as an
artifact. The preflight must prove the local API base URL is alive, the domain
endpoint is protected, a valid authenticated HADES Basic/login session or
cookie is available, and the controlled marker has zero baseline rows in target
and known side-effect tables. Restored Oracle connectivity alone is not API
smoke readiness. If authentication is missing, stop before mutation, record the
auth blocker, and do not mark HTTP parity as closed.

When the migration workspace provides `secrets/ergon.env.ps1`, dot-source it in
the active shell for local smoke/probe execution. Treat it as the approved local
secret source for variables such as `ERGON_HADES_CONN`, `ERGON_SQLCL`,
`ERGON_LEGACY_USER`, `ERGON_LEGACY_PASSWORD`, `ERGON_RESTRICTED_USER`, and
`ERGON_RESTRICTED_PASSWORD`. Use `ERGON_LEGACY_USER`/`ERGON_LEGACY_PASSWORD`
for the positive HADES login preflight and use restricted-user variables only
for permission-denied parity when the case needs a denied fixture. Never print
or persist secret values, session cookies, Authorization headers, or connection
strings; artifacts may record only that the variables were available and which
credential class was used.

Credentials do not authorize mutation by themselves. Before any mutating API
or DB probe, record explicit user approval or an existing gate artifact that
names the screen, resource, disposable marker(s), allowed operations, cleanup
expectation, and exclusions. If approval names a marker such as `CX33P5A`, use
only that marker and its documented negative variants; do not extend the scope
to real business rows, child resources, dependency fixtures, legal documents,
publications, pending flows, or alternate markers without a new approval.

Record:

- API base URL, legacy user/company/transaction context, and VPN/Oracle connectivity state;
- request JSON for each case;
- response status/body for success, validation, duplicate/conflict, and permission cases;
- public ID returned by create and read-after-write/read-after-delete result;
- before/after counts for target and side-effect tables, including pending tables such as `FREQUENCIAS_PND`;
- cleanup route and final zero-count proof.

For permission smokes, run the API with a real denied legacy user fixture or
authenticated principal mapping only when that fixture is available. If the
local app uses fallback properties, it is acceptable for a pilot smoke to start
a temporary API process with a denied `ERGON_USUARIO_PADRAO`, as long as the
artifact states that this is a local fixture and production auth mapping
remains a separate concern. If no valid denied fixture exists, record waiver
instead of blocking the screen and do not claim proven `403` parity.

Do not leave local API processes running after smoke tests.

## Java Implementation Rules

For resources already migrated read-first:

- Reuse existing controller, DTO, FilterDTO, mapper, service, ID converter, endpoint constants, OpenAPI group, and tests when they represent the same resource.
- Match the project's established persistence convention before introducing low-level database access. If the project/starter uses Spring Data/JPA repositories or starter services for writes, prefer that pattern unless the chosen legacy write path requires lower-level same-connection PL/SQL handling and the deviation is documented in `write-route-decision.md`.
- When the operation must preserve Oracle package state, triggers, generated DML, or PL/SQL routines, look first for an established project/starter legacy executor or session-context helper. If none exists, recommend or implement a small legacy-backed execution adapter instead of scattering `JdbcTemplate`/connection handling across resource services.
- Keep the shared adapter generic. Application services should choose the route and bind the payload; the adapter should execute legacy work inside the correct context and translate errors.
- Remove read-only 405 behavior only for operations whose write gates are closed.
- Keep unrelated write operations blocked.
- Avoid making `@Immutable` read models mutable unless the resource is intentionally moved away from view-backed reads.
- Prefer a dedicated command DTO for write payloads when response/read DTO contains derived, hidden, view-only, or display-only fields.
- Keep `ROWID` internal; if a legacy routine requires it, resolve it server-side from the public key where possible.
- Initialize Oracle session context on the same physical connection used for the write.
- Reuse the shared legacy context provider/resolvers from the read API when available. Do not inject fallback user/company properties directly into each write service.
- Clean up/reset package context before returning pooled connections.
- Keep write routes idempotency-aware at the API boundary. If the legacy route is not idempotent, the contract must state retry behavior and the API smoke must prove duplicate/collision handling before exposing the operation as safe for automated clients.

If any write path requires a new shared legacy bridge, centralize it in the host/runtime layer. Do not encode screen-specific Oracle session handling, HADES user/company mapping, or PL/SQL error normalization separately in each controller/service.

## Dependency And Cleanup Parity

For delete/update operations, verify both direct blockers and blockers created transitively by legacy triggers/packages. A code/detail table can generate additional rows in tables such as `FINFREQ_*`, publication, pending, audit, or company-association tables.

Use controlled fixture data only. Do not test dependency deletes against real business records unless explicitly approved. A dependency parity run should record:

- baseline absence of the fixture;
- API mutation that creates the main row;
- fixture setup route for dependent rows and whether it uses generated DML or direct DML;
- failed API delete/update response and mapped HTTP status;
- Oracle proof that main and dependent rows were preserved;
- cleanup route and final Oracle proof that all fixture rows are gone.

If cleanup reveals a legacy maintenance mechanism such as `HADES.PACK_TRG_STAT`, document it as fixture cleanup evidence only. Do not use trigger bypass as the production write path unless the legacy screen itself proves that behavior.

## Case Reference

Use [case-ergadm00033-write-pilot.md](references/case-ergadm00033-write-pilot.md) when designing or validating this skill with a real first-phase read migration.

Use [case-ergadm00189-create-delete-pilot.md](references/case-ergadm00189-create-delete-pilot.md) when a migration needs examples of create/delete probes against a self-committing legacy routine, API-level success/negative/permission smokes, raw Oracle error normalization, permission denial, duplicate cleanup, final zero-count proof, explicit pilot deferrals, and `ROWID`-internal public-key design.

Use [operation-prompt-examples.md](references/operation-prompt-examples.md) when the user wants a didactic PT-BR guide or ready-to-use prompts for starting write migration by operation type. It contains diagrams and prompt templates for insert/create, update, delete, duplicate, association writes, business actions, and blocked-write review.

The ERGadm00033 case is useful because:

- The read-first backend resources already define blocked write behavior.
- Backend resources `tipos-frequencia` and `codigos-frequencia` are implemented as read-first resources.
- `TipoFrequenciaResourceService` and `CodigoFrequenciaResourceService` currently return 405 for writes.
- Legacy XML shows `recordPanelEdit` over `TIPO_FREQ_`.
- Legacy packages/triggers show write side effects through `PCK_TIPO_FREQ`, `PCK_TIPO_FREQ_EMPRESA`, generated DML triggers, `FLAG_PACK.GET_EMPRESA`, and validation errors.

## Required Output By Phase

For Phase 4 audit closure, produce or update only audit/readiness artifacts:

- `write-risk.md` with payload, route candidates, target tables, side effects, HADES/EP/session-context findings, and operation states;
- `write-api-handoff.md` with the exact Phase 5 inputs, blockers, and deferrals;
- canonical table-rule audit SQL/output/summaries under `oracle-results/table-rule-audit/`;
- `phase-4-execution-gate.md` carrying evidence and residuals.

Do not mark `WRITE_TABLE_DIRECT_SAFE`, implementation-ready, or Java-implementation-approved in Phase 4 artifacts.

For Phase 5/6 write contract and implementation attempts, produce or update:

- `write-contract.md`;
- `write-route-decision.md` when route ambiguity exists;
- `plsql-error-map.md`;
- `write-parity-matrix.md`;
- focused Oracle confirmation SQL/output for write;
- Java implementation plan or code changes;
- updated API/OpenAPI/x-ui tests;
- final operation state: `Implemented`, `Blocked`, `Deferred`, or `Not API`.
- updated operation inventory or closure checklist with every standard operation state.

When implementation is blocked, state the exact missing evidence and next query/runtime check.

## Do Not

- Do not bypass legacy package/session behavior with direct repository `save` unless triggers/packages prove this is safe.
- Do not expose view-backed DTOs as write payloads without removing derived/internal/read-only fields.
- Do not trust any client-side disabled state as authorization.
- Do not treat read parity as write parity.
- Do not implement batch delete, duplicate, publication, legal-document, or pending behavior unless the specific flow is closed.
- Do not use trigger bypass mechanisms such as `PACK_TRG_STAT` in application write endpoints unless the exact legacy UI route uses them and parity proves it.
