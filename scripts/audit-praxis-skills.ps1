[CmdletBinding()]
param(
    [ValidateSet('praxis', 'ergon-migration')]
    [string]$Family = 'praxis',
    [string]$ManifestPath,
    [string]$RepoRoot,
    [string]$SkillsRoot,
    [switch]$Json,
    [switch]$FailOnDrift
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'codex-skills-common.ps1')

$resolvedRepoRoot = Resolve-PraxisRepoRoot -RequestedRoot $RepoRoot
$resolvedSkillsRoot = Resolve-CodexSkillsRoot -RequestedRoot $SkillsRoot
$manifestBundle = Read-CodexSkillManifest -RepoRoot $resolvedRepoRoot -Family $Family -ManifestPath $ManifestPath
$manifest = $manifestBundle.Manifest

$results = foreach ($skill in $manifest.skills) {
    $sourceDir = Get-CodexSkillSourcePath -RepoRoot $resolvedRepoRoot -Skill $skill
    $installedDir = Join-Path $resolvedSkillsRoot $skill.name
    $status = 'OK'
    $sourceErrors = @()
    $missingFiles = @()
    $extraFiles = @()
    $differentFiles = @()
    $sourceHash = $null
    $sourceTreeHash = $null
    $installedHash = $null

    if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
        $status = 'SOURCE_MISSING'
        $sourceErrors = @("source path not found: $sourceDir")
    }
    else {
        $sourceErrors = @(Test-CodexSkillStructure -SkillRoot $sourceDir -ExpectedName $skill.name)
        $skillMd = Join-Path $sourceDir 'SKILL.md'
        $sourceHash = Get-CodexSkillContentHash -Path $skillMd
        $sourceTreeHash = Get-CodexSkillTreeHash -Root $sourceDir
        if ($skill.skillMdSha256 -and $sourceHash -ne $skill.skillMdSha256) {
            $status = 'SOURCE_DRIFT'
            $sourceErrors += "SKILL.md hash differs from manifest: $sourceHash"
        }
        if ($skill.treeSha256 -and $sourceTreeHash -ne $skill.treeSha256) {
            $status = 'SOURCE_DRIFT'
            $sourceErrors += "skill tree hash differs from manifest: $sourceTreeHash"
        }
    }

    if ($status -eq 'OK' -and $sourceErrors.Count -gt 0) {
        $status = 'SOURCE_INVALID'
    }

    if (-not (Test-Path -LiteralPath $installedDir -PathType Container)) {
        if ($status -eq 'OK') {
            $status = 'MISSING'
        }
    }
    elseif (Test-Path -LiteralPath $sourceDir -PathType Container) {
        $sourceMap = Get-CodexSkillFileHashMap -Root $sourceDir
        $installedMap = Get-CodexSkillFileHashMap -Root $installedDir
        $missingFiles = @($sourceMap.Keys | Where-Object { $_ -notin $installedMap.Keys } | Sort-Object)
        $extraFiles = @($installedMap.Keys | Where-Object { $_ -notin $sourceMap.Keys } | Sort-Object)
        $sharedFiles = @($sourceMap.Keys | Where-Object { $_ -in $installedMap.Keys })
        $differentFiles = @($sharedFiles | Where-Object { $sourceMap[$_] -ne $installedMap[$_] } | Sort-Object)

        $installedSkillMd = Join-Path $installedDir 'SKILL.md'
        if (Test-Path -LiteralPath $installedSkillMd -PathType Leaf) {
            $installedHash = (Get-FileHash -LiteralPath $installedSkillMd -Algorithm SHA256).Hash
        }

        if ($missingFiles.Count -gt 0 -or $extraFiles.Count -gt 0 -or $differentFiles.Count -gt 0) {
            if ($status -eq 'OK') {
                $status = 'DRIFT'
            }
        }
    }

    [pscustomobject]@{
        Skill = $skill.name
        Family = $manifest.family
        Status = $status
        SourcePath = $sourceDir
        InstalledPath = $installedDir
        ManifestHash = $skill.skillMdSha256
        ManifestTreeHash = $skill.treeSha256
        SourceHash = $sourceHash
        SourceTreeHash = $sourceTreeHash
        InstalledHash = $installedHash
        SourceErrors = $sourceErrors
        MissingFiles = $missingFiles
        ExtraFiles = $extraFiles
        DifferentFiles = $differentFiles
    }
}

$manifestNames = @($manifest.skills | Select-Object -ExpandProperty name)
$otherFamilyNames = @()
foreach ($knownFamily in @('praxis', 'ergon-migration')) {
    if ($knownFamily -eq $Family) {
        continue
    }

    $otherManifestBundle = Read-CodexSkillManifest -RepoRoot $resolvedRepoRoot -Family $knownFamily
    $otherFamilyNames += @($otherManifestBundle.Manifest.skills | Select-Object -ExpandProperty name)
}
$otherFamilyNames = @($otherFamilyNames | Sort-Object -Unique)

$installedOnly = @()
if (Test-Path -LiteralPath $resolvedSkillsRoot) {
    $installedOnly = @(
        Get-ChildItem -LiteralPath $resolvedSkillsRoot -Directory |
            Where-Object { $_.Name -notin $manifestNames } |
            Select-Object -ExpandProperty Name |
            Sort-Object
    )
}

$sourceRoot = Join-Path $resolvedRepoRoot 'codex-skills'
$sourceDirs = @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Where-Object { $_.Name -ne '__pycache__' } | Select-Object -ExpandProperty Name)
$sourceInOtherFamilyManifest = @($sourceDirs | Where-Object { $_ -notin $manifestNames -and $_ -in $otherFamilyNames } | Sort-Object)
$sourceNotInManifest = @($sourceDirs | Where-Object { $_ -notin $manifestNames -and $_ -notin $otherFamilyNames } | Sort-Object)

$report = [pscustomobject]@{
    Family = $manifest.family
    ManifestPath = $manifestBundle.Path
    SourceRoot = $sourceRoot
    SkillsRoot = $resolvedSkillsRoot
    Summary = [pscustomobject]@{
        TotalManifestSkills = $results.Count
        Ok = @($results | Where-Object Status -eq 'OK').Count
        Drift = @($results | Where-Object Status -eq 'DRIFT').Count
        Missing = @($results | Where-Object Status -eq 'MISSING').Count
        SourceInvalid = @($results | Where-Object { $_.Status -like 'SOURCE_*' }).Count
        InstalledOnly = $installedOnly.Count
        SourceNotInManifest = $sourceNotInManifest.Count
        SourceInOtherFamilyManifest = $sourceInOtherFamilyManifest.Count
    }
    Results = $results
    InstalledOnly = $installedOnly
    SourceNotInManifest = $sourceNotInManifest
    SourceInOtherFamilyManifest = $sourceInOtherFamilyManifest
}

$blockingProblemCount =
    $report.Summary.Drift +
    $report.Summary.Missing +
    $report.Summary.SourceInvalid +
    $report.Summary.SourceNotInManifest

if ($Json) {
    $report | ConvertTo-Json -Depth 8
}
else {
    Write-Host "Codex skills audit"
    Write-Host "Family: $($report.Family)"
    Write-Host "Manifest: $($report.ManifestPath)"
    Write-Host "Source: $($report.SourceRoot)"
    Write-Host "Destination: $($report.SkillsRoot)"
    Write-Host ""
    Write-Host ("Summary: OK={0} DRIFT={1} MISSING={2} SOURCE_INVALID={3} INSTALLED_ONLY={4} SOURCE_NOT_IN_MANIFEST={5} SOURCE_IN_OTHER_FAMILY_MANIFEST={6}" -f $report.Summary.Ok, $report.Summary.Drift, $report.Summary.Missing, $report.Summary.SourceInvalid, $report.Summary.InstalledOnly, $report.Summary.SourceNotInManifest, $report.Summary.SourceInOtherFamilyManifest)

    foreach ($item in $results) {
        Write-Host ""
        Write-Host ("[{0}] {1}" -f $item.Status, $item.Skill)

        if ($item.SourceErrors.Count -gt 0) {
            Write-Host ("  source errors: {0}" -f ($item.SourceErrors -join '; '))
        }
        if ($item.MissingFiles.Count -gt 0) {
            Write-Host ("  missing: {0}" -f ($item.MissingFiles -join ', '))
        }
        if ($item.ExtraFiles.Count -gt 0) {
            Write-Host ("  extra: {0}" -f ($item.ExtraFiles -join ', '))
        }
        if ($item.DifferentFiles.Count -gt 0) {
            Write-Host ("  different: {0}" -f ($item.DifferentFiles -join ', '))
        }
    }

    if ($installedOnly.Count -gt 0) {
        Write-Host ""
        Write-Host ("Installed-only directories outside family manifest: {0}" -f ($installedOnly -join ', '))
    }

    if ($sourceNotInManifest.Count -gt 0) {
        Write-Host ""
        Write-Host ("Source directories outside selected manifest: {0}" -f ($sourceNotInManifest -join ', '))
    }

    if ($sourceInOtherFamilyManifest.Count -gt 0) {
        Write-Host ""
        Write-Host ("Source directories tracked by another family manifest: {0}" -f ($sourceInOtherFamilyManifest -join ', '))
    }
}

if ($FailOnDrift -and $blockingProblemCount -gt 0) {
    throw ("Codex skills audit is not clean for family '{0}': DRIFT={1} MISSING={2} SOURCE_INVALID={3} SOURCE_NOT_IN_MANIFEST={4}." -f $report.Family, $report.Summary.Drift, $report.Summary.Missing, $report.Summary.SourceInvalid, $report.Summary.SourceNotInManifest)
}

