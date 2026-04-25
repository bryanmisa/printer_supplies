@echo off
cd /d "%~dp0app"
echo Starting SuppliesPro on http://localhost:8080
echo.
echo Opening browser...
start http://localhost:8080
python manage.py runserver 0.0.0.0:8080