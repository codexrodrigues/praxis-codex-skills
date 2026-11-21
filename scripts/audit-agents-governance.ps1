[CmdletBinding()]
param(
    [string]$Target = '.',
    [switch]$RootAgents,
    [int]$MaxRootBytes = 16384,
    [int]$MaxLocalBytes = 18432,
    [int]$MaxSkillsChars = 34000,
    [switch]$AllowPrivate,
    [switch]$NoNested,
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$mojibakeTokens = @(
    ([char]0x00C3 + [char]0x00A3),
    ([char]0x00C3 + [char]0x00A7),
    ([char]0x00C3 + [char]0x00A1),
    ([char]0x00C3 + [char]0x00A9),
    ([char]0x00C3 + [char]0x00AD),
    ([char]0x00C3 + [char]0x00B3),
    ([char]0x00C3 + [char]0x00BA),
    ([char]0x00C3 + [char]0x00B5),
    ([char]0x00C3 + [char]0x00AA),
    ([char]0x00C3 + [char]0x00A2),
    ([char]0x00C3 + [char]0x0083),
    ([char]0x00E2 + [char]0x20AC + [char]0x201D),
    ([char]0x00E2 + [char]0x20AC + [char]0x201C),
    ([char]0xFFFD).ToString()
)

$publicPatterns = @(
    @{ Code = 'legacy-studio-name'; Regex = '(?i)\bpraxis-rules-studio\b' },
    @{ Code = 'neon-branch-or-endpoint-id'; Regex = '\b(?:ep-[a-z0-9-]+\.aws\.neon\.tech|br-[a-z0-9-]+-[a-z0-9]{6,})\b' },
    @{ Code = 'local-machine-path'; Regex = '(?:[A-Za-z]:[/\\](?:Users|Developer)[/\\]|/Users/|/mnt/[a-z]/)' }
)

$resolved = (Resolve-Path -LiteralPath $Target).Path
$ignoredDirs = @('.git', 'node_modules', 'dist', 'target', '.angular', '.m2repo')

if (Test-Path -LiteralPath $resolved -PathType Leaf) {
    [string[]]$files = @($resolved)
    $rootFile = if ($RootAgents) { $resolved } else { $null }
}
else {
    if ($NoNested) {
        $candidate = Join-Path $resolved 'AGENTS.md'
        [string[]]$files = if (Test-Path -LiteralPath $candidate -PathType Leaf) { @($candidate) } else { @() }
    }
    else {
        [string[]]$files = @(Get-ChildItem -LiteralPath $resolved -Filter 'AGENTS.md' -Recurse -File | Where-Object {
            $parts = $_.FullName.Split([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
            -not ($parts | Where-Object { $_ -in $ignoredDirs })
        } | Select-Object -ExpandProperty FullName | Sort-Object)
    }
    $rootFile = if ($RootAgents) { Join-Path $resolved 'AGENTS.md' } else { $null }
}

$findings = New-Object System.Collections.Generic.List[object]

foreach ($file in $files) {
    $bytes = [IO.File]::ReadAllBytes($file)
    $isRoot = ($null -ne $rootFile -and [string]::Equals($file, $rootFile, [System.StringComparison]::OrdinalIgnoreCase))
    $limit = if ($isRoot) { $MaxRootBytes } else { $MaxLocalBytes }

    if ($bytes.Length -gt $limit) {
        $findings.Add([PSCustomObject]@{
            file = $file
            code = 'size-budget-exceeded'
            detail = "$($bytes.Length) bytes > limit $limit bytes"
        })
    }

    $utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)
    try {
        $text = $utf8Strict.GetString($bytes)
    }
    catch {
        $findings.Add([PSCustomObject]@{
            file = $file
            code = 'invalid-utf8'
            detail = $_.Exception.Message
        })
        continue
    }

    $lines = $text -split "`r?`n"
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $lineNum = $i + 1
        $line = $lines[$i]

        foreach ($tok in $mojibakeTokens) {
            if ($line.Contains($tok)) {
                $findings.Add([PSCustomObject]@{
                    file = $file
                    code = 'utf8-mojibake'
                    detail = "line $lineNum contains mojibake token"
                })
                break
            }
        }

        if (-not $AllowPrivate) {
            foreach ($p in $publicPatterns) {
                if ($line -match $p.Regex) {
                    $findings.Add([PSCustomObject]@{
                        file = $file
                        code = $p.Code
                        detail = "line $lineNum matches $($p.Code)"
                    })
                }
            }
        }
    }
}

if (Test-Path -LiteralPath $resolved -PathType Container) {
    $skillsJsonPath = Join-Path $resolved '.agents\skills.json'
    if (Test-Path -LiteralPath $skillsJsonPath -PathType Leaf) {
        try {
            $skillsCfg = Get-Content -LiteralPath $skillsJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $totalChars = 0
            foreach ($entry in @($skillsCfg.entries)) {
                if (-not $entry.path) { continue }
                $dotCandidate = Join-Path (Join-Path $resolved '.agents') $entry.path
                $baseDir = if (Test-Path -LiteralPath $dotCandidate -PathType Container) { $dotCandidate } else { Join-Path $resolved $entry.path }
                if (-not (Test-Path -LiteralPath $baseDir -PathType Container)) { continue }

                [string[]]$names = if ($null -ne $entry.include_only) {
                    @($entry.include_only | ForEach-Object { [string]$_ })
                } else {
                    @(Get-ChildItem -LiteralPath $baseDir -Directory | Select-Object -ExpandProperty Name | Sort-Object)
                }

                foreach ($name in $names) {
                    $skillMd = Join-Path (Join-Path $baseDir $name) 'SKILL.md'
                    if (-not (Test-Path -LiteralPath $skillMd -PathType Leaf)) { continue }
                    $rawText = Get-Content -LiteralPath $skillMd -Raw -Encoding UTF8
                    if ($rawText -match '(?s)\A---\r?\n(.*?)\r?\n---') {
                        $relSkill = $skillMd.Substring($resolved.Length).TrimStart('\', '/').Replace('\', '/')
                        $totalChars += ("- $name ($relSkill): ".Length + $Matches[1].Length)
                    }
                }
            }

            if ($totalChars -gt $MaxSkillsChars) {
                $findings.Add([PSCustomObject]@{
                    file = $skillsJsonPath
                    code = 'skills-budget-exceeded'
                    detail = "$totalChars chars > limit $MaxSkillsChars chars"
                })
            }
        }
        catch {
            $findings.Add([PSCustomObject]@{
                file = $skillsJsonPath
                code = 'invalid-skills-json'
                detail = $_.Exception.Message
            })
        }
    }
}

if ($Json) {
    @{ checked = $files.Count; findings = $findings } | ConvertTo-Json -Depth 4
}
else {
    foreach ($f in $findings) {
        Write-Host "[FAIL] $($f.code) | $($f.file) | $($f.detail)"
    }
    $status = if ($findings.Count -eq 0) { 'PASS' } else { 'FAIL' }
    Write-Host "AGENTS governance audit: $status (files=$($files.Count), findings=$($findings.Count))"
}

if ($findings.Count -gt 0) {
    exit 1
}
