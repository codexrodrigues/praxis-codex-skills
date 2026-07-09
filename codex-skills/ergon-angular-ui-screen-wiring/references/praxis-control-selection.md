# Praxis Control Selection For Ergon Screens

Use this matrix when translating legacy XML fields into Praxis DTO and FilterDTO metadata.

## Filter Controls

| Legacy pattern | Public DTO field? | Praxis control | Notes |
|---|---:|---|---|
| Company/current enterprise selected globally | No | None | Resolve from backend session/app context. Do not repeat in each screen filter. |
| User/session/role/package flag/hidden item | No | None | Server-side only. Never publish in `x-ui`. |
| Short free search over code/name/mnemonic | Yes | `SEARCH_INPUT` | Praxis table maps this to `inlineInput`. Use one search field instead of several duplicated legacy text boxes. |
| Exact numeric code | Yes, when needed | `NUMERIC_TEXT_BOX` | Praxis table maps this to `inlineNumber`. Prefer secondary/advanced placement if a global search already covers it. |
| Small fixed local enum | Yes | `SELECT` | Provide enum/options in schema. |
| Medium local list | Yes | `SEARCHABLE_SELECT` | Use when all options are cheap and local. |
| Remote LOV/options/filter | Yes | `ASYNC_SELECT` | Provide endpoint/resourcePath, value/display/filter/sort metadata, and by-ids support where selected values must be rehydrated. |
| Governed business entity | Yes | `ENTITY_LOOKUP` | Use for identity, status, authorization policy, dependency filters, detail display, or multi-screen reuse. |
| Boolean flag | Yes | `TOGGLE` | For filters use inline toggle. Keep tri-state semantics explicit if null means all. |
| Date | Yes | `DATE_PICKER` | Prefer date range for from/to pairs. |
| Date interval | Yes | date range metadata | Preserve inclusive/exclusive semantics in service tests. |
| Dependent LOV | Yes | `ASYNC_SELECT` or `ENTITY_LOOKUP` | Add `dependsOn` and `dependencyFilterMap`; validate disabled/loading behavior in UI. |

## Response DTO Controls

| Field type | Praxis control/display | Notes |
|---|---|---|
| Public id | Hidden or low priority | Required for row identity but usually not a business column. |
| Code | Numeric/text display | Keep sortable if the legacy grid sorts by it. |
| Description/name | Text display | Usually primary row label. |
| Mnemonic/abbreviation | Text display | Keep separate when the legacy screen has distinct fields. |
| Company scope label | Read-only display | Do not make it a public filter unless multi-company search is approved. |
| Boolean detail fields | Toggle/read-only checkbox | Required for detail parity if visible in the legacy form. |
| LOV description | Prefer description + raw code if useful | Keep raw id/code in DTO when needed for selection, display label for users. |

## Metadata Requirements

For remote selects and entity lookups, the schema must include enough `x-ui` metadata for Angular to work without hard-coded adapters:

- `controlType`
- `resourcePath` or `endpoint`
- `valueField`
- `displayField`
- `filterField`
- `sortField` and `sortOrder` when stable ordering matters
- `optionsPageSize`
- `/options/filter` support
- `/options/by-ids` support when the component must rehydrate selected values
- `optionSource` with `key`, `type`, dependencies, capabilities, and policy when using governed option sources

## Ergon-Specific Rules

- Treat XML binds as candidates, not public DTO fields, until classified.
- Collapse repeated legacy filters when Praxis can express the user intent with one search field.
- Preserve business semantics in service/adapter tests, not only labels.
- Prefer PT-BR labels with accents in `@UISchema`; keep Java field names ASCII.
- If a legacy field is visible only because of layout or old framework mechanics, mark it `layout-only`.

