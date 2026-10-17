# Connect Existing Widgets Through The Editor

Use the installed palette/registry, current widget keys and port contracts as the
connection inventory. Read Core composition semantics and the source/target
component skills. Observing a property in JSON or an Angular output does not
prove that the current graph exposes a compatible public port.

## Establish The Delivery Before Drawing A Link

For each interaction record source key/port, actual event envelope, target
key/port or writable state path, required projection, clear value and expected
effect. Choose the smallest compatible declared delivery:

- Filter to collection: inspect whether the source emits the DTO directly or
  wraps it (for example `{ formData }`). Match the consumer's `filterCriteria`
  or `queryContext` shape; field existence alone does not establish equivalence.
- Selection to detail: project the declared stable identity, including composite
  identity when required. Empty selection must clear the previous detail/context.
  Exercise A -> B -> empty and a fresh object/context for the same identity when
  the detail contract supports updates; identity equality alone may not refresh it.
  Keep runtime selection transient rather than saving the selected record.
- Chart to query consumer: use the event authorized for the requested behavior.
  Observational point clicks and structured point actions are distinct. Some
  chart target catalogs require an existing compatible link before offering the
  target; inspect that evidence rather than filling an arbitrary target name.
- State to indicator/content: bind the supported input/context to a declared
  state/measure path. A noninteractive editorial card needs no outgoing link.
- Action to surface/navigation: use the structured action and the target's
  declared payload contract; a button label is not an executable action ID.

For a card that should filter, establish an actual emitter: for example a List
rendered as cards with declared selection/item events, a supported native KPI,
or a Rich Content action whose registered action can perform the intended task.
Do not invent `cardClick` on an editorial component or create host event listeners.

## Operate And Verify

1. Open the connection editor, inspect the current links/dock and select source
   and destination ports. Read their descriptions and compatibility diagnostics.
2. Configure only supported condition/transform/policy controls. Inspect the
   saved link after committing each edit; entered path text alone is not proof
   the control accepted it. Advanced JSON is usable only in a documented editable
   surface and when the user allows it; an export/inspector is not an importer.
3. Exercise the source's normal UI, then observe target behavior and available
   trace/diagnostics. A line on the canvas is structural evidence, not execution.
4. Exercise clear/empty selection, repeat the action and verify unrelated scope
   survives. Do not add a reverse feedback link merely to make two controls look
   synchronized. Intentional cycles require Core's supported explicit guards.
5. Follow the page's actual autosave policy; save acknowledgement and reopen are
   separate proof. Recheck target identity and payload after reopening.

## Cross-Component Acceptance

A successful query link preserves the resource's structural/security scope,
updates matching results and resets pagination as the consumer specifies. A
successful detail link changes records and handles no selection. A successful
state link resolves values without rewriting child configuration. An authorized
action reaches its declared target; it does not establish permission to submit
a business mutation. Record partial/blocked outcomes at the owner boundary.
