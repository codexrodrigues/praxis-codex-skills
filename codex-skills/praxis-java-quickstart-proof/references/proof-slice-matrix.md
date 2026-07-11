# Proof Slice Matrix

| Capability | Minimum operational evidence |
| --- | --- |
| Resource/schema | OpenAPI, filtered schema, ETag/hash, response links |
| Filter/read | Matching and non-matching fixture, paging/sort if published |
| Action/surface | Catalog, capability, allowed and denied execution |
| Option source | Filter plus by-ids selected reload and dependency if published |
| Stats/export | Capability, result policy, allowed and denied field/scope |
| Write | Valid mutation, readback, rejected mutation, cleanup |

Keep evidence sanitized and deterministic. A Quickstart test proves consumption;
it does not redefine the canonical contract.
