# Runtime Capture Form

Use this form while the authenticated legacy screen is open in the Codex in-app browser.

Do not paste credentials, cookies, tokens, full HTML, or screenshots with sensitive data.

## 1. Navigation

| Item | Value |
| --- | --- |
| Entry point used |  |
| Menu/search term |  |
| Selected menu result text |  |
| Final URL |  |
| Visible title |  |
| Visible module/breadcrumb |  |
| Debug/XML/runtime panel available? | yes / no |

## 2. Session Context

| Item | Value |
| --- | --- |
| Visible/current company |  |
| Visible/current user, if shown without sensitive data |  |
| Transaction shown in debug/runtime, if available |  |
| Screen opens with data before required selectors? | yes / no |

## 3. Required Selectors

| Field | Visible Label | Observed Value | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. Main Grid Runtime Binds

Capture default values first, then change one filter at a time.

| Bind Order | Token | Default Value | Changed Value | Trigger/Action |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 4.1 Read Filter And Paging Exercises

Exercise every read behavior that the Java API or migrated UI will need. If a field cannot be exercised, record why.

| Behavior | UI action | Legacy result summary | API/filter implication | Captured? |
| --- | --- | --- | --- | --- |
| Default load | Open screen with default selectors |  |  | yes / no |
| Text search | Type a representative search term |  |  | yes / no |
| Exact/code filter | Filter by a known code/id |  |  | yes / no |
| Empty/null filter | Clear filters and reload |  |  | yes / no |
| Company/scope selector | Change selector if safe |  |  | yes / no |
| Pagination next/previous | Move pages |  |  | yes / no |
| Sort/order | Observe or change ordering if UI allows |  |  | yes / no |

## 5. Main Grid Visible Behavior

| Item | Value |
| --- | --- |
| Rows loaded after required selectors? | yes / no |
| Page size, if visible |  |
| Visible default sort |  |
| Visible columns |  |
| Hidden/key fields shown in debug, if any |  |
| Selected row exposes chosen API key? | yes / no / not visible |
| Selected row exposes internal legacy row locator such as `ROWID`/`ROWID_REG`? | yes / no / not visible |
| Detail panel changes when row is selected? | yes / no |

## 5.1 Selected Row Correlation

| Item | Value | Evidence | API Decision |
| --- | --- | --- | --- |
| Public API key candidate |  |  | expose / not expose |
| Internal legacy key or row locator |  |  | keep internal / expose with justification |
| Matching Oracle row proof |  |  |  |
| Related action locator, such as publication/anulacao field |  |  | keep internal / defer |

## 6. Actions

Only observe button state unless a safe read-only click is clearly needed.

| Action | Visible State | Safe Result Observed | Parameters/Destination |
| --- | --- | --- | --- |
| `Novo` | enabled / disabled / hidden |  |  |
| `Editar` | enabled / disabled / hidden |  |  |
| `Apagar` | enabled / disabled / hidden |  |  |
| `Salvar` | enabled / disabled / hidden |  |  |
| `Cancelar` | enabled / disabled / hidden |  |  |
| Popup/link | enabled / disabled / hidden |  |  |

## 7. Runtime SQL/Debug

If the legacy screen exposes debug/runtime SQL, capture only concise snippets.

| Evidence | Captured? | Notes |
| --- | --- | --- |
| main grid `sqlSelect` | yes / no |  |
| main grid `sqlParameters` | yes / no |  |
| actual bind values after default load | yes / no |  |
| actual bind values after filters | yes / no |  |
| hidden fields for selected row | yes / no |  |
| debug says XML source is DB/HADES/local resource | yes / no |  |

## 7.1 Options And Related Reads

| Read surface | UI action | Legacy source/evidence | Required for current migration slice? | Status |
| --- | --- | --- | --- | --- |
| Options/lookup | Open combo/search options |  | yes / no | captured / deferred / blocked |
| Related tab | Click tab and record parent binds |  | yes / no | captured / deferred / blocked |
| Related link/popup | Click only if safe or record parameters |  | yes / no | captured / deferred / blocked |

## 8. Outcome For Closure

| Closure Question | Answer |
| --- | --- |
| Can runtime binds be promoted from XML-only to runtime/manual evidence? | yes / no |
| Can selected row/detail be keyed by the chosen public key? | yes / no |
| Are internal legacy locators kept separate from public API keys? | yes / no |
| Are list/detail/options/related read parity gaps recorded in `read-parity-matrix.md`? | yes / no |
| Is read scope enough to defer write safely? | yes / no |
| Does any visible behavior contradict XML/Oracle evidence? | yes / no |
