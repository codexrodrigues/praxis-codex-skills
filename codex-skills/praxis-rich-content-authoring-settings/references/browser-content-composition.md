# Compose Content Through Its Widget Editor

Start from the installed Rich Content metadata/presets. Use the content editor's
guided structure, preview and permitted advanced JSON as views of one document.
The page and shell editors own outer placement/chrome; Rich Content owns the
internal card/group layout and document/context bindings.

Choose a block by the operator's need: feature header for identity, metric/stat
group for a summary, card/compose for related content, timeline for chronology,
action/link for a declared next step. A preset supplies structure; replace sample
content deliberately. Native semantic blocks usually avoid rebuilding each
icon/value/text fragment manually.

1. Select the block in the document tree and inspect identity/content, then its
   children and presentation controls. Configure nested compose and card slots
   through the current editor rather than assuming nested content is JSON-only.
2. Bind actual state/context paths. A displayed number is not proof of a live
   source; distinguish a literal, derived measure, remote aggregate and fallback.
   Resolve missing/raw placeholder values before resizing the card to fit them.
3. Use registered structured actions and real route/surface payloads. Keep literal
   payload and expression bindings separate. Page configuration Save does not
   authorize executing a business command exposed by an authored button.
4. For a card intended to filter a collection, inspect its actual output/action
   contract first. Rich Content's document/context inputs do not imply a public
   `cardClick` output. Consider List card presentation with declared item/selection
   events or a native scope/KPI capability, then use Page Builder's connection
   editor. Do not add a host event bus or conflate decorative status with filtering.
5. Inspect media support before embedding a registered component. A host-specific
   radar or other media component requires its own registered input contract;
   a generic content editor cannot create an absent component/editor capability.

Use `praxis-ui-product-design` for emphasis, theme inheritance, typography and
internal wrapping. Test long labels, zero/error states, keyboard actions and
narrow composition. Verify the document and unrelated widget inputs survive
Apply/save/reopen. A JSON parser accepting a field does not prove normalization
preserves it or the renderer uses it.
