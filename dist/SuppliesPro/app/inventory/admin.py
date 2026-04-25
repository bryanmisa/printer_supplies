from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    User, Supplier, SupplyType, PrinterModel, Printer, Supply,
    Delivery, DeliveryItem, SupplyInstallation, AuditLog
)


class AdminSite(admin.AdminSite):
    site_header = 'Printer Supplies Administration'
    site_title = 'Admin Portal'
    index_title = 'Administration'

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.role == 'admin'


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'department')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ['groups', 'user_permissions']


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_name', 'email', 'phone', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_name']


class SupplyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


class PrinterModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer']
    search_fields = ['name', 'manufacturer']


class PrinterAdmin(admin.ModelAdmin):
    list_display = ['name', 'printer_model', 'serial_number', 'custodian', 'status', 'location']
    list_filter = ['status']
    search_fields = ['name', 'serial_number']


class SupplyAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'supply_type', 'current_stock', 'status']
    list_filter = ['supply_type', 'is_active']
    search_fields = ['name', 'sku']


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'delivery_date', 'created_by']
    list_filter = ['delivery_date', 'supplier']
    search_fields = ['supplier__name']


class DeliveryItemAdmin(admin.ModelAdmin):
    list_display = ['delivery', 'supply', 'quantity']
    list_filter = ['supply']


class SupplyInstallationAdmin(admin.ModelAdmin):
    list_display = ['printer', 'supply', 'installed_by', 'installed_at', 'is_active']
    list_filter = ['is_active']


class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'object_repr', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['object_repr']
    readonly_fields = ['user', 'action', 'content_type', 'object_id', 'object_repr', 'changes', 'timestamp']


admin_site = AdminSite(name='admin')

admin_site.register(User, UserAdmin)
admin_site.register(Supplier, SupplierAdmin)
admin_site.register(SupplyType, SupplyTypeAdmin)
admin_site.register(PrinterModel, PrinterModelAdmin)
admin_site.register(Printer, PrinterAdmin)
admin_site.register(Supply, SupplyAdmin)
admin_site.register(Delivery, DeliveryAdmin)
admin_site.register(DeliveryItem, DeliveryItemAdmin)
admin_site.register(SupplyInstallation, SupplyInstallationAdmin)
admin_site.register(AuditLog, AuditLogAdmin)
admin_site.register(Group)