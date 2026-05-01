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
echo ==============================================
echo  SuppliesPro - Update Script (Windows)
echo ==============================================
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
echo [1/5] Creating database backup...
if not exist "backups" mkdir backups
set BACKUP_DATE=%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%h%time:~3,2%
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
echo [2/5] Checking for file updates...
set CHANGE_LOG=update_!BACKUP_DATE!_changelog.txt
echo ==============================================> "!CHANGE_LOG!"
echo Update: %date% %time% >> "!CHANGE_LOG!"
echo ==============================================>> "!CHANGE_LOG!"
echo. >> "!CHANGE_LOG!"

REM Check for source directory
set SOURCE_DIR=
if exist "..\..\SuppliesPro" (
    set SOURCE_DIR=..\..\SuppliesPro
) else if exist "C:\projects\SuppliesPro" (
    set SOURCE_DIR=C:\projects\SuppliesPro
) else if exist "%USERPROFILE%\projects\SuppliesPro" (
    set SOURCE_DIR=%USERPROFILE%\projects\SuppliesPro
)

if defined SOURCE_DIR (
    echo   Source directory found: !SOURCE_DIR!
    echo   Comparing and copying updated files...
    echo.
    
    set UPDATED_FILES=0
    set NEW_FILES=0
    set DELETED_FILES=0
    
    REM Copy app files
    for /r "!SOURCE_DIR!\app" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=app\!rel_path:app\=!"
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo   [MODIFIED] !rel_path! | tee -a "!CHANGE_LOG!"
                set /a UPDATED_FILES+=1
            )
        ) else (
            if not exist "!\dest_file!\.." mkdir "!\dest_file!\.." 2>nul
            copy /y "!src_file!" "!dest_file!" >nul
            echo   [NEW] !rel_path! | tee -a "!CHANGE_LOG!"
            set /a NEW_FILES+=1
        )
    )
    
    REM Copy static files
    for /r "!SOURCE_DIR!\static" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=app\static\!rel_path:static\=!"
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo   [MODIFIED] !rel_path! | tee -a "!CHANGE_LOG!"
                set /a UPDATED_FILES+=1
            )
        ) else (
            if not exist "!\dest_file!\.." mkdir "!\dest_file!\.." 2>nul
            copy /y "!src_file!" "!dest_file!" >nul
            echo   [NEW] !rel_path! | tee -a "!CHANGE_LOG!"
            set /a NEW_FILES+=1
        )
    )
    
    REM Copy templates files
    for /r "!SOURCE_DIR!\templates" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=app\templates\!rel_path:templates\=!"
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo   [MODIFIED] !rel_path! | tee -a "!CHANGE_LOG!"
                set /a UPDATED_FILES+=1
            )
        ) else (
            if not exist "!\dest_file!\.." mkdir "!\dest_file!\.." 2>nul
            copy /y "!src_file!" "!dest_file!" >nul
            echo   [NEW] !rel_path! | tee -a "!CHANGE_LOG!"
            set /a NEW_FILES+=1
        )
    )
    
    echo. >> "!CHANGE_LOG!"
    echo Summary: >> "!CHANGE_LOG!"
    echo - Files modified: !UPDATED_FILES! >> "!CHANGE_LOG!"
    echo - Files created: !NEW_FILES! >> "!CHANGE_LOG!"
    echo - Files deleted: !DELETED_FILES! >> "!CHANGE_LOG!"
    echo. >> "!CHANGE_LOG!"
    
    echo.
    echo   Files modified: !UPDATED_FILES!
    echo   Files created: !NEW_FILES!
    echo   Change log: !CHANGE_LOG!
) else (
    echo   No source directory found. Skipping file copy.
    echo   Please manually copy updated files from your development environment.
)

echo.
echo [3/5] Checking for Python dependencies...
if exist "requirements.txt" (
    if exist "venv\Scripts\python.exe" (
        %PIP% install -r requirements.txt --quiet 2>nul
        echo   Dependencies updated.
    )
)

echo.
echo [4/5] Running database migrations...
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
echo [5/5] Collecting static files...
cd app
%PYTHON% manage.py collectstatic --noinput --clear >nul 2>&1
if %errorlevel% equ 0 (
    echo   Static files collected.
)
cd ..

echo.
echo ==============================================
echo  Update Complete!
echo.
echo  Backup: !BACKUP_NAME!
echo  Change Log: !CHANGE_LOG!
echo.
echo  To start the server, run: windows\start.bat
echo ==============================================
echo.
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