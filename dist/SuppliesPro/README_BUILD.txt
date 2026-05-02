# SuppliesPro - Build & Deployment Guide

## Folder Structure

After building, the deployment package will have this structure:

```
SuppliesPro/
├── app/
│   ├── inventory/          # Main application
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── ...
│   ├── rbac/               # Role-based access control
│   │   ├── migrations/
│   │   └── ...
│   ├── templates/          # Global templates
│   ├── static/             # Static files (CSS, JS, images)
│   ├── staticfiles/        # Collected static files
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── manage.py
│   └── db.sqlite3         # Database (after setup)
├── linux/
│   ├── build.sh           # Build/update deployment package
│   ├── setup.sh          # Initial setup script
│   ├── start.sh          # Start production server
│   ├── update.sh         # Update existing installation
│   └── run_production.sh # Run in production mode
├── windows/
│   ├── build.bat          # Build/update deployment package
│   ├── setup.bat          # Initial setup script
│   ├── start.bat          # Start production server
│   ├── update.bat         # Update existing installation
│   └── run_production.bat # Run in production mode
├── backups/              # Database backups
├── requirements.txt      # Python dependencies
├── CHANGELOG.txt        # Update history
└── README.txt           # This file
```

## Building the Deployment Package

### Linux/Mac
```bash
cd dist/SuppliesPro/linux
./build.sh [source_directory]
```

**Arguments:**
- `source_directory` (optional): Path to source code. Defaults to `../../printer_supplies`

**Example:**
```bash
./build.sh /home/bryan/projects/printer_supplies
```

### Windows
```cmd
cd dist\SuppliesPro\windows
build.bat [source_directory]
```

**Arguments:**
- `source_directory` (optional): Path to source code. Defaults to `..\..\printer_supplies`

**Example:**
```cmd
build.bat C:\projects\printer_supplies
```

## What the Build Script Does

1. **Creates folder structure** - Ensures all required directories exist
2. **Copies updated files** - Django app, templates, static files
3. **Detects modifications** - Only updates files that have changed
4. **Creates changelog** - `build_[date]_changelog.txt` with:
   - `[NEW]` - New files that were added
   - `[MODIFIED]` - Files that were updated
5. **Preserves deployment scripts** - Doesn't overwrite existing linux/windows scripts
6. **Creates requirements.txt** - If not present

## Initial Setup (First Time)

### Linux/Mac (Development)
```bash
cd SuppliesPro/linux
./start.sh
```

### Windows (Development)
```cmd
cd SuppliesPro\windows
start.bat
```

### Linux/Mac (Production - Waitress)
```bash
cd SuppliesPro/linux
./start.sh
```
Server accessible from: `http://0.0.0.0:8080` (other computers can access)

### Windows (Production - Waitress)
```cmd
cd SuppliesPro\windows
start.bat
```
Server accessible from: `http://0.0.0.0:8080` (other computers can access)

## Running as a Service (Auto-Start on Boot)

### Linux - systemd Service (Recommended)
```bash
cd SuppliesPro/linux
sudo ./install_service.sh
```

This will:
1. Install SuppliesPro as a systemd service
2. Start the service automatically on boot
3. Keep the server running after logout
4. Auto-restart on crash (10 second delay)

**Service commands:**
```bash
sudo systemctl start suppliespro      # Start service
sudo systemctl stop suppliespro       # Stop service
sudo systemctl restart suppliespro   # Restart service
sudo systemctl status suppliespro    # Check status
sudo journalctl -u suppliespro -f  # View logs
sudo systemctl disable suppliespro   # Disable auto-start
```

### Linux - Cron @reboot (Alternative)
Add to crontab (`crontab -e`):
```
@reboot /path/to/SuppliesPro/linux/startup.sh
```

### Windows - NSSM Service (Recommended)
1. Download NSSM (Non-Sucking Service Manager): https://nssm.cc/download
2. Install service:
```cmd
cd SuppliesPro\windows
runas /user:Administrator install_service.bat
```

### Windows - Task Scheduler (Alternative)
The `install_service.bat` will automatically:
1. Create a scheduled task that runs on system startup
2. Add a shortcut to the Startup folder for user login
3. Start the server immediately

**Task commands:**
```cmd
schtasks /run /tn "SuppliesPro"     # Start task
schtasks /end /tn "SuppliesPro"     # Stop task
schtasks /delete /tn "SuppliesPro" /f  # Delete task
```

## Updating Existing Installation

### Linux/Mac
```bash
cd SuppliesPro/linux
./setup.sh
```
This will:
1. Create virtual environment
2. Install dependencies (including Waitress)
3. Create database with migrations
4. Create admin user

### Windows
```cmd
cd SuppliesPro\windows
setup.bat
```
This will:
1. Create virtual environment
2. Install dependencies (including Waitress)
3. Create database with migrations
4. Create admin user

The update script will:
1. Backup the database
2. Copy updated files from source
3. Log all changes to `update_[date]_changelog.txt`
4. Update Python dependencies
5. Run database migrations
6. Collect static files

## Change Logs

After each build/update, a changelog file is created:
- Build: `build_[date]_changelog.txt`
- Update: `update_[date]_changelog.txt`

These files contain:
- List of new files (`[NEW]`)
- List of modified files (`[MODIFIED]`)
- Summary with file counts

## Notes

- The build script preserves existing deployment scripts in `linux/` and `windows/`
- Database file (`db.sqlite3`) is NOT copied - use setup.sh for fresh install
- Static files are collected during update using Django's `collectstatic`
- Virtual environment (`venv/`) is created during setup, not copied
