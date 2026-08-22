# ADPilot Pro - Local System Startup Script (PowerShell)
param (
    [int]$BackendPort = 8001,
    [int]$FrontendPort = 3000
)

$ErrorActionPreference = "Continue"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "             STARTING ADPILOT PRO LOCAL ENVIRONMENT             " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Navigate to Project Root
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location -Path $ProjectRoot
Write-Host "[1/4] Project root: $ProjectRoot" -ForegroundColor Green

# 2. Environment & Python path
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "  -> Created .env from template." -ForegroundColor Yellow
}
$env:PYTHONPATH = "src"

# 3. Start Backend FastAPI via Uvicorn
Write-Host "[2/4] Launching FastAPI Backend on port $BackendPort..." -ForegroundColor Green
$BackendProcess = Start-Process -FilePath "uvicorn" -ArgumentList "adpilot.api.main:app --host 127.0.0.1 --port $BackendPort" -PassThru -NoNewWindow
Start-Sleep -Seconds 3

# Check Backend Health
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:$BackendPort/healthz" -Method Get -TimeoutSec 5
    Write-Host "  -> Backend is HEALTHY (Status: $($health.status), Version: $($health.version))" -ForegroundColor Green
} catch {
    Write-Host "  -> Waiting for backend to finish initialising..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# 4. Start Frontend Vite Dev Server
Write-Host "[3/4] Launching React Dashboard on port $FrontendPort..." -ForegroundColor Green
Set-Location -Path (Join-Path $ProjectRoot "frontend")
$FrontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -PassThru -NoNewWindow
Set-Location -Path $ProjectRoot
Start-Sleep -Seconds 2

# 5. Ready Summary
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "               ADPILOT PRO IS NOW RUNNING LOCALLY               " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  👉 Frontend Dashboard: http://localhost:$FrontendPort" -ForegroundColor Yellow
Write-Host "  👉 Backend API:        http://127.0.0.1:$BackendPort" -ForegroundColor Yellow
Write-Host "  👉 Swagger API Docs:   http://127.0.0.1:$BackendPort/docs" -ForegroundColor Yellow
Write-Host "  👉 Health Endpoint:    http://127.0.0.1:$BackendPort/healthz" -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "To stop the system, run: .\scripts\stop_local.ps1" -ForegroundColor Gray
