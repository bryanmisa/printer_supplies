#!/bin/bash
# SuppliesPro - Install Dependencies for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR/app"

# Use virtual environment if it exists
if [ -f "../venv/bin/python3" ]; then
    PYTHON="../venv/bin/python3"
    PIP="../venv/bin/pip"
else
    if ! command -v python3 &> /dev/null; then
        echo "[ERROR] Python 3 is not installed."
        echo "Install Python: sudo apt install python3 python3-venv (Ubuntu/Debian)"
        echo "           or: sudo yum install python3 python3-venv (Fedora/RHEL)"
        echo "           or: brew install python3 (Mac)"
        read -p "Press Enter to exit..."
        exit 1
    fi
    PYTHON="python3"
    PIP="pip3"
fi

echo "==============================================="
echo "  SuppliesPro - Install Dependencies"
echo "==============================================="
echo

# Create virtual environment if it doesn't exist
if [ ! -f "../venv/bin/python3" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ../venv
    PYTHON="../venv/bin/python3"
    PIP="../venv/bin/pip"
fi

echo "Installing Python dependencies..."
$PIP install -r ../requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo
    echo "==============================================="
    echo "  Dependencies installed successfully!"
    echo
    echo "  Next steps:"
    echo "    1. Run: ./linux/setup.sh"
    echo "    2. Run: ./linux/start.sh"
    echo "==============================================="
else
    echo "[ERROR] Installation failed."
fi

read -p "Press Enter to exit..."