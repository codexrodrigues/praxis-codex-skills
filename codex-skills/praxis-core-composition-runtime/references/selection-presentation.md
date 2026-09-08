# Selection presentation through canonical links

Use this workflow when a selected row supplies a widget identity or formatted
subtitle. Core owns execution and presentation; Page Builder owns the connections
editor. A business field name never selects a formatter or routes primary intent.

## Inspect before authoring

From the Angular repository, read:

- `projects/praxis-core/docs/composition-value-format.md`
- `projects/praxis-core/src/lib/i18n/composition-value-format.ts` and its spec
- `projects/praxis-core/src/lib/composition/transform-runtime.service.ts`
- `projects/praxis-core/src/lib/composition/composition-format.integration.spec.ts`
- `projects/praxis-core/src/lib/composition/link-executor.service.ts`
- `examples/ai-recipes/praxis-dynamic-page.widget-selection-identity.json` and its referenced `.page.json`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.spec.ts`

The supported surface is `WidgetPageDefinition.composition.links[].transform`.
Do not advertise `format-value` in `UiCompositionPlanTransform`: its agentic
shorthand requires a separate compiler implementation and proof. A generated
registry, deterministic handler check, and a live LLM authoring gate are different
evidence; never present one as all three.

## Author the projection

1. Ground the table's canonical `selectionChange` endpoint and row fields. The
   recipe's `name`/`birthDate` are fixture fields, not universal resource aliases.
2. Deliver selection to writable `transient` state; never persist selected rows
   into `page.state.values`. Preserve the independent `resourceId` link for a
   remote detail form. Do not add an avatar-specific event or port.
3. Keep four synchronous links in document order: replace the identity with the
   current name/photo and empty labels; format date; format document; compose the
   subtitle from present parts. Empty selection must also replace the identity.
   A failed transform retains the destination's previous value; resetting first
   ensures that value belongs to the new selection. `fallbackValue` handles
   `undefined`, not exceptions. Debouncing or reordering needs a new coherence proof.
4. Use `format-value` with `config.format`, consuming the prior step output or
   an explicit existing `TransformStep.input`. `date` accepts a valid civil
   `YYYY-MM-DD` string, not a timestamp; `mask` requires text and exact digit
   count, preserves leading zeros, and does not validate CPF check digits.
   See the canonical doc for numeric defaults and options; do not generalize
   date/mask rejection to the numeric formatter's existing zero conversion.
5. Prove the initial state before any event as well as clear. The recipe uses a
   literal title prefix; a host can use the form's existing `emptyState` instead.
   Shell interpolation resolves paths, not conditional/formatting expressions.

Invalid format configuration produces `SEMANTIC_TRANSFORM_FORMAT_INVALID`.
Invalid date/mask data produces `RUNTIME_TRANSFORM_STEP_FAILED`. Verify independent
failures retain distinct link-qualified diagnostic ids and `subject.linkId`.

## Smallest useful proof

- Run formatter, transform runtime, and `composition-format.integration.spec.ts`
  for civil dates, leading zeros, missing/invalid values, reset, recovery, two
  failed links, source immutability, and serialize/reopen with no selected data.
- Reopen the connections editor: inspect transient layer, format, mask/locale,
  guidance, invalid configuration blocking Apply, and unchanged JSON round-trip.
  Apply updates the page draft; Save persists it. Inspect the open editor at
  desktop and narrow width, not just the final runtime screen.
- For a remote form, inspect its own pending/error/retry behavior with
  `praxis-form-schema-runtime-modes`. Immediate header rendering does not prove
  that the previous form values disappear in the first frame.
- Keep deterministic fixture, real HTTP, persistence, and LLM evidence separate.
  Preserve the existing page and conditional ETag when applying an authorized
  migration. Do not overwrite concurrent layout/config changes from a fixture.
- For implementation changes, review Core/Page Builder docs, capabilities,
  manifests, recipe and public-site mirrors. Run focal builds and a direct
  consumer proof when public runtime/config changes; docs-only guidance does
  not require rebuilding packages or publishing the registry.
