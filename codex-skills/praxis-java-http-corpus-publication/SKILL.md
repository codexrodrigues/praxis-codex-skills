---
name: praxis-java-http-corpus-publication
description: Use when publishing or auditing a Java/Praxis resource proof in praxisui-http-examples: canonical Quickstart/starter HTTP evidence, request and payload files, examples.manifest.json, sourceOfTruth, safety classification, responseShapeHint, LLM operational lanes, protected contracts, manifest generation, and focused corpus smokes.
---

# Praxis Java HTTP Corpus Publication

Publish a corpus entry only after the Java resource contract is proven. The corpus
indexes reproducible HTTP evidence for humans and AI; it does not become a second
source of schemas, metadata, authorization, or business behavior.

## Start From Canonical Evidence

Inspect the owning starter/Quickstart resource, controller, schemas, HTTP proof,
security/header requirements, and existing corpus entries. Classify the gap as
already supported, poorly materialized, partial, or a real corpus gap. Fix a
backend contract defect in its canonical owner before changing the example.

Choose one evidence slice: schema/discovery, read/filter, option reload,
action/surface/capability, stats/export, or a protected write. Preserve only
sanitized fixtures and deterministic non-secret headers/payloads.

## Publish The Example

1. Add the request and payload under the corpus conventions and record the
   canonical `sourceOfTruth`. Do not hard-code a workaround URL or invent headers.
2. Register every artifact in `examples.manifest.json` with method, endpoint,
   payload references, `responseShapeHint`, safety state, auth/header needs, and
   evidence flags. Keep `llmOperational`, `protectedContract`, and `referenceOnly`
   mutually exclusive.
3. Put safe, read-oriented, confirmed examples in the LLM lane only after the
   published backend proof succeeds. Keep destructive writes and protected flows
   out of the default lane; they may document contracts without becoming default
   operational prompts.
4. Regenerate derived LLM material from the manifest. Never hand-edit generated
   LLM surface files.
5. When smoke evidence disagrees with Java proof, classify runtime/corpus/canonical
   drift and repair the owner. Do not weaken flags to make a failing endpoint look
   operational.

Read [corpus-publication-matrix.md](references/corpus-publication-matrix.md)
when choosing example layer, required manifest evidence, or smoke gate.

## Boundaries And Validation

- `praxis-metadata-starter` owns schema/discovery/metadata semantics.
- `praxis-api-quickstart` owns reference-host HTTP behavior and proof.
- `praxisui-http-examples` owns derived request files, manifest claims, generated
  LLM surface, and corpus validation.

Run `npm run verify:manifest`; regenerate LLM surface when affected; run the
narrowest relevant public/auth/LLM smoke. State whether validation reached a
published backend or only checked structure. Use `praxis-java-contract-conformance`
when the Java resource itself still lacks evidence.

## Companion Skills

- `praxis-java-quickstart-proof`: obtain the operational Java proof first.
- `praxis-http-examples-corpus-manifest`: manifest and evidence flags.
- `praxis-http-examples-contract-surfaces`: request/header/payload semantics.
- `praxis-http-examples-llm-smoke`: safe LLM lane and smoke selection.

Close with canonical owner, example layer, manifest evidence, generated artifacts,
smoke result, and any unresolved backend gap. A corpus entry is ready when it
helps reproduce a real contract without making an unsafe flow look routine.
