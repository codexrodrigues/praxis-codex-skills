---
name: praxis-crud-drawer-adapter-contract
description: Use when changing or reviewing `@praxisui/crud` drawer mode, `CRUD_DRAWER_ADAPTER`, `CrudDrawerAdapter`, the lightweight `@praxisui/crud/drawer-adapter` secondary entrypoint, default drawer fallback, drawer result callbacks, bundle-entrypoint ADR alignment, or host drawer integration divergence.
---

# Praxis CRUD Drawer Adapter Contract

Use this skill for the thin host adapter seam around CRUD drawer mode. The adapter is an optional shell override, not a second CRUD runtime.

## Canonical Boundary

- `@praxisui/crud` owns drawer open-mode orchestration through `CrudLauncherService`.
- `CRUD_DRAWER_ADAPTER` is the host seam used only when a product must render the CRUD form in its own drawer shell.
- Without an adapter, drawer mode must fall back to the package default: `DialogService.openAsync(DynamicFormDialogHostComponent)` with drawer presentation.
- The secondary entrypoint `@praxisui/crud/drawer-adapter` is the preferred host import path. It exists to keep bootstrap bundles light and must not pull the full CRUD barrel.
- Hosts may provide visual chrome, telemetry, and layout integration. They must not redefine save/delete/close semantics, operation resolution, form contracts, or CRUD metadata.

## Required Inventory

Inspect:

- `projects/praxis-crud/AGENTS.md`
- `projects/praxis-crud/docs/adr/2026-03-drawer-adapter-light-entrypoint.md`
- `projects/praxis-crud/docs/host-crud-runtime-and-openmode.md`
- `projects/praxis-crud/src/public-api.ts`
- `projects/praxis-crud/drawer-adapter/public-api.ts`
- `projects/praxis-crud/src/lib/drawer.adapter.ts`
- `projects/praxis-crud/drawer-adapter/src/drawer-adapter.ts`
- `projects/praxis-crud/src/lib/crud-launcher.service.ts`
- `projects/praxis-crud/src/lib/dynamic-form-dialog-host.component.ts`
- drawer adapter token and launcher specs

Use `praxis-crud-runtime-openmodes` when the change touches general open-mode precedence or action launch behavior. Use `praxis-dialog-overlay-runtime` when the default drawer fallback depends on dialog overlay semantics.

## Adapter Rules

- Import host adapters from `@praxisui/crud/drawer-adapter`, not the root `@praxisui/crud` barrel.
- Keep root public API and secondary entrypoint intentional. If the secondary entrypoint starts exporting heavy services/components, treat it as an architectural regression.
- `CrudDrawerOpenConfig` must carry the resolved action, metadata, mapped inputs, `onClose`, and `onResult`.
- `CrudDrawerResult` is semantic: `save`, `delete`, or `close`, with optional data. The host adapter should propagate these results so `PraxisCrudComponent` can emit `afterSave`, `afterDelete`, `afterClose`, and refresh.
- Do not make the adapter responsible for schema discovery, submit URL inference, CRUD operation resolution, permissions, or persistence.
- Do not copy the default drawer implementation into hosts just to get basic drawer behavior; use `defaults.openMode = 'drawer'` and the built-in fallback.
- If a host drawer is required, prove parity with the default runtime for close, save, delete, dirty/back policy, focus, and responsive sizing.

## Aderencia Before Contract Changes

Classify before adding fields or exports:

- `ja-suportado-so-ux`: default drawer works; host only needs presentation/wiring.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host imports the root barrel or duplicates the default drawer even though the secondary entrypoint exists.
- `suportado-parcialmente`: adapter receives the right contract but misses result propagation, focus, or responsive drawer parity.
- `lacuna-real-de-contrato`: the adapter cannot express a required host drawer lifecycle or semantic result without a new canonical field.

For a real contract gap, update root/secondary public APIs, ADR/docs, launcher specs, drawer token specs, and a host or package consumer proof.

## Validation

Use focused checks:

- `src/lib/drawer-adapter-token.spec.ts`
- `src/lib/crud-launcher.service.spec.ts`
- `src/lib/dynamic-form-dialog-host.component.spec.ts` when fallback drawer behavior changes
- build `praxis-crud` plus secondary entrypoint packaging when public exports change
- docs/ADR review when import path, bundle boundary, or adapter responsibilities change

State whether docs, public API, examples, and registry artifacts were updated or are unaffected.
