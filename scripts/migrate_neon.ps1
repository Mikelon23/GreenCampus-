param(
  [Parameter(Mandatory = $true)]
  [string]$DatabaseUrl
)

$ErrorActionPreference = "Stop"
$env:DATABASE_URL = $DatabaseUrl

Push-Location (Join-Path $PSScriptRoot "..")
try {
  python -m alembic -c backend/alembic.ini upgrade head
}
finally {
  Pop-Location
}
