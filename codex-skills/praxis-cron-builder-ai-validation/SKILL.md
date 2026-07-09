---
name: praxis-cron-builder-ai-validation
description: Use when Codex must change, audit, or validate AI-assisted authoring for `@praxisui/cron-builder`, including `PRAXIS_CRON_BUILDER_AUTHORING_MANIFEST`, AI adapter snapshots, capabilities, context packs, registry ingestion, semantic schedule intent, `cron.expression.set`, `cron.frequency.set`, `cron.timezone.set`, `cron.preset.apply`, `cron.validate`, `cron.preview.generate`, diagnostics, preview safety, docs, examples, or assistant validation for CRON and schedule authoring.
---

# Praxis Cron Builder AI Validation

Use this skill for agentic schedule authoring and validation. AI should author semantic schedule decisions, not raw JSON patches or keyword-routed command strings.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-cron-builder/AGENTS.md`
- `projects/praxis-cron-builder/src/lib/ai/praxis-cron-builder-authoring-manifest.ts`
- `projects/praxis-cron-builder/src/lib/ai/cron-builder-ai.adapter.ts`
- `projects/praxis-cron-builder/src/lib/ai/cron-builder-ai-capabilities.ts`
- `projects/praxis-cron-builder/src/lib/ai/cron-builder-context-pack.ts`
- `projects/praxis-cron-builder/src/lib/schedule-contract.ts`
- `projects/praxis-cron-builder/src/lib/schedule-normalizer.ts`
- `projects/praxis-cron-builder/src/lib/schedule-authoring-runtime.ts`
- `tools/ai-registry/**` when registry projection changes
- focused AI adapter, manifest, schedule runtime, and registry specs

## Canonical Boundary

`PRAXIS_CRON_BUILDER_AUTHORING_MANIFEST` is the canonical AI operation contract for the component. It declares runtime inputs, editable targets, operations, validators, affected paths, submission impact, preconditions, failure modes, and round-trip requirements.

The AI adapter exposes both legacy `value` and structured `schedule` state, plus read-only `diagnostics` and `preview`. The runtime package owns validation and preview semantics. Hosts may supply business context and persistence, but must not become the primary CRON parser or intent router.

## AI Authoring Rules

- Route intent through declared manifest operations and semantic targets, not keyword lists, regex commands, or host-local text heuristics.
- Prefer `cron.frequency.set` with `schedule.kind` and `schedule.recurrence` for business recurrence intent.
- Use `cron.expression.set` only for explicit CRON expression requests.
- Use `cron.timezone.set` for IANA timezone changes and regenerate preview/diagnostics from the same schedule state.
- Use `cron.preset.apply` only after resolving a declared preset by stable label or cron identity.
- Keep `cron.validate` and `cron.preview.generate` read-only. They may write diagnostics or preview output, never schedule/value fields.
- Run diagnostics before mutating schedule or compatibility value paths.
- Preserve `affectedPaths`, `submissionImpact`, validators, and failure modes when adding or changing operations.
- Do not let an AI patch invalid recurrence, invalid timezone, incompatible dialect fields, or preview-only output into persisted schedule state.

## Validation Rules

The manifest validators are operational promises:

- `cron-expression-valid`
- `cron-dialect-compatible`
- `timezone-valid`
- `frequency-maps-to-canonical-expression`
- `preset-exists`
- `preset-maps-to-canonical-expression`
- `preview-matches-expression`
- `invalid-schedules-return-diagnostics`
- `diagnostics-before-patch`
- `editor-runtime-round-trip`

When a task changes authoring behavior, prove that adapter snapshots, runtime CVA state, schedule normalization, preview output, and registry projection still agree.

## Inventory Before New Contract

Classify AI gaps before adding operations or fields:

- `ja-suportado-so-ux`: diagnostics, preview, examples, or context pack evidence exists but is not shown to the assistant well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the operation or validator exists but consumers use a local patch shape or alias.
- `suportado-parcialmente`: the manifest can represent the decision but needs capability, context pack, registry, docs, or test coverage.
- `lacuna-real-de-contrato`: no manifest operation, target, validator, diagnostic, or schedule contract can carry the semantic decision.

For real gaps, update the canonical manifest and its specs before adding host-specific assistant behavior.

## Validation

Use the smallest reliable proof:

- `cron-builder-ai.adapter.spec.ts`
- `praxis-cron-builder-authoring-manifest.spec.ts`
- `cron-builder-ai-capabilities.spec.ts` or context-pack specs when capabilities/context change
- `schedule-authoring-runtime.spec.ts` and `schedule-normalizer.spec.ts` when operations affect compile/diagnostics/preview
- AI registry ingestion validation when manifest projection changes
- docs/playground validation when public AI examples or guides change

Report exact positive and negative prompts validated, especially invalid CRON, invalid timezone, preview-only, and read-only validation cases.

## Companion Skills

- Use `praxis-cron-builder-runtime` for runtime/CVA round-trip and visible preview behavior.
- Use `praxis-cron-schedule-authoring` for semantic schedule config, dialects, compile, validation, and preview contracts.
- Use `praxis-cron-builder-form-field` when AI-authored values flow through metadata-driven forms.
- Use `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion` for shared manifest and registry governance.
