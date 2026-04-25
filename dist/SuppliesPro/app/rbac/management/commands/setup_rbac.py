from django.core.management.base import BaseCommand
from rbac.models import Permission, Role


class Command(BaseCommand):
    help = 'Setup default RBAC roles and permissions'

    PERMISSIONS = [
        {'code': 'users.view', 'name': 'View Users', 'description': 'View user list and user details'},
        {'code': 'users.create', 'name': 'Create Users', 'description': 'Create new users'},
        {'code': 'users.edit', 'name': 'Edit Users', 'description': 'Edit existing user details'},
        {'code': 'users.delete', 'name': 'Delete Users', 'description': 'Delete users from the system'},
        {'code': 'users.toggle', 'name': 'Toggle User Status', 'description': 'Activate or deactivate users'},
        {'code': 'audit.view', 'name': 'View Audit Log', 'description': 'View the audit trail and logs'},
        {'code': 'reports.view', 'name': 'View Reports', 'description': 'Access all reports'},
        {'code': 'reports.inventory', 'name': 'View Inventory Report', 'description': 'View inventory status report'},
        {'code': 'reports.replenishment', 'name': 'View Replenishment Report', 'description': 'View replenishment recommendations'},
        {'code': 'reports.consumption', 'name': 'View Consumption Report', 'description': 'View supply consumption analytics'},
        {'code': 'inventory.view', 'name': 'View Inventory', 'description': 'View supplies, printers, suppliers, and related data'},
        {'code': 'inventory.supplies', 'name': 'Manage Supplies', 'description': 'Create, edit, delete supplies'},
        {'code': 'inventory.printers', 'name': 'Manage Printers', 'description': 'Create, edit, delete printers'},
        {'code': 'inventory.suppliers', 'name': 'Manage Suppliers', 'description': 'Create, edit, delete suppliers'},
        {'code': 'inventory.deliveries', 'name': 'Manage Deliveries', 'description': 'Create, edit, delete deliveries'},
        {'code': 'inventory.printers.models', 'name': 'Manage Printer Models', 'description': 'Create, edit, delete printer models'},
        {'code': 'inventory.supply_types', 'name': 'Manage Supply Types', 'description': 'Create, edit, delete supply types'},
        {'code': 'installations.view', 'name': 'View Installations', 'description': 'View installation records'},
        {'code': 'installations.manage', 'name': 'Manage Installations', 'description': 'Install and dispose supplies on printers'},
    ]

    ROLES = {
        'admin': [
            'users.view', 'users.create', 'users.edit', 'users.delete', 'users.toggle',
            'audit.view',
            'reports.view', 'reports.inventory', 'reports.replenishment', 'reports.consumption',
            'inventory.view', 'inventory.supplies', 'inventory.printers', 'inventory.suppliers',
            'inventory.deliveries', 'inventory.printers.models', 'inventory.supply_types',
            'installations.view', 'installations.manage',
        ],
        'manager': [
            'reports.view', 'reports.inventory', 'reports.replenishment', 'reports.consumption',
            'inventory.view', 'inventory.supplies', 'inventory.printers', 'inventory.suppliers',
            'inventory.deliveries', 'inventory.printers.models', 'inventory.supply_types',
            'installations.view', 'installations.manage',
        ],
        'staff': [
            'reports.view', 'reports.inventory', 'reports.replenishment', 'reports.consumption',
            'inventory.view',
            'installations.view', 'installations.manage',
        ],
    }

    def handle(self, *args, **options):
        self.stdout.write('Setting up RBAC permissions and roles...\n')

        perms_created = 0
        for perm_data in self.PERMISSIONS:
            perm, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults={
                    'name': perm_data['name'],
                    'description': perm_data.get('description', ''),
                }
            )
            if created:
                perms_created += 1
                self.stdout.write(f'  Created permission: {perm.code}')

        self.stdout.write(f'\nPermissions created: {perms_created}')

        roles_created = 0
        role_mappings = {}
        for role_name, perm_codes in self.ROLES.items():
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                roles_created += 1
                self.stdout.write(f'  Created role: {role_name}')

            perms = Permission.objects.filter(code__in=perm_codes)
            role.permissions.set(perms)
            role_mappings[role_name] = list(perms.values_list('code', flat=True))

        self.stdout.write(f'\nRoles created: {roles_created}')
        self.stdout.write('\n--- Role Permission Mappings ---')
        for role_name, perms in role_mappings.items():
            self.stdout.write(f'{role_name}: {len(perms)} permissions')

        self.stdout.write(self.style.SUCCESS('\nRBAC setup complete!'))
        self.stdout.write('\nDefault roles:')
        self.stdout.write('  - admin: Full access to all features')
        self.stdout.write('  - manager: Reports + Inventory management (no user management)')
        self.stdout.write('  - staff: Reports + View-only inventory + Install/Dispose supplies')