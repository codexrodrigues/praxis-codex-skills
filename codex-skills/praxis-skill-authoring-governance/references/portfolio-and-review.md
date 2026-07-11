# Portfolio And Review

## Portfolio Lanes

Use this taxonomy to prevent a large portfolio from becoming a collection of
component descriptions.

| Lane | Unit of work | Examples |
| --- | --- | --- |
| Foundation | Host and public contract baseline | Java host, resource baseline, DTO semantics, schema contracts |
| Runtime handoff | Materialization by real consumers | options, actions, surfaces, capabilities, error and export paths |
| Enterprise behavior | Cross-cutting correctness | availability, governance, concurrency, audit, command execution |
| Operational proof | Repeatable evidence | quickstart pilot, HTTP corpus, diagnostics, focused validation |
| Ergon migration factory | Legacy-to-API throughput | discovery, lineage, write route, mutation probes, parity, cleanup |

An item belongs in the lane determined by its canonical owner and repeatable
decision, not by the application where it was discovered.

## Review Matrix

For each proposed skill, answer these questions before adding it.

| Question | Passing evidence |
| --- | --- |
| What repeated decision becomes faster? | A concrete task and measurable rework it removes. |
| Is it platform guidance or a contract gap? | Source inventory and one of the required classifications. |
| Who owns the semantics? | A named starter, runtime library, config boundary, or migration family. |
| Why is a separate skill necessary? | Distinct trigger, workflow, and focused proof from neighboring skills. |
| What must it inspect? | Real paths, annotations/types/endpoints, tests, and consumer evidence. |
| What cannot it recommend? | Specific local aliases, parallel contracts, or unproven shortcuts. |
| How is success proved? | Focused tests, HTTP/consumer materialization, or migration evidence pack. |

## Delivery Gates

Promote a candidate from planned to active only when all apply:

1. Its trigger description distinguishes it from adjacent skills.
2. Its workflow names the canonical owner and a source audit.
3. It has at least one realistic success path and one must-fail boundary.
4. The repository manifest records only real dependencies and current hashes.
5. Canonical source and installed projection have been audited after sync.

Prefer one proven skill over several speculative ones. A new skill is justified
when it materially reduces rediscovery of a canonical route; otherwise update
the closest existing skill or the platform contract.
