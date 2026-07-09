# Research Curation

Use this file to ground Praxis UI design guidance in current product-design and enterprise-UX practices.

## Design-System Operating Model

The adopted Praxis principle is not magic aesthetics; it is a design-system operating model. Lovable is useful as one reference point because its documented design-system workflow emphasizes persistent knowledge, reusable component systems, adherence checks, setup verification, live preview, and browser testing.

- keep persistent project/workspace knowledge with product vision, journeys, personas, features, design-system guidance, and role behavior
- define reusable design systems with components, styling guidelines, setup instructions, tokens, component catalog, constraints, and generated rules
- enforce adherence by detecting raw colors, one-off values, inline overrides, and local component implementations where design-system components should be used
- verify setup after design-system attachment: build config, CSS imports, theme providers, dependencies, and wiring
- use live preview, screenshots, and browser testing as part of the feedback loop

Praxis mapping:

- `AGENTS.md` is the durable workspace guidance.
- `codex-skills/praxis-ui-product-design` is the reusable design/UX playbook.
- `@praxisui/*` libraries and tokens are the canonical component system.
- Angular Material tokens and Praxis tokens must remain the primary theme surface so host applications can provide custom themes without component CSS patches.
- Browser screenshots and focused Playwright checks are the visual adherence loop.

## Enterprise Design-System Sources

Use these principles without copying another system's visual identity:

- Carbon: design systems combine working code, design tools, human-interface guidelines, and component guidance. Forms should gather information with little fuss, group related tasks, follow logical order, and progressively disclose additional inputs.
- Fluent 2: layout uses spacing and hierarchy to create relationships, highlight what matters, and help people make decisions; spacing should often replace extra divider lines.
- Atlassian: design systems are guidelines, foundations, tools, and components; layout shells and panels should constrain composition so responsiveness and rhythm remain consistent.
- shadcn/ui: start from well-designed, accessible, editable components that teams can customize and extend instead of rebuilding rough equivalents.
- NN/g complex-application guidance: complex apps should reduce clutter without reducing capability, support flexible workflows, coordinate transitions across workspaces, and make important information visually salient.

Official source links used during curation:

- Lovable design systems: https://docs.lovable.dev/features/design-systems
- Lovable best practices: https://docs.lovable.dev/tips-tricks/best-practice
- Lovable glossary: https://docs.lovable.dev/glossary
- Carbon design system: https://carbondesignsystem.com/
- Carbon forms pattern: https://carbondesignsystem.com/patterns/forms-pattern/
- Fluent 2 layout: https://fluent2.microsoft.design/layout
- Atlassian design system: https://atlassian.design/get-started/about-atlassian-design-system
- shadcn/ui: https://ui.shadcn.com/
- NN/g complex application design: https://www.nngroup.com/articles/complex-application-design/

## Praxis Product Interpretation

Praxis is closer to an enterprise authoring workstation than a marketing product.

Prioritize:

- task continuity
- scan speed
- edit confidence
- visible state
- stable layout
- canonical component reuse
- accessibility and keyboard operation
- visual hierarchy over decoration

Do not prioritize:

- generic SaaS landing-page composition
- oversized cards for every section
- decorative color or animation
- local patching that bypasses platform primitives
- aesthetic novelty over authoring correctness

## Surface-Specific Product Baselines

Authoring tools:

- selected object is visible and comparable
- dirty, invalid, saving, saved, readonly, and permission-limited states are visible
- primary editor/canvas/list/rule builder dominates the workspace
- preview/result is available when runtime effect or round-trip confidence matters
- Apply, Save, Reset, Cancel, destructive actions, and recovery are visually distinct

Runtime components:

- default, loading, empty, invalid, disabled, readonly, hover, focus, selected, and error states are covered when relevant
- host-provided labels/copy/config remain the source of domain text
- component tokens and accessibility semantics are preserved
- host theme customization works through Material/Praxis tokens

Playgrounds and examples:

- demonstrate real component behavior, not a marketing shell
- include realistic data and state controls
- keep explanatory copy short and connected to the example
- do not redefine contracts owned by backend/runtime/docs

Public docs:

- explain the component and show reproducible examples
- link back to canonical contracts when relevant
- avoid making docs the sole source of a runtime/backend contract

## Evidence To Capture In Final Reports

When using this research in a task, report:

- canonical owner selected
- design-system or component primitive reused or changed
- visual defects found before/after
- desktop and narrow/mobile screenshot coverage
- validation run and validation skipped
- derived docs/examples reviewed or explicitly not applicable
