param(
  [Parameter(Mandatory = $true)]
  [string]$TableName,

  [string]$Owner = 'ERGON',

  [Parameter(Mandatory = $true)]
  [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

$skillDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$templatePath = Join-Path $skillDir 'scripts\table_rule_audit.sql.tpl'

$table = $TableName.Trim().ToUpperInvariant()
$ownerUpper = $Owner.Trim().ToUpperInvariant()
$tableBase = $table.TrimEnd('_')

if ($table -notmatch '^[A-Z0-9_$#]+$') {
  throw "Invalid Oracle table name: $TableName"
}
if ($ownerUpper -notmatch '^[A-Z0-9_$#]+$') {
  throw "Invalid Oracle owner name: $Owner"
}

$text = Get-Content -LiteralPath $templatePath -Raw
$text = $text.Replace('__TABLE_NAME__', $table).Replace('__TABLE_BASE__', $tableBase).Replace('__OWNER__', $ownerUpper)

$outFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$outDir = Split-Path -Parent $outFull
if ($outDir -and !(Test-Path -LiteralPath $outDir)) {
  New-Item -ItemType Directory -Path $outDir | Out-Null
}

Set-Content -LiteralPath $outFull -Value $text -Encoding UTF8
Write-Output $outFull
