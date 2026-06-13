# Inicia frontend Vite
$ErrorActionPreference = "Stop"
$FrontendRoot = Split-Path -Parent $PSScriptRoot
Set-Location $FrontendRoot

if (-not (Test-Path "node_modules")) {
    Write-Host ">>> Instalando dependencias..." -ForegroundColor Cyan
    npm install
}

Write-Host ">>> Frontend en http://127.0.0.1:5173" -ForegroundColor Green
npm run dev -- --host 127.0.0.1 --port 5173
