---
name: praxis-reactive-determinations
description: Use when implementing, auditing, or proving Praxis Reactive Determinations across metadata, governed rule snapshots, Java hosts, Angular Dynamic Form/CRUD/Stepper, diagnostics, and HTTP corpus: definition registries, trigger/form modes, input/output bindings, provenance, execution ordering, stale/cancel handling, last-known-good snapshot consumption, or migration away from legacy Form Effects.
---

# Praxis Reactive Determinations

Use this skill for the end-to-end handoff from a governed semantic decision to
reactive form behavior. Reactive Determinations replaced the former Form Effect
contract; do not reintroduce removed `@FormEffect` annotations, `formEffects`
schema blocks, or frontend-authored business formulas.

## Canonical Owners

- `praxis-config-starter` owns governed domain-rule authoring, approvals,
  publication, immutable snapshots, active heads, rollback, and materialization.
- `praxis-metadata-starter` owns the public metadata vocabulary and compiles
  registered determination definitions into operation-specific `x-ui` schema.
- The Java host owns facts, executable provider/registry implementations,
  authorization, transactions, and business effects.
- `praxis-ui-angular` owns the generic runtime materialization and diagnostics.
  It does not become the business-rule owner.
- Quickstart and HTTP Examples prove the chain; they do not redefine it.

## Required Source Audit

Inspect the affected owner and direct consumers:

- Metadata `docs/spec/reactive-determinations.md`,
  `uischema/determination/**`, compiler and contract specs
- Config `DomainRuleReactiveDeterminationSpec`, snapshot/control-plane services,
  materialization migration, rule tests, and active-head rules
- Quickstart `ReactiveDeterminationPilotConfiguration`, applied resolver,
  provider/ruleset, tenant-scope and resolver tests
- Angular Core reactive-determination model, Dynamic Form runtime service/spec,
  CRUD dialog/drawer handoff, Stepper adapter, Metadata Editor diagnostics, and
  component metadata/registry projection
- HTTP examples, payloads, manifest, corpus verifier, and smoke

## Contract Rules

- A definition has stable identity, scope, applicable form modes, trigger mode,
  typed input bindings, typed output bindings, and provenance.
- Resolve operation-specific metadata for the actual create/edit/action surface.
  A definition present on another operation is not applicable evidence.
- Input bindings read the current governed form snapshot. Output bindings write
  only declared targets under their documented write policy; do not patch
  arbitrary config or component state.
- Preserve definition/snapshot provenance through metadata, runtime diagnostics,
  HTTP evidence, and authoring explanations. Labels and prompts cannot select a
  determination.
- Order executions deterministically. When inputs change again, stale results
  must not overwrite a newer form state. Cancellation, debounce, concurrency,
  and partial output behavior must be explicit and tested.
- Fail closed for unknown definitions, invalid bindings, missing provider,
  incompatible snapshot, denied scope, malformed result, or unresolved output.
  Do not fall back to a local formula or legacy Form Effect.
- A host consuming governed snapshots validates scope, compatibility, content
  hash, head identity, and monotonic activation before an atomic last-known-good
  swap. A failed candidate leaves the last valid runtime active and visible in
  health/diagnostics without leaking snapshot payloads.
- Dynamic Form owns generic execution and form-state application. CRUD and
  Stepper pass the correct operation/form context; they do not duplicate the
  determination engine.

## Implementing Reactive Determinations in a New Java/Spring Boot Host (Step-by-Step)

When building or evolving a Spring Boot host that uses `praxis-metadata-starter`, implement Reactive Determinations with the following exact contract so `ReactiveDeterminationMetadataCompiler` compiles `x-ui.reactiveDeterminations` into `GET /schemas/filtered` without failing closed:

### 1. Declare Output/Preview Fields on `CreateDTO` and `UpdateDTO`
- `ReactiveDeterminationMetadataCompiler` verifies that **every** `input.fieldPath` and `output.fieldPath` exists in the form operation's request body schema (`CreateDTO` for `CREATE`, `UpdateDTO` for `EDIT`).
- If a reactive determination populates a read-only preview or calculated field (e.g., `netSalary`, `availableVacanciesPreview`, `expectedEndDate`), declare that field on both `CreateDTO` and `UpdateDTO` (annotated with `@UISchema(readOnly = true, ...)` when the user should not edit it manually).

### 2. Declare Explicit `@Operation(operationId = ...)` on Form Operations and the Capability Endpoint
Because `AbstractResourceController` inherits `create` and `update`, SpringDoc generates unstable default `operationId`s (`create_1`, `create_2`) across multiple controllers unless overridden. Always override `create` and `update` with explicit `operationId`s and expose a non-persisting `POST` determination endpoint (without path variables):

```java
@PostMapping
@Operation(
    operationId = "createEmployee",
    summary = "Create employee record",
    description = "Creates an employee record after validating position capacity and compensation."
)
@Override
public ResponseEntity<RestApiResponse<EmployeeResponseDTO>> create(@Valid @RequestBody CreateEmployeeDTO dto) {
    return super.create(dto);
}

@PutMapping("/{id}")
@Operation(
    operationId = "updateEmployee",
    summary = "Update employee record",
    description = "Updates an existing employee record and revalidates compensation and assignment."
)
@Override
public ResponseEntity<RestApiResponse<EmployeeResponseDTO>> update(
        @PathVariable Long id,
        @Valid @RequestBody UpdateEmployeeDTO dto) {
    return super.update(id, dto);
}

@PostMapping("/determinations/position-compensation-preview")
@Operation(
    operationId = "determineEmployeePositionCompensationPreview",
    summary = "Determine position floor, work schedule, and available vacancies",
    description = "Non-persisting reactive determination that projects position parameters and vacancy balance while editing the employee form."
)
public ResponseEntity<PositionCompensationPreviewResponse> determinePositionCompensationPreview(
        @Valid @RequestBody PositionCompensationPreviewRequest request) {
    return ResponseEntity.ok(service.determinePositionCompensationPreview(request));
}
```

### 3. Register `@Bean ReactiveDeterminationDefinitionProvider`
Bind the form operation `operationId`s (`ReactiveDeterminationScope`) to the determination capability `operationId` using valid JSON Pointers starting with `"/"`:

```java
@Configuration(proxyBeanMethods = false)
public class EmployeeReactiveDeterminationConfig {

    @Bean
    ReactiveDeterminationDefinitionProvider employeePositionCompensationDeterminationProvider() {
        return () -> List.of(
            new ReactiveDeterminationDefinition(
                "human-resources.employees.position-compensation-preview",
                List.of(
                    new ReactiveDeterminationScope("createEmployee", ReactiveDeterminationFormMode.CREATE),
                    new ReactiveDeterminationScope("updateEmployee", ReactiveDeterminationFormMode.EDIT)
                ),
                "determineEmployeePositionCompensationPreview",
                ReactiveDeterminationTriggerMode.ON_CHANGE,
                List.of("/positionId", "/departmentId"),
                List.of(
                    new ReactiveDeterminationInputBinding("/positionId", "/positionId"),
                    new ReactiveDeterminationInputBinding("/departmentId", "/departmentId")
                ),
                List.of(
                    new ReactiveDeterminationOutputBinding("/baseSalaryFloor", "/baseSalaryFloor"),
                    new ReactiveDeterminationOutputBinding("/defaultWeeklyHours", "/weeklyHours"),
                    new ReactiveDeterminationOutputBinding("/availableVacanciesPreview", "/availableVacanciesPreview")
                ),
                new ReactiveDeterminationProvenance(
                    ReactiveDeterminationProvenanceKind.HOST,
                    "hr-host-service",
                    "1"
                )
            )
        );
    }
}
```

### 4. Five Strict Compiler Invariants (`ReactiveDeterminationMetadataCompiler`)
1. **Valid JSON Pointers (`/`):** Every `sourcePath`, `input.fieldPath`, `input.requestPath`, `output.responsePath`, and `output.fieldPath` must start with `"/"` (e.g., `"/positionId"`).
2. **`sourcePaths` Subset of `inputs`:** Every path in `sourcePaths` must also appear as an `input.fieldPath` in `inputs`. (In `EDIT` mode, you may pass additional context inputs such as `new ReactiveDeterminationInputBinding("/id", "/employeeId")` in `inputs` without listing `"/id"` in `sourcePaths`).
3. **Schema Property Existence:** Every `input.fieldPath` and `output.fieldPath` must resolve in the `CreateDTO`/`UpdateDTO` OpenAPI schema, every `input.requestPath` must resolve in the determination `Request` DTO schema, and every `output.responsePath` must resolve in the determination `200 OK` `Response` DTO schema.
4. **Non-Overlapping Inputs and Outputs:** `input.fieldPath` and `output.fieldPath` must never be identical or parent/child of each other within the same definition (prevents infinite trigger loops).
5. **Form Mode HTTP Method Match:** `ReactiveDeterminationFormMode.CREATE` requires a `POST` form operation; `ReactiveDeterminationFormMode.EDIT` requires a `PUT` or `PATCH` form operation; and the determination capability operation (`definition.operationId()`) must be a `POST` operation without `{...}` path parameters.

### 5. Deep Domain Discovery for Reactive Determinations ("Além do Óbvio" — 4 Families)
Do not leave enterprise forms passive until submit. Audit `CreateDTO`, `UpdateDTO`, and entity relationships to discover Reactive Determinations across four families:
1. **Cross-Entity Lookup & Directory Projection:** When the user selects a foreign key or code (`"/postalCode"`, `"/positionId"`, `"/departmentId"`, `"/contractPlanId"`), auto-populate address fields, salary floor, standard work schedule, cost center, or responsible manager.
2. **Multi-Field Deterministic Calculations:** When gross amount, deductions, rate, or start date + duration change (`"/grossSalary"`, `"/baseDeductions"`, `"/startDate"`, `"/probationDays"`), compute net amount, total deductions, or expected end/review date in real time.
3. **Chained Reactive Determinations (`A -> B -> C`):** When Determination 1 writes an output field (e.g., `"/netSalary"`), a second `ReactiveDeterminationDefinition` that lists `"/netSalary"` in its `sourcePaths` and `inputs` is automatically triggered by `@praxisui/dynamic-form` to compute downstream fields (e.g., `"/expectedPaymentDate"` or approval tier).
4. **Draft Policy, Quota & Eligibility Preview:** While the user fills out an assignment or movement form, evaluate vacancy balance, qualification compatibility, or schedule conflict and populate read-only preview fields (`"/availableVacanciesPreview"`, `"/eligibilityDiagnosticPreview"`) before submit.


## Chained governed calculations

For an engine contract that supports direct dependency outputs (1.5 G1), compose
versioned host Java calculations through the approved RuleSet DAG and evaluate
once per request. The engine runtime skill defines the restricted output channel;
metadata input/output bindings are not an alternative dataflow engine. Validate
the published engine coordinate before adoption: beta.15/contract 1.4 does not
transport intermediate outputs. G1 source tests alone do not prove an operational
Reactive Determination or an adopted dependency.

Keep derived facts out of submitted authority. Preview, command and sandbox
must use the same executable registry and evaluation service. A downstream
calculation consumes and validates its direct predecessor's typed output; never
repair missing output with a second evaluation, local formula or client value.
The Java output channel does not expose prior outputs to JSON Logic or replace
form cancellation, provenance, precondition capture and stale-result handling.
Use existing execution status/pending/unsatisfied evidence for UX; completion of
pending alone is not satisfaction. Preserve the draft on technical failure or
precondition conflict, distinguish prior displayed values from current valid
results, and never automatically refresh concurrency tokens and resubmit.
Do not expose raw engine results or mistake concurrent unit tests for tenant
authorization proof. Test the actual package and authenticated HTTP/UI handoff.
Prove the chain without prefilled derived values before claiming the example is
ready, then prove the actual published packages and HTTP/UI handoff separately.

## Financial draft and dependent-resource handoff

For payroll facts, three payment dates or event create/edit/move, read
[the financial handoff procedure](references/payroll-financial-handoff.md).
It separates the host's financial/CAS authority from the consumer's snapshot
capture, real metadata FormArray, persistent validation and runtime satisfaction.
Inspect the actual published Core/Dynamic Form packages before changing a generic
contract. Treat G4 source and mocked consumer tests as candidate evidence until
the corresponding schema, authenticated HTTP, isolated Neon and UI gates pass.

## Governed runtime upgrades

Before adopting a new engine contract, inventory every active-snapshot consumer, including secondary pilots, caches, preload jobs, fixtures and public receipts. Config owns historical verification versus executable admission: an intact incompatible snapshot remains history, while an invalid one must not be relabeled merely incompatible. Never rewrite hashes, approvals or engine tuples in persisted snapshots.

Publish a newly approved compatible composition without activating it, prewarm with the real host registry, report canonical probes and perform explicit conditional activation. Absence of a head requires the governed bootstrap rollout; it is not a shortcut around readiness. Candidate preload cannot establish last-known-good. Run the 1.4→1.5 cutover under maintenance without mixed-version traffic. After the first 1.5 selection, recover forward to the compatible line; do not resume the old runtime over migrated heads. Test all affected families, partial cutover/recovery, rollback within the compatible line and rejection of old-line activation. Preserve draft/result diagnostics in UI and distinguish source tests, candidate package tests, published dependency adoption and real authenticated HTTP/UI proof.

Close the upgrade proof only after a real non-persisting consumer operation and official host observation confirm active adoption after A, B and same-line rollback. Match the selected scope, snapshot/hash and activation identity; candidate readiness alone is insufficient.

## Implementation Workflow

1. Inventory what the platform already publishes: active decision/snapshot,
   registered definition, operation schema, bindings, runtime service,
   diagnostics, and HTTP proof.
2. Classify the gap. Missing UI diagnostics or adapter propagation is not a new
   metadata contract. Missing business logic belongs to Config/host, not Angular.
3. Implement at the canonical owner and update the complete handoff only where
   its public projection changed.
4. Preserve beta cleanup: migrate consumers and derived docs in the same cycle;
   do not keep parallel Form Effect and Reactive Determination paths without an
   explicit operational requirement.
5. Prove tenant/operation/form-mode isolation and sanitized diagnostics.

## Proof Matrix

Minimum focused gates:

```bash
# metadata owner
mvn "-Dtest=ReactiveDeterminationMetadataCompilerTest,ReactiveDeterminationSpecContractTest" test

# Angular runtime
npm run test:core -- --include=projects/praxis-core/src/lib/models/form/reactive-determination.model.spec.ts
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/services/reactive-determination-runtime.service.spec.ts

# quickstart host
mvn "-Dtest=AppliedReactiveDeterminationResolverTest,ReactiveDeterminationTenantScopeHttpTest" test

# HTTP corpus
node smoke/verify-reactive-determination-corpus.mjs
node smoke/smoke-reactive-determinations.mjs
```

Run each command from its owning repository and add Config snapshot/rule tests
when authoring, publication, head, or materialization changes.

Prove happy execution, invalid inputs/business rejection, stale/cancel race,
tenant or operation mismatch, incompatible snapshot/LKG behavior, and absence
of legacy Form Effect output. Review Metadata docs, Angular JSON API/registry,
Quickstart pilot docs, HTTP manifest/LLM surface, and public examples whenever
the mirrored contract changes.

## Companion Skills

- `praxis-config-domain-decisions` and `praxis-rules-engine-runtime`: governed rule/snapshot lifecycle.
- `praxis-metadata-schema-contracts`: operation-specific schema and `x-ui` publication.
- `praxis-form-schema-runtime-modes` and `praxis-form-actions-hooks-runtime`: Angular form context and lifecycle.
- `praxis-crud-dialog-form-host-lifecycle` and `praxis-stepper-wizard-runtime`: host adapters.
- `praxis-api-quickstart-domain-pilots` and `praxis-http-examples-contract-surfaces`: operational/public proof.
