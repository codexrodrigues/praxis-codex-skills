# Overlapping state-to-input projections

Use this workflow when a state edit is persisted correctly but a widget displays
an older value after hydration. Core owns snapshot input materialization; a host
must not repair it by renaming link IDs, duplicating state, patching form config,
or reordering the entire composition graph.

## Audit the owning projection

Inspect these sources in `praxis-ui-angular`:

- `projects/praxis-core/src/lib/composition/composition-runtime.engine.ts`,
  especially `projectStateWidgetInputs`, and its focused specs
- `projects/praxis-core/src/lib/composition/state-input-projection-order.ts`
  and `state-input-projection-order.spec.ts`
- `projects/praxis-core/src/lib/widgets/widget-input-path.ts` and
  `connection-manager.service.ts`
- `projects/praxis-core/src/lib/widgets/widget-page-composition.factory.ts` and
  `widget-page-composition.serialization.ts`, which normalizes persisted links
- `projects/praxis-core/docs/table-connections-persistence-lab-baseline.md`
- `projects/praxis-core/test-dev/e2e/table-connections-persistence-lab.playwright.spec.ts`

Trace the rendered control's output through the declared event link, state value,
persisted page, reloaded runtime and final widget input. A correct saved value does
not prove a correct input projection. Inspect the effective destination path:
`context` can replace the object containing a separate
`context.detailFilterEmployeeId` override.

## Keep ordering scoped to snapshot writes

For state-to-input writes to the same top-level widget within one ordering
segment, apply an ancestor path before its descendant so the specific override
survives the base object. Compare path tokens using the shared internal accessor
grammar, not string prefixes: similarly named fields are not automatically
ancestors. Equal effective paths retain their existing relative order. This is a
Core implementation rule, not a new authored priority, public input, policy or
host-side merge contract.

A nested delivery to that same widget is a barrier between segments: flat writes
must not move across it. Keeping the nested delivery in its original slot alone
is insufficient, because moving a whole `config` write past a nested child update
can change the child content. Preserve the existing order across this barrier;
do not invent precedence between whole configuration and nested child writes.
A nested delivery to a different widget does not split this widget's segment.

Evaluate links in their existing order and order only the resulting snapshot
writes. Do not reorder event dispatch, conditions, transforms, diagnostics,
trace/matched-link evidence, policies or side effects to obtain the same final
input. Targets with `nestedPath` are excluded from this precedence rule; preserve
their existing materialization semantics. This does not add dotted/bracket input
paths to nested targets or permit `bindingPath` for new nested endpoints.

## Prove the actual edit and reload

1. Cover whole-object plus descendant projections in both link orders within one
   segment, equal paths, unrelated fields/widgets and token boundaries in focused
   Core specs. Cover interleaved nested deliveries to the same widget as barriers,
   including whole-config writes, and verify that another widget's nested delivery
   does not create a barrier. Prove event and side-effect execution order separately.
2. In the existing persistence lab, keep the source selection fixed, open the real
   form control, edit its independent detail filter and wait for its real CVA and
   `valueChange` path. Assert the displayed control and runtime state agree.
3. Wait for the canonical page writer to persist the edit, inspect the stored
   page state, reload and assert that the actual control retains the edit. This
   lab persists on edit; it has no Save or submit button for this step. Repeat
   with another value to detect stale context or a one-time hydration success.
   Verify source and tabs selection did not follow the independent filter. Do
   not replace this with synthetic output emission only.
4. Use the existing focused Core, app-consumer and browser lanes from the owning
   baseline. Record source/dependency identity and the tested host. Keep local
   storage proof distinct from remote persistence or authorization; report any
   unexecuted gate. This guidance does not certify a runtime patch by itself.

For the projection change, start from the Angular repository with:

```bash
npm run test:core -- \
  --include=projects/praxis-core/src/lib/composition/state-input-projection-order.spec.ts \
  --include=projects/praxis-core/src/lib/composition/composition-runtime.engine.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/connection-manager.service.spec.ts
```

The browser regression above must exercise the actual control after reload; do
not count a core snapshot or a stubbed form as that evidence.
