# Connection Editor: Semantics, Geometry, And Inspection

Use for the radial connection diagram, port catalogue, inspector, structural
route, minimap, compact relationship list, and their interaction lifecycle.
The owner is `projects/praxis-page-builder`; persisted semantics remain
`WidgetPageDefinition.composition.links`, shared endpoints, and page state.
The diagram is a derived projection, not a second graph document.

## Inspect The Existing Sources

Under `projects/praxis-page-builder/src/lib/editor/connection-editor/`, inspect
`connection-editor.component.ts` and the relevant `connection-editor-*.util.ts`
and specs: graph, layout, geometry, port-order, wire, trace, caption, and routing.
Inspect `connection-editor-state-name.component.ts` for state naming, the package
README, public API, i18n catalogs, and authoring manifest for derived impact.
Use the official host's current scripts and route; `/dynamic-page-lab` on 4003
is an operational example, not the owner of diagram behavior.

## Materialize Meaning Before Adding Contracts

- Resolve component input/output labels and descriptions from
  `ComponentMetadataRegistry.resolveEditorial()` and the owning package's
  `ComponentMetadataEditorialDescriptor`; fall back to the existing port
  contract and identifier. Inspect provider registration before declaring a
  missing label a public-contract gap.
- Page-state names consume `state.schema[path].description` for values and
  `state.derived[path].description` for derived state. Respect the layer;
  identical paths in different layers are not interchangeable. Transient
  state does not borrow a persisted description.
- Naming information edits that existing description through page history.
  Preserve values, endpoints, paths and derived definitions; test Cancel,
  Undo/Redo and reopening. Applying a name locally is not saving the page.
  Do not silently migrate an older saved page or invent business aliases.
- Show one readable causal summary with source, information, and destination.
  Keep ids, intent codes and transform internals in technical disclosure.
  Reuse the same resolved copy in catalogue, draft selectors, list, tooltip,
  inspector, and structural route. A readable label never changes identity.

## Structural Route Is Not Execution

`connection-editor-trace.util.ts` explains configured connections. It does not
execute conditions, emit events, prove delivery, or certify runtime ordering.
Seed a route from the exact endpoint of the selected connection: widget, port,
direction and nested path; state path and layer; or global action id. Selecting
a node explicitly is an aggregate view and must not replace that exact scope.

Compare propagation with Core's composition runtime. State fan-out requires
matching path/layer. Do not infer output events from receiving a component
input; stop expansion through blocking diagnostics and guard against cycles.
Group explanatory micro-steps by canonical connection for the main journey.
Inspecting another link or closing details preserves route origin and progress;
ending the route is an explicit action. Test two outputs on one component,
nested children, distinct state layers, fan-out, cycles and blocked links.

## Geometry Invariants

1. Keep node identity accents stable across layout/selection and retain icons
   and names. Link color expresses a different dimension; explain categories
   with text and terminal/line geometry. Do not rely on color alone or imply
   active data delivery through decorative perpetual animation.
2. Allocate visual perimeter anchors per connection incidence, including
   crowded state hubs. Several visual anchors may represent the same canonical
   port; do not clone ports, state paths or saved links to obtain spacing.
3. Place captions before routing. The four-side caption map must govern DOM
   placement, angular port reservations, path obstacles and fit bounds. A CSS
   translation of the label alone leaves obsolete detours in the router.
4. Keep world-space caption reservations and routes stable while zooming.
   Cap the visible text by shrinking inside its reservation toward the radial;
   preserve full accessible names. Fit/reset must not depend on prior zoom.
   The current implementation caps visible text at 16 screen pixels; inspect
   the source before changing this internal policy or its geometry tests.
5. Route around bodies and captions using the existing visibility graph and
   reuse derived routes in consumers. Automatic arrangement should coordinate
   node positions, ports and captions; manual rotation is not the user's
   prerequisite for understanding a connection.
6. Separate the clipped map from toolbar, legend and navigation controls.
   The map's movement belongs to pan/zoom: `overflow: hidden` still permits
   native programmatic scrolling, including focus/scrollIntoView side effects.
   Use non-scrolling clipping for that surface and keep native scrolling on
   its catalogue/compact-list children. Prove both axes stay at zero with
   overflowing geometry; a stable transform alone misses this second viewport.
   Tooltip/catalogue live outside the transformed zoom layer. Test paint order
   and hit testing, not z-index numbers alone; informational hover must not
   intercept the connection beneath it or compete with pinned details/drafts.
7. Project minimap pointer coordinates through the actual SVG aspect-preserving
   transform, including letterboxing. Fit and incremental zoom share limits;
   disabled limit controls retain meaningful state and keyboard continuity.
8. When the available stage is too small, use the relationship list with the
   same catalogue/inspector and route controls. Inspect current stage-width
   and stage-height thresholds; do not infer responsiveness from window width
   alone. Keep the measurement source stable to avoid mode oscillation.

Obstacle avoidance is not global crossing minimization. Manually overlapping
nodes can prevent a clear path; a conservative reservation can exceed visible
caption size at high zoom. Do not promise optimal or crossing-free layouts.
Before replacing the router, compare identical canonical topologies, port
constraints, labels and renderer states. Include state fan-out, cycles and a
dense bipartite graph; report crossings, collisions, length, area, determinism,
layout time and interaction cost separately. An isolated ELK benchmark of an
earlier geometry is neither proof of the current renderer nor evidence of
better human comprehension. Do not introduce a dependency from that result alone.

## Inspection Journey And Proof

Inspection must not start a draft or emit `pageChange`. Creating/editing a
connection is explicit. Catalogue and inspector are exclusive; opening the
inspector from a catalogue must remember the initiating node, port, connection
and internal scroll context using stable ids, even for an incoming connection.
Closing restores that context, not automatically the wire's source radial.
Escape dismisses one layer; hover cleanup must not reset an active route.

Exercise all entry points: wire, bottom list, Locate, compact relationship,
catalogue and toolbar. Include pointerdown before click as well as Enter/Space:
outside-pointer dismissal can erase context before the click captures it.
After rendering, focus a visible task control. A removed, inert or clipped
radial is not a valid restoration target; use a visible editor fallback.
Keep draft cancellation ownership intact.

Use the owning focal specs plus Page Builder build. In the browser, include
light/dark catalogue contrast, a long catalogue, desktop, narrow stage, high
zoom, and destination-catalogue → incoming-link → inspector → Escape → catalogue
→ Escape → initiating control. Verify focused DOM identity and visible bounds,
paint/hit testing, map transform, native map scrolling and catalogue scrolling
separately. A stable signal/transform alone does not prove no visual jump.
Record interrupted reloads as incomplete evidence; never turn static route
preview or simulated interaction into a claim of runtime execution or a user study.

For view-only changes, prove no persisted mutation and inspect manifest/API
impact before deciding generation is unnecessary. For naming, link edits or
public authoring changes, add the corresponding history, round-trip, consumer
and agentic gates from the owner skills and AGENTS; do not waive them based on
the appearance of the change.
