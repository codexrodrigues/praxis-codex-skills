param(
  [Parameter(Mandatory = $true)]
  [string]$Screen,

  [string]$OutputDir = $(Join-Path "docs\migracao" (Join-Path $Screen "oracle-results")),

  [string[]]$Patterns = @(),

  [string]$Title,

  [string]$MainView,

  [string]$Connection = $(if ($env:ERGON_HADES_CONN) { $env:ERGON_HADES_CONN } else { $env:ERGON_ORACLE_CONNECTION }),

  [string]$SqlclPath = $(if ($env:ERGON_SQLCL) { $env:ERGON_SQLCL } else { ".\tools\sqlcl\bin\sql.exe" }),

  [string]$JavaHome = $env:JAVA_HOME,

  [string]$TextTableLike = "HADADM%",

  [switch]$IncludeXmlMarkers,

  [switch]$IncludeBlobSearch
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $PSCommandPath
$runSql = Join-Path $scriptRoot "run_oracle_query_jdbc.ps1"
$searchText = Join-Path $scriptRoot "search_oracle_text.ps1"
$searchBlob = Join-Path $scriptRoot "search_oracle_blob_text.ps1"

if (-not $Connection) {
  throw "Connection was not provided. Pass -Connection or set ERGON_HADES_CONN."
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$allPatterns = New-Object System.Collections.Generic.List[string]
foreach ($value in @($Screen, $Screen.ToUpperInvariant(), $Title, $MainView)) {
  if (-not [string]::IsNullOrWhiteSpace($value) -and -not $allPatterns.Contains($value)) {
    $allPatterns.Add($value)
  }
}
if ($IncludeXmlMarkers) {
  foreach ($value in @("sqlSelect", "sqlParameters", "<screen", "<page", "<component")) {
    if (-not $allPatterns.Contains($value)) {
      $allPatterns.Add($value)
    }
  }
}
foreach ($value in $Patterns) {
  if (-not [string]::IsNullOrWhiteSpace($value) -and -not $allPatterns.Contains($value)) {
    $allPatterns.Add($value)
  }
}

$registrySql = Join-Path $OutputDir "hades-registry.generated.sql"
@(
  "-- $Screen HADES registry and resource candidate discovery."
  "-- Generated read-only SQL. Do not include credentials in this file."
  ""
  "select *"
  "from hades.transacao"
  "where upper(trans) = upper('$Screen')"
  "   or upper(itemmenu) = upper('$Screen');"
  ""
  "select *"
  "from hades.hadadm00019_transacao"
  "where upper(trans) = upper('$Screen')"
  "   or upper(itemmenu) = upper('$Screen');"
  ""
  "select *"
  "from hades.hadadm00015_transpadaces"
  "where upper(trans) = upper('$Screen');"
  ""
  "select *"
  "from hades.hadadm00023_transpadaces"
  "where upper(trans) = upper('$Screen');"
  ""
  "select padrao_master, padrao, sis, trans, itemmenu, nomenomenu, nometrans, tipo, trans_descr"
  "from hades.hadadm00020_transpadtela"
  "where upper(trans) like upper('%$Screen%')"
  "   or upper(padrao) like upper('%$Screen%')"
  "   or upper(padrao_master) like upper('%$Screen%')"
  "order by sis, trans;"
  ""
  "select owner, table_name, column_name, data_type"
  "from all_tab_columns"
  "where owner = 'HADES'"
  "  and table_name like 'HAD%'"
  "  and data_type in ('CLOB','NCLOB','BLOB','LONG')"
  "order by table_name, column_id;"
  ""
  "select id_arquivos_reg, nome_arquivo, tipo_documento, descr_documento, sis, trans, acesso_ind_trans, ind_armazenamento, data_inclusao"
  "from hades.had_arquivos_regs"
  "where upper(trans) like upper('%$Screen%')"
  "   or upper(nome_arquivo) like upper('%$Screen%')"
  "   or upper(palavras_chave) like upper('%$Screen%')"
  "   or upper(descr_documento) like upper('%$Screen%')"
  "order by data_inclusao desc;"
) | Set-Content -LiteralPath $registrySql -Encoding UTF8

$registryOut = Join-Path $OutputDir "hades-definition-registry.txt"
& $runSql -SqlFile $registrySql -Connection $Connection -SqlclPath $SqlclPath -JavaHome $JavaHome -OutputPath $registryOut -MaxRows 300 | Out-Null

foreach ($pattern in $allPatterns) {
  $safe = ($pattern -replace '[^A-Za-z0-9_.-]', '_')
  if ($safe.Length -gt 80) {
    $safe = $safe.Substring(0, 80)
  }

  $textOut = Join-Path $OutputDir "hades-text-$safe.txt"
  & $searchText -Pattern $pattern -Owner HADES -TableLike $TextTableLike -Connection $Connection -SqlclPath $SqlclPath -JavaHome $JavaHome -OutputPath $textOut | Out-Null

  if ($IncludeBlobSearch) {
    $blobOut = Join-Path $OutputDir "hades-blob-$safe.txt"
    & $searchBlob -Pattern $pattern -Owner HADES -TableLike $TextTableLike -Connection $Connection -SqlclPath $SqlclPath -JavaHome $JavaHome -OutputPath $blobOut | Out-Null
  }
}

Write-Output "HADES screen definition discovery complete: $OutputDir"
