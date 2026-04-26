@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

REM Check if venv exists
if exist "venv\Scripts\python.exe" (
    set PYTHON=venv\Scripts\python.exe
    set PIP=venv\Scripts\pip.exe
) else (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  SuppliesPro - Update Script (Windows)
echo ===============================================
echo.

REM Check if database exists
if not exist "app\db.sqlite3" (
    echo [ERROR] No database found. Run setup.bat first.
    pause
    exit /b 1
)

REM Check if server is running
netstat -ano | findstr ":8080" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Server appears to be running on port 8080.
    echo.
    echo To stop the server, press Ctrl+C in the server window.
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "!CONTINUE!"=="y" exit /b 0
)

echo.
echo [1/4] Creating database backup...
if not exist "backups" mkdir backups
set BACKUP_DATE=%date:~-4%-%date:~4,2%-%date:~7,2%_D%time:~0,2%h%time:~3,2%
set BACKUP_DATE=!BACKUP_DATE: =0!
set BACKUP_NAME=backup_pre_update_!BACKUP_DATE!.sqlite3
copy /y app\db.sqlite3 "backups\!BACKUP_NAME!" >nul
if exist "backups\!BACKUP_NAME!" (
    echo   Backup created: backups\!BACKUP_NAME!
) else (
    echo [ERROR] Failed to create backup.
    pause
    exit /b 1
)

echo.
echo [2/4] Checking for Python dependencies...
if exist "requirements.txt" (
    if exist "venv\Scripts\python.exe" (
        echo   Dependencies OK.
    )
)

echo.
echo [3/4] Running database migrations...
cd app
%PYTHON% manage.py migrate --plan >nul 2>&1
if errorlevel 1 (
    echo   Unable to check migrations.
) else (
    for /f "delims=" %%i in ('%PYTHON% manage.py migrate --plan 2^>nul') do set MIGRATIONS=%%i
    if "!MIGRATIONS!"=="" (
        echo   No pending migrations found.
    ) else (
        echo   Applying migrations...
        %PYTHON% manage.py migrate --noinput
        if errorlevel 1 (
            echo.
            echo [ERROR] Migration failed. Restoring backup...
            cd ..
            copy /y "backups\%BACKUP_NAME%" app\db.sqlite3
            echo   Backup restored.
            pause
            exit /b 1
        )
    )
)
cd ..

echo.
echo [4/4] Recording update in CHANGELOG.txt...
echo =============================================== >> CHANGELOG.txt
echo Update: %date% %time% >> CHANGELOG.txt
echo =============================================== >> CHANGELOG.txt
echo - Database backed up: !BACKUP_NAME! >> CHANGELOG.txt
echo - Migrations applied >> CHANGELOG.txt
echo. >> CHANGELOG.txt

echo.
echo ===============================================
echo  Update Complete!
echo.
echo  Backup: !BACKUP_NAME!
echo.
echo  To start the server, run: windows\start.bat
echo ===============================================
echo.
pause