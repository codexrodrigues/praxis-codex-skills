# Author A Form In A Composed Page

Inspect `praxis-dynamic-form.metadata.ts`, the widget wrapper and the installed
schema/mode contract. Consider a native resource operation/surface before
manually assembling its equivalent in a lower-level form widget.

1. Establish intent: query, read/view, create or edit. Resolve the operation's
   schema, required fields, record identity, capabilities and action/surface
   context. A response schema or filter DTO is not a create/update request.
2. Open the registered content editor. Inspect actual connection/schema controls,
   fields and modes; do not assume a resource selector or submit wiring exists
   merely because the standalone form supports it. Preserve unrelated inputs.
3. Organize fields through supported section/row/column controls, configure
   presentation and schema-backed options, and keep business constraints in
   canonical metadata. Use the fields/option-source skills for dependent selects,
   search, selected values and reset behavior.
4. For selected-record forms, use the declared identity/data input and an exact
   source port. Clear stale selection and reject late data from an earlier record.
   Keep contextual related-record constraints governed; do not expose raw parent
   IDs as ordinary editable choices to compensate for missing context.
5. Check required/invalid state, keyboard order, cancellation and narrow layout.
   Apply/save the form's configuration only within page-authoring scope. That
   operation does not create/update the business record.
6. Execute domain Submit only when the user authorized that business operation
   and the target session/capabilities allow it. Otherwise prove read/view and
   cancel, and retain the unverified write boundary. An enabled editor button
   does not grant mutation authority.

For `praxis-filter-form` inspect its own metadata/widget editor: `valueChange`
and `submit` publish `{ formData }` in the inspected contract. This differs from
the DTO emitted by `praxis-filter`; use `praxis-table-filter-actions` and its
browser-filter reference to project the envelope into the selected query consumer.

Use `praxis-ui-product-design` with the layout skill for task grouping and content
hierarchy. Verify the form document, schema preferences and mode survive Apply,
acknowledged page save and reopen; keep business-write receipt evidence separate.
