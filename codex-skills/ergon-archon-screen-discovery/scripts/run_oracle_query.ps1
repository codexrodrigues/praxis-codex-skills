param(
  [Parameter(Mandatory = $true)]
  [string]$SqlFile,

  [Parameter(Mandatory = $false)]
  [string]$Connection = $(if ($env:ERGON_HADES_CONN) { $env:ERGON_HADES_CONN } else { $env:ERGON_ORACLE_CONNECTION }),

  [Parameter(Mandatory = $false)]
  [string]$SqlclPath = $(if ($env:ERGON_SQLCL) { $env:ERGON_SQLCL } else { $env:SQLCL_PATH }),

  [Parameter(Mandatory = $false)]
  [string]$JavaHome = $env:JAVA_HOME,

  [Parameter(Mandatory = $false)]
  [string]$OutputPath
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SqlFile)) {
  throw "SQL file not found: $SqlFile"
}

if (-not $Connection) {
  throw "Connection was not provided. Pass -Connection or set ERGON_HADES_CONN."
}

if (-not $SqlclPath) {
  $cmd = Get-Command sql -ErrorAction SilentlyContinue
  if ($cmd) {
    $SqlclPath = $cmd.Source
  } elseif (Test-Path -LiteralPath ".\tools\sqlcl\bin\sql.exe") {
    $SqlclPath = (Resolve-Path -LiteralPath ".\tools\sqlcl\bin\sql.exe").Path
  } elseif (Test-Path -LiteralPath "D:\Developer\tools\sqlcl\bin\sql.exe") {
    $SqlclPath = "D:\Developer\tools\sqlcl\bin\sql.exe"
  } else {
    throw "SQLcl was not provided. Pass -SqlclPath, set ERGON_SQLCL, keep SQLcl under tools\sqlcl, or add sql to PATH."
  }
}

if (-not $JavaHome) {
  $candidates = @(
    "D:\Developer\tools\JAVA\graalvm-jdk-21.0.2+13.1",
    "D:\Developer\tools\JAVA\jdk-17.0.2"
  )
  $JavaHome = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
  if (-not $JavaHome) {
    throw "Java home was not provided. Pass -JavaHome or set JAVA_HOME."
  }
}

if (-not (Test-Path -LiteralPath $SqlclPath)) {
  throw "SQLcl not found: $SqlclPath"
}

if (-not (Test-Path -LiteralPath $JavaHome)) {
  throw "Java home not found: $JavaHome"
}

$env:JAVA_HOME = $JavaHome
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

if ($OutputPath) {
  & $SqlclPath -S $Connection "@$SqlFile" | Tee-Object -FilePath $OutputPath
} else {
  & $SqlclPath -S $Connection "@$SqlFile"
}
