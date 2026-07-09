---
name: praxis-rich-crud-screen-authoring
description: Create focused CRUD screens with the @praxisui/crud Angular component using canonical Praxis resource metadata, endpoints, table configuration, built-in form launchers, open modes, capabilities, and actions. Use when the user asks to scaffold, improve, or test a standard Praxis CRUD screen, backoffice resource management page, table-plus-create-edit-view flow, modal/drawer CRUD form flow, or fast CRUD screen powered by Praxis UI Angular.
---

# Praxis CRUD Screen Authoring

Use this skill to create fast, focused CRUD screens with `@praxisui/crud`. The CRUD component already orchestrates table, create/edit/view actions, open modes, and embedded form flows. Do not compose separate `praxis-dynamic-form`, `praxis-table`, `praxis-list`, `praxis-tabs`, or `praxis-dynamic-page` widgets unless the user explicitly asks for a composed dashboard or master-detail experience.

## Operating Rules

- Read the repo `AGENTS.md` files that apply before editing.
- Classify the change before editing: `local-pequena`, `transversal`, `arquitetural`, `contrato-publico`, or `docs-apenas`.
- If the task touches public contracts, generated artifacts, `x-ui`, `/schemas/filtered`, AI contracts, public APIs, examples, playgrounds, or more than one subproject, produce a short plan and impact map before editing.
- Prefer the platform-correct solution over local Angular shortcuts.
- Do not introduce keyword, regex, alias, or fuzzy-text routing as the primary intent decision mechanism.
- Do not create new DTOs, exported types, metadata fields, endpoints, or UI config contracts until you inventory what Praxis already knows.

## First Questions

Ask only what is needed to resolve the canonical CRUD scope:

1. What canonical Praxis resource or endpoint should this CRUD manage?
2. What CRUD mode is expected: simple, operational, or workflow-oriented?
3. Which open mode should the built-in CRUD forms use: modal, drawer, route, or the existing platform default?

If the user already provided the resource and objective, continue without asking.

Do not start by asking for colors, layout taste, or unrelated components. First resolve the resource semantics and the `CrudMetadata`.

## Metadata Inventory

Before designing the CRUD screen, discover what the platform already exposes.

Check, when available:

- canonical resource key and base endpoint
- `/schemas/filtered`
- `/schemas/surfaces`
- `/schemas/actions`
- collection and item capabilities
- HATEOAS links
- `x-ui`
- labels, descriptions, field types, validations, required fields
- option sources, async selects, entity lookups used by the built-in form
- allowed create/edit/view/delete/workflow actions
- ETag and required headers
- existing CRUD examples, labs, playgrounds, or docs for the same resource

Use `praxis-core-resource-runtime` when CRUD behavior depends on core schema discovery,
`GenericCrudService`, capabilities, actions, HATEOAS links, option sources, related-resource
surfaces, or CRUD operation resolution. Use `praxis-core-runtime-contracts` if the task touches
core public API, tokens, providers, or shared model contracts.

For each relevant improvement, classify adherence:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new contract. If there is a real gap, state what behavior cannot be implemented correctly, which canonical source owns the missing data, which consumers are affected, which derived artifacts change, and what minimal validation proves the contract.

## Component Boundary

This skill is for `@praxisui/crud` only.

Use:

- `PraxisCrudComponent`
- `CrudMetadata`
- `metadata.resource.path`
- `metadata.resource.idField`
- `metadata.table`
- `metadata.actions`
- `metadata.defaults.openMode`
- `crudId`
- `enableCustomization`
- built-in create/edit/view form launchers through CRUD actions

Do not use these unless explicitly requested:

- `DynamicWidgetPageComponent`
- direct `praxis-dynamic-form` next to the CRUD
- direct `praxis-table` next to the CRUD
- direct `praxis-list` next to the CRUD
- direct `praxis-tabs`, `praxis-expansion`, charts, steppers, or custom dashboards

If the user asks for those, use or create a separate composed-screen/master-detail skill. Do not stretch this CRUD skill into an application builder.

When the CRUD screen depends on richer table behavior inside `PraxisCrudComponent`, use `praxis-table-runtime-data` for table runtime/data-mode/export concerns, `praxis-table-filter-actions` for filters and row/toolbar/bulk actions, and `praxis-table-authoring-settings` for table editor or Settings Panel parity.

When CRUD opens or embeds richer Dynamic Form behavior, use `praxis-form-runtime-submit` for schema/submit/runtime contracts, `praxis-form-authoring-settings` for form editor round-trip, and `praxis-form-layout-canvas` for schema-driven form layout or visual blocks.

## CRUD Experience Selection

Select the smallest CRUD experience that fits the workflow:

- Simple CRUD: resource metadata plus default table and built-in create/edit/view form actions.
- Operational CRUD: dense table, primary columns, advanced filters, toolbar action, row actions, export, and modal/drawer forms.
- Workflow-oriented CRUD: CRUD plus canonical workflow actions already exposed by metadata/actions/capabilities.

Prefer modal or drawer forms for fast CRUD flows. Prefer route forms only when the existing app pattern or resource complexity requires it.

## UI Composition Guidance

For a non-trivial CRUD, produce a short proposal before implementation:

- resource endpoint and id field
- primary table columns
- filters and search scope
- toolbar actions
- row actions
- create/edit/view open mode
- built-in form ids
- metadata/capability evidence behind important choices

Keep the screen usable and direct. A CRUD skill should accelerate development, so avoid elaborate wrapper layouts, dashboards, or multi-widget pages.

## Implementation Workflow

1. Inspect existing app routes, feature conventions, and local `AGENTS.md`.
2. Inspect the target resource metadata and existing CRUD examples.
3. Decide whether this is a local CRUD host, a reusable `@praxisui/crud` fix, or a contract/platform change.
4. Implement a standalone Angular component that hosts `<praxis-crud>`.
5. Pass a focused `CrudMetadata` object with resource, table, actions, and defaults.
6. Use the CRUD component's built-in form launchers for create/edit/view.
7. Update derived artifacts only if public examples, docs, manifests, playgrounds, or AI surfaces are affected.
8. Run the smallest reliable validation for the changed scope.

For `praxis-ui-angular`, prefer focused builds or tests for the affected app feature or `@praxisui/crud` lib. For public API or cross-lib changes, also validate a direct consumer. Do not use GitHub Actions as the normal development validation path.

## Route Lab Convention

When creating routes to test this skill inside the Angular workspace, prefer:

`praxis-ui-angular/src/app/features/skills-lab/`

Keep skill test routes isolated from existing demos unless the task explicitly promotes the example to an official demo, recipe, or playground. Prefer a local route file such as `skills-lab.routes.ts` inside that folder. Do not wire the route into `src/app/app.routes.ts` when local repo rules restrict edits outside `src/app/features/**`; leave the route candidate exported and ask for explicit authorization before editing the root app route table.

## Completion Checklist

Before finishing, state:

- canonical resource or endpoint used
- metadata/capability surfaces inspected, or why they were unavailable
- adherence classification for notable gaps
- `@praxisui/crud` inputs/actions/open mode used
- files changed
- validation run
- derived artifacts updated, or why none were required
