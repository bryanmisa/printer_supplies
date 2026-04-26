#!/bin/bash
# SuppliesPro - Start Application for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR/app"

# Use virtual environment if it exists
if [ -f "../venv/bin/python3" ]; then
    PYTHON="../venv/bin/python3"
else
    PYTHON="python3"
fi

echo "==============================================="
echo "  SuppliesPro - Starting Server"
echo "==============================================="
echo "  URL: http://localhost:8080"
echo "==============================================="
echo
echo "Opening browser..."
$PYTHON manage.py runserver 0.0.0.0:8080