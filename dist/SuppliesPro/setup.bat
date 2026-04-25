@echo off
cd /d "%~dp0app"
echo Initializing database...
echo.

REM Check if database already exists
if exist "db.sqlite3" (
    echo Database already exists. Skipping initialization.
    echo.
    echo Run start.bat to launch the application.
    pause
    exit /b 0
)

REM Run migrations
python manage.py migrate --noinput
if errorlevel 1 (
    echo.
    echo [ERROR] Migration failed. Run install.bat first.
    pause
    exit /b 1
)

REM Create admin superuser
echo.
echo Creating administrator account...
python manage.py shell -c "from inventory.models import User; User.objects.filter(username='admin').delete() if User.objects.filter(username='admin').exists() else None; User.objects.create_superuser('admin', 'admin@localhost.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" 2>nul || (
    echo Superuser creation skipped.
)

echo.
echo ===============================================
echo Database initialized successfully!
echo.
echo Default Administrator Account:
echo   Username: admin
echo   Password: admin123
echo.
echo URL: http://localhost:8080
echo ===============================================
echo.
echo Run start.bat to launch the application.
pause