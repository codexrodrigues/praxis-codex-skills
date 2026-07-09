---
name: praxis-dialog-overlay-runtime
description: Use when implementing or auditing `@praxisui/dialog` runtime behavior, including `PraxisDialog`, `PraxisDialogComponent`, `PraxisDialogRef`, `DialogOverlayService`, service API, tag mode, confirm/alert/prompt/custom dialogs, presets merge order, focus, Escape/backdrop close, restoreFocus, `dialog|alertdialog` accessibility, panel/backdrop classes, scroll strategy, sizing, positioning, and overlay lifecycle.
---

# Praxis Dialog Overlay Runtime

Use this skill for canonical Praxis dialogs and overlays. `@praxisui/dialog` is the workspace owner for dialog service API, overlay container behavior, presets, tag mode, accessibility, and lifecycle semantics.

## Required Source Audit

Inspect:

- `projects/praxis-dialog/AGENTS.md`
- `README.md`
- `docs/host-dialog-integration.md`
- `src/public-api.ts`
- `src/lib/dialog/dialog.service.ts`
- `src/lib/dialog/dialog.component.ts`
- `src/lib/dialog/dialog.component.html`
- `src/lib/dialog/dialog.ref.ts`
- `src/lib/dialog/overlay/dialog-overlay.service.ts`
- `src/lib/dialog/dialog.types.ts`
- `src/lib/dialog/dialog.tokens.ts`
- focused service/component/preset specs

## Runtime Rules

- Use `PraxisDialog.open`, `confirm`, `alert`, `prompt`, `openByRegistry`, `openTemplateById`, or tag mode; do not add ad hoc overlay shells in consumers.
- Preserve lifecycle streams: `afterOpened`, `beforeClosed`, `afterClosed`, `backdropClick`, `keydownEvents`, `afterAllClosed`.
- Preserve close policy: `disableClose`, `closeOnBackdropClick`, Escape handling, backdrop click handling, and close on navigation.
- Preserve `autoFocus`, `autoFocusedElement`, `restoreFocus`, visible title or accessible label, and correct `ariaRole`.
- Use `alertdialog` for destructive/blocking confirmations.
- Keep preset merge order canonical: type preset, variant preset, local config.
- Use `PraxisLayerScaleStyleService`/core overlay layering before patching individual hosts for z-index issues.

## Validation

Minimum gates:

- compile: `ng build praxis-dialog`
- service API: `src/lib/dialog/dialog.service.spec.ts`
- preset merge: `src/lib/dialog/dialog.service.merge-presets.spec.ts`
- component accessibility/lifecycle: `src/lib/dialog/dialog.component.spec.ts`
- global presets provider: `src/lib/providers/dialog-global-presets.provider.spec.ts`

Review README, integration guide, docs manifest, public API, and examples when runtime behavior changes.
