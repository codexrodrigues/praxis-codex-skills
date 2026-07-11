---
name: praxis-java-config-boundary-integration
description: Use when implementing, auditing, or migrating a Java/Praxis integration between metadata-driven resources and praxis-config-starter: governed decision materializations, /api/praxis/config/**, ui_user_config, ai_registry, api_metadata, host security, Origin and ETag boundaries, and Quickstart/Angular proof.
---

# Praxis Java Config Boundary Integration

Use this skill when a Java host needs both resource metadata and governed
configuration. `praxis-metadata-starter` owns resource structure;
`praxis-config-starter` independently owns persisted configuration, AI
grounding, and the lifecycle of semantic decisions. A host consumes published,
deterministic materializations. It does not recreate their authoring lifecycle.

## Audit Before Integrating

Inspect the resource annotations, filtered schema, surfaces, actions,
capabilities, host security configuration, config-starter auto-configuration,
and the downstream Angular or Quickstart proof. Classify each request as:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

First ask what the platform already knows but is not materializing. A new DTO,
annotation, config endpoint, or resource field is justified only by a real gap
that names the missing canonical data, owner, consumers, derived artifacts, and
minimum proof.

Read [config-integration-matrix.md](references/config-integration-matrix.md)
before deciding the owner or coupling an endpoint.

## Keep The Boundaries Intact

- `praxis-metadata-starter` owns `@ApiResource`, resource-oriented services and
  controllers, `x-ui`, `/schemas/filtered`, catalog/surface/action discovery,
  and resource or instance capabilities.
- `praxis-config-starter` owns `/api/praxis/config/**`, `ui_user_config`,
  `ai_registry`, `api_metadata`, governed Domain Knowledge/Rule intake,
  simulation, approval, publication, and materialization.
- The Java host owns dependency wiring, authenticated principal resolution,
  authorization, data-source configuration, and application of a published
  materialization to its runtime extension point.
- Angular consumes the resulting resource/config contracts. It is not the
  source of truth for policy, tenant scope, ETag, or decision lifecycle.

Do not put config documents, authoring status, raw prompts, decision definitions,
or approval state into a resource DTO or `x-ui`. Do not create a second schema
endpoint under metadata for configuration merely because a screen needs it.

## Integrate A Published Decision

1. Model the domain resource canonically with the resource baseline and expose
   its schemas, actions, surfaces, and capabilities independently of config.
2. Resolve a shared policy, eligibility, validation, workflow action, or UI
   rule through the config decision owner. Preserve tenant, environment,
   resource identity, target identity, source hash, status, diagnostics, and
   evidence references.
3. Simulate, review, approve where governance requires it, and publish through
   the config boundary. A host must consume the applied materialization, never
   a draft, a guessed assistant answer, or a UI-local rule.
4. Bind that deterministic projection at the host extension point. Keep
   unavailable, failed, superseded, reverted, or scope-mismatched projections
   inactive; never silently fall back to a locally inferred policy.
5. Keep config persistence separate from domain persistence. The config starter
   owns its migrations and identity semantics; do not copy `ui_user_config`,
   registry, or metadata tables into the business service.

For user configuration, preserve `X-Tenant-ID`, optional user/environment
scope, quoted ETag conditional reads/writes, secret sanitization, and exact
scope resolution. For protected config APIs, enforce the documented `Origin`,
authenticated principal, tenant/context validation, and authorization at the
host. Caller headers are not corporate authorization.

## Grounding And Safety

`api_metadata`, Domain Catalog, Project Knowledge, and filtered schemas are
grounding evidence, not a text router or a replacement for current resource
semantics. Resolve intent semantically with governed AI/tools and canonical
context first; aliases or lexical matching may only rank candidates after scope
is resolved.

Never expose raw prompts, private evidence, tokens, roles, SQL, or unredacted
config payloads through resource responses, diagnostics, capability snapshots,
or HTTP examples. A config endpoint failure must remain visible as a config
failure; it must not make the resource invent a local decision.

## Prove The Integration

Prove each owner separately, then prove their seam:

1. Run the focused metadata/resource tests and verify `/schemas/filtered`,
   actions, surfaces, and capabilities still describe the resource.
2. Run the focused config-starter tests for the affected persistence, decision,
   grounding, or registry contract.
3. Exercise the host with required Origin and identity headers: an approved,
   in-scope applied materialization changes the intended runtime behavior;
   draft, unpublished, stale, cross-tenant, or invalid materializations do not.
4. Verify ETag conflict and secret-redaction behavior for persisted user config
   when that contract is involved.
5. Use Quickstart and Angular proof only as downstream consumers. Publish a
   HTTP corpus example only after the host proof succeeds and retain the proper
   protected/read-only classification.

Use the smallest focused suites first. For a shared public contract, also review
Quickstart security/config proof, Angular core config consumers, public docs,
and HTTP corpus artifacts. State clearly which runtime proof was executed and
which one remains unavailable.

## Companion Skills

- `praxis-java-resource-authoring`: canonical metadata-driven resource shape.
- `praxis-java-contract-conformance`: resource contract and downstream proof.
- `praxis-config-runtime-persistence`: config headers, scope, ETag, and secrets.
- `praxis-config-domain-decisions`: decision governance and materialization.
- `praxis-config-api-metadata-grounding`: grounded API/schema evidence.
- `praxis-api-quickstart-security-config`: host Origin/security proof.

Close with the ownership classification, applied materialization identity,
host extension point, focused validation, and any real contract gap. The result
is correct when metadata remains canonical for resources and config remains
canonical for governed decisions and persistence.
