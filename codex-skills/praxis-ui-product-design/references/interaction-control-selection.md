# Interaction Control Selection

Use this reference when a Praxis UI feels crude because everything is rendered as generic inputs, buttons, cards, or selects.

## Primitive Decision Matrix

Choose the control by user intent:

- Single immediate command: button or icon button.
- Repeated familiar command: icon button with tooltip and accessible name.
- Primary command: text or icon+text button, visually strongest in the active region.
- Destructive command: separated button, confirmation or undo when data loss is possible.
- Boolean setting: switch, checkbox, or toggle depending on persistence and immediacy.
- Small exclusive mode set: segmented control.
- Visual property with familiar metaphor: icon segmented control.
- Long static option list: select.
- Dynamic/searchable option list: autocomplete or async select.
- Numeric scalar: slider, stepper, or numeric input based on precision.
- Color/status: tokenized swatch or palette.
- Filter: filter chip, filter row, search field, or faceted control.
- Navigation: tabs, side nav, breadcrumb, tree, or list based on depth and comparison.
- Bulk operation: selection affordance plus action toolbar, not hidden per-row buttons only.
- Reorder: drag handle, move up/down buttons, or ordered list controls.
- Previewable setting: control plus live preview/result region when runtime impact matters.

Do not default enum metadata to a select. First decide whether the enum is a mode, visual property, command target, state, filter, or technical value.

## Common Praxis Mappings

Use these as starting points:

- Alignment: segmented icon control for left, center, right, justify.
- Header/avatar appearance: segmented visual mode or compact preview chips.
- Visibility: eye/eye-off toggle.
- Collapsible behavior: collapse/expand icon control or switch.
- Density: compact/default/comfortable segmented control.
- Size: stepper or segmented size tokens when choices are discrete.
- Position: dock/pin/alignment icon control.
- Layout: list/grid/split/canvas segmented icons.
- Font role: select only when values are semantic roles such as title/body/caption; otherwise use typography preview.
- Presets: chips or segmented buttons when count is small and stable.
- Icon choice: searchable icon picker or autocomplete, not a plain text input.

## Praxis Primitive Ownership

Before adding a new control implementation, identify the owner:

- Shared visual primitive used by more than one lib: `@praxisui/core` or the established shared owner.
- Dynamic field control type, alias, option source, inline filter, async-select, or field token: `praxis-dynamic-fields-editorial` and the owning dynamic-fields package.
- Settings panel shell action, drawer, footer, persistence affordance, or `SettingsValueProvider` UX: `@praxisui/settings-panel`.
- Editor-specific composition that does not generalize: owning `@praxisui/*` lib.
- Demo-only composition with no reusable pattern: host/demo.

Do not copy a local segmented control, icon picker, swatch picker, overlay, or toolbar when a shared Praxis or Material primitive already exists or should exist.

## Command Hierarchy

Make command priority visible:

- Put the primary command in the shell or active work region.
- Keep secondary commands nearby but quieter.
- Put destructive actions away from primary success actions.
- Keep reset/cancel distinct from save/apply.
- Use sticky footer actions only for shell-level persistence.
- Use inline actions for item-level edits when the scope is local.

If multiple actions look equally strong, the UI fails the hierarchy test.

## Feedback And Reversibility

Design the consequence of actions:

- Immediate local changes should show selected/active state.
- Deferred changes should show dirty state and Apply/Save availability.
- Long-running actions should show busy state without losing context.
- Destructive actions should support undo, confirmation, or explicit risk copy.
- Reset should explain scope when there are nested editors or selected items.
- Validation should appear near the cause and preserve user input.

## Selection And Bulk Work

Enterprise authoring screens often require comparison and repeated work:

- selected item must remain visible when the inspector scrolls
- lists should show status, invalid/incomplete markers, and concise identity
- bulk selection should expose a contextual toolbar
- per-item actions should not be the only path for repeated operations
- keyboard navigation should work through list, selection, editor, and shell actions

## Progressive Disclosure

Use progressive disclosure to protect scan speed:

- show essential controls first
- move advanced or rare fields behind sections, accordions, or advanced mode
- keep dangerous settings out of the default path
- provide preview/result for complex settings before save
- do not hide required fields behind collapsed advanced areas

## Responsive Adaptation

Control choice may change by viewport:

- desktop can use side-by-side list/details, inspector, and preview
- narrow view should stack workflow steps in task order
- dense icon controls must keep touch targets usable
- sticky footers must not cover form fields or overlays
- long labels should wrap or move above controls rather than compressing inputs

## Accessibility And I18n

Every custom or icon-heavy control must preserve:

- keyboard operation
- focus visibility
- accessible name and role
- selected/pressed/expanded state
- tooltip or visible label when meaning is not universal
- i18n-backed label, tooltip, aria text, and validation text

Do not trade accessibility for visual polish.
