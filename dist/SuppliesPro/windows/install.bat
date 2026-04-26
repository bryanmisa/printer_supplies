@echo off
cd /d "%~dp0..\app"

REM Check if venv exists
if exist "..\venv\Scripts\python.exe" (
    set PYTHON=..\venv\Scripts\python.exe
    set PIP=..\venv\Scripts\pip.exe
    echo Using virtual environment...
) else (
    echo Creating virtual environment...
    python -m venv ..\venv
    set PYTHON=..\venv\Scripts\python.exe
    set PIP=..\venv\Scripts\pip.exe
)

echo.
echo ============================================
echo  SuppliesPro - Install Dependencies (Windows)
echo ============================================
echo.

echo Installing Python dependencies...
%PIP% install -r ..\requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed. Make sure Python is installed and added to PATH.
    echo Download Python at: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.
echo ============================================
echo Dependencies installed successfully!
echo.
echo Next steps:
echo   1. Run: windows\setup.bat
echo   2. Run: windows\start.bat
echo ============================================
echo.
pause