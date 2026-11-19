---
name: praxis-crud-runtime-openmodes
description: "Use when implementing or auditing `@praxisui/crud` runtime orchestration, including `PraxisCrudComponent`, `CrudMetadata`, `crudContext` stability, `CrudLauncherService`, route/modal/drawer open modes, `DynamicFormDialogHostComponent`, drawer adapter token, table/form handoff, bulk execution cancellation and terminal states, capabilities/HATEOAS action launching, schemaUrl/submitUrl binding, and CRUD consumer validation."
---

# Praxis CRUD Runtime Open Modes

Use this skill for the canonical CRUD runtime. CRUD owns the orchestration of table, form launchers, resource actions, open modes, refresh after save/delete, and stable handoff between child components.

Pair with `praxis-crud-drawer-adapter-contract` when drawer mode or the lightweight adapter entrypoint is involved. Pair with `praxis-crud-dialog-form-host-lifecycle` when modal/drawer dynamic-form hosting, result propagation, or refresh-after-save/delete is involved.

## Required Source Audit

Inspect:

- `projects/praxis-crud/AGENTS.md`
- `README.md`
- `docs/host-crud-runtime-and-openmode.md`
- `docs/adr/2026-03-drawer-adapter-light-entrypoint.md`
- `src/public-api.ts`
- `drawer-adapter/public-api.ts` when drawer adapter changes
- `src/lib/praxis-crud.component.ts`
- `src/lib/praxis-resource-page.component.ts` and its focused spec
- Core's `projects/praxis-core/src/lib/services/enterprise-runtime-context.service.ts`
  when enterprise context lifecycle is involved
- `src/lib/crud-launcher.service.ts`
- `src/lib/dynamic-form-dialog-host.component.ts`
- `src/lib/drawer.adapter.ts`
- `src/lib/crud.types.ts`
- focused specs for launcher, dialog host, drawer adapter, and component metadata

## Runtime Boundary

- `PraxisCrudComponent` owns CRUD context, table handoff, selected row, collection links/capabilities, authoring entrypoint, schema-driven `kpiBand` (auto-enabled on `@praxisui/crud@10.0.0-rc.53+` as `{ enabled: true, source: 'schema' }` when `kpiBand` is `undefined`, not `inspect-only`, and the schema/capabilities publish `resourceFacts` or `stats.supported === true`, opting out cleanly via `kpiBand: false` or `{ enabled: false }`; fetches `/schemas/filtered` + `/stats/group-by` or `/filter?page=0&size=1` to synthesize total, `@ResourceFact` `fact:*`, and `@QuickFilter` `qf:*` cards), collection `PARTIAL_FORM` intent surfaces, and enriched toolbar actions (`tone`, `icon`, `modifiedFields`, `disallowedStateReason`).
- `PraxisResourcePage` (`<praxis-resource-page>` on `@praxisui/crud@10.0.0-rc.53`) owns the zero-code resource page header, scope bar (including auto-promotion of schema-derived `x-ui.inlineFilter` criteria when quickFilters exist), KPI band synchronization, `[lockedFilterFields]` / `[schemaFields]` forwarding, contextual Decision Inspector action, and ambient `PraxisWorkspaceQueryContextService` + `PraxisContextFilterProjectorService` re-projection (updating filters and locks in place without destroying DOM via `identityRenderKey`).
- `PraxisDossierPageComponent` (`<praxis-dossier-page>`) provides the turnkey 360° entity dossier: identity hero with metadata chips and LGPD sensitive-field reveal toggle, sibling switcher (`siblingRecords`), capability sync (`refreshItemDiscovery`), embedded view `<praxis-dynamic-form>` (`showRecordFormToggle`), overview tab, and child `<praxis-crud>` tabs pre-wired with `[lockedFilterFields]`.
- `CrudLauncherService` owns open-mode resolution and launch behavior, automatically hydrating saved `praxis-form-config-*` layouts from `ASYNC_CONFIG_STORAGE` (when not explicitly `persistence: 'transient'`) across modal, drawer, and surface launches without host-local launcher wrappers.
- `DynamicFormDialogHostComponent` owns modal/drawer form host wiring to `PraxisDynamicForm`.
- `CRUD_DRAWER_ADAPTER` is the canonical host adapter seam for real drawer implementations.

Do not rebuild CRUD drawers, modals, or table/form launchers in apps when the missing behavior belongs to `@praxisui/crud`.

## Open Mode Rules

- Resolve mode with precedence: action metadata, CRUD defaults, global CRUD defaults, then route fallback.
- Route mode requires `route`.
- Modal/drawer modes require `formId`, unless the canonical CRUD operation can be inferred.
- Drawer mode uses `CRUD_DRAWER_ADAPTER` when provided; otherwise it falls back to the package dialog host with drawer presentation.
- Host adapters must import from `@praxisui/crud/drawer-adapter`; the adapter seam must not become a second CRUD runtime.
- Save/delete results must propagate back to `PraxisCrudComponent` so outputs and table refresh stay component-owned.
- `form.submitUrl` and `form.submitMethod` must appear together.
- `actions[].params` maps row/context values into route/query/input and is not persistence.
- When an action lacks an explicit open binding, prefer discovered CRUD surfaces/actions from capabilities, HATEOAS links, `/schemas/surfaces`, and `/schemas/actions` before falling back to legacy launcher behavior. If an explicit route/modal/drawer binding exists, preserve it and do not refetch discovery just to override the host contract.
- Treat discovery and launcher resolution as sequential decision stages, not retry mechanisms. The launcher fallback is valid only when discovery did not select an executable surface. Once a canonical surface is selected, synchronous or asynchronous materialization/open failure must fail closed without emitting a second toolbar/row action or launching another drawer, modal, or route.
- A table with `crudContext` delegates canonical create/open actions to `PraxisCrudComponent` before any standalone `surface.open` attempt. A standalone table owns exactly one `surface.open` attempt. Correlate request/failure diagnostics with `actionId`, `surfaceId`, mode, resource path, selected path, normalized cause, and `fallback=none`; do not include row data, form payloads, headers, or raw stacks.
- Treat `openMode`, visible row/toolbar actions, and injected CRUD affordances as orchestration evidence only. Availability and executable permission come from capabilities, links, surfaces, actions, and adapter payloads; do not infer workflow permission or backend side effects from a drawer/modal opening or a button label.
- Keep `crudContext` stable; avoid getters or object literals that recreate context each change detection cycle.
- `CrudMetadata.interactionMode='inspect-only'` is the canonical public-local
  inert mode. It suppresses derived and declared operational actions, launchers,
  remote resource/capability discovery, config persistence, and externally
  injected create/view/edit/delete events while retaining purely local
  sort/filter/pagination. Incompatible resource paths, actions, forms, or open
  modes produce diagnostics; they do not silently re-enable execution.
- The `public-local-inspect-only` runtime profile proves a closed local shape
  with `effects: []`. The host still evaluates policy and must not treat a
  matching profile as authorization.

## Duplicate Draft And Seeded Create

Inspect `tryHandleCanonicalDuplicateDraftAction`, the launcher input mapping,
`crud-form-route.ts`, `crud-route-form-handoff.service.ts`, the routed host and
their Router specs before documenting this flow. Follow the row's published
`duplicate-draft` link and canonical create availability/link. Recheck live links,
identity and runtime denials after the POST. Missing link, denial, invalid draft
or preparation failure must stop with localized feedback, without generic workflow
fallback or an empty create form. Reuse the existing opening guard and invalidate
late work on destruction/context changes.

The backend owns the field allowlist, clearing and defaults. CRUD clones the DTO
and launches CREATE with request schema and POST submit, not the source identity
or an update target. Source identity belongs in `contextIdentity`; new-record
`resourceIdentity` stays unset. Use localized copy title/guidance/submit and return
overlay focus to a surviving origin control. Cancel/discard sends no create.
Form's explicit object `initialValue`, including `{}`, suppresses omitted defaults
even in rebuild, preserving false/null and compatible edits. No object seed keeps
ordinary create defaults; the submit pipeline can still omit untouched optional null.

For seeded route create, hosts must adopt public `createCrudFormRoute({ path,
formId, resourcePath })` from `@praxisui/crud`. Generic edit/view routes remain
host-owned and read their entity. The private CRUD handoff stores payload in
memory and sends only an opaque `NavigationExtras.info` marker; claim requires
one matching navigation/final URL/formId/resource/context. Never use a shared
`Symbol.for` slot, URL/history/storage payload, or a new Form/Core seed API.
Back/reload/direct access without a new handoff is unavailable. Do not cache or
detach this destination with custom route reuse. Normal source teardown after
successful guards allows transfer; destination owns lifetime/context after claim.
Redirect, rejection, cancellation and context invalidation release pending data.
Preserve explicit `enableCustomization=false` and true in the private payload;
absence alone selects the host's global fallback, outside DTO/authoring state.

`AbortSignal` on launcher/dialog/adapter is optional and cooperative. External
adapters must honor it; an obsolete pending `surfaceRuntime.push` can only be
closed once its ref resolves. Do not promise universal cancellation. Each Form
owns its local mutable `GenericCrudService` and `FormContextService`; preserving
the ancestor injector does not reuse that client. Copy chrome localization does
not prove full Form i18n: generated “Informações” in the layout service remains
an owner-specific runtime follow-up, while domain labels remain host data.

Validate changed behavior with the duplicate component/launcher/Router/customization
and Form seed/rebuild specs, plus the focused three-mode browser fixture when
runtime changes. For prose-only reconciliation, inspect those sources/evidence
and run doc/skill gates without repeating full Java/Angular suites. Keep local,
mock/browser, real backend integration and published-consumer evidence separate.

## Row Selection And Analytical Drawers

Inspect `PraxisCrudComponent`'s derived table configuration and Table's
`shouldOpenAnalyticalDrawerOnRowClick` before assuming that a row click only
selects a record. CRUD can automatically enable the analytical drawer when its
default or an action uses `openMode='drawer'`; Table can also open a registered
resource drawer. Row selection and drawer opening are separate effects of the
same click. Declaring `outputs.rowClick='emit'` exposes the output; it does not
disable the drawer.

When the authored journey uses a row click to select a record and update a
master/detail dossier, declare
`metadata.table.behavior.drawer.openOnRowClick=false` in the canonical CRUD
recipe. Preserve explicit create/view/edit drawer actions. If the journey uses
a dedicated selection control, exercise that control instead. Do not force-click
through a backdrop, close an unexplained drawer in the test, or change the shared
runtime default to hide a composition defect.

Keep the semantic authoring plan, compiled page and consumer projections aligned.
Prove plan/page parity, selection updating the dossier without an analytical
drawer, and explicit view/edit actions still opening their intended surfaces.
Use the actually adopted SDK: a newer source checkout does not prove that an
older public package implements the same opening policy.

For remote read-only analytical or inquiry resources wired through `<praxis-crud>`
or `<praxis-resource-page>` with `resourcePath`, keep `interactionMode: 'interactive'`
with `selection.enabled: false` (and `openOnRowClick` / `360°` drawer enabled as
needed). Never set `interactionMode: 'inspect-only'` on a remote-backed table
without static `dataSource.data`, because `'inspect-only'` suppresses remote HTTP
execution fail-closed. When the host bootstraps `providePraxisDecisionInspector({ rulesStudioUrl })`
from `@praxisui/visual-builder`, `<praxis-resource-page>` also exposes the native
contextual business-rules inspector inside `SURFACE_DRAWER_BRIDGE` without host-local
glue components.

## Resource Page Context Lifecycle

Consume `EnterpriseRuntimeContextService.contextChanges$` rather than a private
host/global identity event. ResourcePage observes confirmed context; it does not
load context or infer tenant/persona authority from `context`, `crudContext`,
storage values or UI labels. Keep host simulations host-owned: their declarative
remount is not a confirmed platform context.

Distinguish bootstrap from invalidation. An unconfigured runtime's initial null
snapshots and first ready bootstrap keep the existing child. An unchanged
confirmed identity also keeps local scope/filter state. Non-ready snapshots, or
null snapshots after confirmation, hide/destroy the obsolete CRUD until a ready
effective context is confirmed; do not queue a
microtask that reopens it regardless of confirmation.

Compare the canonical identity/version fields, including selection version, user,
tenant, profile and effective context version. A confirmed change recreates the
child and restores the configured default scope and its actual filter. A render
counter alone does not recreate Angular children: track the key in the control
flow that owns the CRUD view. Unsubscribe on destruction and prove that later
context emissions cannot restore or mutate a destroyed page.

Use the ResourcePage spec to assert actual child destruction/replacement,
bootstrap/unchanged preservation, context-version changes, invalidation/recovery,
default-filter restoration and cleanup. Validate the real consuming route/host
when identity switching changes runtime behavior; a stub spec or a dispatched
browser event cannot prove consumer adoption. Inspect the installed package and
integrated source before promising this lifecycle in an older published version.

## Bulk Cancellation And Observation

Inspect both `praxis-bulk-operation-dialog.component.ts` and
`praxis-bulk-edit-dialog.component.ts`, their shared `praxis-bulk-dialogs.spec.ts`,
the CRUD i18n catalog and Core's `PraxisBulkClientService`. Correct shared
transport timing in Core and dialog state projection in CRUD.

Own one polling subscription per observed execution. A cancellation response
with `CANCEL_REQUESTED` does not finalize the execution or authorize loading final
results. Prevent duplicate cancellation requests. Once a terminal response has
been accepted, late cancellation success or failure must not downgrade it or
replace its results. Release subscriptions on terminal completion and destruction,
including synchronous observable completion.

An observation error is an unknown current outcome, not a successful result.
Keep the execution identity and snapshot, explain that effects may have occurred,
and allow explicit read-only resumption or closing without reporting success.
Resumption observes the same execution; it never confirms or evaluates again.
Confirmed item counts alone do not make a pending execution successful. Preserve
the actual terminal status and partial totals when reporting a terminal outcome.

Use the existing i18n namespace for new state messages and controls. Prove both
dialogs with controlled pending, terminal, late cancellation and transport-error
interleavings, including partial confirmations, duplicate clicks, synchronous
completion, teardown and resumption with no additional mutation calls. Build Core
and CRUD as applicable and exercise the direct consumer in a focused browser flow.

This observation repair does not establish custody after closing/reopening the
dialog, reloading its parent, or losing confirmation responses. Audit the parent
owner and existing replay protocol before adding a store or endpoint. Keep those
gates and real backend commit/replay evidence explicit; do not describe UI mocks
as operational acceptance.

## Child Boundaries

CRUD delegates:

- table semantics to `@praxisui/table`
- form fields, layout, submit payload, and schema runtime to `@praxisui/dynamic-form`
- dialog shell behavior to `@praxisui/dialog`
- resource discovery, capabilities, HATEOAS, and operation resolution to `@praxisui/core`

Patch the child owner when the child contract is wrong. Patch CRUD when orchestration, open-mode selection, action binding, or lifecycle stability is wrong.

## Validation

Minimum gates:

- compile: `npm run build:praxis-crud`
- component/runtime: `npx ng test praxis-crud --watch=false --progress=false --include=projects/praxis-crud/src/lib/praxis-crud.component.spec.ts`
- resource-page context: `npx ng test praxis-crud --watch=false --progress=false --include=projects/praxis-crud/src/lib/praxis-resource-page.component.spec.ts`
- table ownership/standalone execution: `npm run test:table -- --include=projects/praxis-table/src/lib/praxis-table.remote-regression.spec.ts --watch=false`
- launcher/open modes: `src/lib/crud-launcher.service.spec.ts`
- form host: `src/lib/dynamic-form-dialog-host.component.spec.ts`
- drawer adapter: `src/lib/drawer-adapter-token.spec.ts`
- metadata/public component docs: `src/lib/praxis-crud.metadata.spec.ts`
- inspect-only/profile: component and metadata/profile specs plus an adversarial
  assertion that no router, HTTP, dialog, drawer, or global action executes
- E2E labs when host behavior changes: focused `test-dev/e2e/*.playwright.spec.ts`

Review public API, drawer adapter entrypoint, README, docs manifest, and official examples when behavior is public.
