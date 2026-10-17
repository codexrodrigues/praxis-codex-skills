# Choose The Query Controls And Their Delivery

Resolve the query owner and filter DTO from the resource schema. Inspect the
installed source metadata and target ports before creating a connection. Multiple
controls can contribute to one effective query when the canonical composition
defines their ownership/merge/clear semantics; do not keep competing independent
filter stores simply because both toolbars are visible.

| Option | Inspected source contract | Composition decision |
| --- | --- | --- |
| Table's integrated filters | Consumer's native schema/filter pipeline | Prefer when the query belongs to that collection; an external filter is not required |
| `praxis-filter` | `change`/`requestSearch` deliver the filter DTO; `contextChange` carries presentation context; `clear` is a separate event | Choose instant change or explicit search deliberately; map only the query payload to the consumer |
| `praxis-filter-form` | `valueChange`/`submit` carry `{ formData }` | Project `formData` before delivering a DTO or wrapping it in query context |
| Selectable cards | Actual List/KPI/registered action contract | Resolve the semantic field/value and emitted envelope; an editorial card does not acquire a click output |
| Chart | Event-specific structured filter/action contract | Respect eligible fields and target grounding; a raw point event is not already a DTO |

These rows document inspected contracts, not universal aliases. Recheck current
`praxis-filter.metadata.ts`, `filter-form/praxis-filter-form.metadata.ts`, consumer
metadata and bridge behavior when the installed version differs.

## Browser Procedure

1. Configure the chosen filter's resource/schema and fields through its registered
   editor. Select native controls/option sources by the field metadata. A literal
   path field is not proof of discovery, and a local field list is not live schema.
2. In the connection editor inspect exact source/target keys, ports and payload.
   Choose the consumer's supported `filterCriteria` or `queryContext` semantics.
   DTO to query context can need a `{ filters: ... }` projection; verify this
   against the actual contract rather than inferring from labels.
3. Configure clear separately where required. A void clear event cannot be
   delivered as a meaningful DTO without an explicit supported projection/action.
   Preserve structural/parent/security constraints, false and zero values.
4. If the table exposes `filtering.filterOwner`, use the documented configuration
   for integrated versus external ownership. Its visibility setting alone does
   not prove that the external link works or that two-way synchronization exists.
5. Exercise a value, another field/value, partial clear, full clear and pagination.
   Compare visible fields/chips/selection with results and, when available in the
   approved lane, query evidence. Detect stale scope or double requests before
   adding more controls. Do not add feedback cycles by default.

Cards can present query controls, show context or summarize a measure. Use the
Rich Content, List or native scope owner appropriate to that capability and
`praxis-ui-product-design` for clear selected/disabled/empty states. Styling an
indicator as a button does not establish an event or an authorized action.
