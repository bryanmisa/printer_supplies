#!/bin/bash
# SuppliesPro - Start Production Server for Linux/Mac
# Uses Waitress WSGI server for production

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

# Collect static files
echo "Collecting static files..."
$PYTHON manage.py collectstatic --noinput --clear >/dev/null 2>&1

echo
echo "============================================="
echo "  SuppliesPro - Production Server (Waitress)"
echo "============================================="
echo "  URL: http://0.0.0.0:8080"
echo
echo "  Press Ctrl+C to stop the server"
echo "============================================="
echo

# Run with Waitress (0.0.0.0 makes it accessible from other computers)
$PYTHON -m waitress --host=0.0.0.0 --port=8080 wsgi:application