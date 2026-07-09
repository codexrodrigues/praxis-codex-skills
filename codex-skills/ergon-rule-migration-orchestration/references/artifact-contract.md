# Parte 2 Artifact Contract

Use `docs/migracao/<SCREEN>/rule-migration/` for all Parte 2 artifacts.

## Required Central Artifacts

### `rule-migration-intake.md`

Records whether Parte 2 can start.

Required sections:

- target screen and operation scope;
- Parte 1 handoff status;
- required Parte 1 artifacts checklist;
- eligible operations;
- excluded operations;
- baseline parity links;
- current approved baseline route links;
- known rules and audits;
- known errors;
- blocking gaps;
- intake decision;
- return-to-Parte-1 rules.

### `rule-traceability-matrix.md`

Central control surface for all rules.

Required columns:

| Column | Meaning |
| --- | --- |
| Rule | Stable Java-oriented rule id or candidate id. |
| Legacy origin | Package, trigger, procedure, HADES routine, constraint, function, or view. |
| Operation | Create/update/delete/duplicate/read/security/etc. |
| Parte 1 artifact | Exact baseline artifact and section/link. |
| Dependencies | Low/medium/high/unknown plus main dependency refs. |
| HADES/EP/client | Inactive, active, multiple, unknown, not applicable, etc. |
| Side effects | None, audit, pending, publication, legal, workflow, table mutation, unknown. |
| Mode | DB-backed, candidate, shadow, preflight, authoritative, contained, rejected, deferred. |
| Promotion boundary | Exact behavior Java may decide. |
| Still DB-backed | Behavior that remains in the legacy route. |
| Double-execution risk | No, yes, accepted, blocker, unknown. |
| Observability | Where shadow/preflight/promotion events are recorded. |
| Fallback | DB-backed, block, feature flag off, legacy-only, manual rollback, etc. |
| Return to Parte 1 | Phase and trigger condition. |
| Status | Rule-level status from `status-taxonomy.md`. |

### `rule-canonical-decision-inventory.md` - Canonical Decision Inventory

Records whether the target behavior is already represented by Praxis platform
semantics before Parte 2 creates or changes a contract.

Required sections:

- target screen, operation, rule slice, and Parte 1 baseline link;
- existing Praxis metadata/config/API/UI evidence, including schemas,
  capabilities, actions, surfaces, HATEOAS links, config/registry/template
  state, error envelope, feature flag, observability, and consumer UI gates;
- one classification per proposed platform change:
  `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
  `suportado-parcialmente`, or `lacuna-real-de-contrato`;
- canonical owner for each needed change: `praxis-config-starter`,
  `praxis-metadata-starter`, `praxis-ui-angular`, backend API resource,
  migration artifact only, or blocked;
- decision boundary: DB-backed, shadow, preflight, authoritative, retained
  defense, deferred, or blocked;
- explicit statement that no UI, dashboard, workflow, or host-local adapter is
  acting as the primary source of the rule.

## Phase Artifacts

| Artifact | Purpose |
| --- | --- |
| `rule-canonical-decision-inventory.md` | Existing platform knowledge, canonical owner, support classification, and whether a real contract gap exists before new rule contracts are introduced. |
| `rule-inventory.md` | Detailed rules extracted from Parte 1 audits and source. |
| `rule-dependency-graph.md` | Nested calls, packages, functions, tables, HADES, and side-effect graph. |
| `hades-rule-chain.sql` | Read-only SQL used to classify scoped HADES routines. |
| `hades-rule-chain.out.txt` | Raw execution output from SQLcl or JDBC fallback. |
| `hades-rule-chain.md` | Summary of HADES parent rows, multiple-EP children, C_ERGON/ERGON objects, effective classification, execution path, and rule impact. |
| `shadow-contract.md` | Scope, Java rule ids, fixtures, inputs, outputs, comparison, observability, fallback. |
| `shadow-results.md` | Phase 14 implementation/runtime evidence, layered status, comparison limits, and divergence classification. |
| `preflight-decision.md` | Whether Java may block selected cases before the approved Parte 1 baseline route. |
| `create-preflight-precedence-plan.md` | Required for create preflight before the approved baseline route when Java could mask a more specific baseline error; records conflicting cases, expected precedence, evidence, and decision. |
| `structured-error-envelope-decision.md` | Required when preflight/shadow equivalence depends on API error shape; records status, code, legacyCode, fields, ruleId, message policy, and accepted deviations or return to Parte 1 Phase 5. |
| `preflight-runtime-evidence-plan.md` | Planning artifact for a future controlled runtime preflight run: exact boundary, flags, approval gate, rollback, executor/no-baseline proof, ALLOW baseline-route proof, envelope parity, observability, cleanup, and expected `preflight-results.md`. |
| `preflight-implementation-readiness.md` | Technical gate before any preflight code: records whether planning is accepted and whether implementation is explicitly approved or still blocked. |
| `preflight-results.md` | Executed preflight evidence proving feature flag plus operational approval gate, rollback, DENY blocked before baseline route, ALLOW still baseline route, compatible response, no-mutation, cleanup, and observability. |
| `promotion-decision.md` | Whether Java becomes authoritative and for what boundary. |
| `legacy-containment.md` | What happens to the old rule after promotion: retained, bypassed, deactivated, fallback-only, or deliberately duplicated. |
| `final-rule-handoff.md` | Consolidated state of all rules after Parte 2 scope. |

## Phase Gate Artifact

Every phase closeout requires:

`phase-<PHASE-ID>-execution-gate.md`

Required sections:

- phase decision;
- scope;
- evidence executed;
- artifacts updated;
- canonical decision inventory status;
- rule statuses changed;
- residual issues;
- return-to-Parte-1 triggers;
- next recommended phase/skill.

## Preflight Artifact Distinction

- `preflight-decision.md` records `Preflight Candidate`, `Preflight Approved`, or `Preflight Deferred - runtime blocked`: the governance decision that Java may analyze, block, or defer a precise proven case in a future guarded run.
- `preflight-runtime-evidence-plan.md` and `preflight-implementation-readiness.md` record planning-only approval. Planning readiness can move a rule to `Preflight Approved Candidate - planning only`, but it must not be treated as implementation approval or runtime evidence.
- `create-preflight-precedence-plan.md` is mandatory before create runtime preflight if a Java DENY before the approved baseline route could hide duplicate, required-field, missing type/code, quantity/format, period/vinculo, permission/security, dependency, or other baseline errors.
- `structured-error-envelope-decision.md` is mandatory before runtime preflight when the legacy/API envelope is not already fully proven. If the contract changes, return to Parte 1 Phase 5; if deviation is accepted, record formal acceptance.
- `preflight-results.md` records `Preflight Running`: runtime proof that the approved preflight was actually enabled, observed, reversible, and did not change approved baseline-route ownership for allowed cases.
- A DENY preflight proof must show the DB-backed executor/legacy routine was not called. Oracle no-mutation counts are necessary but not sufficient.
- Do not advance to Phase 16 promotion decision using only `preflight-decision.md`. Promotion needs either `preflight-results.md` or an explicit decision to remain preflight-only/deferred.
- Do not classify a shadow/preflight comparison as equivalent from HTTP status alone. Compare actual code/message marker, fields, normalized message, and state/side effects when available; if the real code cannot be extracted, mark the comparison `Inconclusive`.
- Do not enable preflight outside controlled smoke with a single static property. Require a second operational approval gate, target environment allowlist/gate id, or an audited dynamic flag provider that fails closed.
- Controlled smoke is not corporate rollout. Before rollout or promotion, `preflight-results.md` or the phase gate must explicitly close target-environment HADES revalidation, rollback model, structured error envelope, observability status interpretation, and non-smoke observation evidence.
