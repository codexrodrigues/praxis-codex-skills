# Payroll financial draft and dependent-resource handoff

This procedure records G4 implementation requirements and inspected candidate
paths. It does not certify an accepted migration, published backend, deployed
host or complete G4. Resolve the current owner source, artifact and evidence
before adopting a candidate method or claiming its operational behavior.

## Inspect the existing contract first

In the platform workspace, consult `docs/engineering/payroll-reactive-p0-p1-20261020/`
(`DECISOES.md`, `FECHAMENTO-R1-R4.md`), `payroll-reactive-p20-20261020/D4-REVISAO.md`
and the current G4 plan/evidence. They fix the pilot's domain choices; a skill must
not invent financial semantics when that evidence is absent or contradictory.

In API Quickstart inspect `ReactiveDeterminationPilotConfiguration`,
`PayrollFinancialEvaluationService`, `PayrollFinancialDomainService`,
`PayrollEventMutationCoordinator`, `PayrollEventReadService`, the exact request
DTOs and operational migrations. In UI Quickstart inspect
`src/app/features/payroll-events/payroll-event-form-host.component.ts` and
`src/app/pages/reactive-determinations-example-page.component.ts` with their
focused specs. Inspect the installed Core/Dynamic Form public API and runtime,
not only framework source or a locally replaced package.

The host owns base discounts, approved-event facts, exact BRL validation,
forecast/scheduling/payment transitions, authorization, locks and all CAS checks.
Preview, write and sandbox use the governed evaluation service; a matching client
output is not financial authority. Preserve forecast, scheduled and confirmed
payment dates as different facts. Pending historical money remains exact decimal
text from authorized original evidence; do not hydrate a currency control with
it or infer discounts, a classified date or an authority from current state.

## Capture before mounting and confirming

- Use a configured, isolated `GenericCrudService.getByIdHttpResponse` reader and
  `readStrongResourceEtag`. Preserve the opaque strong token from that response;
  do not use lookup extras, a synthesized revision or a token refreshed on submit.
- For edit, capture and validate route/body identity, the event ETag and
  `precondicaoFolhaAtual` from the one joined event detail snapshot before mounting.
  Its parent identity must match `folhaPagamentoId`. Pass `initialValue`,
  `resourceId`, the exact PUT request schema/submit URL and `submitResourceVersion`.
  Avoid a second entity read through child `resourcePath`/`readUrl` that could mix
  snapshots. The event ETag is the single `If-Match`; the list contains only parents.
- Create and destination changes require the selected payroll's official GET,
  identity, strong ETag and mutable/reconciled state. Preserve the origin token
  captured with the event. Capture the new destination separately; returning to
  origin reuses the original capture. Reject paid/historical targets. The server
  still enforces current state and the exact affected parent set under locks.
- Cancel/discard obsolete reads by generation, form identity, entity cycle,
  selection and operational session/tenant/environment/API scope. Arm edit
  destination tracking after `entity-hydrated`; create arms after `formReady`.

## Materialize metadata and keep the root invalid until proven

`precondicoesFolhas` belongs to the host request DTO/schema as a typed transport
array of `{folhaPagamentoId, resourceVersion}`. Its hidden/included policy must
come from canonical metadata, with enabled controls. Do not add a local field,
override submit policy or create a generic Angular dependency-token contract.

Use `formReady` to obtain the real schema-derived `FormArray`. Rebuild its items
through `DynamicFormService.createArrayItemGroupFromMetadata` and the array's
`itemSchema.fields`, using `clear`/`push` and controlled emissions. `patchValue`
and reset alone do not resize it. Missing/visible transport metadata blocks the
flow. Check the actual serialized `payloadPreviewChange`, not just raw controls.

Install a persistent root validator for capture state, current identity and the
exact expected parent set. Loading, missing/failed capture, conflict, stale groups
or omitted/tampered serialization must remain INVALID across unrelated changes.
Disabled children, PENDING alone, one-off `setErrors` or `formSubmit stage=before`
are not submission gates. Prove the public submit path cannot bypass the validator.

Reset restores the original captured draft/tokens without GET. A create reset may
reuse only its preserved matching initial capture; otherwise clear/invalidate and
require explicit capture. Conflict retains the draft for comparison and blocks
through reset until explicit reload/review. Never refresh/retry automatically.
Close after success unless the response contract proves a new complete snapshot.

## Prove the handoff without overstating the result

Use real `hasUnsatisfiedReactiveDeterminations` with pending/execution events;
pending ending or `skipped/superseded` alone is not success. Keep prior displayed
values distinguishable from current satisfied results after technical failure.
Financial UI remains in BRL and performs no financial formula.

Start with metadata contracts and focused consumer tests for create/edit/move,
root invalidation, late selection/reset/scope responses, conflict and opaque ETag
serialization. Exercise the installed Dynamic Form runtime and public currency
control at zero, one cent, an integer amount and the domain maximum. Verify one
event detail GET, no origin refresh, both parents on move and only the event ETag
in `If-Match`. For payroll edit, prove base discounts and forecast enter the exact
request while scheduled/confirmed dates remain separate read/action facts.

Mocked HTTP and a consumer build do not prove generated schemas, privileges,
tenant isolation, physical locks, migration triggers or persisted atomicity.
Require authenticated HTTP/UI and assigned Neon proof of stale/foreign-scope
tokens, concurrent event transfer, schedule/pay races, rollback and replay before
accepting those guarantees. Follow `praxis-api-quickstart-operational-proof` for
one-snapshot read authorization and remote evidence custody. Preserve failed cuts
and update public examples/corpus/docs and skill status with the actual evidence.
