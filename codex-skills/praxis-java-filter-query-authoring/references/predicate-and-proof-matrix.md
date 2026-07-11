# Predicate And Proof Matrix

## Predicate Selection

| Business question | Canonical operation | Typical payload | Required decision |
| --- | --- | --- | --- |
| Is this exact state, owner, or identifier? | `EQUAL` / `NOT_EQUAL` | Scalar | Entity field or relation path |
| Does text contain a business term? | `LIKE`, `NOT_LIKE`, `STARTS_WITH`, `ENDS_WITH` | Text | Search scope and sensitive-field exclusion |
| Is it one of these governed values? | `IN` / `NOT_IN` | List | Alias-to-relation mapping and option-source alignment |
| Is a value within a measurable period or amount? | `BETWEEN`, `BETWEEN_EXCLUSIVE`, `NOT_BETWEEN`, `OUTSIDE_RANGE` | Ordered two-value list | Boundaries, type, time zone, normalization |
| Did it occur on a date or relative window? | `ON_DATE`, `IN_LAST_DAYS`, `IN_NEXT_DAYS` | Date or integer days | Clock, zone, inclusivity, audit meaning |
| Is the field absent/present or boolean state? | `IS_NULL`, `IS_NOT_NULL`, `IS_TRUE`, `IS_FALSE` | Activating boolean | Whether absence is meaningful and authorized |
| Does a collection meet a size condition? | `SIZE_EQ`, `SIZE_GT`, `SIZE_LT` | Integer | Collection semantics and query cost |

The annotation operation and `relation` decide predicate semantics. A DTO suffix
is only human-readable contract text; it is never a routing mechanism.

## Alias And Sort Rules

- A DTO alias must point at the real entity path through `relation`.
- Sort aliases require an annotated field and are remapped by the canonical
  specifications builder; prove direct and relation-path cases.
- Preserve resource default sort when no sort is requested.
- Treat option-source sort separately: it must match a validated published sort
  key before provider resolution.

## Minimum Proof

| Change | Minimum proof |
| --- | --- |
| New scalar/list/relation predicate | Known fixture match and non-match, plus alias/relation assertion |
| Range or relative period | Normalizer test and lower/upper or clock-boundary integration proof |
| Pagination or sort | Page contents/order, default sort, and accepted alias assertion |
| Lookup-backed filter | Filter and by-ids reload with dependencies when published |
| Public schema/HTTP contract | Filtered schema evidence and host/quickstart HTTP integration proof |

Reject a payload that is ambiguous, unsupported, unauthorized, or merely a
frontend interpretation. Do not compensate by silently converting it into a
different predicate.
