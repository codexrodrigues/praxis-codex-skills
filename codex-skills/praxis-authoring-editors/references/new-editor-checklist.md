# New Editor Checklist

Use this checklist when creating a new Praxis visual editor or materially expanding one.

## 1. Canonical Contract

- identify the owning lib
- identify the exact config/document shape to be authored
- confirm runtime already consumes that shape, or fix runtime first
- avoid editor-only aliases, temporary shapes, and host-only shims

## 2. Ownership

- confirm whether the work belongs in `settings-panel`, the consumer lib, or `metadata-editor`
- if more than one area is touched, map the round-trip before editing

## 3. Editor Surface

- choose the concrete editor component family
- expose only canonical fields/sections
- wire labels, helper text, placeholders, empty states, and titles through the workspace i18n path
- keep structural panel semantics in `settings-panel`

## 4. Round-Trip

Verify the full path:

`open -> edit -> apply/save -> persistence -> reopen -> runtime consume`

Check specifically:

- field is visible when it should be
- edited value reaches `SettingsValueProvider` or equivalent output contract
- persisted document matches the canonical shape
- reopen restores the same value
- reset semantics are correct
- runtime reflects the saved document without compensating hacks

## 5. Governed Artifacts

Review the owning lib artifacts when the surface is public or governed:

- `README.md`
- `src/public-api.ts`
- subarea docs named by the local `AGENTS.md`
- focused specs for the affected editor family

## 6. Anti-Patterns

Do not:

- create the editor before clarifying contract ownership
- patch only the host when the lib contract is wrong
- support a field only in JSON and call the editor "done"
- persist a different shape than the runtime consumes
- fix `Apply` but ignore `Save`, `Reset`, or reopen
- hardcode internal authoring text outside the canonical i18n path
