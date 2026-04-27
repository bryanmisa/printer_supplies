from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from inventory.models import (
    User, Supplier, SupplyType, PrinterModel, Supply, Printer,
    Delivery, DeliveryItem, SupplyInstallation
)


class Command(BaseCommand):
    help = 'Create dummy data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...\n')

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'  Created admin user: admin/admin123')

        manager, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@example.com',
                'first_name': 'John',
                'last_name': 'Manager',
                'role': 'manager',
            }
        )
        if created:
            manager.set_password('manager123')
            manager.save()
            self.stdout.write(f'  Created manager user: manager/manager123')

        # Create a custodian instead of staff user
        staff_custodian, created = Custodian.objects.get_or_create(
            first_name='Jane',
            last_name='Staff',
            defaults={
                'email': 'jane.staff@example.com',
                'phone': '555-0105',
            }
        )
        if created:
            self.stdout.write(f'  Created custodian: {staff_custodian.full_name}')

        suppliers_data = [
            {'name': 'TechSupply Co', 'contact': 'Mike Johnson', 'email': 'mike@techsupply.com', 'phone': '555-0101', 'address': '123 Tech Street, Silicon Valley, CA'},
            {'name': 'Printer Parts Inc', 'contact': 'Sarah Williams', 'email': 'sarah@printerparts.com', 'phone': '555-0102', 'address': '456 Parts Ave, Austin, TX'},
            {'name': 'Office Solutions', 'contact': 'Bob Davis', 'email': 'bob@officesolutions.com', 'phone': '555-0103', 'address': '789 Office Blvd, New York, NY'},
            {'name': 'Global Supplies Ltd', 'contact': 'Emma Wilson', 'email': 'emma@globalsupplies.com', 'phone': '555-0104', 'address': '321 Global Way, Chicago, IL'},
        ]
        suppliers = []
        for s in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=s['name'],
                defaults={
                    'contact_name': s['contact'],
                    'email': s['email'],
                    'phone': s['phone'],
                    'address': s['address'],
                }
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'  Created supplier: {s["name"]}')

        supply_types_data = [
            {'name': 'Toner Cartridge', 'description': 'Laser printer toner cartridges'},
            {'name': 'Ink Cartridge', 'description': 'Inkjet printer cartridges'},
            {'name': 'Drum Unit', 'description': 'Photoconductive drum units'},
            {'name': 'Toner Powder', 'description': 'Refill toner powder'},
            {'name': 'Maintenance Kit', 'description': 'Printer maintenance kits'},
        ]
        supply_types = []
        for st in supply_types_data:
            supply_type, created = SupplyType.objects.get_or_create(
                name=st['name'],
                defaults={'description': st['description']}
            )
            supply_types.append(supply_type)
            if created:
                self.stdout.write(f'  Created supply type: {st["name"]}')

        printer_models_data = [
            {'name': 'LaserJet Pro 400', 'manufacturer': 'HP'},
            {'name': 'OfficeJet Pro 9015', 'manufacturer': 'HP'},
            {'name': 'ImageCLASS MF644', 'manufacturer': 'Canon'},
            {'name': 'EcoTank ET-4760', 'manufacturer': 'Epson'},
            {'name': 'WorkForce Pro EC-4040', 'manufacturer': 'Epson'},
            {'name': 'VersaLink C405', 'manufacturer': 'Xerox'},
            {'name': 'Laser 135w', 'manufacturer': 'Samsung'},
        ]
        printer_models = []
        for pm in printer_models_data:
            model, created = PrinterModel.objects.get_or_create(
                name=pm['name'],
                manufacturer=pm['manufacturer'],
            )
            printer_models.append(model)
            if created:
                self.stdout.write(f'  Created printer model: {pm["manufacturer"]} {pm["name"]}')

        supplies_data = [
            {'name': 'HP 58A Black Toner', 'sku': 'CF258A', 'type_idx': 0, 'threshold': 10, 'max_threshold': 50, 'stock': 25},
            {'name': 'HP 58X Black Toner XL', 'sku': 'CF258X', 'type_idx': 0, 'threshold': 5, 'max_threshold': 30, 'stock': 12},
            {'name': 'Canon 056 Black Toner', 'sku': 'CNI-056', 'type_idx': 0, 'threshold': 15, 'max_threshold': 60, 'stock': 45},
            {'name': 'Canon 056H Black Toner', 'sku': 'CNI-056H', 'type_idx': 0, 'threshold': 10, 'max_threshold': 40, 'stock': 8},
            {'name': 'Xerox 006R04353 Toner', 'sku': 'XRX-053', 'type_idx': 0, 'threshold': 12, 'max_threshold': 48, 'stock': 30},
            {'name': 'Epson 502 Ink Black', 'sku': 'EPS-502K', 'type_idx': 1, 'threshold': 8, 'max_threshold': 32, 'stock': 0},
            {'name': 'Epson 502 Ink Cyan', 'sku': 'EPS-502C', 'type_idx': 1, 'threshold': 8, 'max_threshold': 32, 'stock': 15},
            {'name': 'HP W1350X Black', 'sku': 'HP1350X', 'type_idx': 0, 'threshold': 10, 'max_threshold': 40, 'stock': 5},
            {'name': 'Canon DR-2080C Drum', 'sku': 'CNI-DR80', 'type_idx': 2, 'threshold': 3, 'max_threshold': 15, 'stock': 7},
            {'name': 'HP 26A Drum Unit', 'sku': 'HP26A-D', 'type_idx': 2, 'threshold': 4, 'max_threshold': 20, 'stock': 11},
            {'name': 'Samsung MLT-D101S', 'sku': 'SAM-D101', 'type_idx': 0, 'threshold': 6, 'max_threshold': 25, 'stock': 18},
            {'name': 'Xerox Maintenance Kit', 'sku': 'XRX-MK', 'type_idx': 4, 'threshold': 2, 'max_threshold': 10, 'stock': 4},
        ]
        supplies = []
        for s in supplies_data:
            supply, created = Supply.objects.get_or_create(
                sku=s['sku'],
                defaults={
                    'name': s['name'],
                    'supply_type': supply_types[s['type_idx']],
                    'low_stock_threshold': s['threshold'],
                    'max_stock_threshold': s['max_threshold'],
                    'current_stock': s['stock'],
                }
            )
            if created:
                supply.printer_models.set(random.sample(printer_models, min(3, len(printer_models))))
                supply.suppliers.set(random.sample(suppliers, min(2, len(suppliers))))
                supply.save()
                self.stdout.write(f'  Created supply: {s["name"]} (Stock: {s["stock"]})')
            supplies.append(supply)

        # Create some custodians
        custodians = []
        custodian_data = [
            {'first': 'John', 'last': 'Doe', 'email': 'john.doe@example.com'},
            {'first': 'Jane', 'last': 'Smith', 'email': 'jane.smith@example.com'},
            {'first': 'Bob', 'last': 'Johnson', 'email': 'bob.johnson@example.com'},
        ]
        for c in custodian_data:
            custodian, created = Custodian.objects.get_or_create(
                first_name=c['first'],
                last_name=c['last'],
                defaults={'email': c['email']}
            )
            custodians.append(custodian)
            if created:
                self.stdout.write(f'  Created custodian: {custodian.full_name}')

        printers_data = [
            {'name': 'Reception Laser Printer', 'model_idx': 0, 'serial': 'HP-LJ-001', 'location': 'Reception Area', 'status': 'active'},
            {'name': 'Accounting HP Office', 'model_idx': 1, 'serial': 'HP-OJ-001', 'location': 'Accounting Department', 'status': 'active'},
            {'name': 'IT Canon Printer', 'model_idx': 2, 'serial': 'CN-MF-001', 'location': 'IT Department', 'status': 'active'},
            {'name': 'HR Epson WorkForce', 'model_idx': 4, 'serial': 'EP-WF-001', 'location': 'HR Office', 'status': 'active'},
            {'name': 'Marketing Xerox', 'model_idx': 5, 'serial': 'XR-VL-001', 'location': 'Marketing Floor', 'status': 'active'},
            {'name': 'Warehouse Samsung', 'model_idx': 6, 'serial': 'SM-L-001', 'location': 'Warehouse Office', 'status': 'maintenance'},
            {'name': 'Lab Canon Backup', 'model_idx': 2, 'serial': 'CN-MF-002', 'location': 'Lab', 'status': 'active'},
            {'name': 'Executive Epson', 'model_idx': 3, 'serial': 'EP-ET-001', 'location': 'Executive Suite', 'status': 'active'},
        ]
        printers = []
        for p in printers_data:
            printer, created = Printer.objects.get_or_create(
                serial_number=p['serial'],
                defaults={
                    'name': p['name'],
                    'printer_model': printer_models[p['model_idx']],
                    'location': random.choice(Location.objects.all()) if Location.objects.exists() else None,
                    'status': p['status'],
                    'custodian': random.choice(custodians) if custodians else None,
                }
            )
            if created:
                self.stdout.write(f'  Created printer: {p["name"]}')
            printers.append(printer)

        now = timezone.now()
        for i in range(3):
            delivery, created = Delivery.objects.get_or_create(
                delivery_date=now.date() - timedelta(days=i * 7),
                supplier=random.choice(suppliers),
                defaults={
                    'notes': f'Regular delivery #{i+1}',
                    'created_by': admin,
                }
            )
            if created:
                selected_supplies = random.sample(supplies, min(3, len(supplies)))
                for supply in selected_supplies:
                    qty = random.randint(5, 20)
                    DeliveryItem.objects.create(delivery=delivery, supply=supply, quantity=qty)
                    supply.current_stock += qty
                    supply.save()
                self.stdout.write(f'  Created delivery: #{delivery.id} from {delivery.supplier.name}')

        installations_created = 0
        for printer in printers[:5]:
            for supply in supplies[:4]:
                if supply.current_stock > 0 and random.random() > 0.3:
                    compat_models = supply.printer_models.all()
                    if printer.printer_model in compat_models:
                        days_ago = random.randint(1, 60)
                        installed = SupplyInstallation.objects.create(
                            printer=printer,
                            supply=supply,
                            installed_by=random.choice([admin, manager]),
                            installed_at=now - timedelta(days=days_ago),
                        )
                        supply.current_stock -= 1
                        supply.save()
                        installations_created += 1

                        if random.random() > 0.5:
                            installed.is_active = False
                            installed.disposed_at = installed.installed_at + timedelta(days=random.randint(5, days_ago))
                            installed.save()

        self.stdout.write(f'  Created {installations_created} supply installations')

        self.stdout.write(self.style.SUCCESS('\nDummy data created successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Manager: manager / manager123')
        self.stdout.write('  Staff:   staff / staff123')