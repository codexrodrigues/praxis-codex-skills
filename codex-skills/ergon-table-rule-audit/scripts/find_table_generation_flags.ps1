param(
  [Parameter(Mandatory = $true)]
  [string]$TableName,

  [string]$DocsRoot = 'docs-legado\v7x'
)

$ErrorActionPreference = 'Stop'

$table = $TableName.Trim().ToUpperInvariant()
if ($table -notmatch '^[A-Z0-9_$#]+$') {
  throw "Invalid Oracle table name: $TableName"
}

$apsDir = Join-Path $DocsRoot 'aps'
if (!(Test-Path -LiteralPath $apsDir)) {
  throw "APS directory not found: $apsDir"
}

$candidates = Get-ChildItem -LiteralPath $apsDir -File -Filter '*.tab' |
  Where-Object {
    $_.BaseName.ToUpperInvariant() -eq $table -or
    $_.BaseName.ToUpperInvariant().TrimEnd('_') -eq $table.TrimEnd('_')
  }

if (!$candidates) {
  Write-Output "No .tab file found for $table under $apsDir"
  exit 0
}

foreach ($file in $candidates) {
  Write-Output "==== $($file.FullName) ===="
  $lines = Get-Content -LiteralPath $file.FullName
  $start = $null
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'ERG_GERA_OBJETOS_TABELA\s*\(') {
      $start = [Math]::Max(0, $i - 4)
      break
    }
  }
  if ($null -eq $start) {
    Write-Output "No ERG_GERA_OBJETOS_TABELA block found."
    continue
  }

  $end = [Math]::Min($lines.Count - 1, $start + 35)
  for ($j = $start; $j -le $end; $j++) {
    if ($lines[$j] -match '^\s*/\s*$' -and $j -gt $start + 5) {
      break
    }
    '{0,5}: {1}' -f ($j + 1), $lines[$j]
  }
}
