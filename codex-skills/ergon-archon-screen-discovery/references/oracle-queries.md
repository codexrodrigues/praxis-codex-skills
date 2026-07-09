# Oracle Discovery Queries

Use these query patterns as read-only building blocks. `ERGON` and `HADES` are default owners for the current Ergon environment; adjust them when the environment differs. Prefer narrow object lists over broad schema scans.

The examples use SQLcl substitution variables for executable snippets:

```sql
define screen_prefix = 'ERGADM00033'
define owners = '''ERGON'',''HADES'''
```

For object lists, write quoted literals directly:

```sql
and object_name in ('ERGADM00033_TIPOFREQ','ERGADM00034_CODFREQ')
```

Avoid leaving pseudo placeholders such as `:object_names` in files executed by SQLcl.

## Setup

```sql
set pagesize 500 linesize 260 trimspool on tab off feedback off verify off
set long 200000 longchunksize 32767
```

## Object Discovery

```sql
select owner, object_name, object_type, status
from all_objects
where owner in ('ERGON','HADES')
  and object_name like upper('&screen_prefix' || '%')
order by owner, object_name, object_type;
```

For exact known objects:

```sql
select owner, object_name, object_type, status
from all_objects
where owner in ('ERGON','HADES')
  and object_name in (:object_names)
order by owner, object_name, object_type;
```

## View Text

```sql
select owner, view_name, text_length, text
from all_views
where owner in ('ERGON','HADES')
  and view_name in (:view_names)
order by owner, view_name;
```

Try `dbms_metadata.get_ddl` when privileges allow it:

```sql
select dbms_metadata.get_ddl('VIEW', :view_name, :owner)
from dual;
```

## Dependencies

Direct and reverse dependency search:

```sql
select owner, name, type, referenced_owner, referenced_name, referenced_type
from all_dependencies
where owner in ('ERGON','HADES')
  and (
    name in (:object_names)
    or referenced_name in (:object_names)
  )
order by owner, name, referenced_owner, referenced_name;
```

Recursive dependency expansion when privileges and Oracle version allow recursive CTEs:

```sql
with seed(owner, name, type) as (
  select 'ERGON', 'ERGADM00033_TIPOFREQ', 'VIEW' from dual
),
deps(lvl, owner, name, type, referenced_owner, referenced_name, referenced_type, path) as (
  select 1, d.owner, d.name, d.type, d.referenced_owner, d.referenced_name, d.referenced_type,
         d.owner || '.' || d.name || ' -> ' || d.referenced_owner || '.' || d.referenced_name
  from all_dependencies d
  join seed s on s.owner = d.owner and s.name = d.name and s.type = d.type
  union all
  select deps.lvl + 1, d.owner, d.name, d.type, d.referenced_owner, d.referenced_name, d.referenced_type,
         deps.path || ' -> ' || d.referenced_owner || '.' || d.referenced_name
  from all_dependencies d
  join deps on deps.referenced_owner = d.owner and deps.referenced_name = d.name and deps.referenced_type = d.type
  where deps.lvl < 8
)
select distinct lvl, owner, name, type, referenced_owner, referenced_name, referenced_type, path
from deps
order by path;
```

If recursive CTEs are not available, iterate the direct dependency query level by level.

Generated confirmation SQL must include either the recursive dependency query or a clearly documented manual level-by-level expansion. Direct dependency output alone is not enough for migration readiness.

## Synonym Resolution

Resolve private/public synonyms and recurse manually until the effective object is reached:

```sql
select owner, synonym_name, table_owner, table_name, db_link
from all_synonyms
where synonym_name in (:object_names)
   or table_name in (:object_names)
order by owner, synonym_name;
```

Record whether the screen references the synonym owner or the final table owner.

Recursive synonym chain helper:

```sql
with syn(depth, owner, synonym_name, table_owner, table_name, db_link, path) as (
  select 1, owner, synonym_name, table_owner, table_name, db_link,
         owner || '.' || synonym_name || ' -> ' || table_owner || '.' || table_name
  from all_synonyms
  where synonym_name in ('EMPRESAS','TIPO_FREQ','CODIGOS_FREQ')
  union all
  select syn.depth + 1, s.owner, s.synonym_name, s.table_owner, s.table_name, s.db_link,
         syn.path || ' -> ' || s.table_owner || '.' || s.table_name
  from all_synonyms s
  join syn on s.owner = syn.table_owner and s.synonym_name = syn.table_name
  where syn.depth < 8
)
select syn.*, o.object_type, o.status
from syn
left join all_objects o on o.owner = syn.table_owner and o.object_name = syn.table_name
order by path;
```

Treat a synonym as resolved only when the final target exists in `ALL_OBJECTS` or has a deliberate `DB_LINK`.

Generated confirmation SQL must include recursive synonym resolution for every object referenced by screen XML, runtime SQL, lookup combos, and related flows.

## Columns

```sql
select owner, table_name, column_id, column_name, data_type,
       data_length, data_precision, data_scale, nullable
from all_tab_columns
where owner in ('ERGON','HADES')
  and table_name in (:object_names)
order by owner, table_name, column_id;
```

## Constraints and Keys

```sql
select ac.owner, ac.table_name, ac.constraint_name, ac.constraint_type,
       ac.r_owner, ac.r_constraint_name, ac.status,
       listagg(acc.column_name, ', ') within group(order by acc.position) columns
from all_constraints ac
left join all_cons_columns acc
  on acc.owner = ac.owner
 and acc.constraint_name = ac.constraint_name
 and acc.table_name = ac.table_name
where ac.owner in ('ERGON','HADES')
  and ac.table_name in (:table_names)
group by ac.owner, ac.table_name, ac.constraint_name, ac.constraint_type,
         ac.r_owner, ac.r_constraint_name, ac.status
order by ac.owner, ac.table_name, ac.constraint_type, ac.constraint_name;
```

Constraint query with referenced table/columns:

```sql
select child.owner child_owner, child.table_name child_table, child.constraint_name child_constraint,
       listagg(child_cols.column_name, ', ') within group(order by child_cols.position) child_columns,
       parent.owner parent_owner, parent.table_name parent_table, parent.constraint_name parent_constraint,
       listagg(parent_cols.column_name, ', ') within group(order by parent_cols.position) parent_columns
from all_constraints child
join all_cons_columns child_cols
  on child_cols.owner = child.owner
 and child_cols.constraint_name = child.constraint_name
 and child_cols.table_name = child.table_name
left join all_constraints parent
  on parent.owner = child.r_owner
 and parent.constraint_name = child.r_constraint_name
left join all_cons_columns parent_cols
  on parent_cols.owner = parent.owner
 and parent_cols.constraint_name = parent.constraint_name
 and parent_cols.table_name = parent.table_name
 and parent_cols.position = child_cols.position
where child.owner in ('ERGON','HADES')
  and child.table_name in (:table_names)
group by child.owner, child.table_name, child.constraint_name,
         parent.owner, parent.table_name, parent.constraint_name
order by child.owner, child.table_name, child.constraint_name;
```

## Indexes

```sql
select ai.owner, ai.index_name, ai.table_owner, ai.table_name,
       ai.uniqueness, ai.status,
       listagg(aic.column_name, ', ') within group(order by aic.column_position) columns
from all_indexes ai
left join all_ind_columns aic
  on aic.index_owner = ai.owner
 and aic.index_name = ai.index_name
where ai.table_owner in ('ERGON','HADES')
  and ai.table_name in (:table_names)
group by ai.owner, ai.index_name, ai.table_owner, ai.table_name,
         ai.uniqueness, ai.status
order by ai.table_owner, ai.table_name, ai.index_name;
```

## Triggers

```sql
select owner, trigger_name, table_owner, table_name, status, triggering_event
from all_triggers
where table_owner in ('ERGON','HADES')
  and table_name in (:table_names)
order by table_owner, table_name, trigger_name;
```

## Grants

```sql
select table_schema owner, table_name, grantee, privilege, grantable
from all_tab_privs
where table_schema in ('ERGON','HADES')
  and table_name in (:object_names)
order by table_schema, table_name, grantee, privilege;
```

Also inspect role and package/function access when security helpers are involved:

```sql
select grantee, granted_role, admin_option, default_role
from all_role_privs
where grantee in (:grantees)
order by grantee, granted_role;

select owner, package_name, object_name, argument_name, position, data_type, in_out
from all_arguments
where owner in ('ERGON','HADES')
  and (package_name in (:package_names) or object_name in (:object_names))
order by owner, package_name, object_name, position;
```

## Source Search

Use for packages, functions, procedures, and triggers that build SQL dynamically or apply hidden rules:

```sql
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and (
    upper(text) like upper('%' || :term1 || '%')
    or upper(text) like upper('%' || :term2 || '%')
  )
order by owner, name, type, line;
```

## Updatable View Columns

Use when the legacy screen exposes `ROWID`, edit/delete buttons, or writes through a view:

```sql
select owner, table_name, column_name, updatable, insertable, deletable
from all_updatable_columns
where owner in ('ERGON','HADES')
  and table_name in (:view_names)
order by owner, table_name, column_name;
```

For write-risk analysis, also inspect view DDL, `INSTEAD OF` triggers, table defaults, and source writes:

```sql
select owner, trigger_name, table_owner, table_name, status, triggering_event
from all_triggers
where table_owner in ('ERGON','HADES')
  and table_name in (:view_names)
  and trigger_type like 'INSTEAD OF%';

select owner, table_name, column_name, data_default, nullable
from all_tab_columns
where owner in ('ERGON','HADES')
  and table_name in (:table_names)
  and data_default is not null
order by owner, table_name, column_id;
```

Search writes in PL/SQL source:

```sql
select owner, name, type, line, text
from all_source
where owner in ('ERGON','HADES')
  and regexp_like(upper(text), '(INSERT|UPDATE|DELETE|MERGE).*(' || upper(:object_fragment) || ')')
order by owner, name, type, line;
```

## Comments

```sql
select owner, table_name, comments
from all_tab_comments
where owner in ('ERGON','HADES')
  and table_name in (:object_names);

select owner, table_name, column_name, comments
from all_col_comments
where owner in ('ERGON','HADES')
  and table_name in (:object_names)
order by owner, table_name, column_name;
```

## Data Confirmation

Only run sample queries with tight filters. For write confirmation, get explicit user approval and use a disposable record in a safe environment.

```sql
select count(*) from <owner>.<object> where <key_column> = :key_value;
select * from <owner>.<object> where <key_column> = :key_value and rownum <= 5;
```
