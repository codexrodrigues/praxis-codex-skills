# Authoring Editor Patterns

Use this reference for Praxis visual authoring surfaces: settings panel, metadata editor, dynamic form editor, table editor, rules editor, action editor, schema editor, layout builder, and page builder.

## Contents

- Common Layouts
- Rule Builders
- Settings Panels
- Metadata-Driven Forms
- Field Width And Row Composition
- Spatial Composition
- Iconography And Visual Controls
- Responsive Workstations
- Dark Theme
- Theme Tokens
- Official Browser QA
- Copy And Microcopy

## Common Layouts

Choose one of these intentionally:

- List plus details: left list/tree for selection, right details for editing.
- Canvas plus inspector: center work area, side inspector for selected object.
- Guided builder: step or segmented flow for complex rule/action construction.
- Split preview: editor controls and live/runtime preview when round-trip confidence matters.
- Single-column form: preferred for focused configuration with limited fields.

Do not combine all layouts at once unless each region has a distinct job.

Decision tree:

- Many comparable objects, rules, fields, columns, actions, or widgets -> list plus details.
- Object has visual placement, layout, drag/drop, or positional meaning -> canvas plus inspector.
- Rule, action, condition, transformation, or multi-part operation -> guided builder.
- Saved config must prove runtime effect or round-trip confidence -> split preview.
- Few fields, no object comparison, no preview requirement -> single-column form.
- If more than one pattern seems necessary, identify the dominant workflow and keep secondary regions quiet.

Do not use a card grid as the default editor layout. Use cards only for comparable repeated items, not as generic spacing containers.

## Rule Builders

Represent rules as a workflow:

1. target: what field/component/data path the rule affects
2. condition: when it applies
3. effect: what changes
4. preview/result: what the user should expect

Visual requirements:

- rule list cards must be compact and comparable
- selected rule must be clear
- incomplete rule state must show exactly what is missing
- advanced JSON or expression editing must not be the primary path when a structured editor can express the contract
- destructive or reset actions must be visually separated from primary creation/update actions

## Settings Panels

Use the settings panel as product chrome, not just a container:

- keep Apply, Save, Reset, and Cancel behavior visually clear
- keep dirty/invalid/busy state visible near the shell controls
- avoid local button implementations for canonical shell actions
- preserve stable panel dimensions while switching tabs
- make tab labels concise and scannable
- preserve focus and selected context after Apply, Save, Reset, Cancel, or close

## Metadata-Driven Forms

Prefer:

- groups based on metadata semantics
- short labels, stronger values, muted helper text
- consistent input heights
- visible required/invalid state
- stable label placement
- progressive disclosure for rarely used fields
- semantic controls that match the option type instead of defaulting every enum to a select
- layout rows sized by expected content and task importance, not a rigid equal-column grid

Avoid:

- one giant property dump
- multi-column forms where fields are read in the wrong order
- helper text wrapping into neighboring fields
- labels that are longer than the field itself
- field rows where labels, helper text, and values share the same visual weight
- text-only selects for visual settings with familiar iconography
- orphan fields: a short field placed alone in a wide row with unused space
- full-width compact controls for booleans, small enum sets, alignment, density, display mode, or icon-like choices
- treating metadata order as a complete layout system. Schema order can provide semantic order, but layout still needs field archetype, group, expected content length, primitive choice, and responsive behavior.

## Field Width And Row Composition

Assign each field/control to a layout archetype before choosing grid columns:

- Full-width: long text, description, JSON/code, markdown, preview/result, table/list, error summary, or any control whose value must be read across the row.
- Paired medium fields: two related values usually edited together, such as title plus icon, min plus max, source plus target, type plus variant, date from plus date to.
- Compact cluster: booleans, presets, alignment, density, visibility, direction, display mode, icon-only commands, segmented controls, and short stable enums.
- Dependent inline group: a controlling field plus its immediate dependent field, such as "source type" plus "source path".
- Advanced section: rare, risky, expert, JSON, integration, or override settings.

Use the archetype to pick row span:

- Do not place one compact control alone in a full-width row.
- Do not stretch compact choices to full width unless the row is a deliberate status, mode, or major scope selector.
- Do not use three equal columns unless all three controls have similar value length and editing importance.
- Pair a small field with a semantically related field, or move it into a compact cluster.
- Keep helper text under the related group, not between unrelated columns.
- Move advanced or low-frequency fields out of the default grid before adding more columns.

## Spatial Composition

Use the available width to improve task flow, not to stretch every control.

Prefer:

- full-width rows for long text, descriptions, JSON/code, preview, and fields where reading across the row is useful
- two related medium fields paired in a row when they are usually edited together
- three-column rows only when all fields have comparable density and expected content length
- compact inline clusters for short choices, toggles, segmented controls, presets, and icon controls
- section rhythm that keeps related controls near each other and separates unrelated groups
- responsive grids that collapse in task order on narrow screens

Avoid:

- equal-width grids that make one short control look lost
- large vertical gaps caused by placing a small control in its own row
- controls whose width implies importance they do not have
- row breaks that separate a label/control from its explanatory or dependent fields
- using empty columns as visual padding instead of real spacing tokens

When a field is visually small but semantically important, emphasize it with label, grouping, selected state, or helper text rather than arbitrary full width.

When reviewing a bad row, name the intended redistribution:

- full-width because content is long
- paired medium fields because they are edited together
- compact cluster because the values are short choices/actions
- dependent inline group because one control scopes the next
- advanced section because it is rare or expert-only

## Iconography And Visual Controls

Use icons strategically when they reduce cognitive load or match a familiar editing convention.

Prefer:

- alignment: segmented icon buttons for left, center, right, justify
- direction/orientation: arrow or axis icons
- visibility: eye/eye-off toggle
- density: compact/comfortable/spacious icon or segmented control
- layout: list/grid/split/canvas icons
- ordering: sort ascending/descending icons
- position/placement: dock/pin/alignment icons
- color or status: tokenized swatches

Do not use icons as decoration. Each icon control must have:

- accessible name
- tooltip or visible label when the meaning is not universal
- selected, hover, focus, disabled, and readonly states
- Material/Praxis icon source or established icon component
- i18n-backed text for labels, tooltips, and aria names

Use icon-only buttons for compact repeated commands. Use icon+text buttons when the action is rare, destructive, ambiguous, or primary for a novice workflow.

If the option set is technical, unbounded, dynamic, or not visually recognizable, a select or autocomplete may be correct.

## Responsive Workstations

Adapt the workstation pattern, not just CSS columns:

- List/details: on narrow screens show the list first, keep selected summary visible, and move details below or into a drawer.
- Canvas/inspector: preserve the canvas/work area first; move inspector below, into a drawer, or into collapsible sections while retaining selection context.
- Guided builder: stack steps in task order and keep progress/status visible.
- Split preview: keep the control and result adjacent in flow; do not bury preview below unrelated settings.
- Footer actions: sticky actions must not overlap fields, overlays, or validation messages.
- Segmented/icon clusters: wrap as groups and preserve touch targets.

## Dark Theme

For dark theme authoring tools:

- use subtle tokenized surfaces, not many bright borders
- reserve tokenized accent for selection, focus, and primary action
- ensure overlays inherit correct Material/Praxis surface and text tokens
- avoid many similar blue accents competing for attention
- keep disabled state distinguishable from readonly state

## Theme Tokens

Authoring editors must be themeable by host applications:

- prefer Angular Material design tokens for Material-backed controls
- prefer Praxis tokens/CSS custom properties for Praxis-owned shell, surfaces, overlays, spacing, radius, elevation, focus, and component states
- do not introduce raw hex/rgb/hsl colors for reusable components unless they are token defaults or documented fallback values
- do not lock editor chrome to one palette in component CSS
- keep dark/light/high-contrast behavior derived from tokens, not duplicate style branches in consumers
- if a required token does not exist, classify whether this is `ja-suportado-so-ux`, `suportado-parcialmente`, or `lacuna-real-de-contrato` before introducing a public token

## Official Browser QA

Before screenshot QA:

- read applicable root, workspace, and subarea `AGENTS.md`
- use official scripts, routes, ports, and origins documented by the repo
- do not invent an ad hoc static server, port, local bridge, or route
- if no official route is discoverable, declare the limitation and use static review plus focused build/spec validation

## Copy And Microcopy

Use product-language copy:

- name the user's object, not the implementation detail, unless this is an expert-only technical editor
- helper text should explain impact, constraints, or next action
- empty states should offer the next step
- error states should name the broken field and how to fix it

Internal authoring text must still follow the repository i18n rules from the relevant Praxis skill and local package guidance.

For internal lib/editor copy, do not introduce hardcoded labels, helper text, placeholders, tooltips, empty states, or error messages. Use the owning lib i18n path, typically `PraxisI18nService`, the lib namespace, and base catalogs for `pt-BR` and `en-US` when the local guidance requires it.
