# Visual authoring preparation: dependencies and execution map

Classification: docs-apenas. Companion to
[the capability review](authoring-capability-review-2026-10-17.md).
This increment changes guidance and records investigation; it does not repair
component code, upgrade packages, author the complete target page or record a video.

## Agreed operation lane

The first video prioritizes visual controls to simulate human authoring. Record
each capability that needs a visible advanced JSON field instead of using JSON
as a speed shortcut. A second video may use LLM-authored component JSON more
extensively. Neither lane imports a completed page. Preparation, isolated probes
and startup work remain outside a future measured take.

## Dependency reconciliation

Baseline: canonical skills commit `e60031468ea6975afd3e57b91dc8b92204d7a138`.
The 12 previously edited entrypoints were already installed correctly, but 11
of their 34 distinct direct dependencies were outdated. Traversing the manifest
recursively produced 115 required skills, including 49 outdated installations.
All 49 matched the older workspace materialization before replacement; none
contained unexplained local changes. The canonical sync script installed the
selected closure. The full family audit then showed 139 OK, 29 DRIFT, zero
missing/source errors; all 115 selected trees were OK. The 29 remaining drift
entries are outside this closure. This is installation parity, not a runtime test.

The governance skill now requires transitive dependency checks for selective
installation. Updated guidance must be rehashed, validated, synchronized and
audited before closure of this increment.

A later shared-installation audit detected new edits in four required installed
skills: fields-inline-overlay-runtime, table-authoring-settings,
table-filter-actions and charts-echarts-engine-boundary. Their added guidance
concerns ongoing temporal controls, microvisualization presentation and table
filter ownership work. Those contents differ from this pinned source and were
not overwritten or silently included in its commit. After syncing this
increment's three edited skills, the shared comparison was 136 OK / 32 DRIFT,
with zero missing/source errors; 112 of the 116 task-required entries (the
original 115 plus authoring governance) were OK. A clean isolated source audit
remains distinct from shared-installation drift introduced during other work.
Before a timed rehearsal, coordinate writes to the shared installation and
reconcile these four changes against their canonical commits; do not repeat a
force sync over unexplained concurrent edits.

## Installed baseline and ownership

- Host: `praxis-hero-hq-ui`, official `http://127.0.0.1:4302`; package declarations
  and the installed Core/Charts/Page Builder packages use `10.0.0-rc.32`.
- Reference: `src/app/pages/dashboard/dashboard-page.definition.json`, containing
  13 widgets, four page data sources and one declared composition link.
- Empty target: `/comando-studio`; `autoPersist=true`. Inspection alone does not
  authorize insertion; an insertion exercise must include explicit restoration.
- Backend base: host `core/platform.config.ts` uses `/api` on localhost. The
  documented `proxy.conf.js` forwards `/api` and `/schemas`; its default target is
  `https://praxis-api-quickstart.onrender.com`. An environment override can change
  the effective target, so declarations alone do not prove the server reached.
- Canonical owners: Core for state/data-source/composition execution; Charts for
  chart document/catalog/runtime translation; Page Builder for editor/composer;
  component editors for child configuration; metadata starter for backend schema,
  resource and capability semantics. The host supplies its domain presentation.

## Widget map

All rows describe the reference configuration. Previous editor inspection is
separate from a new insertion/apply/save/reopen acceptance on this baseline.

| Widget key | Component/editor owner | Data and behavior | Required authoring proof |
| --- | --- | --- | --- |
| heroBanner | Rich Content | State-bound heading/actions and host radar media | Guided nested content, context binding, routes, actual media input editing |
| kpiProntidao | Rich Content | Active/total employees and derived readiness; RH navigation | Remote-source provenance, ratio, progress and action |
| kpiMissoes | Rich Content | Planned/in-progress/total missions; mission navigation | Correct planned ratio and badge, no copied fallback number |
| kpiFolha | Rich Content | Latest payroll aggregate; payroll navigation | Last bucket mapping, currency formatting; `folhaPercent` is initially supplied |
| kpiRiscos | Rich Content | Incident totals/severity; incident navigation | Counts, percentage, badge and zero/error handling |
| payrollChart | Charts | Remote timeseries with net-pay and deductions series | Catalog identity, eligible metrics, date window, canonical document and real data |
| reputationChart | Charts | Remote group-by by team with two average scores | Group/metrics, existing filter semantics, source provenance |
| incidentsSeverityDonut | Charts | Local rows bound to page remote aggregate state | Typed bindings; crossFilter -> recentIncidents.queryContext; native clear |
| defconGaugeChart | Charts | Local data bound to derived DEFCON | Explicit derived formula, scale 1..5, no claim of an independent backend KPI |
| distressSignalsList | List | Resource connection, newest calls, card slots/actions | Resource, sort, selection, virtualization acceptance, declared actions |
| recentIncidents | Table | Resource connection, columns, row details, microvisualization | Query/clear, paging, stable row identity, expansion and derived cell rendering |
| missionsTimeline | Rich Content | Authored editorial events plus state-bound summaries | Label editorial versus live fields; native actions and internal responsive layout |
| domainHub | Rich Content | Action-card grid with routes and state-bound summaries | Actual route payloads, keyboard activation and narrow layout |

These editorial KPI cards navigate; they are not filter emitters. A future card
filter must use an actual registered output/action and consumer query contract.
The reference's host CSS classes are not universal presets. Matching appearance
and improving design through available theme/layout controls needs separate proof.

## Declared read operations

The following operations are reads for statistics and collection filters. Paths include the
host's `/api` base. They are traced from configuration, not guessed from labels.

| Consumer/source | Method and path | Declared request |
| --- | --- | --- |
| heroesStats | POST `/api/human-resources/funcionarios/stats/group-by` | `field=ativo`, COUNT as total; map true/false and total |
| missionsStats | POST `/api/operations/vw-resumo-missoes/stats/group-by` | `field=status`, COUNT as total; map four declared states |
| payrollStats | POST `/api/human-resources/vw-analytics-folha-pagamento/stats/timeseries` | `field=competencia`, MONTH, SUM salarioLiquido; last bucket mapping |
| incidentsStats | POST `/api/risk-intelligence/vw-indicadores-incidentes/stats/group-by` | `field=severidade`, COUNT as total; map four severity groups |
| payrollChart | POST `/api/human-resources/vw-analytics-folha-pagamento/stats/timeseries` | MONTH, 2025-10-01..2026-03-31; SUM salarioLiquido and totalDescontos |
| reputationChart | POST `/api/human-resources/vw-ranking-reputacao/stats/group-by` | `field=equipe`, filter equipe `%`; AVG scorePublico and scoreGovernamental |
| distressSignalsList | POST `/api/operations/sinais-socorro/filter` | Catalog-discovered read operation, paging in query parameters, DTO in body; sort abertoEm descending |
| recentIncidents | POST `/api/operations/incidentes/filter` | Catalog-discovered read operation; queryContext receives severity |

Discovery uses `/schemas/catalog`, the operation-specific `/schemas/filtered`
contract and the exact capabilities href published by discovery. Do not rebuild
capability URLs from resource labels or confuse discovery with execution.

### Fresh HTTP evidence outside the browser take

The local server was initially absent: direct reads received connection refused,
while the already-loaded browser tab still displayed content. Restarted with
documented `npm start`; Angular's first-run telemetry prompt delayed startup.
Canceled the prompt and set `NG_CLI_ANALYTICS=false` only in the server process
environment. No workspace setting was edited. Bundle generation completed and
the official origin became available.

Read-only probes through that local origin, using the host's declared demo
tenant/user headers, returned HTTP 200 for all six statistics requests above,
`/schemas/catalog`, payroll collection capabilities, both collection filter
requests and both exact catalog-published filter request-schema links. The
catalog returned 1462 endpoint entries. Statistics responses use the envelope
`{ status, message, data, _links, timestamp }`; that envelope is not proof that
the editor's transform binds its inner data correctly.

Incidents query returned total 108; severity CRITICA returned 23; signals query
returned 20. These are observed counts, not fixtures or a browser cross-filter
acceptance. Diagnostic GET requests to the two collection base paths returned
405; the catalog then identified their POST `/filter` read operations. This
does not indicate a Table/List runtime defect.

The earlier employee-source HTTP 520 did not recur for the declared employee
statistics request. Its historical root cause remains unproved; do not carry it
forward as an active confirmed outage. No records were created or updated.

## Investigated impediments

### Composer: structural incompatibility, optional for this workflow

Installed Page Builder `composeCollectionScreen` generates `praxis-Card`,
`praxis-StatCard`, `praxis-Form`, `praxis-List` and `praxis-Table`. Installed Core
registry resolves exact IDs and explicit aliases, not case-insensitive names;
the installed component registrations use other canonical IDs. The loader's
missing-metadata branch returns without materializing the component.

Additional mismatches: external filters use `filterChange`; the inspected filter
contracts use other ports/envelopes. Detail wiring uses `rowClick` even for List,
whose item event is `itemClick`. KPI transformation assumes boolean groups while
the group field is configurable. Generation replaces the staged page structures.
No generator was executed. Independent source review confirms these structural
issues; it does not substitute for a browser reproduction of the resulting page.

Owner: Page Builder, consuming real registered presets, ports and schemas. Fixing
case or adding host aliases alone is insufficient. This optional composer is not
needed for per-widget authoring, so its repair is not an automatic prerequisite
for the requested first-video route.

### Chart catalog rejection: identity mismatch evidenced; new canonical chart exercised

The reference supplies runtime `config`, without `chartDocument`. Installed
Charts wrapper derives a document; its mapper prepends `/` to the relative
resource. Catalog resolution derives the operational path from capability hrefs.
Selector matching preserves the `api` segment. If the actual selected candidate
is `/api/human-resources/...`, it differs from the mapped `/human-resources/...`
and can explain `resource-stale`. The freshly read catalog publishes payroll
capabilities at `/api/human-resources/vw-analytics-folha-pagamento/capabilities`,
and its HTTP 200 capability payload confirms resourcePath
`/api/human-resources/vw-analytics-folha-pagamento`. Thus the identity mismatch is
supported by actual discovery and installed mapper behavior. A fresh canonical
chart has separate browser evidence below. Do not try prefixes until validation
passes.

Owner: Charts mapper/editor context and its operational-path contract. A new
canonical insertion preset must be evaluated independently from legacy-config
editor migration; success or failure of one does not certify the other.

### New canonical chart: visual-controls probe

Started from the empty Studio. Through the palette, selected half-width and
`Praxis Chart · Canonical chart`. Opened its content editor, then:

1. Dados -> Fonte: `praxis.stats`.
2. Recurso: the offered payroll analytics candidate; waited for capability
   resolution and the operation selector to become enabled.
3. Operação: série temporal.
4. Estrutura -> Dimensão: Competencia; Métrica: Salario Liquido; aggregation soma;
   changed metric label through its text input.
5. With no validation problems, used Salvar e fechar. The header acknowledged a
   saved layout. The first immediate runtime observation showed one point; it
   was not treated as a settled-data proof.
6. Reloaded the page. Runtime displayed 46 points. Reopened the content editor:
   no validation problems, `praxis.stats`, same resource, série temporal, and no
   previous local-data editor. The editor preview was explicitly synthetic and
   was not counted as live-query evidence.
7. Changed Granularidade from dia to mês through its selector, used Aplicar and
   Salvar e fechar, then inspected the runtime. Captured a screenshot of the
   resulting chart. The reference's exact date window, second series, style,
   interactions, narrow behavior and monthly-setting reopen were not exercised.
8. Used Mais ações -> Excluir widget, confirmed, observed an empty saved canvas,
   then Restaurar Padrão. The header showed Layout padrão. Exited customization
   and requested a reload. A final post-reload confirmation was not completed:
   the shared tab subsequently navigated to another task and was left untouched.

No JSON field was filled, page imported, browser state injected or source edited.
This proves a new canonical chart path and a save/reload/reopen case. It does not
repair or accept the legacy runtime-config migration, prove every chart family,
establish remote Config Store/ETag persistence, or constitute a timed take.

### Derived values: runtime passes; preview replacement reproduced

Instantiated installed `WidgetPageStateRuntimeService` with the reference state
and context in Node after loading Angular compiler. `buildRuntimeSnapshot`
returned zero diagnostics and all seven derived values: readiness 52.5, planned
mission ratio 38, incident ratio 24, badges 09/18, payroll million 3.09 and DEFCON
4.2. These are computations from reference initial values, not fresh API results.
No browser state was injected or changed. This narrows the earlier preview
diagnostic: expressions are not proved defective merely by that editor observation.
An isolated call to the installed editor's real `getDerivedStatePreview` method
then supplied four successful source previews from the reference fallback values
at the shared `kpis` target. It reproduced four invalid-comparison diagnostics
and retained only the derived values whose dependencies came from the last
source. `assignNestedValue` replaces that target object on each iteration. Core's
dynamic-page runtime instead shallow-merges object overlays at the same target.
This source/method reproduction explains the preview discrepancy; its inputs
were controlled values, not new live source previews or a browser regression run.

A small correction and regression specs are prepared separately in an isolated
Angular worktree, based on `47a3b56c9`, preserving concurrent changes in the main
Angular checkout. It combines object properties in the preview using the runtime
semantics, while arrays/scalars/null replace and failed/undefined previews leave
authored values intact. The patch does not change exported shapes or editor
markup. Independent semantic review is complete; focused Angular validation
and downstream adoption remain pending;
preparing it does not upgrade the Hero's installed rc.32 package.

An isolated verifier extracted the exact patched TypeScript method and its
seven-method helper set, transpiled them, and called the installed rc.32 Core
state runtime. It produced all seven reference-derived values with zero
diagnostics and passed 26 overlay/type/failed-preview cases while preserving
input state and source previews. Source SHA-256:
`93c355f9972539437401aa75671d90cd7f5a885285728374474dee4b5204f105`.
This is a method/runtime check, not the Angular TestBed suite or browser
acceptance of the patch. Four Angular regression specs are prepared; their
focused execution is a separate gate. Dependency installation in the isolated
worktree did not complete, including an offline-cache attempt. The task's
installer was stopped while the machine had approximately 730 MB free RAM and
other tasks were running; resource contention was observed, but the cause of
the incomplete installation was not established. Neither the Angular suite nor
a library build was run. No dependency declarations or lockfile were changed.

## Execution gates

1. Close installed guidance parity and capture source/package baselines.
2. Confirm official runtime and actual read/catalog responses. A cached loaded
   browser view is not proof that the local server still responds.
3. Exercise a disposable canonical chart through visual source controls, settled
   Apply, save/reopen and restored empty state before multiplying components.
4. Prove source/derived bindings and the cross-filter/clear path through editors.
5. Complete all agreed widgets, desktop/narrow UX and persistence before timing.
6. Run a complete continuous rehearsal, counting waits and verification. No
   under-ten-minute claim is made by this investigation or by historical recipes.

No runtime code repair is published by this skills documentation increment.
The isolated Angular patch is classified local-pequena: canonical owner Page
Builder, consumers of shared-target source previews affected, focused editor
specs required, no breaking schema/API change. The README/skill explanation of
preview parity is the relevant derived documentation; no metadata/AI registry
shape, HTTP corpus or public export changes are introduced. Its validation and
downstream adoption must close before a recording can rely on corrected preview.
