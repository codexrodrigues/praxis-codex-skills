---
name: ergon-forms-static-extraction
description: Extract and audit static Oracle Forms 6i metadata from admitted FMB baselines. Use for F1 inventory, coverage, source hashes, blocks, items, triggers, attached libraries and structural comparison; do not use for Forms runtime, compilation, Oracle execution or Cronos/browser sources.
---

# Ergon Forms Static Extraction

Operate only after an F0 gate selects a `TECHNICAL_POC_BASELINE` or stronger
baseline. Use the repository-owned `scripts/Export-Forms6iMetadata.ps1`; do not
invent a second extractor or copy Cronos XML tooling.

## Required workflow

1. Verify the FMB path and SHA-256 against the latest F0 gate.
2. Run the versioned exporter to a screen-specific static evidence directory.
3. Parse the JSON and inventory every projected block, item, form/block/item
   trigger, query data source and attached library.
4. Record coverage as `projected`, `empty`, `unsupported` or `failed`; absence
   from the current projection is never evidence that an object does not exist.
5. Produce a phase gate with executed commands, hashes, counts, residuals and
   exact return rules.

## Boundaries

- Static equality is equality only for the projected properties.
- Do not compile FMX, launch Builder/runtime, connect to Oracle, execute PL/SQL,
  infer visible behavior, define target API/UI, or promote business rules.
- Do not treat library names as resolved library identity; carry path/hash
  custody to F2.
- Keep raw source read-only and do not version Oracle binaries or credentials.
- If the baseline hash changes or extraction fails, return to F0.
