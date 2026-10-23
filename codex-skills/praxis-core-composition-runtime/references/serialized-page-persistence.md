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
each accepted snapshot; do not introduce deduplication, coalescing or blind retry.

On component destroy, reject new jobs and let already accepted jobs drain through
their existing adapter contract. This is an in-memory queue per component
instance. It does not serialize other tabs/instances, guarantee completion during
browser unload, or freeze tenant/authentication context for deferred calls.
Capturing a storage key is not evidence that later request headers or server
authorization were captured with it. Keep those guarantees separate and explicit.

## Prove the writer and its real remote consumer

Start with the focused Core persistence spec. Cover delayed acknowledgements,
invocation order, immutable snapshot/key capture, synchronous adapter failure,
empty completion, errors and destroy with queued jobs. A spy returning an already
created Observable cannot prove when the adapter captured the validator.

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
