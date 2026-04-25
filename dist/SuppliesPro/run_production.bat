@echo off
cd /d "%~dp0app"
echo Installing Gunicorn for production server...
pip install gunicorn
if errorlevel 1 (
    echo.
    echo [ERROR] Gunicorn installation failed.
    pause
    exit /b 1
)
echo.
echo Starting SuppliesPro Production Server on http://0.0.0.0:8080
echo.
echo Press Ctrl+C to stop the server.
echo.
gunicorn printer_supplies.wsgi:application --bind 0.0.0.0:8080 --workers 4 --timeout 120