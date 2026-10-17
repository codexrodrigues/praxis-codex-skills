# Configure A Table Widget In A Page

Inspect the selected preset and `PraxisTableWidgetConfigEditor`; opening a table's
standalone settings is not proof of the same hosted entrypoint or context.

1. Establish configuration origin. For a page-authored table, choose the page
   strategy when offered (`inputs.configPersistenceStrategy = 'input-first'`).
   Individual preferences can override page values under `local-first`. Temporary
   component preferences do not prevent the parent page saving its own config.
   Do not erase unrelated preferences to make a demonstration appear correct.
2. In Connection, inspect resource and stable identity. Use Resource Quick Connect
   only where actually exposed; some widget editors offer a text resource field.
   Supply its canonical base resource from discovery, not a guessed label, `/api`
   prefix, `/filter` operation URL or schema path. Keep local-data precedence
   explicit with `praxis-table-data-source-precedence`.
3. Wait for applicable schema/fields, then select columns, labels, formats, order
   and supported renderers. Configure toolbar, pagination and detail only as the
   task requires. Compare authored page size with the settled rendered rows;
   initial success followed by async reversion is a different failure.
4. Select the query owner before adding external filters. For a declared external
   owner, use its supported `filterCriteria`/`queryContext` port and the actual
   payload transform. Check existing structural filters and the clear behavior.
   Use the filter-actions reference instead of implementing a second query store.
5. For selection/detail use declared row identity and ports. A row action or
   exposed record surface does not override a denied Create/Edit operation.
   Use normal read/view/cancel paths for read-only investigation.

Apply and observe toolbar, columns, row count, query behavior and loading/error
states before fresh reopen. Save page acknowledgement and component preference
acknowledgement are different scopes. A successful reload does not prove live
Apply worked; record both stages when they differ. Check horizontal containment,
narrow editor access and visible selection/detail continuity.
