# API-First Factory Integration

Use the API-first factory only after its source artifacts exist and its own
checks pass. It materializes a read-only vertical slice from screen evidence;
it must not infer unresolved semantic fields, SQL, session scope, or writes.

| Stage | Official tool | Output and decision |
| --- | --- | --- |
| Evidence projection | `export-api-first-manifest.ps1` | Factory-internal manifest with provenance and individually gated operations |
| Manifest gate | `check-api-first-manifest.ps1` | Rejects private public fields and premature write readiness |
| Read profile | `new-api-first-read-profile.ps1` | Preliminary profile with `REVIEW_REQUIRED` semantic and SQL fields |
| Profile gate | `check-api-first-read-profile.ps1` | Requires reviewed target, bridge, schema, and query blueprint details |
| Java dry run | `java-read-scaffold.ps1` | Shows generated resource artifacts without writing by default |

The generated Java is a reviewable starting point, not proof. Before `-WriteFiles`,
verify the canonical module root, host conventions, Praxis annotations, Oracle
same-connection context, HADES authorization, filtered schemas, focused tests,
endpoint smoke, and parity state. Writes remain separately gated by table-rule
audit and route decision.
