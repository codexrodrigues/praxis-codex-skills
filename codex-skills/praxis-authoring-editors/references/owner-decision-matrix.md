# Owner Decision Matrix

Use this file when the task is framed as "create or improve an editor" but the owning contract is not obvious yet.

## Fix Or Create In `@praxisui/settings-panel` When

- the task changes shell semantics shared by multiple editors
- footer actions, dirty/valid/busy protocol, shortcuts, drawer lifecycle, or host bridge are the real problem
- the editor needs platform-level `Apply` / `Save` / `Reset` / `Cancel` behavior, not lib-local reinvention
- multiple consumer editors show the same failure mode

Do not push shell contract logic down into a consumer editor just because the visible bug appears there first.

## Fix Or Create In The Consumer Lib When

- the config semantics belong to that lib
- the runtime of that lib already owns the document shape
- the task is exposing or correcting fields, sections, defaults, layout, rules, or payload semantics specific to that lib
- a new editor is needed to author an already-canonical runtime document for that lib

Examples:

- `@praxisui/dynamic-form` for `FormConfig`, layout, rules, messages, hooks, actions
- `@praxisui/table` for columns, behavior, toolbar actions, filter/table authoring
- `@praxisui/list` for list config semantics
- `@praxisui/page-builder` for page/widget/connection authoring

## Fix Or Create In `@praxisui/metadata-editor` When

- the task is structural metadata authoring, not one consumer's wrapper
- renderer coverage, schema normalization, hints, cascade flows, or contextual editing are the real owner
- a new editor path depends on canonical metadata-driven rendering support

Do not create one-off metadata editors in consumer libs when the missing capability belongs in the metadata editor.

## Redirect To `praxis-dynamic-fields-editorial` When

- the change is about `controlType`, aliases, descriptors, selector mappings, editorial discovery, or tooling/runtime divergence for dynamic fields

## Escalate To Platform Review When

- the runtime contract is unclear or duplicated
- the desired editor behavior implies a contract change across libs
- JSON/editor/runtime disagree on what the canonical document should be
- a faster local workaround would create a parallel contract
