[CmdletBinding()]
param(
    [string]$Repository = 'codexrodrigues/praxis-codex-skills',
    [string]$DraftRoot = 'docs/issue-drafts/skill-reviews',
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI (gh) not found. Install gh or create the issues manually from docs/issue-drafts/skill-reviews.'
}

Get-ChildItem -LiteralPath $DraftRoot -Filter '*.md' | Sort-Object Name | ForEach-Object {
    $content = Get-Content -LiteralPath $_.FullName -Raw
    $title = (($content -split "`n") | Where-Object { $_ -match '^# ' } | Select-Object -First 1) -replace '^\#\s+', ''
    if (-not $title) {
        throw "Draft has no H1 title: $($_.FullName)"
    }

    if ($DryRun) {
        Write-Host "DRY-RUN issue: $title"
        return
    }

    $tmp = New-TemporaryFile
    try {
        Set-Content -LiteralPath $tmp -Value $content -Encoding UTF8
        gh issue create --repo $Repository --title $title --body-file $tmp
    }
    finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
}
