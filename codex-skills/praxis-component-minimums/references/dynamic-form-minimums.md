# Dynamic Form Minimums

## Local Minimum

Use this when the host wants to render a form without backend discovery.

Minimum pieces:

- import `PraxisDynamicForm`
- provide `[config]`
- ensure `config.sections`
- ensure `config.fieldMetadata`

This is the minimum local runtime path.

## Remote Metadata-Driven Minimum

Use this when the host wants the form to discover metadata from the backend.

Important distinctions:

- `resourcePath` and optional `resourceId` can connect the form to backend schemas and entity context
- for backend-published surfaces, prefer `schemaUrl`, `submitUrl`, and `submitMethod`
- in detached dialog/drawer hosts, `apiUrlEntry` may be needed together with `apiEndpointKey`

## Metadata Source

Metadata may come from:

- local `FormConfig.fieldMetadata`
- backend schema discovery
- downstream field presentation/editorial resolution from `@praxisui/dynamic-fields`

## Important Rule

Do not answer "just set resourcePath" for every form question.

For local rendering, `FormConfig` is enough.
For backend-published surfaces, explicit discovery/submit URLs are the preferred canonical path.

## Host Requirements

If the form uses:

- `resourcePath`
- `resourceId`
- schema fetch
- CRUD submit
- custom endpoints

then the host must provide the effective API/CRUD service wiring in scope.

## Useful Canonical Facts

- without a prior `FormConfig`, the runtime can generate a default layout from backend metadata
- with customization enabled, local layout can be reconciled with server metadata
- logical context for rebuild preservation depends on `resourcePath`, `resourceId`, and mode
