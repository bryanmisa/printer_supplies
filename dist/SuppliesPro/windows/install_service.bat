@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo  SuppliesPro - Install Windows Service
echo ===============================================
echo.

set SCRIPT_DIR=%~dp0
set PARENT_DIR=%SCRIPT_DIR%..
set APP_DIR=%PARENT_DIR%\app

echo App directory: %APP_DIR%
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as Administrator.
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

REM Check if app directory exists
if not exist "%APP_DIR%" (
    echo [ERROR] App directory not found: %APP_DIR%
    pause
    exit /b 1
)

REM Check if NSSM (Non-Sucking Service Manager) is available
set NSSM_EXE=
where nssm >nul 2>&1
if %errorlevel% equ 0 (
    set NSSM_EXE=nssm
) else if exist "%ProgramFiles%\NSSM\nssm.exe" (
    set NSSM_EXE=%ProgramFiles%\NSSM\nssm.exe
) else if exist "%ProgramFiles(x86)%\NSSM\nssm.exe" (
    set NSSM_EXE=%ProgramFiles(x86)%\NSSM\nssm.exe
)

if "%NSSM_EXE%"=="" (
    echo [WARNING] NSSM not found. Using alternative method.
    echo.
    goto :USE_TASK_SCHEDULER
)

echo [1/2] Installing service using NSSM...

REM Get Python path
if exist "%PARENT_DIR%\venv\Scripts\python.exe" (
    set PYTHON_EXE=%PARENT_DIR%\venv\Scripts\python.exe
) else (
    set PYTHON_EXE=python.exe
)

REM Stop and remove existing service if it exists
%NSSM_EXE% stop SuppliesPro >nul 2>&1
%NSSM_EXE% remove SuppliesPro confirm >nul 2>&1

REM Install service
%NSSM_EXE% install SuppliesPro "!PYTHON_EXE!" "!APP_DIR!\manage.py" runserver 0.0.0.0:8080
%NSSM_EXE% set SuppliesPro AppDirectory "!APP_DIR!"
%NSSM_EXE% set SuppliesPro DisplayName "SuppliesPro Printer Inventory"
%NSSM_EXE% set SuppliesPro Description "Printer Inventory Management System"
%NSSM_EXE% set SuppliesPro Start SERVICE_AUTO_START
%NSSM_EXE% set SuppliesPro AppStdout "!APP_DIR!\logs\service.log"
%NSSM_EXE% set SuppliesPro AppStderr "!APP_DIR!\logs\service_error.log"

REM Create logs directory
if not exist "!APP_DIR!\logs" mkdir "!APP_DIR!\logs"

REM Start service
%NSSM_EXE% start SuppliesPro

echo   Service installed and started!
goto :COMPLETE

:USE_TASK_SCHEDULER
echo [1/2] Installing using Task Scheduler...

REM Create a startup script
set START_SCRIPT=%PARENT_DIR%\windows\run_service.bat
(
echo @echo off
echo cd /d "%APP_DIR%"
if exist "%PARENT_DIR%\venv\Scripts\python.exe" (
    echo "%PARENT_DIR%\venv\Scripts\python.exe" "%APP_DIR%\manage.py" runserver 0.0.0.0:8080
) else (
    echo python "%APP_DIR%\manage.py" runserver 0.0.0.0:8080
)
) > "!START_SCRIPT!"

REM Create scheduled task to run at startup
schtasks /create /tn "SuppliesPro" /tr "!START_SCRIPT!" /sc onstart /ru SYSTEM /f >nul 2>&1

if %errorlevel% equ 0 (
    echo   Task scheduled for startup!
    echo   Starting task now...
    schtasks /run /tn "SuppliesPro"
) else (
    echo   [ERROR] Failed to create scheduled task.
    pause
    exit /b 1
)

:COMPLETE
echo.
echo [2/2] Creating startup script for user login...

REM Create startup shortcut
set STARTUP_FOLDER=%APP_DATA%\Microsoft\Windows\Start Menu\Programs\Startup
if not exist "!STARTUP_FOLDER!" set STARTUP_FOLDER=%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup

if exist "!STARTUP_FOLDER!" (
    (
    echo @echo off
    echo cd /d "%APP_DIR%"
    if exist "%PARENT_DIR%\venv\Scripts\python.exe" (
        echo start "" "%PARENT_DIR%\venv\Scripts\python.exe" "%APP_DIR%\manage.py" runserver 0.0.0.0:8080
    ) else (
        echo start "" python "%APP_DIR%\manage.py" runserver 0.0.0.0:8080
    )
    ) > "!STARTUP_FOLDER!\SuppliesPro.bat"
    echo   Startup shortcut created in: !STARTUP_FOLDER!
)

echo.
echo ==============================================
echo  Installation Complete!
echo ==============================================
echo.
echo  Service Commands:
if not "%NSSM_EXE%"=="" (
    echo  - Start:   nssm start SuppliesPro
    echo  - Stop:    nssm stop SuppliesPro
    echo  - Restart: nssm restart SuppliesPro
    echo  - Status:  nssm status SuppliesPro
    echo  - Remove:  nssm remove SuppliesPro confirm
) else (
    echo  - Start:   schtasks /run /tn "SuppliesPro"
    echo  - Stop:    schtasks /end /tn "SuppliesPro"
    echo  - Delete:  schtasks /delete /tn "SuppliesPro" /f
)
echo ==============================================
echo.
echo  Server will be available at: http://localhost:8080
echo  Or from other computers: http://[your-ip]:8080
echo ==============================================
echo.
pause
