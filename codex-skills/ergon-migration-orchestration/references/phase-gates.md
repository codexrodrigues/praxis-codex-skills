# Phase Gates

## Current Phase Taxonomy

Use the current orchestration numbering from `SKILL.md`:

| Current phase | Purpose |
| --- | --- |
| Phase 0 | Operational preparation |
| Phase 1 | Legacy screen operation inventory |
| Phase 1.5 | New platform reuse discovery |
| Phase 2 | Read/options API contract |
| Phase 3 | Read/options implementation and parity |
| Phase 4 | Write audit by operation |
| Phase 5 | Write contract by operation |
| Phase 6 | Java implementation by operation |
| Phase 7 | Quality Round 2 |
| Phase 8 | Final parity and handoff |
| UI track | Native Praxis UI wiring after backend handoff |
| Dashboard track | Praxis analytics and chart materialization |
| Rule Migration Parte 2 | Governed rule migration after Parte 1 baseline |

Older historical notes may use UI-oriented numbering. Treat those labels as legacy wording only and map the work to the current taxonomy above before deciding gates or next skills.

## Phase 0 - Operational Preparation

Ready when:

- screen or functionality is named;
- target backend/API repository/module is known;
- legacy `.tp` route was opened in an authenticated session, or the blocker is explicit;
- if credentials were available in the active session, browser/app login was attempted before classifying `.tp` or `.xml` as blocked/deferred;
- XML export/download from the legacy app was obtained after authenticated login when possible, or local/classpath XML fallback and authenticated export blocker are explicit;
- Oracle/database connection was tested with a simple read-only probe, or the blocker is explicit;
- environment and database access are known or explicitly unavailable;
- XML/debug source is classified only as source candidate/provisional evidence, without component, SQL, filter, link, table, or write-route extraction;
- visual/UI libraries or apps are not listed as Phase 0 dependencies;
- intended scope is classified as read-only, read-first, write, or unknown;
- output folder under `docs/migracao/<SCREEN>/` is chosen.
- if a scaffold/factory was unavailable, the artifact records `SCAFFOLD_UNAVAILABLE` as a tooling residual and still uses the canonical templates.

Blocking gaps:

- no screen/functionality target;
- no access path to legacy evidence;
- unclear migration objective.
- no usable XML/export/local fallback and no documented export blocker.
- credentials were available but login was not attempted before closing Phase 0 (`RUNTIME_LOGIN_NOT_ATTEMPTED`).
- no Oracle probe result while credentials are available.
- legacy `.tp` route was not tested and no blocker is documented.
- `.tp`/`.xml` status is based only on unauthenticated `401`/`403` while credentials were available.
- Phase 0 artifact promotes XML internals, SQL, links, write route, or Oracle objects as discovered evidence instead of carrying them to Phase 1.
- Phase 0 artifact lists visual/UI dependencies as required dependencies for Parte 1.
- scaffold/factory failure is used to skip `migration-plan.md`, `phase-0-execution-gate.md`, Oracle/XML/browser checks, or canonical gate criteria.

## Phase 1 - Screen Discovery

Ready for read API migration when:

- `browser-runtime.md` records runtime status, or explains why browser capture is unavailable;
- runtime evidence covers default load, filters, selected row/public key proof,
  visible action state, and a representative non-empty fixture, or records a
  deliberate blocker/accepted empty-state decision;
- `runtime-capture-form.md` exists when browser workflow is partial/missing and developer-relayed facts are required;
- `cronos-source-of-truth.md` exists when runtime XML, local XML, HADES/stored XML, or XML-export status is relevant;
- `component-lineage-matrix.md` maps each relevant component to SQL/action/object/API candidate;
- `investigation.md` identifies XML/runtime SQL, binds, views, tables, keys, filters, and related flows;
- HADES registry/access/stored-resource checks are executed or represented by a blocked SQL/helper artifact with the exact rerun path;
- candidate `api-contract.md` or component lineage identifies read endpoint candidates;
- `read-parity-matrix.md` exists and classifies every read endpoint as `Candidate`, `Implemented but needs parity`, `Parity closed`, `Deferred`, or `Blocked`;
- `closure-checklist.md` marks read gates closed;
- `java-session-context.md` exists when SQL depends on package session state;
- write surface is not unknown: it is either absent, deferred, blocked, or ready.
- `operation-inventory.md` uses deterministic states (`Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred`, `Not present`) instead of generic `Unknown`.

Accepted read-first closure labels include `Ready for read API` and `Read handoff ready; write deferred`. The latter means read discovery is closed for implementation while write and related flows remain intentionally out of scope with evidence-backed blockers.

Ready for read implementation, but not read parity closure, when:

- Java/API endpoint design is known but HTTP/API execution has not been compared to legacy runtime;
- the artifact explicitly says `Implemented but needs parity`;
- list/detail/options/filter gaps are in `read-parity-matrix.md`.

Ready for write handoff when:

- all visible write actions are listed: insert, update, delete, duplicate, save/cancel, business actions;
- XML/runtime action source is identified, such as `recordPanelEdit`, `db:*`, generated DML routine, or package call;
- candidate target tables/routines are known;
- public key and hidden key/`ROWID` strategy are described;
- payload evidence is captured or explicitly missing;
- runtime payload capture covers every write action in scope, including operation selector, hidden row locators, routine argument groups, side-effect fields, result messages, and cancel/no-op behavior;
- `write-risk.md` and `write-api-handoff.md` exist.

Blocking gaps:

- no browser/XML evidence for write actions;
- missing `cronos-source-of-truth.md` when XML source-of-truth is part of the phase evidence;
- browser workflow partial/missing without `runtime-capture-form.md`;
- browser capture only proves page load while the main fixture is empty or no
  selected-row/key/action state was observed;
- HADES registry/access blocker named without SQL/helper output or rerun artifact;
- operation status is generic `Unknown` instead of `Blocked`, `Deferred`, `Not present`, `Candidate`, `Ready`, or `Implemented`;
- Markdown evidence has unreadable mojibake for user-facing PT-BR labels and the file encoding has not been corrected;
- write action exists but no routine/table/payload evidence;
- unknown session context for SQL or routines using `FLAG_PACK`, `PACK_HADES`, or similar package state.
- read endpoint marked ready without key/filter/sort/pagination/options parity status.

## Phase 1.5 - New Platform Reuse Discovery

Ready when:

- `platform-reuse-inventory.md` exists and records executed repository searches;
- each operation/resource has one decision: `reuse`, `extend`, `create`, `block`, `defer`, or `not-api`;
- `found` and `compatible` are separated; name-similar resources are not marked `reuse` when DTO/schema/options or legacy semantics are partial;
- DTO role coverage is recorded for response DTO, FilterDTO, command DTO, option DTO/source, mapper/projection, schema, option reload, scope/authorization, and required extension;
- `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` were applied or explicitly marked not applicable with reason;
- `praxis-java-host-project` is recorded when the decision creates or extends a Java/Spring resource;
- `praxis-resource-entity-lookup-backend` is recorded when `RESOURCE_ENTITY`, `OptionSourceRegistry`, `OptionSourceDescriptor`, or `/option-sources/{sourceKey}` are in scope;
- LOV/options decisions consult `platform-option-sources.md` and `options-lov-promotion-status.md`, or record an explicit blocker to generating those inventories;
- dashboard, KPI, cockpit, aggregate, `/stats/*`, `StatsFieldRegistry`, `@UiAnalytics`, or `x-ui.analytics.projections` findings are routed to `praxis-dashboard-analytics`;
- `phase-1-5-execution-gate.md` carries the reuse decisions and the exact Fase 2 continuation.

Blocking gaps:

- no `platform-reuse-inventory.md`;
- generic `Unknown`/TBD status instead of a deterministic reuse decision;
- `Decision=reuse` while compatibility is no, partial, gap, or blocked;
- options/LOV source created or duplicated before checking common platform option sources;
- DTO/schema/options compatibility claimed without Praxis review evidence;
- dashboard/analytics surface treated as ordinary read/options without analytics gate.

## Phase 2 - Read API Migration

Ready when every implemented or ready read endpoint has:

- source component and workflow evidence;
- source SQL/view/package and bind behavior;
- stable public key strategy;
- filter semantics, including null/default/date behavior;
- authorization and company/user scope;
- authorization helper predicates are preserved or equivalently reimplemented; display permission columns alone are not accepted as visibility filtering proof;
- same-connection session context when required;
- user and company context mapping is centralized in a provider/resolver or documented project equivalent; resource services must not each hard-code production identity/company mapping;
- connection cleanup/reset strategy when package state such as `HADES.FLAG_PACK` is set on pooled connections;
- DTO/FilterDTO/option mapping;
- FieldSpec/API contract mapping for DTOs, FilterDTOs, options, `@UISchema`, `@Filterable`, and supported controls;
- pagination and ordering;
- API/backend tests when implemented, or an explicit implementation plan when only `Ready for implementation`;
- service-level tests for same-connection legacy executor usage when SQL depends on `HADES.FLAG_PACK` or equivalent package state;
- deliberate tests for read-only blocked write endpoints when generic resource controllers expose inherited create/update/delete routes;
- OpenAPI/schema/x-ui tests, or a documented planned gap when the test context cannot load them yet;
- `ui-contract-checklist.md` or equivalent section documenting control support across `lib-ui-fieldspec`;
- `read-parity-matrix.md`.
- `read-parity-results.md` once implementation or smoke testing begins.
- no read endpoint remains `Unknown`; use `Candidate`, `Implemented but needs parity`, `Parity closed`, `Deferred`, or `Blocked`.

Blocking gaps:

- endpoint derived from a view name but not from screen/component evidence;
- filters simplified without parity decision;
- session context unknown for SQL using package state;
- identity/company source is scattered across resource services instead of isolated behind replaceable mapper/resolver hooks;
- scoped read endpoint returns rows for a denied-user fixture because it exposed permission metadata instead of applying the legacy visibility predicate;
- implementation proposal assumes `JdbcTemplate` or direct JDBC before inspecting the target module/starter conventions;
- write actions ignored instead of blocked/deferred.
- API exists but has not been executed against the same user/company/scope and is described as closed instead of `Implemented but needs parity`.
- selected control exists only in Java enum but lacks OpenAPI emission or schema evidence.

Intermediate accepted Phase 2 states:

- `Implemented`: code compiles, but tests or parity evidence are still incomplete.
- `Implemented with automated backend tests`: unit/service/controller tests cover route, context bridge, filters/key lookup, and blocked writes.
- `Smoke-tested against Oracle fixture`: one live legacy-confirmed fixture was executed and recorded.
- `Verified`: automated tests and parity evidence exist; any unexecuted parity cases are explicitly deferred.

## Phase 3 - Read/Options Implementation And Parity

Ready when:

- implemented read/options endpoints match the closed Phase 2 contract;
- code/tests exist for list/filter, detail, by-ids/includeIds when used, options, schemas, and blocked writes;
- OpenAPI/schema/x-ui tests exist or are explicitly blocked by documented test-context limitations;
- at least one API/backend smoke or parity result is recorded, or the fixture blocker is explicit;
- `read-parity-results.md` records executed commands, requests, responses, and remaining read gaps;

Blocking gaps:

- API implementation differs from `api-contract.md` without re-running the FieldSpec/UI contract gate;
- writes are accidentally inherited or exposed by generic controllers;
- read/options are described as closed without tests, smoke, or a fixture blocker;
- `phase-3-execution-gate.md` is missing when the phase is classified as closed, blocked, or deferred.

## Phase 4 - Write Audit By Operation

Ready when, for every write target table:

- trigger inventory and status are confirmed from `ALL_TRIGGERS`;
- trigger source order is read from `ALL_SOURCE`;
- product package hooks are identified, including `MAIN_PRE`, `MAIN_POS`, `_PND`, generated DML, constraints, and audit;
- HADES metadata is checked for `HAD_CAD_SPROC` and `HAD_CAD_MULT_EPS`;
- active/inactive status is interpreted using `PACK_EXEC_SPROC` semantics;
- nested dependency graph is produced when Java may re-orchestrate or reimplement behavior;
- summary maps each rule to a migration decision.
- side-effect tables discovered from triggers/packages/source DML are either audited or explicitly classified as out of scope/deferred.
- each write operation has an initial route safety classification: `WRITE_TABLE_DIRECT_CANDIDATE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`.

Blocking gaps:

- target table inferred only by name, not by XML/runtime/routine evidence;
- HADES object existence treated as active without `EXEC`/`EXEC_MULT_EPS` branch analysis;
- dependency graph missing while proposing Java reimplementation.
- only the main table is audited while pending, audit, publication, association, or package DML side-effect tables remain unclassified.
- direct table/platform write is treated as safe while product/client rules, side effects, session context, error precedence, cleanup, or parity are unknown.

## Phase 5 - Write Contract By Operation

Ready for implementation when each operation has:

- `write-contract.md` with endpoint, command DTO, public key strategy, routine/table path, transaction behavior, and session context;
- command DTO and request schema metadata reviewed with `ergon-fieldspec-ui-contract`, including hidden/internal fields and copy-on-duplicate behavior;
- `write-route-decision.md` closed when more than one persistence route exists, such as generated DML procedure, direct table DML, writable view, package routine, or HADES action;
- `plsql-error-map.md` with legacy messages and API mapping;
- `write-parity-matrix.md` with success, invalid input, permission, missing row, duplicate/delete, pending, audit, and rollback cases;
- table-rule audit summaries under `oracle-results/table-rule-audit/` proving the chosen path covers every active rule for target and side-effect tables;
- explicit strategy: `legacy-routine`, `direct-table-with-triggers`, `java-reimplementation`, `blocked`, or `not-api`.
- bridge/runtime decision when same-connection package state, generated DML, or reusable error mapping is needed.
- dependency fixture plan for delete/update operations that can create association or generated-detail rows.
- final route safety state per operation: `WRITE_TABLE_DIRECT_SAFE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`.

Blocking gaps:

- operation-level payload not known;
- runtime payload capture missing for an operation that Phase 3 intends to design;
- no parity cases for side effects;
- no cleanup path for controlled write fixtures that create side-effect rows;
- chosen Java path does not cover active table rules.
- multiple write routes exist but no route is marked `Chosen` with evidence in `write-route-decision.md`.
- operation status is `Unknown`; use `Ready for audit`, `Ready for write design`, `Blocked`, `Deferred`, or `Not API` instead.
- operation is `WRITE_TABLE_DIRECT_CANDIDATE` but Phase 6 implementation is being proposed; only `WRITE_TABLE_DIRECT_SAFE` can authorize direct platform/table write.

## Phase 6 - Java Implementation of Approved Operations

Ready when:

- implementation target package/resource is known;
- existing read DTO/resource/service wiring is reviewed;
- OpenAPI/x-ui schema impact is known and covered by FieldSpec/API contract checks;
- same-connection Oracle session context is implemented if required;
- legacy user/company mapping is reused from the shared provider/resolver used by read APIs, or the deviation is documented;
- shared legacy bridge is used or explicitly rejected when writes require package state/error translation;
- unsupported write operations still return deliberate blocked behavior.

Blocking gaps:

- direct CRUD chosen because framework supports it, not because legacy behavior was closed;
- `ROWID` exposed publicly without explicit decision;
- session state set outside the transaction connection.

## Phase 7 - Quality Round 2

Ready for Phase 8 when:

- the authenticated legacy screen is operated for the representative cases in scope;
- each executed legacy filter/selection/action has an equivalent HTTP request recorded for the new API;
- `quality-round-2.md` records legacy steps, HTTP requests, statuses, row counts, ids/keys, visible fields, labels, ordering, pagination, empty state, and messages;
- browser screenshots, API request/response payloads, and console/network evidence are linked;
- all divergences are classified as `bug`, `accepted gap`, `deferred`, `fixture issue`, or `legacy-only`;
- blocked/deferred actions remain not callable;
- `phase-7-execution-gate.md` is created or updated.

Ready for Phase 8 with adjustments when:

- the declared Phase 7 scope passes;
- non-blocking residuals have owner, classification, and next action;
- any unexecuted mutable cases are explicitly deferred due to fixture/cleanup constraints;
- related read-only gaps are not promoted to full parity.

Blocking gaps:

- no authenticated legacy evidence exists for the cases being claimed;
- API output diverges from visible legacy behavior without explicit accepted gap;
- a blocked/deferred action is callable;
- full parity is claimed while a planning artifact such as `phase-7-*-plan.md` is still the latest phase state;
- `quality-round-2.md` or `phase-7-execution-gate.md` is missing.

## Phase 8 - Final Parity And Handoff

Ready for deployment recommendation when:

- Phase 7 is closed for the current user-facing scope or any open Phase 7 work is explicitly outside the release scope;
- API tests pass;
- OpenAPI/schema tests pass;
- database side-effect checks pass;
- dependency blockers and fixture cleanup checks pass for write operations that can delete/update rows with children;
- parity matrix is executed or any unexecuted case is explicitly deferred;
- residual risks are documented with owner, classification, and next action;
- `parity-results.md`, `backend-api-handoff.md` or scoped `pilot-handoff.md` according to delivery mode, and `phase-8-execution-gate.md` exist.

Ready for handoff with adjustments when:

- the release scope is functional and safe;
- non-blocking residuals are accepted, owned, and carried into handoff;
- partial related read-only flows are clearly named and not promoted to full parity.

Blocking gaps:

- write side effects, dependency blockers, or cleanup evidence are missing for implemented write actions;
- related flows are promoted to full parity from a parent-screen accepted gap;
- residual risks lack owner, accepted/deferred state, or next action;
- `phase-8-execution-gate.md` is missing.

## UI Track - Native Praxis UI Wiring

Ready when:

- backend handoff names the resource/API scope, read/write operation states, schema endpoints, option sources, capabilities, actions, surfaces, HATEOAS links, and residual platform gaps;
- `ergon-angular-ui-screen-wiring` was selected as the execution skill;
- `ui-api-readiness.md`, `ui-dto-contract-review.md`, `ui-translation-map.md`, `ui-implementation-plan.md`, `ui-visual-qa.md`, and `ui-execution-gate.md` exist or are deliberately scoped with explicit blockers;
- `ui-implementation-plan.md` includes a native Praxis source audit across `@praxisui/core`, `@praxisui/crud`, `@praxisui/table`, `@praxisui/dynamic-form`, and `@praxisui/dynamic-fields`;
- every proposed UI improvement is classified as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`;
- the implementation consumes canonical `/schemas/filtered`, capabilities, actions, surfaces, HATEOAS links, option sources, and selected-value reload where applicable;
- local tests or browser QA prove the selected UI scope, or the missing authenticated fixture/browser blocker is explicit.

Blocking gaps:

- UI introduces a local action, surface, drawer, lookup, table, form, command router, or option-source runtime for a concept already owned by `@praxisui/*`;
- action/surface/tab/lookup/command intent is routed by labels, regex, XML names, aliases, or keyword lists instead of canonical metadata and declared tools;
- backend/schema/option/write gaps are patched in Angular instead of returning to the owning backend/API phase;
- visual QA is claimed without executed screenshot/browser evidence or an explicit blocker.

## Dashboard Track - Praxis Analytics And Charts

Ready when:

- `ergon-dashboard-praxis-charts` and `praxis-dashboard-analytics` are selected for dashboard/KPI/cockpit/chart work;
- metric ownership is classified as canonical analytics projection, governed aggregate resource, custom dashboard endpoint, blocked, or platform follow-up;
- chart UI consumes governed metadata and runtime contracts rather than hardcoded metric vocabulary in the host screen;
- filters, query context, capability protection, and option sources are mapped to canonical Praxis resources.

Blocking gaps:

- chart semantics are embedded in Angular configuration while a backend analytics or aggregate contract is required;
- metrics are inferred from labels or XML names without canonical resource/field/analytics grounding;
- protected metrics ignore capabilities, scope, or company/user context.

## Rule Migration Parte 2 Gate

Ready when:

- `ergon-rule-migration-orchestration` is selected and the relevant Parte 1 baseline is closed with `phase-8-execution-gate.md`, `backend-api-handoff.md` or scoped `pilot-handoff.md`, and explicit residuals;
- Phase 4/5 table-rule evidence, HADES findings, read/write operation inventory, route safety states, and parity status are available for the rule scope;
- missing API/write/UI evidence is returned to the exact Parte 1 phase that owns it before rule extraction or promotion;
- shadow mode, preflight, promotion, rollback, and legacy containment are planned as governed rule-migration artifacts.

Blocking gaps:

- Parte 2 starts from table names or source snippets without a closed Parte 1 baseline;
- HADES or table-rule chains are unknown but rule promotion is proposed;
- shadow-mode or preflight evidence is skipped for a behavior that can alter production decisions.
