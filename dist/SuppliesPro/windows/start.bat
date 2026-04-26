@echo off
cd /d "%~dp0..\app"

REM Check if venv exists
if exist "..\venv\Scripts\python.exe" (
    set PYTHON=..\venv\Scripts\python.exe
) else (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  SuppliesPro - Starting Server (Windows)
echo ===============================================
echo  URL: http://localhost:8080
echo ===============================================
echo.
echo Opening browser...
start http://localhost:8080
%PYTHON% manage.py runserver 0.0.0.0:8080