# Legacy Architecture And Documentation Map

Use this reference when `docs-legado/v7x` exists in the migration workspace. This tree is a packaged legacy baseline: application resources, database DDL, generated PL/SQL, Enterprise Architect exports, help/manuals, workflow assets, Forms/Reports, and internal specifications live side by side.

Documentation is a first-class discovery layer, but not the final authority for implementation. Use it to understand architecture, business meaning, model neighborhoods, related flows, and parity cases. Confirm implementation behavior through browser/runtime, Archon XML, local source, and Oracle metadata.

## Legacy Architecture At A Glance

The legacy stack is split across these evidence layers:

| Layer | Where It Lives | What It Usually Contains | Migration Use |
| --- | --- | --- | --- |
| Archon Java screens | `java/techne-archon-ergon/src/main/resources/techne/archon/ergon/crodata/trans/<Modulo>/<SCREEN>.xml` | Screen XML, blocks, `sqlSelect`, `sqlParameters`, actions, tabs, links, hidden fields | Primary screen definition and Oracle seed source |
| Archon controllers | `java/techne-archon-ergon/src/main/java/techne/archon/ergon/controller/<modulo>/<SCREEN>.java` and `<SCREEN>impl.java` | Controller hooks, custom events, integration code | Runtime behavior candidates and parity checks |
| Database object source | `aps/` and `aps/fontes_ergon/` | Tables, constraints, indexes, views, packages, functions, generated object history | Local DDL/source evidence before Oracle confirmation |
| HADES registry | Oracle HADES schema plus `aps` HADES files | Transaction registry, access patterns, generated object metadata, options | Screen registration, authorization metadata, generated helpers |
| Enterprise Architect exports | `EA/*.xml` and zipped EA projects | UML/screens/entities with `documentation` attributes, base tables/views, fields, LOVs, routines | Business/UI/model context; field and flow explanations |
| Model help | `help/ergon_modelagem.zip` | RoboHelp model topics, E/R diagram pages under `ESTRUTURA/`, function docs | Domain model neighborhoods and entity diagrams |
| Reference help | `help/ergon_referencia.zip` | Business concepts under `conceito/`, form help under `form/`, characteristics under `caracteristica/` | Business semantics, user-facing concepts, legacy form references |
| Internal docs | `docs/Interno/**` | Functional specs, technical specs, module docs, architecture notes, implementation practices | Requirements, rules, change rationale, screen/task specs |
| Workflow | `workflow/**` | `.wft`, workflow docs, workflow PL/SQL and message routines | Pending/approval flows and side effects |
| Oracle Forms | `forms/**` | `.fmb`, `.fmx`, model forms, older form assets | Historical screen predecessor candidates; binary unless extract tooling exists |
| Reports | `reports/**` | `.rdf` and report assets | Report flows and output parity candidates |
| Web/Portal | `web/**`, `paginas_cronosjava_portal/**`, `docs/Interno/Modulo.Portal/**` | ASP/portal pages, portal specs, static assets | Related self-service flows, portal parity, historical endpoints |
| Customizations | `javacust/**`, `javacust680/**`, client/module folders | Client-specific overrides and custom Java/resources | Environment/client variation; inspect when target screen may be customized |

## Naming Patterns

Use these patterns to find evidence for any screen. Examples are illustrative only; derive the real terms from the target screen.

| Artifact | Pattern | Example |
| --- | --- | --- |
| Archon XML | `<SCREEN>.xml` under `crodata/trans/<Modulo>/` | `Administracao/ERGadm00189.xml` |
| Java controller | `<SCREEN>.java`, `<SCREEN>impl.java` | `ERGadm00189.java`, `ERGadm00189impl.java` |
| Screen view | `<screen>_<business>.vw` in `aps/fontes_ergon` | `ergadm00189_frequencias.vw` |
| Table DDL patch/history | `<table>.tab` | `frequencias.tab` |
| Primary/unique keys | `<table>.pk`, `<table>.uk` | `frequencias.uk` |
| Constraints/FKs | `<table>.con` | `frequencias.con` |
| Indexes | `<table>.ind` | `frequencias.ind` when present |
| Sequences | `<table>.seq` | `regras_grupo_freq_seq.seq` |
| PL/SQL source | `*.pks`, `*.pkb`, `*.prc`, `*.fnc`, sometimes under `aps/fontes_ergon` | `ergadm00349_freq_data.fnc` |
| HADES/Ergon generated metadata | `HAD*`, `ERG_*`, `PCK_*`, `T_*` names in `aps` and Oracle | `HADADM00019_TRANSACAO`, `T_B_IUD_FREQUENCIAS` |
| Enterprise Architect docs | `EA/*.xml`, search by screen, table, view, visible title, business term | `EA/Portal.xml` |
| Help model topics | `help/ergon_modelagem.zip > ESTRUTURA/*.html` | `02500_frequencias.html` |
| Reference help topics | `help/ergon_referencia.zip > conceito/*.html` and `form/*.html` | `visao_geral_de_frequencia_c.html` |
| Functional/technical specs | `docs/Interno/Especificacoes.*`, `docs/Interno/Modulo.*`, `docs/Interno/Ergon_NG` | specs named by module, business process, task, or screen title |

## Discovery Inputs

For every screen, derive search terms from multiple layers:

- Screen code: `<SCREEN>`.
- Numeric suffix: the numeric part of `<SCREEN>`, when present.
- Module folder from XML path or URL, such as `Administracao`, `Portal`, or `Pericias`.
- Visible title from browser/XML.
- Main screen view from XML/runtime.
- Base table(s) from view/XML/Oracle.
- Lookup/security/helper objects introduced by SQL, filters, links, packages, or triggers.
- Business synonyms from title, labels, help docs, and table names.
- Related screens and linked components from XML.

Do not rely only on the screen code. Many useful documents are named by module, business concept, table, or task number rather than by transaction.

Example term set for a frequency screen:

- Screen code: `ERGadm00189`
- Numeric suffix: `00189`
- Visible title: `Frequencias`
- Main screen view: `ERGADM00189_FREQUENCIAS`
- Base table: `FREQUENCIAS`
- Related objects: `TIPO_FREQ`, `CODIGOS_FREQ`, `MOSTRA_FREQ`, `PCK_FREQUENCIAS`
- Business terms: `frequencia`, `freq`, `licenca`, `afastamento`

## Where To Look By Question

| Question | First Places To Check | Evidence Type |
| --- | --- | --- |
| What SQL does the screen run? | Archon XML, browser debug/runtime, `aps/fontes_ergon/*.vw` | `CONFIRMED_XML`, `CONFIRMED_RUNTIME`, `CONFIRMED_LOCAL_SOURCE` |
| What does this field mean? | EA XML `documentation`, reference help, functional specs, XML labels | `CONFIRMED_LOCAL_DOC` plus XML/source |
| Which table/view backs this grid? | XML `sqlSelect`, EA docs `TABELA / VIEW BASE`, view source, Oracle dependencies | XML/source/Oracle |
| What are the keys and constraints? | Oracle metadata, `aps/*.pk`, `aps/*.uk`, `aps/*.con`, `aps/*.ind` | Oracle preferred; local DDL as support |
| What are valid write paths? | XML edit routines, `db:*`, Java controller, DML packages, triggers, `aps` packages, Oracle grants | XML/source/Oracle |
| Which users may see/edit data? | HADES access registry, XML hidden fields, security helper functions, docs on profiles, Oracle package source | Mixed; runtime still required |
| Which related flows matter? | XML links/tabs/popups, EA docs, help topics, portal specs, workflow files | XML/runtime first; docs for context |
| What parity tests are needed? | Browser workflow, functional specs, reference help, EA docs, workflow docs | Runtime plus docs |
| Is this a portal/self-service flow too? | `web/**`, `paginas_cronosjava_portal/**`, `docs/Interno/Modulo.Portal/**`, `EA/Portal.xml` | Local docs/source |
| Is there client-specific behavior? | `javacust/**`, `javacust680/**`, client/module folders, task specs | Local source/doc candidate |

## Search Procedure

1. Locate Archon XML and controller:

```powershell
$screen = "<SCREEN>"
rg --files docs-legado\v7x\java | rg -i "$screen(\.xml|\.java)|${screen}impl"
```

2. Locate local database source and DDL by screen view, base table, and related objects:

```powershell
$mainView = "<MAIN_VIEW>"
$baseTable = "<BASE_TABLE>"
$relatedObjects = "<RELATED_OBJECT_1>|<RELATED_OBJECT_2>"
rg --files docs-legado\v7x\aps |
  rg -i "($screen|$mainView|$baseTable\.(tab|pk|uk|con|ind|seq)|$relatedObjects)"
```

3. Search text-like architecture/docs sources:

```powershell
$suffix = "<NUMERIC_SUFFIX>"
$titlePattern = "<TITLE_OR_BUSINESS_TERMS>"
rg -n -i "$screen|$suffix|$titlePattern|$mainView|$baseTable" `
  docs-legado\v7x\EA docs-legado\v7x\docs docs-legado\v7x\workflow `
  -g "*.{xml,txt,html,htm,sql}"
```

4. Search help ZIP indexes without unpacking everything:

```powershell
$businessPattern = "<BUSINESS_TERM_1>|<BUSINESS_TERM_2>|<TABLE_OR_TOPIC_HINT>"
tar -tf docs-legado\v7x\help\ergon_modelagem.zip |
  rg -i "$businessPattern|estrutura"

tar -tf docs-legado\v7x\help\ergon_referencia.zip |
  rg -i "$businessPattern|conceito|form/"
```

5. Extract only the needed help topic:

```powershell
tar -xOf docs-legado\v7x\help\ergon_referencia.zip `
  <path/from/zip/listing.html>
```

Example for ERGadm00189:

```powershell
$screen = "ERGadm00189"
$mainView = "ERGADM00189_FREQUENCIAS"
$baseTable = "FREQUENCIAS"
$businessPattern = "frequ|licenca|afastamento"

rg --files docs-legado\v7x\java | rg -i "$screen(\.xml|\.java)|${screen}impl"
rg --files docs-legado\v7x\aps | rg -i "($screen|$mainView|$baseTable\.(tab|pk|uk|con|ind|seq)|tipo_freq|codigos_freq)"
tar -tf docs-legado\v7x\help\ergon_referencia.zip | rg -i "$businessPattern|conceito|form/"
```

6. For `.docx` specs, read `word/document.xml` directly instead of creating converted files:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$docx = "docs-legado\v7x\docs\Interno\Modulo.Portal\Especificacoes.Funcionais\<file>.docx"
$zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $docx))
$entry = $zip.GetEntry("word/document.xml")
$reader = [IO.StreamReader]::new($entry.Open())
$xml = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()
($xml -replace "<[^>]+>", " " -replace "\s+", " ").Trim()
```

7. Treat `.doc`, `.pdf`, `.vsd`, `.ppt`, `.xls`, `.fmb`, `.rdf` as candidate documents unless there is a configured extractor. Prefer filename/path evidence first; extract only when the candidate looks relevant.

## Evidence Rules

- Use `CONFIRMED_LOCAL_DOC` for facts found only in legacy documentation.
- Use docs to explain business meaning and candidate parity cases, not to override runtime/XML/Oracle evidence.
- Promote a documented table/view/function to implementation evidence only after XML/runtime/local source/Oracle confirms it.
- Record path, topic/file name, and a short summary or compliant snippet. Do not paste long Word/PDF/manual passages.
- For ZIP help files, list or extract only the relevant topic. Do not unpack entire help archives into the repository.
- For binary artifacts, record the candidate path and why it matters; do not claim content until extracted.

## Output

Create `legacy-doc-sources.md` in the screen package and summarize:

- Search terms used.
- Folders and archives searched.
- Files/topics matched.
- Business facts found.
- Model/DDL facts found.
- Candidate parity cases or related flows.
- What was not found.
- Which facts were promoted to the main investigation and at what confidence.
