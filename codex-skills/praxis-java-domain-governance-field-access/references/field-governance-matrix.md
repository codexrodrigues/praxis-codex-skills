# Field Governance Matrix

| Surface | Decision to record |
| --- | --- |
| Response/read | Visibility, masking, authority, audit/log treatment |
| Create/update | Edit authority, validation, purpose, derived/default behavior |
| Filter/lookup | Whether search/filtering reveals or accepts the field |
| Option source | Display/search fields, tenant/dependency scope, selected reload exposure |
| Stats/export | Dimension/measure/export eligibility, allowlist, aggregation risk |
| AI/RAG | Display, retrieval, reasoning, summary, training, action, or exclusion |
| Errors/docs | Safe explanation and prohibited internal details |

Default sensitive data to least exposure. A field-access hint or mask never
authorizes backend delivery. Prove the same policy in read, write, filter,
export, analytics, AI and error paths that the resource publishes.
