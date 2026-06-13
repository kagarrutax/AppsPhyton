# Migración completa de base de datos — FastFood Platform
# Uso: .\scripts\migrate.ps1 [-Setup] [-Upgrade] [-Seed] [-ShowCurrent]

param(
    [switch]$Setup,
    [switch]$Upgrade,
    [switch]$Seed,
    [switch]$ShowCurrent
)

$ErrorActionPreference = "Stop"
$BackendRoot = Split-Path -Parent $PSScriptRoot
Set-Location $BackendRoot

$Python = Join-Path $BackendRoot "venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "ERROR: No existe venv. Ejecute: python -m venv venv; pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

function Invoke-Migrate {
    param([string[]]$MigrateArgs)
    & $Python (Join-Path $BackendRoot "scripts\migrate.py") @MigrateArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

# Crear BD si no existe (XAMPP MySQL)
$Mysql = "C:\xampp\mysql\bin\mysql.exe"
if (Test-Path $Mysql) {
    Write-Host ">>> Verificando base de datos fastfood_db..." -ForegroundColor Cyan
    & $Mysql -u root -e "CREATE DATABASE IF NOT EXISTS fastfood_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>$null
}

if ($Setup -or (-not $Upgrade -and -not $Seed -and -not $ShowCurrent)) {
    Write-Host ">>> Setup completo: migrate + seed" -ForegroundColor Green
    Invoke-Migrate @("setup")
    exit 0
}

if ($Upgrade) { Invoke-Migrate @("upgrade") }
if ($Seed)    { Invoke-Migrate @("seed") }
if ($ShowCurrent) { Invoke-Migrate @("current") }

Write-Host ">>> Listo." -ForegroundColor Green
