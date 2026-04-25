@echo off
cd /d "%~dp0app"
echo Installing Python dependencies...
echo.
pip install -r requirements.txt
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
echo   1. Run setup.bat to initialize the database
echo   2. Run start.bat to launch the application
echo ============================================
echo.
pause