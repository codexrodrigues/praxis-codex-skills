# Settings Panel Contract

## Canonical Ownership

- `@praxisui/settings-panel` owns the shell for runtime authoring UX.
- `SettingsPanelBridge` opens editor content.
- `SettingsValueProvider` exposes editor state and edited value.

## Shell Responsibilities

The shell owns:

- open/close lifecycle
- `Apply`, `Save`, `Reset`, `Cancel`
- observing `isDirty$`, `isValid$`, `isBusy$`
- emitting `applied$` and `saved$`
- drawer footer UX, shortcuts, and shell semantics

## Consumer Editor Responsibilities

The consumer editor owns:

- materializing the editable config/document
- internal editor/form consistency
- `getSettingsValue()`
- optional `onSave()`
- optional `reset()`
- reflecting incoming config correctly

## Minimum Signals

- `isDirty$`
- `isValid$`
- `isBusy$`

## Common Failures

- editor updates UI but not `getSettingsValue()`
- `Apply` and `Save` emit different shapes unintentionally
- `reset()` restores the wrong baseline
- dirty state never returns to clean
- consumer duplicates shell logic instead of fixing the shell
