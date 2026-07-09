# Case Pilot: ERGadm00033 Write Migration

Use this case to validate the write API migration skill after the first read-first phase.

## Current Migrated State

Historical UI state, not part of current workflow:

- Path: `ui-administracao-pessoal/src/app/Ergon/Administracao/ERGadm00033`
- Main table uses `resourcePath="tipos-frequencia"`.
- Detail form uses `resourcePath="tipos-frequencia"`.
- Codes tab uses `resourcePath="codigos-frequencia"`.
- `writeEnabled = false`.
- UI buttons exist for `Editar`, `Apagar`, `Novo`, `Duplicar`, `Salvar`, and `Cancelar`, but save/delete paths display blocked/read-only messages.

Backend:

- `TipoFrequenciaController` extends `AbstractResourceController`.
- `TipoFrequenciaResourceService` implements `BaseResourceService`.
- `TipoFrequenciaDto` and `TipoFrequenciaFilterDto` define read-first metadata.
- `TipoFrequencia` maps view `ERGON.ERGADM00033_TIPOFREQ` and is `@Immutable`.
- `TipoFrequenciaResourceService.save`, `update`, and `deleteById` return 405 through read-only behavior.
- Similar read-first pattern exists for `CodigoFrequenciaResourceService`.

## Legacy Evidence

Screen XML:

- XML file: `docs-legado/v7x/java/techne-archon-ergon/src/main/resources/techne/archon/ergon/crodata/trans/Administracao/ERGadm00033.xml`
- Main grid SQL reads `ERGADM00033_TIPOFREQ`.
- Detail section has `component/recordPanelEdit` named `rece`.
- `recordPanelEdit` has `dataTable="TIPO_FREQ_"`.
- `duplicateEnabled="true"`.
- Related codes tab reads `ERGADM00034_CODFREQ` filtered by selected type and company.
- Company selector uses special values such as all/general and no company association.

Legacy PL/SQL/source:

- `docs-legado/v7x/aps/fontes_ergon/pck_tipo_freq.pks`
- `docs-legado/v7x/aps/fontes_ergon/pck_tipo_freq.pkb`
- `docs-legado/v7x/aps/fontes_ergon/pck_tipo_freq_empresa.pks`
- `docs-legado/v7x/aps/fontes_ergon/pck_tipo_freq_empresa.pkb`
- `docs-legado/v7x/aps/tipo_freq_.tab`
- `docs-legado/v7x/aps/tipo_freq_empresa.tab`

Important behavior found locally:

- `PCK_TIPO_FREQ` is used by triggers on `TIPO_FREQ`.
- `MAIN_PRE` and `MAIN_POS` receive operation type `I`, `U`, or `D`.
- Validation: `percentual_extra` cannot be set when `hora_extra != 'S'` (`ergon_erro_pack.trata_erro(9516)`).
- Delete of a type deletes `TIPO_FREQ_EMPRESA` for the current company using `FLAG_PACK.GET_EMPRESA`.
- Insert of a type inserts `TIPO_FREQ_EMPRESA` for the current company using `FLAG_PACK.GET_EMPRESA`.
- Generated object setup uses `ERG_GERA_OBJETOS_TABELA(... P_TABELA => 'TIPO_FREQ_', P_GERA_TRG_DML => TRUE ...)`.
- `TIPO_FREQ_EMPRESA` also has generated trigger/package pattern.

## Why This Is A Good Write Pilot

ERGadm00033 is narrower than ERGadm00189:

- Primary business entity is a catalog/type record.
- Read API already exists.
- UI already has blocked write affordances.
- Write behavior is still non-trivial because table triggers/packages manage validation and company association.

This makes it a good first `Legacy-backed Write API` candidate, but not a direct CRUD candidate.

## Initial Write Strategy Hypothesis

Preferred first investigation:

- Keep read model over `ERGADM00033_TIPOFREQ`.
- Create command DTOs for type writes instead of reusing the read DTO blindly.
- Resolve public id `valor|tipo` to target row and any legacy row key server-side.
- Avoid direct writes to the view.
- Investigate whether Java should call generated DML routines, table DML with generated triggers, or a discovered Archon `db:*` routine.
- Run `ergon-table-rule-audit` for `TIPO_FREQ_` and `TIPO_FREQ_EMPRESA` before deciding the write path.
- Set `FLAG_PACK` company/user/transaction context on the same connection before write.
- Preserve trigger behavior for `TIPO_FREQ_EMPRESA`.

## Required Checks Before Implementing

Oracle metadata:

- Effective owner and object type for `TIPO_FREQ_`, `TIPO_FREQ`, `TIPO_FREQ_EMPRESA`, and view `ERGADM00033_TIPOFREQ`.
- Triggers on `TIPO_FREQ_` and `TIPO_FREQ_EMPRESA`.
- Generated DML procedure names and arguments, if present.
- Grants for the API schema/user.
- Constraints, indexes, defaults, and nullability.
- Source references for `PCK_TIPO_FREQ`, `PCK_TIPO_FREQ_EMPRESA`, `ERGON_ERRO_PACK`, `FLAG_PACK`, and extension packages.
- Table-rule audit reports for `TIPO_FREQ_` and `TIPO_FREQ_EMPRESA`, including generated infrastructure, active HADES/C_ERGON client hooks, execution order, and migration decision per rule.

Runtime/browser:

- Whether legacy edit/new/delete/duplicate are enabled for the same user/company.
- Required fields and field enablement.
- Save validation messages.
- Delete confirmation behavior.
- Duplicate default values.

Java:

- Whether current `@Immutable` entity remains read-only and write uses a separate query/command path.
- Whether write endpoints should live on `TipoFrequenciaController` or a dedicated command service under the same resource.
- Whether `TipoFrequenciaIdConverter` handles all write path ids.
- How read-after-write refreshes the dynamic form/table.

## Candidate Write Operations

| Operation | API Candidate | Initial State | Notes |
| --- | --- | --- | --- |
| Create type | `POST /tipos-frequencia` | Candidate | Requires company context and insert side effect into `TIPO_FREQ_EMPRESA`. |
| Update type | `PUT /tipos-frequencia/{id}` | Candidate | Must preserve trigger validation and reject key changes unless explicitly supported. |
| Delete type | `DELETE /tipos-frequencia/{id}` | Candidate/Blocked | Must check references from codes/frequencies and company association semantics. |
| Duplicate type | `POST /tipos-frequencia/{id}/duplicate` or create with source | Candidate | Legacy defaults must be captured first. |

## Required Parity Cases

- Insert with `horaExtra='S'` and valid `percentualExtra`.
- Insert/update with `percentualExtra` and `horaExtra!='S'` returns equivalent validation error.
- Insert creates current-company association.
- Delete removes current-company association as legacy does.
- Delete with dependent codes/frequencies either fails or cascades according to legacy behavior.
- Update preserves same visibility in `ERGADM00033_TIPOFREQ`.
- No-permission user receives access error.
- Same public id can be read after write through existing `/filter` or detail endpoint.
