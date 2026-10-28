# Corporate SESSION Transport, Governed Pages & Demonstrative Route Budgets

Use this reference when an Angular host integrates corporate `SESSION` + CSRF transport, governed dynamic pages (`praxis-dynamic-page` / `/api/praxis/config/pages/**`), or demonstrative lazy route budgets.

---

## 1. Corporate SESSION Transport

For Quickstart-backed corporate hosts, inspect the backend `AuthController`/CSRF contract and Hero's `corporate-session-*`, `corporate-context`, and `docs/engineering/corporate-session-journey.md` before adding another auth adapter. Core already owns context/choices/CAS; cookie identity and transport belong to the host. Keep demo personas and local page persistence separate from server grants.

Confirm login through `GET /auth/session`, consume its raw `X-XSRF-TOKEN` response header, and send it only on required mutations. Keep passwords/tokens out of storage, logs, and diagnostics. Serialize auth exchanges: discarding a stale callback cannot undo a browser's late `Set-Cookie`. Fence context responses by session generation; `403`/`503` context failures do not mean logout. Preserve uncertain logout explicitly.

Scope credentials/CSRF to the exact configured origin and canonical route boundaries; remove synthetic persona headers while preserving Core-confirmed context headers and ETag/preconditions. Inspect the effective Angular `HttpBackend`: XHR may ignore a redirect option. Reject credential redirects before another destination is contacted; when needed, use a host-private `FetchBackend` only for corporate paths and preserve legacy XHR/progress. Do not switch the whole application transport by convenience.

Proxy `/auth` without spoofing an allowed `Origin`, weakening TLS, or rewriting cookie security. The backend must allow the real origin. Test session restore, raw CSRF, logout uncertainty, response races, exact-origin rejection, and blocked redirects. Browser responses controlled by tests prove consumer behavior, not real `SESSION`, cross-site cookies, CORS, or deployed-backend readiness. Record those limits and reuse unchanged backend evidence instead of requiring another Neon campaign for UI work.

---

## 2. Corporate Page Authoring Context & Lifecycle Fencing

For page authoring hosts, put `EnterpriseRuntimeContextService`, `UiLayoutLifecycleService`, and the host page transport in one explicit corporate ancestor scope shared by entry, editor, and published reader. A component-scoped context paired with a root lifecycle client creates different snapshots. Keep the demo's global headers out of this scope. Invalidate that shared context on every `SESSION` generation change, not only logout; fence reads and writes by both context revision and captured session generation. After `401`/new login, `ready()` must not reuse the previous actor's snapshot.

Use Config `creationKey` receipts and the by-creation-key reconciliation read for a lost creation response; a `404` is not permission to recreate an in-flight command. Keep revision, assignment, freeze, submit, approve, and publish explicit, with the server's current strong validators. Published/catalog HTTP ETags are weak read receipts and must never be required or reused as strong draft/head write validators. Do not report draft creation as successful `SaveAs` publication. Materialize only the host-admitted document profile; a lifecycle state receipt is not an immutable review preview or proof that a page renderer is wired. Keep those acceptance scopes separate.

For published-page copies, inspect Config's `PageRuntimeReadService` and the host transport/editor together. Use the server-provided `copySource` from the published read, correlated with that page and its authorized head. Send it to creation with a new `creationKey`; let Config allocate the new page/draft/route identity and rematerialize the source. Do not clone JSON or reuse source/menu identities on the client. The copy is a draft with no inherited navigation binding: explicitly select its destination group and publish through lifecycle. On authorization denial, clear displayed protected content and fence further writes. A reread may discard unsaved edits; this UI fence neither repairs stored configuration nor grants access. Test copied content, distinct identity, empty initial navigation, and the denial path separately from real publication proof.

Treat navigation groups as a separate governed aggregate: publish the referenced group before publishing a page binding to it. Consume the SDK's runtime navigation in that same corporate provider scope; do not synthesize menus from the page catalog. Inspect Config `P3-A`/`P3-B` and `QuickstartPageConfiguration`/`QuickstartPageDocuments`: the native groups baseline is empty, not a clone of the published groups head. A genuine `head404` selects the existing first-publication precondition; an existing head requires the complete admitted groups document and current strong CAS before editing, or reuse of its groups without rewriting the aggregate. Never replace the full groups document with a paginated/visibility-filtered navigation projection. Prove persistent menu/route behavior separately from draft save and group creation.

---

## 3. Governed Pages Host Adoption Protocol (`P4` / `P5-A` / `P5-B` / `P5-C` / `P5-D`)

When a host adopts governed dynamic pages (`praxis-dynamic-page`), follow this 10-step protocol without inventing parallel storage, routes, or menu registries:

1. **Separate operating modes**: use `PraxisPageSaveAsComponent` + `PraxisPageCopyActionComponent` (`@praxisui/page-builder`) with a Web Lock-protected local repository for browser-local laboratory flows (`P5-A`), and `GovernedPageWorkflowController` + `GovernedPageNavigationController` + `createCorporateGovernedPagePersistenceAdapter` + `/api/praxis/config/pages/**` + `/api/praxis/config/ui-layouts/**` for corporate governed flows (`P4` / `P5-B`).
2. **Enforce volatile child persistence**: render child `praxis-dynamic-form` and `praxis-table` widgets inside governed pages with `configPersistenceStrategy: 'volatile'` and configuration solely in `widget.definition.inputs.config`.
3. **Admit creation sources on the server**: create corporate pages via `POST /api/praxis/config/pages` using an admitted `registered-native` seed or a pinned `published-page` `copySource` (`pageId`, `releaseId`, `revisionId`) correlated with `GET /api/praxis/config/pages/{pageId}/published`.
4. **Reconcile timeouts by creation key**: on network timeout during `POST /api/praxis/config/pages`, query `GET /api/praxis/config/pages/by-creation-key?creationKey=...` with the same `creationKey` before retrying.
5. **Preserve childSources and fixed envelopes**: when saving a revision (`POST /drafts/{draftId}/revisions`), declare `childSources` only for newly added widget keys and keep fixed binding envelopes (`resourcePath`, `mode`, `readOnly`, `operation`) immutable per `widget.key`.
6. **Govern navigation groups and icons**: edit menu bindings (`navigationBindings[]`) in `praxis.dynamic-page.editor` and shared groups (`groups[]`) in `praxis.navigation-groups.editor` using only the host's admitted Material icon catalog (`GOVERNED_PAGE_DEFAULT_ALLOWED_ICONS` / `QuickstartPageConfiguration.ALLOWED_ICONS`).
7. **Complete the release lifecycle**: run `draft -> revision -> assignment -> freeze -> submit -> approve -> publish` (plus `rollback` and `withdraw`) with strong `If-Match` preconditions and distinct author/reviewer/publisher gates where required.
8. **Resolve from the single release head**: render the page catalog (`GET /api/praxis/config/pages`), stable route `/pages/:pageId` (`GET /api/praxis/config/pages/{pageId}/published`), and runtime menu (`GET /api/praxis/runtime/navigation`) from the same active head without falling back to `ui_user_config` or drafts.
9. **Fence session and context epochs**: require authenticated `SESSION`, raw `X-CSRF-TOKEN` on mutations, and confirmed `EnterpriseRuntimeContextService` (`X-Praxis-Context-Version`), invalidating in-flight requests and caches on logout or context switch (`A -> B -> A`).
10. **Migrate legacy pages explicitly**: import legacy `ui_user_config` pages (`LEGACY_PUBLISHED_PAGE_STORAGE_PREFIX`) through `inspectLegacyPublishedPagePayload` and `GovernedPageWorkflowController.importLegacyPublishedPage` (`P5-D`) rather than reading legacy snapshots at runtime.

---

## 4. Demonstrative Host Budgets & Lazy Routes

Inspect the host's actual bootstrap and dependency graph before changing build configuration. Pages may already be lazy while eager metadata/provider imports retain the entire catalog. Prefer the existing provider and injector contracts; keep application singletons, root-consumed options, and required dictionaries at their correct lifetime. Use `praxis-core-providers-bootstrap` for the scope audit. Do not raise budgets, remove deliberately published exports, or switch source aliases to packaged libraries without measuring and preserving style coverage. Report initial assets separately from the catalog fetched on first navigation.

When moving an existing route collection under a persistent lazy parent, preserve URLs, precedence, redirects, feature gates, and dynamic CRUD registration/removal. Use public Router matching and the existing resource registry; never manipulate private loaded-route caches. Exact URL segment matching is route admission, not primary user-intent routing. Preserve multi-segment resource keys.

Shared action routes can reuse the same page instance across different resources. A page that captures `ActivatedRoute.snapshot` once may retain the old resource, `id`, `formId`, or return target. Materialize current `paramMap`, `queryParamMap`, and `data` streams, including query removal. Prove navigation with the real host page and the same instance; a probe with fresh snapshot getters can mask this defect. Validate normal production budgets, direct navigation/refresh, editor round-trips, and panel context after the final productive change.
