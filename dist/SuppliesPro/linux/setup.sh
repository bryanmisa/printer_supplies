#!/bin/bash
# SuppliesPro - Portable Setup Script for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR/app"

# Use virtual environment if it exists
if [ -f "../venv/bin/python3" ]; then
    PYTHON="../venv/bin/python3"
    PIP="../venv/bin/pip"
else
    PYTHON="python3"
    PIP="pip3"
fi

echo "==============================================="
echo "  SuppliesPro - Database Setup"
echo "==============================================="
echo

# Check if database already exists
if [ -f "db.sqlite3" ]; then
    echo "Database already exists. Skipping initialization."
    echo
    echo "Run: ./linux/start.sh"
    read -p "Press Enter to exit..."
    exit 0
fi

# Run migrations
echo "Running migrations..."
$PYTHON manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "[ERROR] Migration failed. Run install.sh first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Create admin account
echo
echo "Creating administrator account..."
$PYTHON manage.py create_admin
if [ $? -ne 0 ]; then
    echo "[WARNING] Admin creation had issues."
fi

echo
echo "==============================================="
echo "  Database initialized successfully!"
echo
echo "  Default Administrator Account:"
echo "    Username: admin"
echo "    Password: admin123"
echo "    Role: Administrator"
echo
echo "  URL: http://localhost:8080"
echo "==============================================="
echo
echo "Run: ./linux/start.sh"
read -p "Press Enter to exit..."