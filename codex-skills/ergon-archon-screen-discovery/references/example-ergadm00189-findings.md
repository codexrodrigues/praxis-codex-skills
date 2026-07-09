# Example Findings: ERGadm00189

This is an example based on checked-in XML and local view source. Browser runtime and Oracle metadata must still be confirmed before promoting these findings to implementation-ready status.

## Screen

- Code: `ERGadm00189`
- Title: `Frequencias` in migration docs; XML title is `Frequências`.
- Module: `Administracao`
- Investigation mode: `Quick discovery`
- Browser status: `Missing`
- Oracle status: `Missing`
- Local XML: `docs-legado/v7x/java/techne-archon-ergon/src/main/resources/techne/archon/ergon/crodata/trans/Administracao/ERGadm00189.xml`
- Local view source: `docs-legado/v7x/aps/fontes_ergon/ergadm00189_frequencias.vw`

## Confirmed XML Evidence

The page declares parameters:

```text
pNumfunc
pNumvinc
```

The screen title is defined in XML line 10 as `Frequências`.

Main pending-records grid:

```sql
select texto_link, sis, trans, usuario
from table(erg_mostra_regpend ('FREQUENCIAS_PND', ?, ?, NULL, NULL, NULL, NULL))
```

Parameters:

```text
#blk001.srcServidores#, #blk001.drpVinculo#
```

Main frequency grid `grdConsultas`:

```sql
SELECT f.*
FROM ergadm00189_frequencias f
WHERE pack_hades.eh_concomitante(nvl(f.dtini,pack_had_util.data_minima),
                                 nvl(f.dtfim, pack_ergon.data_maxima),
                                 nvl(?, pack_had_util.data_minima),
                                 nvl(?, pack_ergon.data_maxima)) = 1
  and f.numfunc = ?
  and f.numvinc = ?
  and f.tipofreq = nvl(?, f.tipofreq)
  and f.codfreq = nvl(?, f.codfreq)
  and mostra_freq(flag_pack.get_usuario,f.tipofreq,f.codfreq) = 1
order by f.dtini desc
```

Parameters:

```text
#dtbIni#, #dtbFim#, #blk001.srcServidores#, #blk001.drpVinculo#, #srcTipoFreq#, #srcCodfreq#
```

Observed tabs and related areas in XML:

- `Detalhes`: master record panel over `grdConsultas`.
- `Publicacoes`: loads `pontpubl` from `FREQUENCIAS` by `rowid`.
- `Documentos legais`: loads `PONTLEI` from `FREQUENCIAS` by `rowid`.

Write behavior exists in XML:

```text
recordPanelEdit rotina = db:erg_dml_freq_formato
onEnterEdit checks $grdConsultas.permissao_usu$
onEnterInsert blocks insert when #blk001.drpVinculo# is null, -1, or empty
onDelete calls Techne.Archon.anulaAto('blkAnulaAtos')
```

Treat this screen as read/write risk until `erg_dml_freq_formato`, triggers, grants, defaults, and pending-record behavior are confirmed.

## Confirmed Local Source Evidence

Local view source defines:

```sql
create or replace force view ergadm00189_frequencias as
...
from FREQUENCIAS f,
     codigos_freq cf
where f.tipofreq = cf.tipofreq
  and f.codfreq = cf.codigo
```

The local view exposes:

- `ROWIDTOCHAR(f.ROWID) ROWID_REG`
- `HAD_FORMATA_PUBLICACOES(f.PONTPUBL) TEXTO_PUBL`
- `ergadm_formata_qtd(cf.formato_qtd, f.QUANTIDADE) qtd_formatada`
- `ERGADM_PERFIL_FREQ(...)` derived profile flags
- `mostra_freq(flag_pack.get_usuario,f.tipofreq,f.codfreq)` as `PERMISSAO_USU`
- lookup descriptions from `TIPO_FREQ` and `CODIGOS_FREQ`

## Object Inventory

| Owner | Object | Type | Role | Confidence | Evidence |
| --- | --- | --- | --- | --- | --- |
| expected `ERGON` | `ERGADM00189_FREQUENCIAS` | view | `screen_view` | `CONFIRMED_XML` and `CONFIRMED_LOCAL_SOURCE` | XML main grid; local `.vw` source |
| expected `ERGON` | `FREQUENCIAS` | table | `domain_table` | `CONFIRMED_LOCAL_SOURCE` | local view source and tab SQL |
| expected `ERGON` | `CODIGOS_FREQ` | table | `lookup/domain_table` | `CONFIRMED_LOCAL_SOURCE` | local view source and controller SQL |
| expected `ERGON` | `TIPO_FREQ` | table | `lookup` | `CONFIRMED_LOCAL_SOURCE` | local view source and type search |
| expected `HADES` or effective owner pending | `PACK_HADES` | package | `security_helper` | `CONFIRMED_XML` | `eh_concomitante`, `GET_OPCAO` |
| expected `ERGON` or effective owner pending | `PACK_ERGON` | package | `security_helper` | `CONFIRMED_XML` | `data_maxima` |
| expected owner pending | `PACK_HAD_UTIL` | package | `security_helper` | `CONFIRMED_XML` | `data_minima` |
| expected owner pending | `FLAG_PACK` | package | `security_helper` | `CONFIRMED_XML` and `CONFIRMED_LOCAL_SOURCE` | current user and transaction |
| expected owner pending | `MOSTRA_FREQ` | function | `security_helper` | `CONFIRMED_XML` and `CONFIRMED_LOCAL_SOURCE` | row visibility/edit permission |
| expected owner pending | `PCK_FREQUENCIAS` | package | `security_helper` | `CONFIRMED_XML` | edit search filters |
| expected owner pending | `ERG_DML_FREQ_FORMATO` | routine | `candidate` | `CONFIRMED_XML` | write routine; metadata pending |
| expected owner pending | `ERG_MOSTRA_REGPEND` | function | `related_screen_view` | `CONFIRMED_XML` | pending records grid |
| expected `HADES` or effective owner pending | `HAD_FORMATA_PUBLICACOES` | function | `document_or_audit` | `CONFIRMED_LOCAL_SOURCE` | local view source |
| expected owner pending | `ERGADM_FORMATA_QTD` | function | `lookup` | `CONFIRMED_LOCAL_SOURCE` | local view source |
| expected owner pending | `ERGADM_PERFIL_FREQ` | function | `security_helper` | `CONFIRMED_LOCAL_SOURCE` | local view source |

## View Lineage

```text
ERGadm00189.grdConsultas SQL
  -> ERGADM00189_FREQUENCIAS
     -> FREQUENCIAS
     -> CODIGOS_FREQ
     -> TIPO_FREQ lookup expression
     -> security/helpers: MOSTRA_FREQ, FLAG_PACK, PACK_HADES, PACK_ERGON, PACK_HAD_UTIL
```

## Related Flows

| From | Action | Destination | Parameters | Confidence |
| --- | --- | --- | --- | --- |
| `grdConsultas.fldAtosIndiv` | publication/acts popup | `Administracao.ERGadm00246` | `'FREQUENCIAS', 'ERGadm00189', pontpubl, rowid_reg, null, 'Ergon'` | `CONFIRMED_XML` |
| `grdREGPEND.fldTexto_link` | pending record popup | `Administracao.ERGadmREGPEND` | servidor, vinculo, pending transaction, `FREQUENCIAS_PND`, title | `CONFIRMED_XML` |
| `Publicacoes` tab | publication block | `component/HADadm_blk001` | `rowid_reg`, `FREQUENCIAS`, servidor, vinculo | `CONFIRMED_XML` |
| `Documentos legais` tab | legal docs block | `component/ERGadm_blk004` | `rowid_reg`, `FREQUENCIAS` | `CONFIRMED_XML` |
| `ERGadm00215` calendar | navigation candidate | `ERGadm00189` when table is `FREQUENCIAS` | generated by `erg_gera_calend_freq` | `CONFIRMED_XML` in related screen |
| `ERGadm00314`, `ERGadm00317`, `ERGadm00324` | toolbar/navigation candidate | `Administracao.ERGadm00189` | servidor/vinculo context | `CONFIRMED_XML` in related screens |

## API Candidates

These are candidates only; do not mark `Required Now` until browser runtime and Oracle metadata are confirmed.

```text
GET /api/admin/servidores/{numfunc}/vinculos/{numvinc}/frequencias
GET /api/admin/servidores/{numfunc}/vinculos/{numvinc}/frequencias/{frequencyKey}
GET /api/admin/servidores/{numfunc}/vinculos/{numvinc}/frequencias/pendencias
GET /api/admin/frequencias/tipos
GET /api/admin/frequencias/tipos/{tipofreq}/codigos
```

Potential write endpoints are blocked until `erg_dml_freq_formato`, key strategy, authorization, pending-record behavior, and triggers are understood.

## Blocking Questions

- Browser: confirm menu search path, default load behavior, page size, visible buttons, and whether edit/delete/new are enabled for the demo user.
- Runtime: capture actual values for `pNumfunc`, `pNumvinc`, date filters, type, and code filters.
- Oracle: resolve synonyms/effective owners for all seed objects.
- Oracle: expand `ERGADM00189_FREQUENCIAS` from metadata and compare to local `.vw` source.
- Oracle: inspect `ERG_DML_FREQ_FORMATO`, table triggers on `FREQUENCIAS`, grants, defaults, constraints, and indexes.
- API: decide stable public key. `ROWID_REG` is a legacy internal key and should not be exposed unless explicitly justified.

## Gates

| Gate | Status | Evidence | Blocks |
| --- | --- | --- | --- |
| Observed | Missing | Browser not exercised | Runtime values and visible permissions |
| Resolved | Missing | Synonyms not queried | Effective owners |
| Expanded | Partial | Local view source found | Oracle metadata confirmation |
| Write-risk checked | Partial | XML shows write routine | Routine, triggers, grants, defaults |
| False-positive checked | Partial | Seed list derived from XML/local source | Oracle source search |
| Confirmation SQL complete | Missing | Not generated in this example | Database handoff |
| API-ready | Blocked | Key/write/scope unresolved | Browser and Oracle confirmation |
