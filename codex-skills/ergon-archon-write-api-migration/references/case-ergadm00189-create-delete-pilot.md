# ERGadm00189 Create/Delete Write Pilot

Use this case as a compact reference for Ergon screens whose valid writes must go through a legacy PL/SQL routine and whose invalid writes can expose raw Oracle errors.

## Proven Pattern

- Read-first API used public `ID_REG`; `ROWID_REG` stayed internal.
- Write route candidate was `ERGON.ERG_DML_FREQ_FORMATO`, not direct table DML, generic JPA save, or direct `ERG_DML_FREQUENCIAS`.
- Browser `Novo/Salvar` and `Apagar/Sim` were accepted as UI-state plus Oracle mutation/cleanup evidence when raw Ajax payload capture was unavailable.
- Positive insert persisted beyond caller rollback, so cleanup had to call the legacy delete route explicitly.
- The Java write slice kept low-level callable PL/SQL inside the legacy bridge/executor path and left screen-specific command DTO, rowid-to-`ID_REG` resolution, and route policy in the application module.
- API smoke closed the pilot, not just unit tests or PL/SQL probes. The accepted smoke set included success create/delete, invalid quantity, missing required field, duplicate/collision, and create permission denial.
- Every API smoke printed Oracle before/after counts for `FREQUENCIAS` and `FREQUENCIAS_PND`, and every created fixture ended with final zero-count proof.

## Required Probes

For the smallest create/delete slice, capture:

- valid create with disposable fixture and final cleanup proof;
- valid delete of a disposable fixture and final zero-count proof;
- invalid code/no mutation;
- invalid quantity/no mutation, including raw `ORA-06502` if the wrapper leaks it;
- missing required fields/no mutation, including raw errors such as `ORA-01422` when Java should pre-validate;
- duplicate/collision, usually `ORA-00001`, mapped to `409`;
- create permission denial with a real legacy user/profile, mapped to `403`.

Keep delete permission denial, dependency-blocked delete, pending-enabled behavior, publication/legal non-null payloads, update, and duplicate operation as separate gates unless the current slice explicitly includes them.

## Required API Smokes

After Java implementation, run the equivalent API-level smokes and store them under the screen package:

- `api-results/write-create-delete-api-smoke-YYYYMMDD.md` with request/response JSON, returned `ID_REG`, read-after-delete `404`, and Oracle final zero-count proof.
- `api-results/write-negative-api-smoke-YYYYMMDD.md` with invalid quantity `422`, missing required field `422`, duplicate/collision `409`, no-mutation proof, and cleanup proof for the first duplicate row.
- `api-results/write-permission-api-smoke-YYYYMMDD.md` when a denied user fixture exists; for this case, `admin_seg` returned `403` with `ERG-00433` and zero mutation.

Use separate markers and safe dates per case. Run a baseline count before calling the API, then a count after each negative case. For duplicate, create the first row through the API, confirm the second call returns conflict, then delete the first row through the API and prove final counts are zero.

If the app has no production auth mapping yet, a local smoke may set `ERGON_USUARIO_PADRAO` to the denied legacy user, but the artifact must say this is a local fixture and production identity mapping remains separate.

## Error Mapping Lesson

Do not assume every user-invalid input returns an Ergon business code. Raw Oracle errors can be part of observed legacy behavior. The migrated API should normalize them into stable client responses and avoid leaking SQL/package details.

## Cleanup Lesson

Every probe must print before/after counts for the target table and side-effect tables. If the routine creates anything, cleanup through the same legacy route and prove final counts are zero. Do not rely on test transaction rollback for routines that may commit internally or use autonomous behavior.

## Pilot Closure Lesson

Close a pilot slice by separating `Smoke closed` cases from `Deferred` cases in `write-parity-matrix.md`.

For ERGadm00189, the pilot deferred:

- delete permission-denied, because it requires a two-user fixture with row-preservation and privileged cleanup;
- delete outside company/scope;
- dependency-blocked delete;
- pending-enabled behavior;
- publication/legal non-null payloads;
- update;
- duplicate button behavior;
- cancel/no-op parity;
- generic unavailable/context-failure resilience beyond existing unit coverage.

Do not leave these as vague "pending" items. Mark them as explicit deferrals with the required future evidence, so the next developer knows the pilot is closed without mistaking it for full write parity.
