# Praxis Skill Review Retrospective - July 2026

## Purpose

This retrospective audits the first closed Praxis skill-review pilots after the
program backlog was emptied. A closed review issue is not automatically treated
as approved. The audit checks whether the issue has reproducible evidence and
whether later source changes created material drift.

## Scope

Initial pilot issues:

| Issue | Skill | Initial purpose |
| --- | --- | --- |
| #170 | `praxis-ai-semantic-intent` | Semantic routing and adversarial validation |
| #188 | `praxis-charts-runtime-data` | Complex chart data/runtime integration |
| #195 | `praxis-core-composition-runtime` | High-impact transversal Angular runtime |

Source repositories checked:

- `praxis-codex-skills`
- `praxis-ui-angular`

## Summary

| Issue | Evidence quality | Current drift reading | Retrospective decision |
| --- | --- | --- | --- |
| #170 `praxis-ai-semantic-intent` | Strong | No material source drift found in scoped AI intent files after the merged runtime fix | `aprovada-com-evidencia` |
| #188 `praxis-charts-runtime-data` | Strong at closure | Material chart runtime/source changes landed after the review | `skill-desatualizada-por-drift` |
| #195 `praxis-core-composition-runtime` | Strong at closure | Material composition runtime change landed after the review | `skill-desatualizada-por-drift` |

## #170 - Praxis AI Semantic Intent

Decision: `aprovada-com-evidencia`.

Evidence found:

- Issue #170 recorded source inventory, happy path, risk path, adversarial path,
  validation commands, limitations, and final classification.
- `praxis-codex-skills` PR #196 was merged as `f420faff`.
- `praxis-ui-angular` PR #144 was merged as `a1a68f1a`, removing the browser
  fallback that inferred executable semantics from clarification text.
- Recorded validation included assistant tests, governed-routing/scope-policy
  specs, production build for `@praxisui/ai`, skills preflight, and remote gates.

Drift check:

- `praxis-ai-semantic-intent/SKILL.md` has not changed after PR #196.
- The relevant `praxis-ui-angular` source history after July 10 shows the
  intended runtime fix `a1a68f1a` in the scoped AI files; no later material
  change was found in the audited AI intent routing files during this pass.

Limitations:

- Full consumer E2E remained blocked by local environment issues documented in
  the issue. This is acceptable because the focal runtime and adversarial
  evidence were strong and the limitation was explicit.

Follow-up:

- None required from this retrospective.

## #188 - Praxis Charts Runtime Data

Decision: `skill-desatualizada-por-drift`.

Evidence found:

- Issue #188 and PR #197 recorded source inventory, adherence classification,
  happy/risk/adversarial proof, focused Angular specs, production build, and
  limits around unpublished backend/dashboard smoke.
- PR #197 was merged as `5ad76b9`.
- The original review correctly corrected `queryContext`, stats POST, schema
  mapper, backend payload adapter, and round-trip guidance.

Drift check:

After PR #197, `praxis-ui-angular` has material chart changes in the audited
surface, including:

- `b75ebe68 fix(charts): align query context runtime contract`
- `9164dbdd fix(charts): complete declarative interaction outputs`
- `fcd5d598 test(charts): codify chart authoring coverage`
- additional chart authoring, widget settings, option-builder and event-contract
  changes in the chart runtime/config-editor surface.

These changes touch the same family of contracts the skill governs:
`queryContext`, chart component events, canonical mapper, schema mapper,
authoring manifest, and chart metadata.

Follow-up required:

- #246: re-audit `praxis-charts-runtime-data` against the current chart runtime,
  query-context and declarative interaction source.
- Update the skill only if the current guidance no longer matches source.
- Re-run focused chart specs and production build.

## #195 - Praxis Core Composition Runtime

Decision: `skill-desatualizada-por-drift`.

Evidence found:

- Issue #195 and PR #198 recorded source inventory, adherence classification,
  happy/risk/adversarial proof, focused Angular specs, production build, and
  limits around Page Builder/browser/global-action integration.
- PR #198 was merged as `4933d55`.
- The original review correctly captured `composition.links`, partial delivery
  policy support, transform catalog boundaries, nested port materialization,
  diagnostics, trace and runtime observations.

Drift check:

After PR #198, `praxis-ui-angular` has a material composition runtime change in
the audited surface:

- `b550c753 feat(composition): detect feedback cycles (#195)`

This change touches `composition-runtime.engine`,
`composition-validator.service`, and their specs. Feedback-cycle diagnostics and
validation are within the skill's runtime/diagnostic boundary, so the skill
needs a focused source-parity check before it can be called current.

Follow-up required:

- #247: re-audit `praxis-core-composition-runtime` against feedback-cycle detection
  and current composition diagnostics.
- Update the skill only if it lacks the new canonical behavior or validation
  gate.
- Re-run focused composition specs and production build.

## Validation

Repository governance checked during this retrospective:

```bash
python3 scripts/audit-praxis-skills.py --family praxis --json
```

Result: 161 Praxis skills OK, 0 drift, 0 missing, 0 source-invalid in the
installed projection.

No Angular test suite was executed during this retrospective pass because the
purpose was evidence triage and drift detection. The follow-up issues must run
their focused Angular gates.
