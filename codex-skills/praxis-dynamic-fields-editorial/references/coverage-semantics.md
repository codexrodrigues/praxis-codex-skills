# Coverage Semantics

## Coverage Types

### Runtime Coverage
The component renders and behaves correctly at runtime.

### Schema/Type Coverage
Types and public metadata reflect supported contract paths.

### Editor/Tooling Coverage
The field is discoverable, named correctly, and usable in editor/tooling.

## Main Rule

Do not collapse all three into one generic "supported" statement.

## Attention Cases

- runtime true, editor/tooling false
- schema/type true, no discovery evidence
- docs claim visual/editor support without proof

## Mismatch Policy

When runtime and editor/tooling diverge:

- keep the mismatch explicit and traceable
- do not hide it with vague wording
- review governed docs/inventory accordingly
