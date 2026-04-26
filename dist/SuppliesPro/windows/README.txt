==============================================
           SuppliesPro Portable
         Printer Supply Management
              FOR WINDOWS
==============================================

REQUIREMENTS
==========
- Windows 10/11
- Python 3.10 or higher (auto-installed in venv)
- Internet connection (for first installation)

QUICK START
==========
1. Run install.bat
   - Creates virtual environment
   - Installs Python dependencies

2. Run start.bat (development) OR run_production.bat (production)
   - Creates database if not exists
   - Launches server at http://localhost:8080

3. Open http://localhost:8080
4. Login: admin / admin123

SCRIPTS
=======
install.bat
  - Creates venv\ folder with Python virtual environment
  - Installs all dependencies from requirements.txt
  - Run once before first use
  - Can be run again to update dependencies

setup.bat
  - Creates database (db.sqlite3)
  - Runs migrations
  - Creates admin account
  - Only needed once (or if database is missing)

start.bat
  - Uses Django development server
  - Auto-reloads when code changes
  - Good for development/testing

run_production.bat
  - Uses Waitress WSGI server (production-ready)
  - Initializes database if not exists
  - Runs in same console window (see requests)
  - Press Ctrl+C to stop
  - Faster than start.bat

update.bat
  - Creates automatic backup in backups/ folder
  - Runs any pending migrations
  - Records update in CHANGELOG.txt
  - Auto-restores if migration fails

DEFAULT LOGIN
===========
Username: admin
Password: admin123

Change the default password after first login!

STOPPING THE SERVER
==================
Press Ctrl+C in the command window to stop the server.

TROUBLESHOOTING
==============
Virtual environment not found:
  - Run install.bat first

Python not recognized:
  - Restart command prompt after installing Python

Port already in use:
  - Stop other applications using port 8080
  - Or edit the .bat files to use port 8081

FEATURES
========
- Track printer supplies and stock levels
- Manage printers with IP addresses
- Install/dispose supplies on printers
- Record deliveries and update inventory
- View reports and analytics
- User management with roles
- Database backup and restore
- Collapsible sidebar menu sections
- Reports: inventory, replenishment, consumption

USER ROLES
==========
Admin
  - Full access to all features
  - Manage users
  - Database backup
  - Audit trail

Manager
  - Manage supplies and printers
  - Record deliveries
  - Install/dispose supplies

Staff
  - View-only access
  - Cannot modify data

FILE STRUCTURE
============
SuppliesPro/
├── windows/
│   ├── README.txt         - This file
│   ├── install.bat        - Install dependencies
│   ├── setup.bat         - Initialize database
│   ├── start.bat         - Run development server
│   ├── run_production.bat - Run production server
│   └── update.bat       - Update script
├── app/
│   ├── manage.py
│   ├── db.sqlite3       - Database (created on first run)
│   ├── printer_supplies/
│   ├── inventory/       - Main application
│   ├── templates/
│   └── static/
├── backups/             - Database backups
├── CHANGELOG.txt       - Update history
├── credentials.txt     - Default login info
└── requirements.txt    - Python dependencies

UPDATING
========

QUICK UPDATE (No Database Changes)
--------------------------------
For CSS, template, or bug fixes:
1. Stop the server
2. Replace modified files in app/ folder
3. Run start.bat or run_production.bat

CODE + DATABASE UPDATE (New Fields)
-----------------------------------
1. Run update.bat (automatic)
   OR manually:
   - Backup db: copy app\db.sqlite3 backups\
   - Copy new migration files to app\
   - Run setup.bat

ROLLBACK
=========
If update fails:
1. Stop the server
2. Find backup in backups/ folder
3. Copy backup to app\db.sqlite3
4. Run start.bat or run_production.bat

SECURITY
========
- Change default admin password
- Use HTTPS in production
- Keep backups in safe location

==============================================
     For support, contact administrator
==============================================