# Entity 360 From a Blank Page

Use for an employee, customer or other entity dossier composed through visible
Praxis editors. Adapt labels and sections to the discovered domain. This is a
workflow reference, not a ready-made Hero HQ page or a promise that every host
already registers the required components.

## Discover before choosing the composition

Build a compact inventory from actual catalogs, `/schemas/filtered`, surfaces,
actions, capabilities, option sources and record links. Record the installed
package cohort, registered palette/providers, backend baseline and persistence
owner. Backend metadata belongs to Metadata Starter; config persistence to Config
Starter; Angular libraries own their runtime; a quickstart is operational proof.

For each candidate section record:

| Item | Questions to resolve |
| --- | --- |
| Identity and selection | What is the canonical resource/id? What record/context does selection emit? |
| Filters and summaries | Which query owner, inline controls, option sources and statistics are published? |
| Relationship | Which surface/child resource, parent field and cardinality are declared? |
| Operations | Which list/detail/create/update/partial/command/export operations actually exist? |
| Permission and state | What principal, scope, availability, precondition and workflow state are required? |
| Presentation | What labels, formatting, privacy policy, value domains and empty/error states exist? |

Do not infer write operations from a readable view, authorization from a visible
surface, parent locking from a query filter, or a safe numeric scale from example
values. Check read data against create/update schemas and domain constraints.
An inconsistent enum/range is an owner issue, not a reason to convert data or
relax validators in the consumer.

Use the smallest native ResourcePage/CRUD/Table composition that meets the job.
Inspect Tabs and related-resource outlet registration before composing generic
launchers. Rich Content tabs organize rich blocks; they do not by themselves prove
support for nested live widgets. Missing registration is host adoption, not proof
that a new library contract is needed. Load component owner skills only as needed.

## Design the journey before filling the canvas

Define a desktop and narrow-screen composition with the user task as its hierarchy:

- One coherent filter workspace, clear/reset and visible active conditions.
- A scan-friendly directory: identity, organizational context, status and primary
  action; use composed cells/chips to reduce repetition without hiding meaning.
- A selected-person header that explains whose dossier is open, key context and
  primary action. Avoid repeating all directory fields as equally weighted cards.
- Domain sections or tabs with meaningful groups, intentional reading order,
  consistent spacing and restrained semantic color. Do not invent charts where
  the API has no meaningful measure.
- Forms with clear groups, required/optional cues, examples/format hints and
  actionable errors; a default schema dump is not finished product design.

Choose tokens and component-owned appearance, typography, density and responsive
controls. Check long names, zero/null values, disabled actions, empty collections,
loading and errors. Give tabs enough clickable area, clear active/hover/focus
states and predictable overflow; test keyboard navigation and panel semantics.
Mobile must expose the full dossier and a clear way back to the list. Preserve
desktop proportions instead of enlarging every card to hide clipping or bindings.

Write these observable acceptance criteria before authoring. A screenshot of
one attractive state does not prove the whole journey.

## Build and prove one vertical slice

Start with filters -> selection -> one dossier section -> one related list ->
native detail/form. Select configuration ownership before configuring content.
Prefer visual controls; use the visible free JSON for supported fields missing
from the form. Preserve a checkpoint, validate/apply/save, inspect the saved value
and exercise its runtime effect. Do not import a finished page when the requested
exercise is individual human editor interaction.

Use stable component IDs and declared ports. Keep selected record data and derived
dossier state ephemeral where appropriate; do not persist personal snapshots just
to retain a preview. Test selecting A then B, clearing selection and filtering a
selected record out. Propagate the current record, not just its unchanged ID.

### Prove ephemeral state discovery before connecting

Declare selection in `state.schema` with `persist:false` and an explicit `initial`
(null or an empty selection object, matching the consuming expressions). Keep real
records out of persisted `values`. Before authoring surfaces, open a new connection
and confirm that the declared path is offered as a writable destination, including
when a derived dossier node already exists. Save/reopen/reload and check again.
Do not discover this integration gate after building every tab.

On rc.26 a browser probe with `values:{}`, schema `selection` initial:null and a
`derived.employeeView` accepted the JSON but omitted `selection` from connection
selectors. Core already supports the initial and non-persistence; the graph only
collected values. Without derived, a fallback path can hide this defect. Existing
links can also recreate a visual port without proving initial discovery or clean
diagnostics. Check the installed graph against the owner fix before claiming it
resolved. Do not switch personal selection to persistent storage to make the
editor offer a port; a null-only positive control belongs in isolated diagnosis,
never in the ordinary rehearsal recipe. If this gate fails, retain the minimal
JSON and report the owner limitation rather than concealing it in take preparation.

Before multiplying the pattern across tabs, prove these transitions:

| Transition | Required observation |
| --- | --- |
| Related list -> New | Correct parent identity already visible, derived canonically; mandatory linkage and permission respected. |
| List -> detail/edit | Correct current record, hydrated labels/options and appropriate view/edit mode. |
| Save -> list | Persisted readback, feedback and correct refresh; retain relevant parent, query, order, page, selection and focus. |
| Cancel -> list | No write; both clean and dirty drafts return predictably to the same context. |
| Error -> form | Draft retained, field/domain error understandable; no false success or silent dismissal. |
| Change parent | No stale child collection/form or cross-parent submission. |

For a related list, distinguish its structural parent scope from editable search
criteria. Use the existing `queryContext.meta` contract with the dynamic parent
filter; do not present the parent as a removable cross-filter chip or hide it with
CSS. In this fragment, replace `<publishedParentField>` with the discovered child
parent field and adapt the selection/id expression to the authored page:

```json
{
  "queryContext": {
    "filters": {
      "<publishedParentField>": "${state.selection.value.selectedRows.0.id}"
    },
    "meta": {
      "relatedResource": true,
      "parentFilterField": "<publishedParentField>",
      "structuralFields": ["<publishedParentField>"]
    }
  }
}
```

For CRUD, place it in `metadata.queryContext`; for standalone Table, use its
`queryContext` input. Audit `@praxisui/table`'s `praxis-table.ts` and
`praxis-table.json-api.md`: `isStructuralQueryContextField` excludes the parent
from `computeActiveCrossFilters`, while `reconcileEditableQueryContextFilters`
retains it when reconciling editable criteria. Keep the parent identity visible
in the surface header/context and allow real child search criteria alongside it.
Prove filter, clear/readback and parent switching without losing the scope. The
browser control proved scoped data without a parent chip and an additional search
result. After transient API pool failures, desktop and mobile clear/readback
recovered six parent-scoped rows through Retry; this does not certify an
uninterrupted flow. Further checks retained desktop ascending sort and page 2
after create/cancel, and mobile page 2/original values after dirty edit/back/discard
with one confirmation.

This protects query context in the UI, not server ACLs or the parent linkage of a
submitted child. Backend authorization and relationship validation remain
independent. An unmarked, removable `queryContext.filters` value does not supply
that structural UX protection. Manually choosing the parent again and reopening
the child list can diagnose persistence, but do not count them as successful
inheritance or return navigation. Defaults alone do not prove lock or authorization.

Read the existing surface adapter, lifecycle/outcome and consuming owner before
inventing configuration. Opening success is not completed/save. A refresh path
implemented in CRUD may be absent in standalone Table; verify the installed
consumer actually handles it. Refetch alone may leave derived selection stale
when the same ID has a new record object. Do not invent JSON property names or
replace version preconditions to conceal this gap.

### Audit nested CRUD session binding before declaring a gap

An explicit CRUD inside a drawer surface can use the existing session instead of
opening a second overlay. Inspect the installed `SurfaceBindingRuntimeService`,
`DynamicWidgetLoaderDirective`, `CrudLauncherService` and
`DynamicFormDialogHostComponent`; pair with `praxis-crud-runtime-openmodes` and
`praxis-crud-dialog-form-host-lifecycle`. Prefer automatic canonical materialization
when it already wires the session correctly. Do not copy discovery catalogs into
page JSON as a new source of truth.

A browser control on public rc.22 proved this `surface.open` payload fragment for
an explicit `praxis-crud` widget, with its create action/defaults using
`openMode: "drawer"`:

```json
{
  "bindings": [{
    "to": "widget.inputs.context.surfaceRuntime",
    "mode": "constant",
    "value": "${surfaceRuntime}"
  }]
}
```

This is a reference to an ephemeral session, not a serialized function or private
runtime injection. In that pipeline, putting the token directly in widget inputs
resolves it before the new surface session exists. The constant binding inserts
the literal after surface-payload template resolution; the widget loader then
resolves it against the open surface context, and the drawer launcher can `push`
the form frame. Recheck these phases in the installed version before reusing it.

For related create, derive the current parent's canonical key into
`action.form.initialValue[childParentField]`; use the existing
`action.form.layoutPolicy` grouped-command preset and
`groupedCommand.contextFields` to present that context. Adapt the field and parent
binding to discovery and the current selection, and verify switching parents.
Initial value and contextual presentation do not prove a locked relationship or
server authorization.

The initial rc.22 control proved one overlay/session with native Voltar/Fechar, clean
cancel returning to the same list, and a real create with the derived parent,
persisted readback, refreshed collection and focus restored to the add action.
It did not certify update, page/order retention, mobile or dirty-draft protection:
changing a draft field and returning showed no confirmation. Modal explicitly
opened inside the drawer and automatic related materialization without this
binding remained defective in that baseline. Track those owner defects and a
removal/adaptation condition; this conditional recipe is not a universal fix or
evidence that every relationship journey is complete.

For an explicit Form Cancel, use `id: "cancel", type: "button"`;
`"cancel"` is not a `FormActionButton.type`. Audit both guards before changing
policy: in rc.22, `backConfig.confirmOnDirty` overrides
`form.behavior.confirmOnUnsavedChanges`, so Form Cancel followed by the CRUD host
can prompt twice. A later browser control proved a single host prompt with this
`metadata` fragment, preserving other defaults/actions and also omitting
`confirmOnDirty` from action-level `back`:

```json
{
  "defaults": { "back": {} },
  "form": {
    "behavior": { "confirmOnUnsavedChanges": false },
    "actions": { "cancel": { "id": "cancel", "type": "button" } }
  }
}
```

Omission preserves the host's default confirmation; do not set
`back.confirmOnDirty: false`. Check saved per-form `crud-back:${formId}` overrides.
Prove that cancelling the prompt keeps the draft and confirming returns to the
same list, then test Voltar, X/Fechar and Escape separately. In that control,
Voltar still left a dirty frame without prompting and the guard appeared later
when closing the list (historical rc.22 observation in Angular issue #613).
This is a conditional Cancel mitigation, not a universal navigation or security fix.

### Prove each surface exit on the installed artifact

If a child guard appears only after returning to the parent, audit the concrete
owner in `@praxisui/settings-panel`:
`src/lib/surface-drawer.component.ts` and
`src/lib/surface-drawer-bridge.provider.ts`. The frame must be active before the
first input application/change-detection pass invokes hosted lifecycle hooks that
register `setCanLeave`. Registration on the previously active frame can make back
skip the child guard and leave a stale guard on the parent. Correct that runtime
owner rather than weakening dirty-state policy in page JSON. Keep session closure
for programmatic scope replacement distinct from dismissing the current child.

A subsequent Hero HQ browser proof used a **locally patched and packed rc.26
settings-panel build**. It did not use the public rc.26 artifact as proof of the
fix, publish a release or perform domain writes. Record the actual source/tree
and artifact identity; a matching version label alone does not identify this fix.
Repeat this matrix when adopting an artifact:

| State and action | Required observation | Scope of that browser proof |
| --- | --- | --- |
| Dirty child: Voltar, X/Fechar, Escape, each separately | Exactly one confirmation; cancelling preserves the modified value; discarding returns to the same parent list. | Desktop and 390px mobile. |
| Context after discard | Parent identity, list page and ordering remain correct; record focus separately. | Desktop retained the external parent, page 2 and ordering. |
| Clean child: Voltar, X/Fechar, Escape | Return to the list without a discard prompt. | 390px mobile. |
| Lookup open: Escape | Close only the lookup, preserving the form and draft. | Observed. |
| Confirmation open: Escape | Cancel the confirmation, preserving the draft and child frame. | Observed. |
| Explicit Form Cancel on a dirty draft | One host prompt; preserve the same cancellation/discard behavior. | Mobile regression check. |
| Close root after child discard | No phantom prompt from a destroyed child guard. | Observed. |
| Backdrop dismissal, when enabled | Apply the current-step guard and preserve the parent. | Not certified by this browser control. |

The local proof validates the explicit nested-CRUD navigation path, not all of
issue #613. Automatic session wiring and modal fallback remained separate pending
paths. Keep the earlier binding recipe version-qualified until the adopted
runtime proves automatic wiring; do not remove it solely because a navigation
patch passed. Do not infer authorization, parent locking or a complete entity-360
journey from these exit checks.

## Test operations with explicit evidence boundaries

Use a per-resource matrix: supported, configured, opened, locally validated,
submitted, persisted/read back, denied or blocked. Keep commands separate from
CRUD and analytical views separate from their writable source resources.

Page configuration Save does not authorize domain writes. When writes are requested,
follow workspace isolation rules, identify the real runtime principal and preserve
restricted permissions. In Praxis database validations use the assigned remote
Neon branch; reads authorized against a public quickstart do not authorize writes
there. Keep config and domain databases isolated when startup may mutate both;
separate owner/migration/runtime identities, protect credentials and bind evidence
to source/build, endpoint, branch and TLS. A proxy's internal `pg_stat_ssl` can differ
from client TLS: verify the actual client transport rather than claiming either
encryption or its absence from one internal flag alone.

Use clearly synthetic fixtures in the assigned environment. Before creating data,
plan and record its cleanup, rollback or assigned-branch disposal, including any
retention needed for review; respect authorization and deletion confirmation.
Through native forms,
exercise required/range/format validation, create/read/update, partial update when
published, clean/dirty cancel, server errors, refresh and version conflicts where
applicable. For commands verify prerequisites, reason/confirmation, state change
and subsequent availability. A stale snapshot after your own edit is a useful
conflict probe, not proof of two-editor concurrency. Do not generalize ETag to
resources that do not publish a versioned contract.

Distinguish generic login from operational binding, current grants, field/record
coverage and published policy. A fail-closed 503 is not necessarily a 403 or a form
bug; retain the actual HTTP status/body and diagnose the owner. Never broaden
permissions merely to make a demonstration pass.

If create fails on generated PK, inspect identity/sequence/restore provenance
read-only before retrying. Do not choose an ID in JSON, advance sequences by repeated
submits or change the public database. A failed constraint request can consume a
sequence value. Distinguish a canonical seed bug from drift in its deployed data.
For delete, inspect whether the action has a native executor/owner and product
confirmation; a visible button may only emit an unhandled event. Complete the
authorization/confirmation required by the active tool policy before removal.

Browser traffic inspection and source/SQL diagnostics are evidence, not human
authoring. Keep them separate from visible editor actions, and never inject a
session or private runtime state to bypass the journey.

## Improve the platform and the guidance together

For each repeated correction, classify: already supported but undiscoverable,
poorly materialized, partially supported, or a real contract gap. First explore
metadata, native composition and supported JSON; keep the smallest accepted or
rejected document and observed effect. JSON cannot repair absent runtime code or
domain infrastructure. If no supported JSON exists, document the audited owner
and missing behavior instead of inventing a field to satisfy a nominal test.

Search current issues/fixes and distinguish installed adoption from newer source.
Create/update owner issues with the job, baseline, steps, JSON/schema proof,
actual outcome, desired visual/interaction states, accessibility/mobile,
round-trip and operational validation. Keep host registration, domain metadata,
infrastructure and library lifecycle defects separately actionable. Include the
removal trigger for any temporary composition; an open issue is not a completed UI.

Audit the authoring journey too: repeated panel changes, hidden configuration
ownership, technical codes without labels, missing examples, JSON-only composition,
weak validation location and unclear Apply/Save/Cancel semantics. Record the actual
detour and desired guided control, preview, preset or feedback in the editor owner's
issue. A visual editor improvement should preserve advanced JSON and round-trip;
faster automation alone does not establish easier human use.

Update this workflow for a reusable decision or procedure, the component owner
skill for a canonical component behavior, and product design guidance only for
reusable visual criteria. Do not turn one host/release workaround, local ID,
private credential or full personal payload into a universal recipe. Publish and
validate in the canonical skills repository, then sync only affected skills.

Finish with the editable saved page, journey screenshots on desktop/mobile,
operation matrix, data/persistence boundaries and unresolved owner issues. Report
quality, preparation and timing separately. Stabilize one complete slice before
optimizing speed or repeating it; never drop UX, real data or required proof to
claim a five-minute result.
