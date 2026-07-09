param(
  [Parameter(Mandatory = $true)]
  [string]$Pattern,

  [string]$Owner = "HADES",

  [string]$TableLike = "%",

  [string]$Connection = $(if ($env:ERGON_HADES_CONN) { $env:ERGON_HADES_CONN } else { $env:ERGON_ORACLE_CONNECTION }),

  [string]$SqlclPath = $(if ($env:ERGON_SQLCL) { $env:ERGON_SQLCL } else { ".\tools\sqlcl\bin\sql.exe" }),

  [string]$JavaHome = $env:JAVA_HOME,

  [int]$MaxSamplesPerColumn = 3,

  [int]$QueryTimeoutSeconds = 8,

  [string]$ExcludeTableRegex = "^(HADES_ERROS.*|HADADM00003_.*|HAD_ARQ_GERADO.*|HAD_WFCAM_.*|HAD_MAIL|HAD_ROTINA_EXEC)$",

  [string]$OutputPath
)

$ErrorActionPreference = "Stop"

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

$work = Join-Path ([System.IO.Path]::GetTempPath()) ("ergon-text-search-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $work | Out-Null

try {
  $javaFile = Join-Path $work "SearchOracleText.java"
  @'
import java.sql.*;
import java.util.*;

public class SearchOracleText {
  static class ConnParts {
    String user;
    String password;
    String jdbcUrl;
  }

  static class ColumnInfo {
    String owner;
    String tableName;
    String columnName;
    String dataType;
  }

  public static void main(String[] args) throws Exception {
    String connText = System.getenv("ERGON_JDBC_CONN");
    if (connText == null || connText.isBlank()) {
      throw new IllegalArgumentException("ERGON_JDBC_CONN was not provided to the Java process.");
    }
    String owner = args[0].toUpperCase(Locale.ROOT);
    String tableLike = args[1].toUpperCase(Locale.ROOT);
    String pattern = args[2];
    int maxSamples = Integer.parseInt(args[3]);
    int timeout = Integer.parseInt(args[4]);
    String excludeTableRegex = args.length >= 6 ? args[5] : "";

    ConnParts parts = parseConnection(connText);
    try (Connection conn = DriverManager.getConnection(parts.jdbcUrl, parts.user, parts.password)) {
      List<ColumnInfo> columns = loadColumns(conn, owner, tableLike);
      if (!excludeTableRegex.isBlank()) {
        columns.removeIf(c -> c.tableName.matches(excludeTableRegex));
      }
      System.out.println("Searching " + columns.size() + " text columns in owner " + owner + " for pattern [" + pattern + "]");
      System.out.println("OWNER|TABLE_NAME|COLUMN_NAME|DATA_TYPE|SAMPLE");
      for (ColumnInfo col : columns) {
        searchColumn(conn, col, pattern, maxSamples, timeout);
      }
    }
  }

  static List<ColumnInfo> loadColumns(Connection conn, String owner, String tableLike) throws SQLException {
    String sql = """
      select owner, table_name, column_name, data_type
      from all_tab_columns
      where owner = ?
        and table_name like ?
        and data_type in ('CHAR','NCHAR','VARCHAR2','NVARCHAR2','CLOB','NCLOB')
      order by owner, table_name, column_id
      """;
    List<ColumnInfo> out = new ArrayList<>();
    try (PreparedStatement ps = conn.prepareStatement(sql)) {
      ps.setString(1, owner);
      ps.setString(2, tableLike);
      try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
          ColumnInfo c = new ColumnInfo();
          c.owner = rs.getString(1);
          c.tableName = rs.getString(2);
          c.columnName = rs.getString(3);
          c.dataType = rs.getString(4);
          out.add(c);
        }
      }
    }
    return out;
  }

  static void searchColumn(Connection conn, ColumnInfo col, String pattern, int maxSamples, int timeout) {
    String qOwner = quoteName(col.owner);
    String qTable = quoteName(col.tableName);
    String qColumn = quoteName(col.columnName);
    boolean lob = col.dataType.equals("CLOB") || col.dataType.equals("NCLOB");
    String where = lob
      ? "dbms_lob.instr(upper(" + qColumn + "), upper(?)) > 0"
      : "upper(" + qColumn + ") like upper(?)";
    String sample = lob
      ? "replace(replace(dbms_lob.substr(" + qColumn + ", 240, greatest(1, dbms_lob.instr(upper(" + qColumn + "), upper(?)) - 80)), chr(10), ' '), chr(13), ' ')"
      : "replace(replace(substr(" + qColumn + ", 1, 240), chr(10), ' '), chr(13), ' ')";
    String sql = "select sample_text from (select " + sample + " as sample_text from " + qOwner + "." + qTable + " where " + where + ") where rownum <= " + maxSamples;

    try (PreparedStatement ps = conn.prepareStatement(sql)) {
      ps.setQueryTimeout(timeout);
      if (lob) {
        ps.setString(1, pattern);
        ps.setString(2, pattern);
      } else {
        ps.setString(1, "%" + pattern + "%");
      }
      try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
          String value = rs.getString(1);
          if (value == null) value = "";
          value = value.replace('|', '/').replace('\n', ' ').replace('\r', ' ');
          if (value.length() > 300) value = value.substring(0, 300) + "...";
          System.out.println(col.owner + "|" + col.tableName + "|" + col.columnName + "|" + col.dataType + "|" + value);
        }
      }
    } catch (Exception e) {
      String message = e.getMessage() == null ? e.getClass().getName() : e.getMessage().split("\\R")[0];
      System.out.println(col.owner + "|" + col.tableName + "|" + col.columnName + "|" + col.dataType + "|SEARCH_ERROR: " + message.replace('|', '/'));
    }
  }

  static String quoteName(String name) {
    return "\"" + name.replace("\"", "\"\"") + "\"";
  }

  static ConnParts parseConnection(String conn) {
    int slash = conn.indexOf('/');
    int at = conn.indexOf('@', slash + 1);
    if (slash <= 0 || at <= slash) {
      throw new IllegalArgumentException("Connection must look like user/password@host:port/service or use an equivalent SQLcl alias that resolves through JDBC.");
    }
    ConnParts parts = new ConnParts();
    parts.user = conn.substring(0, slash);
    parts.password = conn.substring(slash + 1, at);
    String target = conn.substring(at + 1);
    parts.jdbcUrl = target.startsWith("jdbc:") ? target : "jdbc:oracle:thin:@" + target;
    return parts;
  }
}
'@ | Set-Content -LiteralPath $javaFile -Encoding ASCII

  $argsList = @($javaFile, $Owner, $TableLike, $Pattern, $MaxSamplesPerColumn, $QueryTimeoutSeconds, $ExcludeTableRegex)
  $previousJdbcConn = [Environment]::GetEnvironmentVariable("ERGON_JDBC_CONN", "Process")
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_CONN", $Connection, "Process")
  if ($OutputPath) {
    & $JavaExe -cp $ojdbc $argsList | Tee-Object -FilePath $OutputPath
  } else {
    & $JavaExe -cp $ojdbc $argsList
  }
} finally {
  [Environment]::SetEnvironmentVariable("ERGON_JDBC_CONN", $previousJdbcConn, "Process")
  Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
