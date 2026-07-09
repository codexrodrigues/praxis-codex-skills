# Example API Contract: ERGadm00189 Frequências

This is a filled example for the first read-first API slice. Use it as a model, not as proof for every environment. Promote fields to `Required Now` only when the screen package has browser/XML/Oracle evidence.

## Migration Scope

- Screen: `ERGadm00189`
- Title: `Frequências`
- API phase: `read-first`
- Included flows: main frequency list, type/code lookups, selected-record read candidate, schema discovery
- Deferred flows: create, edit, delete, duplicate, pending records, publications, legal documents
- Blocking decisions: stable detail key, write stack closure, publication/legal tab scope
- Source artifacts: `component-lineage-matrix.md`, `closure-checklist.md`, `write-risk.md`, Oracle metadata output

## Current Slice Recommendation

| Endpoint | Status | Reason |
| --- | --- | --- |
| `POST /frequencias/filter` | `Required Now` when read gates are closed | Main grid/list for the migrated screen. |
| `GET /frequencias/{idReg}` | `Candidate` | Use only after `ID_REG` uniqueness, authorization, and not-found behavior are confirmed. |
| `GET /frequencias/by-ids` | `Candidate` | Needed for selected-row rehydration if detail/read panel uses stable ids. |
| `POST /frequencias/options/filter` | `Candidate` | Only if frequencies themselves are reused as options. |
| `POST /tipos-frequencia/options/filter` | `Required Now` | Type lookup/filter. Reuse existing resource if present. |
| `POST /codigos-frequencia/options/filter` | `Required Now` | Code lookup/filter dependent on type. Reuse existing resource if present. |
| `GET /frequencias/schemas` | `Required Now` | Schema discovery for generated UI. |
| `POST/PUT/DELETE /frequencias` | `Blocked` | Generated DML, triggers, pending, audit, publication, legal docs, and session context not closed. |

Do not expose `/ergadm00189-frequencias` or `ROWID_REG` as public resource design. They are implementation evidence.

## Target App Integration

| File / Area | Required Change |
| --- | --- |
| `ApiEndpoints.java` | Add or reuse `FREQUENCIAS_PATH`, `FREQUENCIAS_GROUP`, `FREQUENCIAS_TAG`; check existing type/code resources before adding new lookup paths. |
| `SwaggerConfig.java` | Add/reuse `GroupedOpenApi` for the frequencies group. |
| `SwaggerValidationConfig.java` | Confirm schema validation/logging includes the new group. |
| `application.yaml` | Confirm context path, springdoc path, datasource/profile, and `uifieldspec` settings. |
| Controllers | Prefer `AbstractResourceController` for the main resource. |
| Services | Use `BaseResourceService` boundary; custom Oracle SQL/JDBC is acceptable behind it. |
| DTOs/FilterDTOs | PT-BR labels and explicit x-ui metadata. |
| Tests/scripts | Add OpenAPI/x-ui assertions for filters, options, labels, and unsupported writes. |

## Resource Contract

| Item | Decision |
| --- | --- |
| Resource path | `/frequencias` or module-prefixed equivalent from app convention |
| Controller base | `AbstractResourceController<FrequenciaReadModel, FrequenciaDto, Long, FrequenciaFilterDto>` |
| Service base | `BaseResourceService` boundary with custom Oracle query if needed |
| Entity/read model | View/read projection over `ERGADM00189_FREQUENCIAS` or equivalent SQL |
| DTO | `FrequenciaDto` |
| FilterDTO | `FrequenciaFilterDto extends GenericFilterDTO` |
| ID type | `Long` if `ID_REG` is confirmed unique; otherwise `Candidate` |
| Response envelope | `RestApiResponse` |
| Default sort | `dtini desc` plus deterministic tie-breaker such as `idReg desc` when available |
| Schema URLs | `/schemas/filtered` for request and response schemas |

## DTO Field Map

| Field | JSON Type | Source | UI Metadata | Notes |
| --- | --- | --- | --- | --- |
| `idReg` | number | `ID_REG` | hidden/read-only | Candidate public id after uniqueness proof. |
| `rowidReg` | string | `ROWID_REG` | hidden/internal | Do not expose in public URLs. Needed only for legacy routine/tabs if accepted. |
| `inicio` | date | `DTINI` | label `Início`, date control | Grid/detail date. |
| `termino` | date | `DTFIM` | label `Término`, date control | Nullable end date. |
| `tipoFrequencia` | string | `TIPOFREQ` | label `Tipo de frequência`, select | Use option resource. |
| `codigoFrequencia` | string | `CODFREQ` | label `Código de frequência`, dependent select | Depends on type. |
| `nome` | string | lookup/view expression | label `Nome`, read-only | Display description. |
| `quantidade` | number | `QUANTIDADE` | numeric control | Preserve precision/format. |
| `quantidadeFormatada` | string | `QTD_FORMATADA` | read-only/table display | Display-only when legacy format matters. |
| `observacao` | string | `OBSERVACAO` or equivalent | textarea | Confirm exact source/length. |
| `canEdit` | boolean | permission expression | hidden or capability field | Expose only if the API deliberately publishes dynamic action state. |

## FilterDTO Example

```java
@Schema(name = "FrequenciaFilter", description = "Filtros de frequências")
public class FrequenciaFilterDto extends GenericFilterDTO {

    @UISchema(
        label = "Período",
        type = FieldDataType.DATE,
        controlType = FieldControlType.DATE_RANGE,
        filterable = true
    )
    private List<LocalDate> periodo;

    @UISchema(
        label = "Tipo de frequência",
        controlType = FieldControlType.SELECT,
        endpoint = "/tipos-frequencia/options/filter",
        displayField = "displayField",
        filterField = "displayField",
        optionsPageSize = 20
    )
    private String tipoFrequencia;

    @UISchema(
        label = "Código de frequência",
        controlType = FieldControlType.SELECT,
        endpoint = "/codigos-frequencia/options/filter",
        displayField = "displayField",
        filterField = "displayField",
        dependencyFields = {"tipoFrequencia"},
        resetOnDependentChange = true,
        optionsPageSize = 20
    )
    private String codigoFrequencia;
}
```

The annotations above are UI/schema contract. The service must still translate the fields to the legacy predicates.

## Filter Implementation Map

| FilterDTO Field | Legacy Field | UI Control | Payload Shape | Backend Implementation | Null/Default Behavior | Parity Case |
| --- | --- | --- | --- | --- | --- | --- |
| `periodo` | `Início` + `Término` | `dateRange` | Confirm `start/end` versus array from current UI | Use legacy overlap/concomitance predicate such as `pack_hades.eh_concomitante`, not naive `BETWEEN` unless equivalent | Open start/end maps to legacy min/max dates | Compare default list, start-only, end-only, closed period |
| `tipoFrequencia` | `Tipo de frequência` | select | scalar code | `tipofreq = nvl(:tipo, tipofreq)` equivalent plus authorization | Null means all visible types | Filter by one existing type |
| `codigoFrequencia` | `Código de frequência` | dependent select | scalar code | `codfreq = nvl(:codigo, codfreq)` and enforce parent type if sent | Null means all visible codes for type/scope | Filter by code with and without type |

## Lookup Contracts

| Lookup | Endpoint | Behavior |
| --- | --- | --- |
| Tipo de frequência | `POST /tipos-frequencia/options/filter` | Returns `OptionDTO<String>` with code as value and PT-BR display text. Apply current user/scope rules if legacy lookup does. |
| Código de frequência | `POST /codigos-frequencia/options/filter` | Returns `OptionDTO<String>` filtered by `tipoFrequencia`; backend enforces dependency even if the client omits metadata. |
| Rehydrate selected types/codes | `GET /options/by-ids` | Returns selected options preserving requested ids where project convention supports it. |

## Business Implementation Map

| Behavior | Legacy Evidence | Java Layer | Decision |
| --- | --- | --- | --- |
| Main list | XML SQL over `ERGADM00189_FREQUENCIAS` | service/query object | Custom SQL/JDBC or projection preserving legacy predicates. |
| Period overlap | `pack_hades.eh_concomitante` pattern | query object | Manual predicate mapping. |
| Row visibility | `mostra_freq(flag_pack.get_usuario, ...)` | service/query plus Oracle context | Same-connection context required if package state is used. |
| Type/code options | lookup SQL/tables | lookup service | Reuse existing resources when possible. |
| Writes | `ERG_DML_FREQ_FORMATO` and generated stack | blocked | Do not expose write endpoints in read-first slice. |

## Capability And Write State

| Capability | API Decision |
| --- | --- |
| `canCreate` | Candidate/block until access flags and write stack are closed. |
| `canEdit` | Candidate for UI button state; not permission to expose `PUT`. |
| `canDelete` | Blocked with write-risk evidence. |
| `canDuplicate` | Blocked with write-risk evidence. |
| Publications/legal documents | Candidate related flows, not part of first slice unless scoped. |

## Error Semantics

| Case | HTTP / Behavior |
| --- | --- |
| Empty frequency list | `200` with empty page/items |
| Invalid date range | `400` validation error |
| Unknown type/code | `400` or empty result according to existing app convention; document decision |
| No access to servidor/vínculo/scope | `403` |
| Detail id not found | `404` |
| Write in read-first phase | disabled/omitted endpoint or project-standard `405`/`501` |

## Required Tests

| Check | Expected |
| --- | --- |
| `/v3/api-docs/{group}` | Group exists and contains frequency paths. |
| `/schemas/filtered` request schema | `periodo` has `x-ui.controlType=dateRange`; type/code have select metadata. |
| `POST /filter` default | Matches legacy default list order and visible rows for same user/scope. |
| `POST /filter` with period | Matches legacy start/end behavior. |
| `POST /filter` with type/code | Matches legacy filters and dependent behavior. |
| `/options/filter` type/code | Returns `OptionDTO` shape and PT-BR labels. |
| Unsupported writes | Intentional disabled/501/405 behavior. |

## Parity Matrix

| Case | Legacy Action Or Query | API Request | Expected |
| --- | --- | --- | --- |
| Default list | Open screen after selecting servidor/vínculo | `POST /frequencias/filter` with required scope | Same rows, order, key fields. |
| Period filter | Set `Início`/`Término` in screen | `periodo` filter | Same overlap semantics. |
| Type filter | Select `Tipo de frequência` | `tipoFrequencia` filter | Same visible rows. |
| Code filter | Select `Código de frequência` | `codigoFrequencia` filter | Same visible rows. |
| Empty result | Choose filter with no matches | filter request | Empty page/items. |
| No access | User/scope without permission | filter/detail request | `403` or project access error. |
| Deferred write | Click legacy edit/new/delete only for evidence | no write endpoint or unsupported write | API remains blocked/deferred. |
