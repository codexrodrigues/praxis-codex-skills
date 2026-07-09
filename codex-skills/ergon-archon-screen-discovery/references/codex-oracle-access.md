# Codex Oracle Access Provisioning

Use this reference to provision Oracle access for Codex-operated screen discovery.

## Goal

Codex should run Oracle metadata confirmation directly during investigations. Developers should not need to manually run confirmation scripts for normal discovery work.

## Required Runtime Inputs

Configure these outside the repository and outside the skill files:

```powershell
$env:ERGON_SQLCL = 'D:\Developer\Techne\ErgonX\migracao\tools\sqlcl\bin\sql.exe'
$env:ERGON_HADES_CONN = '<wallet-alias-or-connection-string>'
```

`JAVA_HOME` may also be set explicitly when the workstation has multiple Java runtimes.

For this migration workspace, use this standard local bootstrap file:

```text
secrets\ergon.env.ps1
```

The file should be ignored by Git and sourced by Codex when Oracle access is needed:

```powershell
. .\secrets\ergon.env.ps1
```

Codex may check whether expected variables are set, but must not print the file contents.

## Preferred Secret Handling

Use one of these approaches:

1. Oracle Wallet alias in `ERGON_HADES_CONN`.
2. A workspace/session environment variable injected by the Codex launcher or local environment setup.
3. A temporary connection string supplied only inside the active private session.

Do not store full Oracle connection strings, usernames, passwords, hostnames, service names, wallet passwords, or customer-sensitive values in:

- `SKILL.md`
- generated investigation reports
- generated SQL files
- commits
- issue trackers
- shared prompts
- terminal logs intended for handoff

## Verification Command

After provisioning, Codex can verify access without printing the secret:

```powershell
if ($env:ERGON_HADES_CONN) { 'ERGON_HADES_CONN=SET' } else { 'ERGON_HADES_CONN=NOT_SET' }
if ($env:ERGON_SQLCL) { 'ERGON_SQLCL=SET' } else { 'ERGON_SQLCL=NOT_SET' }
```

Then Codex should execute screen-specific confirmation SQL:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query.ps1 `
  -SqlFile docs\migracao\<SCREEN>\oracle-confirmation.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\confirmation.txt
```

If SQLcl fails in non-interactive Codex execution with a Windows console error, use the JDBC fallback:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile docs\migracao\<SCREEN>\oracle-confirmation.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\confirmation.txt `
  -MaxRows 500
```

For HADES screen registry or stored XML discovery, Codex can run the screen-definition discovery orchestrator without exposing credentials:

```powershell
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\find_hades_screen_definition.ps1 `
  -Screen ERGadm00189 `
  -MainView ERGADM00189_FREQUENCIAS `
  -OutputDir docs\migracao\ERGadm00189\oracle-results
```

Use `-IncludeXmlMarkers` for a deeper XML marker pass and `-IncludeBlobSearch` only when BLOB/resource candidates are likely. Owner-wide searches across legacy text/CLOB/BLOB columns can be slow and noisy.

## Investigation Rule

If Oracle access is configured, Codex must run the confirmation SQL and update the investigation gates. If Oracle access is not configured, Codex should generate the SQL and mark Oracle evidence as pending instead of asking a developer to execute it manually.
