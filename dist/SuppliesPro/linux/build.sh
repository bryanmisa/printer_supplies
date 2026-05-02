#!/bin/bash
# SuppliesPro - Build Script for Linux/Mac
# This script creates/updates the deployment package in dist/SuppliesPro

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PARENT_DIR"
SOURCE_DIR="${1:-$PARENT_DIR/../../printer_supplies}"

echo "==============================================="
echo "  SuppliesPro - Build Script (Linux/Mac)"
echo "==============================================="
echo
echo "Source: $SOURCE_DIR"
echo "Destination: $DIST_DIR"
echo

# Verify source directory
if [ ! -d "$SOURCE_DIR" ]; then
    echo "[ERROR] Source directory not found: $SOURCE_DIR"
    echo "Usage: $0 [source_directory]"
    exit 1
fi

# Create folder structure
echo "[1/4] Creating folder structure..."
mkdir -p "$DIST_DIR/app"
mkdir -p "$DIST_DIR/app/inventory"
mkdir -p "$DIST_DIR/app/rbac"
mkdir -p "$DIST_DIR/app/templates"
mkdir -p "$DIST_DIR/app/static"
mkdir -p "$DIST_DIR/app/staticfiles"
mkdir -p "$DIST_DIR/linux"
mkdir -p "$DIST_DIR/windows"
mkdir -p "$DIST_DIR/backups"

# Create change log
BUILD_DATE=$(date +"%Y-%m-%d_%H%M")
CHANGE_LOG="$DIST_DIR/build_${BUILD_DATE}_changelog.txt"

{
echo "==============================================="
echo "Build: $(date)"
echo "Source: $SOURCE_DIR"
echo "Destination: $DIST_DIR"
echo "==============================================="
echo
} > "$CHANGE_LOG"

echo "[2/4] Copying Django application files..."
COPIED=0
MODIFIED=0

# Copy inventory app
if [ -d "$SOURCE_DIR/inventory" ]; then
    for file in $(find "$SOURCE_DIR/inventory" -type f 2>/dev/null); do
        rel_path="${file#$SOURCE_DIR/}"
        dest_file="$DIST_DIR/app/$rel_path"
        mkdir -p "$(dirname "$dest_file")"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$file" "$dest_file"; then
                cp "$file" "$dest_file"
                echo "[MODIFIED] $rel_path" >> "$CHANGE_LOG"
                ((MODIFIED++))
            fi
        else
            cp "$file" "$dest_file"
            echo "[NEW] $rel_path" >> "$CHANGE_LOG"
            ((COPIED++))
        fi
    done
fi

# Copy rbac app
if [ -d "$SOURCE_DIR/rbac" ]; then
    for file in $(find "$SOURCE_DIR/rbac" -type f 2>/dev/null); do
        rel_path="${file#$SOURCE_DIR/}"
        dest_file="$DIST_DIR/app/$rel_path"
        mkdir -p "$(dirname "$dest_file")"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$file" "$dest_file"; then
                cp "$file" "$dest_file"
                echo "[MODIFIED] $rel_path" >> "$CHANGE_LOG"
                ((MODIFIED++))
            fi
        else
            cp "$file" "$dest_file"
            echo "[NEW] $rel_path" >> "$CHANGE_LOG"
            ((COPIED++))
        fi
    done
fi

# Copy main Django files
for file in manage.py settings.py urls.py wsgi.py asgi.py; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        dest_file="$DIST_DIR/app/$file"
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$SOURCE_DIR/$file" "$dest_file"; then
                cp "$SOURCE_DIR/$file" "$dest_file"
                echo "[MODIFIED] $file" >> "$CHANGE_LOG"
                ((MODIFIED++))
            fi
        else
            cp "$SOURCE_DIR/$file" "$dest_file"
            echo "[NEW] $file" >> "$CHANGE_LOG"
            ((COPIED++))
        fi
    fi
done

echo "[3/4] Copying templates and static files..."

# Copy templates
if [ -d "$SOURCE_DIR/templates" ]; then
    for file in $(find "$SOURCE_DIR/templates" -type f 2>/dev/null); do
        rel_path="${file#$SOURCE_DIR/}"
        dest_file="$DIST_DIR/app/$rel_path"
        mkdir -p "$(dirname "$dest_file")"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$file" "$dest_file"; then
                cp "$file" "$dest_file"
                echo "[MODIFIED] $rel_path" >> "$CHANGE_LOG"
                ((MODIFIED++))
            fi
        else
            cp "$file" "$dest_file"
            echo "[NEW] $rel_path" >> "$CHANGE_LOG"
            ((COPIED++))
        fi
    done
fi

# Copy static files
if [ -d "$SOURCE_DIR/static" ]; then
    for file in $(find "$SOURCE_DIR/static" -type f 2>/dev/null); do
        rel_path="${file#$SOURCE_DIR/}"
        dest_file="$DIST_DIR/app/$rel_path"
        mkdir -p "$(dirname "$dest_file")"
        
        if [ -f "$dest_file" ]; then
            if ! cmp -s "$file" "$dest_file"; then
                cp "$file" "$dest_file"
                echo "[MODIFIED] $rel_path" >> "$CHANGE_LOG"
                ((MODIFIED++))
            fi
        else
            cp "$file" "$dest_file"
            echo "[NEW] $rel_path" >> "$CHANGE_LOG"
            ((COPIED++))
        fi
    done
fi

echo "[4/4] Creating requirements.txt..."
if [ -f "$SOURCE_DIR/requirements.txt" ]; then
    cp "$SOURCE_DIR/requirements.txt" "$DIST_DIR/requirements.txt"
else
    cat > "$DIST_DIR/requirements.txt" << 'EOF'
Django>=4.2
django-select2
Pillow
waitress
django-widget-tweaks
EOF
fi

# Create empty files if they don't exist
if [ ! -f "$DIST_DIR/CHANGELOG.txt" ]; then
    echo "SuppliesPro - Changelog" > "$DIST_DIR/CHANGELOG.txt"
    echo "===============================================" >> "$DIST_DIR/CHANGELOG.txt"
    echo >> "$DIST_DIR/CHANGELOG.txt"
    echo "[NEW] CHANGELOG.txt" >> "$CHANGE_LOG"
    ((COPIED++))
fi

# Copy deployment scripts (preserve existing ones)
for script in linux/windows; do
    if [ -d "$SOURCE_DIR/dist/SuppliesPro/$script" ]; then
        for file in "$SOURCE_DIR/dist/SuppliesPro/$script"/*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                dest_file="$DIST_DIR/$script/$filename"
                if [ -f "$dest_file" ]; then
                    if ! cmp -s "$file" "$dest_file"; then
                        cp "$file" "$dest_file"
                        echo "[MODIFIED] $script/$filename" >> "$CHANGE_LOG"
                        ((MODIFIED++))
                    fi
                else
                    cp "$file" "$dest_file"
                    chmod +x "$dest_file"
                    echo "[NEW] $script/$filename" >> "$CHANGE_LOG"
                    ((COPIED++))
                fi
            fi
        done
    fi
done

# Make scripts executable
chmod +x "$DIST_DIR/linux/"*.sh 2>/dev/null || true

# Summary
{
echo >> "$CHANGE_LOG"
echo "Summary:" >> "$CHANGE_LOG"
echo "- Files copied: $COPIED" >> "$CHANGE_LOG"
echo "- Files modified: $MODIFIED" >> "$CHANGE_LOG"
echo "- Build date: $BUILD_DATE" >> "$CHANGE_LOG"
echo >> "$CHANGE_LOG"
} >> "$CHANGE_LOG"

echo
echo "==============================================="
echo "  Build Complete!"
echo "==============================================="
echo
echo "  Files copied: $COPIED"
echo "  Files modified: $MODIFIED"
echo "  Changelog: $CHANGE_LOG"
echo
echo "  Deployment package ready at: $DIST_DIR"
echo "==============================================="
echo
