# Printer Supplies (SuppliesPro) - Model Update Manual
*Safe database schema changes for Django 4.2 + SQLite3 production deployments*

## Overview
This manual covers safe workflows for updating Django models in the `inventory` and `rbac` apps without data loss, database corruption, or unhandled errors. It addresses two core concerns:
1. Updating existing models without destroying the production database
2. Adding new models with required (non-nullable) ForeignKey relationships to existing models, without migration errors

Django's built-in migration system is designed to be safe by default:
- Invalid or destructive schema changes trigger warnings/errors *before* the database is modified
- Failed migrations roll back atomically (where supported) leaving the database unchanged
- All schema changes are tracked in version-controlled migration files for reproducibility

---

## Prerequisites
- Python 3.10+ environment activated (`.venv` or `venv`)
- Django 4.2+ installed (per `requirements.txt`)
- Access to production server deployment scripts at `dist/SuppliesPro/linux/` (Linux) or `dist/SuppliesPro/windows/` (Windows)
- Existing migration history in `inventory/migrations/` and `rbac/migrations/`

---

## Core Safety Principles
1. **Always backup first**: Create a database backup via *Administration > Database Backup* (`/admin/database/`) or copy `db.sqlite3` before any migration
2. **Test locally first**: Run all migrations in your local development environment before applying to production
3. **Version control migrations**: Never modify existing migration files that have been applied to production
4. **Non-nullable fields require defaults**: Django will block adding a non-nullable field to an existing table unless you provide a default value or one-off default for existing rows
5. **SQLite note**: SQLite has limited `ALTER TABLE` support; Django handles this by creating new tables, copying data, and dropping old tables automatically during migration

---

## Scenario A: Adding a New Standalone Model
*No relationships to existing models*

### Steps
1. Define the new model in the appropriate `models.py` (`inventory/models.py` or `rbac/models.py`):
   ```python
   # Example: Add to inventory/models.py
   class TonerType(models.Model):
       name = models.CharField(max_length=100, unique=True)
       description = models.TextField(blank=True)
       is_active = models.BooleanField(default=True)

       def __str__(self):
           return self.name
   ```

2. Generate migration for the new model:
   ```bash
   python manage.py makemigrations inventory
   # Output: Migrations for 'inventory':
   #   inventory/migrations/0007_add_tonertype.py
   #     - Create model TonerType
   ```

3. Test locally:
   ```bash
   python manage.py migrate
   python manage.py shell
   >>> from inventory.models import TonerType
   >>> TonerType.objects.create(name="Standard Toner")  # Verify model works
   ```

4. Deploy to production (follow [Production Deployment Workflow](#production-deployment-workflow) below)

---

## Critical Scenario: New Model + Required FK to Existing Model
*Your primary concern: Adding a new model linked via a non-nullable (required) ForeignKey to an existing model, with zero errors*

### Example Context
Add a new `TonerType` model, then link it to the existing `Supply` model via a required (non-nullable) ForeignKey.

### Step 1: Create and apply the new model locally
1. Add `TonerType` to `inventory/models.py` (as shown in Scenario A)
2. Generate and apply the migration locally:
   ```bash
   python manage.py makemigrations inventory
   python manage.py migrate
   ```

### Step 2: Create a default instance for the FK
Since the FK will be non-nullable, all existing `Supply` rows need a valid `TonerType` ID. Create a default entry:
```bash
python manage.py shell
>>> from inventory.models import TonerType
>>> default_toner = TonerType.objects.create(name="Default Toner", is_active=True)
>>> print(default_toner.id)  # Note this ID (e.g., 1) for the next step
```

### Step 3: Add the required FK to the existing model
Update `Supply` in `inventory/models.py` to add the FK:
```python
# Inside the Supply model (inventory/models.py)
toner_type = models.ForeignKey(
    TonerType,
    on_delete=models.PROTECT,  # Prevent deleting TonerType if it's still linked to Supplies
    null=False,  # Required (non-nullable)
    blank=False
)
```

### Step 4: Generate the FK migration with a one-off default
Run `makemigrations` and provide the default `TonerType` ID you created in Step 2:
```bash
python manage.py makemigrations inventory
# Django prompt:
# You are trying to add a non-nullable field 'toner_type' to 'supply' without a default; we can't do that (the database needs something to populate existing rows).
# Please select a fix:
#  1) Provide a one-off default now (will be set on all existing rows with a value of NULL)
#  2) Quit and manually define a default value in the model.
# Select an option: 1
# Please enter the default value now, as valid Python code (this is what the migration will set for existing rows):
# >>> 1  # Enter the ID of your default TonerType from Step 2
# Migrations for 'inventory':
#   inventory/migrations/0008_add_tonertype_fk_to_supply.py
#     - Add field toner_type to supply
```

### Step 5: Test the full migration locally
```bash
python manage.py migrate
# Verify existing Supply rows have the default toner_type:
python manage.py shell
>>> from inventory.models import Supply
>>> Supply.objects.first().toner_type  # Should return the default TonerType
```

### Step 6: Deploy to production
Follow the [Production Deployment Workflow](#production-deployment-workflow) below. The migration will safely populate all existing `Supply` rows with the default `TonerType` ID, then set the field to non-nullable. No errors, no data loss.

---

## Scenario B: Updating Existing Models Safely
### B1: Add a nullable field (no errors)
Simply add the field to the model, generate migration, and apply:
```python
# Example: Add to Supply model
warranty_months = models.IntegerField(null=True, blank=True)
```
```bash
python manage.py makemigrations inventory
python manage.py migrate  # No default needed, existing rows get NULL
```

### B2: Add a non-nullable field with a default
```python
# Example: Add required unit field to Supply
unit = models.CharField(max_length=20, default="piece")
```
```bash
python manage.py makemigrations inventory  # Django will use the default for existing rows
python manage.py migrate
```

### B3: Remove a field safely (avoid data loss)
Never delete a field directly from `models.py` and run migrations if the field has data:
1. **Deprecate first**: Mark the field as `null=True, blank=True` and remove it from forms/views
2. Wait for all production data to be migrated/exported if needed
3. Then remove the field from `models.py` and generate migration:
   ```bash
   python manage.py makemigrations inventory --name remove_deprecated_field
   python manage.py migrate
   ```

### B4: Rename a field (use Django's RenameField operation)
*Never just change the field name in `models.py`*—this deletes the old field and creates a new one, losing data.
1. Generate an empty migration:
   ```bash
   python manage.py makemigrations inventory --empty --name rename_supply_field
   ```
2. Edit the empty migration file to use `RenameField`:
   ```python
   from django.db import migrations
   class Migration(migrations.Migration):
       dependencies = [('inventory', '0007_add_tonertype')]
       operations = [
           migrations.RenameField(
               model_name='supply',
               old_name='old_field_name',
               new_name='new_field_name',
           ),
       ]
   ```
3. Run the migration: `python manage.py migrate`

### B5: Change field type/constraints
1. Test the type change locally first (e.g., changing `CharField` to `IntegerField` requires valid data conversion)
2. Generate migration: `python manage.py makemigrations inventory`
3. Review the migration file to ensure it handles data conversion correctly
4. Test locally before deploying

---

## Production Deployment Workflow
*Project-specific steps for `printer_supplies` deployment*

### Pre-Deployment Checklist
- [ ] Database backed up via `/admin/database/` or `cp db.sqlite3 db.sqlite3.backup`
- [ ] All migrations tested locally
- [ ] New/updated `models.py` and migration files committed to version control

### Steps
1. **Copy updated code to production**:
   - Linux: Use `dist/SuppliesPro/linux/build.sh` to update the deployment package
   - Windows: Use `dist/SuppliesPro/windows/build.bat` to update the deployment package
   - Ensure `inventory/migrations/` and `rbac/migrations/` include all new migration files

2. **Run database migrations**:
   ```bash
   # Activate virtual environment first
   source venv/bin/activate  # Linux
   # .\venv\Scripts\activate  # Windows

   python manage.py migrate
   # Verify no errors, check migration output
   ```

3. **Collect static files (if changed)**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Restart the production server**:
   - Linux (systemd): `sudo systemctl restart suppliespro`
   - Linux (manual): `cd dist/SuppliesPro/linux && ./start.sh`
   - Windows: `schtasks /run /tn "SuppliesPro"` or restart the service

5. **Verify deployment**:
   - Check the application at `http://localhost:8080`
   - Verify new models/fields are accessible in the admin panel
   - Check `sudo journalctl -u suppliespro -f` (Linux) for errors

---

## Error Handling & Rollback
### If a migration fails in production:
1. **Stop immediately**: The database is likely unchanged (Django rolls back failed migrations)
2. Check the error message: Common issues include missing defaults, invalid data, or missing migration files
3. Fix the issue locally, generate corrected migrations, and redeploy

### Rollback to a previous migration:
```bash
# Rollback inventory app to migration 0006 (for example)
python manage.py migrate inventory 0006
# WARNING: This will undo all migrations after 0006, including data changes
# Only use if you have a fresh backup to restore from
```

### Restore from backup:
1. Navigate to *Administration > Database Backup* (`/admin/database/`)
2. Upload or select the backup file created before the migration
3. Confirm restore (this will overwrite the current database)

---

## Danger Zones (Avoid These)
1. **Directly renaming fields/models in `models.py`**: This deletes old data and creates new empty fields. Use `RenameField` migration operation instead.
2. **Modifying existing migration files**: Never edit a migration file that has been applied to production—it will cause migration conflicts.
3. **Adding non-nullable FKs without defaults**: This will cause migration errors. Follow the [Critical Scenario](#critical-scenario-new-model--required-fk-to-existing-model) workflow.
4. **Dropping tables with data**: Django will warn you, but forcing this will destroy data. Always backup first.
5. **Using `null=False` on existing fields with NULL values**: Run a query to update NULL values to a default before changing the field to non-nullable.

---

## Quick Reference Cheat Sheet
### Common Commands
| Command | Description |
|---------|-------------|
| `python manage.py makemigrations <app>` | Generate migrations for model changes |
| `python manage.py migrate` | Apply pending migrations |
| `python manage.py migrate <app> <number>` | Rollback to a specific migration |
| `python manage.py sqlmigrate <app> <number>` | View SQL for a specific migration |
| `python manage.py showmigrations` | List all migrations and their applied status |

### Do's
- ✅ Backup database before every production migration
- ✅ Test all migrations locally first
- ✅ Use `RenameField` for field renames
- ✅ Provide defaults for non-nullable new fields

### Don'ts
- ❌ Edit existing applied migration files
- ❌ Delete fields/models directly without deprecation
- ❌ Deploy untested migrations to production
- ❌ Skip database backups before schema changes

---

*Last updated: May 2026 | Applies to SuppliesPro Django 4.2+ deployments*
