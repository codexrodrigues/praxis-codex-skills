# Runtime vs Editorial Chain

## Layers

### Runtime Registry
Responsible for loading the actual component by `controlType`.

Owner:
- `ComponentRegistryService`

### Metadata/Editorial Registry
Responsible for discoverable name, icon, and editorial identity.

Owner:
- `ComponentMetadataRegistry`
- descriptors in `src/lib/editorial/**`

### Derived Catalog/Inventory
Responsible for governed derived discovery surfaces.

### Downstream Consumers
Main consumers:
- `@praxisui/metadata-editor`
- `@praxisui/dynamic-form`
- `praxis-filter`
- editorial tooling

## Rule

A change is complete only when the relevant chain remains coherent.

Runtime success alone does not prove editor/tooling correctness.
