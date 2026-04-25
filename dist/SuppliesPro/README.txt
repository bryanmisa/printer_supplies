===============================================
           SuppliesPro Portable
         Printer Supply Management
===============================================

REQUIREMENTS
- Windows 10/11
- Python 3.10 or higher
  Download: https://www.python.org/downloads/
- Internet connection (for first installation)

QUICK START
==========
1. Run install.bat
   - Installs Python dependencies
   - Requires internet connection

2. Run setup.bat
   - Creates database
   - Runs migrations
   - Creates admin account

3. Run start.bat
   - Launches server at http://localhost:8080
   - Opens browser automatically

SERVER OPTIONS
============
start.bat (Development)
  - Uses Django development server
  - Auto-reloads on code changes
  - Debug mode enabled
  - Good for testing

run_production.bat (Production)
  - Uses Gunicorn WSGI server
  - Better performance
  - Recommended for multi-user environments

DEFAULT LOGIN
============
Username: admin
Password: admin123

Change the default password after first login!
(Go to Administration > Users > Edit > Change Password)

STOPPING THE SERVER
==================
Press Ctrl+C in the command window to stop the server.
Closing the window will also stop the server.

TROUBLESHOOTING
===============
Error "python is not recognized":
  - Install Python from python.org/downloads/
  - Add Python to system PATH
  - Restart command prompt

Error "pip is not recognized":
  - Reinstall Python
  - Check "Add Python to PATH" option during install

Error "port already in use":
  - Stop other applications using port 8080
  - Or change port in batch files (replace 8080 with 8081)

Database locked error:
  - Make sure server is stopped
  - Close other database connections

Installation timeout:
  - Check internet connection
  - Run install.bat again

FEATURES
=======
- Track printer supplies and stock levels
- Manage printers with IP addresses
- Install/dispose supplies on printers
- Record deliveries and update inventory
- View reports and analytics
- User management with roles
- Database backup and restore

DATA BACKUP
==========
Log in as admin and navigate to:
  Administration > Database Backup

Options:
  - Create New Backup - Save current database
  - Download - Save backup to your computer
  - Restore - Replace database with backup
  - Delete - Remove old backup files

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
  - View reports

Staff
  - View-only access
  - Cannot modify data

FILES
=====
start.bat              - Launch application (dev mode)
run_production.bat     - Launch application (prod mode)
install.bat           - Install dependencies
setup.bat            - Initialize database
credentials.txt      - Default login info
README.txt           - This file
backups/            - Database backup storage
app/
  manage.py         - Django management
  db.sqlite3        - Application database
  printer_supplies/ - Project settings
  inventory/        - Main application
  rbac/            - Access control
  templates/       - HTML templates
  static/          - CSS and JavaScript

UPDATING
========
1. Stop the server (Ctrl+C)
2. Backup your database (Admin > Database Backup)
3. Replace app/ folder with new version
4. Run setup.bat to apply migrations
5. Run start.bat

SECURITY
========
- Change default admin password
- Use HTTPS in production (configure web server)
- Keep backups in a safe location
- Regularly create backups

===============================================
         For support, contact admin
===============================================