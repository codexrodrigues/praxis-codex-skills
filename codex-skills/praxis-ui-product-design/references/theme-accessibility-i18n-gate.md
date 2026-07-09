# Theme, Accessibility, And I18n Gate

Use this reference when a Praxis visual change touches CSS, tokens, theme surfaces, overlays, icon-heavy controls, labels, tooltips, aria text, or internal editor copy.

## Token And Theme Protocol

Before changing visual CSS:

1. Locate the current owner of Material theme setup and Praxis CSS custom properties in the workspace.
2. Prefer existing Material tokens, Praxis tokens, or owner-provided CSS custom properties.
3. Treat a new public CSS custom property, token, exported theme helper, or documented theme hook as `contrato-publico`.
4. Use local CSS only for structural composition when it does not encode reusable color, typography, elevation, radius, density, state, or focus semantics.
5. If no token exists, classify the gap before adding one:
   - `ja-suportado-so-ux`
   - `ja-suportado-mal-nomeado-ou-mal-materializado`
   - `suportado-parcialmente`
   - `lacuna-real-de-contrato`

Hardcoded values are acceptable only as private fallbacks behind a token/default or for non-thematic geometry that belongs to the local layout.

## Host Theme Verification

When feasible, verify at least one custom host theme or theme-switch state. Check:

- the host loads a base Angular Material theme stylesheet before relying on Praxis token bridges
- surfaces, borders, focus rings, selected state, validation state, disabled state, and readonly state
- overlay panels and menus
- icon-only and segmented controls
- dark/light or high-contrast behavior when the surface supports it

`@praxisui/core/theme-bridge.css` complements Material/Praxis token mapping; it does not replace Angular Material component theme CSS. If Material-based controls render with native-looking geometry, cramped values, missing horizontal padding, or broken panel spacing, first verify the host's Material theme setup before patching a field component or consumer CSS.

If a host-theme fixture is not discoverable, report that limitation and perform static token review.

## Legacy-Driven Host Theme Modernization

When a Praxis host is being modernized from a legacy product identity, first gather concrete legacy evidence before choosing a palette:

- configuration entries for `logoUrl`, favicon, theme name, or skin name
- image assets under the cited legacy theme folder
- CSS colors used for page background, header, buttons, field focus, borders, links, and status states
- screenshots or templates that show how the legacy identity was actually presented

Prefer mapping these values into private host CSS variables, Material color variables, and Praxis token bridges owned by the host. Do not introduce new shared tokens, public CSS custom properties, or library-level theme hooks unless the same identity/theming requirement clearly applies to more than one Praxis package or official example; that becomes public-contract or platform design work.

For executive/client-facing modernization, keep the legacy brand recognizable but avoid copying legacy bitmap chrome wholesale. Use the old assets as anchors for logo, primary hue, focus color, border tone, and subtle gradients, then express them through modern surfaces, readable contrast, stable field geometry, and visible keyboard focus.

## Overlay Gate

For Material or CDK overlays, verify:

- overlay inherits the active theme class through `OverlayContainer` or the established Praxis bridge
- z-index/layering does not cover shell actions incorrectly
- panel is not clipped by drawer, modal, tab body, or scroll container
- Tab, Shift+Tab, Escape, Enter, and click-away behavior are predictable
- focus returns to the trigger or appropriate next control on close
- scroll strategy does not detach the panel from its trigger

Capture an open overlay screenshot when the change affects select, autocomplete, menu, tooltip, dialog, drawer, popover, or context menu behavior.

## Accessibility Gate

Visual polish must preserve:

- WCAG AA contrast for normal text, helper text, focus, and state indicators where applicable
- visible focus in dark and light themes
- keyboard path for the primary task
- accessible name for icon-only controls
- correct selected/pressed/expanded state for segmented, toggle, menu, and disclosure controls
- reduced-motion compatibility when animation is added
- logical focus order matching visual order

Prefer Material/Praxis components because they carry roles and keyboard behavior. Custom controls need explicit role, aria state, keyboard handling, focus styling, and tests or browser verification when risk is meaningful.

## I18n Gate

Before adding or changing user-visible text:

1. Discover the package's existing i18n path.
2. Use `PraxisI18nService`, the owning lib namespace, and base catalogs when that is the local convention.
3. Update required catalogs together, typically `pt-BR` and `en-US` when present.
4. Validate long translated text in the visual layout.
5. Include labels, placeholders, helper text, tooltips, aria text, empty states, validation, and error messages.

Do not hardcode internal lib/editor copy unless local guidance explicitly permits it.
