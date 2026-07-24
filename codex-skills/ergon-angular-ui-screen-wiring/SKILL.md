---
name: ergon-angular-ui-screen-wiring
description: Translate Ergon/Archon legacy XML screens into new Angular features using Praxis UI. Use when Codex must inspect docs-legado XML/runtime artifacts, identify already-ready Java APIs for a legacy functionality, improve Praxis DTO/FilterDTO/@UISchema/option metadata, wire ui-administracao-pessoal routes/components with @praxisui tables/forms/crud/list, or create reusable UI migration handoff artifacts after read/write API migration.
---

# Ergon Angular UI Screen Wiring

Use this skill to turn a legacy Ergon/Archon screen into a fast, metadata-driven Angular implementation with Praxis UI.

Apply the root migration `AGENTS.md` before changing Angular, DTO/schema, or
runtime integration. The screen must use native Praxis contracts and services
where they exist; defects owned by `praxis-ui-angular`,
`praxis-metadata-starter`, or `praxis-config-starter` must become
`Praxis Platform Follow-up` evidence instead of Ergon-local platform patches.

Before editing Angular, docs, DTO/schema wiring, tests, or generated migration
artifacts, run the duplicate-module-root guard from
`ergon-migration-orchestration` for the target module/artifactId. Do not accept
browser or test evidence produced from a competing temporary root such as
`migracao-package/<module>` unless the user explicitly selected that root for
the task.

Treat Angular as the cockpit for governed Praxis materializations, not as the
source of business semantics. The UI may compose, bind, and visually verify
metadata-driven resources, but it must not decide user intent, redefine field
meaning, invent action availability, or replace missing backend contracts with
screen-local conventions.

## Required Companion Skills

Load only the skills needed for the current task:

- Use `ergon-migration-orchestration` to decide whether the screen is allowed to move into UI work.
- Use `ergon-archon-screen-discovery` when XML/runtime lineage is missing or stale.
- Use `ergon-archon-read-api-migration` when a required read endpoint is absent or incomplete.
- Use `ergon-archon-write-api-migration` when create/update/delete/duplicate actions are in scope.
- Use `ergon-fieldspec-ui-contract` and `praxis-dto-annotations` before changing DTO, FilterDTO, `@UISchema`, `@Filterable`, options, or `/schemas/filtered`.
- Use `praxis-angular-host-project`, `praxis-component-minimums`, and `praxis-dynamic-fields-editorial` before wiring Angular or choosing Praxis controls.
- Use `praxis-rich-crud-screen-authoring` when the target shape is a standard table-plus-create/edit/view/delete flow with `@praxisui/crud`.
- Use `praxis-ui-product-design` and browser/Playwright validation for visual QA.

## Native Praxis Source Audit

Before creating or changing Angular components, routes, config objects, or adapters, inspect the current Praxis runtime source and record the result in `ui-implementation-plan.md`:

- `@praxisui/core`: `API_URL`, `PAX_FETCH_HEADERS`, `ResourceDiscoveryService`, `CrudOperationResolutionService`, `ResourceActionOpenAdapterService`, `ResourceSurfaceOpenAdapterService`, `SurfaceOpenMaterializerService`, `GlobalActionService`, `PraxisSurfaceHostComponent`, and `GenericCrudService`.
- `@praxisui/crud`: `PraxisCrudComponent`, `CrudLauncherService`, open-mode resolution, standard drawer/modal/route behavior, CRUD metadata, and native refresh-after-save/delete flow.
- `@praxisui/table`: `PraxisTable`, schema/filter consumption, row/toolbar actions from capabilities, `duplicate-draft`, `surface.open`, `queryContext`, and event outputs.
- `@praxisui/dynamic-form` and `@praxisui/dynamic-fields`: schema-backed detail/create/edit forms, option-source controls, selected-value reload, command rules, and field shell/editor behavior.

Classify each requested UI feature with the platform adherence categories:

- `ja-suportado-so-ux`: use native Praxis APIs and adjust only composition/layout.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: fix DTO/schema/catalog/resource metadata before adding UI code.
- `suportado-parcialmente`: implement the smallest host composition while recording the missing platform extension.
- `lacuna-real-de-contrato`: stop UI implementation and create the canonical Praxis follow-up with owner, affected consumers, derived docs/examples, tests, and removal criteria.

Only `lacuna-real-de-contrato` may justify a new platform contract. Do not add an Ergon-only `actions`, `surfaces`, lookup, drawer, field semantics, command router, or table adapter layer when the native Praxis runtime already owns the concept.

## Workflow

1. Identify the screen and legacy source.
   - When `docs/migracao/praxis-screen-discovery-matrix.md` exists, use the screen record to select a comparable native Angular reference and identify any manual-runtime residual. Confirm its conclusions in the UI gate and canonical Praxis surfaces before coding.
   - In the ErgonX migration workspace, read `docs/migracao/angular-ui-praxis-migration-roadmap.md` before creating or reviewing a new UI slice. It records the reusable ERGadm00034 lessons and the Cronos rendering model.
   - Also read `docs/migracao/native-praxis-first-guide.md` when it exists. It is the short operational gate for current post-`@praxisui/* 9.0.0-beta.33` Angular work and takes precedence over older pilot patterns.
   - Prefer runtime XML under `docs/migracao/<SCREEN>/runtime`.
   - Use local XML under `docs-legado` only as a candidate unless the phase gate approved it.
   - For Cronos/Archon `.tp` screens, remember that the legacy page is rendered from `TransacaoDescription` through `PageServlet`, `TransacaoDescriptionGetter`, `TransacaoDescriptionRenderer`, `DescriptorRenderer`, and `PaginaWrapper`; exported runtime XML is a serialization of that descriptor, not merely a static file copy.
   - Capture form blocks, grids, filters, buttons/actions, tabs, LOVs, dependencies, and context fields.

2. Classify each legacy element.
   - `filter`: fields used to query the table.
   - `grid`: response DTO/table columns.
   - `detail`: read-only or editable form fields.
   - `tab`: a visible section that must be classified as same-resource detail, child table/subresource, related form, reusable embedded feature, or deferred scope.
   - `action`: new/edit/delete/duplicate/export/print/workflow command.
   - `context`: company, user, role, package flags, session, or hidden infrastructure; do not expose these as public FilterDTO fields unless explicitly approved.
   - `layout-only`: labels, separators, legacy usage buttons, visual grouping, empty containers.

3. Find reusable APIs before creating anything.
   - Search controllers, services, DTOs, FilterDTOs, `ApiPaths`, tests, and docs for matching resource names and legacy binds.
   - Confirm endpoints support the required operation: `/filter`, `/schemas/filtered`, `/options/filter`, `/options/by-ids`, option-sources, find-by-id, and commands.
   - Treat an API as UI-ready only when schema request/response metadata and smoke/parity evidence exist.
   - If a required visible filter, detail field, table column, option/LOV, selected-value reload, or action capability is missing or weak in the backend contract, stop UI implementation and return the issue to Phase 2/3 or Phase 5/6. Do not patch around it in Angular.
   - To prove the UI migration route generalizes, require at least one non-ERGadm00034 pilot to pass the same readiness, DTO, schema, Angular, and browser gates before calling the roadmap reusable.

4. Validate and improve DTO metadata.
   - Compare XML fields and SQL binds with the current DTO/FilterDTO.
   - Before choosing `@Schema` text, `@UISchema.description`, `helpText`, `tooltipOnHover`, controls, `@UISchema(icon)`, `@DomainGovernance`, or `AiUsagePolicy`, consult legacy functional/modeling docs when available (`docs-legado/v7x/help`, `docs-legado/v7x/docs`, `docs-legado/Doc-Sistemas`, EA/XML documentation, and commented DDL/source). Use those facts for business semantics, not as sole SQL/key/runtime proof.
   - Classify every visible field as `CONFIRMED_SEMANTIC`, `TECHNICAL_ONLY`, or `SEMANTIC_UNCONFIRMED` before marking the DTO ready for UI. A field with only a Java name, XML label, database column, or "checkbox legado" explanation is not semantically ready.
   - Treat weak public copy as a backend DTO defect, not a UI polish issue. Missing accents in PT-BR labels, absent `helpText`, generic descriptions, vague icons, raw code values shown where a resolved display field exists, or ambiguous boolean text must return to DTO/schema hardening before Angular compensates locally.
   - For resolved values, decide whether the API publishes a display field, a composed display field, lookup metadata, or a supported `valuePresentation` contract. Do not make Angular concatenate code + description or invent business labels unless the DTO/schema exposes that presentation contract.
   - Decide DTO ownership with `references/praxis-screen-composition.md`: one DTO family per API resource/operation, not one DTO per visual tab by default.
   - Keep session/context values out of public DTOs.
   - Use the control selection matrix in `references/praxis-control-selection.md`.
   - Add or correct `@Schema`, `@UISchema`, `@Filterable`, validation annotations, option metadata, read-only flags, ordering, and labels.
   - Add tests for OpenAPI/schema/x-ui when metadata changes.

5. Translate to Angular with Praxis UI.
   - Prefer resource-driven components over hand-built forms.
   - Classify the UI implementation shape before coding as `native-crud`, `native-table-detail`, `native-table-related-surfaces`, `workflow-action`, or `manual-temporary-gap`. Record the classification in `ui-implementation-plan.md` and `ui-execution-gate.md`.
   - Use `docs/migracao/ERGadm00034/ui-praxis-reference-package-20260702.md` as the current transational reference when it exists. After `@praxisui/* 9.0.0-beta.33`, the reference shape is schema-driven table/detail/forms plus `CrudLauncherService` drawer launch; do not copy historical host-owned `command-drawer` shells.
   - Use `docs/migracao/ui-native-praxis-reference-audit-20260703.md` to choose the narrowest current reference shape. Current complementary examples include `ERGadm00038` for CRUD plus workflow action and related surface, and `ERGadm00229` for read-only table/detail with an external parent selector and native read-only related surfaces. Treat any browser replay residual in those packages as validation evidence still pending, not as permission to reintroduce manual related tables.
   - Before creating any custom Angular launcher, adapter, selector, autocomplete, entity lookup, action/surface opener, capability model, or config editor, inventory the native Praxis runtime and classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only a real contract gap may become a Praxis platform follow-up; supported cases must use the native package path.
   - Use `resourcePath` relative to the configured API base, for example `administracao-pessoal/codigos-frequencia`.
   - Let Praxis table/filter/form consume `/schemas/filtered` wherever possible.
   - Do not build an Ergon launcher for `_links`, `/actions`, `/surfaces`, or `/capabilities`. The Angular packages already provide the native discovery/runtime path through services and components such as `PraxisCrudComponent`, `PraxisTable`, `ResourceDiscoveryService`, `ResourceActionOpenAdapterService`, `ResourceSurfaceOpenAdapterService`, `SurfaceOpenMaterializerService`, `CrudOperationResolutionService`, `CrudLauncherService`, and `GlobalActionService`.
   - Enable and configure the native Praxis discovery path for row, collection, and global operations. If host config disables discovery, such as `actions.row.discovery.enabled = false`, record why in the UI gate and do not call that screen scalable until the backend/runtime contract is consumed natively.
   - For CRUD-style screens, prefer `PraxisCrudComponent` and `CrudLauncherService`. Custom shell composition may use official Praxis services and adapters, but must not duplicate discovery, availability, or action/surface materialization locally.
   - Treat table empty states as a native Praxis state contract, not as host markup. For an initially empty mutable collection, `PraxisCrudComponent` must derive a compact contextual state from the resource label and canonical `create` action. For `surface.relatedResource`, use the state derived by `praxis-related-resource-outlet`. Do not add a screen-local `praxis-empty-state-card`, duplicate create button, or CSS patch inside a table.
   - Keep empty-state contexts distinct: initial empty may expose the canonical create action; filtered/searched empty must guide filter revision and must not suggest creating a duplicate; read-only or permission-limited empty must explain absence without rendering an unavailable action. Explicit `TableConfig.behavior.emptyState` is reserved for a proven domain-specific override and must remain metadata/config driven.
   - For standard CRUD screens, configure `PraxisCrudComponent` from resource metadata, capabilities, `_links`, `/schemas/filtered`, and CRUD metadata. Do not split it into local table + local drawer unless the native source audit classified an actual platform gap.
   - For create/edit or schema-backed commands, use `CrudLauncherService`/`PraxisCrudComponent` with `openMode='drawer'` before building any host-owned drawer. A local drawer, backdrop, z-index, focus policy, submit callback shell, or custom command launcher is allowed only as `manual-temporary-gap` with owner, removal trigger, and an entry in `docs/migracao/platform-issues.md`.
   - For read-only details, use `PraxisDynamicForm` with `responseSchemaUrl` and `layoutPolicy.source='schema'`, `intent='detail'`, `preset='compactPresentation'` before declaring `FormConfig.sections`. Do not keep `sections: []` placeholders.
   - For master-detail headers, require the backend resource to declare `@ApiResource(identity = @ResourceIdentity(...))`. Consume the `resourceIdentity` included in Praxis Table/CRUD row and selection events and render it with `PraxisResourceIdentityComponent`; do not parse `displayLabel`, concatenate code/name in a mapper, or duplicate `keyField/titleField/metadataFields` in the screen.
   - A record key shown in the detail header should remain visually dominant and inherit its field `x-ui.presentation` prefix when applicable; the human title follows it, and ordered secondary metadata stays quieter. This is the canonical dense list-detail signature, not permission for host-owned CSS around raw fields.
     - For related tabs, use `@UiSurface`, `ResourceSurfaceOpenAdapterService`, `SurfaceOpenMaterializerService`, and `PraxisSurfaceHostComponent` before rendering local tables or mapping arrays manually.
     - Hide Praxis table affordances through public config such as `TableConfig.ai.assistant.enabled=false`, not CSS selectors against internal DOM.
     - Govern table affordances explicitly. For every main or related table, record whether each toolbar control is: a business operation from metadata, a user-owned personalization control, or a governed authoring control. Do not treat them as interchangeable.
     - `toolbar.columnsVisibility` is user personalization, not authoring. Keep it disabled unless the user task has optional columns whose visibility is useful to personalize. When enabled, use a stable table identity and user/company-scoped persistence; do not require an administrator merely to choose visible columns.
     - A settings/editor trigger that can change reusable table, filter, form, or surface configuration is governed authoring. It must be rendered only from a public server-resolved authoring capability and its save endpoint must enforce the same capability. Never derive it in Angular from a username, raw HADES role, or a broad `privileged` flag.
     - Related-resource tables must inherit the host table-affordance policy or receive an explicit equivalent policy. A related surface may not silently fall back to library defaults that re-enable columns, authoring, or other utility controls excluded from its parent experience.
     - The screen package must include a compact affordance matrix: table/surface, control, classification, default visibility, persistence scope, capability (when applicable), and standard-versus-authoring-principal QA result. If Praxis cannot materialize the policy or consume the capability, classify it as `lacuna-real-de-contrato` and create a Praxis Platform Follow-up instead of adding host checks.
     - Build only thin screen composition: route, title/breadcrumb integration, resource config, optional detail panel/tabs, child resource wiring, and action gating.
   - For tabs, use the tab strategy in `references/praxis-screen-composition.md`; do not merge unrelated tab data into the main DTO just to match the legacy layout.
   - Hide or disable write actions until the write API gate is closed.
   - For `Duplicar`, do not wire it as a generic action from the legacy button state. Wait for the backend contract to classify it as `duplicate-draft + POST`, a real `@WorkflowAction`, `Blocked`, or `Not present`, then consume the native Praxis discovery/runtime path for that classification.
   - For option and LOV fields, consume canonical option-source metadata, including by-ids reload for selected values. Do not build screen-specific Angular lookup services when `RESOURCE_ENTITY`, `/option-sources/{sourceKey}/options/filter`, or `/options/by-ids` can express the need.
   - Model persisted/default selection and option availability as separate asynchronous inputs.
     For local options, do not write a non-empty `FormControl` value until the matching canonical
     option is present. For remote/entity sources, allow the Praxis control to rehydrate through
     by-ids; do not replace that path with a host-local options array.
   - Before using any option-bearing control in a shell, route guard, global toolbar, filter, edit
     form, or dependent lookup, test both bootstrap orders: value before options and options before
     value. Also test missing ID, context/dependency change during load, and teardown during load.
     Reconciliation must not emit a user selection event, refresh the route repeatedly, or create
     an effect cycle that writes the same value/metadata back into the component.

6. Verify end to end.
   - Run backend tests affected by DTO/schema/API changes.
   - Run frontend tests/lint/build for `ui-administracao-pessoal`.
   - Start the dev server when the UI needs one.
   - Use browser/Playwright screenshots for desktop and mobile; verify table, filters, loading/empty/error states, row selection, detail rendering, and no text overlap. Empty-state QA must cover initial empty and filtered empty separately, assert the presence/absence of the canonical primary action, and prove there is no horizontal overflow or oversized decorative vacancy.
   - Verify the UI consumed canonical evidence: `/schemas/filtered`, capabilities/actions/surfaces/HATEOAS, option sources, and read/write gates. A screen is not reusable if it works only because host code bypasses those surfaces.
   - Before promoting a screen as a reusable reference, run `tools/migration-factory/check-angular-praxis-reference-pattern.ps1` with `-Strict` against the component and resource config when the checker exists.

## Output Artifacts

For each screen, create or update these files under `docs/migracao/<SCREEN>/`:

- `ui-api-readiness.md`
- `ui-dto-contract-review.md`
- `ui-translation-map.md`
- `ui-implementation-plan.md`
- `ui-visual-qa.md`
- `ui-execution-gate.md`

Use `references/ui-artifact-templates.md` for concise templates.

Historical `phase-6-5-ui-execution-gate.md` files may remain as evidence from older pilots, but new UI packages should close with `ui-execution-gate.md`.

## Hard Gates

- Do not create a duplicate API when an approved reusable resource already covers the functionality.
- Do not create a duplicate Angular runtime for concepts owned by `@praxisui/core`, `@praxisui/crud`, `@praxisui/table`, `@praxisui/dynamic-form`, or `@praxisui/dynamic-fields`.
- Do not expose `empresa`, `usuario`, HADES/package flags, SQL names, ROWID, cookies, tokens, or hidden XML state in public DTOs or `x-ui`.
- Do not use a free text filter for a governed lookup when a usable option endpoint/source exists.
- Do not implement Angular when a visible legacy detail/grid field required for the target slice is absent from the response/detail DTO. Return to the backend read/options phase and fix the DTO, mapper/adapter, schema, and tests.
- Do not implement Angular when `/schemas/filtered` would emit a weaker control than the known legacy/Praxis contract, such as `SEARCH_INPUT` for an approved remote LOV. Return to the backend contract phase.
- Do not implement or accept Angular workarounds for weak semantic DTO metadata. Labels, icons, help, tooltips, domain descriptions, governance, AI policy, display fields, and value presentation must come from DTO/schema or a documented Praxis platform contract.
- Do not accept a screen-local `selectedRecordLabel` mapper as the primary master-detail identity when `x-ui.resource.identity` is available. A textual label may remain only as fallback for older published packages and must have an explicit removal trigger.
- Do not implement a local launcher or hardcoded enablement model for Praxis actions, surfaces, capabilities, or HATEOAS links when the native Praxis runtime can discover and materialize them.
- Do not route action, surface, tab, lookup, or command intent by labels, regexes, XML names, or keyword lists. Resolve the canonical operation/resource/surface/action first; textual matching may only rank candidates after that semantic scope is known.
- Do not implement or promote host-owned `command-drawer`, `FormConfig.sections`, `sections: []`, `::ng-deep`, `ViewEncapsulation.None`, or local table/rendering workarounds as a reference pattern. If a workaround is unavoidable, classify it as `manual-temporary-gap` and register the platform/workflow follow-up before closing the UI gate.
- Do not fix `praxis-ui-angular` or Praxis starter defects inside the Ergon host. Record a `Praxis Platform Follow-up` with owner, expected behavior, observed evidence, impact, temporary workaround, and a suggested prompt for the Praxis specialist.
- Do not mark a DTO/UI handoff as ready while visible fields remain `SEMANTIC_UNCONFIRMED`, unless the gap is explicitly documented as accepted with conservative copy and an owner to investigate legacy docs/source.
- Do not enable create/edit/delete/duplicate in Angular unless command APIs are implemented and gated. For duplicate specifically, `duplicateEnabled=true` in XML is not enough; the contract must prove copied/reset fields, defaults, save route, and whether the correct Praxis shape is `duplicate-draft + POST` or `@WorkflowAction`.
- Do not mark the UI ready without executing schema and visual QA.
