[CmdletBinding()]
param(
    [string]$Repository = 'codexrodrigues/praxis-codex-skills',
    [string]$DraftRoot = 'docs/issue-drafts/skill-reviews'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw 'Python not found. Run python3 scripts/generate-skill-review-issue-drafts.py instead after installing Python.'
}

$script = Join-Path $PSScriptRoot 'generate-skill-review-issue-drafts.py'
& $python.Source $script --repository $Repository --draft-root $DraftRoot
if ($LASTEXITCODE -ne 0) {
    throw "Python issue draft generator failed with exit code $LASTEXITCODE."
}
