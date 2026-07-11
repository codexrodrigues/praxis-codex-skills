---
name: praxis-java-command-concurrency-authoring
description: Use when implementing, auditing, or migrating a Praxis Java business command with state changes: @WorkflowAction, command request/response schemas, ResourceCommandExecutionRequest and Result, idempotency, item or collection scope, resource version ETag, If-Match preconditions, conflict/denial outcomes, action availability, and safe Angular/runtime handoff.
---

# Praxis Java Command Concurrency Authoring

Treat a business command as an explicit governed transition, not a convenient PATCH.
It must state what changes, which state and authority permit it, retry behavior,
expected version, and a result that callers can safely materialize.

## Establish The Transition

Inspect resource, state model, CRUD path, action catalog, availability, command service,
persistence version, errors, direct consumer, and focused tests. Decide whether it is an
ordinary edit, item command, collection command, or accepted asynchronous operation.

Classify each command endpoint, request field, outcome, idempotency key, precondition,
ETag behavior, or action metadata as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or
`lacuna-real-de-contrato`. New command semantics belong in canonical resource/action
contracts, never in a host controller convention.

## Author The Command Contract

1. Model the transition with `@WorkflowAction`, stable ID, collection/item scope,
   schemas, side effect, authorization/state boundary, HTTP outcome, and negative path.
   Keep ordinary CRUD on the resource base.
2. Use dedicated request/response DTOs. Document intent, targets, validation,
   reversibility, confirmation, external effects, audit, and governance. Never reuse
   a create DTO or untyped map.
3. Use `ResourceCommandExecutionRequest`, `ResourceCommandExecutionProvider`, and
   `ResourceCommandExecutionResult` when the starter command infrastructure applies.
   Return accepted, denied, expected failure, or sanitized unexpected outcome deliberately.
4. Define idempotency by domain: scope, key, fingerprint, retention, replay result, and
   conflict behavior. Replay is valid only for the same caller-authorized command.
5. For mutable item commands, use resource-version ETag and `If-Match` when persisted
   version support exists. Reject stale or required-missing conditions canonically;
   never compare versions only in Angular or silently overwrite. Schema and resource
   version ETags solve different problems.
6. Align action catalog, capabilities, `ResourceStateSnapshot`, endpoint enforcement,
   and `_links`. Availability is not security; execution enforces the same decision.
7. For collection commands, define per-item outcome, atomicity, partial failure, retry,
   and ordering. Never report complete success when targets were denied or conflicted.

Read [command-outcome-matrix.md](references/command-outcome-matrix.md) when selecting
scope, preconditions, idempotency, result status, or focused proof.

## Preserve Boundaries

- `praxis-metadata-starter` owns command execution types, resource version
  preconditions, action discovery, schemas, and capability projection.
- The host owns domain transition, transaction boundary, idempotency storage,
  external-effect coordination, and authorization. Do not leak database version,
  package, queue, token, or internal exception details.
- `praxis-ui-angular` consumes action schemas, links, capabilities and safe conflicts.
  It does not infer idempotency or manufacture `If-Match` locally.

Do not resolve command intent from labels, route fragments, keywords, regexes, or aliases.
Use resource/action IDs, schemas, availability, capabilities, and governed context;
text can only rank already-scoped candidates.

## Prove The Command Under Stress

Prove permitted execution; denied state/authority; validation failure; same retry;
different conflicting command; stale/missing `If-Match`; result/status schema;
action/capability/`_links` alignment; and no repeated external side effect. For collection
commands, prove mixed outcome and atomicity/ordering rules.

Use focused command execution, version-precondition, action catalog, capability, and
negative-path tests. Add quickstart HTTP proof for public commands and Angular action
runtime tests when metadata or precondition behavior changes.

## Companion Skills

- `praxis-java-availability-discovery-authoring`: action, availability, capability,
  and HATEOAS alignment.
- `praxis-java-resource-authoring`: operation and DTO/service boundary.
- `praxis-metadata-discovery-capabilities`: canonical action/capability discovery.
- `praxis-metadata-schema-contracts`: action schemas, ETag, and public headers.
- `praxis-java-contract-conformance`: evidence pack and Angular readiness.

Close with transition matrix, idempotency/precondition policy, outcome contract, stress
evidence, and platform gaps. A command is ready when retry, stale, and denied callers
all receive deliberate safe behavior.
