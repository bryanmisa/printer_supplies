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

REM Collect static files
echo Collecting static files...
%PYTHON% manage.py collectstatic --noinput --clear >nul 2>&1

echo.
echo ==============================================
echo  SuppliesPro - Production Server (Waitress)
echo ==============================================
echo  URL: http://0.0.0.0:8080
echo  (Accessible from other computers on network)
echo.
echo  Press Ctrl+C to stop the server
echo ==============================================
echo.

REM Run with Waitress (0.0.0.0 makes it accessible from other computers)
%PYTHON% -m waitress --host=0.0.0.0 --port=8080 wsgi:application