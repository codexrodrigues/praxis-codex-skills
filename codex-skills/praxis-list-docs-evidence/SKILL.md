---
name: praxis-list-docs-evidence
description: Use when updating or auditing `@praxisui/list` README, json-api docs, docs manifest, living examples, executive reference evidence, docs shell publication, landing/playground synchronization, declared-only status tables, screenshots, or example/E2E evidence for list/card/tile behavior.
---

# Praxis List Docs Evidence

Use this skill when `@praxisui/list` documentation, examples, playgrounds, or evidence artifacts must stay aligned with real runtime and authoring behavior.

Use `praxis-angular-docs-playgrounds` for cross-project docs publication and `praxis-list-runtime-data`, `praxis-list-authoring-settings`, or `praxis-list-ai-validation` for the behavior being documented.

## Canonical Sources

- Overview: `projects/praxis-list/README.md`
- JSON API: `projects/praxis-list/src/lib/praxis-list.json-api.md`
- Docs manifest: `projects/praxis-list/docs/praxis-docs.manifest.json`
- Runtime owner: `src/lib/components/praxis-list.component.ts`
- Data owner: `src/lib/services/list-data.service.ts`
- Authoring owner: `src/lib/editors/list-config-editor.component.ts` and `src/lib/list-editor-capability.ts`
- AI owner: `src/lib/ai/praxis-list-authoring-manifest.ts`
- Living docs/showcase: `src/lib/examples/praxis-list-doc-page.component.ts`
- Executive evidence: `docs/2026-03-executive-list-reference-checklist.md`, `docs/2026-03-executive-list-platform-backlog.md`, and `test-dev/e2e/praxis-list-executive-reference-evidence.playwright.spec.ts`

Docs are projections of these sources. Do not invent behavior in landing copy, examples, or guides.

## Required Checks

Before updating public content:

1. Identify whether the behavior is Active, Partial, Declared-only, Schema-only, Deprecated, or internal-only.
2. Verify the source file or spec that proves the status.
3. Check whether the same behavior appears in README, json-api docs, docs manifest, living examples, AI manifest, and landing docs.
4. If the behavior changed, update the derived surfaces in the same cycle or record why they are not affected.

## What Not To Overclaim

Do not document these as active unless runtime evidence changed:

- `layout.virtualScroll`
- `layout.stickySectionHeader`
- `actions[].emitPayload`
- `events.*`
- `a11y.highContrast`
- `a11y.reduceMotion`
- template `slot` renderer coverage beyond what component code proves

When docs describe a partial path, include the limitation so future AI agents do not implement host workarounds against a false contract.

## Validation

Use the smallest matching proof:

- docs frontmatter/publication changes: `npm run docs:validate-frontmatter:changed`
- living docs component changes: `src/lib/examples/praxis-list-doc-page.component.spec.ts`
- executive evidence changes: `test-dev/e2e/praxis-list-executive-reference-evidence.playwright.spec.ts`
- authoring canonical evidence: `test-dev/e2e/list-authoring-canonical.playwright.spec.ts`
- remote pagination docs: `test-dev/e2e/list-remote-pagination.playwright.spec.ts`
- docs/AI registry projection: `npm run generate:registry:ingestion` when docs metadata or component metadata feeds registry

For landing-page sync, read `praxis-ui-landing-page/AGENTS.md` and preserve official local origins and validators.

## Output Expectations

Report:

- behavior status classification
- canonical source consulted
- docs/examples/playgrounds changed or reviewed
- validation command run
- any remaining drift or intentional omission
