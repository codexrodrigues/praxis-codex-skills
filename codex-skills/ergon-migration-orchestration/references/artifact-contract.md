# Artifact Contract

## Standard Folder

Use:

```text
docs/migracao/<SCREEN>/
```

Recommended structure:

```text
docs/migracao/<SCREEN>/
  migration-plan.md
  browser-runtime.md
  runtime-capture-form.md
  cronos-source-of-truth.md
  legacy-doc-sources.md
  component-lineage-matrix.md
  investigation.md
  api-contract.md
  read-parity-matrix.md
  read-parity-results.md
  production-context-integration.md
  java-session-context.md
  authorization-scope.md
  write-risk.md
  write-api-handoff.md
  write-contract.md
  write-route-decision.md
  plsql-error-map.md
  write-parity-matrix.md
  ui-contract-checklist.md
  phase-<PHASE-ID>-<slug>-plan.md
  phase-<PHASE-ID>-execution-gate.md
  parity-results.md
  closure-checklist.md
  oracle-confirmation.sql
  hades-registry.sql
  oracle-results/
    ...
```

## Phase Management Files

Required per screen:

- `migration-plan.md`: created in Phase 0 and updated when scope, repositories, operations, environment, or phase order changes.
- `operation-inventory.md`: created by Phase 1 closeout and maintained through every later phase.

Required whenever a phase reaches a decision state:

- `phase-<PHASE-ID>-execution-gate.md`: standalone closeout created or updated whenever a phase is classified as `Ready for next phase`, `Ready for next phase with adjustments`, `Blocked`, or `Deferred`.

Use `docs/migracao/phase-execution-gate-template.md` as the reusable source for `phase-<PHASE-ID>-execution-gate.md`. Prefer the standalone file. An embedded closeout section inside another artifact is only a temporary exception for planning or blocked analysis, and must be promoted to the standalone gate when the phase is closed.

Every gate closed as `Ready for next phase` or `Ready for next phase with adjustments` must include `Continuacao Curta` with next phase, skill, required inputs, expected outputs, carried residuals, and execution intent. This lets the user resume with only `continuar`, `seguir`, `ok`, `1`, `proximo`, or `proximo passo`. If this section is missing or ambiguous, the next short command repairs the gate instead of advancing.

Scaffold/factory scripts are optional helpers. If they are missing or broken, create the required artifacts from the canonical templates and record `SCAFFOLD_UNAVAILABLE` as a tooling residual with path, impact, and next action. Do not skip required evidence or change gate criteria because a scaffold failed.

Optional planning/reentry artifact:

- `phase-<PHASE-ID>-<slug>-plan.md`: use before execution when a phase has partial scope, inherited residuals, conditional fixtures, mutation risk, multiple execution rounds, browser/API/Oracle coordination, or a previous gate classified the screen as `Ready for next phase with adjustments`.

A plan is not evidence and is not a closeout. It must link the previous gate, list carried residuals, define allowed/blocked operations, name evidence to capture, and state the expected closeout artifact.

Naming convention:

- integer phases: `phase-7-plan.md`, `phase-7-execution-gate.md`;
- decimal phases: replace the dot with a hyphen, for example `phase-1-5-execution-gate.md`.

## Phase 1 to Phase 2 Handoff

Phase 2 is read API migration. Phase 1 must provide enough evidence for read endpoints:

- screen code and visible title;
- component lineage for each read area;
- source SQL/XML/runtime evidence;
- bind tokens and observed/default values;
- filter behavior;
- key strategy and hidden key fields;
- scope/session context;
- authorization evidence;
- Cronos/XML source-of-truth decision in `cronos-source-of-truth.md` when runtime XML, local XML, HADES/stored XML, or XML-export status is relevant;
- HADES registry/access/stored-resource SQL or executed output; if blocked, the package must include the exact SQL/helper command needed to resume;
- `runtime-capture-form.md` when the browser workflow is partial/missing and the developer must relay runtime facts;
- endpoint candidate status: `Required Now`, `Candidate`, `Deferred`, or `Not API`;
- write surface status so read migration does not accidentally enable writes.
- read-first closure status when applicable, including `Read handoff ready; write deferred`;
- same-connection session-context setup/cleanup requirements when screen SQL depends on package state;
- public API key and any internal legacy row locator such as `ROWID_REG`, with exposure decision.

If any evidence detail is unknown, the discovery artifact must explain the next evidence needed. Do not use generic `Unknown` as an operation/backend state in `operation-inventory.md`; choose `Blocked`, `Deferred`, `Not present`, `Candidate`, `Ready`, or `Implemented`.

## Phase 1.5 to Phase 2 Handoff

`platform-reuse-inventory.md` must include:

- search terms and executed commands for controllers, resources, DTOs, FilterDTOs, command DTOs, option DTOs/sources, mappers, services, repositories, `/schemas/filtered`, `x-ui`, authorization/scope, and related resources;
- one decision per operation/resource: `reuse`, `extend`, `create`, `block`, `defer`, or `not-api`;
- separate `found` and `compatible` columns; a found resource with partial/no compatibility cannot be handed off as `reuse`;
- DTO role coverage for response DTO, FilterDTO, create/update command, duplicate draft, option DTO/source, mapper/projection, schema evidence, option reload, scope/authorization, semantic fit, and required extension;
- `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` review evidence, or concrete `not applicable` reason;
- `praxis-java-host-project` review when the next contract will create or alter Java/Spring resource/controller/service code;
- `praxis-resource-entity-lookup-backend` review when `RESOURCE_ENTITY`, `OptionSourceRegistry`, `OptionSourceDescriptor`, or `/option-sources/{sourceKey}` are involved;
- for LOV/options, the decision from `platform-option-sources.md` and `options-lov-promotion-status.md`: `PLATFORM_OPTION_SOURCE_RESOLVED`, `PLATFORM_OPTION_SOURCE_REVIEW_REQUIRED`, `PLATFORM_OPTION_SOURCE_BACKLOG_REQUIRED`, or a blocker explaining why the inventory could not be generated;
- for dashboard/KPI/cockpit/analytics, the decision to run `praxis-dashboard-analytics` and whether the API will be an aggregate Praxis resource or a custom dashboard endpoint;
- Phase 2 gaps and residuals that must be carried into `api-contract.md`.

If `Decision=reuse` conflicts with compatibility, options/LOV common source status is missing, or Praxis review evidence is absent for public DTO/schema/options decisions, return to Phase 1.5 before drafting a final Phase 2 contract.

## Phase 1 to Phase 4 Write Audit Handoff

`write-api-handoff.md` must include:

- screen code and visible title;
- current read migration status;
- write actions discovered from browser/XML;
- action source: component id, event, XML snippet, runtime/debug evidence;
- legacy routine or table path per action;
- runtime payload fields captured from browser/debug evidence, including operation selector, hidden keys, `P_ROWID_REG`, `PB_*`, `PP_*`, `P_MENS`, validation messages, and cancel/no-op behavior;
- key strategy, including public key and any internal `ROWID`;
- target tables and side-effect tables;
- session context requirements;
- legacy bridge/shared-executor recommendation when same-connection context, generated routines, or Oracle error translation are required;
- authorization evidence;
- blockers and explicit next operation recommendation.

If any item is not captured, the handoff must use `Not captured`, `Partial`, or `Blocked` and explain the next evidence needed. Do not use `Unknown` as a final handoff status.

Payload inferred only from PL/SQL signatures, XML argument lists, or table columns is not enough for `Ready for write design`. If runtime payload cannot be captured, mark the operation `Blocked` or `Deferred` and record the exact next browser/debug step.

`Unknown` is not a write-design-ready state. Use operation-level states:

- `Ready for audit`: table/routine candidates are known enough to run Phase 4, but write contract is not ready.
- `Ready for write design`: payload, keys, session context, target tables, side effects, and table-rule summaries are closed.
- `Blocked`: missing evidence or access prevents progress.
- `Deferred`: intentionally postponed with risk.
- `Not API`: not part of the migrated API surface.

## Phase 2 to Phase 3 Handoff

Read API migration must provide:

- finalized `api-contract.md`;
- `read-parity-matrix.md`;
- implementation files or explicit implementation plan;
- read-only unsupported write behavior;
- backend automated test summary covering service/query route, same-connection session context when required, key lookup/by-ids, includeIds where relevant, and blocked writes;
- `read-parity-results.md` after implementation begins, with test command/result and any Oracle/browser smoke fixture result;
- `production-context-integration.md` when default user/company mapping remains a production handoff rather than a closed decision;
- remaining read gaps and deferred endpoints.

## Phase 4 to Phase 5 Handoff

For each table, the canonical table-rule summary is:

```text
docs/migracao/<SCREEN>/oracle-results/table-rule-audit/<TABLE>.summary.md
```

The summary must include:

- ordered rules;
- layer: trigger, package, HADES, C_ERGON, generated DML, constraint, audit, pending;
- type: product, client, generated, audit, session context;
- active status;
- evidence: Oracle source line or SQL result summary;
- dependency risk;
- migration decision.

Store raw SQL/output under:

```text
docs/migracao/<SCREEN>/oracle-results/table-rule-audit/
```

Use `tmp/` only for exploratory work; copy final evidence into the screen package when closing a phase.

## Phase 5 to Phase 6 Handoff

`write-contract.md` must include:

- operation status;
- endpoint and HTTP method;
- command DTO;
- routine/table call strategy, copied from a closed `write-route-decision.md`;
- transaction and rollback behavior;
- session context setup and cleanup;
- error mapping reference;
- parity matrix reference;
- unsupported operations and expected HTTP behavior.

`write-route-decision.md` must be produced before Java write implementation when more than one legacy persistence route is possible. It must include:

- candidate routes, such as generated DML procedure, direct table DML, writable view/instead-of trigger, package routine, or HADES action;
- route safety state per operation: `WRITE_TABLE_DIRECT_SAFE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`;
- evidence for each route: XML/runtime/debug, `ALL_OBJECTS`, `ALL_ARGUMENTS`, `ALL_TRIGGERS`, `ALL_SOURCE`, and table-rule audit summaries;
- coverage matrix proving whether each route preserves product rules, client rules, side effects, audit, session context, and transaction semantics;
- decisive runtime evidence or the exact experiment still required;
- one of these decisions: `Chosen`, `Blocked - needs runtime trace`, `Blocked - unsafe transaction`, `Rejected`, or `Deferred`;
- final instruction for the developer: implement only the chosen route, keep operation blocked, or run the listed experiment first.

`WRITE_TABLE_DIRECT_SAFE` is allowed only when direct table/platform persistence is the chosen route and evidence proves rule coverage, HADES/client classification, side-effect coverage, session/context behavior, error mapping, cleanup, and parity. `WRITE_TABLE_DIRECT_CANDIDATE` is not a handoff state for implementation.

`plsql-error-map.md` must include:

- legacy error source;
- raw code/message pattern;
- API status;
- response body fields;
- parity case.

`write-parity-matrix.md` must include:

- operation;
- scenario;
- setup data;
- legacy behavior;
- API expected behavior;
- database side effects;
- status.

## Phase 7 to Phase 8 Handoff

`quality-round-2.md` and `phase-7-execution-gate.md` must include:

- authenticated legacy browser evidence for each claimed case;
- equivalent HTTP request/response evidence for each implemented endpoint;
- comparison of rows, ids/keys, visible fields, labels, ordering, paging, empty state, and messages;
- all divergences classified as `bug`, `accepted gap`, `deferred`, `fixture issue`, or `legacy-only`;
- proof that blocked/deferred operations remain blocked or omitted by the API;
- decision: `Ready for Phase 8`, `Ready for Phase 8 with adjustments`, `Blocked`, or `Deferred`.

If Phase 7 is only planned, the latest artifact must be named as a plan and must not be used as handoff evidence.

## Phase 8 Final Handoff

`parity-results.md`, `backend-api-handoff.md` or scoped `pilot-handoff.md`, and `phase-8-execution-gate.md` must include:

- exact release scope by screen/resource/operation;
- API parity state;
- write side-effect and cleanup evidence for implemented writes;
- related flows classified as full parity, partial read-only, accepted gap, blocked, or deferred;
- residual owner, next action, and whether the residual blocks handoff;
- explicit statement that reusable implementation patterns such as `direct-table-with-triggers` are not reusable unless the new screen's evidence proves the same route.
