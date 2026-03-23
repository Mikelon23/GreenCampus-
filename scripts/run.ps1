param(
  [switch]$SkipMigrations,
  [switch]$SkipSeed,
  [switch]$StartFrontend,
  [switch]$StartSimulator,
  [string]$BackendHost = "0.0.0.0",
  [int]$BackendPort = 8000,
  [string]$SimEmail = "admin@greencampus.local",
  [string]$SimPassword = "ChangeMe123!",
  [string]$DatabaseUrl
)

$ErrorActionPreference = "Stop"

function Fix-PathKey {
  $path = [Environment]::GetEnvironmentVariable("Path", "Process")
  if ($null -ne $path -and $path.Length -gt 0) {
    [Environment]::SetEnvironmentVariable("Path", $null, "Process")
    [Environment]::SetEnvironmentVariable("PATH", $path, "Process")
  }
}

function Load-EnvValue {
  param([string]$EnvPath, [string]$Key)
  if (-not (Test-Path $EnvPath)) { return $null }
  $lines = Get-Content $EnvPath
  foreach ($line in $lines) {
    if ($line.Trim().StartsWith("#") -or -not $line.Contains("=")) { continue }
    $parts = $line.Split("=", 2)
    if ($parts[0].Trim().Equals($Key, [System.StringComparison]::OrdinalIgnoreCase)) {
      return $parts[1].Trim()
    }
  }
  return $null
}

function Wait-ForBackend {
  param([string]$BaseUrl, [int]$Attempts = 20, [int]$DelaySeconds = 1)
  for ($i = 0; $i -lt $Attempts; $i++) {
    try {
      $zones = Invoke-RestMethod -Uri "$BaseUrl/api/zones" -Method Get -TimeoutSec 2
      if ($zones) { return $zones }
    } catch { }
    Start-Sleep -Seconds $DelaySeconds
  }
  return $null
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot
Fix-PathKey

if (-not $DatabaseUrl) {
  $DatabaseUrl = Load-EnvValue -EnvPath (Join-Path $repoRoot "backend\.env") -Key "DATABASE_URL"
}
if (-not $DatabaseUrl) {
  throw "DATABASE_URL is required (provide -DatabaseUrl or set it in backend/.env)."
}

$env:PYTHONPATH = "$repoRoot\backend\_deps_compat;$repoRoot\backend\_deps;$repoRoot"
$env:DATABASE_URL = $DatabaseUrl

if (-not $SkipMigrations) {
  python -m alembic -c backend\alembic.ini upgrade head
}

if (-not $SkipSeed) {
  python scripts\seed_data.py
}

$backendArgs = @("-m", "uvicorn", "backend.main:app", "--host", $BackendHost, "--port", $BackendPort.ToString())
$backendProc = Start-Process -FilePath python -ArgumentList $backendArgs -WorkingDirectory $repoRoot `
  -RedirectStandardOutput "backend\uvicorn.log" -RedirectStandardError "backend\uvicorn.err" -PassThru
Write-Output ("Backend PID: " + $backendProc.Id)

$baseUrl = "http://localhost:$BackendPort"

if ($StartSimulator) {
  $zones = Wait-ForBackend -BaseUrl $baseUrl
  if (-not $zones) {
    Write-Warning "Backend did not become ready. Simulator not started."
  } else {
    $loginBody = @{ email = $SimEmail; password = $SimPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
    $token = $login.access_token
    $zoneIds = ($zones | ForEach-Object { $_.id }) -join ","
    $simCmd = "set SIM_API_BASE_URL=$baseUrl& set SIM_AUTH_TOKEN=$token& set SIM_ZONE_IDS=$zoneIds& python simulation\simulator.py"
    $simProc = Start-Process -FilePath cmd.exe -ArgumentList "/c", $simCmd -WorkingDirectory $repoRoot -PassThru
    Write-Output ("Simulator PID: " + $simProc.Id)
  }
}

if ($StartFrontend) {
  $frontendCmd = "cd /d $repoRoot\frontend && npm run dev"
  $frontProc = Start-Process -FilePath cmd.exe -ArgumentList "/c", $frontendCmd -WorkingDirectory $repoRoot -PassThru
  Write-Output ("Frontend PID: " + $frontProc.Id)
}

Write-Output "Run complete."
