param(
  [Parameter(Mandatory = $true)]
  [string]$InputPath,

  [Parameter(Mandatory = $true)]
  [string]$OutputPath,

  [string]$TableName,

  [int]$MaxEdges = 80,

  [int]$MaxCallRows = 80
)

$ErrorActionPreference = 'Stop'

if (!(Test-Path -LiteralPath $InputPath)) {
  throw "Input file not found: $InputPath"
}

function Convert-ToRows {
  param(
    [string[]]$Lines,
    [string]$HeaderText
  )

  $rows = @()
  for ($i = 0; $i -lt $Lines.Count; $i++) {
    if ($Lines[$i] -eq $HeaderText) {
      $headers = $HeaderText.Split('|')
      for ($j = $i + 1; $j -lt $Lines.Count; $j++) {
        $line = $Lines[$j]
        if ($line -match '^Rows shown:' -or $line -match '^== Statement ' -or [string]::IsNullOrWhiteSpace($line)) {
          break
        }
        $parts = $line.Split([char[]]'|', $headers.Count)
        if ($parts.Count -lt $headers.Count) {
          continue
        }
        $obj = [ordered]@{}
        for ($k = 0; $k -lt $headers.Count; $k++) {
          $obj[$headers[$k]] = $parts[$k]
        }
        $rows += [pscustomobject]$obj
      }
    }
  }
  return $rows
}

function Escape-Md {
  param([string]$Value)
  if ($null -eq $Value) { return '' }
  return ($Value -replace '\|', '\|' -replace "`r|`n", ' ').Trim()
}

function Get-NodeId {
  param([string]$Label)
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($Label)
  $hash = [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA1Managed).ComputeHash($bytes)).Replace('-', '').Substring(0, 10)
  return "N$hash"
}

function Get-Category {
  param(
    [string]$Owner,
    [string]$Name,
    [string]$Type
  )

  $n = "$Owner.$Name.$Type".ToUpperInvariant()
  if ($n -match 'TRIGGER|T_B_|T_A_|AUDIT|AUDHD') { return 'orquestracao/auditoria' }
  if ($n -match 'PCK_EXEC_EP_CERG|HAD_CAD_SPROC|HAD_CAD_MULT_EPS') { return 'despacho cliente' }
  if ($n -match 'C_ERGON|POA_|EP__|TPOA_') { return 'cliente' }
  if ($n -match 'FLAG_PACK|SESS|USUARIO|EMPRESA') { return 'contexto sessao' }
  if ($n -match 'PEND|WORKFLOW') { return 'pendencia/workflow' }
  if ($n -match 'PUBLIC|PUBL|DOCUMENT') { return 'publicacao/documento' }
  if ($n -match 'ERRO|VALID|CONSIST') { return 'validacao/erro' }
  if ($Type -match 'TABLE|VIEW') { return 'dados' }
  if ($n -match 'PCK_|PACK_') { return 'package/utilitaria' }
  return 'indefinida'
}

$lines = Get-Content -LiteralPath $InputPath

$seedRows = @(Convert-ToRows -Lines $lines -HeaderText 'SEED_ROLE|OWNER|OBJECT_TYPE|OBJECT_NAME|STATUS')
$depRows = @(Convert-ToRows -Lines $lines -HeaderText 'DEP_LEVEL|ROOT_OWNER|ROOT_NAME|ROOT_TYPE|SOURCE_OWNER|SOURCE_NAME|SOURCE_TYPE|TARGET_OWNER|TARGET_NAME|TARGET_TYPE|DEPENDENCY_TYPE|SOURCE_PATH')
$callRows = @(Convert-ToRows -Lines $lines -HeaderText 'OWNER|NAME|TYPE|LINE|CALL_CLASS|TEXT')
$dynamicRows = @(Convert-ToRows -Lines $lines -HeaderText 'SOURCE_TABLE|SPROC|EP|ORDEM|EXEC|EXEC_MULT_EPS|EXECUTION_STATUS|SINTAXE')
if ($dynamicRows.Count -eq 0) {
  $dynamicRows = @(Convert-ToRows -Lines $lines -HeaderText 'SOURCE_TABLE|SPROC|EP|ORDEM|EXEC|EXEC_MULT_EPS|SINTAXE')
}

$titleTable = if ($TableName) { $TableName.Trim().ToUpperInvariant() } else { 'tabela alvo' }
$out = New-Object System.Collections.Generic.List[string]

$out.Add("# Mapa de Dependencias Aninhadas - $titleTable")
$out.Add("")
$out.Add('Este arquivo resume dependencias estruturais de `ALL_DEPENDENCIES`, chamadas candidatas em `ALL_SOURCE` e sintaxes dinamicas de HADES. Use o `.out.txt` bruto como evidencia completa.')
$out.Add("")
$out.Add("## Resumo")
$out.Add("")
$out.Add("| Item | Total |")
$out.Add("| --- | ---: |")
$out.Add("| Objetos semente | $($seedRows.Count) |")
$out.Add("| Arestas estruturais | $($depRows.Count) |")
$out.Add("| Linhas de chamada candidatas | $($callRows.Count) |")
$out.Add("| Sintaxes dinamicas HADES | $($dynamicRows.Count) |")
$out.Add("")

$out.Add("## Objetos Semente")
$out.Add("")
$out.Add("| Papel | Objeto | Tipo | Status |")
$out.Add("| --- | --- | --- | --- |")
foreach ($row in $seedRows | Select-Object -First 80) {
  $objName = Escape-Md "$($row.OWNER).$($row.OBJECT_NAME)"
  $out.Add(('| {0} | `{1}` | {2} | {3} |' -f (Escape-Md $row.SEED_ROLE), $objName, (Escape-Md $row.OBJECT_TYPE), (Escape-Md $row.STATUS)))
}
if ($seedRows.Count -gt 80) {
  $out.Add("| ... | ... | ... | $($seedRows.Count - 80) objetos omitidos |")
}
$out.Add("")

$out.Add("## Diagrama")
$out.Add("")
$out.Add('```mermaid')
$out.Add("flowchart TD")

$edgeRows = @($depRows |
  Where-Object { $_.SOURCE_OWNER -and $_.TARGET_OWNER } |
  Select-Object -First $MaxEdges)

$nodeLabels = @{}
foreach ($row in $edgeRows) {
  $sourceLabel = "$($row.SOURCE_OWNER).$($row.SOURCE_NAME)`n($($row.SOURCE_TYPE))"
  $targetLabel = "$($row.TARGET_OWNER).$($row.TARGET_NAME)`n($($row.TARGET_TYPE))"
  $sourceId = Get-NodeId $sourceLabel
  $targetId = Get-NodeId $targetLabel
  $nodeLabels[$sourceId] = $sourceLabel
  $nodeLabels[$targetId] = $targetLabel
  $safeSourceLabel = $sourceLabel.Replace('"', "'")
  $safeTargetLabel = $targetLabel.Replace('"', "'")
  $out.Add(('  {0}["{1}"] --> {2}["{3}"]' -f $sourceId, $safeSourceLabel, $targetId, $safeTargetLabel))
}
if ($edgeRows.Count -eq 0) {
  $out.Add('  A["Nenhuma dependencia estrutural encontrada no limite configurado"]')
}
$out.Add('```')
if ($depRows.Count -gt $MaxEdges) {
  $out.Add("")
  $out.Add(('> Diagrama limitado a {0} arestas de {1}. Use a tabela abaixo e o `.out.txt` para o grafo completo.' -f $MaxEdges, $depRows.Count))
}
$out.Add("")

$out.Add("## Dependencias Estruturais")
$out.Add("")
$out.Add("| Nivel | Origem | Destino | Tipo destino | Categoria | Evidencia |")
$out.Add("| ---: | --- | --- | --- | --- | --- |")
foreach ($row in $depRows | Select-Object -First 160) {
  $category = Get-Category -Owner $row.TARGET_OWNER -Name $row.TARGET_NAME -Type $row.TARGET_TYPE
  $source = "$($row.SOURCE_OWNER).$($row.SOURCE_NAME)"
  $target = "$($row.TARGET_OWNER).$($row.TARGET_NAME)"
  $out.Add(('| {0} | `{1}` | `{2}` | {3} | {4} | ALL_DEPENDENCIES {5} |' -f (Escape-Md $row.DEP_LEVEL), (Escape-Md $source), (Escape-Md $target), (Escape-Md $row.TARGET_TYPE), (Escape-Md $category), (Escape-Md $row.DEPENDENCY_TYPE)))
}
if ($depRows.Count -gt 160) {
  $out.Add("| ... | ... | ... | ... | ... | $($depRows.Count - 160) dependencias omitidas |")
}
$out.Add("")

$out.Add("## Chamadas Candidatas em Fonte")
$out.Add("")
$out.Add("| Objeto | Linha | Classe | Trecho |")
$out.Add("| --- | ---: | --- | --- |")
foreach ($row in $callRows | Select-Object -First $MaxCallRows) {
  $obj = "$($row.OWNER).$($row.NAME) ($($row.TYPE))"
  $text = Escape-Md $row.TEXT
  if ($text.Length -gt 180) { $text = $text.Substring(0, 180) + '...' }
  $out.Add(('| `{0}` | {1} | {2} | `{3}` |' -f (Escape-Md $obj), (Escape-Md $row.LINE), (Escape-Md $row.CALL_CLASS), $text))
}
if ($callRows.Count -gt $MaxCallRows) {
  $out.Add("| ... | ... | ... | $($callRows.Count - $MaxCallRows) linhas omitidas |")
}
$out.Add("")

$out.Add("## Dependencias Dinamicas / Incertas")
$out.Add("")
if ($dynamicRows.Count -eq 0) {
  $out.Add("Nenhuma sintaxe dinamica HADES foi retornada para a tabela alvo.")
} else {
  $out.Add("| Origem | SPROC | EP | Ordem | EXEC | Status execucao | Sintaxe |")
  $out.Add("| --- | --- | --- | ---: | --- | --- | --- |")
  foreach ($row in $dynamicRows | Select-Object -First 80) {
    $syntax = Escape-Md $row.SINTAXE
    if ($syntax.Length -gt 180) { $syntax = $syntax.Substring(0, 180) + '...' }
    $status = if ($row.PSObject.Properties.Name -contains 'EXECUTION_STATUS') { $row.EXECUTION_STATUS } else { 'UNCLASSIFIED_LEGACY_OUTPUT' }
    $out.Add(('| {0} | `{1}` | `{2}` | {3} | {4} | {5} | `{6}` |' -f (Escape-Md $row.SOURCE_TABLE), (Escape-Md $row.SPROC), (Escape-Md $row.EP), (Escape-Md $row.ORDEM), (Escape-Md $row.EXEC), (Escape-Md $status), $syntax))
  }
}
$out.Add("")

$out.Add("## Como Usar na Migracao Java")
$out.Add("")
$out.Add("- Trate o grafo como mapa de impacto, nao como prova unica de regra de negocio.")
$out.Add('- Use `ALL_DEPENDENCIES` para saber quais objetos podem ser afetados ao chamar/reimplementar uma regra.')
$out.Add('- Use `ALL_SOURCE` para confirmar ordem, parametros, mensagens e chamadas dinamicas.')
$out.Add("- Quando houver `EXECUTE IMMEDIATE` ou sintaxe HADES, use o status de execucao para separar alvo ativo de candidato inativo/dinamico.")
$out.Add("- Antes de reimplementar em Java, cada dependencia ativa deve ser classificada como: reimplementar, manter DB-backed, preservar hook, auditoria/publicacao, ou fora do escopo.")

$outFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$outDir = Split-Path -Parent $outFull
if ($outDir -and !(Test-Path -LiteralPath $outDir)) {
  New-Item -ItemType Directory -Path $outDir | Out-Null
}

Set-Content -LiteralPath $outFull -Value $out -Encoding UTF8
Write-Output $outFull
