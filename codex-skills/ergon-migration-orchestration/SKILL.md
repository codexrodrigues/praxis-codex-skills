---
name: ergon-migration-orchestration
description: Orchestrate complex Ergon/Archon legacy-to-Java migrations across ordered phases. Use when Codex must plan, audit, gate, or coordinate screen discovery, table rule audit, read API migration, write API migration, parity testing, handoff artifacts, or when the user asks what phase/skill should run next.
---

# Ergon Migration Orchestration

Use this skill as the top-level conductor for Ergon/Archon migrations. It does not replace the specialized skills; it decides the order, required artifacts, phase gates, and next action.

## Core Rule

Never let a later phase compensate for missing evidence from an earlier phase silently. If an artifact is missing, either produce it now with the right skill or mark the phase as blocked with the exact gap.

Before changing code, contracts, templates, or migration artifacts, apply the
root migration `AGENTS.md` platform governance. Classify the change as
`docs-apenas`, `local-pequena`, `transversal`, `contrato-publico`, or
`arquitetural`; identify the canonical owner; and record the impact map when
the change touches public contract, multiple consumers, or architecture.

Do not solve Praxis platform gaps by inventing Ergon-local semantics. If the
issue belongs to `praxis-ui-angular`, `praxis-metadata-starter`, or
`praxis-config-starter`, create a `Praxis Platform Follow-up` with objective
evidence and a prompt for the Praxis specialist. A temporary Ergon workaround
must have an owner, removal trigger, canonical replacement, and must prevent
the screen from being treated as a scalable example while it exists.

Every phase closeout must produce a reusable gate packet: final decision, evidence actually executed, residual issues with owners, explicit return-to-previous-phase rules, and the next recommended prompt/skill. If the screen advances with non-blocking residuals, classify it as `Ready for next phase with adjustments` and carry those residuals into the next phase and handoff.

Endpoint readiness is not a static-test decision. Do not call an endpoint `Verified` or promote it to handoff solely because unit tests, OpenAPI generation, schema assertions, or mocked service tests passed. For backend API handoff, require executed endpoint evidence plus legacy/API/database comparison with the same user/company/context and filters. If any part was not executed, use a narrower state such as `Implemented with automated tests`, `Schema/static contract passed`, `Executed endpoint smoke`, `Legacy parity pending`, `Blocked`, or `Deferred`.

For write operations, classify the route per operation instead of assuming either generic CRUD or DB-backed by default. The conservative default is: unknown rule, context, route, side effect, or error behavior means `WRITE_DB_BACKED_REQUIRED` or `WRITE_BLOCKED`. Direct table/Praxis CRUD can be approved only as `WRITE_TABLE_DIRECT_SAFE` when Phase 4/5 evidence proves it preserves required behavior, errors, session context, side effects, and parity.

## Canonical Phase Management Artifacts

Use these files to make phase state deterministic across agents and developers:

- `docs/migracao/<SCREEN>/phase-<PHASE-ID>-execution-gate.md`: required whenever a phase is classified as `Ready for next phase`, `Ready for next phase with adjustments`, `Blocked`, or `Deferred`. This file is the phase closeout; do not treat a functional artifact such as `quality-round-2.md` as a substitute.
- `docs/migracao/<SCREEN>/phase-<PHASE-ID>-<slug>-plan.md`: optional planning/reentry artifact. Use it before execution when scope is partial, a previous gate carried residuals, fixtures are conditional, browser/API/Oracle evidence must be coordinated, mutation risk exists, or a phase is resumed after an earlier closeout. A plan is not execution evidence and is not a gate closeout.

`<PHASE-ID>` uses dots converted to hyphens: Phase 1.5 is `1-5`.

When the user explicitly asks for planning only, create or update a `phase-<PHASE-ID>-<slug>-plan.md` and leave the phase state `Open`. When evidence has been executed or a phase decision is made, create or update the standalone `phase-<PHASE-ID>-execution-gate.md`.

## Short Continuation Commands

If the latest phase gate is `Ready for next phase` or `Ready for next phase with adjustments`, a short user command such as `continuar`, `seguir`, `ok`, `1`, or `proximo` is enough to start the next recommended phase.

When handling a short continuation command:

1. Locate the latest `docs/migracao/<SCREEN>/phase-<PHASE-ID>-execution-gate.md`.
2. Confirm its state is `Ready for next phase` or `Ready for next phase with adjustments`.
3. Read the gate's `Continuacao Curta` or next-step section as the source of truth.
4. Start the recommended next phase with the recommended skill and required input artifacts; do not stop after merely restating the prompt when the gate is unambiguous.
5. Carry residuals from the gate into the new phase.
6. Do not ask the user for a long prompt unless the gate is missing, ambiguous, `Blocked`, `Deferred`, or points to multiple possible next phases.

Short continuation is not automatic chaining. The user still needs to send a follow-up command, but it may be short because the gate is the source of truth.

Every phase gate that closes as `Ready for next phase` or `Ready for next phase with adjustments` must include a complete short-continuation contract: next phase, skill, required inputs, expected outputs, carried residuals, and the exact execution intent. If any of those fields is missing, treat the next short command as a request to repair/clarify the gate before running the next phase.

## Standard Legacy Operation Inventory

Treat Ergon/Archon screens as framework-driven until evidence proves otherwise. At intake and discovery time, create an operation inventory for the screen using this baseline:

- `Consultar/listar`: default grid/list load, filters, pagination, sorting, empty result, company/user scope.
- `Ler detalhe`: row selection, detail panel, nested detail form, public key, internal `ROWID`/locator strategy.
- `Novo/Salvar`: create mode, defaults, required fields, validation messages, generated DML routine/table route, success side effects, cleanup.
- `Editar/Salvar`: update mode, immutable keys, changed-field payload, validation messages, side effects.
- `Apagar`: delete/anulation button, confirmation dialog, permission/dependency blockers, cleanup and row preservation proof.
- `Duplicar`: copied/defaulted fields, new-key strategy, save route, duplicate validation.
- `Cancelar`: no-mutation behavior from create/edit/duplicate modes.
- `Documentos legais`: legal-document tab/block, linked component/screen, `PONTLEI`/document locators, read/write scope.
- `Publicacoes/atos` and `Pendencias`: include when visible, linked, or reached by triggers/packages, even if deferred from the current slice.

For every operation, record one of: `Implemented`, `Ready`, `Blocked`, `Deferred`, or `Not present`. Do not expose or hand off an operation unless its backend/API state is `Implemented` with parity evidence or intentionally blocked/deferred.

## Standard Praxis Metadata/API Mapping

For every operation in the inventory, map the legacy behavior to the new platform surface before implementation:

| Legacy operation | New platform/Praxis surface | Required migration decision |
| --- | --- | --- |
| `Consultar/listar` | `POST /<resource>/filter`; `BaseResourceService.filterWithIncludeIds`; DTO/FilterDTO metadata | Implement filters, paging, sort, scope, authorization, empty state, and parity cases. |
| `Ler detalhe` | `GET /<resource>/{id}`; `BaseResourceService.findById`; optionally `GET /by-ids` / `findAllById` | Choose stable public ID; keep `ROWID` internal unless explicitly accepted. |
| Lookups/options | `POST /<resource>/options/filter`; `GET /options/by-ids`; `OptionDTO`; `@UISchema(endpoint, filterField, sortField, optionsPageSize)` | Implement combo semantics and selected-value reloads used by the UI. |
| `Novo/Salvar` | `POST /<resource>`; `BaseResourceService.save` | Use direct platform save only when safe; otherwise route through a screen-specific legacy-backed service under the shared Ergon bridge. |
| `Editar/Salvar` | `PUT /<resource>/{id}`; `BaseResourceService.update` | Use command DTOs when read DTOs contain derived/internal fields; preserve legacy validation and side effects. |
| `Apagar` | `DELETE /<resource>/{id}`; `BaseResourceService.deleteById`; batch delete only when explicitly closed | Prove confirmation, permission, dependency blockers, no-mutation failures, and cleanup. |
| `Duplicar` | `POST /<resource>/{id}/duplicate-draft`; `DuplicateDraftResourceService.duplicateDraft`; `DuplicateDraftUtils`; `@UISchema(copyOnDuplicate)` | Generate an editable draft, then persist through `POST`; do not assume every copied field is allowed. Use `@WorkflowAction` only if runtime proves duplicate is a business command with its own immediate effect or dedicated workflow route. |
| `Cancelar` | No backend mutation | Record no-op proof and avoid adding a backend mutation endpoint. |
| `Documentos legais` | Separate related resource or linked component API using the same filter/detail/write pattern | Resolve link keys such as `PONTLEI` server-side and scope write only after parity is closed. |
| `Publicacoes/atos` / `Pendencias` | Separate related resource/workflow API; often backed by reusable legacy blocks or related transactions | Do not fold into the main resource unless XML/runtime evidence proves the same route. |

All resources must also expose or deliberately block the relevant schema and action metadata: `/schemas`, `/schemas/filtered`, `@UISchema`, HATEOAS/action links, and explicit `405`/`501` or omitted routes for unsupported operations. For legacy-backed reads/writes that depend on Oracle package state, keep the Praxis metadata/API controller/service contract while placing same-connection `HADES.FLAG_PACK` setup, cleanup, procedure calls, and Oracle error translation behind the shared Ergon bridge.

Praxis semantic contract rules for Ergon:

- Treat the resource endpoint, DTO, FilterDTO, schemas, options, `_links`, `/actions`, `/surfaces`, and `/capabilities` as one contract. Do not create parallel capability/action models for Ergon screens.
- Before creating a new endpoint, launcher, adapter, metadata field, action, surface, capability, option source, or Angular component, inventory the native Praxis support and classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only `lacuna-real-de-contrato` justifies a new Praxis contract request.
- Use the canonical owner map: `praxis-metadata-starter` owns `x-ui`, schemas, HATEOAS, actions, surfaces, capabilities, annotations, and resource-oriented metadata; `praxis-config-starter` owns `/api/praxis/config/**`, user config, AI registry, templates, ETag, and AI authoring contracts; `praxis-ui-angular` owns the official Angular runtime, components, adapters, launchers, materializers, editors, and dynamic fields; `praxis-api-quickstart` is an operational reference, not the semantic owner.
- Keep simple create/update/delete as resource operations when the write gate proves they are safe. Do not mark `POST`, `PUT`, or `DELETE` as `@WorkflowAction` only because the legacy UI had a button.
- Use `@ResourceIntent` for partial same-resource maintenance flows that are more specific than generic CRUD but still belong to the same resource contract.
- Use `@UiSurface` for discoverable UI experiences, read projections, related tabs, or embedded flows. A surface must point to a real resource/operation/schema path; it must not inline private SQL, HADES, `ROWID`, empresa, usuario, or session details.
- Use `@WorkflowAction` only for business commands such as approve, cancel business state, reopen, publish, generate pending work, or other non-CRUD commands with their own payload, availability, and parity evidence. Do not promote `Duplicar` to `@WorkflowAction` by name alone; ordinary duplicate remains `duplicate-draft + POST`.
- Expose availability through the canonical Praxis capability/action/surface machinery. For Ergon/HADES decisions, use the existing HADES starter/`HadesLegacyAccessGuard`/legacy bridge plus optional Praxis extension points such as `ActionAvailabilityRule`, `SurfaceAvailabilityRule`, and `ResourceStateSnapshotProvider`. Fail closed and expose only public availability, never the HADES/SQL/user/company reason.

Use these route safety states for write-like operations:

- `READ_PRAXIS_SAFE`: read/options behavior can be delivered by the standard Praxis metadata/API platform surface with parity evidence.
- `WRITE_TABLE_DIRECT_CANDIDATE`: direct platform/table write may be viable, but audit/parity is not closed.
- `WRITE_TABLE_DIRECT_SAFE`: direct platform/table write is approved for the exact operation because evidence proves no required rule/side effect is skipped, or all required behavior is covered by triggers/constraints/defaults/session-safe infrastructure and parity.
- `WRITE_DB_BACKED_REQUIRED`: the operation must use the validated DB-backed/legacy route to preserve behavior.
- `WRITE_BLOCKED`: missing or contradictory evidence prevents implementation.
- `WRITE_DEFERRED`: intentionally out of scope with risk recorded.

`WRITE_TABLE_DIRECT_CANDIDATE` does not authorize Java implementation. `WRITE_TABLE_DIRECT_SAFE` must be recorded in `write-route-decision.md`, `write-contract.md`, `write-parity-matrix.md`, and the phase gate.

Run the Praxis metadata/API contract review whenever a phase designs or changes DTOs, FilterDTOs, command DTOs, options, OpenAPI schemas, `@UISchema`, or `@Filterable`. Use `praxis-dto-annotations` for DTO annotation/metadata semantics and `ergon-fieldspec-ui-contract` for FieldSpec/Angular schema consumption. Also use `praxis-java-host-project` when creating or changing Java/Spring resources, and `praxis-resource-entity-lookup-backend` when the contract includes `RESOURCE_ENTITY`, `OptionSourceRegistry`, `OptionSourceDescriptor`, or `/option-sources/{sourceKey}`. The gate covers the API/schema/options contract.

When local migration docs provide `docs/migracao/backend-praxis-first-playbook.md`,
use it before Java contract or implementation work to choose the narrowest
backend shape: read-only resource, create/update resource, legacy-backed
resource, duplicate draft + POST, related `@UiSurface`, `@WorkflowAction`,
governed option source, dashboard/analytics resource, host/security boundary,
no backend mutation, blocked, or deferred. When the shape decision must be
auditable in a screen package, copy
`docs/migracao/backend-praxis-first-checklist-template.md` to
`docs/migracao/<SCREEN>/backend-praxis-first-checklist.md` and record the
operation state, Phase 1.5 decision, Praxis/Ergon resources reused, public
contract guardrails, route safety, and minimum validation. Do not use this
checklist to skip a phase or to promote a reference case; Phase 8 reference
promotion still uses `backend-praxis-reference-audit.md` and the reference
checklist.

## Parte 1 Scope

The Parte 1 scope is generating Java/Spring read and write APIs. This is the only active scope for this orchestration.

In this scope:

- the Praxis metadata/API contract review validates DTO, FilterDTO, command DTO, options, OpenAPI/schema, and `@UISchema` contracts exposed by the backend, and must record whether `praxis-dto-annotations`, `ergon-fieldspec-ui-contract`, `praxis-java-host-project`, and `praxis-resource-entity-lookup-backend` were applied or explicitly not applicable.
- Endpoint readiness means API execution evidence plus legacy/API/database parity.
- Phase 7 compares the authenticated legacy behavior against implemented endpoints and database effects.
- Phase 8 produces `backend-api-handoff.md` or `pilot-handoff.md`.
- When a Phase 8 backend screen is intended to become a reusable Praxis
  reference case, require `backend-praxis-reference-audit.md`. If
  `docs/migracao/backend-praxis-reference-quick-guide.md` exists, use it first
  to choose the reference shape; then read
  `docs/migracao/backend-praxis-reference-playbook.md` for the detailed
  boundary and create the audit from
  `docs/migracao/backend-praxis-reference-audit-template.md` when present,
  instead of copying the newest pilot blindly. The
  `phase-8-execution-gate.md` must record whether backend reference promotion is
  intended, which shape was selected, the audit state, whether the package may
  enter the quick guide/playbook as a reusable reference, the allowed wording
  when the state is `NOT_REFERENCE_READY`, the global guide checker result, and
  any gap that prevents unrestricted reuse. A functional Phase 8 handoff
  without this audit must not be advertised as a reusable Praxis backend
  exemplar. The
  current validated baseline is: `ERGadm00034` for partial mutable resource
  plus related surface, `ERGadm00036` for controlled CRUD pilot, `ERGadm00038`
  for an advanced scoped pilot with CRUD, canonical `@WorkflowAction` and
  read-only related `@UiSurface`, `ERGadm00039` for master-detail parent/child
  CRUD, `ERGadm00069` for mature CRUD pilot with browser replay, duplicate
  draft and cancel/no-op proof, and `ERGadm00229` for the scoped shared
  legal-document related-write slice. Full `ERGadm00229` remains
  not-reference-ready. `ERGadm00235` is a Phase 8 validated
  `NOT_REFERENCE_READY` control package for blocked calendario create/update
  boundaries; use it for learning what is missing, not as an implementation
  baseline. Treat all reusable cases as bounded references, not unrestricted
  full-screen templates.
  Before copying or promoting a backend reference, validate the selected screen
  with `tools/migration-factory/validate-phase-gate.ps1 -Screen <SCREEN> -Phase
  8 -MigrationRoot docs/migracao` and
  `tools/migration-factory/check-praxis-semantic-contract.ps1 -ScreenPath
  docs/migracao/<SCREEN> -Strict`. For a complete baseline refresh, run the
  quick-guide loop over `ERGadm00034`, `ERGadm00036`, `ERGadm00038`,
  `ERGadm00039`, `ERGadm00069`, `ERGadm00229`, and `ERGadm00235`, then run the
  strict semantic check over `docs/migracao`. If validation fails, do not
  promote the example; fix or downgrade the audit/gate first. If strict
  validation reports `BACKEND_REFERENCE_GUIDE_PROMOTES_NOT_READY`, treat it as
  guide/audit drift: a screen whose audit is `NOT_REFERENCE_READY` was described
  as a reusable reference or implementation baseline. Correct the quick
  guide/playbook wording to non-reference/control learning material, or reopen
  the screen audit and Phase 8 gate before promotion.

Denied/restricted-user fixtures are not per-screen blockers for migration.
For screens governed by the shared HADES/security bridge
(`ergon-hades-security-starter`, `ergon-legacy-bridge`,
`HadesLegacyAccessGuard`, `ErgonLegacyExecutor` or equivalent), absence of a
real denied principal must be recorded as `waived`/accepted risk or
`closed_by_bridge_contract`, not as `Blocked`. Never claim proven `403` parity
without an executed denied fixture. Reopen as blocking only when the screen
bypasses the shared guard/bridge, exposes company/user/profile/session context
publicly, implements custom security outside HADES, or product explicitly
requires a proven `403` release gate.

For a new screen, do not assume `docs/migracao/<SCREEN>` already exists. If the package or `migration-plan.md` is missing, create the initial screen package, produce `migration-plan.md`, produce `phase-0-execution-gate.md`, and keep the phase at Phase 0 until the intake target, backend module candidates, repository access, Oracle connection status, XML/export source status, legacy app/browser access, evidence-source availability, initial expected operations, risks, and next prompt are explicit. Phase 0 does not close the real functional scope; Phase 1 does that from observed legacy evidence and `operation-inventory.md`. Verify every cited local evidence path before presenting it as available; if a historical artifact exists only in Git history or is missing from the working tree, mark it as `HEAD-only`, `missing`, or `unconfirmed` instead of treating it as a local source. Do not start Phase 1, API contract, or Java implementation from the first prompt unless the user explicitly provides equivalent Phase 0 evidence.

Phase 0 is operational preparation for Phase 1. Before closing it, try to open the legacy `.tp` route, try to download/export the screen XML from the legacy app when credentials/session allow it, identify any local/classpath XML fallback, and test Oracle with a simple read-only probe when database credentials are available. If any of these cannot be done, record the exact blocker, impact on Phase 1, and next action. A Phase 0 with no usable XML/export/local fallback, no legacy browser access, and no Oracle access must be `Blocked`, not `Ready`.

When the repository provides `tools/migration-factory/download-runtime-xml.ps1`, use it as the preferred deterministic path for `.xml` runtime export before hand-written browser-text extraction. It parses the login form, resolves `form action`, keeps cookies in memory, validates the saved file with an XML parser, and writes sanitized evidence. Provide credentials only through an already-created `PSCredential` object or pre-existing environment variables such as `ERGON_LEGACY_USER` and `ERGON_LEGACY_PASSWORD`; never put literal secrets in the command. If the helper returns `RUNTIME_LOGIN_SAFE_INJECTION_REQUIRED`, then use browser login/manual login or ask for a safe credential injection path.

Legacy browser authentication is part of Phase 0 when credentials are provided in the active user message or the active private session. Do not stop at an unauthenticated HTTP `401`/`403` probe and defer login to Phase 1. First try to establish an authenticated browser/app session, then reopen the `.tp` route and retry the `.xml` export/download using the authenticated session/cookies. Never write credentials, passwords, tokens, or cookies to artifacts. Record only credential/session status such as `available in active session`, `login attempted`, `login succeeded`, `login failed`, `MFA/manual login required`, `export forbidden after authenticated login`, or `browser automation unavailable`.

For Cronos/Archon demo-style login, do not treat `HttpOnly` cookies as a blocker by itself. If the unauthenticated `.tp` returns a login HTML with a `SESSION` cookie and a login form, parse the actual `<form action>` and resolve it against the response URL using normal URL resolution. For example, `action="/login"` on `http://host/Ergon/Administracao/SCREEN.tp` means `http://host/login`, not `http://host/Ergon/login`. Do not invent `/Ergon/login`, `/Administracao/login`, or other login paths unless the HTML action or redirect actually points there.

Use an in-memory HTTP session/cookie container to:

1. request the `.tp` route and retain the `SESSION` cookie only in memory;
2. submit credentials to the resolved form action with the form field names observed in the HTML, commonly `username` and `password`;
3. request the matching `.xml` route with the same in-memory session;
4. save the XML only if the response is XML for the requested transaction and the saved file parses as XML, then record path, HTTP status, content type, byte size, SHA-256, parser result, and timestamp.

Do not write the username, password, cookie, Authorization header, request body, or connection string into artifacts, logs, command transcripts, screenshots, or generated scripts. Do not place credential literals in shell commands or reusable scripts. Prefer credentials already available through a local secrets/env file, environment variables, or the active browser login path.

If credentials are present only in the active conversation/session and no non-recording shell injection path exists, do not give up immediately. First use the in-app browser or Chrome login form when available, because typing into the authorized login page does not require putting the secret in a shell transcript. After browser login succeeds, retry `.tp` and `.xml` from the authenticated browser/session. If browser automation cannot submit the login safely, ask the user to log in manually or provide a safe credential injection method. Only then mark `RUNTIME_LOGIN_SAFE_INJECTION_REQUIRED`, `XML_RAW_EXPORT_NOT_SAVED`, `RUNTIME_XML_EXPORT_AUTH_BLOCKED`, or a similar residual.

Even when credentials cannot be submitted, parse the unauthenticated login HTML when available and record sanitized login mechanics: form action resolved URL, method, field names, HTTP status, and whether a `SESSION` cookie was issued. Do not record field values.

Never treat text copied from Chromium's XML viewer as raw XML unless it round-trips through an XML parser. The viewer can decode escaped markup inside attributes, for example `valor="&lt;div ...&gt;"` becoming `valor="<div ...>"`, which makes the saved text invalid XML. If a browser-derived file fails XML parsing, classify it as `RUNTIME_XML_BROWSER_TEXT_INVALID`, keep it only as diagnostic evidence, and rely on a raw response body, authenticated HTTP export, local XML, or HADES/Cronos source for structural discovery.

Only classify `.tp` or `.xml` as a non-blocking Phase 0 residual after one of these is true: authenticated login succeeded and the route/export still failed; browser login was impossible for a documented reason; or the user did not provide usable credentials. If credentials are available but login was not attempted, keep Phase 0 `Open` or `Blocked` with `RUNTIME_LOGIN_NOT_ATTEMPTED`; do not close it as `Ready for next phase with adjustments`.

Phase 0 must not perform technical XML discovery. It may record that a local XML/export/database source candidate exists and, when cheap, confirm screen code/title. It must not extract or promote grid SQL, filters, binds, links, components, `dataTable`, write routes, Oracle objects, or field lineage; those belong to Phase 1. The Phase 0 readiness matrix lists only backend/API modules and libraries needed for Java/Spring APIs.

Scaffold or factory scripts are convenience helpers only. Do not depend on them as the source of truth for Phase 0. If a scaffold/factory is missing, broken, or points to an absent template, continue by creating `migration-plan.md` and `phase-0-execution-gate.md` from the canonical repository templates, and record a non-business tooling residual such as `SCAFFOLD_UNAVAILABLE` with path, impact, and next action. A missing scaffold must not silently relax Phase 0 evidence requirements, must not justify skipping Oracle/XML/browser checks, and must not be recorded as a blocker for the business migration unless no canonical templates are available.

## Ordered Phases

1. **Phase 0 - Operational Preparation**
   - Define the screen/functionality to investigate, target backend/API module candidates, environment, repository access, database access, XML/debug source, legacy app/browser access, credentials availability, and initial expected user operations using the Standard Legacy Operation Inventory.
   - For Cronos/Archon screens, require a runtime XML export decision before Phase 1: `.tp` reachability, matching `.xml` export/download result, credential/session status, export permission status, parser-valid saved XML status, local XML path candidate, and whether the source-of-truth check is `ready`, `blocked`, or `deferred`.
   - If legacy credentials are available in the active session, attempt browser/app login before deciding `.tp` or `.xml` status. Reopen `.tp` and retry `.xml` after login. When the login page exposes a login form, resolve its real action URL and try the same flow with an in-memory HTTP session to persist the raw XML export. An unauthenticated `401`/`403` alone is not enough to defer authenticated runtime capture.
   - Test Oracle/banco with a simple read-only probe when credentials are available. Record the environment, success/failure, and whether Phase 1 can run Oracle/HADES checks.
   - Treat local XML as a source candidate only in Phase 0. Do not parse component lineage, grid SQL, filters, links, write `dataTable`, hidden fields, or route semantics in this phase.
   - Record only backend/API repositories and shared libraries required for Java/Spring API migration. Do not include visual/UI libraries as Phase 0 dependencies.
   - Do not store credentials in artifacts. Phase 0 may state that credentials are available for the active session, unavailable, invalid, or insufficient for XML export, but must not record usernames/passwords/secrets.
   - If credentials or authenticated runtime access are unavailable, close Phase 0 only with an explicit `RUNTIME_AUTH_BLOCKED` or `RUNTIME_XML_EXPORT_AUTH_BLOCKED` residual carried into Phase 1.
   - Treat scope as provisional in this phase. The real migration scope is closed in Phase 1 after observed legacy evidence.
   - Output: `migration-plan.md`.
   - Closeout: `phase-0-execution-gate.md`.

2. **Phase 1 - Legacy Screen Operation Inventory**
   - Use `ergon-archon-screen-discovery`.
   - Close browser/XML/runtime SQL, component lineage, read data sources, keys, authorization, session context, visible actions, related links, and write surface discovery for every standard operation.
   - When a local legacy XML exists, require an explicit source-of-truth artifact before closing Phase 1: produce `cronos-source-of-truth.md` comparing local XML evidence against authenticated runtime/debug evidence and HADES/Oracle registry or stored-resource candidates. For Cronos/ErgonNG, treat XML as import/export for database-persisted page structure; check transaction, controls, properties, screen pattern/customization tables, and user screen pattern before accepting the local XML. Keep local XML at `CONFIRMED_LOCAL_SOURCE` until runtime/HADES equivalence is proven. If HADES/Oracle is unavailable, the artifact must exist with a `Blocked` or `Partial` decision and the exact rerun command/query.
   - For Cronos bind semantics, do not block only on Chrome/browser automation when XML plus Oracle metadata can answer the question. If `sqlParameters`, the SQL predicate, a reused component or equivalent screen, and Oracle metadata/view source close the value semantics, record the bind as `BIND_SEMANTICS_CLOSED_BY_XML_ORACLE` and classify it as public filter, server-side scope, constant bind, parent-row context, or internal runtime parameter. Use `docs/migracao/phase1-cronos-bind-resolution-standard.md` when present. For standard Cronos `recordPanelEdit + dataTable`, XML plus local Cronos framework source may close create/update payload as `SOURCE_DERIVED_PAYLOAD_READY_FOR_DB_PROBE`; browser/runtime remains mandatory for visible workflow, action state, restricted users, final parity, and non-standard write actions whose payload is not source-derived.
   - If the browser workflow is not fully operated by Codex, require `runtime-capture-form.md` so the developer has a structured way to provide the missing visible/runtime facts. `browser-runtime.md` alone is not enough when it only infers behavior from XML. For process validation before developer handoff, an unoperated or partial visual workflow blocks Phase 1 readiness; do not close Phase 1 as `Ready for next phase` or `Ready for next phase with adjustments` while default load, runtime binds, selected-row/public-key proof, visible action state, and representative non-empty fixture/context are missing.
   - When the workspace provides `docs/migracao/phase1-scope-authorization-standard.md`, apply it before Phase 1 handoff. `allowed-default-context` may close from authenticated browser default load, non-empty fixture, selected-row public key, and same-connection Ergon/HADES Oracle context. For API-only screens governed by `ergon-hades-security-starter` and `ergon-legacy-bridge`, `company-scoped-context` and `restricted-user-context` close by the shared bridge/security contract and must not block each screen individually. Reopen them as blocking only when evidence shows a bypass of `HadesLegacyAccessGuard`/equivalent, `ErgonLegacyExecutor`/equivalent, public exposure of company/user/profile/security context, or custom security outside HADES. When the factory provides `new-phase1-scope-authorization-decision-pack.ps1`, generate the decision pack only for genuinely open scope/authorization cases; it structures owner approval/blocker evidence but does not make the gate Ready by itself. Do not expose company/user/profile/session context as public FilterDTO, schema, URL, option payload, or x-ui fields.
   - Require HADES registry/access/stored-resource coverage before Phase 1 can close. This can be executed evidence or an explicit blocked SQL/helper artifact, but a gate with `HADES_REGISTRY_NOT_CHECKED` must not advance to Phase 1.5.
   - `operation-inventory.md` must use deterministic states (`Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred`, `Not present`) instead of generic `Unknown`.
   - Output: `investigation.md`, `component-lineage-matrix.md`, `browser-runtime.md`, `runtime-capture-form.md` when needed, `cronos-source-of-truth.md`, `legacy-doc-sources.md`, `closure-checklist.md`, `operation-inventory.md`, `read-parity-matrix.md`, `write-risk.md`/`write-api-handoff.md` when writes exist, Oracle/HADES SQL and outputs when applicable.
   - Closeout: `phase-1-execution-gate.md`.

3. **Phase 1.5 - New Platform Reuse Discovery**
   - Search the new Java/OMS modules before proposing new endpoints.
   - For each operation/resource, decide `reuse`, `extend`, `create`, `block`, `defer`, or `not-api`.
   - Treat this as a lightweight routing gate, not implementation or parity: use targeted repository searches, record commands and findings, and do not require build, endpoint execution, Oracle, browser, or legacy/API comparison in this phase.
   - Separate `found` from `compatible`. A controller, DTO, service, endpoint, or option source that is only name-similar is not enough for `reuse`; if the Praxis metadata/API contract or legacy semantics are partial, choose `extend`, `create`, `block`, or `defer`.
   - Apply `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` before marking DTO/schema/options findings as compatible; record the review in `platform-reuse-inventory.md`.
   - For LOV/options, first generate or refresh `docs/migracao/platform-option-sources.md` with `tools/migration-factory/export-platform-option-sources.ps1 -Force` when that helper exists. Use it with `docs/migracao/options-lov-promotion-status.md` before creating new source backlog or blocking generic option discovery. Record `generatedAt`, covered property files/modules, and promotion status source in the gate or `platform-reuse-inventory.md`. Classify matches as `PLATFORM_OPTION_SOURCE_RESOLVED`, near matches as `PLATFORM_OPTION_SOURCE_REVIEW_REQUIRED`, and missing sources as `PLATFORM_OPTION_SOURCE_BACKLOG_REQUIRED` only when the target microservice/module was covered. Treat review-required as `extend` by default; use `block` only when a concrete gap such as missing selected-value reload or required dependency prevents the current screen contract. A dependent source is not `RESOLVED` from `filter` evidence alone; prove self-contained `GET .../by-ids` or contextual `POST .../by-ids` with the dependencies the Angular runtime will actually send.
   - Inspect endpoint constants, controllers, resource/query services, response DTOs, FilterDTOs, command DTOs, duplicate-draft DTOs, option DTOs/sources, mappers, repositories/entities, `/schemas/filtered`, `x-ui`/`@UISchema`, `@Filterable`, options/by-ids support, OpenAPI/schema tests, authorization/scope services, shared legacy context services, and already migrated related-screen resources.
   - For each operation, record DTO role coverage and Praxis metadata/API evidence: response DTO, FilterDTO, create/update command, duplicate draft, option DTO/source, mapper/projection, route, schema evidence, option reload, scope/authorization, semantic fit, and required extension.
   - Keep write-like operations (`Novo`, `Editar`, `Apagar`, `Duplicar`, legal documents, publications, pending flows) below implementation readiness unless Phase 4/5 gates are already closed. Phase 1.5 may identify reuse/extension candidates, but write route safety remains Phase 4/5.
   - Output: `platform-reuse-inventory.md` with search terms, executed commands, found/compatible/score, decision per operation, DTO role coverage, Praxis metadata/API evidence, duplicate-endpoint blockers, and Phase 2 gaps; plus candidate `api-contract.md` decisions that point to existing resources when reusing or extending.
   - Closeout: `phase-1-5-execution-gate.md`.

4. **Phase 2 - Read/Options API Contract**
   - Use `ergon-archon-read-api-migration`, `praxis-dto-annotations`, `ergon-fieldspec-ui-contract`, and the Praxis metadata/API contract gate. Add `praxis-resource-entity-lookup-backend` for governed option sources and `praxis-java-host-project` when the contract will create or change a Java/Spring resource.
   - Convert closed read candidates into Java/Spring contracts for `Consultar/listar`, `Ler detalhe`, `by-ids`, lookups/options, schemas, and read-only related tabs in scope.
   - Consume `platform-reuse-inventory.md`: each operation must carry the Phase 1.5 decision (`reuse`, `extend`, `create`, `block`, `defer`, or `not-api`) into the API contract.
   - Close the Praxis metadata/API contract for endpoints, request DTOs, response DTOs, `/schemas/filtered`, `x-ui`/`@UISchema`, `FilterDTO`, `@Filterable`/relation semantics, options/by-ids or governed option sources, public keys, server-side scope, and authorization.
   - Keep write-like operations blocked or deferred until Phase 4/5; Phase 2 may define read-only metadata around them only when explicitly in scope.
   - Output: finalized `api-contract.md` using the repository template when available, `ui-contract-checklist.md`, `read-parity-matrix.md`, and Phase 3 test plan.
   - Closeout: `phase-2-execution-gate.md`.

5. **Phase 3 - Read/Options Implementation And Parity**
   - Use `ergon-archon-read-api-migration`, `praxis-dto-annotations`, `praxis-java-host-project`, and `ergon-fieldspec-ui-contract` before creating or changing DTOs, FilterDTOs, OptionDTOs, resources, services, annotations, schema tests, or x-ui metadata. Add `praxis-resource-entity-lookup-backend` for governed option sources.
   - Implement only the read/options contracts whose gates are closed.
   - Execute implemented endpoints with recorded payloads and responses for `POST /filter`, `GET /{id}`, `/by-ids`, `/options/filter`, `/options/by-ids`, and schema endpoints when applicable.
   - Output: code/tests, OpenAPI/schema tests, API tests, endpoint execution evidence, and `read-parity-results.md`. Include `x-ui` tests when the backend contract exposes UI metadata.
   - Closeout: `phase-3-execution-gate.md`.

6. **Phase 4 - Write Audit By Operation**
   - Use `ergon-table-rule-audit` and `ergon-archon-write-api-migration`.
   - For every write-like operation, close payload capture, target routines/tables, generated DML, triggers, product/client rules, EP/EPA hooks, audit, pending, publications, legal documents, HADES dispatch, and nested dependencies.
   - Treat this as an Ergon write framework audit, not a simple table audit. Apply the checklist in `docs/migracao/phase-4-write-framework-checklist.md` when available.
   - Before closing this phase, require a product/client execution matrix for each target table phase. The matrix must distinguish package EPs (`EPB__<TABLE>`, `EPA__<TABLE>`) from trigger EPs (`EP_TRG_B_<TABLE>`, `EP_TRG_A_<TABLE>`), identify the effective HADES branch, record `P_MENS`, record whether `v_ep` can skip a product block, and list product rules inside and outside `IF v_ep THEN`.
   - Classify each write operation as `WRITE_TABLE_DIRECT_CANDIDATE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`. Do not close Phase 4 with a direct-table candidate when HADES/client hooks, package-only rules, session context, side effects, or error precedence are unknown.
   - Output: `write-risk.md`, `write-api-handoff.md`, and audit summaries under `oracle-results/table-rule-audit/`.
   - Closeout: `phase-4-execution-gate.md`.

7. **Phase 5 - Write Contract By Operation**
   - Use `ergon-archon-write-api-migration`, `praxis-dto-annotations`, `ergon-fieldspec-ui-contract`, and the Praxis metadata/API contract review. Add `praxis-resource-entity-lookup-backend` for governed option sources and `praxis-java-host-project` when the contract will create or change a Java/Spring resource.
   - Before closing a public write contract, require explicit write payload evidence: `write-payload-evidence.md`, `write-payload-fixture-request.md`, or `factory/*write*payload*.md/json`. The artifact must capture or source-derive the operation payload, operation discriminator such as `P_OPER`/`_op`, hidden/internal values kept server-side, error shape, fixture and cleanup/read-after-write plan. If this evidence is missing, create the request/artifact and close Phase 5 as `Blocked`; do not infer command DTOs from table-rule audit alone.
   - Produce per-operation contracts for `Novo/Salvar`, `Editar/Salvar`, `Apagar`, `Duplicar`, `Cancelar`, legal documents, publications, pending flows, and any screen-specific action.
   - Decide legacy route, bridge use, command DTOs, request schemas, public key strategy, blocked/deferred behavior, error mapping, and parity matrix.
   - Include or link the product/client execution matrix. Each operation must state whether the active route is `product only`, `client + product`, `client replaces gated product block`, `client blocks by P_MENS`, `inactive`, or `blocked`.
   - Record one final route safety state per operation: `WRITE_TABLE_DIRECT_SAFE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`. `WRITE_TABLE_DIRECT_SAFE` requires route evidence, rule coverage, side-effect coverage, error mapping, cleanup, and parity evidence; otherwise choose DB-backed or blocked.
   - Output: `write-payload-evidence.md` or a documented payload blocker/request, `write-contract.md`, `write-route-decision.md`, `plsql-error-map.md`, `write-parity-matrix.md`, and updated `ui-contract-checklist.md`.
   - Closeout: `phase-5-execution-gate.md`.

8. **Phase 6 - Java Implementation By Operation**
   - Use `ergon-archon-write-api-migration`, `praxis-dto-annotations`, `praxis-java-host-project`, and `ergon-fieldspec-ui-contract` before creating or changing command DTOs, request/response DTOs, resources, services, annotations, schema tests, actions, capabilities, or x-ui metadata. Add `praxis-resource-entity-lookup-backend` for governed option sources.
   - Implement only operations with closed contracts, reusing/extending existing new-platform resources when Phase 1.5 requires it.
   - Output: code, OpenAPI/schema tests, API/service tests, parity tests, and explicit blocks for remaining operations. Include `x-ui` tests when the backend contract exposes UI metadata.
   - Closeout: `phase-6-execution-gate.md`.

9. **Phase 7 - Quality Round 2**
   - Operate the authenticated legacy screen and compare its visible filter/detail/options behavior against the implemented endpoints.
   - For each case, record legacy steps, equivalent HTTP request, payload, status, row counts, ids/keys, visible fields, labels, ordering, paging, empty state, messages, and database effects for writes. Record Praxis metadata/HATEOAS/action state only when it is part of the exposed backend contract.
   - For implemented writes, execute API-level success and negative probes even when legacy browser parity is blocked: validation failure with no mutation, missing target, duplicate/conflict when applicable, read-after-write/read-after-failure, before/after counts, and final zero-count cleanup for disposable fixtures.
   - If the legacy `.tp` route or browser is unreachable, record the exact route, error, date, and impact. API probes may improve evidence but do not close visible legacy parity or authorize final handoff unless an explicit waiver is recorded.
   - Classify divergences as `bug`, `accepted gap`, `deferred`, `fixture issue`, or `legacy-only`.
   - Output: `quality-round-2.md`, browser/API evidence, and legacy-vs-endpoint comparison matrix.
   - Closeout: `phase-7-execution-gate.md`.

10. **Phase 8 - Final Parity And Handoff**
   - Consolidate API, legacy, and database side-effect parity.
   - Include dependency parity and fixture cleanup proof for writes that can create association, pending, publication, legal, audit, or generated-detail rows.
   - Output: `parity-results.md`, residual risks, deployment decision, `backend-api-handoff.md` or scoped `pilot-handoff.md`, and skill/process updates when reusable learning was found.
   - Closeout: `phase-8-execution-gate.md`.

## Phase Gate Policy

Use [phase-gates.md](references/phase-gates.md) when deciding readiness. A phase can be:

- `Open`: still being investigated.
- `Blocked`: missing evidence or access prevents a safe decision.
- `Ready for next phase`: required artifacts are present and reviewed.
- `Ready for next phase with adjustments`: required scope works, but non-blocking residuals are named with owners and must be carried into the next phase/handoff.
- `Deferred`: intentionally postponed with explicit risk.

## Required Handoff

Use [artifact-contract.md](references/artifact-contract.md) to verify that the next skill has everything it needs. Do not start Phase 2 if read candidates lack SQL/binds/keys/scope evidence or if Phase 1.5 has not decided whether each candidate should reuse, extend, or create new Java/OMS resources. Do not start Phase 5 if `write-api-handoff.md` or `operation-inventory.md` lacks write actions, routines/tables, payload evidence, public key strategy, session context, blockers, target operation status, or Phase 4 table-rule summaries for every target and side-effect table in scope.

## Recommended Next Step Logic

When the user asks "qual proximo passo recomendado?":

1. Identify current phase from existing artifacts.
2. Check the gate for that phase.
3. If gate is open, recommend the smallest action that closes the highest-risk missing artifact.
4. If gate is closed, recommend the next phase and the first skill/prompt to run.
5. State whether Java implementation is allowed or blocked.

When the user says only `continuar`, `seguir`, `ok`, `1`, or `proximo`, treat it as consent to execute the latest gate's recommended next phase if the latest gate is ready. If the latest gate is not ready, explain the blocker and recommend the smallest corrective action.

For UI-specific continuation after backend/API phases, prefer the canonical
screen UI gate when present:
`docs/migracao/<SCREEN>/ui-execution-gate.md`. Historical files such as
`phase-6-5-ui-execution-gate.md` may remain as evidence, but new UI packages
should close with `ui-execution-gate.md`. If the gate state mentions a
temporary drawer residual such as `REFERENCE_PARTIAL_PENDING_DRAWER`, carry that
residual explicitly and do not promote the screen as a final reusable Praxis UI
reference until the drawer workaround is removed and strict validation passes.

When the current or recommended next step mentions backend reference case,
example screen, Praxis exemplar, reusable pilot, or Phase 8 hardening, read
`docs/migracao/backend-praxis-reference-quick-guide.md` when present, then read
`docs/migracao/backend-praxis-reference-playbook.md` for the detailed boundary.
Use these artifacts to select the reference shape and require or update
`backend-praxis-reference-audit.md` before promoting any screen as
`REFERENCE_READY`, `REFERENCE_READY_WITH_GAPS`, or `NOT_REFERENCE_READY`.
When `docs/migracao/backend-praxis-reference-audit-template.md` exists, use it
as the starting shape for new audits; use filled audits only as examples for
the selected reference family. Validate the selected screen's Phase 8 gate and
strict Praxis semantic contract before reusing it as migration guidance; common
blockers are stale Phase 8 gates, unacknowledged historical Oracle errors,
mojibake, missing `Praxis Platform Follow-up`, audit/handoff mismatches, and
`BACKEND_REFERENCE_GUIDE_PROMOTES_NOT_READY` when a `NOT_REFERENCE_READY` audit
is promoted by global guide wording.

When the current or recommended next step mentions Angular UI reference case,
Praxis UI exemplar, UI factory acceleration, or ERGadm00034 as an Angular case,
read `docs/migracao/ERGadm00034/ui-praxis-reference-package-20260702.md` when
present, then read `docs/migracao/ERGadm00034/ui-execution-gate.md`. For
post-`@praxisui/* 9.0.0-beta.33` hosts, the desired Angular reference shape is
schema-driven table/detail/forms plus `CrudLauncherService` with
`openMode='drawer'`, without a host-owned `command-drawer` shell. If the gate
state is `REFERENCE_CANONICAL_CODE_READY_PENDING_AUTHENTICATED_QA`, code and
static validation may be reused as a pattern, but final visual promotion still
requires authenticated QA. Before promoting any Angular screen as a reusable UI
reference, run the static checker
`tools/migration-factory/check-angular-praxis-reference-pattern.ps1`; use
`-Strict` for final canonical references and `-AllowTemporaryDrawer` only for a
documented legacy in-progress exception.

Treat `Read handoff ready; write deferred` as a closed Phase 1 state for read-first migration when runtime binds, public key strategy, authorization/scope, same-connection session context, and evidence-backed write deferral are present. In that state, recommend Phase 2 read API migration and keep write audit/contract/implementation blocked until Phases 4-6.

Do not treat Phase 1 as read-ready until Phase 1.5 has searched the new Java/OMS codebase for existing resources and separated `found` from `compatible` per operation. If an endpoint, option source, DTO, schema, or related service already exists, recommend reuse only when the Praxis metadata/API contract and legacy semantics are compatible; otherwise recommend extension, creation, block, or deferral with the semantic gap documented.

Do not treat Phase 4 as closed for any write operation until the table-rule audit has a product/client execution matrix. The matrix must answer: which EPs are package-level, which EPs are trigger-level, whether HADES executes simple or multiple EPs, whether the client branch is active, whether `P_MENS` can block, whether `v_ep` can skip product validation, and which product rules are outside the `v_ep` gate.

Do not treat Phase 5 as ready for Java implementation until `write-contract.md` or `write-route-decision.md` consumes that matrix and a write payload evidence artifact exists for the operation. If the contract only says "HADES active/inactive" but does not say how that affects product execution, or if payload/error/fixture evidence is missing, keep the operation `Blocked`.

Do not treat direct table/Praxis CRUD as safe merely because the table has triggers or no obvious PL/SQL routine. Direct write is implementation-ready only when the operation is explicitly `WRITE_TABLE_DIRECT_SAFE`. If the operation is only `WRITE_TABLE_DIRECT_CANDIDATE`, recommend the next Phase 4/5 audit or probe instead of implementation.

Do not treat a DTO/FilterDTO/command/options contract as closed until the API contract has verified payload shape, schema metadata, options semantics, and request/response behavior. In particular, remote selects need options endpoints and `filterField`/`sortField`; date ranges need array payload semantics; controls such as `rangeSlider` need explicit backend/schema proof before handoff.

Treat `Implemented with automated backend tests; smoke-tested` as implementation progress, not contract or handoff closure. For reads it is Phase 3 progress until legacy/API comparison closes; for writes it is Phase 6 progress until API parity, side-effect/cleanup evidence, and Phase 7 comparison are recorded. Recommend expanding backend parity: filter variations, empty result, company isolation, authorization helper predicates, and OpenAPI/schema assertions. If a denied/restricted-user fixture exists, it must prove rows are hidden or forbidden before any `403` parity claim. If no valid denied principal exists, record waiver/accepted risk and continue; do not block the screen.

For write pilots, prefer this sequence after the first successful slice:

1. Update the shared skill/process with newly proven legacy behavior before starting another screen.
2. Harden the shared bridge if the same connection/context/error-mapping code is reusable.
3. Add or update route-decision and parity templates so the next operation checks `ERG_DML_*`, direct DML, writable views, dependency blockers, and cleanup paths consistently.
4. Only then start the next migrated operation or screen.

Treat a write pilot as closed only when implementation evidence and API parity evidence are separated clearly. A closed pilot should have API result artifacts for success and representative negative cases, Oracle target/side-effect counts before and after each mutation, final zero-count cleanup proof for disposable fixtures, and a parity matrix section listing every deferred flow by name. Do not treat "implemented locally" or "PL/SQL probe passed" as pilot closure without API smoke evidence.

After Phase 3 read/options implementation and parity are closed, and writes are not yet audited, recommend Phase 4 runtime write payload capture and table-rule audit as the next step. Capture `Novo`, `Editar`, `Apagar`, `Duplicar`, `Salvar`, `Cancelar`, hidden keys/`ROWID`, `P_OPER`, `P_ROWID_REG`, `PB_*`, `PP_*`, `P_MENS`, validation messages, and cancel/no-op behavior before drafting Phase 5 command DTOs or endpoints.

After the first Phase 6 write pilot implementation, prefer API-level parity closure before moving to another screen: success create/delete, validation failure, duplicate/collision when applicable, permission denial when a real user fixture exists, read-after-write/read-after-delete, and cleanup proof. If no real denied user fixture exists, record an accepted-risk waiver instead of blocking the screen. If dependency blockers, pending, publication/legal, update, duplicate-button, or cancel/no-op are not in the pilot, require explicit deferrals in `write-parity-matrix.md` and `closure-checklist.md`.

After Phase 6 implementation, recommend Phase 7 Quality Round 2 before handoff. The agent must use the authenticated legacy browser session to execute representative filters/selections and compare them with the implemented endpoints, especially `POST /filter`, `GET /{id}`, `/by-ids`, and `/options/*`. For writes, the agent must also run API success/negative probes and cleanup evidence for implemented operations. Do not promote the screen when visible legacy behavior differs from the endpoint, or when the legacy route is unreachable, without an explicit accepted gap, deferral, or waiver.

When endpoints are already implemented, recommend an Endpoint Execution Parity pass before any handoff decision if the evidence is only static. That pass must execute the endpoints, capture payloads/responses, validate the exposed API contract metadata, and compare with the authenticated legacy screen using the same user/company/context and filters. If the legacy comparison cannot run, record the exact fixture/access blocker and keep the endpoint below `Verified`.

## User Guidance

For a didactic PT-BR roadmap with examples of prompts and diagrams, load [pt-br-roadmap.md](references/pt-br-roadmap.md).
