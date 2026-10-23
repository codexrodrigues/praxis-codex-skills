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

For operational approval/workflow/validation admission, inspect Config's
`docs/domain-rules/operational-policy-resolution.md` and use the public embedded
`OperationalPolicyService.resolveOperationalPolicy(OperationalPolicyTarget,
DomainRuleGovernancePrincipal)` instead of reading repositories or the UX list.
Pass authenticated scope already resolved by the host. Target grammar/family
validation is not resource/action existence or authorization; validate those in
the canonical host registry.

Preserve NEVER_APPLIED, ELIGIBLE_APPLIED_HEAD,
PREVIOUSLY_APPLIED_WITHOUT_ELIGIBLE_HEAD and INCONSISTENT_OR_UNAVAILABLE. Initial
absence allows continuation only when the operation explicitly declares
ALLOW_IF_NEVER_APPLIED, still with mandatory lookup. Withdrawal/error/inconclusive
history block; never catch a Config failure and return empty. Only an eligible
head carries a verified typed effect/payload. ALLOW does not bypass other gates,
segregated approval or domain invariants. Bind/revalidate the resolution fingerprint
at the orchestrator's documented unit boundaries; it is not instantaneous
revocation across the independent Config and domain transactions.

For protected bulk evaluation, the host maps that canonical resolution into Metadata's
`BulkPolicyObservation` (trusted tenant/environment, canonical target coordinates, state,
fingerprint and observedAt) inside mandatory `BulkEvaluationGovernance`. Keep the full
resolution for actual evaluation of effect/specialization; the Metadata observation is
opaque provenance, not a second policy engine or a public evidence reference. The required
policy target set and its consistent capture belong to the provider. Bind the real evaluator
revision and current authorization fingerprint; do not manufacture a grant revision from
JWT claims or a static authority catalog. The current HTTP gate does not certify worker
identity. `matchesCurrentEvidence` requires fresh reads and validated outcomes before use;
equality cannot turn withdrawal/error or unsupported specialization into admission. See
Metadata `docs/spec/BULK-EVALUATION-EVIDENCE.md`; SDK storage/comparison proof does not close
the corporate grants/provider/READY gates or instantaneous revocation across transactions.

Quickstart now supplies a host-owned current-grant foundation in
`QuickstartOperationalContextResolver` / `QuickstartPrincipalGrantRepository`; inspect
`docs/OPERATIONAL-GRANTS-CONTEXT.md` and pair with `praxis-api-quickstart-security-config`.
It binds a dedicated operational database to immutable namespace/tenant/environment, reads
revocable versioned grants independently under READ COMMITTED and publishes Config's existing
server attributes only after authorization. Its fingerprint covers the grant and required
authority, not field/target/reference authorization. Provider adoption, multi-coordinate
policy capture, ETag scope wiring, worker identity and READY remain separate gates; do not
invent an empty Metadata context SPI before an actual consumer establishes the requirement.
The existing HTTP policy gate is not automatically switched to this new source.

Audit every early return around admission, including missing business input and
cached idempotent responses. A mandatory policy read must not disappear on those
branches. Checking current policy does not prove that an existing receipt ledger
is tenant/environment-scoped; verify that separately before claiming corporate
replay isolation. Registry authority hints supplement domain authorization.
Use trusted server tenant/environment context; an explicitly configured corporate
single-tenant default is not proof of multi-tenant identity propagation.

Test specialized host evaluators against the canonical producer and real authored
fixtures, not only hand-written projection JSON. Backend validation currently
copies definition parameters, including the nested validationPolicy effect marker;
verified legacy BLOCK may lack that marker. When present, validate it. Workflow
requiredStates can coexist with the canonical condition over `state`; supplier
blockedStatuses can coexist with the condition over `supplier.status`. Equivalent
representations must agree. Unsupported or contradictory specializations fail
closed, rather than being filtered out as absent policy. Do not generalize these
specialists into an undocumented rule evaluator.

Author a replacement through existing Config review/publication routes. New
operational publications require explicit effect in the source's existing policy
slot; do not patch the payload in the host. Old unverifiable hashes require a
new governed identity for the same target, not history rewrites. Keep lifecycle
calls in a clean Config persistence context under READ COMMITTED; Config rejects
pending external entity changes before its PostgreSQL scope mutex. Its independent
read may need an extra Config pool connection. Keep domain persistence separate.

For the pre-release Quickstart proof, enable both `praxis.palette.proof=true` and
`praxis.operational.policy.proof=true` against the isolated candidate. The latter
must fail if the Java API/bean is absent. The focal HTTP test uses Config PostgreSQL
and proves publication, retirement and ALLOW replacement in all three families.
Verify candidate identity in the packaged host; do not claim SNAPSHOT publication,
migration DDL proof from the host fixture, or completed bulk-provider adoption.
Compile production consumers with real SDK imports. An isolated SNAPSHOT override
proves a candidate, not that the committed dependency pin can compile. Keep that
adoption in a draft PR until a published, resolvable coordinate supplies the API;
do not hide this gate through reflection, a production fallback, or a silent pin
change. In HTTP probes, use the resource controller baseline actually discovered
by the action/surface registries; annotations alone on arbitrary controllers do
not prove registered resource admission.

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
