# Codex Browser Runtime Capture

Use this reference when the developer has the legacy Ergon screen open in the Codex in-app browser.

## Goal

Capture user-visible behavior and runtime/debug evidence from the authenticated legacy session without storing credentials or broad page dumps.

## Capture Rules

- Treat the Codex in-app browser as the preferred runtime surface for authenticated legacy screens.
- Ask the developer to log in manually when needed, then continue from the authenticated page.
- Record concise facts, not full HTML dumps.
- Do not store credentials, session tokens, cookies, or screenshots containing sensitive personal data.
- Mark developer-relayed visible facts as `CONFIRMED_RUNTIME_MANUAL` until Codex-readable browser/debug evidence verifies them.
- Mark SQL, bind order, hidden fields, and permission logic as `CONFIRMED_RUNTIME` only when captured from browser debug, network/runtime panels, XML/debug output, or another reproducible artifact.

## Minimum Capture

For each screen, create or update `browser-runtime.md` in the screen package:

```text
docs/migracao/<SCREEN>/browser-runtime.md
```

Record:

- Current URL and whether it was direct navigation or menu/search.
- Page title, module, and visible breadcrumb/menu path.
- Main visible blocks, grids, tabs, and row count/page size.
- Required selectors before data loads, especially servidor/vinculo/company fields.
- Enabled/disabled state for `Novo`, `Editar`, `Apagar`, `Salvar`, `Cancelar`, and popup actions.
- Default values and empty/null behavior for filters.
- Runtime/debug `sqlSelect`, `sqlParameters`, bind values, hidden fields, and component ids when available.
- Every popup/linked screen opened from the page, including parameters passed.
- Validation messages and authorization failures observed during safe read-only exploration.

## Factory-Assisted Capture

When the migration factory is available and local credentials were provisioned
through `secrets\ergon.env.ps1`, prefer the sanitized helper before asking the
developer for manual browser notes:

```powershell
.\tools\migration-factory\capture-browser-runtime.ps1 -Screen <SCREEN>
```

The helper opens the authenticated `.tp`, waits for default load, captures a
sanitized runtime sample, row texts, pagination, URL and title, and stores the
evidence under `docs/migracao/<SCREEN>/browser-evidence/`. It must not persist
usernames, passwords, cookies, tokens or broad HTML dumps.

When DOM inspection succeeds, the evidence includes a structured `runtime`
object with final URL/title, footer row count, pagination, table column samples,
filter controls/defaults, candidate action states, and a selected-row text
candidate. The canonical Phase 1 artifact generator consumes this structure and
also remains backward-compatible with older `cliOutputSanitized` evidence that
contains a parseable `### Result` JSON block.

Interpret helper status conservatively:

- `captured`: the screen loaded and a non-empty runtime fixture was observed.
- `captured_empty_fixture`: the screen loaded, but the main business grid was
  empty. Keep Phase 1 blocked for parity/API readiness until a representative
  fixture/context is found or the empty state is explicitly accepted.
- `blocked`: the screen was not confirmed. Investigate login, direct URL/menu
  access, authorization, unstable DOM or legacy errors before relying on XML
  alone.

The helper recognizes both legacy pagination forms, including
`Exibindo registros X - Y de N` and `Exibindo N registro(s) de N`. If it
misclassifies a visible non-empty page, fix the helper or record a manual
`CONFIRMED_RUNTIME_MANUAL` note and keep the gate blocked until reproducible
evidence exists.

XML-derived payload candidates can reduce manual work, but they do not replace
runtime evidence for default filter values, real bind values, selected-row key,
authorization/scope, button state, pagination/order, empty-state behavior and
read parity fixtures.

Structured browser capture can close only the visible/default-load portions it
actually observed, such as non-empty fixture, row count, visible columns,
filter controls and candidate button state. Keep Phase 1 blocked for API
handoff until actual runtime/debug bind values, public key decision,
authorization/scope and endpoint parity are captured or explicitly deferred.

## Opening The Target Transaction

When the authenticated browser is at the Ergon Home/Menu screen, do not assume the developer knows the navigation path. Drive the navigation explicitly:

1. Confirm the visible logged-in user, visible company, current URL path, and current menu/home transaction.
2. Click or focus the top search field labeled like `Buscar transacao`.
3. Type the target transaction code, for example `ERGadm00033`. If the screen is better known by title, search the title only after the code search fails.
4. Wait for search results or autocomplete. Record the exact result text shown.
5. Select the result that matches the target code/title. Do not guess a final URL unless menu search is unavailable.
6. Wait for the screen to load and record final URL path, visible title, breadcrumb/module, and whether a grid/form is visible.
7. If the search returns no result, capture that fact and then try the area menu path from the left/home menu, recording every click label.
8. If neither search nor menu opens the screen, mark runtime navigation as `Blocked - screen not reachable for current user` and continue from XML/Oracle only.

For screens opened by direct URL, still perform a menu/search lookup when practical. This proves that the target user can reach the transaction through the legacy navigation, not only by URL.

Use `CONFIRMED_RUNTIME_MANUAL` for visible navigation facts relayed by the developer. Promote to `CONFIRMED_RUNTIME` only when Codex or a saved debug/runtime artifact verifies the facts.

## Runtime Status

Use these statuses in the investigation:

- `Missing`: no authenticated browser observation.
- `Partial`: screen is open or some visible facts are recorded, but not all critical workflows are exercised.
- `Complete`: default load, filters, tabs, links, visible permissions, and runtime/debug SQL or an explicit “debug unavailable” note are recorded.

## Suggested Capture Shape

```markdown
# <SCREEN> Browser Runtime Capture

## Session

- Captured at:
- Browser surface: Codex in-app browser / Chrome / Playwright fallback
- URL:
- Navigation: direct URL / menu search
- Search term:
- Selected result:
- Title:
- Module:
- Browser status: Partial / Complete

## Navigation

| Step | Action | Observed result | Confidence |
| --- | --- | --- | --- |
| 1 | Start from Home/Menu |  |  |
| 2 | Search transaction code/title |  |  |
| 3 | Select menu/search result |  |  |
| 4 | Confirm loaded screen |  |  |

## Visible UI

| Area | Visible Label | Component Id | State | Notes |
| --- | --- | --- | --- | --- |

## Runtime Parameters

| Component | Token / Field | Observed Value | Trigger | Notes |
| --- | --- | --- | --- | --- |

## Actions

| Action | Visible State | Result | Parameters / Destination | Notes |
| --- | --- | --- | --- | --- |

## Debug / XML Runtime Evidence

| Evidence Type | Component | Snippet / Object Seeds | Confidence |
| --- | --- | --- | --- |

## Gaps

- 
```
