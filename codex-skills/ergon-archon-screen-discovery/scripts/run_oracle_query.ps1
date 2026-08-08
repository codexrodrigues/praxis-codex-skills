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

$work = Join-Path ([System.IO.Path]::GetTempPath()) ("ergon-sqlcl-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $work | Out-Null

try {
  $stdoutPath = Join-Path $work "stdout.txt"
  $stderrPath = Join-Path $work "stderr.txt"

  # SQLcl can fail with java.io.IOException when its console streams are sent
  # through a PowerShell pipeline under non-interactive Windows execution.
  # Redirect its process streams directly instead of piping through Tee-Object.
  & $SqlclPath -S $Connection "@$SqlFile" 1> $stdoutPath 2> $stderrPath
  $sqlclExitCode = $LASTEXITCODE

  $stdout = if (Test-Path -LiteralPath $stdoutPath) {
    [System.IO.File]::ReadAllText($stdoutPath)
  } else {
    ""
  }
  $stderr = if (Test-Path -LiteralPath $stderrPath) {
    [System.IO.File]::ReadAllText($stderrPath)
  } else {
    ""
  }
  $output = $stdout + $stderr

  if ($OutputPath) {
    $outputDirectory = Split-Path -Parent $OutputPath
    if ($outputDirectory) {
      New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
    }
    [System.IO.File]::WriteAllText($OutputPath, $output, [System.Text.UTF8Encoding]::new($false))
  }

  if ($output) {
    Write-Output $output
  }

  if ($sqlclExitCode -ne 0) {
    throw "SQLcl exited with code $sqlclExitCode. Review the captured output."
  }

  if ($output -match '(?im)^\s*(?:ORA-|SP2-|TNS-|ERROR:|Exception\b|java\.(?:io|lang)\.|SQLCL_ERROR_CLASS=)') {
    throw "SQLcl reported an Oracle or Java error despite a zero exit code. Review the captured output."
  }
} finally {
  Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
