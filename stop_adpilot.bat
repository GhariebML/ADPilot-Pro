@echo off
title ADPilot Pro - Shutdown
color 0C
cd /d "%~dp0"

echo ==============================================================================
echo                 STOPPING ALL ADPILOT PRO LOCAL SERVICES
echo ==============================================================================
echo.

echo [*] Closing Backend and Frontend windows...
taskkill /FI "WINDOWTITLE eq ADPilot Pro - Backend Server*" /F /T >nul 2>&1
taskkill /FI "WINDOWTITLE eq ADPilot Pro - Frontend Dashboard*" /F /T >nul 2>&1

echo [*] Terminating Python and Node.js server processes...
taskkill /IM "uvicorn.exe" /F >nul 2>&1
powershell -Command "Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue" >nul 2>&1

echo.
echo [OK] All local ADPilot Pro services stopped.
timeout /t 2 >nul
exit /b 0
