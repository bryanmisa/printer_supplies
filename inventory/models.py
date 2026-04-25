from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name() or self.username


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PrinterModel(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['manufacturer', 'name']

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Printer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired'),
    ]
    name = models.CharField(max_length=200)
    printer_model = models.ForeignKey(PrinterModel, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100, unique=True)
    custodian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='printers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    @property
    def current_installation(self):
        return self.installations.filter(is_active=True).first()


class Supply(models.Model):
    STATUS_CHOICES = [
        ('out_of_stock', 'Out of Stock'),
        ('low_stock', 'Low Stock'),
        ('normal', 'Normal'),
        ('overstock', 'Overstock'),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    printer_models = models.ManyToManyField(PrinterModel, related_name='supplies')
    suppliers = models.ManyToManyField(Supplier, blank=True, related_name='supplies')
    current_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    low_stock_threshold = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    max_stock_threshold = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def status(self):
        if self.current_stock == 0:
            return 'out_of_stock'
        elif self.max_stock_threshold and self.current_stock > self.max_stock_threshold:
            return 'overstock'
        elif self.current_stock <= self.low_stock_threshold:
            return 'low_stock'
        return 'normal'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Delivery(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    delivery_date = models.DateField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-delivery_date']

    def __str__(self):
        return f"Delivery #{self.id} from {self.supplier.name}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='items')
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['delivery', 'supply']

    def __str__(self):
        return f"{self.supply.name} x{self.quantity}"


class SupplyInstallation(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='installations')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='installations')
    installed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    disposed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-installed_at']

    def __str__(self):
        status = "Active" if self.is_active else "Disposed"
        return f"{self.supply.name} in {self.printer.name} ({status})"

    def dispose(self):
        self.is_active = False
        self.disposed_at = models.now()
        self.save()


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('install', 'Installed'),
        ('dispose', 'Disposed'),
        ('delivery', 'Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=500)
    changes = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.action} - {self.object_repr} at {self.timestamp}"