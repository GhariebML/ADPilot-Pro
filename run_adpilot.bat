@echo off
title ADPilot Pro v3.0 - Launcher
color 0B
cd /d "%~dp0"

echo ==============================================================================
echo                      STARTING ADPILOT PRO v3.0
echo             Autonomous Multi-Agent Marketing Operating System
echo ==============================================================================
echo.

:: 1. Verify .env
if not exist ".env" (
    if exist ".env.example" (
        copy /y ".env.example" ".env" >nul
        echo [*] Created .env from template.
    )
)

:: 2. Terminate any previous lingering processes on ports 8001 & 3000
echo [*] Cleaning up previous processes...
taskkill /FI "WINDOWTITLE eq ADPilot Pro - Backend Server*" /F /T >nul 2>&1
taskkill /FI "WINDOWTITLE eq ADPilot Pro - Frontend Dashboard*" /F /T >nul 2>&1

:: 3. Launch Backend in its own window
echo [*] Starting FastAPI Backend on http://127.0.0.1:8001...
start "ADPilot Pro - Backend Server (Port 8001)" "%~dp0scripts\start_backend.bat"

:: 4. Launch Frontend in its own window
echo [*] Starting React Dashboard on http://localhost:3000...
start "ADPilot Pro - Frontend Dashboard (Port 3000)" "%~dp0scripts\start_frontend.bat"

:: 5. Wait 3 seconds and launch browser directly
echo [*] Opening ADPilot Pro in your default browser...
timeout /t 3 /nobreak >nul
start "" "http://localhost:3000"

echo.
echo ==============================================================================
echo                 ADPILOT PRO IS NOW RUNNING SUCCESSFULLY!
echo ==============================================================================
echo.
echo   [+] Frontend URL:     http://localhost:3000
echo   [+] Backend API:      http://127.0.0.1:8001
echo   [+] API Swagger Docs: http://127.0.0.1:8001/docs
echo   [+] Health Endpoint:  http://127.0.0.1:8001/healthz
echo.
echo ==============================================================================
echo                             QUICK ACTIONS
echo ==============================================================================
echo.
echo   [1] Open Dashboard (http://localhost:3000)
echo   [2] Open Swagger Docs (http://127.0.0.1:8001/docs)
echo   [3] Stop All Services & Exit
echo.

:MENU_LOOP
set "CHOICE="
set /p CHOICE="Enter your choice (1, 2, or 3): "

if "%CHOICE%"=="1" (
    start "" "http://localhost:3000"
    goto MENU_LOOP
)
if "%CHOICE%"=="2" (
    start "" "http://127.0.0.1:8001/docs"
    goto MENU_LOOP
)
if "%CHOICE%"=="3" (
    echo.
    echo [*] Shutting down ADPilot Pro...
    call "%~dp0stop_adpilot.bat"
    exit /b 0
)

goto MENU_LOOP
