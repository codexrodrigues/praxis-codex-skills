---
name: praxis-crud-dialog-form-host-lifecycle
description: Use when changing or reviewing `@praxisui/crud` modal/drawer form host lifecycle, `DynamicFormDialogHostComponent`, package `DialogService`, `CrudLauncherService` dialog fallback, dynamic-form input mapping, form submit/cancel result handling, refresh after save/delete, close/back policy, maximize state, focus, or table/form/dialog lifecycle integration.
---

# Praxis CRUD Dialog Form Host Lifecycle

Use this skill for the operational cycle where a CRUD action opens a dynamic form by modal or drawer and returns a semantic result to the CRUD table.

## Canonical Boundary

- `PraxisCrudComponent` owns table action dispatch, selected row, collection links/capabilities, result events, and refresh after save/delete.
- `CrudLauncherService` owns action normalization, override merge, open-mode resolution, route/modal/drawer launch, and dynamic-form input mapping.
- `DynamicFormDialogHostComponent` owns the package form host chrome around `PraxisDynamicForm` for modal/drawer presentation.
- `@praxisui/dynamic-form` owns form field rendering, submit payload normalization, hooks, rules, persistence, and schema-driven runtime.
- Dialog shell behavior belongs to the package dialog/fallback services, not to table or host apps.

## Required Inventory

Inspect:

- `projects/praxis-crud/AGENTS.md`
- `projects/praxis-crud/README.md`
- `projects/praxis-crud/docs/host-crud-runtime-and-openmode.md`
- `projects/praxis-crud/src/lib/praxis-crud.component.ts`
- `projects/praxis-crud/src/lib/crud-launcher.service.ts`
- `projects/praxis-crud/src/lib/dynamic-form-dialog-host.component.ts`
- `projects/praxis-crud/src/lib/dialog.service.ts`
- `projects/praxis-crud/src/lib/crud.types.ts`
- focused component, launcher, dialog service, and dialog host specs

Use `praxis-form-runtime-submit` for dynamic-form submit contracts, `praxis-table-runtime-data` for table refresh/runtime data, and `praxis-dialog-overlay-runtime` for overlay/focus/accessibility details.

## Lifecycle Rules

- Keep `crudContext` stable; do not use template getters or object literals that recreate table handoff state on every change detection cycle.
- Normalize create aliases only into canonical create before launcher/discovery. Do not add broad local action vocabularies for business workflows.
- Resolve modal/drawer form inputs from action params, runtime operation resolution, capabilities, HATEOAS links, explicit form contract, inferred form id, and row initial value.
- `form.submitUrl` and `form.submitMethod` must remain operationally coherent. Do not fake submit contracts in the host dialog.
- Modal and default drawer open through the package dialog host. Drawer presentation changes CSS/classes/sizing, not the semantic save/delete/close result model.
- For drawer mode, `PraxisCrudComponent` must consume the managed launcher callbacks (`onClose`, `onResult`) as the lifecycle source. Do not subscribe directly to a drawer `ref.afterClosed()` in the component; `CrudLauncherService` normalizes the drawer close payload into `CrudDrawerResult` and emits semantic `close` when the shell closes without payload.
- On `save` and `delete`, emit the corresponding CRUD output and refresh the table via the component-owned table refetch path.
- Do not refresh the table merely because a drawer/modal opened, a duplicate draft was fetched, or a close event happened. Refresh only after the semantic mutation result (`save` or `delete`) is received.
- Canonical delete is not a form open mode. It uses confirmation plus resolved HTTP delete/action contract.
- Preserve back/return behavior for route mode and cancel/close behavior for modal/drawer mode.
- Maximize/remember-state behavior is dialog-host chrome only; it must not mutate form config or CRUD metadata.

## Aderencia Before Contract Changes

Classify before changing contracts:

- `ja-suportado-so-ux`: lifecycle data exists and only needs host/dialog presentation correction.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: save/delete/close is represented but projected as generic close or stale table state.
- `suportado-parcialmente`: CRUD knows the operation but dynamic-form input mapping, capabilities, or result propagation is incomplete.
- `lacuna-real-de-contrato`: the lifecycle cannot express a required operation, result, or refresh signal with existing CRUD/dynamic-form/dialog contracts.

For a real gap, name the canonical owner, impacted consumers, docs/examples, public API, and focused tests.

## Validation

Use focused checks:

- `src/lib/praxis-crud.component.spec.ts`
- `src/lib/crud-launcher.service.spec.ts`
- `src/lib/dialog.service.spec.ts`
- `src/lib/dynamic-form-dialog-host.component.spec.ts`
- dynamic-form focused specs when submit payload or form runtime changes
- table focused specs when refresh/runtime data changes
- build `praxis-crud`; build direct consumers when public APIs or cross-lib contracts change

State explicitly when no docs, examples, public API, manifest, or registry artifacts need updates.
