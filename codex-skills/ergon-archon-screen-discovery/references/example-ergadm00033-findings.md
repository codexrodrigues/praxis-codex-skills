# Example Findings: ERGadm00033

This is an example, not a global rule. Re-confirm every finding when investigating another screen or environment.

## Screen

- Code: `ERGadm00033`
- Title: `Tipos de frequência`
- Main related screen: `ERGadm00034` through links such as `/Ergon/Administracao/ERGadm00034.tp?pSigla=<TIPO>&pFreq=<CODIGO>`

## Confirmed XML/Runtime SQL

Main grid:

```sql
select *
from ERGADM00033_TIPOFREQ
where VALOR = ?
  and (
    busca_searchbox_varchar2('null', null, tipo, nvl(?,' ')) = 1
    or busca_searchbox_varchar2('null', null, nome, nvl(?,' ')) = 1
  )
  and tipo = nvl(?, tipo)
order by tipo
```

Parameters observed:

```text
#drpSelecEmpresa.drpSelecEmpresa#
#txtTipoFreqFiltro#
#txtTipoFreqFiltro#
#txtTipoFreqFiltroParam#
```

Codes tab grid:

```sql
select *
from ERGADM00034_CODFREQ
where tipofreq = ?
  and VALOR = ?
order by codigo
```

Company selector:

```sql
select valor, descr
from SELEC_COMBO_EMPRESA_VW
```

## Object Inventory

| Object | Role | Confidence | Notes |
| --- | --- | --- | --- |
| `ERGON.ERGADM00033_TIPOFREQ` | `screen_view` | `CONFIRMED_XML` | Main grid source |
| `ERGON.TIPO_FREQ_` | `domain_table` | `CONFIRMED_ORACLE_METADATA` | Base type table |
| `ERGON.TIPO_FREQ_EMPRESA` | `scope_table` | `CONFIRMED_ORACLE_METADATA` | Type/company association |
| `ERGON.ERGADM00034_CODFREQ` | `related_screen_view` | `CONFIRMED_XML` | Codes tab and related screen |
| `ERGON.CODIGOS_FREQ_` | `domain_table` | `CONFIRMED_ORACLE_METADATA` | Frequency code table |
| `ERGON.CODIGOS_FREQ_EMPRESA` | `scope_table` | `CONFIRMED_ORACLE_METADATA` | Code/company association |
| `HADES.SELEC_COMBO_EMPRESA_VW` | `lookup` | `CONFIRMED_XML` | Company combo |
| `HADES.EMPRESAS` | `lookup/domain` | `CONFIRMED_ORACLE_METADATA` | Company source |
| `ERGON.CMP3$108058` | `candidate` | `CANDIDATE_UNCONFIRMED` | Matches legal document columns but needs direct evidence |
| `ERGON.CMP4$108058` | `candidate` | `CANDIDATE_UNCONFIRMED` | Matches legal document columns but needs direct evidence |

## View Semantics

`ERGON.ERGADM00033_TIPOFREQ` uses:

```text
VALOR = -2: records without company association
VALOR = -1: general/all records
VALOR = company id: records associated to that company and allowed by access rule
```

Security and session helpers observed:

```text
flag_pack.get_empresa
flag_pack.get_usuario()
acesso_usuario_empresa(...)
```

## Minimal Read API Candidates

Treat as candidates until aligned with the target Java project conventions:

```text
GET /api/admin/tipos-frequencia/empresas
GET /api/admin/tipos-frequencia
GET /api/admin/tipos-frequencia/{tipo}
GET /api/admin/tipos-frequencia/{tipo}/codigos
GET /api/admin/tipos-frequencia/{tipo}/codigos/{codigo}
GET /api/admin/tipos-frequencia/{tipo}/codigos/{codigo}/documentos-legais
```

## Open Questions

- Confirm legal document source from XML/runtime or metadata before implementing.
- Decide whether Oracle session functions remain authoritative for current user/company.
- Decide whether `VALOR=-1/-2` is exposed by the API as raw values or modeled as an enum/scope object.
- Replace `ROWID` with stable natural keys where possible.
