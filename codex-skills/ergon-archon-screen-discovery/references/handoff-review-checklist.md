# Screen Discovery Handoff Review Checklist

Use this before handing an investigation to the implementation team.

## Evidence

- [ ] Fase 0 entry is valid: `migration-plan.md` exists, `phase-0-execution-gate.md` recommends `ergon-archon-screen-discovery`, and the screen code/scope are explicit.
- [ ] `phase-1-execution-gate.md` exists; a `.prelim.md` draft alone is not treated as handoff-ready.
- [ ] The discovery mode is stated as Quick discovery, Full discovery, or API migration, with unavailable evidence sources marked Blocked, Partial, Missing, or Not applicable.
- [ ] Screen code, title, module, navigation path, and final URL are recorded.
- [ ] Browser status is marked as Complete, Partial, or Missing.
- [ ] The page was found through the menu/search field when browser access was available.
- [ ] `browser-runtime.md` exists for assisted Codex-browser sessions and contains only sanitized runtime notes.
- [ ] `runtime-capture-form.md` exists when the browser workflow is Partial or Missing and the developer must relay runtime facts.
- [ ] `runtime-parity-workbook.md` and `factory/runtime-parity-workbook.json` exist, are current for the latest browser/Oracle run, and classify binds, filter payloads, option payloads, public key, allowed/default context, and bridge security contract as executed or blocked.
- [ ] `phase1-corporate-baseline.md` and `factory/phase1-corporate-baseline.json` exist when the migration factory is available and list only the remaining fixture, runtime bind, public key, and allowed/default context actions.
- [ ] `phase1-scope-authorization-decision-pack.md` and `factory/phase1-scope-authorization-decision-pack.json` exist only when scope/authorization cases remain genuinely open because of bridge bypass, custom security, or unresolved allowed/default context, with owner decision templates and sanitized evidence references only.
- [ ] `public-key-correlation.md` and `factory/public-key-correlation.json` exist, and any `blocked_*` status keeps the Phase 1 gate blocked.
- [ ] `cronos-source-of-truth.md` exists when runtime XML, local XML, HADES/stored XML, or XML-export status is part of the package.
- [ ] Local/runtime XML differences are classified in `cronos-source-of-truth.md` as matched, divergent, blocked, forbidden, not found, or local-only unconfirmed.
- [ ] `legacy-doc-sources.md` exists when `docs-legado/v7x` is available, with documentation facts separated from implementation evidence.
- [ ] The searched documentation layers are named explicitly: `java`, `aps`, `EA`, `help`, `docs/Interno`, `workflow`, `forms`, `reports`, `web`/portal, and customizations when relevant.
- [ ] No documentation-only fact is promoted to API readiness unless it is tied to browser/runtime, XML/debug, local source, Oracle metadata, or an accepted deferral.
- [ ] `component-lineage-matrix.md` maps each relevant XML/debug component to functional role, SQL/action/link, binds/hidden keys, API translation, resource/endpoint candidate, DTO/FilterDTO/OptionDTO/CommandDTO impact, readiness, and blocking checks.
- [ ] Layout-only/static components are marked `Not API`; the package does not create one endpoint per visual component.
- [ ] `closure-checklist.md` states whether the screen is Open, Ready for read API, Ready for write API, or Deferred.
- [ ] Local XML/source files inspected are listed with paths.
- [ ] Main screen SQL and `sqlParameters` are captured from XML/debug/runtime.
- [ ] Related flows, tabs, links, popups, and hidden fields are represented or explicitly skipped.

## Oracle

- [ ] Oracle seed objects are derived from browser/XML/runtime evidence.
- [ ] HADES registry/access/stored-resource SQL or helper output exists, or a blocked artifact tells the next developer exactly what to run.
- [ ] Synonyms are resolved or marked pending.
- [ ] Screen views are expanded to physical tables or marked pending.
- [ ] Columns, constraints, indexes, grants, packages, triggers, and updatable views are checked or marked not applicable.
- [ ] Oracle confirmation SQL exists and states whether it was executed.
- [ ] Public key correlation SQL/output exists when Oracle is available, or the package contains a blocked artifact with the exact retry command/cause.
- [ ] No credentials or sensitive row dumps are present in generated artifacts.

## API Migration

- [ ] `closure-checklist.md` supports the requested API scope before implementation starts.
- [ ] Each endpoint is marked Required Now, Candidate, Blocked, Deferred, or Not API.
- [ ] No endpoint is Required Now while keys, allowed/default context, bridge routing, session context, source confidence, runtime behavior, parity cases, or write behavior is unresolved.
- [ ] API ids, `GET /{id}`, `by-ids`, DTO ids, and option ids do not expose `ROWID`, `ROWID_REG`, `P_ROWID_REG`, package state, or hidden technical keys unless a later gate explicitly approves that exception.
- [ ] DTO fields include source column, type, nullability, conversion, and confidence.
- [ ] `ROWID` is rejected or explicitly justified for public API exposure.
- [ ] Company/user scope and special values are documented.
- [ ] Scope/authorization follows `docs/migracao/phase1-scope-authorization-standard.md`: allowed-default may close only with authenticated browser plus same-connection Oracle context; company-scoped and restricted-user close by the shared bridge/security contract for API-only screens unless a bypass/custom security route is detected.
- [ ] Open company-scoped or restricted-user cases are routed through the scope/authorization decision pack only when they are genuine bypass/custom-security blockers; the package does not mark the gate Ready by itself.
- [ ] Company/user/profile/session context is not exposed as public FilterDTO, schema, URL, option payload, or x-ui fields.
- [ ] List endpoints document pagination, default sort, deterministic tie-breaker, filters, and total-count strategy.
- [ ] Capability/button state is mapped or explicitly left out of the API.
- [ ] Java same-connection session context is checked when SQL/packages depend on session package state.
- [ ] Parity cases cover default list, filters, allowed/default context, related flows, empty results, and access failures; company/restricted parity may be covered by the shared bridge unless a screen-specific bypass is detected.
- [ ] `lib-ui-fieldspec` contract is documented: `AbstractResourceController`, `BaseResourceService`, DTO, FilterDTO, ID type, `@UISchema`, standard endpoint enablement, options endpoints, schemas, `RestApiResponse`, and HTTP examples.
- [ ] Target application wiring is documented: `ApiEndpoints.java`, `SwaggerConfig.java`, `application.yaml`, existing resources reused/updated, and tests/scripts impacted.
- [ ] PT-BR labels/descriptions in `@UISchema`/`@Schema` were reviewed for accents, terminology, hidden/internal fields, and UI impact.

## Handoff

- [ ] Findings separate confirmed evidence from candidates.
- [ ] `operation-inventory.md` uses deterministic states only: Implemented, Ready, Candidate, Blocked, Deferred, or Not present.
- [ ] Markdown artifacts preserve readable UTF-8 PT-BR labels; no mojibake such as `CÃ³digos`, `DescriÃ§Ã£o`, or replacement characters.
- [ ] False positives and rejected candidates are recorded.
- [ ] Every ambiguity has one concrete next check.
- [ ] Browser, XML/source, Oracle, and API gates are complete, partial, missing, blocked, or not applicable.
