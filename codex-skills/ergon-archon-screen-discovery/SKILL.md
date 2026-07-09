---
name: ergon-archon-screen-discovery
description: Investigate legacy Ergon/Archon screens for Oracle lineage and Java API migration. Use when Codex needs to map screens such as ERGadm00033 or ERGadm00034, debug/XML components, sqlSelect/sqlParameters, related flows, Oracle views, physical tables, synonyms, dependencies, packages, triggers, permissions, DTOs, parity tests, or a minimal backend API contract.
---

# Ergon Archon Screen Discovery

Use this skill to turn an exploratory Ergon/Archon screen investigation into a reproducible migration package. Prefer evidence-backed conclusions over naming conventions. When coordinating a multi-phase migration, use `ergon-migration-orchestration` first to verify phase gates and artifact handoff.

For developer onboarding and day-to-day execution, use [developer-quickstart.md](references/developer-quickstart.md). For repeatable starts, use [prompt-template.md](references/prompt-template.md). For didactic PT-BR user guidance and ready-to-use prompts by reading/discovery scenario, use [read-prompt-examples.md](references/read-prompt-examples.md). For team handoff review, use [handoff-review-checklist.md](references/handoff-review-checklist.md). For database access provisioning, use [codex-oracle-access.md](references/codex-oracle-access.md). For authenticated browser-session capture, use [codex-browser-runtime-capture.md](references/codex-browser-runtime-capture.md) and [runtime-capture-form-template.md](references/runtime-capture-form-template.md). For Cronos XML source-of-truth decisions, use [cronos-source-of-truth-template.md](references/cronos-source-of-truth-template.md). For legacy documentation discovery, use [legacy-docs-discovery.md](references/legacy-docs-discovery.md). For component-to-API inventory, use [component-lineage-matrix-template.md](references/component-lineage-matrix-template.md). For read endpoint parity gates, use [read-parity-matrix-template.md](references/read-parity-matrix-template.md). For Java/API package-state parity, use [java-oracle-session-context.md](references/java-oracle-session-context.md). For API endpoint design, use [api-design-patterns.md](references/api-design-patterns.md), [lib-ui-fieldspec-api.md](references/lib-ui-fieldspec-api.md), and [java-api-implementation-playbook.md](references/java-api-implementation-playbook.md). For a filled read-first frequency API model, use [example-ergadm00189-api-contract.md](references/example-ergadm00189-api-contract.md). For architecture-level write patterns, use [archon-write-patterns.md](references/archon-write-patterns.md). For write behavior and write deferral, use [write-risk-template.md](references/write-risk-template.md), [write-risk-detail-template.sql](references/write-risk-detail-template.sql), and [write-api-handoff-template.md](references/write-api-handoff-template.md). For deciding whether a screen can move to API implementation, use [closure-checklist-template.md](references/closure-checklist-template.md).

## Platform Governance

Apply the root migration `AGENTS.md` while producing discovery artifacts. The
screen discovery phase must identify whether a finding belongs to the Ergon
host, `praxis-metadata-starter`, `praxis-config-starter`, `praxis-ui-angular`,
or another owner.

When discovery finds missing or weak support for `_links`, `/actions`,
`/surfaces`, `/capabilities`, `/schemas/filtered`, `x-ui`, option sources, or
Angular runtime behavior, do not prescribe an Ergon-local workaround as the
default. First classify the need as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Only real contract
gaps should become `Praxis Platform Follow-up`.

Keep HADES, SQL, `ROWID`, empresa, usuario, perfil, package names, and session
context as evidence for backend implementation, not public DTO/schema/URL/x-ui
contract.

## Operating Principle

Investigate in this order unless the user gives a stronger reason to change it:

1. Open the legacy screen and observe the actual user workflow.
2. Find the Archon XML/debug definition for the same screen.
3. Extract screen SQL, component names, bind tokens, links, filters, page size, hidden fields, and default values from browser/XML evidence.
4. Use the extracted SQL objects as the seed list for Oracle metadata discovery.
5. Expand Oracle lineage, security, grants, triggers, keys, and write risks only after the screen evidence is anchored.
6. Close write behavior as either API-ready or explicitly blocked/deferred with evidence before claiming read/API readiness.

Do not start from broad Oracle scans or name matching when browser/XML evidence is available. The screen XML and runtime SQL are the primary evidence for what the user-facing workflow actually uses.

## Standard Operation Inventory

Every Ergon/Archon screen discovery must produce or update `operation-inventory.md`. Start from the standard framework operations and then mark each one with one of the allowed states: `Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred`, or `Not present`.

- `Consultar/listar`: default load, visible filters, pagination, sorting, company/user scope, empty state.
- `Ler detalhe`: row selection, detail form/panel, nested grids, public key, internal locators.
- `Novo/Salvar`: create button, edit state, defaults, required fields, validation messages, `P_OPER`/routine/table route, success side effects.
- `Editar/Salvar`: editable fields, immutable keys, changed-field payload, validation messages, side effects.
- `Apagar`: delete/anulation button, confirmation text, permission and dependency blockers.
- `Duplicar`: copied/defaulted values, new key fields, whether it reuses create route.
- `Cancelar`: no-op behavior from create/edit/duplicate modes.
- `Documentos legais`: tab/block/component, read source, write route when editable, `PONTLEI` or equivalent link key.
- `Publicacoes/atos`, `Pendencias`, and other related framework blocks when visible in XML, browser, or table-rule side effects.

For each row, record: browser evidence, XML/component evidence, Oracle/source evidence, candidate endpoint, FieldSpec/platform mapping, current backend state, parity state, and exact next check. Do not collapse `Novo`, `Editar`, `Apagar`, `Duplicar`, and `Documentos legais` into a generic "writes pending" note.

Use this FieldSpec mapping baseline when filling `operation-inventory.md`:

- `Consultar/listar`: `POST /<resource>/filter` backed by `BaseResourceService.filterWithIncludeIds`.
- `Ler detalhe`: `GET /<resource>/{id}` backed by `BaseResourceService.findById`; `GET /by-ids` when the UI needs selected-row reloads.
- Lookups/options: `POST /options/filter`, `GET /options/by-ids`, `OptionDTO`, and `@UISchema(endpoint/filterField/sortField/optionsPageSize)`.
- `Novo/Salvar`: `POST /<resource>` backed by `save` only after write gates close; otherwise blocked/deferred.
- `Editar/Salvar`: `PUT /<resource>/{id}` backed by `update` only after update payload and side effects close.
- `Apagar`: `DELETE /<resource>/{id}` backed by `deleteById`; batch delete is a separate explicit decision.
- `Duplicar`: `POST /<resource>/{id}/duplicate-draft` through `DuplicateDraftResourceService.duplicateDraft`, then normal create on save.
- `Cancelar`: no backend mutation; prove UI state reset/no write.
- `Documentos legais`, `Publicacoes/atos`, and `Pendencias`: separate related resources/workflows unless runtime/XML proves they are fields of the main resource.

For Ergon screens that depend on `HADES.FLAG_PACK`, note that the FieldSpec endpoint shape stays standard while implementation must run context setup/cleanup on the same Oracle connection through the shared legacy bridge.

## New Platform Reuse Discovery

After the legacy operation inventory is anchored, search the target Java/OMS modules before creating new API candidates. Produce `platform-reuse-inventory.md` with one row per operation/resource and a decision: `reuse`, `extend`, `create`, `block`, `defer`, or `not-api`.

Inspect at minimum:

- endpoint/path constants and OpenAPI groups;
- controllers, resource services, DTOs, FilterDTOs, mappers, repositories, entities, and tests;
- resources already migrated for related screens or shared lookups/options;
- `docs/migracao/platform-option-sources.md` generated by `tools/migration-factory/export-platform-option-sources.ps1 -Force` when the workspace has that helper, plus `docs/migracao/options-lov-promotion-status.md`, before treating a LOV/option as new or blocked; record `generatedAt`, covered property files/modules, and promotion status source so a missing source is not inferred from stale or incomplete coverage;
- shared services for legacy context, authorization, legal documents, publications, pending flows, and FieldSpec schemas;
- semantic gaps between the existing new-platform resource and the legacy screen behavior.

If an existing resource matches the legacy operation, record the exact path/class and prefer reuse or extension. Do not propose a duplicate endpoint unless the incompatibility is explicit.
For LOV/options, record `PLATFORM_OPTION_SOURCE_RESOLVED` when sourceKey, dependencies, selected-value reload, and visible semantics match; `PLATFORM_OPTION_SOURCE_REVIEW_REQUIRED` when an existing source is close but semantically incomplete; and `PLATFORM_OPTION_SOURCE_BACKLOG_REQUIRED` only when no configured/promoted source fits and the target microservice/module was covered by the inventory. Treat review-required as an `extend` decision by default; use `block` only when the gap prevents the current screen contract.

## Phase Boundary

Use this as phases 1 and 1.5 of the migration:

1. `ergon-archon-screen-discovery` discovers and closes the screen boundary: browser workflow, XML/runtime SQL, Oracle lineage, keys, scope, authorization, read API candidates, and write risk/handoff.
2. It may produce a candidate read API contract, but `ergon-archon-read-api-migration` owns final read API design/implementation.
3. Write endpoints remain `Blocked` or `Deferred` unless write behavior is fully closed.
4. When write remains blocked/deferred, create `write-risk.md` and `write-api-handoff.md` so `ergon-archon-write-api-migration` can run after the read API phase.
5. Before leaving phase 1, close the screen's write surface: visible actions, XML/runtime action source, candidate routines/tables, payload evidence or explicit gap, key/ROWID strategy, session context, and blockers.
6. Before handing off to `ergon-archon-read-api-migration`, create `read-parity-matrix.md` from [read-parity-matrix-template.md](references/read-parity-matrix-template.md). Do not mark the read phase as closed if list/detail/options/related read endpoints lack explicit parity status and gaps.
7. Before handing off to read/write API skills, produce `platform-reuse-inventory.md` or mark reuse discovery blocked with exact missing repository/module access.
8. Use `ergon-table-rule-audit` only for table-level write-rule closure, normally after the read API phase and after target tables are known.

If the user asks for write implementation before these artifacts exist, keep the work in discovery mode and close the missing handoff evidence first.

## Legacy System Access

Default demo entry point:

- `http://ergon-demo-644.techne.com.br/Ergon/Administracao/ERGadm_mnu001.tp`

Use the authenticated browser surface that actually has the session. Prefer the Codex in-app browser when the user has it open or can log in interactively. Use Chrome when the user asks for Chrome, the authenticated session is already in Chrome, or the user's profile/extensions are needed. Use Playwright only as a fallback for repeatable screenshots or scripted smoke checks after the browser-session path is understood.

Legacy Archon pages can have unstable DOM locators. If DOM inspection hangs or returns unreliable results, use screenshots plus coordinate/CUA-style actions to operate the page, and record the limitation in `browser-runtime.md`. Do not downgrade confirmed visible behavior just because DOM automation is weak.

If credentials are provided in the conversation, use them only for the active private session, but do not write them into reports, SQL files, commits, logs, screenshots, command history artifacts, or generated files. If credentials need to be reused locally, prefer environment variables or a private password manager outside the repository.

After login:

1. Confirm the authenticated Home/Menu screen: visible user, visible company, current URL path, and current menu transaction.
2. Click or focus the search field labeled like `Buscar transacao`.
3. Search for the target page code first, for example `ERGadm00033`, `ERGadm00034`, or `ERGadm00189`. Search by visible title only if the code does not return a result.
4. Open the matched page from the search result instead of guessing the final URL.
5. Record the selected result text, navigation path, visible title, module/breadcrumb, and final URL path.
6. Exercise the visible workflow: default load, company selector, search/filter fields, tabs, links, action buttons, pagination, and detail navigation.
7. Capture observed parameters and changed SQL behavior after each interaction.

If the search does not find the transaction, try the visible menu/area path and record each clicked label. If neither search nor menu opens the screen, mark navigation as `Blocked - screen not reachable for current user`.

If login or browser access is unavailable, continue from local XML/source and mark `Observed` as `Missing` or `Partial` in the gates.

## Runtime XML Export Gate

For Cronos/Archon `.tp` transactions, always try the matching `.xml` runtime export before treating local XML as final:

```text
/<Application>/<Module>/<Transaction>.xml
```

Example: `http://ergon-demo-644.techne.com.br/Ergon/Administracao/ERGadm00034.xml`.

This route is handled by Cronos export code, requires an authenticated user with layout-export permission (`privilegiado` or `alteraLayout`), retrieves the runtime descriptor, and serializes it through `TransactionXmlWriter`. It is not merely a static file read.

If `tools/migration-factory/download-runtime-xml.ps1` exists in the repository, run it before any manual extraction from the browser viewer. It is the preferred path because it saves the raw response only after XML parser validation and writes sanitized evidence. Pass credentials only through a pre-created `PSCredential` or pre-existing env vars; do not put secrets in the command.

Required behavior:

1. Use credentials only for the active private session; never write them to artifacts, logs, SQL, commits, screenshots, command history, or prompt templates.
2. Open the `.tp` route to prove the runtime screen is reachable for the current user.
3. Download the `.xml` route for the same application/module/transaction. If browser JavaScript cannot read `HttpOnly` cookies or lacks `fetch`/`XMLHttpRequest`, do not stop there: when the login page exposes a form, parse the actual `<form action>` and resolve it against the response URL. Example: `action="/login"` under `/Ergon/Administracao/<SCREEN>.tp` resolves to `http://host/login`, not `/Ergon/login`. Use an in-memory HTTP session/cookie container to request `.tp`, submit the resolved login action with the observed form fields, then request `.xml`. Keep credentials and cookies only in memory.
4. Save the exported XML under `docs/migracao/<SCREEN>/runtime/<SCREEN>.authenticated.xml` or `docs/migracao/<SCREEN>/runtime-exported-xml/<SCREEN>.xml` only when it contains no credentials or sensitive runtime data beyond screen metadata and the saved file parses as XML.
5. Record URL, HTTP status, redirect/login status, content type, byte size, SHA-256 hash, parser result, timestamp, and non-sensitive user/session context.
6. Compare exported XML against local product XML under `docs-legado/**/crodata/trans/<Module>/<Transaction>.xml`.
7. Produce or update `cronos-source-of-truth.md` with one of: `RUNTIME_EXPORTED_XML_MATCH`, `RUNTIME_EXPORTED_XML_DIVERGED_FROM_LOCAL`, `RUNTIME_XML_EXPORT_FORBIDDEN`, `RUNTIME_XML_EXPORT_AUTH_BLOCKED`, `RUNTIME_XML_EXPORT_NOT_FOUND`, or `LOCAL_XML_ONLY_UNCONFIRMED`. This artifact is mandatory whenever a runtime XML, local XML, HADES/stored XML, or XML-export residual exists. If HADES/Oracle is unavailable, still create the file and mark the source-of-truth decision `Blocked` or `Partial`; do not leave the decision only inside `investigation.md`.

Never use `document.documentElement.outerHTML` from Chromium's XML viewer as the raw XML export; it can capture the viewer page instead of the original resource. If the raw XML cannot be saved, record the exact attempted methods and residual such as `XML_RAW_EXPORT_NOT_SAVED`.

Do not treat copied/rendered text from Chromium's XML viewer as raw XML unless an XML parser accepts the saved file. The viewer can display escaped XML attribute content as literal markup, producing invalid XML such as attributes containing raw `<div ...>`. If parsing fails, classify the file as `RUNTIME_XML_BROWSER_TEXT_INVALID`; use it only as diagnostic evidence and continue from parser-valid local XML, raw HTTP export, or HADES/Cronos source.

Never place credential literals in shell commands, generated scripts, report snippets, or command transcripts. Prefer a local secrets/env file, environment variables, or an already-authenticated browser session. If no safe non-recording credential path exists, ask the user for one before running an HTTP login from the shell.

When credentials exist only in the active conversation/session, prefer logging in through the authenticated browser surface over embedding credentials in shell. If browser automation cannot safely submit the login, ask the user to log in manually and continue from that session. Even without submitting credentials, parse and record sanitized login mechanics from the login HTML: resolved form action, method, field names, HTTP status, and issued cookie names only.

Use exported runtime XML as the primary structural source when it exists and diverges from local XML. Still capture browser/runtime evidence for SQL behavior, binds, permissions, action availability, write payloads, and dynamic controller behavior; exported XML alone does not close API parity.

## Cronos Bind And Scope Resolution

For Cronos/Archon screens, do not treat Chrome/browser automation as the only
way to close bind semantics. When the open question is bind order, lookup source,
special selector values, or company/session scope, first combine parser-valid XML
and Oracle metadata:

1. Read `sqlParameters` and bind order from the runtime XML or from the accepted
   source in `cronos-source-of-truth.md`.
2. Read the SQL predicate where the bind is applied, for example `VALOR = ?`.
3. Locate the reused component definition or an equivalent screen component that
   defines the same control.
4. Resolve the combo/searchbox source through Oracle metadata, view text,
   dependencies, synonyms, or package/function source.
5. Save the read-only Oracle output under `docs/migracao/<SCREEN>/oracle-results/`.
6. Classify the bind as public filter, server-side scope, constant bind,
   parent-row context, or internal runtime parameter.

Example pattern already proven in `ERGadm00034`: `component/HADadm_blk003`
exposes `drpSelecEmpresa`; equivalent screens define it with
`select valor, descr from SELEC_COMBO_EMPRESA_VW order by valor`; Oracle view
text confirms `-1` = all companies, `-2` = no company, and
`flag_pack.get_empresa` = current company. That means `VALOR` is internal
company/query-mode scope, not a public `FilterDTO`, schema, URL, `OptionDTO.extra`,
or x-ui field when a functional key exists.

Use `docs/migracao/phase1-cronos-bind-resolution-standard.md` when present. If
XML plus Oracle metadata closes the semantics and no browser evidence
contradicts it, record `BIND_SEMANTICS_CLOSED_BY_XML_ORACLE` or equivalent in
the gate instead of blocking only because Chrome/browser automation is
unavailable. Browser/runtime evidence is still required for visible workflow,
action availability, messages, write payloads, restricted-user behavior, and
final legacy/API parity.

## Cronos RecordPanel Write Payload Resolution

For standard Cronos/Archon write panels, do not make browser navigation the first
or only path to close create/update payloads. If XML shows
`component/recordPanelEdit` with `dataTable` and without `rotina`,
`insertMethod`, `updateMethod`, or `deleteMethod`, resolve the payload from
parser-valid XML plus the local Cronos framework source before asking the
developer to operate the browser.

Required source-derived check:

1. Locate the `recordPanelEdit` component and its `dataTable`.
2. Extract sibling/child `component/editField/*` controls in layout order:
   `field`, `fieldTarget`, `caption`, `dataType`, `required`, `validators`,
   `initialValue`, `valueProperty`, `displayProperty`, and lookup SQL/options.
3. Confirm in Cronos source that `RecordPanelEditImpl` dispatches `dataTable` to
   `createManagerDescription()`.
4. Confirm `ManagerDescriptionParameters` uses `_op` for operation, `_p_` for
   proposed values, `_o_` for original values, and `_q_p_` for query/reload
   values.
5. Confirm `ManagerTableParametersImpl` and `AbstractTableDescription` generate
   table `INSERT`, `UPDATE ... WHERE PK`, and `DELETE ... WHERE PK`.
6. Confirm `ManagerDescriptionImpl` executes the generated Oracle SQL on the
   application connection and reloads rows by internal rowid/query description.

When `tools/migration-factory/new-cronos-recordpanel-write-payload.ps1` exists,
run it with `-Strict` and save the generated Markdown/JSON under
`docs/migracao/<SCREEN>/factory/`. A passing result may close create/update
payload discovery as `SOURCE_DERIVED_PAYLOAD_READY_FOR_DB_PROBE`.

This source-derived payload replaces browser payload capture for the standard
`recordPanelEdit + dataTable` pattern. Browser remains useful for visible
success/error messages, action availability, duplicate defaults, permissions,
cancel/no-op behavior, and final UI parity, but it should not block payload
closure when XML + Cronos source already prove the route.

## Assisted Codex Browser Session

When the in-app browser is available, ask the developer to log in once if needed, then operate from the authenticated page. For direct URLs such as:

```text
http://ergon-demo-644.techne.com.br/Ergon/Administracao/ERGadm00189.tp
```

record the page as `Browser access status: Partial` as soon as the authenticated screen is visible, even before every workflow is exercised. Then complete the observation by clicking through the visible UI:

- Confirm final URL, title, module, and whether the menu/search path also finds the page.
- Inspect frames, popups, debug panels, XML/debug buttons, network/runtime SQL panels, and hidden fields exposed by the legacy UI.
- Prefer direct browser observation for dynamic behavior that automation often misses: enabled/disabled actions, popup navigation, row selection, tab lazy loading, validation messages, and session-specific authorization.
- Save only concise evidence. Do not dump full page HTML, screenshots with sensitive data, or credential-bearing logs into the migration package.
- If Codex cannot programmatically inspect the in-app browser in the current environment, have the developer keep the page open and use browser-visible facts they provide as `CONFIRMED_RUNTIME_MANUAL`; do not upgrade SQL/bind behavior to `CONFIRMED_RUNTIME` until Codex or a captured debug artifact verifies it.

Create or update `docs/migracao/<SCREEN>/browser-runtime.md` using [codex-browser-runtime-capture.md](references/codex-browser-runtime-capture.md). Also create `runtime-capture-form.md` from [runtime-capture-form-template.md](references/runtime-capture-form-template.md) when Codex cannot inspect the browser DOM directly and the developer must relay visible/debug facts. `browser-runtime.md` is the working runtime notebook; summarize only stable findings back into `investigation.md`.

For Phase 1 validation before developer handoff, `runtime-capture-form.md` is not a substitute for executed runtime evidence. If default load, runtime bind values, page size, selected-row/public-key proof, visible action state, or representative non-empty fixture/context are missing, close Phase 1 as `Blocked`; do not mark it `Ready for next phase` or `Ready for next phase with adjustments`.

When the workspace provides `docs/migracao/phase1-scope-authorization-standard.md`, use it as the Phase 1 scope/authorization contract. The factory workbook should record `phase1-scope-authorization-v2-bridge` when the screen is an API-only Ergon/HADES bridge. `allowed-default-context` can close only with authenticated browser default load, non-empty fixture, selected row, public-key correlation, and same-connection Ergon/HADES Oracle context. For API-only screens governed by `ergon-hades-security-starter` and `ergon-legacy-bridge`, `company-scoped-context` and `restricted-user-context` close by the shared bridge/security contract and must not block each screen individually. Reopen them as blocking only when the screen bypasses `HadesLegacyAccessGuard`/equivalent, bypasses `ErgonLegacyExecutor`/equivalent, exposes company/user/profile/security context publicly, or implements custom security outside HADES. When the factory provides `new-phase1-scope-authorization-decision-pack.ps1`, generate its Markdown/JSON pack only for genuinely open scope cases; the pack requests owner decisions but does not close Phase 1 by itself. Do not turn company, user, profile, permission, or session binds into public FilterDTO/schema/URL/option/x-ui fields.

## Workflow

1. Identify the target screen code, URL, title, module, and user-visible workflow.
2. Open the default legacy entry point when no direct URL is known, log in using credentials provided by the user for the active session, and locate the screen through the page/menu search field.
3. Run the Runtime XML Export Gate for the matching `.xml` route. If export succeeds, compare it with local product XML and use the runtime export as the primary structural source when it diverges. If export is blocked, record the blocker and continue with lower confidence.
4. Inspect the running screen with the Codex in-app browser when available, or Chrome when the user's Chrome profile is required. Capture visible grids, tabs, actions, links to related screens, debug tree nodes, XML/debug `sqlSelect`, `sqlParameters`, page size, filters, hidden fields, and observed bind values. If browser inspection is unavailable, continue from local XML/source and mark browser evidence as missing or manual-only.
5. Inspect local legacy artifacts when present, especially `docs-legado/**/<SCREEN>.xml`, view scripts, Java services, DTOs, and resource classes. Treat XML `sqlSelect`, `sqlParameters`, component ids, links, and filter bindings as an initial source for Oracle seed objects only after classifying runtime export availability.
6. Inspect the legacy architecture/documentation tree when `docs-legado/v7x` is available using [legacy-docs-discovery.md](references/legacy-docs-discovery.md). This tree has known evidence layers: Archon XML/controllers under `java`, local DDL/source under `aps`, Enterprise Architect exports under `EA`, RoboHelp model/reference archives under `help`, functional/technical specs under `docs/Interno`, workflow assets under `workflow`, and older Forms/Reports assets under `forms` and `reports`. Use these sources for business meaning, candidate parity cases, model context, and related-flow discovery; do not let documentation override browser/XML/Oracle evidence.
7. Build a narrow seed list from browser/XML SQL before querying Oracle. Include screen views, lookup views, linked-screen views, packages/functions referenced by SQL, and objects introduced by related flows.
8. Query Oracle metadata using [oracle-queries.md](references/oracle-queries.md). Treat `ERGON` and `HADES` as defaults, not universal owners. Resolve synonyms, expand views recursively, inspect columns, constraints, indexes, triggers, grants, package arguments, source references, updatable columns, and write risks.
9. Classify every object by role and confidence. Do not promote structural matches to confirmed objects without evidence.
10. If screen SQL, views, helpers, triggers, or packages depend on Oracle package state such as `HADES.FLAG_PACK`, document the Java same-connection context strategy using [java-oracle-session-context.md](references/java-oracle-session-context.md). Do this before marking any Java/API contract as ready.
11. Produce or update read-only Oracle confirmation SQL from [oracle-confirmation-template.md](references/oracle-confirmation-template.md) when Oracle access is available or when follow-up confirmation is needed. When the repository has `tools/migration-factory/new-phase1-oracle-sql.ps1` and `factory/extraction.json` exists, use that generator before writing any manual Oracle/HADES SQL. It standardizes `oracle-confirmation.sql` and `hades-registry.sql` from XML seeds, preserves owner/package/subprogram identity, avoids known dictionary mistakes such as `ALL_PROCEDURES.STATUS`, expands view/physical lineage, reports owner collisions, covers HADES registry/access/menu/stored-resource candidates, and adds minimal non-empty smoke probes for read/view seeds. Manual SQL is allowed only as a supplemental artifact with the exact reason recorded in the gate. A Phase 1 package must include both object confirmation coverage and HADES registry coverage, either in `oracle-confirmation.sql` plus `hades-registry.sql`, or in one clearly sectioned SQL file. Use the executed outputs to fill the component-to-API matrix and candidate API contract facts: DTO fields, FilterDTOs, options, keys, scope, authorization, session context, related resources, and blocked/deferred writes. If execution fails, save a sanitized blocked note under `oracle-results/` and keep all Oracle/HADES findings below `CONFIRMED_ORACLE_METADATA`. Before closing the gate, scan every referenced Oracle/tool output for `ORA-`, `SP2-`, `TNS-`, `ERROR:`, `Exception`, and `IllegalArgumentException`; a corrected supplemental SQL may supersede a failed statement only when the gate explicitly records the failed output and the replacement evidence.
12. Create or update `read-parity-matrix.md` from [read-parity-matrix-template.md](references/read-parity-matrix-template.md). For every read endpoint candidate, record the legacy component, Oracle source, Java/API source if it exists, key strategy, filters/binds, paging/sort, options behavior, HTTP/API execution status, and the exact remaining gap. A read API can be "implemented" and still not be "parity closed".
13. When the XML/browser shows create, edit, delete, duplicate, pending, publication, legal-document behavior, or `recordPanelEdit` with a `db:*` routine, read [archon-write-patterns.md](references/archon-write-patterns.md), then create `write-risk.md` from [write-risk-template.md](references/write-risk-template.md) and a focused `write-risk-detail.sql` from [write-risk-detail-template.sql](references/write-risk-detail-template.sql). Use exact routines/tables/triggers from XML/runtime evidence; avoid broad table-name source searches. If the screen is closed as `Ready for read API` or receives a read-first implementation while write remains blocked/deferred, create `write-api-handoff.md` from [write-api-handoff-template.md](references/write-api-handoff-template.md).
14. Before starting Phase 3 write design, close write payloads for every visible write action in scope. For standard Cronos `recordPanelEdit + dataTable`, prefer the source-derived XML + Cronos framework path above and then require a controlled DB probe. For rotina/object-method/custom actions, or when XML/source does not prove the route, capture runtime write payloads for `Novo`, `Editar`, `Apagar`, `Duplicar`, `Salvar`, `Cancelar`, legal-document actions, publication actions, pending actions, and any screen-specific business action. Record UI state before/after click, confirmation dialogs, hidden keys such as `ROWID_REG`, operation selector values, selected public id, `P_MENS`, routine arguments, legal-document/publication/pending fields, changed debug/network request, and observed validation messages. If neither source-derived payload nor runtime payload can be captured, mark the operation `Blocked` or `Deferred` with the exact next XML/source/browser/debug step; do not leave `operation-inventory.md` with a generic `Unknown` backend state and do not infer payloads from PL/SQL signatures alone.
15. Use gates before finalizing: `Observed`, `Resolved`, `Expanded`, `Read-parity planned/executed`, `Write-risk checked`, `False-positive checked`, `Confirmation SQL complete`, `Session-context checked`, and, for Java work, `API-ready`.
16. Produce the investigation report using [investigation-template.md](references/investigation-template.md).
17. If the user is planning Java migration, read [api-design-patterns.md](references/api-design-patterns.md), [lib-ui-fieldspec-api.md](references/lib-ui-fieldspec-api.md), and [java-api-implementation-playbook.md](references/java-api-implementation-playbook.md), then produce the API contract using [api-migration-template.md](references/api-migration-template.md). Keep endpoints as `Candidate`, `Blocked`, or `Deferred` until keys, scope, authorization, session context, runtime binds, FieldSpec contract, read parity plan, and write boundaries are closed.
18. Load [example-ergadm00033-findings.md](references/example-ergadm00033-findings.md) only when the target is ERGadm00033/ERGadm00034 or when the user explicitly asks for that example.
19. Load [example-ergadm00189-findings.md](references/example-ergadm00189-findings.md) only when the target is ERGadm00189 or when the user explicitly asks for that example. Load [example-ergadm00189-api-contract.md](references/example-ergadm00189-api-contract.md) when drafting or validating a read-first frequency API contract.
20. Load [case-review-ergadm00189.md](references/case-review-ergadm00189.md) when improving the skill process or when investigating a similar read/write frequency screen.

## Browser Capture Checklist

Capture enough runtime evidence to explain what the user sees and how the SQL changes:

- Login entry point, navigation path, final URL, screen title, and module.
- Search terms used in the menu/page search field and the selected result.
- Initial grid SQL, page size, default order, visible columns, hidden key fields, and default bind values.
- Company selector or scope selector values, including special values such as `-1` and `-2` when present.
- Filter behavior for each visible search field, including empty/null/default behavior.
- Tabs and nested grids loaded only after user interaction.
- Links to related screens and the exact parameters passed in the URL or runtime state.
- Action buttons, edit/delete/detail flows, confirmation dialogs, and whether the screen appears read-only.
- Runtime/debug SQL snippets, `sqlSelect`, `sqlParameters`, component ids, and observed bind values.

Prefer concise evidence snippets. Do not paste huge XML/debug dumps into the final report.

## XML And SQL First

Before deep Oracle investigation, extract from the screen XML/debug:

- Component id and user-visible area.
- `sqlSelect` and `sqlParameters`.
- Bind token order and default/null behavior.
- Lookup/combo SQLs.
- Linked screen URLs and parameter names.
- `ROWID`, hidden ids, composite keys, generated columns, and any edit/delete action metadata.
- Page size, sorting, filters, and search helper functions.

Use this extraction to produce the Oracle seed list. Every object in the seed list should have a source reference: browser runtime, XML/debug, local source, or an explicitly marked candidate reason.

## Component To API Inventory

Every investigation must include `component-lineage-matrix.md`. Treat it as a component-to-API inventory, not as HTML reconstruction and not as an Oracle dependency dump.

Create it from [component-lineage-matrix-template.md](references/component-lineage-matrix-template.md) and force one decision per relevant component:

- `main-list`: usually one `POST /<resource>/filter`.
- `filter`: a `FilterDTO` field plus backend predicate/bind mapping.
- `lookup`: an option resource with `/options/filter` and `/options/by-ids`.
- `detail`: `GET /<resource>/{id}` only after public key strategy closes.
- `field`: DTO field, read-only/hidden/internal decision, or `Not API`.
- `related-resource`: separate resource or deferred related flow.
- `navigation`: link/relationship, not automatically a new endpoint.
- `write-action`: `Blocked` until write-risk closes.
- `authorization/capability` or `context`: service/session policy, not display metadata only.
- `layout-only`: `Not API`.

For each row, include evidence, SQL/action/link, binds/params/hidden keys, API translation, resource/endpoint candidate, DTO/FilterDTO/OptionDTO/CommandDTO impact, status, and blocking checks.

Do not create one API per visual component. Multiple components can feed the same business resource. Do not use the matrix as a dependency dump. Deep view expansion, triggers, grants, and package internals belong in `investigation.md` and Oracle results; the matrix should explain why each component matters for API migration.

## Closure Before API

Do not move a screen from discovery into API implementation until `closure-checklist.md` is complete enough to support the intended scope.

Use [closure-checklist-template.md](references/closure-checklist-template.md) and classify the final state:

- `Open`: investigation still has blocking unknowns.
- `Ready for read API`: read/list/detail scope is closed, but write or related flows may remain deferred.
- `Ready for write API`: read and write behavior are both understood with parity checks.
- `Deferred`: investigation is intentionally paused with explicit blockers.

If the user asks to avoid API work until discovery is closed, keep all API endpoints in `Candidate` or `Blocked` status and focus on closing runtime, keys, authorization, write behavior, and related flows.

For read-first migrations, write may be explicitly deferred without blocking read API discovery only when the deferral is evidence-backed. Record the routines, triggers, package hooks, audit, pending-record behavior, publication/legal-document coupling, and missing parity cases in `write-risk.md`. Do not leave write as an unexamined unknown.

Use a read-first closure label such as `Read handoff ready; write deferred` when the runtime/read surface is closed but write/related flows are intentionally blocked. This state is acceptable for Phase 2 read API migration when the package records runtime binds, selected-row evidence, public key strategy, authorization/scope, same-connection session context, and write deferral evidence.

When a read-first screen has real write behavior, also create `write-api-handoff.md`. This is the boundary artifact for a future write-focused skill. It should summarize implemented read endpoints, write entry points, candidate legacy routines, payload candidates, side effects, blockers, and whether the next phase is `Legacy-backed Write API candidate`, `Blocked`, or `Not suitable`. Do not use `Unknown` as a final status in `write-api-handoff.md`; if payload, routine, or side-effect evidence is missing, record `Not captured` or `Blocked` with the exact next browser/debug/Oracle check.

When browser runtime exposes both a stable API key and legacy row locator, keep the split explicit. Prefer the stable key, such as `ID_REG`, for public read endpoints. Treat `ROWID`, `ROWID_REG`, XML hidden ids, and component-specific fields such as row-level publication/anulacao locators as internal bridge evidence unless a later write contract explicitly accepts exposure.

## API Contract Design

Use [api-design-patterns.md](references/api-design-patterns.md) and [lib-ui-fieldspec-api.md](references/lib-ui-fieldspec-api.md) before drafting `api-contract.md`. Use [java-api-implementation-playbook.md](references/java-api-implementation-playbook.md) before editing Java API code. For ERGadm00189 or similar frequency screens, compare the draft against [example-ergadm00189-api-contract.md](references/example-ergadm00189-api-contract.md).

The API contract should be derived from the component lineage matrix and closure checklist:

- Context/selectors become scope parameters or context endpoints.
- Main grids become list endpoints only after filters, sort order, pagination, key fields, and authorization are known.
- Detail panels become detail endpoints only after stable public key strategy is decided.
- Lookups become lookup endpoints when they are reused by the API surface or have independent authorization/filter behavior.
- Related tabs and popups remain `Candidate` unless included in the current migration slice.
- Write actions remain `Blocked` or `Deferred` until `write-risk.md` proves they are write-ready.
- Components marked `layout-only`, static labels, visual grouping, separators, or debug-only helpers stay `Not API` unless they carry data, action, authorization, or source semantics.

Do not expose Archon internals as API contract by default: `ROWID`, XML component ids, link display fields, debug parameters, and stored procedure names are implementation evidence, not public resource design.

Each endpoint in `api-contract.md` must have status, legacy source, key strategy, scope/session-context decision, DTO field map, error behavior, and parity cases. If any of these is missing, the endpoint is not `Required Now`.

For Java APIs in this workspace, the default implementation target is `lib-ui-fieldspec`: `AbstractResourceController`, `BaseResourceService`, `GenericFilterDTO`, `@UISchema`, `OptionDTO`, `RestApiResponse`, `/filter`, `/options/*`, `/by-ids`, `/schemas`, and optional cursor/locate/stats endpoints. Do not design custom endpoint shapes when the FieldSpec resource pattern covers the use case. Do not enable generated CRUD writes from the resource controller unless `write-risk.md` is closed as `Write API ready`.

FieldSpec metadata is not enough by itself. The executor must map each DTO/FilterDTO field to both UI behavior and backend behavior. Date interval filters should normally use `FieldControlType.DATE_RANGE` for the UI, while the service/query must preserve the exact legacy predicate, for example interval overlap logic instead of a naive `BETWEEN` when the XML SQL uses concomitance helpers. Dynamic filters, dependent selects, and options endpoints need explicit service/query implementations and parity cases.

Materializing an API means coding the complete resource slice, not only generating DTO annotations. The executor must update or create endpoint constants, OpenAPI grouping, controller/resource, service/query implementation, DTO, FilterDTO, option endpoints, mapper/conversion code, unsupported endpoint behavior, and OpenAPI/x-ui/parity tests for every endpoint marked `Required Now`.

Before choosing a specialized `controlType`, verify the backend contract in `lib-ui-fieldspec`: `FieldControlType.java`, `CustomOpenApiResolver.java`, and `OpenApiUiUtils.java`. `DATE_RANGE`/`dateRange` is a date interval control; numeric ranges or other ranges must be mapped separately and must not assume API support just because the backend enum exists.

Before implementation, inspect the target application wiring. For `ms-administracao-pessoal`, verify `ApiEndpoints.java`, `SwaggerConfig.java`, `SwaggerValidationConfig.java`, `application.yaml`, existing controllers/services/DTOs/FilterDTOs, and OpenAPI/x-ui test scripts. New resources normally need path/group/tag constants plus a `GroupedOpenApi`; existing resources should be extended when they already represent the same business concept. User-facing annotations must be PT-BR with accents and consistent legacy terminology because they drive the generated UI.

## Write-Risk Closure

Treat write behavior as a separate closure surface whenever the screen exposes create, edit, delete, duplicate, save/cancel, pending approval, publication, legal document, or generated DML hooks.

Archon/Ergon write screens commonly follow the generated DML architecture described in [archon-write-patterns.md](references/archon-write-patterns.md): XML `recordPanelEdit` or reusable blocks call `db:*` routines, often `ERG_DML_*`, which can interact with generated triggers, audit packages, `FLAG_PACK` session state, pending packages, publication blocks, and legal-document routines. Use this as a checklist, not a substitute for per-screen confirmation.

Use `write-risk.md` for the migration decision and `write-risk-detail.sql` for the Oracle evidence. A good write-risk pass answers:

- Which UI actions can write, and which XML components trigger them.
- Which DML routines, generated procedures, packages, triggers, and target tables are involved.
- Whether payloads include related publication/legal/pending fields beyond the visible main form.
- Which validations and legacy error messages must be preserved.
- Which side effects exist: audit, pending workflow, generated history, publication/legal pointers, autonomous transactions, extension hooks, and session-package dependencies.
- Whether the current phase is `Write API ready`, `Blocked for write API`, or `Deferred`.

For write-ready handoff, add a payload closure section before Phase 3. For standard Cronos `recordPanelEdit + dataTable`, this section may reference the source-derived XML + Cronos framework artifact and the required DB probe. For other write actions, it should cover each visible operation separately and include:

- action path: selected row/context, button clicked, dialog/tab state, and save/cancel behavior;
- operation discriminator: `P_OPER`, insert/update/delete/duplicate mode, or equivalent hidden value;
- keys: public API id, `ROWID_REG`/`P_ROWID_REG`, publication/legal row locators, and whether each is public or internal;
- payload groups: `PB_*` frequency/business fields, `PP_*` publication fields, legal-document fields, pending fields, flex fields, and defaults omitted by the UI;
- context: `FLAG_PACK` user, transaction, company, role/sis when visible or inferred from confirmed session context;
- result: success message, validation message, confirmation text, changed row, pending/publication side effects, or cancellation with no mutation.

If the browser does not expose a network request, first check whether XML + local Cronos source can close a standard `recordPanelEdit + dataTable` payload. Otherwise use Archon debug/runtime panels, hidden field inspection, screenshots plus manual notes, and Oracle before/after probes. Keep credentials and broad HTML dumps out of the artifacts.

If the first Java migration phase is read-only, prefer `Blocked for write API` or `Deferred` with concrete evidence over a vague "write pending" note.

## Java Oracle Session Context

When SQL uses session package state such as `flag_pack.get_usuario`, `flag_pack.get_transacao`, or `flag_pack.get_empresa`, treat Java session-context handling as a closure gate.

Use [java-oracle-session-context.md](references/java-oracle-session-context.md) and document:

- The source of the API user and how it maps to the legacy `USUARIO` value.
- The transaction code to set, usually the screen code confirmed in HADES.
- The company value source or explicit reason it is not applicable.
- The exact package setters needed before the query.
- The same-connection strategy for Spring/JPA/JDBC, especially when using connection pools.
- The cleanup/reset strategy to prevent context leakage between pooled requests.
- Parity cases for privileged, allowed, denied, and company-scoped users.

Do not consider a read API ready if the only context setup is an external SQLcl session. SQLcl initializes its own connection, not the API server's pooled connection.

Read-first and write-ready are separate API states. A read-first API may proceed when read gates are closed and write is explicitly `Blocked` or `Deferred` with concrete write-risk evidence. A write API may proceed only when generated DML routines, triggers, audit, pending, publication/legal document coupling, permissions, session context, validations, and write parity cases are closed.

## HADES Screen Registry And Stored XML

Archon/Ergon screens can be registered in HADES tables even when the XML is also present in local application resources. Always check HADES before declaring XML unavailable.

For a target screen such as `ERGadm00189`, first query transaction and access mapping tables:

- `HADES.TRANSACAO` and `HADES.HADADM00019_TRANSACAO`: transaction code, menu item, title, web/type flags, optional form fields.
- `HADES.TRANSPADACES`, `HADES.HADADM00015_TRANSPADACES`, and `HADES.HADADM00023_TRANSPADACES`: access pattern and create/edit/delete permissions (`PODECAD`, `PODEALT`, `PODEREM`).
- `HADES.TRANSPADTELA`, `HADES.HADADM00020_TRANSPADTELA`, `HADES.PADTELA`, and `HADES.MENUDEF`: menu/path and screen pattern metadata when present.
- `HADES.HAD_ARQUIVOS_REGS` and `HADES.HAD_VW_ARQUIVOS_REGS`: attached file/blob candidates when a screen-specific XML or resource is stored as an uploaded artifact.

Then search for the screen code and XML markers across HADES text columns:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\find_hades_screen_definition.ps1 `
  -Screen ERGadm00189 `
  -MainView ERGADM00189_FREQUENCIAS `
  -OutputDir docs\migracao\ERGadm00189\oracle-results
```

Useful patterns include the screen code, visible title, `sqlSelect`, `sqlParameters`, the main view name, and linked transaction names. Run narrow searches first; broad owner-wide text scans can be slow and noisy in legacy schemas. Use `-IncludeXmlMarkers` only when the first pass does not locate the definition. Use `-IncludeBlobSearch` only for targeted passes because BLOB search samples limited bytes from candidate rows.

For one-off searches, use:

- `scripts/search_oracle_text.ps1` for `VARCHAR2`, `CLOB`, `NCLOB`, and similar text columns.
- `scripts/search_oracle_blob_text.ps1` for text-like BLOB candidates. It samples at most 2000 bytes per row by default and reports snippets only when the pattern matches.

## Suggested Artifact Layout

When creating files for a migration package, prefer this shape unless the repository has a stronger convention:

```text
docs/migracao/<SCREEN>/
  investigation.md
  browser-runtime.md
  runtime-capture-form.md
  legacy-doc-sources.md
  component-lineage-matrix.md
  closure-checklist.md
  oracle-confirmation.sql
  write-risk.md
  write-risk-detail.sql
  write-api-handoff.md
  operation-inventory.md
  api-contract.md
  oracle-results/
```

Keep credentials and raw sensitive data out of these artifacts.

Discovery does not open a new migration package. If `docs/migracao/<SCREEN>/`,
`migration-plan.md`, or `phase-0-execution-gate.md` are missing, return to the
canonical Parte 1 entry point in
`docs/migracao/backend-api-only-roadmap.md` and run Fase 0 with
`ergon-migration-orchestration`.

## Investigation Modes

Use the smallest mode that satisfies the request:

- `Quick discovery`: browser/XML/local source only. Useful when Oracle access is missing.
- `Full discovery`: browser/XML/local source plus Oracle metadata confirmation.
- `API migration`: full discovery plus REST contract, DTO map, key strategy, and parity matrix.

State which mode was used and which evidence sources were unavailable.

## Confidence Levels

Use one of these labels for every object, relationship, SQL statement, and proposed API field:

- `CONFIRMED_RUNTIME`: observed through browser/runtime SQL, data mutation, or network/runtime evidence.
- `CONFIRMED_RUNTIME_MANUAL`: observed by the developer in an authenticated browser session and relayed to Codex, but not yet captured in a Codex-readable artifact. Use this only for visible UI facts, not SQL lineage or bind semantics.
- `CONFIRMED_XML`: found directly in Archon XML/debug, including `sqlSelect`, `sqlParameters`, component definitions, or links.
- `CONFIRMED_LOCAL_DOC`: found in legacy documentation such as EA exports, help/modelagem, reference help, functional/technical specs, or module manuals. Use for business meaning and candidate parity, not as sole proof for implementation SQL.
- `CONFIRMED_ORACLE_METADATA`: found through Oracle dependency, view text, constraint, trigger, grant, package argument, source reference, or synonym resolution queried from Oracle.
- `CONFIRMED_LOCAL_SOURCE`: found in local checked-in SQL, XML, Java, PL/SQL, or generated artifacts but not yet confirmed against Oracle metadata.
- `INFERRED_METADATA`: inferred from schema, column alignment, naming, or related metadata.
- `CANDIDATE_UNCONFIRMED`: plausible but not proven. Keep out of implementation contracts unless explicitly marked pending.

Use the legacy `CONFIRMED_DEPENDENCY` label only when updating older reports would be disruptive; otherwise prefer the split Oracle/local labels.

## Object Roles

Classify objects by functional role:

- `screen_view`: view directly queried by the screen.
- `screen_registry`: HADES transaction, menu, access-pattern, or stored-resource metadata that identifies how the screen is registered and exposed.
- `domain_table`: base table for the main business entity.
- `scope_table`: association table for company, user, role, or visibility scope.
- `related_screen_view`: view queried by a linked screen or nested tab.
- `lookup`: combo/list-of-values source.
- `document_or_audit`: legal document, history, audit, or attachment-like data.
- `security_helper`: package/function/view enforcing current user, company, or permission.
- `candidate`: object that needs another evidence source before use.

## Oracle Access

Codex should operate Oracle discovery directly when the environment has been provisioned with database access. Do not hand routine confirmation steps back to the developer to run manually. Use `scripts/run_oracle_query.ps1` when SQLcl is available. Keep queries read-only unless the user explicitly asks for a controlled write test.

If SQLcl fails in non-interactive Codex execution because of Windows console handling, use `scripts/run_oracle_query_jdbc.ps1`. It uses the `ojdbc11.jar` bundled under the workspace SQLcl installation, strips SQLcl formatting commands, and executes read-only `select`/`with` statements from the same confirmation SQL file.

Do not embed or print credentials in generated artifacts. Prefer passing the connection string through a parameter or environment variable. Limit row samples and avoid dumping sensitive business data.

Recommended local variables:

- `ERGON_HADES_CONN`: SQLcl connection string or wallet alias.
- `ERGON_SQLCL`: path to `sql.exe`.
- `JAVA_HOME`: Java runtime used by SQLcl.

Default workspace SQLcl path:

```text
tools\sqlcl\bin\sql.exe
```

Provision credentials outside the skill and repository. Acceptable options, in preference order:

1. Oracle Wallet or an approved local secret provider, with `ERGON_HADES_CONN` using the wallet alias.
2. Process/session environment variable injected into the Codex workspace before the investigation starts.
3. Temporary user-provided connection string for the active session only.

For this migration workspace, the standard local bootstrap file is:

```text
secrets\ergon.env.ps1
```

It should define:

```powershell
$env:ERGON_HADES_CONN = '<wallet-alias-or-connection-string>'
$env:ERGON_SQLCL = 'D:\Developer\Techne\ErgonX\migracao\tools\sqlcl\bin\sql.exe'
```

Codex may dot-source this file during an investigation when it exists locally, but must not print its contents.

The skill may document required variable names and paths, but must not store Oracle usernames, passwords, hosts, service names, wallet passwords, or full connection strings in `SKILL.md`, generated reports, SQL files, commits, tickets, or shared prompts.

Example execution:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query.ps1 `
  -SqlFile docs\migracao\<SCREEN>\oracle-confirmation.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\confirmation.txt
```

Fallback execution:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile docs\migracao\<SCREEN>\oracle-confirmation.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\confirmation.txt `
  -MaxRows 500
```

When Oracle is unavailable, still generate the confirmation SQL if it would unblock a database-owning teammate. Mark its evidence as `CONFIRMED_LOCAL_SOURCE` or `CANDIDATE_UNCONFIRMED` until execution results are attached or summarized.

When Oracle is available to Codex, execute the confirmation SQL, save the output under the screen package, summarize the result in the investigation report, and promote only proven findings to `CONFIRMED_ORACLE_METADATA`.

## API Readiness Criteria

Do not mark Java implementation as ready until these points are resolved or explicitly scoped out:

- The main screen SQL is confirmed by browser/runtime, XML/debug, or local source.
- Synonyms are resolved to effective owner/object.
- Screen views and related views are expanded to physical tables.
- Stable keys are selected for list/detail/related endpoints, and any `ROWID` exposure is rejected or explicitly justified.
- Company/user scope behavior is understood, including special values and security helper packages/functions.
- Pagination, sorting, filter semantics, default values, and null behavior are documented from legacy behavior.
- Write behavior is either out of scope or checked through triggers, updatable views, defaults, packages, grants, and source writes.
- Legacy documentation has been searched when `docs-legado/v7x` is available, and doc-only facts are separated from implementation evidence.
- Java same-connection session context is documented when screen SQL, views, helpers, triggers, or packages depend on package state such as `HADES.FLAG_PACK`.
- Parity cases are defined for default list, scoped list, filters, related flows, empty results, and authorization failures.
- The `lib-ui-fieldspec` contract is decided: resource path, DTO, FilterDTO, ID type, `@UISchema`, options endpoints, schema URLs, response envelope, disabled/501 endpoints, and HTTP examples.
- FieldSpec filters are implemented, not only described: each FilterDTO field has UI control metadata, backend predicate/service logic, null/default behavior, and parity cases.

If any of these points is unresolved, mark the endpoint as `Candidate`, `Blocked`, or `Deferred` in the API contract instead of `Required Now`.

## Team Handoff Notes

For each screen handoff, include:

- What was observed in the browser and what was not.
- Which XML/source files were inspected.
- Which `docs-legado/v7x` layers were searched, what facts were promoted, and what remains doc-only.
- Which Oracle confirmation SQL was generated and whether it was executed.
- Which findings are confirmed versus candidates.
- Which endpoints are `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`.
- Whether Java/API session-context handling is required for package-state dependencies.
- The exact next check needed for every ambiguity.

Avoid broad follow-ups such as "confirmar no banco". Prefer concrete checks such as "run synonym resolution for `ERGADM00034_CODFREQ`" or "open the codes tab and capture bind values for `tipofreq` and `VALOR`".

## Required Output

Every investigation must include:

- Screen summary and navigation path.
- Browser/XML evidence with component names and SQL snippets.
- `cronos-source-of-truth.md` for Cronos/Archon screens when runtime XML, local XML, HADES/stored XML, or XML export status is part of the evidence. It must record the chosen source state, hashes/dates when available, HADES/stored-resource status, and whether the local XML is accepted, rejected, divergent, or still unconfirmed.
- `runtime-capture-form.md` from [runtime-capture-form-template.md](references/runtime-capture-form-template.md) whenever the browser workflow is not fully operated by Codex and the developer must provide manual/runtime facts. Do not rely on `browser-runtime.md` alone when the workflow is only inferred from XML.
- `runtime-parity-workbook.md` and `factory/runtime-parity-workbook.json` with baseline cases for real runtime binds, filter/options payloads, public key correlation, scope/authorization, and future legacy-vs-API parity seeds. A Phase 1 handoff must not treat API candidates as closed while this workbook has placeholders or stale browser evidence.
- `phase1-corporate-baseline.md` and `factory/phase1-corporate-baseline.json` when the migration factory is available, listing only the remaining fixture, runtime bind, public key, and allowed/default context blockers. For API-only screens governed by the shared Ergon/HADES bridge, company-scoped and restricted-user cases are architecture-level parity seeds, not per-screen blockers, unless a bridge bypass or custom security route is detected.
- `phase1-scope-authorization-decision-pack.md` and `factory/phase1-scope-authorization-decision-pack.json` when the migration factory is available and scope/authorization remains open, with owner decision templates and only sanitized evidence references.
- Legacy documentation summary in `legacy-doc-sources.md` when `docs-legado/v7x` is available, including searched layers, matched paths/topics, doc-only facts, promoted facts, and limits.
- Component-to-API inventory in `component-lineage-matrix.md`, mapping relevant XML/debug components to functional role, SQL/action/link, binds/hidden keys, API translation, resource/endpoint candidate, DTO/FilterDTO/OptionDTO/CommandDTO impact, readiness, and blocking checks.
- Operation inventory covering at least list, detail, create/save, edit/save, delete, duplicate, cancel, legal documents, publications/acts, and pending flows with per-operation state.
- Closure checklist with the screen's final state and remaining blockers before API implementation.
- Write-risk summary in `write-risk.md` when write-like behavior exists, including explicit ready/blocked/deferred decision.
- Write API handoff in `write-api-handoff.md` when read-first is closed and write-like behavior remains blocked/deferred, including legacy-backed write candidacy and exact next checks.
- Oracle object inventory with owner, object type, role, confidence, and evidence.
- View lineage from screen view to physical tables.
- Synonym resolution to the effective owner/object.
- HADES registry/access/stored-resource coverage, either as executed output or as an explicit blocked artifact with the exact connection/runtime blocker. A Phase 1 gate must not say `HADES_REGISTRY_NOT_CHECKED` unless the package also contains the SQL/helper command that will close that blocker.
- Security and company-scope behavior, including package/function dependencies.
- Confirmation SQL coverage, including any intentionally skipped related flows.
- Ambiguities and confirmation steps.

For Java migration tasks, also include:

- Minimal REST resources mapped from screen blocks/tabs/actions, with current-slice recommendation.
- Endpoint readiness gates; do not mark an endpoint `Required Now` while blocking decisions remain for keys, scope, authorization, session context, source data, browser/runtime behavior, parity cases, or write behavior.
- `lib-ui-fieldspec` resource mapping: controller/service base classes, DTO, FilterDTO, ID type, `@UISchema` requirements, standard endpoints enabled/disabled/501, options endpoints, schema URLs, and response envelope.
- Target application integration changes: `ApiEndpoints.java`, `SwaggerConfig.java`, config/properties, reused resources, updated DTOs/FilterDTOs/services, and OpenAPI/x-ui tests.
- Control availability evidence for specialized x-ui controls, especially range controls, across FieldSpec backend and generated OpenAPI/schema metadata.
- Key design options for every detail endpoint, including stable natural keys, composite keys, URL encoding, and why `ROWID` is or is not exposed.
- DTO fields with source column, type, nullability, conversion rules, and confidence.
- Query params, pagination, sorting, deterministic tie-breaker, filter behavior, and error semantics.
- Capability/action-state map only when the backend API exposes it deliberately.
- Company/user scope contract, including special values such as `-1` or `-2` when present.
- Parity test matrix comparing legacy behavior to the proposed API.

Use only the migration state vocabulary in `operation-inventory.md`: `Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred`, or `Not present`. Avoid generic `Unknown` as an operation/backend state; if evidence is missing, choose `Blocked` with a concrete next check, or `Not present` plus a Phase 4 side-effect check when the XML/browser pass did not show the operation.

Write Markdown reports as UTF-8 and preserve PT-BR accents from the legacy screen. If terminal output shows mojibake such as `CÃ³digos`, verify the file encoding before copying it into artifacts; do not normalize user-facing labels to ASCII.

## Do Not

- Do not treat one screen's findings as global Ergon rules.
- Do not treat legacy documentation as implementation proof unless browser/runtime, XML/debug, local source, or Oracle metadata confirms it.
- Do not mark generated tables such as `CMP*$...` as confirmed without XML, runtime, source, dependency, or data-change evidence.
- Do not propose Java write APIs until read flow, authorization, keys, routines, triggers, audit/pending side effects, and parity tests are understood. For read-first migration, document write deferral with evidence instead.
- Do not paste huge XML, logs, or full table samples into the final report; summarize and preserve only high-value evidence.
