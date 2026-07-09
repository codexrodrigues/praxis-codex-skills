# Authoring Round-Trip Checklist

1. Identify the canonical config/document source.
2. Identify the concrete editor family and canonical owning lib.
3. Open the canonical editor.
4. Confirm the changed field:
   - appears
   - has the correct label
   - is editable
   - uses the correct default
5. Change the value.
6. Apply or save.
7. Confirm runtime reflects the change.
8. Reopen the editor.
9. Confirm the value persists without drift.
10. Exercise reset when relevant.
11. Confirm no adjacent config was lost.
12. If the surface is public, review the owning lib `README`, `public-api`, and governed docs for sync.

## Explicit Risks To Check

- supported in JSON but invisible in editor
- visible but not persisted
- persisted but ignored by runtime
- `Apply` works and `Save` fails
- `Save` works and reopen rewrites
- `Reset` clears too much
- defaults mask a persistence bug
- metadata renderer or coverage checklist lies about support
- internal authoring text is correct functionally but still hardcoded
