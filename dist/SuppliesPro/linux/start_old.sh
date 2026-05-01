#!/bin/bash
# SuppliesPro - Start Application for Linux/Mac
# For auto-start on boot, use install_service.sh OR add to crontab:
# @reboot /path/to/startup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR/app"

# Use virtual environment if it exists
if [ -f "../venv/bin/python3" ]; then
    PYTHON="../venv/bin/python3"
else
    PYTHON="python3"
fi

# Create logs directory
mkdir -p "$PARENT_DIR/app/logs"

echo "==============================================="
echo "  SuppliesPro - Starting Server"
echo "==============================================="
echo "  URL: http://localhost:8080"
echo "  Logs: $PARENT_DIR/app/logs/server.log"
echo "==============================================="
echo

# Start server (nohup for persistence after logout)
nohup $PYTHON manage.py runserver 0.0.0.0:8080 > "$PARENT_DIR/app/logs/server.log" 2>&1 &

echo "Server started in background!"
echo "PID: $!"
echo "To stop: kill $!"