---
name: praxis-crud-runtime-openmodes
description: Use when implementing or auditing `@praxisui/crud` runtime orchestration, including `PraxisCrudComponent`, `CrudMetadata`, `crudContext` stability, `CrudLauncherService`, route/modal/drawer open modes, `DynamicFormDialogHostComponent`, drawer adapter token, table/form handoff, capabilities/HATEOAS action launching, schemaUrl/submitUrl binding, and CRUD consumer validation.
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
- `src/lib/crud-launcher.service.ts`
- `src/lib/dynamic-form-dialog-host.component.ts`
- `src/lib/drawer.adapter.ts`
- `src/lib/crud.types.ts`
- focused specs for launcher, dialog host, drawer adapter, and component metadata

## Runtime Boundary

- `PraxisCrudComponent` owns CRUD context, table handoff, selected row, collection links/capabilities, authoring entrypoint, and action dispatch.
- `CrudLauncherService` owns open-mode resolution and launch behavior.
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
- Treat `openMode`, visible row/toolbar actions, and injected CRUD affordances as orchestration evidence only. Availability and executable permission come from capabilities, links, surfaces, actions, and adapter payloads; do not infer workflow permission or backend side effects from a drawer/modal opening or a button label.
- Keep `crudContext` stable; avoid getters or object literals that recreate context each change detection cycle.

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
- component/runtime: `src/lib/praxis-crud.component.spec.ts`
- launcher/open modes: `src/lib/crud-launcher.service.spec.ts`
- form host: `src/lib/dynamic-form-dialog-host.component.spec.ts`
- drawer adapter: `src/lib/drawer-adapter-token.spec.ts`
- metadata/public component docs: `src/lib/praxis-crud.metadata.spec.ts`
- E2E labs when host behavior changes: focused `test-dev/e2e/*.playwright.spec.ts`

Review public API, drawer adapter entrypoint, README, docs manifest, and official examples when behavior is public.
