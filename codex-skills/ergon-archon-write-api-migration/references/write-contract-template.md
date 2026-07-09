# Write Contract Template

## Scope

- Screen:
- Resource:
- Operation: create / update / delete / duplicate / association / related-write
- Strategy: `legacy-routine` / `direct-table-with-triggers` / `java-reimplementation` / `blocked` / `not-api`
- Status: `Ready for audit` / `Ready for write design` / `Ready for implementation` / `Implemented` / `Blocked` / `Deferred` / `Not API`
- Table-rule handoff: `Write API safe to design` / `DB-backed write path required` / `Blocked` / `Deferred`
- Legacy bridge: `existing` / `new shared adapter` / `not needed` / `blocked`

## Entry Gate

| Gate | Required Evidence | Status | Blocker / Deferral |
| --- | --- | --- | --- |
| Discovery and component lineage | `closure-checklist.md`, `component-lineage-matrix.md`, `operation-inventory.md`, `write-api-handoff.md` |  |  |
| Read API / read-first behavior | read endpoint tests, read smoke/parity, blocked-write behavior for unsupported operations |  |  |
| Table-rule audit | summaries for target and side-effect tables, HADES/EP/C_ERGON/generator coverage, nested dependency graph |  |  |
| Praxis DTO/FieldSpec review | `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` decisions |  |  |
| Java host review | `praxis-java-host-project` decision and host convention |  |  |
| Option-source review | `praxis-resource-entity-lookup-backend` decision when payload/actions need governed options |  |  |
| Mutation approval | named screen/resource/marker/operations/cleanup/exclusions approved before mutating probes or API smokes |  |  |

## Legacy Evidence

| Evidence | Location | Confidence | Notes |
| --- | --- | --- | --- |
| XML write component |  |  |  |
| Routine/table |  |  |  |
| Trigger/package |  |  |  |
| Table-rule audit |  |  |  |
| EP/HADES gate |  |  | Include `HAD_CAD_SPROC`, `HAD_CAD_MULT_EPS`, active/inactive branch, and preserved hook decision |
| Runtime browser behavior |  |  |  |
| Runtime payload capture |  |  | Include operation selector, hidden keys, `PB_*`, `PP_*`, `P_MENS`, and side fields |
| Oracle metadata output |  |  |  |
| Positive write probe |  |  | Include final cleanup proof if fixture persists beyond rollback |
| Negative write probes |  |  | Include invalid payload, missing required field, duplicate/collision, no permission, and no-mutation proof |
| API write smoke |  |  | Include request/response JSON, readback, Oracle counts, and cleanup proof |

## Table Rule Coverage

| Table | Rule / Source | Order | Active? | Nested Dependencies | Covered By Write Path | Decision |
| --- | --- | ---: | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## API Contract

- Method/path:
- Path variables:
- Request DTO:
- Response DTO:
- Success HTTP status:
- Error shape:
- Authorization:
- Session context:
- Transaction boundary:
- Rollback / partial-mutation behavior:
- Retry / idempotency behavior:
- Legacy route:
- Error translation:

## Praxis Skill Review

| Skill/review | Scope | Decision | Evidence |
| --- | --- | --- | --- |
| `praxis-dto-annotations` | command DTO, request/response DTO, `@Schema`, `@UISchema`, `@Filterable`, `x-ui`, `/schemas/filtered` | `applied` / `not applicable` / `blocked` |  |
| `ergon-fieldspec-ui-contract` | FieldSpec/Angular schema consumption, actions, capabilities, command metadata | `applied` / `not applicable` / `blocked` |  |
| `praxis-java-host-project` | resource/controller/service structure to be created or changed in Phase 6 | `applied` / `not applicable` / `blocked` |  |
| `praxis-resource-entity-lookup-backend` | governed option sources in payloads, duplicate drafts, related resources, or action metadata | `applied` / `not applicable` / `blocked` |  |

Do not mark this contract `Ready for implementation` if command DTOs or public
schema metadata changed and `praxis-dto-annotations` was not applied or blocked
with a concrete owner/action.

## Payload Map

| API Field | Java Type | Legacy Field / Arg | Required | Validation | Default | Notes |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Runtime Payload Evidence

| UI Action | Operation Selector | Hidden/Public Keys | Legacy Args Sent | Args Derived Server-Side | Args Omitted/Defaulted | Confirmation / Validation |
| --- | --- | --- | --- | --- | --- | --- |
| Novo |  |  |  |  |  |  |
| Editar |  |  |  |  |  |  |
| Apagar |  |  |  |  |  |  |
| Duplicar |  |  |  |  |  |  |
| Salvar |  |  |  |  |  |  |
| Cancelar |  |  |  |  |  |  |

## Side Effects

| Side Effect | Legacy Source | Active? | Preserved By | Verification |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Legacy Transaction Semantics

| Route | Self-commit / autonomous transaction risk | Rollback reliable? | Cleanup required? | Evidence |
| --- | --- | --- | --- | --- |
|  | Unknown / Yes / No | Unknown / Yes / No | Unknown / Yes / No |  |

## Legacy Outcome Classification

Classify each write scenario after probing Oracle side effects. Do not infer outcome from HTTP status alone.

| Scenario | Outcome | Target row effect | Pending/audit/publication effect | Evidence |
| --- | --- | --- | --- | --- |
|  | `APPLIED` / `PENDING_CREATED` / `BLOCKED_BY_LEGACY_ERROR` / `UNKNOWN` |  |  |  |

## Dependency And Cleanup Plan

| Fixture / Dependency | Setup Route | Expected Blocker | Cleanup Route | Final Probe |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Document any technical cleanup mechanism such as `PACK_TRG_STAT` as test-fixture cleanup only. Do not make it part of the production endpoint unless the legacy UI route itself proves that behavior.

## Error Probe Summary

| Probe | Legacy Result | Mutation? | API Mapping | Evidence |
| --- | --- | --- | --- | --- |
| invalid payload |  | none |  |  |
| missing required field |  | none |  |  |
| duplicate/collision |  | first row only / none |  |  |
| no permission |  | none |  |  |

If a probe returns a raw Oracle error for business-invalid input, record it here and map it to a stable API response. Add Java pre-validation where the invalid field is deterministic, but do not replace the chosen DB-backed route for valid writes.

## Implementation Decision

State why this operation is safe to implement now, or why it remains blocked.
If blocked or deferred, name the owning phase/skill and the smallest concrete evidence needed to reopen the decision. Do not replace the missing evidence with a parallel API, UI-only workaround, direct repository write, or command DTO invented from PL/SQL arguments.

## Pilot Closure

If this is a limited pilot slice, list:

- cases closed by API smoke;
- cases intentionally deferred from the pilot;
- exact future evidence needed for every deferred case;
- whether backend handoff may proceed or must remain blocked.
