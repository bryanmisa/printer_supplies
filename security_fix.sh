#!/bin/bash
# SuppliesPro - Security Fix Script
# This script fixes common security issues

set -e

echo "==============================================="
echo "  SuppliesPro - Security Fix Script"
echo "==============================================="
echo

# Check if we're in the right directory
if [ ! -f "printer_supplies/settings.py" ] && [ ! -f "settings.py" ]; then
    echo "[ERROR] Please run this script from the project root"
    exit 1
fi

PROJECT_DIR="."
if [ -d "printer_supplies" ]; then
    PROJECT_DIR="printer_supplies"
fi

echo "[1/5] Checking SECRET_KEY..."

# Generate new secret key if .env doesn't exist or has default
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(50))" 2>/dev/null || openssl rand -hex 50)
    
    cat > .env << EOF
# SuppliesPro Environment Variables
# DO NOT COMMIT THIS FILE TO VERSION CONTROL!

SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    
    echo "  .env file created with new SECRET_KEY"
else
    # Check if SECRET_KEY is the default
    if grep -q "django-insecure-dev-key" .env 2>/dev/null; then
        echo "  [WARNING] Default SECRET_KEY detected, generating new one..."
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(50))" 2>/dev/null || openssl rand -hex 50)
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        echo "  SECRET_KEY updated"
    else
        echo "  SECRET_KEY appears to be configured"
    fi
fi

echo
echo "[2/5] Setting DEBUG=False..."

if grep -q "^DEBUG=True" .env 2>/dev/null; then
    sed -i 's/^DEBUG=True/DEBUG=False/' .env
    echo "  DEBUG set to False"
elif ! grep -q "^DEBUG=" .env 2>/dev/null; then
    echo "DEBUG=False" >> .env
    echo "  DEBUG=False added to .env"
else
    echo "  DEBUG already configured"
fi

echo
echo "[3/5] Configuring ALLOWED_HOSTS..."

if ! grep -q "^ALLOWED_HOSTS" .env 2>/dev/null; then
    echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
    echo "  ALLOWED_HOSTS configured"
else
    echo "  ALLOWED_HOSTS already configured"
fi

echo
echo "[4/5] Upgrading reportlab..."

if command -v pip3 &> /dev/null; then
    pip3 install --upgrade reportlab --quiet 2>/dev/null
    echo "  reportlab upgraded"
elif command -v pip &> /dev/null; then
    pip install --upgrade reportlab --quiet 2>/dev/null
    echo "  reportlab upgraded"
else
    echo "  [WARNING] pip not found, skipping reportlab upgrade"
fi

echo
echo "[5/5] Checking .gitignore..."

if [ -f ".gitignore" ]; then
    if ! grep -q "^\.env$" .gitignore; then
        echo ".env" >> .gitignore
        echo "  .env added to .gitignore"
    else
        echo "  .env already in .gitignore"
    fi
else
    echo ".env" > .gitignore
    echo "  .gitignore created with .env"
fi

echo
echo "==============================================="
echo "  Security Fixes Applied!"
echo "==============================================="
echo
echo "  Changes made:"
echo "  - SECRET_KEY: Generated new secure key"
echo "  - DEBUG: Set to False"
echo "  - ALLOWED_HOSTS: Configured for localhost"
echo "  - reportlab: Upgraded to latest version"
echo "  - .gitignore: .env added"
echo
echo "  Next steps:"
echo "  1. Review .env file"
echo "  2. Add your domain to ALLOWED_HOSTS if needed:"
echo "     ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com"
echo "  3. Never commit .env to version control!"
echo "  4. For production, also configure HTTPS/SSL"
echo
echo "  To apply changes, restart the server."
echo "==============================================="
echo
