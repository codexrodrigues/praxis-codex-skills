# Praxis Skill Review Program

## Objective

Codify current Praxis platform knowledge in executable Codex skills so future
implementation uses canonical owners, contracts, tooling, and validation with
less local adaptation and less trial and error.

Skill count is an inventory metric. Program completion requires source parity
and operational evidence.

## Baseline

Baseline captured on 2026-07-10.

| Metric | Count |
| --- | ---: |
| Versioned skills | 155 |
| Praxis skills | 146 |
| Ergon migration skills | 9 |
| Generated review drafts | 155 |
| Review issues found | 50 |
| Open Praxis review issues | 31 |
| Closed Praxis review issues | 10 |
| Closed Ergon review issues | 9 |
| Skills without a review issue | 105 |

The 146 Praxis skills provide strong canonical Angular coverage. They do not
prove exhaustive Angular coverage or whole-platform parity. The current
Angular-only exhaustive estimate remains 180-200 skills, but new skills must be
created from source evidence or repeated implementation misses rather than a
numeric target.

## Coverage Model

Track each skill through five independent levels:

1. `inventory`: present in exactly one canonical manifest.
2. `backlog`: represented by a review issue.
3. `source-parity`: compared with current owners, contracts, implementation,
   specs, docs, manifests, examples, and direct consumers.
4. `operational-proof`: exercised in a happy path, a risk/edge case, and an
   adversarial scenario with focused local validation.
5. `approved`: evidence is reproducible and the final audit is recorded.

## Project Taxonomy

Use one primary project classification per review:

- `praxis-ui-angular`
- `praxis-config-starter`
- `praxis-metadata-starter`
- `praxis-api-quickstart`
- `praxisui-http-examples`
- `praxis-ui-landing-page`
- `transversal`
- `ergon-migration`

Cross-project consumers belong in the impact map; they do not create a second
canonical owner.

## Review Lifecycle

Use these states in the issue body or project tracking:

`backlog -> ready -> source-audited -> skill-updated -> locally-proven -> approved`

Use one terminal exception when needed:

- `blocked-by-platform-gap`: a real contract gap prevents correct guidance.
- `superseded`: another skill or issue owns the same canonical knowledge.

## Definition Of Done

A skill review is complete only when:

- the relevant `AGENTS.md`, public API, implementation, specs, docs, manifests,
  examples, and direct consumers were considered;
- observed gaps were classified as `ja-suportado-so-ux`,
  `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or
  `lacuna-real-de-contrato`;
- the skill routes to canonical owners and rejects unjustified local contracts;
- skill files, metadata, dependencies, and manifest hashes are consistent;
- structural preflight passes;
- a happy path, risk/edge case, and adversarial scenario were exercised;
- the smallest reliable local platform validation passed;
- commands, results, limitations, and unexecuted validations are recorded;
- a PR or commit is associated with the issue;
- the final audit classifies the result as `aprovada-com-evidencia`,
  `implementada-sem-auditoria-funcional`, `precisa-reabertura`, or
  `skill-desatualizada-por-drift`.

## Execution Order

Prioritize by architectural risk instead of draft filename order:

1. AI semantic intent, core contracts/public API, dynamic fields, dynamic form,
   table, and table rule builder.
2. Charts, page builder, visual builder, metadata editor, and settings.
3. CRUD, dialog, list, rich content, manual form, and editorial forms.
4. Specialized controls and derived documentation/playground surfaces.

Execute batches of three to five skills from the same family. Reuse the source
inventory, but require independent evidence and acceptance for each issue.

## Initial Pilots

| Issue | Skill | Purpose |
| --- | --- | --- |
| #170 | `praxis-ai-semantic-intent` | Prove semantic-routing and adversarial validation. |
| #188 | `praxis-charts-runtime-data` | Prove a complex data/runtime integration review. |
| #195 | `praxis-core-composition-runtime` | Prove a high-impact transversal Angular review. |

Freeze the final issue contract only after all three pilots expose whether the
required evidence is practical and sufficient.

## Retrospective Audit

Audit the ten closed Praxis review issues after the pilots. A closed issue is not
automatically approved when it lacks linked PR, commands, results, or operational
evidence. Preserve valid implementation and create a focused follow-up only when
the missing proof or source drift is material.

## Local Validation

Validate repository governance with:

```bash
python3 scripts/preflight-python-fallbacks.py
```

Each issue must also define the smallest reliable validation in the platform
project it audits. GitHub Actions remains a final gate, not the default feedback
loop for skill review work.
