# Runtime Components Reference

Use this file when adding Praxis UI pages/routes/components to an Angular host.

## First Adoption Path

Prove one backend resource across the core runtimes before expanding:

1. `@praxisui/table`
2. `@praxisui/dynamic-form`
3. `@praxisui/crud`
4. `@praxisui/list`

Against the public quickstart API, use:

```ts
export const RESOURCE_PATH = 'human-resources/funcionarios';
```

`resourcePath` is the base resource. Do not pass `/api`, `/filter`, `/options`, `/schemas/filtered`, `/{id}`, query strings, or operation URLs as `resourcePath`. Praxis runtime services derive schema, filter, options, item, submit, capabilities, actions, and surfaces from the base resource plus metadata.

Keep this derivation semantic and canonical. If a component needs a field, filter, action, surface, option source, capability, or relationship that is not available from the runtime, first audit whether it already exists in `/schemas/filtered`, catalog/domain discovery, capabilities, actions, surfaces, HATEOAS links, option-source descriptors, or remote config. Only introduce a host-local bridge when the gap is explicitly temporary and cannot yet be solved in the canonical owner.

Use `queryContext` for host-provided filters, pagination, sort, contextual fan-out, and related-resource constraints. Avoid inventing local filter/search DTOs or using legacy bridge inputs for new hosts unless the existing host requires compatibility.

## Table

Remote minimum after host bootstrap:

```html
<praxis-table
  tableId="employees-table"
  [resourcePath]="resourcePath">
</praxis-table>
```

Use a local `TableConfig` only for host presentation decisions such as selected columns, renderers, density, action placement, or local visual preferences. Let the backend publish schema, filters, surfaces, capabilities, option sources, and export/action availability.

When a host supplies `TableConfig` only to stabilize a migration screen, use the public config surface for table chrome. For example, disable the table assistant affordance with `ai.assistant.enabled=false` unless the screen has an approved assistant use case; do not hide it with selectors against internal table DOM.

For advanced filters, do not hardcode a parallel search form when the backend publishes filter metadata. Use Praxis table/filter runtime.

Gate optional operations such as export through capabilities/HATEOAS links; do not infer support from route shape alone.

For contextual screens, pass `queryContext` rather than mutating `resourcePath` or building a local fetcher.

When supplying a local `TableConfig`, start with a typed minimal config such as `const config: TableConfig = { columns: [] }` and add only properties accepted by the published type. Do not invent booleans such as `pagination`, `sorting`, or `filtering`; those are runtime/backend concerns unless the component type exposes them.

In current published trains, `configPersistenceStrategy="volatile"` is valid for table when customization is disabled or intentionally transient.

## Dynamic Form

Remote metadata-driven minimum:

```html
<praxis-dynamic-form
  [formId]="'employees-form'"
  [resourcePath]="resourcePath"
  [resourceId]="selectedId"
  [mode]="'view'">
</praxis-dynamic-form>
```

For create flows, omit `resourceId` and use `mode="create"`.

Use operation-specific `schemaUrl`, `submitUrl`, and `submitMethod` when the backend publishes a specific action/surface contract and `resourcePath` is not the precise operation.

Host-only/transient fields belong in local `FormConfig.fieldMetadata` with source/transient/submit policy semantics, not as fake backend DTO fields.

A local `FormConfig` may be used as a temporary layout bridge while backend metadata or generated layout quality catches up. Do not promote it as the canonical migration pattern when the layout semantics belong in `x-ui`, generated presets, or the shared runtime. Record the removal trigger when the bridge compensates for a platform/runtime gap.

## CRUD

CRUD composes table/form behavior and needs `GenericCrudService` plus dynamic-form metadata providers.

Use CRUD metadata for the host's orchestration choices; do not duplicate backend metadata in the CRUD config. The same resource should still resolve through the canonical backend surfaces.

```html
<praxis-crud
  [crudId]="'employees-crud'"
  [metadata]="crudMetadata">
</praxis-crud>
```

Minimum remote metadata shape:

```ts
const crudMetadata = {
  component: 'praxis-crud',
  resource: {
    path: 'human-resources/funcionarios',
    idField: 'id',
  },
  table: { columns: [] },
  queryContext: {
    filters: {},
    sort: ['nomeCompleto,asc'],
    page: { index: 0, size: 10 },
  },
  defaults: {
    openMode: 'modal',
  },
};
```

Use the component's documented metadata type when editing real code; the shape above exists to preserve the semantic anchors. Do not model CRUD operation names as `actions[].type = 'create' | 'view' | 'edit'` unless the published type for that train explicitly supports it. In current action contracts, `type` can describe presentation kind such as button/icon/menu rather than the business operation. Do not recreate CRUD by manually composing a table and a dynamic form unless the requested UX is truly outside `@praxisui/crud`.

## List

Use list to prove the same collection can be rendered with a different reading surface.

```html
<praxis-list
  [listId]="'employees-list'"
  [config]="listConfig"
  [queryContext]="queryContext">
</praxis-list>
```

Minimum remote data source shape:

```ts
const listConfig = {
  dataSource: {
    type: 'resource',
    resourcePath: 'human-resources/funcionarios',
    sort: ['nomeCompleto,asc'],
  },
};

const queryContext = {
  filters: {},
  sort: ['nomeCompleto,asc'],
  page: { index: 0, size: 10 },
};
```

When a list config includes a data source, keep the resource path relative and point it at the same backend resource. Pass contextual filters/pagination/sort through the component's `queryContext` input when the published `PraxisListConfig.dataSource` type does not expose `queryContext`. Use local templating/skinning for presentation, not for semantic resource behavior. Do not fetch data with host `HttpClient` just to pass local data unless the screen is explicitly local-only.

In current published trains, list persistence strategies may be limited to `input-first` and `local-first`; do not assume table's `volatile` strategy is accepted by list.

## Related Surfaces And Row Actions

For row actions that open backend surfaces:

- Backend owns operation, schema, availability, and surface identity.
- Host selects presentation widget, route/drawer/modal behavior, title/icon, and contextual payload handling.
- Prefer public Praxis services and tokens instead of ad hoc row-action HTTP calls: `ResourceDiscoveryService`, `ResourceSurfaceOpenAdapterService`, `SurfaceOpenMaterializerService`, `PraxisSurfaceHostComponent`, and `GLOBAL_SURFACE_SERVICE`.
- Do not parse `_links`, materialize widgets, or build schema payloads by hand when the public surface services cover the flow.
- For materialized surfaces, check `PraxisSurfaceHostComponent` outputs such as `rowClick`, `selectionChange`, and `widgetEvent` before adding host event bridges.
- For related resources, prefer published `surface.relatedResource` plus `RelatedResourceSurfaceResolverService` or `PraxisRelatedResourceOutletComponent`. Do not duplicate the parent-child relationship in local filters unless the product intentionally overrides the canonical query context.

## Expansion Path

Add after the core path works:

- `@praxisui/manual-form`: hand-authored layout using Praxis fields.
- `@praxisui/tabs`: grouped composition and lazy views.
- `@praxisui/stepper`: multi-step flows.
- `@praxisui/expansion`: grouped panels and rich reading surfaces.
- `@praxisui/charts`: analytics surfaces and embedded visualizations.
- `@praxisui/editorial-forms`: guided narrative/editorial blocks.
- `@praxisui/settings-panel` and `@praxisui/metadata-editor`: authoring and configuration.
- `@praxisui/page-builder` and `@praxisui/ai`: governed composition and assistant workflows.

Load companion skills for dynamic-fields/editorial/authoring tasks before changing config editors, control catalogs, or Settings Panel behavior.

## Host-Owned Styling

The host owns theme, shell, navigation, branding, and layout. Praxis UI should remain host-themeable through Material/Praxis tokens and CSS custom properties.

For visual/product quality work, use `praxis-ui-product-design` and validate desktop plus narrow viewport when feasible.
