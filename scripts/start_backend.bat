@echo off
title ADPilot Pro - Backend Server (Port 8001)
color 09
cd /d "%~dp0.."

set PYTHONPATH=%CD%\src;%PYTHONPATH%

if exist "%CD%\.venv\Scripts\activate.bat" (
    call "%CD%\.venv\Scripts\activate.bat"
    python -m uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001 --reload
) else if exist "%CD%\venv\Scripts\activate.bat" (
    call "%CD%\venv\Scripts\activate.bat"
    python -m uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001 --reload
) else (
    python -m uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001 --reload
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Backend failed to start.
    pause
)
