---
name: praxis-list-runtime-data
description: Use when implementing, reviewing, or explaining `@praxisui/list` runtime behavior: list/card/tile layouts, local versus remote data resolution, `dataSource.data`, `dataSource.resourcePath`, `queryContext`, pagination, grouping, selection, item actions, templating slots, skin, export, rich-content convergence, and declared-only runtime boundaries.
---

# Praxis List Runtime Data

Use this skill for the runtime side of `@praxisui/list`: rendering configurable lists, cards, and tiles from local or remote collections without moving list semantics into host apps.

## Canonical Owner

`@praxisui/list` owns list/card/tile presentation, list config interpretation, local/remote data precedence, list templating, selection payloads, skin application, item actions, export event emission, and list-specific runtime docs. Host apps own authorization, route shell, durable domain state, API provider wiring, and business data.

Use `praxis-core-resource-runtime` when the change depends on `GenericCrudService`, `resourcePath`, query context, HATEOAS, capabilities, or collection export contracts. Use `praxis-angular-public-api-governance` for root exports and package boundaries.

## Required Source Audit

Before editing or advising:

- `projects/praxis-list/AGENTS.md`
- `projects/praxis-list/README.md`
- `projects/praxis-list/src/public-api.ts`
- `projects/praxis-list/src/lib/models/list-config.model.ts`
- `projects/praxis-list/src/lib/components/praxis-list.component.ts`
- `projects/praxis-list/src/lib/services/list-data.service.ts`
- `projects/praxis-list/src/lib/services/list-skin.service.ts`
- `projects/praxis-list/src/lib/utils/template-evaluator.ts`
- `projects/praxis-list/src/lib/utils/selection-adapter.ts`
- `projects/praxis-list/src/lib/utils/rich-content-adapter.ts`
- `projects/praxis-list/src/lib/praxis-list.json-api.md`

## Runtime Rules

- `dataSource.data` has priority over `dataSource.resourcePath` when both exist. Do not weaken this precedence in docs, examples, or host adapters.
- `dataSource.resourcePath` enters remote mode only when local data is absent and a `GenericCrudService` is available.
- Remote mode configures `GenericCrudService` with the base resource path and calls `/filter` through `filter(query, pageable)`. Only an empty query may fall back to `getAll()` on failure. Active criteria fail closed with the retryable error stream; never widen a failed filtered query to unfiltered records.
- Loading must be visible and announced without requiring a skeleton configuration. Keep search/toolbars mounted, hide stale row actions and empty/error content during the pending request, and retain keyboard focus in the collection when retry/pagination replaces its trigger. Test delayed requests as well as immediate failures.
- Before enabling `ui.searchField` in an operational fixture or example, verify that the query field exists in the canonical filter schema/DTO. A field displayed in response rows is not necessarily searchable; an ignored criterion can produce plausible but unfiltered results.
- `layout.groupBy` groups the loaded items in the runtime service. Do not implement duplicate grouping in a host unless the host is intentionally pre-shaping local data.
- `layout.pageSize`, `dataSource.sort`, and `dataSource.query` participate in the request signature; changes should reset pagination where the runtime does so.
- `selection` supports `none`, `single`, and `multiple`, with return modes `value`, `item`, or `id`. Validate form binding and `compareBy` before changing payload semantics.
- `actions` may emit local events or delegate to shared `GlobalActionService` through canonical `globalAction`. Do not persist command strings or host-only action DSLs.
- `export` uses the shared collection export contract from `@praxisui/core`; optional export UI must still be gated by capability/link evidence when the resource is remote.
- Select `configPersistenceStrategy` deliberately. `volatile` disables local
  storage for transient/public materializations; `input-first` and
  `local-first` retain their documented precedence. Never persist a runtime
  projection merely because the list opened.
- Owner-authored runtime profiles describe the closed local shape or declared
  remote read effects. A matching profile is execution evidence for host policy,
  not authorization and not a substitute for resource capabilities.

## Active Versus Declared

Keep docs and implementation honest:

- Active or materially supported: `dataSource`, `skin`, `selection`, `i18n`, `ui`, collection `export`, most layout basics, and common templating slots.
- Partial: `layout` as a whole, `templating` as a whole, `actions`, `a11y`, row layout, expansion, rich-content convergence, and advanced template types.
- Declared-only or not runtime-proven: `events.*`, `layout.virtualScroll`, `layout.stickySectionHeader`, `actions[].emitPayload`, `a11y.highContrast`, and `a11y.reduceMotion`.

Do not describe declared-only fields as active runtime behavior. If a task needs one active, classify it as a platform contract/runtime gap and implement it in `@praxisui/list`, then update docs, editor, manifest, and tests.

## Rich Content And Templating

Treat list templating as list-owned unless a path is explicitly promoted to shared rich content. `mapListTemplateToRichContentP0(...)` is the restricted bridge to shared rich content vocabulary. The promoted subset is small: `text`, `icon`, `image`, `chip` to badge, `metric`, and `compose`. Do not silently promote `component`, `slot`, `html`, `rating`, `currency`, or `date` into shared rich content without a semantic decision.

Render the promoted presenter nodes with Rich Content's existing `layout="inline"` in compact list/card/tile slots (row slots, leading/primary/secondary, metadata, trailing/status and features). Preserve block flow for empty-state regions, section headers and rich-content expansion documents. Do not remove document containment or add consumer CSS to compensate for a compact host using block layout. Check actual badge/text geometry and readability in desktop and narrow real-shell screenshots: DOM text or node presence alone can pass while a shrink-to-fit presenter has zero width.

Template expressions are list template expressions like `${item.field}` with simple pipes, not general Json Logic. Json Logic belongs to rules/effects, not template interpolation.

## Validation

Use the smallest proof that matches the change:

- runtime data precedence or remote loading: `src/lib/services/list-data.service.spec.ts`
- component rendering, events, selection, templating, skin, or export: `src/lib/components/praxis-list.component.spec.ts` plus focused utility specs
- volatile/profile behavior: `src/lib/components/praxis-list.volatile-persistence.spec.ts`, metadata/profile specs, and registry projection proof
- remote pagination: `test-dev/e2e/list-remote-pagination.playwright.spec.ts` when browser evidence is required
- surface host integration: `test-dev/e2e/surface-open-list-demo.playwright.spec.ts` when list is opened as a composed surface
- public API or docs behavior: use `praxis-angular-public-api-governance` and `praxis-list-docs-evidence`

Prefer `ng build praxis-list` from `praxis-ui-angular` for compile validation of the lib, and use `praxis-angular-validation-gates` to decide whether consumer builds, AI registry, docs validators, or Playwright are required.
