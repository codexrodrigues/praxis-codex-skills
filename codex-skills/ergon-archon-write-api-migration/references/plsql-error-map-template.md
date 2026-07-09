# PL/SQL Error Map Template

Map legacy errors into API responses without leaking SQL, stack traces, credentials, or internal package state.

| Legacy Source | Rule Evidence | Error Code / Pattern | Legacy Meaning | API Status | API Field | API Message | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

Required cases:

- validation error;
- raw Oracle validation failure that must be normalized, such as `ORA-06502` for invalid quantity or `ORA-01422` for missing required code;
- no permission;
- selected row not found;
- duplicate key;
- dependent record exists;
- package/session context missing;
- unexpected Oracle failure.

Probe guidance:

- Record the exact SQL/output path for every mapping.
- Preserve stable legacy business codes such as `ERG-00433`, but do not expose Oracle stack traces, package names, rowids, or bind dumps.
- If the routine leaks a raw Oracle error for a user-invalid payload, map it to `422` or `409` as appropriate and add Java pre-validation when the missing/invalid field is obvious.
- For duplicate constraints, map unique-key failures such as `ORA-00001` to `409 Conflict` unless the legacy screen proves a different user-facing validation.
- For permission errors raised by the routine, map business denial to `403`; do not infer write permission from read visibility or button state alone.

API smoke guidance:

- Link the API result artifact for every implemented mapping, not only the PL/SQL probe.
- For raw Oracle validation errors such as `ORA-06502` and `ORA-01422`, confirm the API envelope returns a stable business status/message and that target/side-effect table counts remain unchanged.
- For duplicate/collision, confirm the API returns `409`, preserves only the first row, then cleans it through the approved route and proves final counts zero.
- For permission denial, confirm a real denied legacy user/profile returns `403` and no mutation.
- Leave untested mappings as `Deferred` or `Blocked` with the exact missing fixture.
