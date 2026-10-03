# Bulk SQL phase proof

Use this procedure when a real PostgreSQL lock test invokes an HTTP flow that also
performs governed readiness, OpenAPI composition or policy capture. First identify
which phase owns the promised timeout. A failed whole-request timing assertion
does not establish a broken SQL limit.

## Inspect the concrete flow

In `praxis-api-quickstart`, inspect:

- `src/main/java/com/example/praxis/apiquickstart/hr/service/EventosFolhaApprovalProposalService.java`:
  `capture` calls `BulkOperationLifecycle.requireReady` before evaluation and the
  storage transaction; `boundStorageStatements` applies the local SQL limit.
- `src/main/java/com/example/praxis/apiquickstart/hr/service/EventosFolhaApprovalEvaluationProvider.java`:
  `evaluateForProposalCapture` starts its own capture budget after readiness.
- `src/test/java/com/example/praxis/apiquickstart/config/EventosFolhaApprovalEvaluationHttpTest.java`:
  `persistRaw`, `EvaluationProbeController`,
  `boundsTheBlockedCompanionInsertWithoutChangingPoolOrServerTimeouts` and its
  adjacent `boundsTheProtectedReadStatementUnderAnExclusiveProposalLock` proof.

The canonical readiness implementation belongs to Metadata's
`src/main/java/org/praxisplatform/uischema/bulk/BulkOperationLifecycle.java`.
Do not replace it with a cached READY boolean or omit composition to make timing
pass. In the demonstrated host profile, composition has a 60s preparation/admission
budget, capture has an 8s budget, and storage uses a five-second transaction timeout plus
`SET LOCAL statement_timeout='5s'`. These limits belong to different boundaries;
the storage assertion must not include all earlier HTTP preparation.

The fixture's external client uses a finite 90s read timeout. On Boot 3.5, derive
a per-test client through the public
`original.withRequestFactorySettings(settings -> settings.withReadTimeout(Duration.ofSeconds(90)))`
API and assert the public read-timeout setting. Preserve and verify authentication,
converters, interceptors, root URI/URI handler, connect timeout, redirects and SSL
builder settings. Audit any configuration applied to the original RestTemplate
after construction: builder cloning alone does not preserve those mutations;
carry required settings through public APIs and prove their behavior. Keep the
original client and factory untouched; restore the original client reference on
setup failure and in `AfterEach`, asserting the original factory identity. Do not
cast to OkHttp or inspect a private HTTP client's timeout through reflection.
This restriction does not prohibit separate clock or business-oracle reflection.
The 90s observation allowance is not an end-to-end SLA or server cancellation
deadline. Do not increase Metadata's internal connect/read/composition limits or
change global clients to repair a test's phase selection.

## Observe the real blocked statement

1. Acquire the fixture's exclusive evaluation-table lock on an independent
   administrative connection and record its PostgreSQL backend PID. Keep the
   lock until the failure response, releasing it in `finally` on failure.
2. Generate the authenticated JWT before starting one owned worker. Invoke the
   same real HTTP route/service with the original domain assertions. Do not rely
   on inherited servlet or security thread state, and do not log the JWT.
3. Use a separate administrative observer connection, outside the runtime pool.
   Correlate `pg_stat_activity` and `pg_locks` by backend PID, exact database and
   runtime role, active INSERT into `praxis_bulk.praxis_bulk_evaluation`, lock
   wait, ungranted `RowExclusiveLock` on that exact relation, and the recorded
   blocker PID in `pg_blocking_pids`. SQL text matching alone is insufficient.
4. Give the observer its own bounded query and overall wait. In the concrete
   fixture, the pre-observation window is at most 90s from request submission;
   once the statement is observed, the phase deadline accounts for its already
   elapsed age and allows at most 10s from that statement's start. Stop if HTTP
   finishes before the correlated wait is observed; do not silently accept an
   unrelated 503 or retry through a different path.
5. Read `clock_timestamp() - query_start` from PostgreSQL. Bracket that observer
   query with monotonic timestamps and record response completion in the worker,
   immediately after the HTTP call returns. Preserve the initial age so late
   observation does not incorrectly restart the lower-bound clock.

Let `a` be the initial PostgreSQL statement age, `m0`/`m1` the monotonic times
before/after the observer query, and `r` HTTP completion, all in the same duration
unit. The fixture estimates:

```text
lower = a + (r - m1)
upper = a + (r - m0)
```

Record `a`, `m1 - m0`, both bounds, backend/blocker IDs and whole HTTP elapsed
separately. The bracket includes observer uncertainty; the interval extends
through application CPU, error handling, rollback, response serialization and client receipt.
It is not pure PostgreSQL lock-wait duration. PostgreSQL supplies the initial
age; do not subtract a database absolute timestamp from the client wall clock.
Clock changes or an unexpectedly large sampling interval require diagnosis.

The accepted concrete five-second SQL fixture requires `lower >= 4s` and
`upper < 10s`. These are that fixture's observation tolerances, not a general
recipe or permission to increase a production budget. Investigate excess time
and identify the SQL/response phases before changing an assertion. Preserve the
503 sanitization, rollback, absent proposal/evaluation rows and original pool
settings (`statement_timeout=0` before and after this fixture). The lock must
still be held when the failure response arrives, so unlocking cannot fabricate
the expected outcome.

## Cleanup and evidence

Always release the blocker, close owned connections, join the actual worker with
a finite allowance, shut down/await its executor, and check that the observed
backend is neither active nor left in a transaction. Preserve the primary error;
attach cleanup failures as suppressed errors. A future timeout or cancellation
does not prove backend cancellation. Report residual work as a failed cleanup,
not a green proof. Real PostgreSQL here proves the scoped fixture, not fleet
latency, a hard server deadline or a pure SQL timing measurement.

Before any `clean` or rerun that overwrites shared reports, snapshot evidence
outside `target`: source commit and changed-file bytes/hashes, POM and resolved
dependency identity, JAR hash, command, XML and log hashes, and the observed
timings/cleanup outcome. Preserve failed and corrected runs separately. The
coordinator owns the build target and must authorize its use; do not launch a
second build against an active target or database.

Deleted diagnostic sources can leave stale `*Test.class` files in
`target/test-classes`; ordinary compilation does not necessarily remove them.
If discovered tests or hardcoded candidate guards contradict the current source
tree, compare compiled classes with current sources and document the mismatch.
After preserving evidence, a coordinated clean build is justified to remove
stale outputs. Do not weaken artifact guards, exclude real tests, or claim that
old XML validates the cleaned tree. Re-run the affected method and its relevant
neighbor after a local fixture correction; a published dependency adoption still
requires the host's broader `verify` gate without a candidate version override.
