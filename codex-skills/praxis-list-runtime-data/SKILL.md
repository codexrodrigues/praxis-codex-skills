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
- Remote mode configures `GenericCrudService` with the base resource path, calls `/filter` through `filter(query, pageable)`, and falls back to `getAll()` when `/filter` fails.
- `layout.groupBy` groups the loaded items in the runtime service. Do not implement duplicate grouping in a host unless the host is intentionally pre-shaping local data.
- `layout.pageSize`, `dataSource.sort`, and `dataSource.query` participate in the request signature; changes should reset pagination where the runtime does so.
- `selection` supports `none`, `single`, and `multiple`, with return modes `value`, `item`, or `id`. Validate form binding and `compareBy` before changing payload semantics.
- `itemActions & actions`: Ações declarativas no item (`itemActions` ou `actions`) suportam despacho via `GlobalActionService` (através de `command`/`params` ou `globalAction`), emissão de evento local `actionClick` com assinatura fixa `{ actionId, item, index }`, visibilidade condicionada por HATEOAS (`hateoasRel` validado contra `_links` / `links`) e renderização em menu kebab (`kind: 'menu-item'` ou `placement: 'menu'`).
- `quickView`: `TemplateDef.quickView` e `ComposeItemDef.quickView` (`ResourceQuickViewBinding`) habilitam Quick View transversal governado por registro via `[praxisQuickView]` (`PraxisQuickViewTriggerDirective`), isolando cliques com `stopPropagation()` para preservar seleção e botões de ação do item, e preservando `quickView` em `rules.slotOverrides`.
- `layout.virtualScroll`: Virtual scrolling canônico via `@angular/cdk/scrolling` (`CdkVirtualScrollViewport` com `itemSize`, `minBufferPx`, `maxBufferPx` e `viewportHeight`). Habilitado declarativamente via `layout.virtualScroll: { enabled: true, itemSize: 64, viewportHeight: '480px' }` ou `@Input() virtualScroll`.
- `export` uses the shared collection export contract from `@praxisui/core`; optional export UI must still be gated by capability/link evidence when the resource is remote.
- `emptyState & setup CTA`: When `items` are empty and no custom `templating.emptyState` is configured, `PraxisList` renders the canonical `<praxis-empty-state-card>` from `@praxisui/core`, distinguishing three states: **Setup State** (`isResourceConnectionMissing() === true`, icon `link`, with `primaryAction` opening `ResourceQuickConnectComponent` via `openQuickConnect()` and secondary action opening `openConfigEditor()` only when `enableCustomization === true`), **Filtered/Search Empty State** (`hasActiveSearchTerm() === true`, icon `search_off`, with secondary action *"Limpar busca"* / `clearSearch()`), and **Runtime No-Data State** (`icon="inbox"`). Connecting via `openQuickConnect()` strips empty `dataSource.data`, resets stale search/query/sort from any previous resource, and routes through `applyAuthoringPayload` so schema inference and `configPatchChange` (`{ inputPatch: { config } }`) execute canonically on both Apply (`settings-applied`) and Save (`settings-saved`).
- `i18n & locale`: Em hosts em português ou que utilizam formatação de data relativa (`type: 'relative'`), data (`type: 'date'`), moeda (`type: 'currency'`) ou paginação, a aplicação consumidora deve prover explicitamente `{ provide: LOCALE_ID, useValue: 'pt-BR' }`, além de `registerLocaleData`. Sem essa injeção, o Angular adota o fallback `en-US` do framework, forçando o `Intl.RelativeTimeFormat` a gerar termos em inglês (ex.: `2 days ago` em vez de `anteontem`). No schema da lista, `config.i18n.locale` deve ser configurado quando o componente precisar fixar um idioma específico independentemente do locale global.

## Active Versus Declared

Keep docs and implementation honest:

- Active or materially supported: `dataSource`, `skin`, `selection`, `i18n`, `ui`, collection `export`, `layout.virtualScroll` (CDK virtual scrolling), `itemActions` (com HATEOAS e menu kebab), most layout basics, and common templating slots.
- Partial: `layout` as a whole, `templating` as a whole, `a11y`, row layout, expansion, rich-content convergence, and advanced template types.
- Declared-only or not runtime-proven: `events.*`, `layout.stickySectionHeader`, `actions[].emitPayload`, `a11y.highContrast`, and `a11y.reduceMotion`.

Do not describe declared-only fields as active runtime behavior. If a task needs one active, classify it as a platform contract/runtime gap and implement it in `@praxisui/list`, then update docs, editor, manifest, and tests.

## Rich Content And Templating

Treat list templating as list-owned unless a path is explicitly promoted to shared rich content. `mapListTemplateToRichContentP0(...)` is the restricted bridge to shared rich content vocabulary. The promoted subset is small: `text`, `icon`, `image`, `chip` to badge, `metric`, and `compose`. Do not silently promote `component`, `slot`, `html`, `rating`, `currency`, or `date` into shared rich content without a semantic decision.

Template expressions are list template expressions like `${item.field}` with simple pipes, not general Json Logic. Json Logic belongs to rules/effects, not template interpolation.

## Validation

Use the smallest proof that matches the change:

- runtime data precedence or remote loading: `src/lib/services/list-data.service.spec.ts`
- component rendering, events, selection, templating, skin, or export: `src/lib/components/praxis-list.component.spec.ts` plus focused utility specs
- remote pagination: `test-dev/e2e/list-remote-pagination.playwright.spec.ts` when browser evidence is required
- surface host integration: `test-dev/e2e/surface-open-list-demo.playwright.spec.ts` when list is opened as a composed surface
- public API or docs behavior: use `praxis-angular-public-api-governance` and `praxis-list-docs-evidence`

Prefer `ng build praxis-list` from `praxis-ui-angular` for compile validation of the lib, and use `praxis-angular-validation-gates` to decide whether consumer builds, AI registry, docs validators, or Playwright are required.
