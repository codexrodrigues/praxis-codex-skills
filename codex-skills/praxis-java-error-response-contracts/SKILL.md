---
name: praxis-java-error-response-contracts
description: Use when implementing, auditing, or migrating Praxis Java API failures: canonical exception mapping, structured validation and field errors, resource not found, authorization and availability denial, idempotency and concurrency conflict, option-source/filter failures, workflow command outcomes, sanitized diagnostics, and Angular form/action error materialization.
---

# Praxis Java Error Response Contracts

Treat an error as a stable public outcome of a resource operation. Do not expose
framework exceptions, Oracle/JPA messages, stack traces, provider details, or a
host-specific envelope that forces Angular and migration code to branch locally.

## Classify The Failure Before Mapping It

Inspect the endpoint, DTO validation, service transition, exception handler,
canonical error response type, existing error tests, direct Angular consumer, and
legacy evidence when applicable. State whether the failure is invalid input,
field validation, missing resource, forbidden/availability denial, business rule,
duplicate/conflict, idempotency conflict, stale precondition, external dependency,
or unexpected internal failure.

Classify a proposed error field, code, endpoint mapping, diagnostic detail, or
HTTP status as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Prefer the canonical
exception handler and response model; do not add controller-local `try/catch` or
an alternate problem envelope for one resource.

## Publish A Safe Structured Outcome

1. Map DTO and bean validation to the canonical structured response, preserving
   field path, stable code/category, safe user message, and operation context.
   A consumer must be able to associate a field error without parsing prose.
2. Map resource absence, authorization, unavailable state, and business denial to
   distinct public outcomes. Do not report an unavailable workflow action as an
   ordinary validation error, and do not make capability visibility a substitute
   for endpoint authorization.
3. Map duplicate/idempotency/concurrency failures deliberately. A stale or
   missing required `If-Match` is a resource-version precondition outcome;
   schema-cache ETag behavior is not a write conflict. Preserve retry guidance
   only when it is safe and governed by the command contract.
4. Map filter, option-source, and lookup failures to their public policy: invalid
   payload, unsupported capability, unsupported structured filter/sort, page
   limit, dependency policy, or selected reload limitation. Do not leak provider,
   SQL, datasource, or context attributes.
5. Translate legacy/Oracle/JPA failures into a stable business response when they
   represent invalid public input or known conflict. Preserve raw details only in
   protected server diagnostics and migration evidence, never in client output.
6. Keep unexpected failures sanitized, correlated, observable, and distinct from
   caller-correctable errors. Do not fabricate field-level guidance when the host
   cannot safely identify a field.

Read [failure-mapping-matrix.md](references/failure-mapping-matrix.md) when
choosing response category, evidence, or client behavior.

## Keep The Error Wire Single-Sourced — Published In Metadata rc.150

The `CustomProblemDetail` wire correction is published in
`praxis-metadata-starter` rc.150. Inspect `CustomProblemDetail`, the
Spring/Boot-configured Jackson mapper and MVC serialization path,
`GlobalExceptionHandler`, the generated error schema, and focused
serialization and HTTP tests before adopting it. A typed `code` or `target`
must produce one flat `errors[]` member; the inherited
`ProblemDetail.properties` map must not be a second authority for either
value. Null or blank `target` clears the typed field and must not leave a stale
extension that reappears after serialization or round-trip. Reserve
`type`, `title`, `status`, `detail`, `instance`, `message`, `category`, `code`,
`target`, and `properties`: `setProperty` rejects these keys and
`setProperties` validates and copies the caller's map before atomically
replacing it. `getProperties()` must not expose a mutable alias; distinguish
its empty `Map.of()` view from a map containing null extension values. Preserve
the public object shape and the property-based `message` creator on round-trip,
without reintroducing a legacy delegating-string form. The private JSON setter
must reject any incoming `properties` wrapper, including null, object, array,
or scalar, while legitimate Java `setProperties` remains available. Hide only
the Java container getter from the OpenAPI schema: the public schema still
declares flat `code`, `target`, `category`, and `status`, and must not become a
closed object that rejects legitimate flat extensions. Handle `traceId` and a
declared outcome according to their explicit contracts, without letting either
replace a typed field or expose a private cause.

The DTO must flatten legitimate extensions independently of an external
ProblemDetail mix-in: explicit `@JsonAnyGetter` on the immutable container view
and `@JsonAnySetter` on the validated extension setter preserve the same wire
and flat round-trip. Keep the explicit incoming `properties` rejection setter.
Test a plain `new ObjectMapper()` with no mix-in as well as the Spring-configured
mapper. A builder that installs the mix-in can mask a defect in the starter's
fallback ObjectMapper or a host-supplied mapper. Require absent container output
even for an empty extension map, null extension preservation, reserved-key
rejection and exact flat round-trip. Do not remove the no-wrapper HTTP oracle or
change a global mapper to hide a DTO contract inconsistency.

Prove the raw response JSON with the corresponding Spring/Boot-configured
mapper and MVC infrastructure: enable strict duplicate-member detection on
emitted bytes **before** `readTree`, which can discard a duplicate. Assert one
flat `errors[].code` and, when applicable, one
`errors[].target`; verify field clearing and round-trip, reserved-extension
rejection, all shapes of incoming `properties` wrapper, safe `traceId`/outcome,
and agreement with the declared schema fields. Include a real validation-field
error and a sanitized non-field failure. A focused Spring MVC test with its
real Jackson mix-in proves that
configuration, not an entire Boot host. Do not use `getProperties()` assertions
or a hand-built JSON tree as proof of the public wire. Record owner fix, HTTP
consumer proof, schema/corpus updates, and publication status separately.
Use `CustomProblemDetailTest` for constructor, map, clear, wrapper, and
round-trip behavior; `CustomProblemDetailHttpSerializationTest` for raw MVC
serialization; and
`AbstractResourceControllerJpaWriteIntegrationTest.resourceWritesPublishCanonicalStructuredFailureSchema`
for the served schema. Count only evidence actually run on the final source.

## Governed OpenAPI Publication Unavailability

For the governed 503 behavior published in Metadata `rc.149` and exercised by
the host in PR 340, inspect
`CachedOpenApiDocumentService.requirePublishedSnapshot`,
`GovernedOpenApiPublicationUnavailableException`,
`GlobalExceptionHandler.handleGovernedOpenApiPublicationUnavailable`, and
`docs/spec/BULK-OPERATION-LIFECYCLE.md`. The dedicated exception remains an
`IllegalStateException` subtype with its original private cause. Classify only
failures at the published-snapshot guard into that subtype; do not broadly map
`IllegalStateException`, callback failures, or programming errors to availability.
Unexpected failures outside that boundary retain sanitized HTTP 500.

Map the dedicated subtype through the canonical handler to HTTP 503, envelope
`failure`, category `SYSTEM`, and stable code
`GOVERNED_OPENAPI_PUBLICATION_UNAVAILABLE` in the published response. The
single-source wire correction above was published separately in Metadata
rc.150; the host must still prove adoption against that released artifact. Do not
infer rc.150 host behavior from this earlier 503 proof.
Use the fixed public message `Governed OpenAPI publication is temporarily unavailable.`
Never derive public message/detail from the cause or expose SQL, credentials,
stack traces, or private generation/digest diagnostics. Cold, suspended, or stale
publication denies structural serving without fresh HTTP or fallback. The 503
outcome authorizes neither automatic recapture nor a domain mutation retry:
`publish` and `reconcilePublished` remain explicit governed recovery operations
with their existing state/generation rules. Do not teach consumers to parse the
message, infer the private cause, or repeat a command because this code appeared.

Use `GovernedOpenApiPublicationUnavailableExceptionTest` to assert 503,
`failure`/`SYSTEM`, exact code and safe message, full public JSON without private
cause details, and cause identity retained for diagnostics. Preserve
`GlobalExceptionHandlerTest.shouldKeepGenericExceptionAsInternalServerError` as
the counterexample for unexpected `IllegalStateException`; validate actual
cold/suspended serving separately. Direct handler coverage alone does not prove
HTTP dispatch or host security; use the host's actual cold/suspended HTTP proof
for those claims. Do not describe this published 503 as an unpublished
`rc.146` candidate.

## Preserve Platform Boundaries

- `praxis-metadata-starter` owns canonical exception mapping, response shape,
  resource/action/filter/option-source semantics, and public metadata contracts.
- The host owns domain validation, authorization enforcement, translation of
  private persistence or integration failures, logging, correlation, and safe
  operational diagnostics.
- `praxis-ui-angular` consumes codes, field paths, statuses and declared action
  outcomes. It must not classify errors from English/Portuguese message text or
  infer a backend exception type from a status alone.

Do not route error handling by keywords, regexes, labels, or raw message matching.
Use structured status, category/code, field path, action/resource identity, and
declared operation context; text is explanatory only.

## Prove Success And Failure Together

For each changed operation, prove a valid request plus the relevant negative path:
field validation, missing target, denied state/authority, duplicate or idempotency
conflict, stale precondition, invalid option/filter request, and sanitized unknown
failure where applicable. Confirm invalid commands do not mutate data or trigger
external side effects. Verify field/action consumers can materialize the response.

Use focused exception-handler, controller, command, filter/option-source, and
quickstart HTTP tests. Run Angular form/action/runtime specs when a public error
shape or field mapping changes. Review docs and HTTP corpus only when they publish
the changed response contract.

## Companion Skills

- `praxis-java-command-concurrency-authoring`: command denial, conflict,
  precondition, idempotency, and safe outcome semantics.
- `praxis-java-filter-query-authoring`: invalid filter payload and query policy.
- `praxis-java-option-source-provider-authoring`: lookup/provider policy failures.
- `praxis-java-contract-conformance`: end-to-end error evidence and readiness.
- `praxis-metadata-schema-contracts`: public operation schemas and headers.

Close with failure-to-response mapping, sanitized HTTP evidence, no-mutation proof,
consumer materialization result, and any platform gap. An error contract is ready
when callers can recover or correct safely without learning backend internals.
