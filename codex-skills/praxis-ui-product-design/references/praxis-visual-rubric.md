# Praxis Visual Rubric

Use this rubric for screenshots, UI audits, and visual polish tasks.

## Contents

- Immediate Failures
- Hierarchy
- Product Specificity And Signature
- Layout And Density
- Themeability
- Forms And Config Editors
- Iconography
- State Design
- Accessibility
- Visual Fixture Coverage

## Immediate Failures

Fail the UI if any item is true:

- Operational/editor first viewport behaves like a landing page instead of exposing the working surface.
- Header, tabs, side panel, drawer, modal, footer, menu, or toolbar overlaps content.
- A dropdown, tooltip, select panel, autocomplete, context menu, or popover is clipped by its container.
- Text is truncated without an intentional truncation affordance.
- Helper text, labels, values, and section titles have nearly equal visual weight.
- More than two nested framed surfaces appear in the same region without strong structural reason.
- The primary action is not identifiable.
- Empty state consumes a large region without telling the user the next action.
- Focus state is invisible or visually inconsistent.
- Mobile or narrow layouts require horizontal scrolling for normal use.
- Dark theme relies mostly on borders instead of hierarchy, spacing, and surface contrast.
- Styling hardcodes colors, spacing, radius, elevation, typography, focus, overlay, or state values where Material/Praxis tokens should carry the theme.
- New internal editor/lib copy is hardcoded instead of using the applicable Praxis i18n path.
- Visual settings such as alignment, display mode, density, direction, or placement are exposed only as text selects when a familiar icon/segmented control is available.
- Compact controls are stranded in wide empty rows, or short visual choices are stretched to full-width fields without row-level purpose.
- A metadata-driven editor uses a rigid equal-column grid without considering field archetype, expected content length, semantic grouping, and responsive task order.
- A request for a modern, delightful, premium, or distinctive result is visually indistinguishable from an untouched Material sample or generic AI admin template.
- The stated visual thesis or product-specific signature cannot be identified in the rendered result.

## Hierarchy

Pass when:

- the main task, selected entity, and primary action are clear
- selected entity shows name, type, status, and incomplete/invalid state when applicable
- secondary actions are available but quieter
- headings and section labels create a predictable scan path
- selected state is visible without heavy border noise
- advanced controls do not dominate the default view
- primary action is in the shell or active work region, not hidden in a secondary card

## Product Specificity And Signature

For redesigns and requests for modern, delightful, premium, polished, or distinctive UI, pass when:

- the surface has a concrete visual thesis grounded in the operator and domain
- one memorable spatial, informational, typographic, data, or interaction signature is visible
- three likely generic defaults were named and replaced with intentional alternatives
- the result cannot be reduced to default Material styling plus local spacing changes
- the signature uses real workflow information and does not fabricate frontend-only semantics
- typography, composition, shape, color, iconography, and motion reinforce one direction
- boldness is concentrated in the signature while routine operational chrome remains quiet
- the product character survives empty, selected, invalid, busy, readonly, and narrow states
- the design remains host-themeable and accessible; distinction does not depend on hardcoded effects

## Layout And Density

Pass when:

- related controls are grouped by proximity before adding containers
- spacing follows a repeatable rhythm
- rows and control heights remain stable across states
- panels have clear purpose: navigation, canvas/editor, inspector, or details
- wide screens use space for comparison, editing, or preview rather than decorative emptiness
- at most one framed surface is nested inside the active work region unless the layout pattern documents a stronger reason
- repeated controls keep stable dimensions across hover, focus, invalid, selected, and busy states
- each row has an intentional distribution: full-width for long text/preview, paired columns for related medium fields, compact clusters for short choices/actions
- short controls such as booleans, modes, alignment, density, small presets, and icon choices use intrinsic or compact width unless emphasis requires otherwise
- blank grid cells are used only to preserve alignment, not as accidental whitespace
- grouping follows the user's task sequence rather than a fixed equal-column template
- every visibly awkward row can be explained as one of: full-width long content, paired medium fields, compact cluster, dependent inline group, or advanced section

## Themeability

Pass when:

- Angular Material tokens and Praxis tokens/CSS custom properties are the primary styling mechanism
- host applications can change theme without patching internal component CSS
- surfaces, overlays, focus rings, disabled/readonly states, selected state, and validation state inherit the active theme
- examples and playgrounds demonstrate token usage instead of raw local color systems
- component-local CSS uses fallback literals only behind a token or documented default
- public tokens, CSS custom properties, or theme hooks are introduced only through public-contract governance

## Forms And Config Editors

Pass when:

- labels are short and clear
- helper text explains constraints or consequences, not obvious labels
- field groups match the user's task model
- advanced fields are progressively disclosed
- validation appears near the cause and explains the fix
- keyboard flow is logical
- no card grid is used as the default config-editor layout
- enum controls use the right UI primitive for the meaning: segmented icon control for small visual choices, swatch for color/status, slider/stepper for numeric ranges, toggle for booleans, select/autocomplete for long or dynamic option sets
- controls with very different expected content length are not forced into equal widths when that creates visual imbalance

## Iconography

Pass when:

- icons are used for standard visual concepts such as alignment, visibility, layout, density, ordering, placement, and navigation
- icons come from the established Material/Praxis icon path instead of local SVG copies
- icon controls have accessible names and i18n-backed tooltips or labels
- selected, hover, focus, disabled, and readonly states are visible
- icon-only controls are compact and familiar; ambiguous controls use icon+text

## State Design

Pass when relevant states are designed:

- empty
- loading
- saving/applying
- error
- disabled
- readonly
- hover
- focus
- selected
- dirty/unsaved
- invalid/incomplete
- permission-limited
- long-content and high-volume data
- open overlay/dropdown/menu

## Accessibility

Pass when:

- contrast is sufficient in dark and light surfaces
- focus order follows visible order
- icon-only buttons have accessible names and visible tooltips when unfamiliar
- controls expose semantic roles through the chosen component library
- motion or animation is not required to understand state
- the primary task can be completed without a mouse when the underlying controls support keyboard operation
- focus is restored after modal, drawer, popover, or overlay close
- Escape, Enter, and Tab behavior is predictable for overlays and editor shells

## Visual Fixture Coverage

When feasible, validate with representative content:

- short and long names
- empty and populated list/table/tree
- selected item
- invalid field or incomplete rule
- loading and saving/applying state
- readonly or permission-limited state
- open overlay/dropdown/menu
- translated or longer UI text
- narrow viewport

If the fixture is not available, report the missing state instead of claiming full visual coverage.

