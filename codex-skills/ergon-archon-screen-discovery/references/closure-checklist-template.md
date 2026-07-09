# Screen Closure Checklist Template

Use this checklist before moving a legacy screen investigation into API implementation. A screen is not API-ready while any required item is unchecked or explicitly blocked.

## Closure Status

- Screen:
- Closure owner:
- Last updated:
- Overall status: `Open` / `Blocked` / `Ready for read API` / `Read handoff ready; write deferred` / `Ready for write API` / `Deferred`
- Decision summary:

Use `Open` only while the discovery is still in progress and no execution gate has been closed. If `phase-1-execution-gate.md` is `Blocked`, this checklist must also say `Blocked` and point to the same blockers.

## Runtime

- [ ] Final URL, title, module, and navigation/menu search path are confirmed.
- [ ] `browser-runtime.md` is filled with sanitized runtime notes.
- [ ] `runtime-capture-form.md` exists when browser workflow is partial/missing or developer-relayed facts are required.
- [ ] Required context selectors are exercised, such as servidor, vinculo, empresa, or profile.
- [ ] Main grid/list loads with observed default values.
- [ ] Runtime bind values are captured or explicitly marked unavailable.
- [ ] Pagination, sorting, visible columns, hidden key fields, and row selection are documented.
- [ ] Selected-row correlation records both public API key and any internal legacy row locator such as `ROWID_REG`, with exposure decision.
- [ ] Visible action state is captured for create, edit, delete, save, cancel, links, and popups.
- [ ] Runtime/debug SQL or XML is captured when available, or absence of debug access is documented.

## XML And Component Lineage

- [ ] Local XML or runtime XML/debug source is located.
- [ ] `cronos-source-of-truth.md` exists when runtime XML, local XML, HADES/stored XML, or XML-export status is relevant.
- [ ] Local/runtime/HADES XML comparison is classified as matched, divergent, blocked, forbidden, not found, or local-only unconfirmed.
- [ ] `sqlSelect`, `sqlParameters`, lookup SQLs, links, hidden fields, and action metadata are extracted.
- [ ] `component-lineage-matrix.md` covers every API-relevant block, grid, filter, lookup, detail, tab, action, context/capability item, and related screen.
- [ ] Each relevant component has a functional role, API translation, endpoint/resource or `Not API` decision, DTO/FilterDTO/OptionDTO/CommandDTO impact, status, and blocking check.
- [ ] Pure layout/static labels/containers are marked `Not API` and are not used to create endpoints.
- [ ] Each matrix row has readiness and a concrete blocking check.
- [ ] Related flows are represented or explicitly scoped out.

## HADES Registry And Stored Definition

- [ ] HADES transaction/access registry is checked.
- [ ] HADES registry/access/stored-resource SQL or helper output exists; if blocked, the package has an exact rerun command/artifact.
- [ ] Create/edit/delete access flags are recorded separately from browser-visible button state.
- [ ] Stored XML/resource discovery is run or explicitly skipped with reason.
- [ ] Any HADES text/BLOB hits are summarized without dumping sensitive content.

## Oracle Metadata

- [ ] Oracle confirmation SQL has been generated and executed by Codex when access is available.
- [ ] Referenced Oracle outputs were scanned for `ORA-`, `SP2-`, `TNS-`, `ERROR:`, `Exception`, and `IllegalArgumentException`; any failure is corrected/rerun or explicitly recorded as a blocker/residual.
- [ ] Seed objects are derived from XML/runtime/component matrix, not broad naming guesses.
- [ ] Synonyms are resolved.
- [ ] Views are expanded to physical tables and helpers.
- [ ] Columns, constraints, indexes, defaults, grants, triggers, and package/function arguments are checked.
- [ ] Source search is narrow and covers write-risk objects separately.
- [ ] False positives and rejected candidates are recorded.

## Keys And API Boundary

- [ ] Public key strategy is decided for list/detail endpoints.
- [ ] `ROWID` exposure is rejected or explicitly justified.
- [ ] Internal legacy locators such as `ROWID_REG`, XML hidden ids, and row-level action fields are kept out of public API unless a later write contract explicitly accepts them.
- [ ] Stable unique key evidence is attached for the chosen key.
- [ ] Path/query parameters are mapped from runtime/XML binds.
- [ ] DTO fields have source, type, nullability, conversion, and confidence.
- [ ] Endpoint statuses are assigned: `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`.
- [ ] `operation-inventory.md` uses deterministic operation states only: `Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred`, or `Not present`.
- [ ] Main-grid/list endpoints have pagination, default sort, tie-breaker, filters, and total-count strategy.
- [ ] Lookup endpoints are separated from main-list endpoints when they have different sources or scope rules.
- [ ] Capability/action state is either exposed deliberately by the API or kept out of scope with evidence.
- [ ] Parity cases exist for every `Required Now` endpoint.

## Read Parity

- [ ] `read-parity-matrix.md` exists and covers every read endpoint candidate in the current slice.
- [ ] Default list load has legacy runtime/Oracle evidence: current selectors, page size, visible columns, default sort, and row count or representative rows.
- [ ] API/HTTP parity is executed when Java code already exists; otherwise the matrix marks the endpoint as `Implemented but needs parity`, not closed.
- [ ] Every visible filter/search field has bind behavior, null/default behavior, and an API filter mapping or explicit deferral.
- [ ] Pagination and ordering are compared against the legacy screen, including deterministic tie-breaker when the legacy order is not unique.
- [ ] Detail endpoint key strategy is tested with a selected row and does not rely on public `ROWID` unless explicitly approved.
- [ ] Options/lookup endpoints are tested for value, label, ordering, search, and by-ids rehydration when the migrated UI will use them.
- [ ] Related tabs, popups, and links are either covered by read parity or explicitly deferred with owner phase/skill.
- [ ] Authorization and scope cases exist for current user/company/profile, special values, and denied access when applicable.
- [ ] Residual read gaps are listed as blockers or accepted deferrals before moving to read API implementation.

## lib-ui-fieldspec API Contract

- [ ] `lib-ui-fieldspec` local docs were checked before API design.
- [ ] Target application integration points were checked, including `ApiEndpoints.java`, `SwaggerConfig.java`, `application.yaml`, existing DTOs/FilterDTOs/services/controllers, and test scripts.
- [ ] Resource path, controller base, service base, DTO, FilterDTO, and ID type are decided.
- [ ] `AbstractResourceController` / `BaseResourceService` is used, or deviation is justified.
- [ ] `ApiEndpoints.java` has path/group/tag constants or the existing resource constants are reused.
- [ ] `SwaggerConfig.java` has a `GroupedOpenApi` for the resource or an existing group covers it.
- [ ] `POST /filter`, `/options/*`, `/by-ids`, `/schemas`, cursor, locate, stats, and write endpoints are individually enabled, blocked, deferred, or left as `501`.
- [ ] `@UISchema` requirements are documented for grid, form, filter, read-only, hidden, numeric/date, select, and option fields.
- [ ] PT-BR labels/descriptions preserve accents and user-facing terminology from the legacy screen.
- [ ] Markdown artifacts are UTF-8 readable and do not contain mojibake for user-facing labels.
- [ ] Specialized controls are verified in `lib-ui-fieldspec` before API handoff.
- [ ] Date interval filters use an explicit range control decision, such as `FieldControlType.DATE_RANGE`, after backend schema support is confirmed and the backend predicate is mapped.
- [ ] Numeric or non-date range controls, such as `rangeSlider`, are used only after backend schema support is confirmed.
- [ ] Every dynamic filter has backend implementation details, not only generated schema metadata.
- [ ] Dependent selects have both `@UISchema` dependency metadata and service-side enforcement.
- [ ] Business validations are assigned to service/domain/legacy routine; DTO annotations are not the only validation layer.
- [ ] `OptionDTO` endpoints use `valueField` / `displayField` semantics.
- [ ] `RestApiResponse` envelope and optional unwrap behavior are decided.
- [ ] `X-Data-Version` is implemented or explicitly not supported.
- [ ] HTTP examples or tests cover FieldSpec standard endpoints required by the slice.
- [ ] OpenAPI/x-ui assertions are updated when annotations or endpoint schemas change.

## Authorization And Scope

- [ ] Current user/session source is understood.
- [ ] Current company/profile/transaction context is understood.
- [ ] Oracle package state dependencies are identified, such as `FLAG_PACK`.
- [ ] Java same-connection context setup strategy is documented when package state is used.
- [ ] Java same-connection context cleanup/reset policy is documented when package state is used.
- [ ] API identity-to-legacy-user mapping is decided or explicitly blocked.
- [ ] Connection-pool cleanup/reset policy is decided or explicitly blocked.
- [ ] Screen-specific security helpers are mapped.
- [ ] Special values such as `-1`, `-2`, null, empty string, and default dates are documented.
- [ ] Authorization parity cases are defined.

## Write Behavior

- [ ] Write actions are classified as in scope, blocked, or out of scope.
- [ ] `write-risk.md` exists when any write-like UI action or related write flow exists.
- [ ] `write-risk-detail.sql` is generated from XML/runtime seed objects and executed when Oracle access is available.
- [ ] DML routines, table triggers, package hooks, grants, defaults, and validation messages are reviewed.
- [ ] Insert, update, delete, duplicate, pending-record, publication, and legal-document side effects are documented.
- [ ] Write parity cases are defined, or write APIs are explicitly deferred.
- [ ] `write-api-handoff.md` exists when the screen is `Ready for read API` or `Read-first API implemented` and write remains blocked/deferred.
- [ ] `write-api-handoff.md` states whether the next phase is `Legacy-backed Write API candidate`, `Blocked`, or `Not suitable`, and uses `Not captured`/`Blocked` instead of generic `Unknown` for missing payload or route evidence.
- [ ] `write-api-handoff.md` lists exact blockers and next Oracle/runtime checks for the future write skill.

## Final Decision

| Area | Status | Evidence | Remaining Blocker |
| --- | --- | --- | --- |
| Runtime |  |  |  |
| XML/component matrix |  |  |  |
| HADES registry/stored definition |  |  |  |
| Oracle metadata |  |  |  |
| Key strategy |  |  |  |
| Authorization/scope |  |  |  |
| Java session context |  |  |  |
| Read API readiness |  |  |  |
| Read parity |  |  |  |
| Write API readiness |  |  |  |
| Related flows |  |  |  |
