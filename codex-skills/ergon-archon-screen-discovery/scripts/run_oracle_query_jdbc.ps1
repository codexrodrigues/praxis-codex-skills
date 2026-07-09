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
  [string]$OutputPath,

  [Parameter(Mandatory = $false)]
  [int]$MaxRows = 500,

  [Parameter(Mandatory = $false)]
  [switch]$ApplyErgonContext,

  [Parameter(Mandatory = $false)]
  [string]$ErgonUser = $(if ($env:ERGON_LEGACY_USUARIO) { $env:ERGON_LEGACY_USUARIO } else { $env:ERGON_LEGACY_USER }),

  [Parameter(Mandatory = $false)]
  [string]$ErgonEmpresa = $(if ($env:ERGON_LEGACY_EMPRESA) { $env:ERGON_LEGACY_EMPRESA } else { "" }),

  [Parameter(Mandatory = $false)]
  [string]$ErgonTransacao,

  [Parameter(Mandatory = $false)]
  [string]$ErgonSis = $env:ERGON_LEGACY_SIS,

  [Parameter(Mandatory = $false)]
  [string]$ErgonRole = $env:ERGON_LEGACY_ROLE
)

$ErrorActionPreference = "Stop"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

if (-not (Test-Path -LiteralPath $SqlFile)) {
  throw "SQL file not found: $SqlFile"
}

if (-not $Connection) {
  throw "Connection was not provided. Pass -Connection or set ERGON_HADES_CONN."
}

if (-not $SqlclPath) {
  if (Test-Path -LiteralPath ".\tools\sqlcl\bin\sql.exe") {
    $SqlclPath = (Resolve-Path -LiteralPath ".\tools\sqlcl\bin\sql.exe").Path
  } else {
    throw "SQLcl path was not provided. Set ERGON_SQLCL or keep SQLcl under tools\sqlcl."
  }
}

if (-not $JavaHome) {
  $java = Get-Command java -ErrorAction SilentlyContinue
  if (-not $java) {
    throw "Java was not found. Set JAVA_HOME."
  }
  $JavaExe = $java.Source
} else {
  $JavaExe = Join-Path $JavaHome "bin\java.exe"
  if (-not (Test-Path -LiteralPath $JavaExe)) {
    throw "Java not found: $JavaExe"
  }
}

$sqlclRoot = Split-Path -Parent (Split-Path -Parent $SqlclPath)
$ojdbc = Join-Path $sqlclRoot "lib\ojdbc11.jar"
if (-not (Test-Path -LiteralPath $ojdbc)) {
  throw "ojdbc11.jar not found under SQLcl: $ojdbc"
}

$work = Join-Path ([System.IO.Path]::GetTempPath()) ("ergon-jdbc-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $work | Out-Null

try {
  $javaFile = Join-Path $work "RunOracleSql.java"
  @'
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.sql.*;
import java.util.*;

public class RunOracleSql {
  static class ConnParts {
    String user;
    String password;
    String jdbcUrl;
  }

  public static void main(String[] args) throws Exception {
    System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out), true, StandardCharsets.UTF_8));
    System.setErr(new PrintStream(new FileOutputStream(FileDescriptor.err), true, StandardCharsets.UTF_8));
    String conn = System.getenv("ERGON_JDBC_CONN");
    if (conn == null || conn.isBlank()) {
      throw new IllegalArgumentException("ERGON_JDBC_CONN was not provided to the Java process.");
    }
    String sqlFile = args[0];
    int maxRows = args.length >= 2 ? Integer.parseInt(args[1]) : 500;
    ConnParts cp = parseConnection(conn);
    Class.forName("oracle.jdbc.OracleDriver");
    try (Connection c = DriverManager.getConnection(cp.jdbcUrl, cp.user, cp.password)) {
      c.setReadOnly(true);
      applyErgonContext(c);
      List<String> statements = parseSql(Files.readString(Path.of(sqlFile), StandardCharsets.UTF_8));
      int index = 0;
      for (String sql : statements) {
        index++;
        System.out.println();
        System.out.println("== Statement " + index + " ==");
        System.out.println(firstLine(sql));
        try (Statement st = c.createStatement()) {
          st.setFetchSize(100);
          boolean hasResult = st.execute(sql);
          if (hasResult) {
            printResult(st.getResultSet(), maxRows);
          } else {
            System.out.println("Update count: " + st.getUpdateCount());
          }
        } catch (SQLException e) {
          System.out.println("ERROR: " + e.getMessage());
        }
      }
    }
  }

  static void applyErgonContext(Connection c) throws SQLException {
    String enabled = System.getenv("ERGON_JDBC_APPLY_ERGON_CONTEXT");
    if (!"1".equals(enabled)) return;

    String user = blankToNull(System.getenv("ERGON_JDBC_LEGACY_USER"));
    String sis = blankToNull(System.getenv("ERGON_JDBC_LEGACY_SIS"));
    String transacao = blankToNull(System.getenv("ERGON_JDBC_LEGACY_TRANSACAO"));
    String role = blankToNull(System.getenv("ERGON_JDBC_LEGACY_ROLE"));
    String empresa = blankToNull(System.getenv("ERGON_JDBC_LEGACY_EMPRESA"));

    try {
      if (user != null) callStringProcedure(c, "HADES.FLAG_PACK.SET_USUARIO", user);
      if (sis != null) callStringProcedure(c, "HADES.FLAG_PACK.SET_SIS", sis);
      if (transacao != null) callStringProcedure(c, "HADES.FLAG_PACK.SET_TRANSACAO", transacao);
      if (role != null) callStringProcedure(c, "HADES.FLAG_PACK.SET_ROLE", role);
      if (empresa != null) callEmpresaProcedure(c, empresa);
    } catch (SQLException e) {
      System.out.println("ERROR_CONTEXT_SETUP: " + e.getMessage());
      throw e;
    }
  }

  static String blankToNull(String value) {
    if (value == null || value.isBlank()) return null;
    return value.trim();
  }

  static void callStringProcedure(Connection c, String procedure, String value) throws SQLException {
    try (CallableStatement cs = c.prepareCall("{ call " + procedure + "(?) }")) {
      cs.setString(1, value);
      cs.execute();
    }
  }

  static void callEmpresaProcedure(Connection c, String value) throws SQLException {
    try (CallableStatement cs = c.prepareCall("{ call HADES.FLAG_PACK.SET_EMPRESA(?) }")) {
      try {
        cs.setInt(1, Integer.parseInt(value));
      } catch (NumberFormatException e) {
        cs.setString(1, value);
      }
      cs.execute();
    }
  }

  static ConnParts parseConnection(String conn) {
    ConnParts cp = new ConnParts();
    if (conn.startsWith("jdbc:oracle:")) {
      cp.jdbcUrl = conn;
      cp.user = System.getenv("ERGON_DB_USER");
      cp.password = System.getenv("ERGON_DB_PASSWORD");
      if (cp.user == null || cp.password == null) {
        throw new IllegalArgumentException("JDBC URL requires ERGON_DB_USER and ERGON_DB_PASSWORD.");
      }
      return cp;
    }
    int slash = conn.indexOf('/');
    int at = conn.indexOf('@', slash + 1);
    if (slash <= 0 || at <= slash) {
      throw new IllegalArgumentException("Expected connection format user/password@host:port/service or JDBC URL.");
    }
    cp.user = conn.substring(0, slash);
    cp.password = conn.substring(slash + 1, at);
    cp.jdbcUrl = "jdbc:oracle:thin:@" + conn.substring(at + 1);
    return cp;
  }

  static List<String> parseSql(String text) {
    List<String> cleaned = new ArrayList<>();
    for (String rawLine : text.split("\\R")) {
      String line = rawLine.stripTrailing();
      String trimmed = line.trim();
      String lower = trimmed.toLowerCase(Locale.ROOT);
      if (trimmed.isEmpty() || trimmed.startsWith("--")) continue;
      if (lower.startsWith("set ") || lower.startsWith("column ") || lower.startsWith("prompt ")) continue;
      cleaned.add(line);
    }
    String joined = String.join("\n", cleaned);
    List<String> out = new ArrayList<>();
    StringBuilder sb = new StringBuilder();
    boolean inQuote = false;
    for (int i = 0; i < joined.length(); i++) {
      char ch = joined.charAt(i);
      if (ch == '\'') {
        sb.append(ch);
        if (inQuote && i + 1 < joined.length() && joined.charAt(i + 1) == '\'') {
          sb.append(joined.charAt(++i));
        } else {
          inQuote = !inQuote;
        }
      } else if (ch == ';' && !inQuote) {
        addStatement(out, sb);
      } else {
        sb.append(ch);
      }
    }
    addStatement(out, sb);
    return out;
  }

  static void addStatement(List<String> out, StringBuilder sb) {
    String s = sb.toString().trim();
    sb.setLength(0);
    String lower = s.toLowerCase(Locale.ROOT);
    if (!s.isEmpty() && (lower.startsWith("select") || lower.startsWith("with"))) {
      out.add(s);
    }
  }

  static String firstLine(String sql) {
    String s = sql.replace('\n', ' ').replaceAll("\\s+", " ").trim();
    return s.length() > 180 ? s.substring(0, 180) + "..." : s;
  }

  static void printResult(ResultSet rs, int limit) throws SQLException {
    ResultSetMetaData md = rs.getMetaData();
    int cols = md.getColumnCount();
    for (int i = 1; i <= cols; i++) {
      if (i > 1) System.out.print("|");
      System.out.print(md.getColumnLabel(i));
    }
    System.out.println();
    int rows = 0;
    while (rs.next() && rows < limit) {
      rows++;
      for (int i = 1; i <= cols; i++) {
        if (i > 1) System.out.print("|");
        Object value = rs.getObject(i);
        String text = value == null ? "" : String.valueOf(value).replace('\n', ' ').replace('\r', ' ');
        if (text.length() > 500) text = text.substring(0, 500) + "...";
        System.out.print(text);
      }
      System.out.println();
    }
    System.out.println("Rows shown: " + rows);
  }
}
'@ | Set-Content -LiteralPath $javaFile -Encoding ASCII

  $previousJdbcConn = [Environment]::GetEnvironmentVariable("ERGON_JDBC_CONN", "Process")
  $previousApplyContext = [Environment]::GetEnvironmentVariable("ERGON_JDBC_APPLY_ERGON_CONTEXT", "Process")
  $previousContextUser = [Environment]::GetEnvironmentVariable("ERGON_JDBC_LEGACY_USER", "Process")
  $previousContextEmpresa = [Environment]::GetEnvironmentVariable("ERGON_JDBC_LEGACY_EMPRESA", "Process")
  $previousContextTransacao = [Environment]::GetEnvironmentVariable("ERGON_JDBC_LEGACY_TRANSACAO", "Process")
  $previousContextSis = [Environment]::GetEnvironmentVariable("ERGON_JDBC_LEGACY_SIS", "Process")
  $previousContextRole = [Environment]::GetEnvironmentVariable("ERGON_JDBC_LEGACY_ROLE", "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_CONN", $Connection, "Process")
  if ($ApplyErgonContext) {
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_APPLY_ERGON_CONTEXT", "1", "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_USER", $ErgonUser, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_EMPRESA", $ErgonEmpresa, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_TRANSACAO", $ErgonTransacao, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_SIS", $ErgonSis, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_ROLE", $ErgonRole, "Process")
  } else {
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_APPLY_ERGON_CONTEXT", $null, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_USER", $null, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_EMPRESA", $null, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_TRANSACAO", $null, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_SIS", $null, "Process")
    [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_ROLE", $null, "Process")
  }
  $previousErrorActionPreference = $ErrorActionPreference
  try {
    $ErrorActionPreference = "Continue"
    if ($OutputPath) {
      & $JavaExe "-Dfile.encoding=UTF-8" -cp $ojdbc $javaFile (Resolve-Path -LiteralPath $SqlFile).Path $MaxRows 2>&1 |
        Tee-Object -FilePath $OutputPath
    } else {
      & $JavaExe "-Dfile.encoding=UTF-8" -cp $ojdbc $javaFile (Resolve-Path -LiteralPath $SqlFile).Path $MaxRows 2>&1
    }
    $javaExitCode = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $previousErrorActionPreference
  }
  if ($javaExitCode -ne 0) {
    exit $javaExitCode
  }
} finally {
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_CONN", $previousJdbcConn, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_APPLY_ERGON_CONTEXT", $previousApplyContext, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_USER", $previousContextUser, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_EMPRESA", $previousContextEmpresa, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_TRANSACAO", $previousContextTransacao, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_SIS", $previousContextSis, "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_LEGACY_ROLE", $previousContextRole, "Process")
  Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
