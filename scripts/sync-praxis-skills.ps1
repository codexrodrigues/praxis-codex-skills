[CmdletBinding()]
param(
    [ValidateSet('praxis', 'ergon-migration')]
    [string]$Family = 'praxis',
    [string]$ManifestPath,
    [string]$RepoRoot,
    [string]$SkillsRoot,
    [switch]$DryRun,
    [switch]$Force,
    [Alias('DeleteExtraneous')]
    [switch]$DeleteExtraneousWithinManifest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'codex-skills-common.ps1')

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        if ($DryRun) {
            Write-Host "DRY-RUN create directory: $Path"
            return
        }
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Copy-SkillDirectory {
    param(
        [string]$SourceDir,
        [string]$DestinationDir
    )

    Ensure-Directory -Path $DestinationDir
    if ($DryRun) {
        Write-Host "DRY-RUN copy: $SourceDir -> $DestinationDir"
        return
    }

    Copy-Item -Path (Join-Path $SourceDir '*') -Destination $DestinationDir -Recurse -Force -Container
}

function Remove-ExtraManifestFiles {
    param(
        [string]$SourceDir,
        [string]$DestinationDir
    )

    $sourceMap = Get-CodexSkillFileHashMap -Root $SourceDir
    $destinationMap = Get-CodexSkillFileHashMap -Root $DestinationDir
    $extraFiles = @($destinationMap.Keys | Where-Object { $_ -notin $sourceMap.Keys } | Sort-Object)

    foreach ($extraFile in $extraFiles) {
        $target = Join-Path $DestinationDir $extraFile
        $resolvedDestination = (Resolve-Path -LiteralPath $DestinationDir).Path
        $resolvedTarget = (Resolve-Path -LiteralPath $target).Path
        if (-not $resolvedTarget.StartsWith($resolvedDestination, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove path outside skill destination: $resolvedTarget"
        }

        if ($DryRun) {
            Write-Host "DRY-RUN remove extra file within managed skill: $resolvedTarget"
        }
        else {
            Remove-Item -LiteralPath $resolvedTarget -Force
        }
    }
}

$resolvedRepoRoot = Resolve-PraxisRepoRoot -RequestedRoot $RepoRoot
$resolvedSkillsRoot = Resolve-CodexSkillsRoot -RequestedRoot $SkillsRoot
$manifestBundle = Read-CodexSkillManifest -RepoRoot $resolvedRepoRoot -Family $Family -ManifestPath $ManifestPath
$manifest = $manifestBundle.Manifest

Ensure-Directory -Path $resolvedSkillsRoot

$conflicts = New-Object System.Collections.Generic.List[string]

foreach ($skill in $manifest.skills) {
    $sourceDir = Get-CodexSkillSourcePath -RepoRoot $resolvedRepoRoot -Skill $skill
    $destinationDir = Join-Path $resolvedSkillsRoot $skill.name

    if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
        throw "Manifest source path not found for $($skill.name): $sourceDir"
    }

    $structureErrors = @(Test-CodexSkillStructure -SkillRoot $sourceDir -ExpectedName $skill.name)
    if ($structureErrors.Count -gt 0) {
        throw "Invalid source skill $($skill.name): $($structureErrors -join '; ')"
    }

    $sourceSkillHash = Get-CodexSkillContentHash -Path (Join-Path $sourceDir 'SKILL.md')
    if ($skill.skillMdSha256 -and $sourceSkillHash -ne $skill.skillMdSha256) {
        throw "Source hash drift for $($skill.name). Manifest=$($skill.skillMdSha256) Actual=$sourceSkillHash"
    }
    $sourceTreeHash = Get-CodexSkillTreeHash -Root $sourceDir
    if ($skill.treeSha256 -and $sourceTreeHash -ne $skill.treeSha256) {
        throw "Source tree hash drift for $($skill.name). Manifest=$($skill.treeSha256) Actual=$sourceTreeHash"
    }

    if (Test-Path -LiteralPath $destinationDir -PathType Container) {
        $sourceMap = Get-CodexSkillFileHashMap -Root $sourceDir
        $destinationMap = Get-CodexSkillFileHashMap -Root $destinationDir
        $differentFiles = @($sourceMap.Keys | Where-Object { $_ -in $destinationMap.Keys -and $sourceMap[$_] -ne $destinationMap[$_] } | Sort-Object)
        $extraFiles = @($destinationMap.Keys | Where-Object { $_ -notin $sourceMap.Keys } | Sort-Object)

        if (($differentFiles.Count -gt 0 -or $extraFiles.Count -gt 0) -and -not $Force) {
            $conflicts.Add("$($skill.name): destination differs; rerun with -Force to overwrite managed files")
            continue
        }
    }

    Copy-SkillDirectory -SourceDir $sourceDir -DestinationDir $destinationDir

    if ($DeleteExtraneousWithinManifest -and (Test-Path -LiteralPath $destinationDir -PathType Container)) {
        Remove-ExtraManifestFiles -SourceDir $sourceDir -DestinationDir $destinationDir
    }

    if (-not $DryRun) {
        $metadata = New-CodexSkillInstallMetadata -Manifest $manifest -Skill $skill -ManifestPath $manifestBundle.Path -SourceHash $sourceTreeHash
        $metadata | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $destinationDir '.codex-skill-install.json') -Encoding UTF8
    }
}

if ($conflicts.Count -gt 0) {
    Write-Host "Codex skills sync blocked by destination drift."
    foreach ($conflict in $conflicts) {
        Write-Host " - $conflict"
    }
    throw "Sync blocked: $($conflicts.Count) conflict(s)."
}

if ($DryRun) {
    Write-Host "Codex skills sync dry-run complete."
}
else {
    Write-Host "Codex skills synced."
}

Write-Host "Family: $($manifest.family)"
Write-Host "Manifest: $($manifestBundle.Path)"
Write-Host "Destination: $resolvedSkillsRoot"

