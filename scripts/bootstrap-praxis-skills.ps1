[CmdletBinding()]
param(
    [ValidateSet('praxis', 'ergon-migration')]
    [string]$Family = 'praxis',
    [string]$ManifestPath,
    [string]$RepoRoot,
    [string]$SkillsRoot,
    [switch]$DryRun,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$syncScript = Join-Path $PSScriptRoot 'sync-praxis-skills.ps1'
if (-not (Test-Path -LiteralPath $syncScript -PathType Leaf)) {
    throw "Sync script not found: $syncScript"
}

$syncArgs = @{
    Family = $Family
}

if ($ManifestPath) {
    $syncArgs.ManifestPath = $ManifestPath
}
if ($RepoRoot) {
    $syncArgs.RepoRoot = $RepoRoot
}
if ($SkillsRoot) {
    $syncArgs.SkillsRoot = $SkillsRoot
}
if ($DryRun) {
    $syncArgs.DryRun = $true
}
if ($Force) {
    $syncArgs.Force = $true
}

& $syncScript @syncArgs

if ((Get-Variable -Name LASTEXITCODE -Scope Global -ErrorAction SilentlyContinue) -and $LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Codex skills bootstrap complete."
