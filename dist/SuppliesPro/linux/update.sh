#!/bin/bash
# SuppliesPro - Update Script for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

# Use virtual environment if it exists
if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
    PIP="venv/bin/pip"
else
    PYTHON="python3"
    PIP="pip3"
fi

echo
echo "==============================================="
echo "  SuppliesPro - Update Script (Linux/Mac)"
echo "==============================================="
echo

# Check if database exists
if [ ! -f "app/db.sqlite3" ]; then
    echo "[ERROR] No database found. Run setup.sh first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if server is running
if lsof -i :8080 >/dev/null 2>&1; then
    echo "[WARNING] Server appears to be running on port 8080."
    echo
    echo "To stop the server, press Ctrl+C in the server window."
    echo
    read -p "Continue anyway? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        exit 0
    fi
fi

echo
echo "[1/4] Creating database backup..."
if [ ! -d "backups" ]; then
    mkdir backups
fi

BACKUP_DATE=$(date +"%Y-%m-%d_%H%M")
BACKUP_NAME="backup_pre_update_${BACKUP_DATE}.sqlite3"
cp app/db.sqlite3 "backups/$BACKUP_NAME"

if [ -f "backups/$BACKUP_NAME" ]; then
    echo "  Backup created: backups/$BACKUP_NAME"
else
    echo "[ERROR] Failed to create backup."
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "[2/4] Checking for Python dependencies..."
if [ -f "requirements.txt" ] && [ -f "venv/bin/python3" ]; then
    echo "  Dependencies OK."
fi

echo
echo "[3/4] Running database migrations..."
cd app
$PYTHON manage.py migrate --plan 2>/dev/null
if [ $? -eq 0 ]; then
    MIGRATIONS=$($PYTHON manage.py migrate --plan 2>/dev/null)
    if [ -z "$MIGRATIONS" ]; then
        echo "  No pending migrations found."
    else
        echo "  Applying migrations..."
        $PYTHON manage.py migrate --noinput
        if [ $? -ne 0 ]; then
            echo
            echo "[ERROR] Migration failed. Restoring backup..."
            cd ..
            cp "backups/$BACKUP_NAME" app/db.sqlite3
            echo "  Backup restored."
            read -p "Press Enter to exit..."
            exit 1
        fi
    fi
fi
cd ..

echo
echo "[4/4] Recording update in CHANGELOG.txt..."
{
echo "==============================================="
echo "Update: $(date)"
echo "==============================================="
echo "- Database backed up: $BACKUP_NAME"
echo "- Migrations applied"
echo
} >> CHANGELOG.txt

echo
echo "==============================================="
echo "  Update Complete!"
echo
echo "  Backup: $BACKUP_NAME"
echo
echo "  To start the server, run: ./linux/start.sh"
echo "==============================================="
echo
read -p "Press Enter to exit..."