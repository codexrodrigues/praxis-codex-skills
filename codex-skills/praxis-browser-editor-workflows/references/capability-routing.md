# Route By Capability, Then Compose

Use this matrix for any authored page. Resolve the operator's task and data scope
before choosing components; the word dashboard, registration or cockpit does not
select a fixed architecture. Inspect native resource pages and declared surfaces
before assembling a lower-level equivalent. A card is a presentation choice,
not evidence of a query, event, permission or record mutation.

## Select The Owners

| Required capability | Functional guidance | Evidence to inspect |
| --- | --- | --- |
| Page, canvas, widget shell, hosted editor | `praxis-page-builder-authoring` | Registered insertion preset, child config editor, page identity and persistence |
| Events, state, selection/detail, filters between widgets | `praxis-page-builder-composition`, `praxis-core-composition-runtime` | Exact ports, payload shape, transform and diagnostics |
| Palette and editor availability | `praxis-core-component-registry-contracts` | Installed registry ID, preset inputs, ports and editor context |
| Statistical chart and eligible fields | `praxis-charts-authoring-settings`, `praxis-charts-authoring-catalogs` | Resource catalog, capabilities, dimensions/metrics, effective source |
| Editable or read-only schema form | `praxis-form-authoring-settings`, `praxis-form-schema-runtime-modes` | Operation-specific schema, mode, record context and submit boundary |
| Collection columns, paging and detail | `praxis-table-authoring-settings` or `praxis-list-authoring-settings` | Resource, data precedence, configuration origin and row/item contract |
| Integrated or external query controls | `praxis-table-filter-actions`, plus the chosen filter/form owner | Filter DTO versus form envelope, query owner, apply/clear behavior |
| Editorial cards, metrics, progress, timeline or navigation | `praxis-rich-content-authoring-settings` | Document/context, bindings, supported structured actions |
| Visual hierarchy and composition across all widget types | `praxis-ui-product-design` | User journey, emphasis, density, theme inheritance, narrow editor/runtime |
| Apply, save, preferences and reopen | `praxis-settings-roundtrip-authoring` | Parent propagation, autosave and acknowledged persistence |

Use the installed registry and current visible editors to choose a path. Frontmatter
routes the task to guidance; a label search only finds candidates in that scope.
An available TypeScript input need not be a public composition port. An editor
on the standalone component need not exist in its Page Builder wrapper.

## Maintain A Small Capability Ledger

For each selected widget record: stable key and component ID; preset; editor
entrypoint; resource/schema/operation; data origin; input/output ports and payload;
configuration origin; shell/layout ownership; expected interaction; proof status.
Record page sources and derived state once rather than once per consumer.

Use explicit statuses:

- **Installed source inspected:** the package exposes the contract; behavior has
  not yet been exercised through this host's UI.
- **UI inspected:** the control/catalog/port was observed; changing it and saving
  have not yet been proved.
- **Exercised:** the declared interaction worked, with data origin and permission
  scope recorded.
- **Round-trip proved:** the applied value and behavior survived acknowledged
  save and fresh reopen/reload.
- **Blocked/partial:** retain the diagnostic, owner and exact unfinished proof.

Record the installed version, source revision and historical recipe separately.
For rehearsal readiness, audit the chosen skills and their transitive manifest
dependencies, not only the entrypoints synchronized most recently. Reconcile
installation differences through `praxis-skill-authoring-governance`; installing
guidance does not upgrade the host's component packages.
A prior version's successful rehearsal is neither a current regression nor a
current acceptance. Do not generalize a host HTTP failure into missing platform
support or repair an unavailable selector by guessing URLs.

## Check That Guidance Stays Composable

Use these scenarios to review routing; they are not claims of executed acceptance:

| Scenario | Required path | Failure that must stay visible |
| --- | --- | --- |
| Analytical view | Governed chart, eligible metric, query consumer, clear | Synthetic preview presented as live data, unsupported target or stale selection |
| Customized registration | Operation schema, form layout, validation, cancel, permitted submit | Saving page layout confused with creating/updating the business record |
| Search and selection/detail | Single query owner, collection, selected identity, detail | Empty selection retaining a previous record or clear destroying structural scope |

Compose only the capabilities needed by the task. For related-record forms reuse
[entity-360.md](entity-360.md); for native collection choices reuse
[collection-screen.md](collection-screen.md). A read-only run can prove inspection
and cancellation, not successful writes. Timed runs use [rehearsal.md](rehearsal.md)
and retain all agreed functional and visual checks.
