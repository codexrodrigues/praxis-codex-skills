[CmdletBinding()]
param(
    [string]$Repository = 'codexrodrigues/praxis-codex-skills',
    [string]$DraftRoot = 'docs/issue-drafts/skill-reviews',
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw 'Python not found. Run python3 scripts/create-skill-review-issues.py instead after installing Python.'
}

$script = Join-Path $PSScriptRoot 'create-skill-review-issues.py'
$pythonArgs = @($script, '--repo', $Repository, '--draft-root', $DraftRoot)
if ($DryRun) {
    $pythonArgs += '--dry-run'
}

& $python.Source @pythonArgs
if ($LASTEXITCODE -ne 0) {
    throw "Python issue creator failed with exit code $LASTEXITCODE."
}
