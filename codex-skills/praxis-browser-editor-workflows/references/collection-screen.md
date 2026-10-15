# Collection Screen Through Editors

## Choose the native composition

Read resource catalogs/schema and original metadata. Check the installed
CRUD/Table filterBar, scopeBar, KPI, stats and authoring support before rebuilding
with generic widgets. Static reference numbers are not real counts. A closed
issue may be implemented in main but absent from the installed release.

When requested, use a single filter workspace: search, fields, scopes, active
conditions, advanced filters and clear. Decide whether KPIs are informational or
intentional shortcuts; interactive ones must explain and reflect the same query.
Avoid independent Status controls or competing query owners. This design advice
does not assert every installed editor can materialize it without an owner fix.

## Generic route proved in rc.17

Prefer a simpler native composition when available. The exercised alternative was
Rich Content header, two Lists (scope/KPIs), Table, page dataSources/derived state,
and native composition links. Child editor envelopes were:

```json
{"kind":"praxis.list.editor","version":1,"config":{}}
```

```json
{"kind":"praxis.table.editor","version":1,"config":{},"bindings":{"resourcePath":"<catalog resourcePath>","horizontalScroll":"auto"}}
```

These illustrate envelopes, not complete defaults. Rich Content uses its own
RichContentDocument. Apply JSON in the owner editor and save its result.

For a page-owned exercise, choose **Origem da configuração** before saving each
List/Table: rc.17 labels are **Configuração da página** (List) and **Definida nesta
página** (Table). Verify `configPersistenceStrategy: "input-first"` in the saved
widget inputs. The new-widget default `local-first` can let individual preferences
override/merge the page configuration; a valid child JSON does not set this input.
This choice is for page-owned composition, not a universal ban on user preferences.

Scope items carried queries such as `{"filters":{"ativo":true}}` in
`item.queryContext`. The graph used `itemClick -> pick-path(item.queryContext)
-> state.values.selectedScopeQuery -> Table.queryContext`. State schema:
`type: PraxisDataQueryContext`, `mergeStrategy: replace`, `initial: null`.
In that version empty-object path flattening could hide the parent port; null
plus typed schema exposed it. This is historical evidence, never a universal
initialization requirement. If reproduced in the current release, classify and
track the Core/connection-editor materialization issue with a removal trigger for
the workaround; do not add a second state contract by reflex.

After selecting **Extrair um campo**, enter `item.queryContext`, leave the field,
and verify the delivered-value summary before **Aplicar conexão**. Confirm the
saved `transform.steps[].config.path` in the visible Praxis JSON immediately.
In one rc.17 browser take, locator fill/typing showed the intended text while the
pipeline retained `payload`; focusing the field, selecting all, using native
keyboard text input and Tab committed the intended path. Treat this as observed
automation/editor interaction, not a proved library defect or universal API rule.
Do not repeat the same failing fill across links. If the graph already received
an item envelope, reset the query through its page-state editor, then retest.

Derived List configs synchronized active styling. Literal per-item slot rules
avoided ambiguous nested template evaluation in a templated config. This was an
advanced alternative, not a requirement for giant derived configs or CSS; prefer
current native data/context bindings and guided controls when they suffice.

Core already handled Table queryContextClear for this state-to-query link: full
clear reset the originating scope without a return connection. Test partial
clear, remaining field filters, search and pagination reset separately; full
clear is not proof of those cases. Do not introduce a cycle by reflex.

## Data and action checks

- Use declared statistics resources/capabilities. Distinguish global totals from
  filtered results, counts from averages and illustrative scores from real values.
  Weight grouped averages according to the intended measure; do not average
  averages blindly or fill missing API values with reference literals.
- Preserve metadata/capability authority. The exercised employee catalog declared
  surface detail; its inline action was
  `{"id":"detail","action":"detail","label":"Visualizar","icon":"visibility"}`
  with discovery enabled. Resolve the actual catalog ID for each resource rather
  than copying this example as a default. Wait for contextual actions to load.
- Keep denied Create/Edit and do not submit domain writes in a read-only exercise.
  Opening a read surface does not authorize mutation.
- Test scopes, any KPI shortcut, native clear, pagination and an allowed detail.
  Verify counts and synchronized state, not merely a successful request.

## Visual checks

Use theme tokens and component-owned presentation before CSS. Evaluate cell
padding together with widths to avoid cropping avatars/badges. The exercised
Table accepted appearance.spacing.cellPadding, column width and column style
`white-space: normal; overflow-wrap: anywhere;`. Inspect saved JSON and renderer
result in the installed release.

Use natural height, distinguish occupied rows from pixels, and arrange after
dimensions are final. Stack mobile from the final reading order. Device canvas
overrides do not necessarily set a child's internal responsive direction.

Check long labels, loading/error/empty states, keyboard/focus, contrast and narrow
panels. Mobile must not overflow globally; a wide table can scroll internally.
Check the entire filter area, not only the first card.

For this full-width vertical rc.17 reconstruction, finish dimensions before the
final organization: one occupied row per natural block, full width, then
**Coluna de trabalho → Usar organização no rascunho** and mobile **Empilhar widgets**
when available in the installed editor. Preserve other intended compositions.
Verify saved device geometry, not just desktop spans.
For a frameless shell that still needs body padding, retain framed presentation,
choose **Sem moldura**, and set **Mostrar cabeçalho: Nunca**; **Somente conteúdo**
sets `kind:none` and can bypass shell spacing. Do not clear required pixel-height
fields to request automatic size; use the actual natural-size/device controls.
