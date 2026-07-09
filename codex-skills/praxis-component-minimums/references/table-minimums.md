# Table Minimums

## Local Minimum

Use this when the host wants a table without backend bootstrap.

Minimum path:

- render `<praxis-table>`
- provide local `data` and/or local `config`

This does not require remote schema discovery.

## Remote Minimum

Use this when the host wants the canonical Praxis remote table flow.

Minimum path:

- render `<praxis-table>`
- provide `resourcePath`
- ensure the host already has the Praxis API/CRUD wiring the runtime expects

When `resourcePath` is effective:

- the table configures remote mode
- schema bootstrap comes from `/schemas/filtered`
- data bootstrap comes from the backend resource/filter flow
- columns can be generated automatically from backend metadata

Remote bootstrap is not the same as optional operation availability. Export, bulk operations, and similar collection affordances need their own capability or link evidence.

## Important Rule

For remote table bootstrap, `resourcePath` is the canonical lightweight entry point.

But do not omit the host requirement:

- `resourcePath` alone is not enough if the host has no effective API/CRUD configuration
- `resourcePath` alone is not enough to claim collection export support
- for export, require `capabilities.canonicalOperations.export === true` or `_links.export`
- do not infer export support from a generic `POST /{resource}/export` route; the backend service must opt in

## Empty / Quick Connect

Without `resourcePath`, the table does not enter remote mode.
It falls into local or empty flow according to the runtime precedence.

The empty state can invite quick connection, but that is a UX helper, not the whole runtime contract.
