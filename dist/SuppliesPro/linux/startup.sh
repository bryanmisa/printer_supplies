#!/bin/bash
# SuppliesPro - Simple Linux Startup Script
# Use this if you don't want to use systemd service
# Add to crontab with: @reboot /path/to/startup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PARENT_DIR/app"

# Use virtual environment if it exists
if [ -f "$PARENT_DIR/venv/bin/python3" ]; then
    PYTHON="$PARENT_DIR/venv/bin/python3"
else
    PYTHON="python3"
fi

cd "$APP_DIR"
nohup $PYTHON manage.py runserver 0.0.0.0:8080 > "$APP_DIR/logs/server.log" 2>&1 &

echo "SuppliesPro server started!"
echo "Log file: $APP_DIR/logs/server.log"
