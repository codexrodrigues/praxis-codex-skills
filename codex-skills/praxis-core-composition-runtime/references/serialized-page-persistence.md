# Serializing the dynamic page writer

Use this workflow when automatic page saves overlap or a remote form edit reaches
state but does not survive reload. Core's `DynamicWidgetPageComponent` owns the
page writer. Config owns backend persistence, ETag/scope and authorization; pair
with `praxis-config-runtime-persistence` for that contract. Do not move the queue
into a demo host, disable conditional writes, or add a retry to hide a self-race.

## Audit the invocation boundary

Inspect these sources in `praxis-ui-angular`:

- `projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.ts`,
  especially `savePage`, canonical serialization and `ngOnDestroy`
- `projects/praxis-core/src/lib/widgets/dynamic-widget-page.persistence.spec.ts`
- `projects/praxis-core/src/lib/services/config-storage.service.ts` and its spec
- `projects/praxis-core/src/lib/services/enterprise-runtime-context.service.ts`,
  `models/enterprise-runtime-context.model.ts` and
  `tokens/enterprise-runtime-context.token.ts` under the same `src/lib/`
- `tools/e2e/playwright/tabs-valuechange-remote.playwright.spec.ts`

Capture the key and canonical page snapshot when a job is accepted. Invoke
`AsyncConfigStorage.saveConfig` only when that job reaches the front of the
instance's queue. `ApiConfigStorage` reads its cached ETag while constructing the
save Observable: constructing several Observables first and subscribing in order
can still reuse the same validator. Keep the interface and request payload intact;
adapters must return an Observable, including synchronous adapters. Do not treat
an invalid adapter return or a synchronous throw as successful persistence.

Keep the adapter's acknowledged cache update ahead of the next invocation.
The first `next` is the storage acknowledgement and releases that job without
waiting for extra emissions or source completion. `EMPTY` releases it without an
acknowledgement; an error releases a failed save. Neither empty completion nor an
error may fabricate an ETag, version, successful save or new public acknowledgement
event. Continuing the queue after failure is not retry or confirmation. Preserve
each accepted snapshot while its owning context remains valid; do not introduce
deduplication, coalescing or blind retry.

On component destroy, reject new jobs and let already accepted jobs drain through
their existing adapter contract while their context remains unchanged. This is
an in-memory queue per component instance. It does not serialize other
tabs/instances or guarantee completion during browser unload.

## Bind the owner to confirmed context

When `PRAXIS_ENTERPRISE_RUNTIME_CONTEXT_OPTIONS` is explicitly configured, inspect
the existing `EnterpriseRuntimeContextService`; do not introduce another context
store or a host flag. The page instance captures its initial ready provenance:
state, selection version, user, effective context version, tenant, environment,
organization, profile and module. A refresh timestamp is not that identity.
Without explicit context configuration, local/offline consumers keep their
existing behavior and do not acquire an HTTP dependency from this guard.

Mount the configured page only after confirmed `ready` context. An instance
created before readiness does not later enable persistence merely because the
context becomes ready. A different or invalidated snapshot,
including the temporary null snapshot during refresh or selection, permanently
invalidates persistence for that instance. Recreate the page after confirmation
and rebootstrap through its remote load. Changing an input or key does not
reassign the preceding page to the new context; there is no automatic hot-switch
of an existing document.

Check provenance again immediately before invoking the adapter for each queued
job. Discard obsolete jobs without acknowledgement; never redirect their payload
to the new tenant through a freshly evaluated headers factory. Reject new saves
from that obsolete owner too. Ignore its late load `next`, `error` and `complete`
callbacks so an old document cannot hydrate the new context or restore persistence
readiness. Keep observing context while accepted jobs drain after destroy, then
release the observation when the queue completes. A context change after destroy
still invalidates those queued jobs.

A fresh owner must receive host input/defaults coherent with its new context. A
missing remote document does not prove that a parent did not retain the preceding
tenant's state. The guard does not reset parent-owned state or introduce another
page store. `pageChange` remains local state notification, not a persistence ack;
this guard adds no success or failure UI.

This is a provenance guard, not an authentication or authorization freeze. A
request already sent remains subject to backend admission and ETag; the guard
does not cancel it, undo its effects or retry a refusal. `ApiConfigStorage` builds
headers synchronously when invoked, which is the guarded boundary. A custom
adapter that defers its own header resolution beyond that invocation is outside
this guarantee and needs its own context-bound proof. Never manufacture headers,
grants, cached validators or a successful ack to compensate. Pair with
`praxis-config-runtime-persistence` for server authority and scope semantics.

## Prove the writer and its real remote consumer

Start with the focused Core persistence spec. Cover delayed acknowledgements,
invocation order, immutable snapshot/key capture, synchronous adapter failure,
empty completion, errors and destroy with queued jobs. The current focused spec
contains ten tests, including six context-provenance regressions. Use the real
context service and HTTP adapter to prove pending A plus queued A, selection of B,
and a pending A refusal with both `412` and `403`: no queued A request may use B's
headers. Edits on the obsolete owner remain blocked; a new owner must load B's
document before its B save. Also cover a late A load, creation before readiness,
drain on destroy without a context change, and rejection when context changes
after destroy. A spy returning an already created Observable cannot prove when
the adapter captured either validator or headers. These unit transport controls
are not a remote corporate SESSION/admission proof.

```bash
npm run test:core -- \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.persistence.spec.ts \
  --include=projects/praxis-core/src/lib/services/config-storage.service.spec.ts
```

Use the existing remote browser regression for the full consumer proof:

1. Fill the actual filter control with `410`, then `193`, preserving source/tabs
   selection. Wait for automatic persistence; do not replace the CVA and
   `valueChange` path with synthetic emission or seeded storage.
2. Require each target PUT to return `200`, the canonical payload with 14 fixture
   composition links and no legacy `connections`, a quoted ETag and server version.
   Inspect the acknowledged payload, not only local state or outgoing JSON.
3. Reopen in fresh browser contexts. Require a remote `200` GET without a cached
   validator, matching acknowledged payload/ETag/version and restored real controls.
   A local adapter, `304` cache reuse or a runtime snapshot alone is not this proof.
4. Track every request for the exact fixture identity. Reject a hidden `412` or
   other failed target PUT even if another succeeds; record `requestfailed` and
   require zero pending target requests before closing the page. Preserve source,
   dependency, served-host and assigned isolated Neon branch evidence.

Demo/local headers and a development host profile do not certify SESSION-backed
tenant authorization. The list fixture and local persistence lab remain useful
component proofs, not substitutes for this remote round-trip or corporate security.
Record missing gates and their owner; a prepared skill update is not a passing
runtime or remote validation result.
