from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from inventory import views
from inventory.admin import admin_site

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/database/', views.database_backup, name='database_backup'),
    path('admin/', admin_site.urls),

    path('', views.dashboard, name='dashboard'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:pk>/toggle/', views.user_toggle_active, name='user_toggle'),
    path('users/<int:pk>/reset-password/', views.user_reset_password, name='user_reset_password'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('supplies/', views.SupplyListView.as_view(), name='supply_list'),
    path('supplies/create/', views.SupplyCreateView.as_view(), name='supply_create'),
    path('supplies/<int:pk>/', views.SupplyDetailView.as_view(), name='supply_detail'),
    path('supplies/<int:pk>/update/', views.SupplyUpdateView.as_view(), name='supply_update'),
    path('supplies/<int:pk>/delete/', views.SupplyDeleteView.as_view(), name='supply_delete'),

    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/toggle/', views.supplier_toggle_active, name='supplier_toggle'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),

    path('printers/', views.PrinterListView.as_view(), name='printer_list'),
    path('printers/create/', views.PrinterCreateView.as_view(), name='printer_create'),
    path('printers/<int:pk>/', views.PrinterDetailView.as_view(), name='printer_detail'),
    path('printers/<int:pk>/update/', views.PrinterUpdateView.as_view(), name='printer_update'),
    path('printers/<int:pk>/delete/', views.PrinterDeleteView.as_view(), name='printer_delete'),
    path('printers/<int:pk>/install/', views.install_supply, name='printer_install'),

    path('printer-models/', views.PrinterModelListView.as_view(), name='printer_model_list'),
    path('printer-models/<int:pk>/', views.PrinterModelDetailView.as_view(), name='printer_model_detail'),
    path('printer-models/create/', views.PrinterModelCreateView.as_view(), name='printer_model_create'),
    path('printer-models/<int:pk>/update/', views.PrinterModelUpdateView.as_view(), name='printer_model_update'),
    path('printer-models/<int:pk>/delete/', views.PrinterModelDeleteView.as_view(), name='printer_model_delete'),
    path('printer-models/<int:pk>/toggle/', views.PrinterModelToggleView.as_view(), name='printer_model_toggle'),

    path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    path('deliveries/create/', views.DeliveryCreateView.as_view(), name='delivery_create'),
    path('deliveries/<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery_detail'),

    path('installations/', views.InstallationListView.as_view(), name='installation_list'),
    path('installations/<int:pk>/dispose/', views.dispose_supply, name='installation_dispose'),

    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/replenishment/', views.replenishment_report, name='replenishment_report'),
    path('reports/consumption/', views.consumption_report, name='consumption_report'),

    path('audit/', views.audit_log, name='audit_log'),

    path('supply-types/', views.SupplyTypeListView.as_view(), name='supply_type_list'),
    path('supply-types/create/', views.SupplyTypeCreateView.as_view(), name='supply_type_create'),
    path('supply-types/<int:pk>/', views.SupplyTypeDetailView.as_view(), name='supply_type_detail'),
    path('supply-types/<int:pk>/update/', views.SupplyTypeUpdateView.as_view(), name='supply_type_update'),
    path('supply-types/<int:pk>/delete/', views.SupplyTypeDeleteView.as_view(), name='supply_type_delete'),

    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('departments/<int:pk>/toggle/', views.DepartmentToggleView.as_view(), name='department_toggle'),

    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/create/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locations/<int:pk>/update/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),
    path('locations/<int:pk>/toggle/', views.LocationToggleView.as_view(), name='location_toggle'),

    path('custodians/', views.CustodianListView.as_view(), name='custodian_list'),
    path('custodians/create/', views.CustodianCreateView.as_view(), name='custodian_create'),
    path('custodians/<int:pk>/', views.CustodianDetailView.as_view(), name='custodian_detail'),
    path('custodians/<int:pk>/update/', views.CustodianUpdateView.as_view(), name='custodian_update'),
    path('custodians/<int:pk>/delete/', views.CustodianDeleteView.as_view(), name='custodian_delete'),
    path('custodians/<int:pk>/toggle/', views.CustodianToggleView.as_view(), name='custodian_toggle'),

    path('search/', views.global_search, name='global_search'),
    path('api/printer/<int:printer_id>/compatible-supplies/', views.api_compatible_supplies, name='api_compatible_supplies'),
    path('api/quick-add/<str:model_name>/', views.api_quick_add, name='api_quick_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)