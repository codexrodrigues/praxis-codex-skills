# Package-Owned vs Host Custom

## Package-Owned Fields

Fields maintained by `@praxisui/dynamic-fields` must follow the canonical library path:

- editorial descriptor
- derived metadata
- derived catalog
- governed docs/inventory when relevant

Do not treat a library-owned field as a host extension workaround.

## Host Custom Fields

Host fields may use:

- `ComponentRegistryService.register(...)`
- `ComponentMetadataRegistry.register(ComponentDocMeta)`

This supports runtime plus controlled editorial fallback.

## Common Mistakes

- patching `dynamic-form` just to make a Praxis-owned field appear
- adding a new package-owned field without editorial descriptor
- consumer-specific alias workaround instead of fixing registry/editorial chain
- copying the library's internal editorial path into the host
