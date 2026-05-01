@echo off
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PARENT_DIR=%SCRIPT_DIR%..
set DIST_DIR=%PARENT_DIR%
set SOURCE_DIR=%1

if "%SOURCE_DIR%"=="" set SOURCE_DIR=%PARENT_DIR%\..\..\printer_supplies

echo.
echo ===============================================
echo  SuppliesPro - Build Script (Windows)
echo ===============================================
echo.
echo Source: %SOURCE_DIR%
echo Destination: %DIST_DIR%
echo.

REM Verify source directory
if not exist "%SOURCE_DIR%" (
    echo [ERROR] Source directory not found: %SOURCE_DIR%
    echo Usage: %0 [source_directory]
    pause
    exit /b 1
)

REM Create folder structure
echo [1/4] Creating folder structure...
if not exist "%DIST_DIR%\app" mkdir "%DIST_DIR%\app"
if not exist "%DIST_DIR%\app\inventory" mkdir "%DIST_DIR%\app\inventory"
if not exist "%DIST_DIR%\app\rbac" mkdir "%DIST_DIR%\app\rbac"
if not exist "%DIST_DIR%\app\templates" mkdir "%DIST_DIR%\app\templates"
if not exist "%DIST_DIR%\app\static" mkdir "%DIST_DIR%\app\static"
if not exist "%DIST_DIR%\app\staticfiles" mkdir "%DIST_DIR%\app\staticfiles"
if not exist "%DIST_DIR%\linux" mkdir "%DIST_DIR%\linux"
if not exist "%DIST_DIR%\windows" mkdir "%DIST_DIR%\windows"
if not exist "%DIST_DIR%\backups" mkdir "%DIST_DIR%\backups"

REM Create change log
set BUILD_DATE=%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%%time:~3,2%
set BUILD_DATE=!BUILD_DATE: =0!
set CHANGE_LOG=%DIST_DIR%\build_!BUILD_DATE!_changelog.txt

echo =============================================== > "!CHANGE_LOG!"
echo Build: %date% %time% >> "!CHANGE_LOG!"
echo Source: %SOURCE_DIR% >> "!CHANGE_LOG!"
echo Destination: %DIST_DIR% >> "!CHANGE_LOG!"
echo =============================================== >> "!CHANGE_LOG!"
echo. >> "!CHANGE_LOG!"

echo [2/4] Copying Django application files...
set COPIED=0
set MODIFIED=0

REM Copy inventory app
if exist "%SOURCE_DIR%\inventory" (
    for /r "%SOURCE_DIR%\inventory" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=%DIST_DIR%\app\!rel_path!"
        
        REM Create directory if not exists
        for %%i in ("!dest_file!") do set "dest_dir=%%~dpi"
        if not exist "!dest_dir!" mkdir "!dest_dir!" 2>nul
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo [MODIFIED] !rel_path! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        ) else (
            copy /y "!src_file!" "!dest_file!" >nul
            echo [NEW] !rel_path! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        )
    )
)

REM Copy rbac app
if exist "%SOURCE_DIR%\rbac" (
    for /r "%SOURCE_DIR%\rbac" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=%DIST_DIR%\app\!rel_path!"
        
        for %%i in ("!dest_file!") do set "dest_dir=%%~dpi"
        if not exist "!dest_dir!" mkdir "!dest_dir!" 2>nul
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo [MODIFIED] !rel_path! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        ) else (
            copy /y "!src_file!" "!dest_file!" >nul
            echo [NEW] !rel_path! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        )
    )
)

REM Copy main Django files
for %%f in (manage.py settings.py urls.py wsgi.py asgi.py) do (
    if exist "%SOURCE_DIR%\%%f" (
        if exist "%DIST_DIR%\app\%%f" (
            fc "%SOURCE_DIR%\%%f" "%DIST_DIR%\app\%%f" >nul 2>&1
            if errorlevel 1 (
                copy /y "%SOURCE_DIR%\%%f" "%DIST_DIR%\app\%%f" >nul
                echo [MODIFIED] %%f >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        ) else (
            copy /y "%SOURCE_DIR%\%%f" "%DIST_DIR%\app\%%f" >nul
            echo [NEW] %%f >> "!CHANGE_LOG!"
            set /a COPIED+=1
        )
    )
)

echo [3/4] Copying templates and static files...

REM Copy templates
if exist "%SOURCE_DIR%\templates" (
    for /r "%SOURCE_DIR%\templates" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=%DIST_DIR%\app\!rel_path!"
        
        for %%i in ("!dest_file!") do set "dest_dir=%%~dpi"
        if not exist "!dest_dir!" mkdir "!dest_dir!" 2>nul
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo [MODIFIED] !rel_path! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        ) else (
            copy /y "!src_file!" "!dest_file!" >nul
            echo [NEW] !rel_path! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        )
    )
)

REM Copy static files
if exist "%SOURCE_DIR%\static" (
    for /r "%SOURCE_DIR%\static" %%f in (*) do (
        set "src_file=%%f"
        set "rel_path=!src_file:%SOURCE_DIR%\=!"
        set "dest_file=%DIST_DIR%\app\!rel_path!"
        
        for %%i in ("!dest_file!") do set "dest_dir=%%~dpi"
        if not exist "!dest_dir!" mkdir "!dest_dir!" 2>nul
        
        if exist "!dest_file!" (
            fc "!src_file!" "!dest_file!" >nul 2>&1
            if errorlevel 1 (
                copy /y "!src_file!" "!dest_file!" >nul
                echo [MODIFIED] !rel_path! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        ) else (
            copy /y "!src_file!" "!dest_file!" >nul
            echo [NEW] !rel_path! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        )
    )
)

echo [4/4] Creating requirements.txt...
if exist "%SOURCE_DIR%\requirements.txt" (
    copy /y "%SOURCE_DIR%\requirements.txt" "%DIST_DIR%\requirements.txt" >nul
) else (
    (
    echo Django>=4.2
    echo django-select2
    echo Pillow
    echo waitress
    echo django-widget-tweaks
    ) > "%DIST_DIR%\requirements.txt"
)

REM Create empty files if they don't exist
if not exist "%DIST_DIR%\CHANGELOG.txt" (
    echo SuppliesPro - Changelog > "%DIST_DIR%\CHANGELOG.txt"
    echo =============================================== >> "%DIST_DIR%\CHANGELOG.txt"
    echo. >> "%DIST_DIR%\CHANGELOG.txt"
    echo [NEW] CHANGELOG.txt >> "!CHANGE_LOG!"
    set /a COPIED+=1
)

REM Copy deployment scripts
if exist "%SOURCE_DIR%\dist\SuppliesPro\linux" (
    for %%f in ("%SOURCE_DIR%\dist\SuppliesPro\linux\*") do (
        set "filename=%%~nxf"
        if not exist "%DIST_DIR%\linux\!filename!" (
            copy /y "%%f" "%DIST_DIR%\linux\!filename!" >nul
            echo [NEW] linux\!filename! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        ) else (
            fc "%%f" "%DIST_DIR%\linux\!filename!" >nul 2>&1
            if errorlevel 1 (
                copy /y "%%f" "%DIST_DIR%\linux\!filename!" >nul
                echo [MODIFIED] linux\!filename! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        )
    )
)

if exist "%SOURCE_DIR%\dist\SuppliesPro\windows" (
    for %%f in ("%SOURCE_DIR%\dist\SuppliesPro\windows\*") do (
        set "filename=%%~nxf"
        if not exist "%DIST_DIR%\windows\!filename!" (
            copy /y "%%f" "%DIST_DIR%\windows\!filename!" >nul
            echo [NEW] windows\!filename! >> "!CHANGE_LOG!"
            set /a COPIED+=1
        ) else (
            fc "%%f" "%DIST_DIR%\windows\!filename!" >nul 2>&1
            if errorlevel 1 (
                copy /y "%%f" "%DIST_DIR%\windows\!filename!" >nul
                echo [MODIFIED] windows\!filename! >> "!CHANGE_LOG!"
                set /a MODIFIED+=1
            )
        )
    )
)

REM Summary
echo. >> "!CHANGE_LOG!"
echo Summary: >> "!CHANGE_LOG!"
echo - Files copied: !COPIED! >> "!CHANGE_LOG!"
echo - Files modified: !MODIFIED! >> "!CHANGE_LOG!"
echo - Build date: !BUILD_DATE! >> "!CHANGE_LOG!"
echo. >> "!CHANGE_LOG!"

echo.
echo ===============================================
echo  Build Complete!
echo ===============================================
echo.
echo  Files copied: !COPIED!
echo  Files modified: !MODIFIED!
echo  Changelog: !CHANGE_LOG!
echo.
echo  Deployment package ready at: %DIST_DIR%
echo ===============================================
echo.
pause
