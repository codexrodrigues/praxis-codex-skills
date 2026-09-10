---
name: praxis-page-builder-authoring
description: Use when Codex must create, inspect, or fix @praxisui/page-builder authoring editors: PageConfigEditorComponent, DynamicPageConfigEditorComponent, WidgetShellEditorComponent, SettingsValueProvider, Settings Panel bridge, page settings, canvas/grouping/device/state/context editors, widget shell actions, ComponentDocMeta.configEditor hosting, visual/textual round-trip, save/apply/reset/reopen, i18n, page editor runtime parity, or authoring changes that may require Page Builder agentic validation gates.
---

# Praxis Page Builder Authoring

Use this skill for the visual/textual authoring editors that produce or update `WidgetPageDefinition`. The goal is not "any editor can mutate JSON"; the goal is a stable round-trip between canonical page semantics, visual editors, Settings Panel, persistence, and runtime rendering.

Pair it with:

- `praxis-settings-panel-shell` and `praxis-settings-roundtrip-authoring` for Settings Panel protocol, footer state, apply/save/reset/cancel, and bridge behavior.
- `praxis-authoring-editors` for cross-component editor ownership rules.
- `praxis-page-builder-composition` for `WidgetPageDefinition`, canvas, composition links, connection graph, and runtime materialization.
- `praxis-page-builder-ai-agentic` when authoring changes affect AI manifests, UI composition plans, or agentic preview/apply.

## Canonical Chain

Keep this chain coherent:

`WidgetPageDefinition -> Page/DynamicPage config editor state -> SettingsValueProvider output -> pageChange/apply/save -> ui_user_config identity/ETag when persisted -> reopen -> praxis-dynamic-page runtime`

For widget shell:

`widget.shell -> WidgetShellEditorComponent -> ShellEditorResult -> page.widgets[].shell / pagePreset -> runtime shell`

For child widget config:

`ComponentDocMeta.configEditor or child ComponentAuthoringManifest -> child-owned document/input patch -> page.widgets[].definition.inputs`

Page Builder hosts child editors; it does not redefine child component config documents.
When a child editor needs schemas, capabilities, resource catalogs, page targets, ports, or diagnostics only for authoring, provide them through `ComponentDocMeta.configEditor.contextResolver` as transient `context/contextDiagnostics`. Do not persist those values in `page.widgets[].definition.inputs`; only the editor's explicit settings result may update child inputs.
If the child editor is Visual Builder, Dynamic Form, Table, Chart, List, Rich Content, or another Praxis component, load that component's authoring skill and preserve its document/apply semantics inside `page.widgets[].definition.inputs`.
When a hosted child editor returns a `SettingsValueProvider` payload, Page Builder must apply the
child-owned canonical input patch/document projection as `definition.inputs`, not wrap it in a
Page-Builder-local envelope or merge back transient context. Missing blocks in a replace-all child
document must remain cleared unless the child owner declares merge semantics.

Each editor session must remain tied to the current page/widget instance and authoring context. Pass
the transient owner through the Settings Panel bridge, preserve a valid session across a controlled
`pageChange -> [page]` echo of the same canonical document, and invalidate it when page identity,
widget instance, context or authoring eligibility changes. Negotiate panel replacement before
destroying the previous owner; stale close/context callbacks must not replace a newer editor or keep
Apply/Save subscriptions alive after their target disappears.

## Required Source Inventory

Before editing Page Builder authoring, inspect:

- `projects/praxis-page-builder/AGENTS.md`
- `projects/praxis-page-builder/src/lib/page-config-editor/page-config-editor.component.ts`
- `projects/praxis-page-builder/src/lib/page-config-editor/page-config-editor.component.spec.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-config-editor.component.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-config-editor.component.spec.ts`
- `projects/praxis-page-builder/src/lib/editor/widget-shell-editor.component.ts`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.ts` when links or page state are editor-visible
- `projects/praxis-page-builder/src/lib/editor/component-palette-dialog.component.ts` when insertion presets or child editor launch points change
- `projects/praxis-page-builder/src/lib/i18n/page-builder.*.ts` when labels, helper text, errors, or empty states change
- `projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.ts` when authorable paths change

Also inspect `projects/praxis-core` composition and widget shell models when changing page or shell shape.

## Editor Rules

Page config editors may edit page layout/theme presets, canvas, grouping, device layouts, context, and state. They must preserve unknown canonical fields unless the change explicitly removes deprecated compatibility semantics.

Treat JSON text areas as advanced escape hatches that still produce validated canonical objects. Do not persist invalid JSON strings, legacy grid options, or page-builder-only shapes that `praxis-dynamic-page` cannot render.

Widget shell editor owns shell chrome only: title, subtitle, icon, preset, appearance, window actions, and shell actions. It must not mutate child component inputs. Available widget actions and commands should come from `ComponentMetadataRegistry` and `ComponentDocMeta`, not local command vocabularies.

When `applyToAll` or page preset behavior changes, confirm whether the canonical owner is page preset, shell preset, or widget shell. Do not silently copy shell style into every widget when a page-level preset can express the decision.

### Preset comparison and appearance overrides

Resolve page layout presets through Core's resolver, including `presetFamily`
fallback, and preserve an explicit page theme while comparing layouts. Shell previews
must render Core's resolved preset; avoid a second appearance catalog in the editor.
Changing a shell preset preserves explicit appearance overrides; the explicit
"Use style only" action clears them. Keep that distinction visible in preview and
customization count.

Round-trip Core's `card.borderWidth/borderStyle/backdropFilter/fallbackBackground` and
`header.borderWidth/borderStyle` with the other appearance fields. Trim CSS input
before deciding whether to emit an override; whitespace-only values restore
inheritance. Validate header border color with `border-bottom-color`, since its
single divider cannot consume the card's multi-side color shorthand. Invalid values
must block Save. Test corrected validity, Apply, clearing overrides and fresh remote
reopen without altering child inputs or persisting resolved inherited context.

## Page Spacing And Canvas Geometry

Shared lateral breathing room belongs to `WidgetPageDefinition.layout.paddingInline`, not to
individual table cells or form sections. Inspect `page-layout-spacing.ts`, the Page Builder
README's shared-margin section and Core's wrapper materialization. Device layout overrides base
layout, then the host `--pdx-page-padding-inline` token applies (default `0px`). Explicit `0px`
removes the inset; clearing the editor removes the override and restores inheritance, preserving
other layout properties. Validate aligned header/table/form edges and drag/resize coordinates:
the inset belongs outside the canvas; editing-control safety space remains separate.

For Size, widget limits, responsive stacking or direct resize, inspect Core's
`docs/rfc-dynamic-page-canvas-runtime.md`, geometry helpers/specs and the Page Builder README's
**Direct canvas manipulation** section. These paths author existing `canvas.items`, device
overrides, `constraints` and `contentSize`; do not persist measured geometry or validation callbacks
as child inputs. Distinguish omitted inherited height, explicit `'auto'`, and an adjustable size.
Validate locks, inherited bounds, active-device measurements, cancellation of the complete resize
transaction and unchanged child inputs. A numeric editor check alone does not certify usable body
space or remote persistence; use the real consumer and the owning resize round-trip tests.

## Round-Trip Checklist

For Connection Editor, separate inspection from mutation. Selecting a port
opens its catalogue; explicit create/edit actions start a cancellable draft.
Opening, zooming, following a structural route and dismissing details must not
emit page changes. Naming state information is different: it edits the existing
`state.schema[path].description` or `state.derived[path].description` through
history, preserving paths, values and endpoints; persistence still uses page
Save. Do not name transient state through a persisted layer or fill absent
descriptions by guessing business meaning. Load the connection-editor reference
in `praxis-page-builder-composition` for panel, route and geometry invariants.

Before calling a Page Builder editor ready, verify:

- opening an existing page preserves `WidgetPageDefinition` without converting it to legacy `GridPageDefinition`.
- layout/theme/shell presets survive apply/save/reopen.
- canvas items reference existing widget keys.
- grouping and device layout JSON parse and preserve shape.
- page context/state remain structured objects.
- widget shell changes affect only `page.widgets[].shell`.
- child widget settings open through the child `ComponentDocMeta.configEditor` or manifest path.
- destroying/removing the page or widget owner cancels its editor tree without Save, while replacing one child preserves the parent draft and focus when the replacement is vetoed.
- transient child editor context from `configEditor.contextResolver` is separated from persisted inputs and is not saved back to `page.widgets[].definition.inputs`.
- Page Builder does not persist `context`, `contextDiagnostics`, runtime drawer `surfaceRuntime`,
  `result$` envelopes, row-selection payloads, resolved catalogs, or diagnostics output as child
  widget inputs unless the child owner explicitly declares those paths as stable inputs.
- Visual Builder or rule editors hosted as child config preserve JSON Logic/graph round-trip and do not leak Page Builder-only rule state.
- reset returns to the initial page/shell and updates dirty/valid/busy state.
- runtime preview consumes the same document shape that persistence saves.
- i18n covers user-visible editor text.

## Validation

Run focused validation:

- page config editor: page config editor spec and dynamic page config editor spec.
- widget shell: widget shell editor coverage plus metadata/registry integration where action catalogs are involved.
- Settings bridge: Settings Panel focused specs or a real editor open/apply/save/reopen smoke.
- composition-visible authoring: connection editor specs and `praxis-page-builder-composition`.
- public behavior: `ng build praxis-page-builder`; browser validation when visible editor layout or page runtime changes.

Report skipped E2E explicitly. Build/spec validation is enough for non-agentic editor-only changes. Escalate to `praxis-page-builder-ai-agentic` and the full Playwright validation gate from `projects/praxis-page-builder/AGENTS.md` when the authoring change touches agentic authoring, SSE, manifests, backend tools, patch/apply, LLM integration, or Settings Panel bridge behavior used by agentic preview/apply.

### Preset selection and document fidelity

Selecting an organization reference must not synthesize a canvas for an existing
flow page, freeze omitted canvas defaults, or persist a resolved theme/context
shell as an explicit page override. Compare the authored document before/after,
including omitted fields; only an explicit base-grid edit may introduce its canvas.
Prove theme changes and clear/reopen inheritance after Apply. In Widget Settings,
Undo stages an inverse preview that still requires Apply; do not confuse it with
discarding the current draft or persisting the page.


## Collective Canvas Arrangement

For explicit base-canvas arrangement, inspect Core `prepareCanvasArrangement` and
its focused specs. The editor prepares geometry, compares numbered before/after maps with stable widget identity, stages it,
and uses the existing panel Apply/Undo flow. Keep the proposal transient and reject
it when its source draft changes. An exact Apply echo may preserve the single undo;
page replacement and Reset invalidate it. Preserve child inputs, composition, heights,
limits and device documents. Locked positions are obstacles, not permission to move
an entire locked group. Partial device anchors may block base reorganization; do not
invent overrides or claim a device/selection solver. Column choices express geometry,
not inferred business roles or a new assistant tool.

For page-level Apply, consume the owner-confirmed session receipt through the existing
`SettingsValueProvider.acceptAppliedValue`. Capture the authored document before runtime
bootstrap enriches it. Advance the dirty baseline only on that receipt, never during
`getSettingsValue`; test Apply → Undo → Apply through the actual panel.

Revalidate staged arrangements at final submission with Core
`validateCanvasArrangement(candidate, source)`. Device numeric constraints still apply
when positions inherit. Grid edits after staging must not emit out-of-bounds items.
A rendered diagnostic can change without a form fingerprint change; handle a null
candidate before reading canvas. Keep Undo tied to reviewed geometry across unrelated
edits, and restore only geometric fields so content/limits/gap edits survive.
Include the four `canvas-arrangement-regressions.spec.ts` cases and the mixed-edit
Apply/Undo browser journey when changing this path.

Keep Visual templates, Layout templates, Arrange and Adjustments as exclusive tasks
in the canvas page editor. Theme/shell samples derive from canonical tokens and
remain illustrative; composition diagrams explain roles, not actual canvas positions.
The nine distribution choices are transient ratios passed to Core, not new persisted
preset IDs. Verify tab navigation does not dirty the document, errors route to the
correct adjustment, proposal feedback receives focus, and narrow/keyboard use retains
access to the primary tabs. More choices must not bury the before/after review.
