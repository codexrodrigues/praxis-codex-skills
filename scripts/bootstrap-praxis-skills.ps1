[CmdletBinding()]
param(
    [ValidateSet('praxis', 'ergon-migration')]
    [string]$Family = 'praxis',
    [string]$ManifestPath,
    [string]$RepoRoot,
    [string]$SkillsRoot,
    [string]$WorkspaceRoot,
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

if ($WorkspaceRoot -and -not $DryRun) {
    $sourceRepoRoot = if ($RepoRoot) { $RepoRoot } else { Split-Path -Parent $PSScriptRoot }
    $targetWorkspace = [System.IO.Path]::GetFullPath($WorkspaceRoot)
    $targetWorkspaceScripts = Join-Path $targetWorkspace 'scripts\workspace'
    New-Item -ItemType Directory -Force -Path $targetWorkspaceScripts | Out-Null

    $sourceWorkspaceScripts = Join-Path $sourceRepoRoot 'scripts\workspace'
    if (Test-Path -LiteralPath $sourceWorkspaceScripts -PathType Container) {
        foreach ($scriptFile in Get-ChildItem -LiteralPath $sourceWorkspaceScripts -File) {
            Copy-Item -LiteralPath $scriptFile.FullName -Destination (Join-Path $targetWorkspaceScripts $scriptFile.Name) -Force
        }
    }

    foreach ($governanceScript in @('audit-agents-governance.py', 'audit-agents-governance.ps1')) {
        $src = Join-Path (Join-Path $sourceRepoRoot 'scripts') $governanceScript
        if (Test-Path -LiteralPath $src -PathType Leaf) {
            Copy-Item -LiteralPath $src -Destination (Join-Path $targetWorkspaceScripts $governanceScript) -Force
        }
    }

    $sourceSkillsJson = Join-Path $sourceRepoRoot '.agents\skills.json'
    if (Test-Path -LiteralPath $sourceSkillsJson -PathType Leaf) {
        $targetAgentsDir = Join-Path $targetWorkspace '.agents'
        New-Item -ItemType Directory -Force -Path $targetAgentsDir | Out-Null
        Copy-Item -LiteralPath $sourceSkillsJson -Destination (Join-Path $targetAgentsDir 'skills.json') -Force
    }

    $sourceRootAgents = Join-Path $sourceRepoRoot 'docs\platform-governance\workspace-root-AGENTS.md'
    $targetRootAgents = Join-Path $targetWorkspace 'AGENTS.md'
    if ((Test-Path -LiteralPath $sourceRootAgents -PathType Leaf) -and ($Force -or -not (Test-Path -LiteralPath $targetRootAgents -PathType Leaf))) {
        Copy-Item -LiteralPath $sourceRootAgents -Destination $targetRootAgents -Force
    }
}

Write-Host "Codex skills bootstrap complete."
