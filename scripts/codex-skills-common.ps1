Set-StrictMode -Version Latest

function Resolve-PraxisRepoRoot {
    param([string]$RequestedRoot)

    if ($RequestedRoot -and $RequestedRoot.Trim()) {
        return (Resolve-Path -LiteralPath $RequestedRoot).Path
    }

    return (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
}

function Resolve-CodexSkillsRoot {
    param([string]$RequestedRoot)

    if ($RequestedRoot -and $RequestedRoot.Trim()) {
        return $RequestedRoot
    }

    if ($env:CODEX_HOME -and $env:CODEX_HOME.Trim()) {
        return [System.IO.Path]::Combine($env:CODEX_HOME, 'skills')
    }

    $home = [Environment]::GetFolderPath('UserProfile')
    return [System.IO.Path]::Combine($home, '.codex', 'skills')
}

function Resolve-CodexSkillManifestPath {
    param(
        [string]$RepoRoot,
        [string]$Family,
        [string]$ManifestPath
    )

    if ($ManifestPath -and $ManifestPath.Trim()) {
        return (Resolve-Path -LiteralPath $ManifestPath).Path
    }

    $manifestName = switch ($Family) {
        'praxis' { 'praxis-skills.manifest.json' }
        'ergon-migration' { 'ergon-migration-skills.manifest.json' }
        default { throw "Unsupported skill family: $Family" }
    }

    return (Resolve-Path -LiteralPath (Join-Path (Join-Path $RepoRoot 'codex-skills') $manifestName)).Path
}

function Read-CodexSkillManifest {
    param(
        [string]$RepoRoot,
        [string]$Family,
        [string]$ManifestPath
    )

    $resolvedManifest = Resolve-CodexSkillManifestPath -RepoRoot $RepoRoot -Family $Family -ManifestPath $ManifestPath
    $manifest = Get-Content -LiteralPath $resolvedManifest -Raw | ConvertFrom-Json

    if ($manifest.family -ne $Family) {
        throw "Manifest family '$($manifest.family)' does not match requested family '$Family': $resolvedManifest"
    }

    $names = @($manifest.skills | ForEach-Object { $_.name })
    $duplicates = @($names | Group-Object | Where-Object { $_.Count -gt 1 } | Select-Object -ExpandProperty Name)
    if ($duplicates.Count -gt 0) {
        throw "Duplicate skill names in manifest ${resolvedManifest}: $($duplicates -join ', ')"
    }

    foreach ($skill in $manifest.skills) {
        if (-not $skill.name -or -not $skill.name.Trim()) {
            throw "Manifest contains a skill without name: $resolvedManifest"
        }
        if (-not $skill.sourcePath -or -not $skill.sourcePath.Trim()) {
            throw "Manifest skill '$($skill.name)' has no sourcePath: $resolvedManifest"
        }
        if (-not $skill.version -or -not $skill.version.Trim()) {
            throw "Manifest skill '$($skill.name)' has no version: $resolvedManifest"
        }
        if (-not $skill.treeSha256 -or -not $skill.treeSha256.Trim()) {
            throw "Manifest skill '$($skill.name)' has no treeSha256: $resolvedManifest"
        }

        $dependencies = @($skill.dependencies)
        if ($manifest.family -eq 'praxis') {
            $ergonDependencies = @($dependencies | Where-Object { $_ -like 'ergon-*' })
            if ($ergonDependencies.Count -gt 0) {
                throw "Praxis skill '$($skill.name)' cannot depend on Ergon migration skills: $($ergonDependencies -join ', ')"
            }
        }

        $unknownDependencies = @($dependencies | Where-Object { $_ -notin $names -and $_ -notlike 'praxis-*' -and $_ -notlike 'ergon-*' })
        if ($unknownDependencies.Count -gt 0) {
            throw "Skill '$($skill.name)' has unknown dependency naming: $($unknownDependencies -join ', ')"
        }
    }

    return [pscustomobject]@{
        Path = $resolvedManifest
        Manifest = $manifest
    }
}

function Get-CodexSkillSourcePath {
    param(
        [string]$RepoRoot,
        [object]$Skill
    )

    return Join-Path $RepoRoot $Skill.sourcePath
}

function Get-CodexSkillFileHashMap {
    param([string]$Root)

    $map = @{}

    if (-not (Test-Path -LiteralPath $Root)) {
        return $map
    }

    Get-ChildItem -LiteralPath $Root -Recurse -File | Where-Object {
        $_.Name -ne '.codex-skill-install.json'
    } | ForEach-Object {
        $relative = $_.FullName.Substring($Root.Length).TrimStart('\')
        $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
        $map[$relative] = $hash
    }

    return $map
}

function Get-CodexSkillTreeHash {
    param([string]$Root)

    $map = Get-CodexSkillFileHashMap -Root $Root
    $lines = @($map.Keys | Sort-Object | ForEach-Object { "$($map[$_])  $_" })
    $payload = [string]::Join("`n", $lines)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [System.BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-', '')
    }
    finally {
        $sha.Dispose()
    }
}

function Test-CodexSkillStructure {
    param(
        [string]$SkillRoot,
        [string]$ExpectedName
    )

    $errors = New-Object System.Collections.Generic.List[string]
    $skillMd = Join-Path $SkillRoot 'SKILL.md'

    if (-not (Test-Path -LiteralPath $skillMd -PathType Leaf)) {
        $errors.Add('missing SKILL.md')
        return $errors
    }

    $head = Get-Content -LiteralPath $skillMd -TotalCount 20
    if ($head.Count -lt 3 -or $head[0] -ne '---') {
        $errors.Add('SKILL.md missing YAML frontmatter start')
        return $errors
    }

    $endIndex = -1
    for ($i = 1; $i -lt $head.Count; $i++) {
        if ($head[$i] -eq '---') {
            $endIndex = $i
            break
        }
    }

    if ($endIndex -lt 0) {
        $errors.Add('SKILL.md missing YAML frontmatter end')
        return $errors
    }

    $frontmatter = $head[1..($endIndex - 1)]
    $nameLine = $frontmatter | Where-Object { $_ -match '^name:\s*(.+)\s*$' } | Select-Object -First 1
    $descriptionLine = $frontmatter | Where-Object { $_ -match '^description:\s*(.+)\s*$' } | Select-Object -First 1

    if (-not $nameLine) {
        $errors.Add('SKILL.md frontmatter missing name')
    }
    else {
        $actualName = ($nameLine -replace '^name:\s*', '').Trim().Trim('"').Trim("'")
        if ($actualName -ne $ExpectedName) {
            $errors.Add("SKILL.md name '$actualName' does not match manifest name '$ExpectedName'")
        }
    }

    if (-not $descriptionLine) {
        $errors.Add('SKILL.md frontmatter missing description')
    }

    return $errors
}

function New-CodexSkillInstallMetadata {
    param(
        [object]$Manifest,
        [object]$Skill,
        [string]$ManifestPath,
        [string]$SourceHash
    )

    return [pscustomobject]@{
        managedBy = 'praxis-plataform'
        family = $Manifest.family
        manifestVersion = $Manifest.version
        manifestPath = $ManifestPath
        skill = $Skill.name
        skillVersion = $Skill.version
        sourcePath = $Skill.sourcePath
        sourceHash = $SourceHash
        installedAt = (Get-Date).ToString('o')
    }
}
