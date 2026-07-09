SET HEADING ON PAGESIZE 500 LINESIZE 260 FEEDBACK OFF VERIFY OFF TIMING OFF TRIMSPOOL ON
WHENEVER SQLERROR CONTINUE

PROMPT ========== 0) Target ==========
SELECT '__OWNER__' AS target_owner, '__TABLE_NAME__' AS target_table FROM dual;

PROMPT ========== 1) Triggers on target table ==========
SELECT table_owner, owner, trigger_name, trigger_type, triggering_event, status
FROM all_triggers
WHERE table_owner = '__OWNER__'
  AND table_name = '__TABLE_NAME__'
ORDER BY
  CASE trigger_type
    WHEN 'BEFORE STATEMENT' THEN 1
    WHEN 'BEFORE EACH ROW'  THEN 2
    WHEN 'AFTER EACH ROW'   THEN 3
    WHEN 'AFTER STATEMENT'  THEN 4
    ELSE 9
  END,
  trigger_name;

PROMPT ========== 1b) Generated object inventory ==========
SELECT owner, object_type, object_name, status
FROM all_objects
WHERE owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
  AND (
       object_name IN (
         'PCK___TABLE_NAME__',
         'PCK___TABLE_BASE__',
         'PCK___TABLE_NAME___PND',
         'PCK___TABLE_BASE___PND',
         'ERG_DML___TABLE_NAME__',
         'ERG_DML___TABLE_BASE__',
         'ERG_DML___TABLE_NAME___PUBL',
         'ERG_DML___TABLE_BASE___PUBL',
         'AUDHD___TABLE_NAME__',
         'AUDHD___TABLE_BASE__',
         'AUDIT___TABLE_NAME__',
         'AUDIT___TABLE_BASE__',
         'T_BS_IUD___TABLE_NAME__',
         'T_BS_IUD___TABLE_BASE__',
         'T_B_IUD___TABLE_NAME__',
         'T_B_IUD___TABLE_BASE__',
         'T_A_IUD___TABLE_NAME__',
         'T_A_IUD___TABLE_BASE__'
       )
    OR object_name LIKE 'T\_%\___TABLE_NAME__' ESCAPE '\'
    OR object_name LIKE 'T\_%\___TABLE_BASE__' ESCAPE '\'
    OR object_name LIKE 'AUD%\___TABLE_NAME__' ESCAPE '\'
    OR object_name LIKE 'AUD%\___TABLE_BASE__' ESCAPE '\'
    OR object_name LIKE 'ERG\_DML\___TABLE_NAME__%' ESCAPE '\'
    OR object_name LIKE 'ERG\_DML\___TABLE_BASE__%' ESCAPE '\'
    OR object_name LIKE 'PCK\___TABLE_NAME__%' ESCAPE '\'
    OR object_name LIKE 'PCK\___TABLE_BASE__%' ESCAPE '\'
    OR object_name LIKE 'V\___TABLE_NAME__%' ESCAPE '\'
    OR object_name LIKE 'V\___TABLE_BASE__%' ESCAPE '\'
    OR object_name LIKE '%\___TABLE_NAME___EMPRESA' ESCAPE '\'
    OR object_name LIKE '%\___TABLE_BASE___EMPRESA' ESCAPE '\'
  )
ORDER BY owner, object_type, object_name;

PROMPT ========== 1c) Invalid object errors for target-related objects ==========
SELECT owner, name, type, sequence, line, position, text
FROM all_errors
WHERE owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
  AND (
       name IN (
         'PCK___TABLE_NAME__',
         'PCK___TABLE_BASE__',
         'PCK___TABLE_NAME___PND',
         'PCK___TABLE_BASE___PND',
         'ERG_DML___TABLE_NAME__',
         'ERG_DML___TABLE_BASE__',
         'ERG_DML___TABLE_NAME___PUBL',
         'ERG_DML___TABLE_BASE___PUBL',
         'AUDHD___TABLE_NAME__',
         'AUDHD___TABLE_BASE__',
         'AUDIT___TABLE_NAME__',
         'AUDIT___TABLE_BASE__',
         'T_BS_IUD___TABLE_NAME__',
         'T_BS_IUD___TABLE_BASE__',
         'T_B_IUD___TABLE_NAME__',
         'T_B_IUD___TABLE_BASE__',
         'T_A_IUD___TABLE_NAME__',
         'T_A_IUD___TABLE_BASE__'
       )
    OR name LIKE 'T\_%\___TABLE_NAME__' ESCAPE '\'
    OR name LIKE 'T\_%\___TABLE_BASE__' ESCAPE '\'
    OR name LIKE 'AUD%\___TABLE_NAME__' ESCAPE '\'
    OR name LIKE 'AUD%\___TABLE_BASE__' ESCAPE '\'
    OR name LIKE 'ERG\_DML\___TABLE_NAME__%' ESCAPE '\'
    OR name LIKE 'ERG\_DML\___TABLE_BASE__%' ESCAPE '\'
    OR name LIKE 'PCK\___TABLE_NAME__%' ESCAPE '\'
    OR name LIKE 'PCK\___TABLE_BASE__%' ESCAPE '\'
  )
ORDER BY owner, name, type, sequence;

PROMPT ========== 1d) Synonyms pointing to target-related objects ==========
SELECT owner, synonym_name, table_owner, table_name, db_link
FROM all_synonyms
WHERE table_owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
  AND (
       table_name = '__TABLE_NAME__'
    OR table_name IN (
         'PCK___TABLE_NAME__',
         'PCK___TABLE_BASE__',
         'PCK___TABLE_NAME___PND',
         'PCK___TABLE_BASE___PND',
         'ERG_DML___TABLE_NAME__',
         'ERG_DML___TABLE_BASE__',
         'ERG_DML___TABLE_NAME___PUBL',
         'ERG_DML___TABLE_BASE___PUBL'
       )
    OR table_name LIKE 'PCK\___TABLE_NAME__%' ESCAPE '\'
    OR table_name LIKE 'PCK\___TABLE_BASE__%' ESCAPE '\'
    OR table_name LIKE 'ERG\_DML\___TABLE_NAME__%' ESCAPE '\'
    OR table_name LIKE 'ERG\_DML\___TABLE_BASE__%' ESCAPE '\'
  )
ORDER BY owner, synonym_name;

PROMPT ========== 2) Trigger key calls in source order ==========
SELECT owner, name AS trigger_name, line, RTRIM(text) AS text
FROM all_source
WHERE type = 'TRIGGER'
  AND (owner, name) IN (
    SELECT owner, trigger_name
    FROM all_triggers
    WHERE table_owner = '__OWNER__'
      AND table_name = '__TABLE_NAME__'
  )
  AND (
       INSTR(UPPER(text), 'MAIN_PRE') > 0
    OR INSTR(UPPER(text), 'MAIN_POS') > 0
    OR INSTR(UPPER(text), 'EXEC_EP_TRG_') > 0
    OR INSTR(UPPER(text), 'EXEC_EP_PCK_') > 0
    OR INSTR(UPPER(text), 'GRAVA_PEND') > 0
    OR INSTR(UPPER(text), 'PACK_ERG_PEND') > 0
    OR INSTR(UPPER(text), 'PACK_HAD_PEND') > 0
    OR INSTR(UPPER(text), 'TRATA_ERRO') > 0
  )
ORDER BY owner, name, line;

PROMPT ========== 2b) Complete trigger source ==========
SELECT owner, name AS trigger_name, line, RTRIM(text) AS text
FROM all_source
WHERE type = 'TRIGGER'
  AND (owner, name) IN (
    SELECT owner, trigger_name
    FROM all_triggers
    WHERE table_owner = '__OWNER__'
      AND table_name = '__TABLE_NAME__'
  )
ORDER BY owner, name, line;

PROMPT ========== 3) Product package PCK_<TABLE>: EP and dispatch calls ==========
SELECT owner, name, type, line, RTRIM(text) AS text
FROM all_source
WHERE owner = '__OWNER__'
  AND name IN ('PCK___TABLE_NAME__', 'PCK___TABLE_BASE__', 'PCK___TABLE_NAME___PND', 'PCK___TABLE_BASE___PND')
  AND type IN ('PACKAGE', 'PACKAGE BODY')
  AND (
       INSTR(UPPER(text), 'MAIN_PRE') > 0
    OR INSTR(UPPER(text), 'MAIN_POS') > 0
    OR INSTR(UPPER(text), 'EXEC_EP_') > 0
    OR INSTR(UPPER(text), 'EPB__') > 0
    OR INSTR(UPPER(text), 'EPA__') > 0
    OR INSTR(UPPER(text), 'EP__') > 0
    OR INSTR(UPPER(text), 'POA_') > 0
  )
ORDER BY owner, name, type, line;

PROMPT ========== 3b) Product package business-rule candidates ==========
SELECT owner, name, type, line, RTRIM(text) AS text
FROM all_source
WHERE owner = '__OWNER__'
  AND name IN ('PCK___TABLE_NAME__', 'PCK___TABLE_BASE__', 'PCK___TABLE_NAME___PND', 'PCK___TABLE_BASE___PND')
  AND type IN ('PACKAGE BODY')
  AND (
       INSTR(UPPER(text), 'RAISE') > 0
    OR INSTR(UPPER(text), 'ERRO') > 0
    OR INSTR(UPPER(text), 'MENS') > 0
    OR INSTR(UPPER(text), 'VALID') > 0
    OR INSTR(UPPER(text), 'CONSIST') > 0
    OR INSTR(UPPER(text), 'TRATA') > 0
    OR INSTR(UPPER(text), 'PCK_') > 0
    OR INSTR(UPPER(text), 'PACK_') > 0
    OR INSTR(UPPER(text), 'EP__') > 0
    OR INSTR(UPPER(text), 'POA_') > 0
  )
ORDER BY owner, name, type, line;

PROMPT ========== 3c) Product package complete source for rule windows ==========
SELECT owner, name, type, line, RTRIM(text) AS text
FROM all_source
WHERE owner = '__OWNER__'
  AND name IN ('PCK___TABLE_NAME__', 'PCK___TABLE_BASE__', 'PCK___TABLE_NAME___PND', 'PCK___TABLE_BASE___PND')
  AND type IN ('PACKAGE BODY')
ORDER BY owner, name, type, line;

PROMPT ========== 4) HADES parent EP metadata ==========
SELECT sproc, tipo, exec, exec_mult_eps, sintaxe
FROM hades.had_cad_sproc
WHERE sproc IN (
  'EPB____TABLE_NAME__',
  'EPB____TABLE_BASE__',
  'EPA____TABLE_NAME__',
  'EPA____TABLE_BASE__',
  'EPB____TABLE_NAME___PND',
  'EPB____TABLE_BASE___PND',
  'EPA____TABLE_NAME___PND',
  'EPA____TABLE_BASE___PND',
  'EP_TRG_B___TABLE_NAME__',
  'EP_TRG_B___TABLE_BASE__',
  'EP_TRG_A___TABLE_NAME__',
  'EP_TRG_A___TABLE_BASE__'
)
   OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
   OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
ORDER BY sproc;

PROMPT ========== 5) HADES multiple EP chain ordered by ORDEM ==========
SELECT sproc, ep, ordem, exec, sintaxe
FROM hades.had_cad_mult_eps
WHERE sproc IN (
  'EPB____TABLE_NAME__',
  'EPB____TABLE_BASE__',
  'EPA____TABLE_NAME__',
  'EPA____TABLE_BASE__',
  'EPB____TABLE_NAME___PND',
  'EPB____TABLE_BASE___PND',
  'EPA____TABLE_NAME___PND',
  'EPA____TABLE_BASE___PND',
  'EP_TRG_B___TABLE_NAME__',
  'EP_TRG_B___TABLE_BASE__',
  'EP_TRG_A___TABLE_NAME__',
  'EP_TRG_A___TABLE_BASE__'
)
   OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
   OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
ORDER BY sproc, ordem, ep;

PROMPT ========== 6) Client executable objects by table/EP name ==========
SELECT owner, object_type, object_name, status
FROM all_objects
WHERE owner IN ('C_ERGON', 'C_HADES')
  AND object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
  AND (
       UPPER(object_name) LIKE '%__TABLE_NAME__%'
    OR UPPER(object_name) LIKE '%__TABLE_BASE__%'
    OR UPPER(object_name) LIKE 'POA\_%__TABLE_NAME__%' ESCAPE '\'
    OR UPPER(object_name) LIKE 'POA\_%__TABLE_BASE__%' ESCAPE '\'
    OR UPPER(object_name) LIKE 'EP\_\_%__TABLE_NAME__%' ESCAPE '\'
    OR UPPER(object_name) LIKE 'EP\_\_%__TABLE_BASE__%' ESCAPE '\'
  )
ORDER BY owner, object_type, object_name;

PROMPT ========== 7) Client source snippets for matched functions/procedures ==========
WITH hades_syntax AS (
  SELECT sintaxe
  FROM hades.had_cad_sproc
  WHERE sintaxe IS NOT NULL
    AND (
      sproc IN (
        'EPB____TABLE_NAME__',
        'EPB____TABLE_BASE__',
        'EPA____TABLE_NAME__',
        'EPA____TABLE_BASE__',
        'EPB____TABLE_NAME___PND',
        'EPB____TABLE_BASE___PND',
        'EPA____TABLE_NAME___PND',
        'EPA____TABLE_BASE___PND',
        'EP_TRG_B___TABLE_NAME__',
        'EP_TRG_B___TABLE_BASE__',
        'EP_TRG_A___TABLE_NAME__',
        'EP_TRG_A___TABLE_BASE__'
      )
      OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
      OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
    )
  UNION ALL
  SELECT sintaxe
  FROM hades.had_cad_mult_eps
  WHERE sintaxe IS NOT NULL
    AND (
      sproc IN (
        'EPB____TABLE_NAME__',
        'EPB____TABLE_BASE__',
        'EPA____TABLE_NAME__',
        'EPA____TABLE_BASE__',
        'EPB____TABLE_NAME___PND',
        'EPB____TABLE_BASE___PND',
        'EPA____TABLE_NAME___PND',
        'EPA____TABLE_BASE___PND',
        'EP_TRG_B___TABLE_NAME__',
        'EP_TRG_B___TABLE_BASE__',
        'EP_TRG_A___TABLE_NAME__',
        'EP_TRG_A___TABLE_BASE__'
      )
      OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
      OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
    )
),
dispatch_objects AS (
  SELECT DISTINCT o.object_name
  FROM hades_syntax h
  JOIN all_objects o
    ON o.owner = 'C_ERGON'
   AND o.object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
   AND INSTR(UPPER(h.sintaxe), o.object_name) > 0
)
SELECT owner, name, type, line, RTRIM(text) AS text
FROM all_source
WHERE owner = 'C_ERGON'
  AND type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE BODY')
  AND name IN (SELECT object_name FROM dispatch_objects)
  AND line <= 180
ORDER BY owner, name, type, line;

PROMPT ========== 8) HADES.PACK_EXEC_SPROC execution semantics ==========
SELECT line, RTRIM(text) AS text
FROM all_source
WHERE owner IN ('HADES', 'C_HADES')
  AND name = 'PACK_EXEC_SPROC'
  AND type = 'PACKAGE BODY'
  AND (
       INSTR(UPPER(text), 'EXEC_MULT_EPS') > 0
    OR INSTR(UPPER(text), 'HAD_CAD_MULT_EPS') > 0
    OR INSTR(UPPER(text), 'EXECUTA_EP') > 0
    OR INSTR(UPPER(text), 'EXECUTE IMMEDIATE') > 0
    OR INSTR(UPPER(text), 'R.EXEC') > 0
    OR INSTR(UPPER(text), 'P_HAD_CAD_SPROC.EXEC') > 0
  )
ORDER BY line;

PROMPT ========== 9) Dependencies referencing table ==========
SELECT owner, name, type, referenced_owner, referenced_name, dependency_type
FROM all_dependencies
WHERE referenced_owner = '__OWNER__'
  AND referenced_name = '__TABLE_NAME__'
  AND referenced_type = 'TABLE'
ORDER BY owner, name, type;

PROMPT ========== 10) Constraints on table ==========
SELECT constraint_name, constraint_type, r_constraint_name, status,
       search_condition
FROM all_constraints
WHERE owner = '__OWNER__'
  AND table_name = '__TABLE_NAME__'
ORDER BY constraint_type, constraint_name;

PROMPT ========== 10b) Table columns, nullable flags, defaults ==========
SELECT column_id, column_name, data_type, data_length, data_precision, data_scale,
       nullable, data_default
FROM all_tab_columns
WHERE owner = '__OWNER__'
  AND table_name = '__TABLE_NAME__'
ORDER BY column_id;

PROMPT ========== 10c) Source DML target candidates for side effects ==========
WITH hades_syntax AS (
  SELECT sintaxe
  FROM hades.had_cad_sproc
  WHERE sintaxe IS NOT NULL
    AND (
      sproc IN (
        'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
        'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
        'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
        'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
        'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
        'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
      )
      OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
      OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
    )
  UNION ALL
  SELECT sintaxe
  FROM hades.had_cad_mult_eps
  WHERE sintaxe IS NOT NULL
    AND (
      sproc IN (
        'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
        'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
        'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
        'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
        'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
        'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
      )
      OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
      OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
    )
),
dispatch_objects AS (
  SELECT DISTINCT o.owner, o.object_name
  FROM hades_syntax h
  JOIN all_objects o
    ON o.owner = 'C_ERGON'
   AND o.object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
   AND INSTR(UPPER(h.sintaxe), o.object_name) > 0
),
source_scope AS (
  SELECT '__OWNER__' AS owner, 'PCK___TABLE_NAME__' AS name FROM dual
  UNION SELECT '__OWNER__', 'PCK___TABLE_BASE__' FROM dual
  UNION SELECT '__OWNER__', 'PCK___TABLE_NAME___PND' FROM dual
  UNION SELECT '__OWNER__', 'PCK___TABLE_BASE___PND' FROM dual
  UNION SELECT '__OWNER__', 'ERG_DML___TABLE_NAME__' FROM dual
  UNION SELECT '__OWNER__', 'ERG_DML___TABLE_BASE__' FROM dual
  UNION SELECT '__OWNER__', 'ERG_DML___TABLE_NAME___PUBL' FROM dual
  UNION SELECT '__OWNER__', 'ERG_DML___TABLE_BASE___PUBL' FROM dual
  UNION SELECT owner, trigger_name
  FROM all_triggers
  WHERE table_owner = '__OWNER__'
    AND table_name = '__TABLE_NAME__'
  UNION SELECT owner, object_name FROM dispatch_objects
)
SELECT owner, name, type, line,
       CASE
         WHEN INSTR(UPPER(text), 'INSERT INTO') > 0 THEN 'INSERT'
         WHEN INSTR(UPPER(text), 'UPDATE ') > 0 THEN 'UPDATE'
         WHEN INSTR(UPPER(text), 'DELETE FROM') > 0 THEN 'DELETE'
         WHEN INSTR(UPPER(text), 'MERGE INTO') > 0 THEN 'MERGE'
         ELSE 'DML_CANDIDATE'
       END AS dml_kind,
       RTRIM(text) AS text
FROM all_source
WHERE (owner, name) IN (SELECT owner, name FROM source_scope)
  AND (
       INSTR(UPPER(text), 'INSERT INTO') > 0
    OR INSTR(UPPER(text), 'UPDATE ') > 0
    OR INSTR(UPPER(text), 'DELETE FROM') > 0
    OR INSTR(UPPER(text), 'MERGE INTO') > 0
  )
ORDER BY owner, name, type, line;

PROMPT ========== 11) Generated DML procedure source hints ==========
SELECT owner, name, type, line, RTRIM(text) AS text
FROM all_source
WHERE owner = '__OWNER__'
  AND name IN ('ERG_DML___TABLE_NAME__', 'ERG_DML___TABLE_BASE__', 'ERG_DML___TABLE_NAME___PUBL', 'ERG_DML___TABLE_BASE___PUBL')
  AND type = 'PROCEDURE'
  AND (
       INSTR(UPPER(text), 'EXECUTA_DML') > 0
    OR INSTR(UPPER(text), 'PCK_') > 0
    OR INSTR(UPPER(text), 'EP') > 0
    OR INSTR(UPPER(text), 'PACK_HAD_PEND') > 0
    OR INSTR(UPPER(text), 'PUBLIC') > 0
    OR INSTR(UPPER(text), 'AUDIT') > 0
  )
ORDER BY owner, name, line;

EXIT;
