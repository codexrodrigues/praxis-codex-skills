param(
  [Parameter(Mandatory = $true)]
  [string]$TableName,

  [string]$Owner = 'ERGON',

  [int]$MaxDepth = 3,

  [Parameter(Mandatory = $true)]
  [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

$skillDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$templatePath = Join-Path $skillDir 'scripts\table_nested_dependency.sql.tpl'

$table = $TableName.Trim().ToUpperInvariant()
$ownerUpper = $Owner.Trim().ToUpperInvariant()
$tableBase = $table.TrimEnd('_')

if ($table -notmatch '^[A-Z0-9_$#]+$') {
  throw "Invalid Oracle table name: $TableName"
}
if ($ownerUpper -notmatch '^[A-Z0-9_$#]+$') {
  throw "Invalid Oracle owner name: $Owner"
}
if ($MaxDepth -lt 1 -or $MaxDepth -gt 8) {
  throw "MaxDepth must be between 1 and 8. Use small values to avoid noisy legacy dependency graphs."
}

$text = Get-Content -LiteralPath $templatePath -Raw
$text = $text.
  Replace('__TABLE_NAME__', $table).
  Replace('__TABLE_BASE__', $tableBase).
  Replace('__OWNER__', $ownerUpper).
  Replace('__MAX_DEPTH__', [string]$MaxDepth)

$outFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$outDir = Split-Path -Parent $outFull
if ($outDir -and !(Test-Path -LiteralPath $outDir)) {
  New-Item -ItemType Directory -Path $outDir | Out-Null
}

Set-Content -LiteralPath $outFull -Value $text -Encoding UTF8
Write-Output $outFull
