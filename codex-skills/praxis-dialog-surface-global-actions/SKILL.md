---
name: praxis-dialog-surface-global-actions
description: Use when changing or reviewing `@praxisui/dialog` surface/global-action materialization, `providePraxisSurfaceGlobalActions`, `GLOBAL_SURFACE_SERVICE`, `PraxisSurfaceHostComponent` dialog hosting, `SURFACE_DRAWER_BRIDGE`, surface open payloads, component/template registry resolution, selection result forwarding, dialog surface runtime, or metadata-driven dialog/surface open integration.
---

# Praxis Dialog Surface Global Actions

Use this skill for the bridge where metadata-driven global actions materialize surfaces inside dialogs or host drawers. This is not a generic overlay shortcut; it is the runtime projection of governed surface/action contracts.

## Canonical Boundary

- `@praxisui/core` owns `GlobalActionRef`, `GLOBAL_SURFACE_SERVICE`, `GLOBAL_DIALOG_SERVICE`, surface open payloads, materializers, component metadata registry, and shared action validation.
- `@praxisui/dialog` owns the dialog-backed implementation of global dialog/surface actions.
- `providePraxisDialogGlobalActions()` bridges alert, confirm, prompt, and registered component dialogs through `GLOBAL_DIALOG_SERVICE`.
- `providePraxisSurfaceGlobalActions()` bridges materialized surfaces through `GLOBAL_SURFACE_SERVICE`, using `PraxisDialog` for dialog presentation and `SURFACE_DRAWER_BRIDGE` for drawer presentation.
- Hosted child widgets own their own runtime semantics and authoring manifests.

## Required Inventory

Inspect:

- `projects/praxis-dialog/AGENTS.md`
- `projects/praxis-dialog/README.md`
- `projects/praxis-dialog/docs/host-dialog-integration.md`
- `projects/praxis-dialog/src/lib/providers/dialog-global-actions.provider.ts`
- `projects/praxis-dialog/src/lib/providers/surface-global-actions.provider.ts`
- `projects/praxis-dialog/src/lib/providers/dialog-global-presets.provider.ts`
- `projects/praxis-dialog/src/lib/dialog/dialog.service.ts`
- `projects/praxis-dialog/src/lib/dialog/dialog.tokens.ts`
- `projects/praxis-dialog/src/lib/praxis-dialog.metadata.ts`
- `projects/praxis-core/src/lib/models/global-action.model.ts`
- core surface/global-action services, payload validators, and focused specs

Use `praxis-core-global-actions-metadata` for shared action contracts and `praxis-dialog-global-actions-ai` for dialog authoring manifests and registry ingestion.

## Materialization Rules

- Persist and consume structured `GlobalActionRef`/surface payloads, not command strings or localized action aliases.
- `dialog.open` requires `componentId`. Resolve via `ComponentMetadataRegistry` first, then dialog content registry.
- Apply `inputs` after the component exists and trigger change detection.
- Surface open payloads must pass through the core `SurfaceOpenMaterializerService` before dialog/drawer projection.
- Dialog surface runtime may expose `closed$`, `result$`, `emitResult`, `close`, and `updateSize`; it must not become a business workflow engine.
- Forward row/selection outputs from `PraxisSurfaceHostComponent` as surface results when the hosted component emits them.
- Drawer presentation requires `SURFACE_DRAWER_BRIDGE`; do not silently fall back to a different drawer contract.
- Host/domain side effects after `afterClosed` or `result$` remain host-owned.

## Red Flags

Refactor or reject:

- `surface.open:{...}` strings, `showAlert:*` command strings, or local switch/case action grammars
- dialog providers that bypass core payload validation or materialization
- unregistered component ids invented by AI or host code
- surface drawer implementations that skip `SURFACE_DRAWER_BRIDGE`
- child widget config patched through dialog shell contracts instead of delegated child manifests

## Validation

Use focused checks:

- `src/lib/providers/dialog-global-actions.provider.spec.ts`
- `src/lib/providers/surface-global-actions.provider.spec.ts`
- `src/lib/providers/dialog-global-presets.provider.spec.ts`
- core global action/payload validator specs when shared action contracts change
- service/component specs when overlay lifecycle or registry open behavior changes
- registry ingestion/docs validation when component metadata, manifests, or docs projections change

State whether public API, docs, examples, AI registry, or generated assets were updated or intentionally unaffected.
