@echo off
cd /d "%~dp0..\app"

REM Check if venv exists
if exist "..\venv\Scripts\python.exe" (
    set PYTHON=..\venv\Scripts\python.exe
) else (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  SuppliesPro - Database Setup (Windows)
echo ===============================================
echo.

REM Check if database already exists
if exist "db.sqlite3" (
    echo Database already exists. Skipping initialization.
    echo.
    echo Run: windows\start.bat
    pause
    exit /b 0
)

REM Run migrations
echo Running migrations...
%PYTHON% manage.py migrate --noinput
if errorlevel 1 (
    echo.
    echo [ERROR] Migration failed. Run install.bat first.
    pause
    exit /b 1
)

REM Create admin superuser with correct role
echo.
echo Creating administrator account...
%PYTHON% manage.py create_admin
if errorlevel 1 (
    echo.
    echo [WARNING] Admin creation had issues. You can create one manually:
    echo   %PYTHON% manage.py shell
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
echo Run: windows\start.bat
pause