#!/bin/bash
# SuppliesPro - Linux systemd Service Setup
# Run this script to install SuppliesPro as a systemd service
# This will keep the server running after logout and restart

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PARENT_DIR/app"
SERVICE_NAME="suppliespro"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "==============================================="
echo "  SuppliesPro - Install Linux Service"
echo "==============================================="
echo
echo "App directory: $APP_DIR"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] This script must be run as root (use sudo)"
    exit 1
fi

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "[ERROR] App directory not found: $APP_DIR"
    exit 1
fi

# Get Python path
if [ -f "$PARENT_DIR/venv/bin/python3" ]; then
    PYTHON_PATH="$PARENT_DIR/venv/bin/python3"
elif [ -f "$PARENT_DIR/venv/bin/python" ]; then
    PYTHON_PATH="$PARENT_DIR/venv/bin/python"
else
    PYTHON_PATH=$(which python3 || which python)
fi

echo "[1/3] Creating systemd service file..."

# Create service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=SuppliesPro Printer Inventory Management
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_PATH $APP_DIR/manage.py runserver 0.0.0.0:8080
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "  Service file created: $SERVICE_FILE"

echo
echo "[2/3] Enabling and starting service..."

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable "$SERVICE_NAME"

# Start service
systemctl start "$SERVICE_NAME"

# Check status
sleep 2
systemctl is-active --quiet "$SERVICE_NAME"
if [ $? -eq 0 ]; then
    echo "  Service started successfully!"
else
    echo "  [WARNING] Service may have failed to start. Check logs with: journalctl -u $SERVICE_NAME"
fi

echo
echo "[3/3] Creating log viewing script..."
cat > "$SCRIPT_DIR/view_logs.sh" << 'EOF'
#!/bin/bash
sudo journalctl -u suppliespro -f
EOF
chmod +x "$SCRIPT_DIR/view_logs.sh"

echo "  Log viewer created: $SCRIPT_DIR/view_logs.sh"

echo
echo "==============================================="
echo "  Installation Complete!"
echo "==============================================="
echo
echo "  Service Commands:"
echo "  - Start:   sudo systemctl start suppliespro"
echo "  - Stop:    sudo systemctl stop suppliespro"
echo "  - Restart: sudo systemctl restart suppliespro"
echo "  - Status:  sudo systemctl status suppliespro"
echo "  - Logs:    sudo journalctl -u suppliespro -f"
echo "  - Disable: sudo systemctl disable suppliespro"
echo "==============================================="
echo
