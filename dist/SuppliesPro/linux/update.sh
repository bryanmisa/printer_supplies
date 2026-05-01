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

# Check if source directory exists for file copying
SOURCE_DIR=""
if [ -d "$PARENT_DIR/../../SuppliesPro" ]; then
    SOURCE_DIR="$PARENT_DIR/../../SuppliesPro"
elif [ -d "/home/bryan/projects/SuppliesPro" ]; then
    SOURCE_DIR="/home/bryan/projects/SuppliesPro"
fi

echo
echo "[1/5] Creating database backup..."
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
echo "[2/5] Checking for file updates..."
CHANGE_LOG="update_${BACKUP_DATE}_changelog.txt"
touch "$CHANGE_LOG"

if [ -n "$SOURCE_DIR" ] && [ -d "$SOURCE_DIR" ]; then
    echo "  Source directory found: $SOURCE_DIR"
    echo "  Comparing and copying updated files..."
    echo
    echo "===============================================" >> "$CHANGE_LOG"
    echo "Update: $(date)" >> "$CHANGE_LOG"
    echo "===============================================" >> "$CHANGE_LOG"
    echo >> "$CHANGE_LOG"
    
    # Copy updated files and log changes
    UPDATED_FILES=0
    NEW_FILES=0
    DELETED_FILES=0
    
    # Copy app files
    for src_file in $(find "$SOURCE_DIR/app" -type f 2>/dev/null); do
        rel_path="${src_file#$SOURCE_DIR/}"
        dest_file="app/${rel_path#app/}"
        
        if [ -f "$dest_file" ]; then
            # Check if file is different
            if ! cmp -s "$src_file" "$dest_file"; then
                cp "$src_file" "$dest_file"
                echo "  [MODIFIED] $rel_path" | tee -a "$CHANGE_LOG"
                ((UPDATED_FILES++))
            fi
        else
            # New file
            mkdir -p "$(dirname "$dest_file")"
            cp "$src_file" "$dest_file"
            echo "  [NEW] $rel_path" | tee -a "$CHANGE_LOG"
            ((NEW_FILES++))
        fi
    done
    
    # Copy static files
    for src_file in $(find "$SOURCE_DIR/static" -type f 2>/dev/null); do
        rel_path="${src_file#$SOURCE_DIR/}"
        dest_file="app/static/${rel_path#static/}"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$src_file" "$dest_file"; then
                cp "$src_file" "$dest_file"
                echo "  [MODIFIED] $rel_path" | tee -a "$CHANGE_LOG"
                ((UPDATED_FILES++))
            fi
        else
            mkdir -p "$(dirname "$dest_file")"
            cp "$src_file" "$dest_file"
            echo "  [NEW] $rel_path" | tee -a "$CHANGE_LOG"
            ((NEW_FILES++))
        fi
    done
    
    # Copy template files
    for src_file in $(find "$SOURCE_DIR/templates" -type f 2>/dev/null); do
        rel_path="${src_file#$SOURCE_DIR/}"
        dest_file="app/templates/${rel_path#templates/}"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$src_file" "$dest_file"; then
                cp "$src_file" "$dest_file"
                echo "  [MODIFIED] $rel_path" | tee -a "$CHANGE_LOG"
                ((UPDATED_FILES++))
            fi
        else
            mkdir -p "$(dirname "$dest_file")"
            cp "$src_file" "$dest_file"
            echo "  [NEW] $rel_path" | tee -a "$CHANGE_LOG"
            ((NEW_FILES++))
        fi
    done
    
    echo >> "$CHANGE_LOG"
    echo "Summary:" >> "$CHANGE_LOG"
    echo "- Files modified: $UPDATED_FILES" >> "$CHANGE_LOG"
    echo "- Files created: $NEW_FILES" >> "$CHANGE_LOG"
    echo "- Files deleted: $DELETED_FILES" >> "$CHANGE_LOG"
    echo >> "$CHANGE_LOG"
    
    echo
    echo "  Files modified: $UPDATED_FILES"
    echo "  Files created: $NEW_FILES"
    echo "  Change log: $CHANGE_LOG"
else
    echo "  No source directory found. Skipping file copy."
    echo "  Please manually copy updated files from your development environment."
fi

echo
echo "[3/5] Checking for Python dependencies..."
if [ -f "requirements.txt" ] && [ -f "venv/bin/python3" ]; then
    $PIP install -r requirements.txt --quiet 2>/dev/null
    echo "  Dependencies updated."
fi

echo
echo "[4/5] Running database migrations..."
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
echo "[5/5] Collecting static files..."
cd app
$PYTHON manage.py collectstatic --noinput --clear >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  Static files collected."
fi
cd ..

echo
echo "==============================================="
echo "  Update Complete!"
echo
echo "  Backup: $BACKUP_NAME"
echo "  Change Log: $CHANGE_LOG"
echo
echo "  To start the server, run: ./linux/start.sh"
echo "==============================================="
echo
read -p "Press Enter to exit..."