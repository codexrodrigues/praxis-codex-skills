-- <SCREEN> write-risk detail.
-- Read-only Oracle metadata/source checks. Do not include credentials in this file.
-- Replace placeholders with XML/runtime-derived routines, tables, triggers, and packages.

set pagesize 500 linesize 260 trimspool on tab off feedback off verify off
set long 200000 longchunksize 32767

prompt == Write routine signatures ==
select owner, package_name, object_name, argument_name, position, sequence,
       data_type, in_out, defaulted
from all_arguments
where owner in ('ERGON','HADES')
  and object_name in ('<WRITE_ROUTINE_1>', '<WRITE_ROUTINE_2>')
order by owner, package_name, object_name, sequence, position;

prompt == Publication arguments on write routines ==
select owner, package_name, object_name, argument_name, position, sequence,
       data_type, in_out, defaulted
from all_arguments
where owner in ('ERGON','HADES')
  and object_name in ('<WRITE_ROUTINE_1>', '<WRITE_ROUTINE_2>')
  and upper(argument_name) like 'PP\_%' escape '\'
order by owner, package_name, object_name, sequence, position;

prompt == Write routine source ==
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and name in ('<WRITE_ROUTINE_1>', '<WRITE_ROUTINE_2>')
order by owner, name, type, line;

prompt == Generated DML evidence in write routines ==
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and name in ('<WRITE_ROUTINE_1>', '<WRITE_ROUTINE_2>')
  and (
    upper(text) like '%HAD_GERA_PROC_DML%'
    or upper(text) like '%DBMS_SQL.BIND_VARIABLE_ROWID%'
    or upper(text) like '%ROWID%'
    or upper(text) like '%TRATA_ERRO%'
    or upper(text) like '%PP\_%' escape '\'
  )
order by owner, name, type, line;

prompt == Write target triggers ==
select owner, trigger_name, table_owner, table_name, status,
       triggering_event, trigger_type
from all_triggers
where table_owner in ('ERGON','HADES')
  and table_name in ('<TARGET_TABLE_1>', '<TARGET_TABLE_2>')
order by table_owner, table_name, trigger_name;

prompt == Write target trigger source ==
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and name in ('<TRIGGER_1>', '<TRIGGER_2>', '<TRIGGER_3>')
order by owner, name, type, line;

prompt == Generated trigger and table package candidates ==
select owner, object_name, object_type, status
from all_objects
where owner in ('ERGON','HADES')
  and object_name in (
    'T_BS_IUD_<TARGET_TABLE_1>',
    'T_B_IUD_<TARGET_TABLE_1>',
    'T_A_IUD_<TARGET_TABLE_1>',
    'PCK_<TARGET_TABLE_1>',
    '<TARGET_TABLE_1>_PND',
    'PCK_<TARGET_TABLE_1>_PND',
    'T_BS_IUD_<TARGET_TABLE_2>',
    'T_B_IUD_<TARGET_TABLE_2>',
    'T_A_IUD_<TARGET_TABLE_2>',
    'PCK_<TARGET_TABLE_2>',
    '<TARGET_TABLE_2>_PND',
    'PCK_<TARGET_TABLE_2>_PND'
  )
order by owner, object_type, object_name;

prompt == Package validation and side-effect slices ==
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and name in ('<PACKAGE_1>', '<PACKAGE_2>')
  and (
    upper(text) like '%TRATA_ERRO%'
    or upper(text) like '%INSERT%'
    or upper(text) like '%UPDATE%'
    or upper(text) like '%DELETE%'
    or upper(text) like '%FLAG_PACK%'
    or upper(text) like '%PACK_HAD_PEND%'
    or upper(text) like '%PACK_ERG_PEND%'
    or upper(text) like '%PEND%'
    or upper(text) like '%AUDIT%'
    or upper(text) like '%PUBLIC%'
    or upper(text) like '%PONTPUBL%'
    or upper(text) like '%PONTLEI%'
    or upper(text) like '%PRAGMA AUTONOMOUS_TRANSACTION%'
    or upper(text) like '%COMMIT%'
  )
order by owner, name, type, line;

prompt == Pending/publication/legal-document coupling candidates ==
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and name in (
    '<PACKAGE_1>',
    '<PACKAGE_2>',
    'PACK_ERG_PEND',
    'PACK_HAD_PEND',
    'ASSOCIA_PONTLEI'
  )
  and (
    upper(text) like '%UTILIZA_REGPEND%'
    or upper(text) like '%CHAVE_PEND%'
    or upper(text) like '%STATUS_PEND%'
    or upper(text) like '%PENDENTE%'
    or upper(text) like '%EFETIV%'
    or upper(text) like '%REJEIT%'
    or upper(text) like '%PONTPUBL%'
    or upper(text) like '%PONTLEI%'
    or upper(text) like '%ERG_LEI_REGISTRO%'
  )
order by owner, name, type, line;

prompt == Write target relevant columns ==
select owner, table_name, column_id, column_name, data_type,
       data_length, data_precision, data_scale, nullable, data_default
from all_tab_columns
where owner in ('ERGON','HADES')
  and table_name in ('<TARGET_TABLE_1>', '<TARGET_TABLE_2>')
  and (
    column_name in ('ID_REG','ROWID_REG','PONTPUBL','PONTLEI','DTINI','DTFIM','CHAVE_PEND','STATUS_PEND','OPER_PEND','TRANS_PEND')
    or column_name like '%PEND%'
    or column_name like '%AUD%'
  )
order by owner, table_name, column_id;

prompt == Write grants ==
select table_schema owner, table_name, grantee, privilege, grantable
from all_tab_privs
where table_schema in ('ERGON','HADES')
  and table_name in (
    '<TARGET_TABLE_1>',
    '<TARGET_TABLE_2>',
    '<WRITE_ROUTINE_1>',
    '<PACKAGE_1>',
    '<PACKAGE_2>'
  )
order by table_schema, table_name, grantee, privilege;
