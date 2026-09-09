# Widget shell material review

## Ownership and diagnosis

Core owns `projects/praxis-core/src/lib/widgets/widget-shell-presets.ts`,
`widget-shell.model.ts` and `widget-shell.component.ts`. Page Builder owns editing
and preview; the lab is a consumer. Classify an indistinguishable preset as
`ja-suportado-mal-nomeado-ou-mal-materializado` until tracing the actual catalog,
resolved `context.ui.shell`, explicit `appearance` and computed child styles proves
otherwise. Do not create a second host catalog or infer a material from its label.

Inspect `widget-shell-material.spec.ts`, `widget-shell-published-presets.spec.ts`,
the shell editor specs and the lab's `widget-surface-experiments.playwright.spec.ts`.
The public Core/Page Builder/Charts READMEs explain the supported fields and precedence.

## Material promises

- Glass needs a translucent surface, a useful backdrop and blur, plus paired text
  colors. Test dark and light backgrounds behind it. A gradient alone is not glass.
- Graphite is opaque. Elevation, outline, tonal and frameless treatments need visible
  differences in their corresponding properties, without changing the child's data.
- Card borders accept CSS widths/styles/colors per side; the header is one bottom
  divider. Validate against the specific CSS property, not a more permissive shorthand.
- A layered gradient border is continuous. Do not imply that native dashed or dotted
  gaps cut that gradient. The demonstration must explain that limitation.
- Check opaque fallback without backdrop-filter, with reduced transparency and in
  expanded/fullscreen or sticky-header modes; preserve foreground contrast.
- Nest shells. Material custom properties must not accidentally bleed from the outer
  card into an inner one; explicit context-based inheritance must continue to work.

## Proof matrix

Compare real Table, Chart, Dynamic Form and Micro Visualization consumers. Exercise
base presets, explicit overrides, clearing overrides, long content, empty/loading/error
states and narrow widths. Use the same inputs while comparing appearances. A chart's
accessible-data table must retain its own readable opaque foreground/background pair.

The lab's `widget-surface-experiments.ts` is a host-only fixture matrix of palette,
tone, fill and stroke combinations through existing `appearance`; those demo colors
are not new public tokens or preset IDs. Label active overrides as customized, and
turning the experiment off must restore the preset without replacing business inputs.

Measure computed rendered colors and alpha stops, including the background behind
transparent surfaces. Check that the requested palette actually reached the DOM
before reporting contrast. Synthetic fixture colors alone cannot certify the render.
Contrast measurements do not certify every intermediate gradient pixel, focus indicator,
chart mark, browser, assistive technology or possible corporate theme. Record the
matrix tested, its limits and the fresh execution separately from earlier reports.

Prove edit -> Apply/Save -> fresh reopen against the canonical config endpoint and
ETag. Use isolated test configurations and clean them up; do not overwrite shared
business fixtures. Visual proof and persistence proof are separate acceptance gates.
