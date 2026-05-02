==============================================
           SuppliesPro Portable
         Printer Supply Management
==============================================

QUICK START - CHOOSE YOUR PLATFORM
===================================

WINDOWS USERS:
============
1. Open the windows/ folder
2. Run install.bat
3. Run start.bat or run_production.bat
4. Open http://localhost:8080
5. Login: admin / admin123

LINUX/MAC USERS:
==============
1. Open the linux/ folder
2. Run: chmod +x *.sh
3. Run: ./install.sh
4. Run: ./start.sh or ./run_production.sh
5. Open http://localhost:8080
7. Login: admin / admin123

FILES INCLUDED
=============
windows/   - Windows scripts (.bat)
linux/     - Linux/Mac scripts (.sh)
app/       - Django application
backups/   - Database backup storage
CHANGELOG.txt - Update history
credentials.txt - Default login info
README.txt  - This file (main)
requirements.txt - Python dependencies

SCRIPTS OVERVIEW
================

INSTALLATION
-----------
install.bat / install.sh
  - Creates virtual environment (venv)
  - Installs Python dependencies
  - Run once before first use

SETUP
-----
setup.bat / setup.sh
  - Creates database
  - Runs migrations
  - Creates admin account
  - Only needed once

START (Development)
-------------------
start.bat / start.sh
  - Uses Django development server
  - Auto-reloads on code changes
  - Good for development

RUN_PRODUCTION (Production)
-------------------------
run_production.bat / run_production.sh
  - Uses Waitress WSGI server
  - No auto-reload (faster)
  - Initializes database if not exists
  - Shows server in console
  - Press Ctrl+C to stop

UPDATE
------
update.bat / update.sh
  - Automatic backup before update
  - Runs pending migrations
  - Records in CHANGELOG.txt
  - Auto-restores on failure

STOPPING THE SERVER
==================
Press Ctrl+C in the command window to stop the server.
Closing the window will also stop the server.

DEFAULT LOGIN
=============
Username: admin
Password: admin123

Change the default password after first login!

FULL DOCUMENTATION
================
See README.txt in each platform folder:
- windows/README.txt for Windows detailed guide
- linux/README.txt for Linux/Mac detailed guide

==============================================
     For support, contact administrator
==============================================