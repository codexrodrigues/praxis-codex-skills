# Failure Mapping Matrix

| Failure class | Required public evidence | Do not expose |
| --- | --- | --- |
| Field/input validation | Status, stable code/category, field path, safe correction message | Framework validator text as sole contract |
| Missing resource | Resource/action identity and not-found outcome | Repository/entity implementation detail |
| State or authority denial | Safe unavailable/forbidden outcome and action context | Role internals or lifecycle query details |
| Duplicate/idempotency conflict | Conflict identity and retry/replay policy when safe | Constraint name or storage key internals |
| Stale precondition | Resource-version conflict/precondition response | Schema ETag as write version |
| Filter/option source policy | Invalid field/sort/filter/capability outcome | SQL, provider, datasource, context attributes |
| Legacy integration failure | Stable business error plus protected evidence reference | ORA/JDBC/package text in client output |
| Unexpected failure | Sanitized category and correlation/diagnostic route | Stack trace, token, session, secrets |

## Minimum Negative Proof

For every changed write or command, test one valid outcome and one expected
failure with readback/no-mutation evidence. For fields, prove the runtime receives
a targetable field path. For actions, prove denied availability and endpoint
enforcement agree. Treat a raw backend exception as a migration finding, not as a
client contract.
