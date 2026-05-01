@echo off
REM SuppliesPro - Windows Startup Script
REM This script will be called on system startup

set SCRIPT_DIR=%~dp0
set PARENT_DIR=%SCRIPT_DIR%..
set APP_DIR=%PARENT_DIR%\app

REM Create logs directory if not exists
if not exist "%APP_DIR%\logs" mkdir "%APP_DIR%\logs"

REM Get Python path
if exist "%PARENT_DIR%\venv\Scripts\python.exe" (
    set PYTHON=%PARENT_DIR%\venv\Scripts\python.exe
) else (
    set PYTHON=python.exe
)

cd /d "%APP_DIR%"
start "" /b %PYTHON% manage.py runserver 0.0.0.0:8080 > "%APP_DIR%\logs\server.log" 2>&1

echo SuppliesPro server started!
echo Log file: %APP_DIR%\logs\server.log
