# Investigation Template

Use this as the final report shape for screen discovery.

## Screen

- Code:
- Investigation mode: Quick discovery / Full discovery / API migration
- URL:
- Title:
- Module:
- User-visible workflow:
- Related screens:

## Access And Navigation

- Legacy entry point:
- Credentials source: Provided in session / Environment / Not available
- Menu/search term used:
- Selected search result:
- Final URL:
- Browser access status: Complete / Partial / Missing
- Notes:

## Browser and XML Evidence

| Area | Component | Evidence | SQL/Link/Parameter | Confidence |
| --- | --- | --- | --- | --- |
| Main grid |  |  |  |  |
| Detail panel |  |  |  |  |
| Tab |  |  |  |  |
| Action/link |  |  |  |  |

## XML And SQL Extraction

| Component | XML/Debug Location | `sqlSelect` Object Seeds | `sqlParameters` / Bind Tokens | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Use this section to show how the Oracle seed list was derived. Do not list Oracle objects as confirmed here unless they are directly present in XML/debug/runtime evidence.

## Legacy Documentation Sources

| Source Layer | Path / Topic | Fact Found | Promoted To Main Findings | Confidence |
| --- | --- | --- | --- | --- |
| Archon docs/source |  |  | yes/no |  |
| EA/help/specs |  |  | yes/no |  |
| Workflow/forms/reports/portal |  |  | yes/no |  |

Summarize the detailed evidence in `legacy-doc-sources.md`. Use `CONFIRMED_LOCAL_DOC` for documentation-only facts and do not promote them to implementation behavior without XML/runtime/local source/Oracle confirmation.

## Runtime Parameters

| Bind Order | Archon Token | Component | Observed Value | Null/Default Behavior | Effect On SQL | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Oracle Object Inventory

| Owner | Object | Type | Role | Confidence | Evidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Use `CONFIRMED_ORACLE_METADATA` only for evidence actually queried from Oracle. Use `CONFIRMED_LOCAL_SOURCE` for checked-in XML, SQL, Java, or PL/SQL not yet confirmed in Oracle.

## View Lineage

Show view-to-table expansion. Include filters, joins, derived fields, and security helpers.

```text
SCREEN SQL
  -> VIEW
     -> TABLE
     -> SCOPE TABLE
     -> LOOKUP/HELPER
```

## Synonym Resolution

| Referenced Name | Synonym Owner | Final Owner | Final Object | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

State whether synonym resolution was executed against Oracle. If it was not, mark final owners as expected resolution, not confirmed metadata.

## Security and Scope

- Current user source:
- Current company source:
- Current transaction source:
- Oracle package context dependencies:
- Java/API same-connection context strategy:
- Connection-pool cleanup/reset strategy:
- Company access function/view:
- Special values:
- Risk notes:

## Fields and Data Rules

| UI Field | Source Object | Source Column | Type | Nullability | Conversion | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Related Flows

| From | Action | Destination | Parameters | Objects Introduced | Confidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Every related flow must be represented in the confirmation SQL or listed as deliberately skipped with a reason.

## Confirmation SQL Coverage

| Area | Covered In SQL | Executed | Result Location | Gaps |
| --- | --- | --- | --- | --- |
| Objects and synonyms |  |  |  |  |
| Recursive dependencies |  |  |  |  |
| Constraints and indexes |  |  |  |  |
| Triggers and updatable views |  |  |  |  |
| Grants, roles, packages |  |  |  |  |
| Source search and write risk |  |  |  |  |
| Related flows |  |  |  |  |
| Java Oracle session context |  |  |  |  |

## Candidates and Open Questions

| Candidate | Why It Matches | Missing Evidence | How To Confirm |
| --- | --- | --- | --- |
|  |  |  |  |

## Rejected Candidates / False Positives

| Candidate | Why It Matched | Evidence Against | Final Status |
| --- | --- | --- | --- |
|  |  |  |  |

## Recommended Next Checks

List concrete, bounded checks only: XML node to inspect, query to run, click path to exercise, or parity case to execute.

## Gates

| Gate | Status | Evidence | Blocks |
| --- | --- | --- | --- |
| Observed | Complete/Partial/Missing |  |  |
| Resolved | Complete/Partial/Missing |  |  |
| Expanded | Complete/Partial/Missing |  |  |
| Write-risk checked | Complete/Partial/Missing/Not applicable |  |  |
| False-positive checked | Complete/Partial/Missing |  |  |
| Confirmation SQL complete | Complete/Partial/Missing |  |  |
| Session-context checked | Complete/Partial/Missing/Not applicable |  |  |
| API-ready | Complete/Partial/Blocked/Not applicable |  |  |
