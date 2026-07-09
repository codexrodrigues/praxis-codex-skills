# Praxis Screen Composition For Legacy Ergon Screens

Use this guide when the legacy XML has multiple blocks, tabs, forms, and tables.

## Tab Classification

Every legacy tab must be assigned one composition type before Angular work starts.

| Legacy tab type | Angular/Praxis composition | Backend contract |
|---|---|---|
| Same record detail fields | Tab with schema-driven dynamic form/read-only form | Same response/detail DTO, grouped with `@UISchema` metadata when supported |
| Large detail form not useful in grid | Detail panel tab loaded after row selection | `findById` or detail endpoint; keep grid DTO lean if needed |
| Child table dependent on selected row | Tab with nested `praxis-table` | Child resource with parent id filter/context |
| Child form/list that has its own lifecycle | Embedded resource route/component | Separate resource API and command APIs |
| Reusable platform feature, e.g. legal documents | Shared embedded feature | Dedicated reusable API/component, not duplicated per screen |
| Legacy usage/help/instruction tab | Usually omit or move to help docs | No business API unless explicitly required |
| Hidden rowid/session bridge | Backend-only context | Do not publish ROWID/session values in DTO/x-ui |
| Tab with no ready API | Disabled/deferred tab with documented gap | `ui-api-readiness.md` marks gap/blocked/deferred |

## DTO Ownership

Do not create one DTO merely because the legacy XML has one tab. Create DTOs around API resources and operations.

| Situation | DTO strategy | Reason |
|---|---|---|
| Main table/list | `ResourceDTO` + `ResourceFilterDTO` | Drives `praxis-table`, inline filters, sorting, paging, and `/schemas/filtered`. |
| Same-resource detail tab with few extra fields | Reuse `ResourceDTO` or detail schema group | Fastest path; Praxis can render groups/tabs from one schema when the fields share lifecycle. |
| Same-resource detail needs many fields not shown in list | `ResourceSummaryDTO` for table and `ResourceDetailDTO` for detail | Keeps grid payload lean while preserving full detail parity. |
| Child table under selected row | `ChildDTO` + `ChildFilterDTO` with public parent id | Lets nested `praxis-table` use its own schema, filters, paging, and options. |
| Child form with independent create/edit/delete | `ChildDTO`, `ChildFilterDTO`, and command DTOs | Separate lifecycle and validation require separate contract. |
| Shared platform feature used by many screens | Shared feature DTOs | Avoids duplicating legal documents, publications, attachments, workflow, or audit contracts per screen. |
| Command action on selected record | Command DTO, not the read DTO | Write semantics, validation, and audit differ from read/list fields. |
| Context/hidden legacy state | No public DTO field | Resolve in backend session/adapter. |

Use the smallest DTO family that lets Praxis generate the UI without hand-coded adapters. If a tab can consume an existing resource schema, reuse it. If it has independent filters, paging, commands, or lifecycle, it needs its own resource DTO family.

## Angular Pattern

Prefer this structure for migrated screens:

1. Main page component owns route, title, layout, selected row state, and action availability.
2. Main `praxis-table` renders the primary resource and schema-driven filters.
3. Row selection populates a compact detail region.
4. Tabs under the detail region render:
   - schema-driven detail form for same-resource fields;
   - nested `praxis-table` for child resources;
   - shared feature component for reusable capabilities;
   - disabled/deferred placeholder only when the API gate is not ready.
5. Write buttons are enabled only from capabilities/command gates, not copied from the legacy XML.

Screen-local Angular config is composition only. A local `FormConfig` may control sections, rows,
columns, tab placement, density, and presentation mode, but it must not become the source of labels,
icons, helper text, tooltips, business descriptions, governance, AI policy, or code/description
translation. If the UI needs those values and the schema does not provide them, return to DTO/schema
hardening or record a Praxis platform gap.

For read-only detail tabs, prefer `PraxisDynamicForm` presentation mode backed by DTO/schema. When
legacy fields have both code and description, choose the display contract in the API/schema before
building the Angular layout; do not encode screen-specific concatenation rules in the component.

## Parent-Child Wiring

For child tables/forms, do not pass legacy `rowid` to the UI. Use a public parent id from the selected row.

Recommended backend options:

- Child `FilterDTO` has a public parent id field such as `codigoFrequenciaId`.
- Backend maps the public id to legacy keys internally.
- Session/company context stays server-side.
- Child resource exposes its own `/filter`, `/schemas/filtered`, and options metadata.

## ERGadm00034 Example

Legacy tabs:

- `Detalhes`: same selected codigo de frequencia record. Use read-only dynamic form initially; enable edit only after write API gates.
- `Documentos legais`: related/reusable legal document feature. The XML uses `CODIGOS_FREQ_` and legacy `rowid`; Angular should not receive rowid. Model this as a child/reusable feature keyed by public codigo-frequencia id, or defer the tab until the legal-documents API exists.

ERGadm00034 semantic lesson:

- The DTO can be technically complete and still not ready if public labels are unaccented, helper
  text is absent, boolean/flag descriptions only say "checkbox legado", icons are chosen from the
  column name instead of domain meaning, or fields such as `sexo`/`tipoPreenchimento` have
  description fields that the UI cannot consume cleanly.
- This must be resolved in DTO/schema metadata and schema tests before repeating the pattern on
  other screens.
