# Oracle Confirmation SQL Template

Use this checklist when creating an `oracle-confirmation.sql` artifact. Keep it read-only and executable in SQLcl. Prefer concrete literal object lists over pseudo-placeholders.

When the migration workspace provides `tools/migration-factory/new-phase1-oracle-sql.ps1` and Phase 1 already has `docs/migracao/<SCREEN>/factory/extraction.json`, use that generator first. This template is the checklist for reviewing the generated SQL or for writing supplemental SQL when the generated coverage is insufficient. Do not make agents hand-craft the normal object/HADES confirmation path unless the generator is unavailable or the gate records the concrete gap.

## Required Header

Include:

- Target screen code and date.
- Connection assumptions without credentials.
- Owners searched.
- Object seed list derived from browser/XML/runtime SQL.
- Source evidence for each seed object: runtime, XML/debug, local source, or candidate reason.
- Owner/package/subprogram identity when present in XML/runtime evidence; do not collapse `OWNER.OBJECT` or `PACKAGE.PROCEDURE` into an unqualified name.
- Components or related flows intentionally excluded.

## Required Sections

Every confirmation SQL should cover these sections unless explicitly marked `NOT APPLICABLE` with a reason in a comment:

1. SQLcl setup: `pagesize`, `linesize`, `long`, `trimspool`, `feedback`, `verify`.
2. Seed object list with comments tying each object back to screen XML/debug/runtime evidence, source component, role, owner hint, package and subprogram.
3. Seed object existence from `ALL_OBJECTS`, preserving owner hints and reporting owner collisions.
4. Recursive synonym resolution from every screen-referenced object and lookup.
5. View text or `DBMS_METADATA.GET_DDL` for screen views and related-screen views.
6. Recursive dependency expansion from screen views, related views, packages, and write targets.
7. Derived physical table/view list from recursive lineage.
8. Reverse dependencies for physical tables and screen views.
9. Columns/defaults for views, tables, derived physical objects, and candidate write targets.
10. Constraints with referenced parent tables and columns.
11. Indexes for physical tables and stable-key candidates.
12. Regular triggers on physical tables.
13. `INSTEAD OF` triggers and `ALL_UPDATABLE_COLUMNS` for views.
14. Grants on views, tables, packages, and helpers.
15. Role privileges for the application schema or runtime grantees when known.
16. Package/function arguments for security helpers and business-rule packages.
17. Narrow source search for screen-specific packages/functions and separate write-risk search for discovered write targets. Avoid broad terms such as `%FREQUENCIAS%` unless the output is intentionally bounded.
18. Table defaults and nullable generated fields relevant to write planning.
19. Tight data smoke checks for each required endpoint and special scope value.
20. One comment block listing candidate objects that were deliberately not promoted.

## HADES Registry Coverage

Every Phase 1 package must have HADES registry coverage before API readiness. Prefer a separate `hades-registry.sql`; alternatively include a clearly named HADES section inside `oracle-confirmation.sql`. It should verify transaction/menu/access metadata before API readiness:

- `HADES.TRANSACAO` and `HADES.HADADM00019_TRANSACAO`.
- `HADES.TRANSPADACES`, `HADES.HADADM00015_TRANSPADACES`, and `HADES.HADADM00023_TRANSPADACES`.
- `HADES.TRANSPADTELA` and `HADES.HADADM00020_TRANSPADTELA` when menu/path metadata is expected.
- `HADES.PADTELA` and `HADES.MENUDEF` when source-of-truth, menu/path, or pattern metadata can affect the API boundary.
- `HADES.HAD_ARQUIVOS_REGS` and `HADES.HAD_VW_ARQUIVOS_REGS` for stored-resource candidates.
- Targeted text/blob candidates for stored XML/resources when local XML exists, runtime XML exists, local/runtime hashes diverge, local XML is missing, or browser debug implies DB-stored definitions.

Treat HADES registry output as metadata evidence, not as proof of actual browser-visible authorization. Button state still needs runtime confirmation in `browser-runtime.md`.

If Oracle execution is blocked, still create the SQL/helper artifact and a sanitized `oracle-results/*blocked*.md` note with the exact blocker. Do not leave `HADES_REGISTRY_NOT_CHECKED` only as prose in `phase-1-execution-gate.md`; the next developer must have a command or SQL file to run.

Use the orchestrator for the first pass:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\find_hades_screen_definition.ps1 `
  -Screen <SCREEN> `
  -MainView <MAIN_VIEW_FROM_XML_OR_RUNTIME> `
  -OutputDir docs\migracao\<SCREEN>\oracle-results
```

Add `-IncludeXmlMarkers` only when the first pass does not find the definition, and `-IncludeBlobSearch` only when a table/resource candidate makes BLOB sampling useful.

## Related Flow Rule

Every object or screen listed under `Related Flows` in the investigation must appear in the confirmation SQL seed list, a source-search term, or an explicit `SKIPPED` comment with the reason.

## Confidence Rule

If this SQL has not been executed, mark outputs based on it as `CONFIRMED_LOCAL_SOURCE` or `CANDIDATE_UNCONFIRMED`, not `CONFIRMED_ORACLE_METADATA`.

If the SQL has been executed, attach or summarize the result location in the investigation report before promoting evidence to `CONFIRMED_ORACLE_METADATA`.

## Oracle Dictionary Safety Notes

Do not select `STATUS` from `ALL_PROCEDURES`; that dictionary view does not expose object status in every supported Oracle version. For procedure/package validity, join or pair these views instead:

```sql
select owner, object_name, object_type, status
from all_objects
where owner = '<OWNER>'
  and object_name in ('<PACKAGE_OR_PROCEDURE>');

select owner, package_name, object_name, argument_name, position, sequence, data_type, in_out
from all_arguments
where owner = '<OWNER>'
  and (
    package_name in ('<PACKAGE>')
    or object_name in ('<PROCEDURE>')
  )
order by package_name, object_name, sequence;
```

Before closing the gate, scan every referenced `oracle-results/*.out.txt` file for `ORA-`, `SP2-`, `TNS-`, `ERROR:`, `Exception`, and `IllegalArgumentException`. If any execution error remains, either correct and rerun the SQL, or record an explicit blocker/residual such as `ORACLE_CONFIRMATION_FAILED` or `ORACLE_OUTPUT_ERROR_PRESENT`. Do not summarize a file containing an untriaged execution error as confirmed Oracle metadata.
