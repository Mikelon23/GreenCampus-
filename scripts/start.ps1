Param(
  [switch]$Simulator
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw "docker is required."
}

try {
  docker compose version | Out-Null
} catch {
  throw "docker compose (v2) is required."
}

if (-not (Test-Path ".env")) {
  Write-Output "No .env found. Creating one from .env.example ..."
  Copy-Item ".env.example" ".env"
}

Write-Output "[1/4] Building images..."
docker compose build

Write-Output "[2/4] Starting database..."
docker compose up -d db

Write-Output "[3/4] Running migrations + seed (backend-init)..."
docker compose up --no-deps --abort-on-container-exit backend-init

Write-Output "[4/4] Starting backend + frontend..."
docker compose up -d backend frontend

if ($Simulator) {
  Write-Output "Starting simulator profile..."
  docker compose --profile simulator up -d simulator
}

Write-Output ""
Write-Output "Frontend: http://localhost:3000"
Write-Output "Backend:  http://localhost:8000 (Swagger: /docs)"

