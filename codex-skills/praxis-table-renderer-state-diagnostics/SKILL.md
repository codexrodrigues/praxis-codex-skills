---
name: praxis-table-renderer-state-diagnostics
description: Use when Codex must implement, audit, or debug @praxisui/table renderers and user-visible states: column renderers, rich-content adapters, data formatting, empty/loading/error states, loadingStateChange, runtime observations, diagnostics, i18n copy, row/column renderer precedence, or renderer-specific specs.
---

# Praxis Table Renderer State Diagnostics

Use this skill when a table issue is about what the user sees: cells, renderers, formatting, empty/loading/error states, diagnostics, or runtime observations.

Rendering is a materialization of table config, schema metadata, rich-content contracts, and runtime state. Do not solve display issues by scraping DOM text or adding one-off host rendering branches.

## Source Audit

Inspect before editing:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/praxis-table.ts`
- `projects/praxis-table/src/lib/praxis-table.html`
- `projects/praxis-table/src/lib/praxis-table.scss`
- `projects/praxis-table/src/lib/data-formatter/**`
- `projects/praxis-table/src/lib/utils/rich-content-adapter.ts`
- renderer-specific `praxis-table.*rich-content.spec.ts`
- `projects/praxis-table/src/lib/i18n/table-runtime.i18n.ts`
- `projects/praxis-table/src/lib/praxis-table.metadata.ts`
- runtime observation and loading state specs when applicable.

Inspect `@praxisui/core` rich-content, i18n, loading, and runtime observation contracts when those are the shared source.

## Renderer Rules

- Resolve renderer behavior from column config, schema metadata, rich-content adapter, and table rule integration. Do not infer renderer intent from labels as the primary decision.
- Preserve renderer-specific contracts for icon, image, badge, link, button, chip, progress, avatar, toggle, menu, rating, html, compose, and micro-visualization.
- Keep row/column conditional renderer placement owned by table; visual effect payload semantics belong to `@praxisui/table-rule-builder`.
- Use data formatter services for dates, numbers, booleans, currency, percentage, value mapping, masks, and text transforms.
- Keep unsafe HTML, raw media URLs, large payloads, and unredacted runtime observations out of user-facing diagnostics unless the contract explicitly allows them.

## State And Diagnostics Rules

- Loading state should flow through table runtime state and `loadingStateChange`, plus shared core loading renderer when configured.
- Empty states should distinguish initial empty, filtered empty, and configured no-data actions.
- Error states should preserve user-visible message, runtime logs, and recoverable action where available.
- Runtime observations must be serializable and redacted, using core observation contracts rather than console-only diagnostics.
- User-facing chrome text belongs in `table-runtime.i18n.ts`; editor chrome belongs in `table-editor.i18n.ts`.

## Aderence Inventory

Classify before adding renderer/state fields:

- `ja-suportado-so-ux`: renderer/state exists but copy, visual affordance, or diagnostics are incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a local renderer alias should map to existing column/rich-content/formatter contracts.
- `suportado-parcialmente`: renderer/state works but i18n, accessibility, observation, docs, or focused specs are incomplete.
- `lacuna-real-de-contrato`: no table/core renderer, state, formatter, observation, or rich-content contract can express the visual decision.

Only real gaps justify new public rendering contracts. Otherwise fix materialization, i18n, or diagnostics in the owner.

## Validation

Use focused proof:

- matching `praxis-table.*rich-content.spec.ts`
- `data-formatting.service.spec.ts`
- `praxis-table.empty-state.spec.ts`
- loading/error/runtime operation specs.
- runtime observation specs when diagnostics are emitted.
- browser screenshot validation for visual, layout, accessibility, or interaction changes.

For first-step issue resolution, audit: source column/schema config, renderer choice, formatter path, rich-content payload, loading/empty/error branch, i18n key, observation envelope, and focused spec coverage.

## Companion Skills

- Use `praxis-table-runtime-data` for surrounding data/pagination/sorting runtime.
- Use `praxis-rich-content-runtime` for rich-content document and node contracts.
- Use `praxis-table-rule-table-integration` for conditional visual effects embedded in table.
- Use `praxis-core-widget-observations` for runtime observation envelopes.
- Use `praxis-ui-product-design` for visual QA.
