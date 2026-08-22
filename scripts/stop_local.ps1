# ADPilot Pro - Local System Shutdown Script (PowerShell)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "             STOPPING ADPILOT PRO LOCAL SERVICES                " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# Stop Uvicorn processes
$uvicornProcesses = Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue
if ($uvicornProcesses) {
    Write-Host "Stopping Uvicorn backend processes ($($uvicornProcesses.Count))..." -ForegroundColor Yellow
    $uvicornProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
}

# Stop Vite / Node dev servers running in project
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Host "Stopping Node.js frontend dev servers..." -ForegroundColor Yellow
    $nodeProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
}

Write-Host "All local ADPilot services stopped successfully." -ForegroundColor Green
