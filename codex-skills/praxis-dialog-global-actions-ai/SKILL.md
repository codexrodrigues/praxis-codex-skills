---
name: praxis-dialog-global-actions-ai
description: Use when changing or validating `@praxisui/dialog` global actions, registries, providers, and AI authoring, including `providePraxisDialogGlobalActions`, `GLOBAL_DIALOG_SERVICE`, `ComponentMetadataRegistry` lookup, dialog content/template registries, `provideDialogGlobalPresetsFromGlobalConfig`, `PRAXIS_DIALOG_AUTHORING_MANIFEST`, child host delegation, metadata-driven `dialog.open|alert|confirm|prompt`, registry ingestion, docs, and global action integration.
---

# Praxis Dialog Global Actions AI

Use this skill when dialogs are opened by metadata-driven/global-action flows or AI authoring. Dialog can host components and templates, but child semantics remain with the child component manifest.

Pair with `praxis-dialog-surface-global-actions` when the work touches `GLOBAL_SURFACE_SERVICE`, `PraxisSurfaceHostComponent`, `SURFACE_DRAWER_BRIDGE`, surface materialization, selection result forwarding, or dialog surface runtime.

## Required Source Audit

Inspect:

- `projects/praxis-dialog/AGENTS.md`
- `src/lib/providers/dialog-global-actions.provider.ts`
- `src/lib/providers/surface-global-actions.provider.ts`
- `src/lib/providers/dialog-global-presets.provider.ts`
- `src/lib/dialog/dialog.tokens.ts`
- `src/lib/dialog/dialog.service.ts`
- `src/lib/ai/praxis-dialog-authoring-manifest.ts`
- `src/lib/praxis-dialog.metadata.ts`
- README, integration docs, docs manifest, and focused specs

## Global Action Boundary

- `providePraxisDialogGlobalActions()` provides `GLOBAL_DIALOG_SERVICE` for alert, confirm, prompt, and open.
- `dialog.open` requires `componentId`.
- Resolve `componentId` through `ComponentMetadataRegistry` first, then dialog content registry.
- Apply `inputs` after component creation and trigger change detection.
- Surface actions must pass through core surface materialization before dialog/drawer projection.
- Host/domain action after close remains host-owned; dialog does not own business authorization or persistence.
- Treat the resolved value from `alert`, `confirm`, `prompt`, and `open` as the `afterClosed()` lifecycle result of the opened dialog.
  It may confirm user interaction, carry a prompt value, or forward a child payload, but it is not by itself a governed business decision,
  persistence command, authorization check, or metadata mutation. If a close result should trigger domain work, route that continuation
  through the owning global action/composition contract or backend-confirmed action instead of parsing dialog labels, messages, or result
  payloads in the consumer.
- Global config can provide dialog presets through `provideDialogGlobalPresetsFromGlobalConfig()`.

## Authoring Manifest Rules

Use `PRAXIS_DIALOG_AUTHORING_MANIFEST`.

- Shell, size, position, backdrop, close policy, and preset operations edit dialog config only.
- `dialog.closePolicy.set` is potentially destructive and requires confirmation when it can trap or dismiss user work.
- `childHost.configure` must validate component/template registration and delegate child config to the child manifest.
- AI must not route dialog intent by frontend keywords or invent unregistered component ids.

## Validation

Minimum gates:

- global actions: `src/lib/providers/dialog-global-actions.provider.spec.ts`
- surface actions: `src/lib/providers/surface-global-actions.provider.spec.ts`
- presets from global config: `src/lib/providers/dialog-global-presets.provider.spec.ts`
- manifest: `src/lib/ai/praxis-dialog-authoring-manifest.spec.ts`
- service/preset specs when shell behavior changes
- compile: `ng build praxis-dialog`
- registry/docs: `npm run generate:registry:ingestion` when generated registry artifacts are affected

Pair with `praxis-dialog-overlay-runtime` for runtime overlay/focus/accessibility behavior.
