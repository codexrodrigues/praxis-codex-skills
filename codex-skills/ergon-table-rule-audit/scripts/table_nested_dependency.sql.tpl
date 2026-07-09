SET HEADING ON PAGESIZE 500 LINESIZE 320 FEEDBACK OFF VERIFY OFF TIMING OFF TRIMSPOOL ON
WHENEVER SQLERROR CONTINUE

PROMPT ========== 0) Target ==========
SELECT '__OWNER__' AS target_owner, '__TABLE_NAME__' AS target_table, '__TABLE_BASE__' AS target_base, __MAX_DEPTH__ AS max_depth
FROM dual;

PROMPT ========== 1) Dependency seed objects ==========
WITH dispatch_objects AS (
  SELECT DISTINCT o.owner, o.object_type, o.object_name, 'HADES_DISPATCH_TARGET' AS seed_role
  FROM all_objects o
  WHERE o.owner = 'C_ERGON'
    AND o.object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
    AND EXISTS (
      SELECT 1
      FROM (
        SELECT sintaxe
        FROM hades.had_cad_sproc
        WHERE sproc IN (
          'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
          'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
          'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
          'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
          'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
          'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
        )
           OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
           OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
        UNION ALL
        SELECT sintaxe
        FROM hades.had_cad_mult_eps
        WHERE sproc IN (
          'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
          'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
          'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
          'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
          'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
          'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
        )
           OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
           OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
      ) h
      WHERE h.sintaxe IS NOT NULL
        AND INSTR(UPPER(h.sintaxe), o.object_name) > 0
    )
),
seed_objects AS (
  SELECT owner, 'TRIGGER' AS object_type, trigger_name AS object_name, 'TABLE_TRIGGER' AS seed_role
  FROM all_triggers
  WHERE table_owner = '__OWNER__'
    AND table_name = '__TABLE_NAME__'
  UNION
  SELECT owner, object_type, object_name,
         CASE
           WHEN object_name LIKE 'PCK\_%' ESCAPE '\' THEN 'PRODUCT_PACKAGE'
           WHEN object_name LIKE 'ERG\_DML\_%' ESCAPE '\' THEN 'GENERATED_DML'
           WHEN object_type = 'TRIGGER' THEN 'GENERATED_TRIGGER'
           ELSE 'TARGET_RELATED_OBJECT'
         END AS seed_role
  FROM all_objects
  WHERE owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
    AND object_type IN ('TRIGGER', 'PACKAGE', 'PACKAGE BODY', 'PROCEDURE', 'FUNCTION')
    AND (
         object_name IN (
           'PCK___TABLE_NAME__','PCK___TABLE_BASE__',
           'PCK___TABLE_NAME___PND','PCK___TABLE_BASE___PND',
           'ERG_DML___TABLE_NAME__','ERG_DML___TABLE_BASE__',
           'ERG_DML___TABLE_NAME___PUBL','ERG_DML___TABLE_BASE___PUBL',
           'AUDHD___TABLE_NAME__','AUDHD___TABLE_BASE__',
           'AUDIT___TABLE_NAME__','AUDIT___TABLE_BASE__',
           'T_BS_IUD___TABLE_NAME__','T_BS_IUD___TABLE_BASE__',
           'T_B_IUD___TABLE_NAME__','T_B_IUD___TABLE_BASE__',
           'T_A_IUD___TABLE_NAME__','T_A_IUD___TABLE_BASE__'
         )
      OR object_name LIKE 'PCK\___TABLE_NAME__%' ESCAPE '\'
      OR object_name LIKE 'PCK\___TABLE_BASE__%' ESCAPE '\'
      OR object_name LIKE 'ERG\_DML\___TABLE_NAME__%' ESCAPE '\'
      OR object_name LIKE 'ERG\_DML\___TABLE_BASE__%' ESCAPE '\'
      OR object_name LIKE 'T\_%\___TABLE_NAME__' ESCAPE '\'
      OR object_name LIKE 'T\_%\___TABLE_BASE__' ESCAPE '\'
      OR object_name LIKE 'AUD%\___TABLE_NAME__' ESCAPE '\'
      OR object_name LIKE 'AUD%\___TABLE_BASE__' ESCAPE '\'
    )
  UNION
  SELECT owner, object_type, object_name, seed_role FROM dispatch_objects
)
SELECT s.seed_role, s.owner, s.object_type, s.object_name, o.status
FROM seed_objects s
LEFT JOIN all_objects o
  ON o.owner = s.owner
 AND o.object_type = s.object_type
 AND o.object_name = s.object_name
ORDER BY s.seed_role, s.owner, s.object_type, s.object_name;

PROMPT ========== 2) Nested structural dependency graph ==========
WITH dispatch_objects AS (
  SELECT DISTINCT o.owner, o.object_type, o.object_name, 'HADES_DISPATCH_TARGET' AS seed_role
  FROM all_objects o
  WHERE o.owner = 'C_ERGON'
    AND o.object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
    AND EXISTS (
      SELECT 1
      FROM (
        SELECT sintaxe
        FROM hades.had_cad_sproc
        WHERE sproc IN (
          'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
          'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
          'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
          'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
          'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
          'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
        )
           OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
           OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
        UNION ALL
        SELECT sintaxe
        FROM hades.had_cad_mult_eps
        WHERE sproc IN (
          'EPB____TABLE_NAME__','EPB____TABLE_BASE__',
          'EPA____TABLE_NAME__','EPA____TABLE_BASE__',
          'EPB____TABLE_NAME___PND','EPB____TABLE_BASE___PND',
          'EPA____TABLE_NAME___PND','EPA____TABLE_BASE___PND',
          'EP_TRG_B___TABLE_NAME__','EP_TRG_B___TABLE_BASE__',
          'EP_TRG_A___TABLE_NAME__','EP_TRG_A___TABLE_BASE__'
        )
           OR UPPER(sproc) LIKE '%__TABLE_NAME__%'
           OR UPPER(sproc) LIKE '%__TABLE_BASE__%'
      ) h
      WHERE h.sintaxe IS NOT NULL
        AND INSTR(UPPER(h.sintaxe), o.object_name) > 0
    )
),
seed_objects AS (
  SELECT owner, 'TRIGGER' AS object_type, trigger_name AS object_name, 'TABLE_TRIGGER' AS seed_role
  FROM all_triggers
  WHERE table_owner = '__OWNER__'
    AND table_name = '__TABLE_NAME__'
  UNION
  SELECT owner, object_type, object_name,
         CASE
           WHEN object_name LIKE 'PCK\_%' ESCAPE '\' THEN 'PRODUCT_PACKAGE'
           WHEN object_name LIKE 'ERG\_DML\_%' ESCAPE '\' THEN 'GENERATED_DML'
           WHEN object_type = 'TRIGGER' THEN 'GENERATED_TRIGGER'
           ELSE 'TARGET_RELATED_OBJECT'
         END AS seed_role
  FROM all_objects
  WHERE owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
    AND object_type IN ('TRIGGER', 'PACKAGE', 'PACKAGE BODY', 'PROCEDURE', 'FUNCTION')
    AND (
         object_name IN (
           'PCK___TABLE_NAME__','PCK___TABLE_BASE__',
           'PCK___TABLE_NAME___PND','PCK___TABLE_BASE___PND',
           'ERG_DML___TABLE_NAME__','ERG_DML___TABLE_BASE__',
           'ERG_DML___TABLE_NAME___PUBL','ERG_DML___TABLE_BASE___PUBL',
           'AUDHD___TABLE_NAME__','AUDHD___TABLE_BASE__',
           'AUDIT___TABLE_NAME__','AUDIT___TABLE_BASE__',
           'T_BS_IUD___TABLE_NAME__','T_BS_IUD___TABLE_BASE__',
           'T_B_IUD___TABLE_NAME__','T_B_IUD___TABLE_BASE__',
           'T_A_IUD___TABLE_NAME__','T_A_IUD___TABLE_BASE__'
         )
      OR object_name LIKE 'PCK\___TABLE_NAME__%' ESCAPE '\'
      OR object_name LIKE 'PCK\___TABLE_BASE__%' ESCAPE '\'
      OR object_name LIKE 'ERG\_DML\___TABLE_NAME__%' ESCAPE '\'
      OR object_name LIKE 'ERG\_DML\___TABLE_BASE__%' ESCAPE '\'
      OR object_name LIKE 'T\_%\___TABLE_NAME__' ESCAPE '\'
      OR object_name LIKE 'T\_%\___TABLE_BASE__' ESCAPE '\'
      OR object_name LIKE 'AUD%\___TABLE_NAME__' ESCAPE '\'
      OR object_name LIKE 'AUD%\___TABLE_BASE__' ESCAPE '\'
    )
  UNION
  SELECT owner, object_type, object_name, seed_role FROM dispatch_objects
),
graph AS (
  SELECT LEVEL AS dep_level,
         CONNECT_BY_ROOT d.owner AS root_owner,
         CONNECT_BY_ROOT d.name AS root_name,
         CONNECT_BY_ROOT d.type AS root_type,
         d.owner AS source_owner,
         d.name AS source_name,
         d.type AS source_type,
         d.referenced_owner AS target_owner,
         d.referenced_name AS target_name,
         d.referenced_type AS target_type,
         d.dependency_type,
         SYS_CONNECT_BY_PATH(d.owner || '.' || d.name || '(' || d.type || ')', ' -> ') AS source_path
  FROM all_dependencies d
  WHERE d.referenced_owner NOT IN ('SYS', 'SYSTEM')
    AND d.referenced_name NOT IN ('STANDARD', 'DBMS_STANDARD')
  START WITH EXISTS (
    SELECT 1
    FROM seed_objects s
    WHERE s.owner = d.owner
      AND s.object_name = d.name
      AND (
           s.object_type = d.type
        OR (s.object_type = 'PACKAGE BODY' AND d.type = 'PACKAGE')
        OR (s.object_type = 'PACKAGE' AND d.type = 'PACKAGE BODY')
      )
  )
  CONNECT BY NOCYCLE
       PRIOR d.referenced_owner = d.owner
   AND PRIOR d.referenced_name = d.name
   AND PRIOR d.referenced_type = d.type
   AND LEVEL < __MAX_DEPTH__
)
SELECT dep_level, root_owner, root_name, root_type,
       source_owner, source_name, source_type,
       target_owner, target_name, target_type,
       dependency_type, source_path
FROM graph
ORDER BY root_owner, root_name, dep_level, source_owner, source_name, target_owner, target_name;

PROMPT ========== 3) Source call candidates inside seed and dependency objects ==========
WITH dispatch_objects AS (
  SELECT DISTINCT o.owner, o.object_type, o.object_name
  FROM all_objects o
  WHERE o.owner = 'C_ERGON'
    AND o.object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE', 'PACKAGE BODY')
    AND EXISTS (
      SELECT 1
      FROM (
        SELECT sintaxe
        FROM hades.had_cad_sproc
        WHERE (sproc LIKE '%__TABLE_NAME__%' OR sproc LIKE '%__TABLE_BASE__%')
          AND sintaxe IS NOT NULL
        UNION ALL
        SELECT sintaxe
        FROM hades.had_cad_mult_eps
        WHERE (sproc LIKE '%__TABLE_NAME__%' OR sproc LIKE '%__TABLE_BASE__%')
          AND sintaxe IS NOT NULL
      ) h
      WHERE INSTR(UPPER(h.sintaxe), o.object_name) > 0
    )
),
source_scope AS (
  SELECT owner, trigger_name AS name, 'TRIGGER' AS type
  FROM all_triggers
  WHERE table_owner = '__OWNER__'
    AND table_name = '__TABLE_NAME__'
  UNION
  SELECT owner, object_name AS name, object_type AS type
  FROM all_objects
  WHERE owner IN ('__OWNER__', 'HADES', 'C_HADES', 'C_ERGON')
    AND object_type IN ('PACKAGE', 'PACKAGE BODY', 'PROCEDURE', 'FUNCTION')
    AND (
         object_name LIKE '%__TABLE_NAME__%'
      OR object_name LIKE '%__TABLE_BASE__%'
      OR object_name IN (
           'PCK___TABLE_NAME__','PCK___TABLE_BASE__',
           'PCK___TABLE_NAME___PND','PCK___TABLE_BASE___PND',
           'ERG_DML___TABLE_NAME__','ERG_DML___TABLE_BASE__'
         )
    )
  UNION
  SELECT owner, object_name AS name, object_type AS type
  FROM dispatch_objects
)
SELECT s.owner, s.name, s.type, s.line,
       CASE
         WHEN INSTR(UPPER(s.text), 'EXECUTE IMMEDIATE') > 0 THEN 'DYNAMIC_SQL'
         WHEN INSTR(UPPER(s.text), 'TRATA_ERRO') > 0 OR INSTR(UPPER(s.text), 'RAISE') > 0 THEN 'ERROR_OR_VALIDATION'
         WHEN INSTR(UPPER(s.text), 'FLAG_PACK') > 0 THEN 'SESSION_CONTEXT'
         WHEN INSTR(UPPER(s.text), 'PACK_HAD_PEND') > 0 OR INSTR(UPPER(s.text), 'PACK_ERG_PEND') > 0 OR INSTR(UPPER(s.text), 'GRAVA_PEND') > 0 THEN 'PENDING_WORKFLOW'
         WHEN INSTR(UPPER(s.text), 'PCK_EXEC_EP_CERG') > 0 THEN 'CLIENT_EP_DISPATCH'
         WHEN INSTR(UPPER(s.text), 'PCK_') > 0 OR INSTR(UPPER(s.text), 'PACK_') > 0 THEN 'PACKAGE_CALL'
         WHEN INSTR(UPPER(s.text), 'EP__') > 0 OR INSTR(UPPER(s.text), 'POA_') > 0 THEN 'EP_OR_CLIENT_CALL'
         ELSE 'CALL_CANDIDATE'
       END AS call_class,
       RTRIM(s.text) AS text
FROM all_source s
WHERE EXISTS (
    SELECT 1
    FROM source_scope sc
    WHERE sc.owner = s.owner
      AND sc.name = s.name
      AND (
           sc.type = s.type
        OR (sc.type = 'PACKAGE' AND s.type = 'PACKAGE BODY')
        OR (sc.type = 'PACKAGE BODY' AND s.type = 'PACKAGE')
      )
  )
  AND (
       INSTR(UPPER(s.text), 'PCK_') > 0
    OR INSTR(UPPER(s.text), 'PACK_') > 0
    OR INSTR(UPPER(s.text), 'EP__') > 0
    OR INSTR(UPPER(s.text), 'POA_') > 0
    OR INSTR(UPPER(s.text), 'TRATA_ERRO') > 0
    OR INSTR(UPPER(s.text), 'RAISE') > 0
    OR INSTR(UPPER(s.text), 'FLAG_PACK') > 0
    OR INSTR(UPPER(s.text), 'EXECUTE IMMEDIATE') > 0
    OR INSTR(UPPER(s.text), 'GRAVA_PEND') > 0
  )
ORDER BY s.owner, s.name, s.type, s.line;

PROMPT ========== 4) Dynamic HADES syntax that may hide runtime dependencies ==========
SELECT 'HAD_CAD_SPROC' AS source_table, sproc, NULL AS ep, NULL AS ordem,
       exec, exec_mult_eps,
       CASE
         WHEN NVL(exec_mult_eps, 'N') <> 'S'
          AND exec = 'S'
          AND sintaxe IS NOT NULL THEN 'ACTIVE_PARENT'
         WHEN NVL(exec_mult_eps, 'N') = 'S' THEN 'MULTI_PARENT_SEE_ROWS'
         ELSE 'INACTIVE_PARENT_OR_NO_SYNTAX'
       END AS execution_status,
       sintaxe
FROM hades.had_cad_sproc
WHERE (sproc LIKE '%__TABLE_NAME__%' OR sproc LIKE '%__TABLE_BASE__%')
  AND sintaxe IS NOT NULL
UNION ALL
SELECT 'HAD_CAD_MULT_EPS' AS source_table, m.sproc, m.ep, m.ordem,
       m.exec, s.exec_mult_eps,
       CASE
         WHEN s.exec_mult_eps = 'S'
          AND m.exec = 'S'
          AND m.sintaxe IS NOT NULL THEN 'ACTIVE_MULTI_ROW'
         WHEN s.exec_mult_eps = 'S' THEN 'INACTIVE_MULTI_ROW'
         ELSE 'UNREACHED_MULTI_ROW_PARENT_NOT_MULTI'
       END AS execution_status,
       m.sintaxe
FROM hades.had_cad_mult_eps m
LEFT JOIN hades.had_cad_sproc s
  ON s.sproc = m.sproc
WHERE (m.sproc LIKE '%__TABLE_NAME__%' OR m.sproc LIKE '%__TABLE_BASE__%')
  AND m.sintaxe IS NOT NULL
ORDER BY source_table, sproc, ordem, ep;

EXIT;
