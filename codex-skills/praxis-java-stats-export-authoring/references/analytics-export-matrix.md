# Analytics Export Matrix

| Need | Canonical route | Required proof |
| --- | --- | --- |
| Aggregate or group data | Stats registry and support mode | Metric/dimension semantics, filter scope, capability |
| Download collection data | Collection export request/result | Format, scope, allowlist, limit, headers |
| Export selected items | `selected` scope and selected IDs | Selection authorization and result count |
| Export filtered/all/page | Canonical scope plus query filters/sort | Same effective collection policy as list |
| Large/async result | Deferred result and declared capability | Status/result contract and client handling |

## Field Decision Packet

Record business meaning, role (dimension/measure/bucket/export-only/excluded),
allowed aggregation, precision, governance, export eligibility, and consumer.
Do not expose numeric-looking identifiers or sensitive fields as measures merely
because they can be aggregated or serialized.

## Minimum Negative Proof

Prove a denied field, unsupported scope/format, or server-truncated limit. Verify
the response reports the effective policy and does not silently export a broader
default. CSV and XLSX paths must retain formula-injection protection.
