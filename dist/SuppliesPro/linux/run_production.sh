#!/bin/bash
# SuppliesPro - Run Production Server for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Use virtual environment if it exists
if [ -f "$PARENT_DIR/venv/bin/python3" ]; then
    PYTHON="$PARENT_DIR/venv/bin/python3"
    PIP="$PARENT_DIR/venv/bin/pip"
else
    echo "[ERROR] Virtual environment not found. Run install.sh first."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Installing Waitress for production server..."
$PIP install waitress --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Waitress installation failed."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if database exists, if not create it
cd "$PARENT_DIR/app"
if [ ! -f "db.sqlite3" ]; then
    echo
    echo "Creating new database..."
    $PYTHON manage.py migrate --noinput
    $PYTHON manage.py create_admin
fi

echo
echo "==============================================="
echo "  SuppliesPro - Production Server"
echo "==============================================="
echo "  URL: http://localhost:8080"
echo
echo "  Press Ctrl+C to stop the server"
echo "==============================================="
echo
cd "$PARENT_DIR/app"
python3 -c "
import sys
import os
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printer_supplies.settings')
from waitress import serve
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
serve(application, host='0.0.0.0', port=8080)
"