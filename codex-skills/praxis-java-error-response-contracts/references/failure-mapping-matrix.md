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

The pending Metadata error-wire correction makes typed `errors[].code` and
`errors[].target` the single source for those flat JSON members. During its
review, inspect the raw Boot MVC response with strict duplicate-member
detection before parsing a tree; a `ProblemDetail.properties` lookup cannot
prove the wire has no duplicate or stale field. Keep extension names away from
typed, RFC 7807, and envelope members, and verify field clearing and declared
trace/outcome behavior. An incoming JSON `properties` wrapper is rejected in
every value shape; legitimate Java map extensions remain flat. The served
schema must show flat typed fields without exposing the Java map container or
closing the object against allowed extensions. This is candidate guidance
until the owner publishes and a consumer proves the changed wire.

## Minimum Negative Proof

For every changed write or command, test one valid outcome and one expected
failure with readback/no-mutation evidence. For fields, prove the runtime receives
a targetable field path. For actions, prove denied availability and endpoint
enforcement agree. Treat a raw backend exception as a migration finding, not as a
client contract.
