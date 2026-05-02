#!/bin/bash
# Deployment script for SuppliesPro

set -e

echo "Setting up SuppliesPro for production..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
cd app
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo "Run with: cd app && python serve_prod.py"
echo "Or with custom port: PORT=8080 python app/serve_prod.py"
