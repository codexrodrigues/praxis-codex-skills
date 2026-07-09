# Case Review: ERGadm00189

Use this review to improve future screen investigations. It records what the real case changed in the skill.

## Step Review

| Step | Result | Skill Adjustment |
| --- | --- | --- |
| Local XML discovery | Successful. `ERGadm00189.xml` exposed page title, parameters, main grid SQL, pending grid, write routine, tabs, and links. | Keep XML/debug as the seed source before Oracle. |
| Local source discovery | Successful. `ergadm00189_frequencias.vw` confirmed view shape and base objects. | Keep local source as `CONFIRMED_LOCAL_SOURCE` until Oracle execution. |
| Oracle provisioning | Successful after standardizing `secrets/ergon.env.ps1`, `ERGON_HADES_CONN`, `ERGON_SQLCL`, and `tools/sqlcl`. | Skill now documents Codex-operated DB access instead of developer-run scripts. |
| SQLcl execution | Failed in Codex non-interactive Windows execution with `java.io.IOException: Funcao incorreta`. | Added JDBC fallback runner using SQLcl bundled `ojdbc11.jar`. |
| Confirmation SQL execution | Successful via JDBC fallback. Seed objects, synonyms, dependencies, columns, constraints, indexes, triggers, grants, arguments, source search, and smoke counts executed. | Skill now documents fallback execution and `-MaxRows`. |
| Grants query | Initial failure: `ALL_TAB_PRIVS` did not expose `OWNER`; correct column was `TABLE_SCHEMA`. | Updated Oracle query reference to use `table_schema owner`. |
| Source search | Initial search was too broad because `%FREQUENCIAS%` produced noisy output. | Template now recommends narrow screen/helper source search plus separate write-risk search. |
| Write risk | Confirmed as non-trivial: `ERG_DML_FREQ_FORMATO`, `ERG_DML_FREQUENCIAS`, `T_A_IUD_FREQUENCIAS`, `T_B_IUD_FREQUENCIAS`, `PCK_FREQUENCIAS`, and `PCK_FREQUENCIAS_PND` are involved. | Write APIs remain blocked until detailed write contract and parity tests exist. |
| API key | `ID_REG` exists on view/table and is a better candidate than `ROWID_REG`, but uniqueness and URL contract still need confirmation. | API template should keep key decision explicit and block detail/write endpoints until resolved. |
| Browser confirmation | User opened the direct screen URL. Chrome plugin then operated an authenticated tab, selected a vinculo, and confirmed a real grid row. DOM locators were unstable, but CUA-style clicks and screenshots worked. | Prefer the authenticated browser surface available in the session. Use Chrome when the user requests it or the session/profile is already there; use Playwright mainly as fallback/smoke tooling. |
| HADES screen registry | Successful. `HADES.TRANSACAO` / `HADADM00019_TRANSACAO` identify `ERGadm00189` as `Frequencias`; `HADADM00015_TRANSPADACES` / `HADADM00023_TRANSPADACES` show `PDNV` with create/edit/delete allowed. | Skill now includes HADES registry/XML discovery before declaring XML unavailable. |
| HADES text search | Successful after narrowing. Text search found registry/access references for `ERGadm00189`; no text hit for `ERGADM00189_FREQUENCIAS`. Broad `HAD%` scans timed out until noisy tables were excluded and the orchestrator defaulted to `HADADM%`. | Added `find_hades_screen_definition.ps1`, table exclusion defaults, and narrower first-pass behavior. |
| HADES BLOB search | Narrow BLOB search over `HAD_ARQUIVOS_REGS` found no text-like `ERGadm00189` hit in sampled bytes. Oracle RAW sampling required a conservative 2000-byte limit. | Added `search_oracle_blob_text.ps1`; use only for targeted candidates or with explicit deep-search intent. |
| Write deferral | Detailed write-risk query showed `ERG_DML_FREQ_FORMATO` has many arguments, validates quantity/code formats, receives publication fields, and runs under audit/pending triggers/packages. | Add `write-risk.md` and `write-risk-detail.sql` to screen packages; let read API proceed only when write is explicitly blocked/deferred with evidence. |
| Architecture pattern | v7x docs showed `ERG_DML_*` generation through `ERG_REGERA_PROCS_DML`, generated trigger/audit creation through `ERG_GERA_TRIGGER_AUDIT`, central pending flow through `PACK_ERG_PEND`/`ERGadmREGPEND`, and reusable publication/legal blocks. | Added `archon-write-patterns.md`; future write investigations must check generated DML, table triggers/packages, `FLAG_PACK`, pending packages, publication, and legal-document coupling before API design. |
| API contract | The first useful API slice is read-first: list frequencies by servidor/vinculo, lookups for type/code, and possibly detail by `ID_REG` after uniqueness is proven. Write endpoints remain blocked by generated DML, triggers, pending, publication, legal documents, and session context. | Added `api-design-patterns.md`; future API contracts must classify endpoints as `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`, with keys, DTOs, pagination, capabilities, errors, and parity cases. |
| FieldSpec contract | API creation in this workspace should follow `lib-ui-fieldspec`: resource controller/service, `GenericFilterDTO`, `@UISchema`, `OptionDTO`, `RestApiResponse`, `/filter`, `/options/*`, `/by-ids`, `/schemas`, and explicit disabled/501 write/cursor/locate/stats decisions. | Added `lib-ui-fieldspec-api.md`; API contracts must include FieldSpec resource mapping and x-ui field metadata before implementation handoff. |

## Resulting Rules

- Do not ask developers to run normal Oracle confirmation manually; Codex should run it when access is provisioned.
- Keep `secrets/` and `tools/sqlcl/` out of Git.
- Prefer `ERGON_HADES_CONN` and `ERGON_SQLCL` in this migration workspace.
- Use SQLcl first; if it fails under non-interactive Codex execution, use `run_oracle_query_jdbc.ps1`.
- Use `-MaxRows` to prevent source/dependency sections from overwhelming the report.
- Use the Codex in-app browser as the primary authenticated runtime surface; have the developer log in once, then let Codex inspect the live session when browser tooling is available.
- If the user asks to use Chrome or the authenticated session is in Chrome, use the Chrome plugin instead of forcing Playwright. Legacy DOM locators may be unreliable; screenshots plus coordinate/CUA actions are acceptable evidence when recorded clearly.
- Check HADES transaction/access registry tables for the screen code: `TRANSACAO`, `HADADM00019_TRANSACAO`, `TRANSPADACES`, `HADADM00015_TRANSPADACES`, and `HADADM00023_TRANSPADACES`.
- Use `find_hades_screen_definition.ps1` as the first stored XML/resource pass; use `search_oracle_text.ps1` and `search_oracle_blob_text.ps1` for targeted follow-ups.
- Keep HADES text/blob searches narrow. Default exclusions avoid large log/process tables; override only when there is a specific reason.
- Do not use broad `ALL_SOURCE` terms for common table names. Search exact helper/package names, then run a separate targeted write-risk query.
- Promote to `CONFIRMED_ORACLE_METADATA` only after the output file proves the object, dependency, or field.
- Treat write deferral as a positive closure outcome when the first migration phase is read-only: document the routines, triggers, audit, pending, publication, and parity blockers instead of leaving write as an open unknown.
- Do not model write endpoints as direct CRUD until the generated DML architecture is checked: `recordPanelEdit`/`db:*`, `ERG_DML_*`, `HAD_GERA_PROC_DML`, `PP_%` arguments, generated table triggers/packages, `FLAG_PACK`, `_PND` packages, `PACK_ERG_PEND`/`PACK_HAD_PEND`, `HADadm_blk001`, and `ERGadm_blk004`.
- For API handoff, start read-first unless the user explicitly asks for write implementation and `write-risk.md` is closed. Keep detail endpoints as `Candidate` until the stable public key is proven, and keep write endpoints `Blocked` or `Deferred` with exact legacy blockers.
- Do not design ERGadm00189 APIs as ad hoc `/search` or table CRUD endpoints when `lib-ui-fieldspec` resource endpoints cover the use case. Use `/filter` for the grid, `/options/filter` for type/code lookups, and `@UISchema` for labels/control metadata.
