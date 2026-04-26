@echo off
cd /d "%~dp0..\app"

REM Check if venv exists
if exist "..\venv\Scripts\python.exe" (
    set PYTHON=..\venv\Scripts\python.exe
    set PIP=..\venv\Scripts\pip.exe
) else (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo Installing Waitress for production server...
%PIP% install waitress --quiet
if errorlevel 1 (
    echo.
    echo [ERROR] Waitress installation failed.
    pause
    exit /b 1
)

REM Check if database exists, if not create it
if not exist "db.sqlite3" (
    echo.
    echo Creating new database...
    %PYTHON% manage.py migrate --noinput
    %PYTHON% manage.py create_admin
)

echo.
echo ===============================================
echo  SuppliesPro - Production Server
echo ===============================================
echo  URL: http://localhost:8080
echo.
echo  Press Ctrl+C to stop the server
echo ===============================================
echo.
%PYTHON% serve_prod.py