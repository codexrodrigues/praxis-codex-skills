---
name: praxis-settings-panel-shell
description: Use when changing or reviewing `@praxisui/settings-panel` or the praxis-settings-panel package shell behavior, SettingsPanelService, SettingsPanelRef, SettingsValueProvider, BaseSidePanelService, drawer sizing, close/backdrop/Escape mediation, Apply/Save/Reset/Cancel enablement, diagnostics, tokens, or host bridge integration.
---

# Praxis Settings Panel Shell

The `praxis-settings-*` skill family is the canonical Codex skill surface for `@praxisui/settings-panel` and `projects/praxis-settings-panel`; do not create parallel `praxis-settings-panel-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the canonical authoring drawer shell. Do not duplicate drawer chrome, footer protocol, dirty/valid/busy rules, resize, shortcuts, or close mediation in consumer editors when the issue belongs to `@praxisui/settings-panel`.

Resolve paths from `praxis-ui-angular/projects/praxis-settings-panel/` unless another root is named.

## Canonical Boundary

- `SettingsPanelService` opens authoring drawers.
- `SettingsPanelRef` emits `applied$`, `saved$`, `reset$`, `closed$`, and `sizeChanged$`.
- `SettingsValueProvider` is the editor contract: `getSettingsValue`, optional `onSave`, optional `reset`, and required `isDirty$`, `isValid$`, `isBusy$`.
- `BaseSidePanelService` owns shared overlay, scope replacement, backdrop, Escape, width presets, resize, and persisted width.
- `providePraxisSettingsPanelBridge()` is authoring; `providePraxisSurfaceDrawerBridge()` is runtime `surface.open`. Do not mix these semantics.

`BaseSidePanelService` is infrastructure, not an authoring protocol. `SettingsPanelService` adds authoring semantics on top of it; `SurfaceDrawerComponent`/`SURFACE_DRAWER_BRIDGE` uses the same infrastructure for neutral runtime drawers.

## Required Inventory

Inspect:

- `projects/praxis-settings-panel/AGENTS.md`
- `docs/host-settings-panel-integration.md`
- `src/public-api.ts`
- `src/lib/settings-panel.service.ts`
- `src/lib/settings-panel.component.ts`
- `src/lib/settings-panel.component.html`
- `src/lib/settings-panel.component.scss`
- `src/lib/settings-panel.ref.ts`
- `src/lib/settings-panel.types.ts`
- `src/lib/base-side-panel.service.ts`
- `src/lib/base-side-panel.component.ts`
- `src/lib/base-side-panel.component.html`
- `src/lib/base-side-panel.component.scss`
- `src/lib/base-side-panel.ref.ts`
- `src/lib/base-side-panel.types.ts`
- `src/lib/side-panel-theme.contract.ts`
- `src/lib/overlay-escape-defer.ts`
- `src/lib/settings-panel-bridge.provider.ts`
- `src/lib/settings-panel-bridge.provider.spec.ts`
- `src/lib/surface-drawer-bridge.provider.ts`
- `src/lib/surface-drawer-bridge.provider.spec.ts`
- `src/lib/surface-drawer.component.ts`
- `src/lib/surface-drawer.component.html`
- `src/lib/surface-drawer.component.scss`

## Shell Rules

- Keep Apply and Save enabled only when dirty, valid, and not busy.
- `Apply` previews without closing through `applied$`; `Save` emits through `saved$` and closes.
- `Reset` delegates to the hosted editor and emits `reset$`; it must not clear unrelated host state.
- `Cancel`, backdrop, Escape, and replacement of an open panel must pass through the canonical close mediation, including `onBeforeClose` and dirty discard confirmation where applicable.
- Persist width through `persistSizeKey`; expanded/collapsed state must not accidentally overwrite persisted manual width.
- Use `SettingsPanelConfig.diagnostics` only to show/hide status, disabled reason, busy state, or validation state. It must not change the gating rules.
- Use canonical tokens/classes for visual changes: `--pfx-settings-panel-*`, `.praxis-settings-panel-backdrop`, and `.praxis-settings-panel-pane`.
- Do not bypass `SettingsPanelService.open(...)` replacement mediation. It must consult `onBeforeClose('cancel')`, preserve the current panel when vetoed, and apply dirty discard confirmation when relevant.
- Inputs are applied through declared Angular inputs when possible and also passed via the relevant data token (`SETTINGS_PANEL_DATA` for authoring, `BASE_SIDE_PANEL_DATA` for base/runtime).
- Escape must defer to active child CDK overlays before closing the panel. Do not reintroduce local document listeners in consumers that bypass `overlay-escape-defer`.

## Base Side Panel Rules

When changing `BaseSidePanelService` or `BaseSidePanelComponent`:

- Preserve scope isolation. Opening scope `settings-panel` must not close scope `surface-drawer`, and vice versa.
- Default width presets are `narrow=420px`, `default=720px`, `wide=960px`, and `full=100vw`.
- Persisted width uses localStorage key `praxis.side-panel.width:<persistSizeKey>` and accepts only pixel values.
- `updateSize(...)` must update the overlay, emit `sizeChanged$`, and persist when a `persistSizeKey` is bound.
- Horizontal resize is `resizeAxis: 'x'` only; keyboard resize uses ArrowLeft/ArrowRight plus Home/End for min/max when available.
- Backdrop and Escape close should emit typed close results such as `{ type: 'backdrop' }` or `{ type: 'esc' }`.
- Keep base panel neutral: it may host optional footer content, but it must not introduce Settings Panel Apply/Save/Reset semantics.

## Authoring Vs Runtime Drawer

Authoring bridge:

- `providePraxisSettingsPanelBridge()` adapts `SettingsPanelService` to `SETTINGS_PANEL_BRIDGE`.
- It should preserve `id`, `title`, `titleIcon`, component, and input envelope.
- It is for authoring editors with `SettingsValueProvider`, footer protocol, diagnostics, dirty/valid/busy gates, and apply/save/reset/cancel.

Runtime drawer bridge:

- `providePraxisSurfaceDrawerBridge()` adapts `BaseSidePanelService.openHost(...)` to `SURFACE_DRAWER_BRIDGE`.
- It uses scope `surface-drawer`, `SurfaceDrawerComponent`, and neutral runtime chrome.
- It injects `context.surfaceRuntime` into hosted content, exposing `closed$`, `result$`, `close`, `emitResult`, `updateTitle`, and `updateSize`.
- It publishes hosted `rowClick` and `selectionChange` outputs through `result$` using result envelopes with `type`, `data`, `output`, and `payload`.
- It must not show authoring footer/status text such as Apply or Save & Close.
- Treat `context.surfaceRuntime`, `result$`, `rowClick`, and `selectionChange` as runtime interaction
  contracts. They are not authoring documents, persisted config, dirty state, or replacement for a
  `SettingsValueProvider`.
- Do not persist runtime drawer context, runtime selection envelopes, diagnostics visibility, or
  resolved surface state into component config from this bridge. If a host needs an authored
  connection to a runtime drawer, model that in the owning action/composition authoring contract,
  not as Settings Panel shell state.
- In Ergon migrations, a drawer that only needs to show detail, emit a selected row, update title, or
  close with a result should stay on `SURFACE_DRAWER_BRIDGE`. Promote it to Settings Panel authoring
  only when the user is editing a stable config document through an editor that owns
  `SettingsValueProvider`.

## Visual And Token Rules

- Authoring-specific classes: `.praxis-settings-panel-pane`, `.praxis-settings-panel-backdrop`, `.settings-panel-*`.
- Neutral/shared runtime classes: `.praxis-side-panel-pane`, `.praxis-side-panel-backdrop`, `.pfx-base-side-panel-*`, `.pfx-surface-drawer-*`.
- Authoring tokens use `--pfx-settings-panel-*`.
- Neutral runtime/shared tokens use `--pfx-side-panel-*` from `SidePanelThemeContract`.
- `SidePanelThemeContract.cssVars` must use neutral `--pfx-side-panel-*` keys, never `--pfx-settings-panel-*`.
- Hosted editors with wide intrinsic content must fit inside the panel body. Preserve `min-width: 0`, `max-width: 100%`, `overflow-x: hidden`, and body scroll padding rules unless replacing them with an equivalent shell-level solution.

## Validation

Prefer focused checks:

- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.service.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel.component.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/base-side-panel.service.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/base-side-panel.component.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/settings-panel-bridge.provider.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/surface-drawer-bridge.provider.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/surface-drawer.component.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/side-panel-theme.contract.spec.ts`
- screenshot or Playwright evidence when visual drawer behavior is material

Review README, public API, and host integration docs when shell behavior, public tokens, or bridge semantics change.
