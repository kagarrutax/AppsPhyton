# Inicia backend: verifica migración + uvicorn
$ErrorActionPreference = "Stop"
$BackendRoot = Split-Path -Parent $PSScriptRoot
Set-Location $BackendRoot

$Python = Join-Path $BackendRoot "venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "ERROR: Ejecute primero: python -m venv venv; pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

& $Python -c "from app.core.migration import verify_database_migrated; verify_database_migrated(); print('Migracion OK: head')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ejecute: .\scripts\migrate.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host ">>> Iniciando API en http://127.0.0.1:8000" -ForegroundColor Green
& (Join-Path $BackendRoot "venv\Scripts\uvicorn.exe") main:app --reload --host 127.0.0.1 --port 8000
