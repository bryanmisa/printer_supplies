==============================================
           SuppliesPro Portable
         Printer Supply Management
           FOR LINUX / MAC
==============================================

REQUIREMENTS
==========
- Linux (Ubuntu, Debian, Fedora, etc.) or Mac
- Python 3.10 or higher (auto-installed in venv)
- Internet connection (for first installation)

QUICK START
==========
1. Open terminal in linux/ folder
2. Make scripts executable:
   chmod +x *.sh
3. Run install.sh:
   ./install.sh
4. Run start.sh (development) OR run_production.sh (production):
   ./start.sh
   OR
   ./run_production.sh
5. Open http://localhost:8080
6. Login: admin / admin123

SCRIPTS
=======
install.sh
  - Creates venv/ folder with Python virtual environment
  - Installs all dependencies from requirements.txt
  - Run once before first use
  - Can be run again to update dependencies

setup.sh
  - Creates database (db.sqlite3)
  - Runs migrations
  - Creates admin account
  - Only needed once (or if database is missing)

start.sh
  - Uses Django development server
  - Auto-reloads when code changes
  - Good for development/testing

run_production.sh
  - Uses Waitress WSGI server (production-ready)
  - Initializes database if not exists
  - Runs in same terminal window (see requests)
  - Press Ctrl+C to stop
  - Faster than start.sh

update.sh
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
Press Ctrl+C in the terminal to stop the server.

TROUBLESHOOTING
==============
Virtual environment not found:
  - Run install.sh first

python3: command not found:
  - Ubuntu/Debian: sudo apt install python3 python3-venv
  - Fedora: sudo yum install python3 python3-venv
  - Mac: brew install python3

Permission denied:
  - chmod +x *.sh

Port already in use:
  - Stop other applications using port 8080
  - Or edit the .sh files to use port 8081

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
├── linux/
│   ├── README.txt         - This file
│   ├── install.sh         - Install dependencies
│   ├── setup.sh          - Initialize database
│   ├── start.sh          - Run development server
│   ├── run_production.sh - Run production server
│   └── update.sh        - Update script
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
3. Run start.sh or run_production.sh

CODE + DATABASE UPDATE (New Fields)
--------------------------------
1. Run update.sh (automatic)
   OR manually:
   - Backup db: cp app/db.sqlite3 backups/
   - Copy new migration files to app/
   - Run setup.sh

ROLLBACK
========
If update fails:
1. Stop the server
2. Find backup in backups/ folder
3. Copy backup to app/db.sqlite3
4. Run start.sh or run_production.sh

SECURITY
========
- Change default admin password
- Use HTTPS in production
- Keep backups in safe location

==============================================
     For support, contact administrator
==============================================