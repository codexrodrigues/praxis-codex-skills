# Duplicate-draft adoption evidence

Inspect the selected starter's `DuplicateDraftResourceService`, opt-in
`AbstractDuplicateDraftResourceController`, availability composition and concrete
host service. The canonical guide is
`praxis-metadata-starter/docs/guides/DUPLICATE-DRAFT-ADOPTION.md` when available.

1. Attribute the domain decision: copied allowlist, cleared fields, deliberate
   defaults, eligible source states, object scope and permissions. Do not infer
   adoption from a legacy button or structural capability.
2. Keep the draft response schema distinct from the create request when fields
   remain unanswered. Verify actual JSON, required fields and nullability in each
   supported OpenAPI version. An unanswered boolean may be null by domain policy;
   explicitly false can remain valid. Never weaken create validation with a private
   origin marker or silently turn a required choice into false.
   If the draft publishes presentation metadata, verify actual controls, sources
   and value types against the create contract; unused-by-form metadata can still
   misdescribe a public reference or choice. Keep the consumer on the CREATE
   request schema plus draft values, without a second response-driven form.
3. Compare capabilities, actions, links and direct service guards for allowed and
   denied states, missing/inaccessible sources and object scope. Validate malformed
   HTTP context at its boundary without weakening fail-closed availability.
   Require the expected HTTP status and JSON shape before negative assertions:
   a missing field is not boolean false, and an error envelope does not prove
   correct link omission. Inspect effective decision metadata for state leaks,
   distinguishing it from documented allowed states; searching for a word absent
   from the fixture is not a confidentiality regression.
4. Prove no writes/reservations/version or ledger changes, including a caller's
   dirty persistence context. A read-only annotation or absence of save is not
   proof against incidental flush. Revalidate all constraints on final create.
   Ground negative tests in the actual deserialization configuration and contextual
   field catalog: test unknown properties individually and explicitly ignored
   properties separately. Satisfy required payload fields before testing a later
   domain guard; do not relax production validation to repair an invalid fixture.
5. For assigned identifiers, test the persistence layer's new-entity detection
   deterministically and exercise concurrent create plus readback. A barrier before
   HTTP requests does not force both requests past an existence check; successful
   concurrency alone may miss a merge regression.
6. Record source/delta and actual dependency version/hash. Reconcile the consuming
   checkout and run affected tests there before changing adoption to implemented.
   A private override is not public dependency adoption. Preserve historical
   decisions; hash the new attributed decision without redefining other resources.
7. Report backend proof, browser/runtime acceptance and publication separately.
   Never mark an applicable journey not-applicable just to clear its inventory gate.
   Preserve failed campaigns as distinct evidence. Fail-closed unavailability is
   not proof of the expected functional response, and a successful rerun does not
   establish a fix. Do not broaden accepted statuses or repeat until green to
   declare adoption complete.
