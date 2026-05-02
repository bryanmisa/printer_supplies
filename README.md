# SuppliesPro

Printer Supply Management System - Track printer supplies, installations, and consumption across your organization.

## Features

- **Inventory Management** - Track printer supplies with stock levels and thresholds
- **Printer Registry** - Manage printers with IP addresses, locations, and custodians
- **Supply Installations** - Install and dispose supplies on printers
- **Delivery Tracking** - Record deliveries and update stock
- **Reports** - Inventory status, replenishment needs, and consumption analytics
- **User Management** - Role-based access (Admin, Manager, Staff)
- **Database Backup** - Backup and restore for disaster recovery

## Requirements

- Python 3.10+
- SQLite3 (bundled with Python)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd printer_supplies
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Initialize Database

```bash
python manage.py migrate
python manage.py setup_rbac
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

Open http://localhost:8000 in your browser.

## Portable Deployment (Windows)

For deployment on Windows without Python pre-installed:

### 1. Ensure Python is Installed

Download from https://www.python.org/downloads/

### 2. Run Installation

```
SuppliesPro/
├── install.bat    # Install dependencies
├── setup.bat     # Initialize database
├── start.bat    # Launch application
```

### 3. Access Application

Open http://localhost:8080 in your browser.

## Default Credentials

| Role | Username | Password |
|------|---------|----------|
| Admin | admin | admin123 |

**Important:** Change the default password after first login.

## Project Structure

```
printer_supplies/
├── manage.py              # Django CLI
├── requirements.txt      # Python dependencies
├── printer_supplies/     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory/           # Main application
│   ├── models.py       # Database models
│   ├── views.py       # View logic
│   ├── forms.py      # Form definitions
│   └── templates/    # HTML templates
├── rbac/              # Role-based access control
├── templates/          # Base templates
├── static/            # CSS and JavaScript
└── media/            # Uploaded files
```

## Available URLs

| URL | Description |
|-----|-------------|
| `/` | Dashboard |
| `/supplies/` | Supply list |
| `/suppliers/` | Supplier list |
| `/printers/` | Printer list |
| `/deliveries/` | Delivery list |
| `/installations/` | Installation history |
| `/reports/inventory/` | Inventory report |
| `/admin/database/` | Database backup |
| `/audit/` | Audit trail |

## User Roles

| Role | Permissions |
|------|-------------|
| Admin | Full access to all features |
| Manager | Manage supplies, printers, installations |
| Staff | View-only access |

## Database Backup

Navigate to **Administration > Database Backup** to:

- Create a new backup
- Download existing backups
- Restore from a backup
- Delete old backups

## Troubleshooting

### "python is not recognized"

Install Python and add it to your system PATH. Restart your terminal after installation.

### "Port already in use"

Change the port in `manage.py runserver` or stop other applications using that port.

### Database locked

Ensure the server is stopped before running migrations or database operations.

### Static files not loading

```bash
python manage.py collectstatic
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/printer/<id>/compatible-supplies/` | GET | Get compatible supplies for a printer |

## Management Commands

```bash
# Create sample data
python manage.py create_dummy_data

# Setup RBAC permissions
python manage.py setup_rbac

# Collect static files
python manage.py collectstatic
```

## License

This project is proprietary software. All rights reserved.

## Support

For issues or questions, contact your system administrator.