# Guidance from the editor review corrections

The Angular consumer corrections reuse the existing cumulative metadata patch and
Settings Panel asynchronous Save contracts. This documentation change updates only
three canonical skills and their manifest hashes; no dependency or family changes.

- Metadata consumer bridges: opening field baseline, recursive/null semantics,
  A → B → Apply → A, empty final delta, and preservation of other parent fields.
- Settings roundtrip: awaited persistence before shell completion, duplicate-write
  avoidance, stale responses, dirty/reset/Apply distinctions and silent reset state.
- List authoring: standalone persistSettings callback, owner lifecycle, retry,
  volatile mode and tests through the real editor/Settings Panel with a controlled adapter.

Evidence: Angular Layout (35), merge helper (2), Filter Settings (64), List editor,
widget and persistence (47) passed in the implementation worktree based on Angular
main 405ad690. Browser prototype evidence is separate from these component tests.
The guidance does not certify HTTP durability or change canonical backend contracts.

Validation: the three skill structures passed; Python fallback preflight passed
(41 script tests). Both complete families passed fail-on-drift audit against a clean
staging installation (167 Praxis, 19 Ergon). The three changed skills were synced by
the canonical Python fallback because pwsh is absent, then their installed trees
matched the manifest. A temporary filtered manifest scopes sync; the full source
manifest remains canonical and is used for inventory auditing.

The full existing local installation has two unrelated pre-existing differences:
praxis-list-runtime-data and praxis-ui-product-design. They were preserved. The
Ergon installation audit passed. This is scoped installation parity, not a claim
that every locally installed Praxis skill is identical to remote main.
