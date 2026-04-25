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

REM Create admin superuser with correct role
echo.
echo Creating administrator account...
python manage.py create_admin
if errorlevel 1 (
    echo.
    echo [WARNING] Admin creation had issues. You can create one manually:
    echo   python manage.py shell
    echo   from inventory.models import User
    echo   User.objects.create_superuser('admin', 'admin@localhost.com', 'admin123', role='admin')
)

echo.
echo ===============================================
echo Database initialized successfully!
echo.
echo Default Administrator Account:
echo   Username: admin
echo   Password: admin123
echo   Role: Administrator
echo.
echo URL: http://localhost:8080
echo ===============================================
echo.
echo Run start.bat to launch the application.
pause