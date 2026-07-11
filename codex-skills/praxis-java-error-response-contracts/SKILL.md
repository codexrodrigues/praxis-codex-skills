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
