# Downstream Consumers

## `@praxisui/metadata-editor`

Typical impacts:
- friendly name
- icon
- exposed properties
- inline editor coverage
- dynamic renderer grouping/hints

## `@praxisui/dynamic-form`

Typical impacts:
- `controlType` selection
- field metadata editor behavior
- hot metadata
- form behavior when field semantics change

## `praxis-filter`

Typical impacts:
- inline aliases
- compact component discovery
- filter settings UI
- inline tooling coverage

## Docs and Catalogs

Typical impacts:
- inventory
- field catalog
- field selection guide
- inline runtime contract
- derived coverage docs

When the change affects governed docs in this subarea, review the canonical files explicitly:

- `docs/dynamic-fields-inventory.md`
- `docs/dynamic-fields-field-catalog.md`
- `docs/dynamic-fields-field-selection-guide.md`
- `docs/dynamic-fields-inline-filter-catalog.md`
- `docs/dynamic-fields-inline-filter-runtime-contract.md`
- `docs/dynamic-fields-inline-components-guide.md`
- `docs/dynamic-fields-host-custom-field-guide.md`
- `docs/dynamic-fields-host-custom-field-troubleshooting.md`

## Rule

For every `dynamic-fields` change, ask:

- who consumes this discovery?
- who consumes this metadata?
- who depends on this alias?
- who depends on this documented coverage?
