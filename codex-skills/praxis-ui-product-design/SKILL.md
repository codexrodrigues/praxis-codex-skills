---
name: praxis-ui-product-design
description: "Use alongside the canonical functional Praxis skill when the user's request materially asks for visual/product UX quality in Praxis web UI: auditing, reviewing, redesigning, polishing, screenshot QA, visual hierarchy, layout composition, responsive behavior, dark theme quality, accessibility of visual controls, or making Angular UI, authoring editors, settings panels, dynamic form/table/list experiences, playgrounds, or examples feel modern, elegant, usable, professional, or product-grade. Do not use as the primary skill for config round-trip, config shape, persistence, apply/save/reset correctness, public APIs, dynamic-fields discovery, metadata contracts, or ordinary editor correctness unless visual UX is explicitly in scope."
---

# Praxis UI Product Design

Use this skill to make Praxis UI work like a product-grade enterprise authoring platform, not like a raw internal demo.

This is a visual/product QA layer. Use it with the functional Praxis owner skill whenever semantics, contracts, persistence, dynamic-fields discovery, or editor correctness are also in scope.

## Operating Modes

Choose the mode from the user's request before taking action:

- Audit/review mode: inspect, gather evidence, capture screenshots when feasible, and report prioritized findings. Do not edit files unless the user explicitly asks for fixes.
- Implementation mode: edit only when the request asks to create, redesign, polish, improve, fix, or apply changes.

If the request is ambiguous, default to audit/review mode for review wording and implementation mode for build/fix/polish wording.

## Governance Preflight

Before editing in implementation mode, apply the active root, workspace, and subarea `AGENTS.md` files. Local AGENTS may narrow owner, validation, public artifacts, origins, and no-edit areas.

Explicitly classify the change:

- `local-pequena`
- `transversal`
- `arquitetural`
- `contrato-publico`
- `docs-apenas`

For `transversal`, `arquitetural`, or `contrato-publico`, produce the required short plan and impact map before editing:

- canonical subproject affected
- impacted consumers
- public docs potentially affected
- examples, playgrounds, or recipes potentially affected
- minimum tests or validations
- breaking-change risk

Visual/product design does not authorize new public contracts. If the UX need appears to require a new public token, input, output, event, service, config shape, `public-api`, `ComponentDocMeta`, AI manifest field, or metadata-driven field, first classify the fit as:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` can justify a new contract, and it must follow the repository governance gates.

When the same work also uses Angular host or migration skills, align these UX classifications with the shared platform feedback vocabulary:

- `ja-suportado-so-ux` -> `already-supported`: use the native Praxis path and fix only UX/presentation.
- `ja-suportado-mal-nomeado-ou-mal-materializado` -> `already-supported` or `supported-partially`: consume the native primitive, then improve naming/materialization in the owner.
- `suportado-parcialmente` -> `supported-partially`: keep the smallest temporary bridge and record the removal trigger.
- `lacuna-real-de-contrato` -> `platform-gap`: open or register a traceable platform follow-up before adding public contract surface.

If a recurring visual workaround comes from weak migration guidance rather than a missing UI contract, classify it as `migration-skill-gap` and update the relevant `codex-skills/` source.

## Design System Stance

Treat visual quality as a platform concern. Before editing UI, identify the canonical owner of the visual or interaction problem:

- shared component or token in `@praxisui/core`
- component library surface in `@praxisui/*`
- authoring editor or settings-panel pattern
- host/demo-specific composition
- public example, recipe, or playground

Do not solve systemic UI problems with one-off CSS in a consumer. If the same issue would appear in multiple Praxis components, fix the shared primitive, token, component, or editor pattern.

Praxis UI must remain host-themeable. Use Angular Material theming tokens and Praxis design tokens/CSS custom properties as the first styling surface for color, typography, density, spacing, radius, elevation, focus, state, overlay, and surface contrast. Do not hardcode visual values in components, editors, examples, or hosts when a Material or Praxis token can express the intent. Host applications must be able to customize theme without patching internal component CSS.

When theming `@praxisui/table` from a host, prefer the component-owned `--p-table-*` CSS custom properties on the `praxis-table` host, such as header, row, border, paginator, and selection tokens. If the table component declares host-level defaults with higher specificity, override the same tokens on the concrete host state/class instead of styling MDC/Material internals or adding `!important`.

Use this owner decision matrix:

- affects 2+ libs, overlay layers, focus behavior, theme bridge, typography, spacing scale, color tokens, or shared surface contrast -> `@praxisui/core` or the shared owner
- affects one configurable editor family -> the owning `@praxisui/*` lib
- affects Settings Panel shell, footer actions, drawer sizing, or `SettingsValueProvider` UX -> `@praxisui/settings-panel`
- affects only a demo/example with no reusable pattern -> host/demo
- affects config shape, persistence, apply/save/reset, runtime/editor parity, or public APIs -> load the functional owner skill before this visual layer

For `controlType`, aliases, `optionSource`, `async-select`, inline filters, dynamic-fields overlays, package-owned field tokens, or editorial discovery, use `praxis-dynamic-fields-editorial` as the primary skill and this skill only for visual QA.

## Research-Informed Defaults

Apply the detailed rubrics in `references/` when relevant. The non-negotiable defaults are: reuse shared components, preserve host theming through Material/Praxis tokens, choose controls by user intent rather than metadata shape, size fields by content and task importance, keep enterprise screens dense but scannable, validate visual changes with screenshots when feasible, and never trade accessibility or i18n for visual polish.

## Enterprise Authoring Workstation Baseline

Operational and editor screens must expose the working surface, not behave like a landing page. They fail if the first viewport is dominated by hero copy, decorative cards, large illustrations, decorative gradients, or explanatory marketing text instead of the actual task surface.

For Praxis authoring tools, make these visible when applicable:

- current selection: name, type, status, and incomplete/invalid state without opening a hidden panel
- global state: dirty, invalid, saving/applying, saved, readonly, permission-limited
- primary work region: editor/canvas/table/list/rule builder is visually dominant
- action priority: primary, secondary, destructive, and reset/cancel actions are distinct
- persistence feedback: apply/save/reset result is visible near the shell or active work area
- comparison: lists or trees support scanning and comparing related objects
- preview/result: available when round-trip confidence or runtime effect is material
- recovery: errors explain cause and next step without losing progress

First viewport heuristics:

- the primary work region is the largest meaningful region on desktop
- header, tabs, filters, helper text, and toolbar chrome do not dominate vertical space
- inspectors are secondary unless the task is pure property editing
- preview/result is not weaker than helper text when runtime confidence matters
- selected entity summary remains visible in long inspectors or detail panes

## Praxis Visual Doctrine

Praxis UI should feel:

- precise, operational, and trustworthy
- compact without being cramped
- visually quiet until state or action requires emphasis
- metadata-driven but understandable to a human author
- consistent across runtime, authoring, examples, and docs

Avoid:

- nested cards or framed panels without a real information-architecture purpose
- using borders as the primary layout mechanism
- one-off color literals, spacing values, shadows, radii, or typography
- Material/Praxis-token bypasses that prevent host theme customization
- decorative gradients or oversized empty marketing composition in operational tools
- dark-theme surfaces where labels, values, helper text, and borders have similar weight
- local copies of controls that should come from a shared Praxis component

## Preflight

Before editing, answer:

1. What is the primary user workflow?
2. What is the primary action and what is secondary?
3. Which shared Praxis component, token, or editor pattern owns the issue?
4. Is the problem layout architecture, component design, state design, copy, accessibility, or visual polish?
5. Which surface type is this: authoring tool, runtime component, playground/example, or public docs?
6. Are any fields visual choices that should use icons, swatches, segmented controls, sliders, or toggles instead of a generic select?
7. Are commands, modes, filters, navigation, and destructive actions represented by distinct UI primitives?
8. Does the grid distribution match control importance, content length, and grouping, or are there orphan controls/empty columns?
9. Which desktop and narrow/mobile viewport must be checked?
10. Which public examples, playgrounds, recipes, or docs mirror this UI?

If the task affects config shape, persistence, apply/save/reset, dynamic fields discovery, or public component contracts, load the corresponding Praxis canonical skill before editing.

## Surface Matrix

Use the surface type to tune the work:

- Authoring tools: optimize selection, editing, preview/result, dirty/invalid state, persistence, permissions, keyboard flow, and recovery.
- Runtime components: optimize clarity of use, accessibility, tokens, states, responsive behavior, and host integration.
- Playgrounds/examples: optimize demonstrability, realistic controls, minimal explanatory copy, reproducible states, and links back to docs/contracts without redefining them.
- Public docs: optimize explanation, examples, screenshots, and reproducibility; never redefine backend/runtime contracts alone.

## Audit Workflow

Use this workflow when the user asks to review, analyze, critique, inspect, or assess:

1. Inspect the existing UI implementation, applicable AGENTS files, nearby patterns, and available screenshots.
2. Load `references/praxis-visual-rubric.md`; load other references only as their conditions apply.
3. Gather static evidence with focused probes when useful:
   - raw visual literals: `rg "#[0-9a-fA-F]{3,8}|rgb\\(|hsl\\(" <scope>`
   - style bypasses: `rg "::ng-deep|!important|box-shadow|border-radius|z-index" <scope>`
   - token usage: `rg "--pdx-|--praxis-|mat-|Material|token" <scope>`
   - overlay risks: `rg "Overlay|cdk-overlay|mat-select|mat-menu|mat-dialog|mat-autocomplete" <scope>`
   - i18n paths: `rg "PraxisI18nService|i18n|pt-BR|en-US" <scope>`
   - public surfaces: `rg "public-api|@Input|@Output|InjectionToken|ComponentDocMeta" <scope>`
4. Classify findings by hierarchy, information architecture, layout, component choice, interaction primitive choice, spacing/density, spatial composition, state design, accessibility, responsive behavior, theme/tokens, and i18n.
5. Report prioritized findings with file/screenshot evidence and recommend the canonical owner. Do not edit.

## Implementation Workflow

Use this workflow when the user asks to create, redesign, polish, improve, fix, or apply changes:

1. Inspect the implementation, applicable AGENTS files, nearby patterns, and functional owner skill.
2. Run the Governance Preflight and impact map when required.
3. Load required references for the affected visual dimension.
4. Run the quick design-system audit: reused components, Material tokens, Praxis tokens/custom properties, raw values, host-themeability, local duplicate controls, missing primitive/owner, i18n path, and overlay behavior.
5. Classify the UX problem and decide whether the fix belongs in a shared Praxis primitive, owning lib, settings-panel shell, or local host/demo.
6. Implement the smallest canonical platform fix that satisfies repository governance.
7. Run the smallest relevant build/test for the changed package.
8. Open the UI only through official scripts, routes, ports, and origins. Do not invent local servers or origins.
9. Capture desktop plus narrow/mobile screenshots when feasible, including open overlay states when relevant. When the workflow opens a Settings Panel, metadata editor, drawer, side sheet, or inspector, include at least one screenshot with that editor open in the narrow viewport; runtime-only narrow screenshots can miss clipped editor copy, hidden controls, and broken authoring access.
10. Inspect screenshots against the rubrics and iterate on the top visual defects before reporting completion.

If browser validation is not feasible, state exactly why and perform static review against the rubrics.

## Authoring Editor Patterns

For detailed authoring editor guidance, load `references/authoring-editor-patterns.md`. Core rules:

- keep navigation, selection, editing, preview, and persistence roles visually distinct
- make the primary canvas/editor/list/rule builder visually dominant
- use guided builders for rules, actions, conditions, and effects
- use icon or icon+text segmented controls for standard visual options
- group rows by task and size fields by expected content and importance

Avoid:

- property dumps, arbitrary equal-column grids, generic text selects for visual options, clipped overlays, stranded compact controls, and card grids as the default editor layout

## Must-Fail Checks

A Praxis UI change is incomplete if any of these are true:

- the main task is not visually obvious within a few seconds
- the primary action is not clearly prioritized
- a common visual option is represented by a generic text select when a familiar icon/segmented control would be clearer
- a compact field is stretched or stranded in a wide empty row without a layout reason
- text is clipped, overlapped, hidden, or too low contrast
- popovers, dropdowns, tooltips, dialogs, drawers, or overlays are clipped
- narrow/mobile authoring depends on a global toolbar control that is hidden at that breakpoint and the validated workflow has no equivalent accessible entrypoint
- keyboard focus is invisible or the primary keyboard task path is broken
- mobile or narrow layout requires horizontal scrolling for ordinary use
- the implementation bypasses shared Praxis tokens or components without justification
- styling bypasses Material/Praxis tokens and would require host CSS patching to theme
- new internal lib/editor copy is hardcoded instead of using the applicable Praxis i18n path
- CSS custom properties or tokens are introduced as public theming surface without public-contract governance

Load `references/praxis-visual-rubric.md` for the full rubric.

## Validation Evidence

Separate visual evidence from contract evidence:

- Visual evidence: route, official origin/port, viewport sizes, states captured, screenshot/browser tool used, defects fixed, defects deferred.
- Contract evidence: build/test/spec/e2e required by the changed package, public API, config shape, manifest, or AGENTS guidance.

Screenshot evidence never replaces required contract validation.

## References

Load only what is needed, but follow these mandatory routing rules:

- `references/research-curation.md` for the external design-system and UX principles behind this skill.
- Load `references/praxis-visual-rubric.md` in audit mode and before screenshot review.
- Load `references/authoring-editor-patterns.md` for settings panels, builders, schema editors, rule editors, metadata-driven authoring, field layout, or workstation composition.
- Load `references/interaction-control-selection.md` when replacing or choosing selects, buttons, fields, commands, choices, modes, filters, visual properties, destructive actions, preview, or bulk operations.
- Load `references/theme-accessibility-i18n-gate.md` when changing CSS, tokens, theme surfaces, overlays, icon-heavy controls, labels, tooltips, aria text, or internal editor copy.
- Load `references/screenshot-review-checklist.md` before finalizing visual UI work.
