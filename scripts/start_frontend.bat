@echo off
title ADPilot Pro - Frontend Dashboard (Port 3000)
color 0D
cd /d "%~dp0..\frontend"

call npm run dev

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Frontend failed to start.
    pause
)
