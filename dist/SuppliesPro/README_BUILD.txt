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

### Linux/Mac
```bash
cd SuppliesPro/linux
./setup.sh
```

### Windows
```cmd
cd SuppliesPro\windows
setup.bat
```

## Starting the Server

### Linux/Mac
```bash
cd SuppliesPro/linux
./start.sh
```

### Windows
```cmd
cd SuppliesPro\windows
start.bat
```

Server will be available at: `http://127.0.0.1:8080`

## Updating Existing Installation

### Linux/Mac
```bash
cd SuppliesPro/linux
./update.sh
```

### Windows
```cmd
cd SuppliesPro\windows
update.bat
```

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
