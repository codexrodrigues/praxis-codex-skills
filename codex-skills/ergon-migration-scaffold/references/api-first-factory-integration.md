# API-First Factory Integration

Use the API-first factory only after its source artifacts exist and its own
checks pass. It materializes a read-only vertical slice from screen evidence;
it must not infer unresolved semantic fields, SQL, session scope, or writes.

| Stage | Official tool | Output and decision |
| --- | --- | --- |
| Evidence projection | `export-api-first-manifest.ps1` | Factory-internal manifest with provenance and individually gated operations |
| Manifest gate | `check-api-first-manifest.ps1` | Rejects private public fields and premature write readiness |
| Timing start | `start-api-first-timing.ps1` | Immutable prospective anchor tied to the manifest hash before Java work |
| Read profile | `new-api-first-read-profile.ps1` | Preliminary profile with `REVIEW_REQUIRED` semantic and SQL fields |
| Profile gate | `check-api-first-read-profile.ps1` | Requires reviewed target, bridge, schema, and query blueprint details |
| Java dry run | `java-read-scaffold.ps1` | Shows generated resource artifacts without writing by default |

After each real proof, use `record-api-first-timing-milestone.ps1` with an
existing evidence file. The required ordered milestones are
`implementation-started`, `first-endpoint-executed`, `schema-validated`,
`focused-tests-passed`, and `legacy-parity-assessed`.
`check-api-first-timing.ps1` reports elapsed minutes from factory start and from
implementation start to the first endpoint. It rejects a changed source manifest
or missing evidence, so it is unsuitable for reconstructed historical metrics.

The generated Java is a reviewable starting point, not proof. Before `-WriteFiles`,
verify the canonical module root, host conventions, Praxis annotations, Oracle
same-connection context, HADES authorization, filtered schemas, focused tests,
endpoint smoke, and parity state. Writes remain separately gated by table-rule
audit and route decision.
