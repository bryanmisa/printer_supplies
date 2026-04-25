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

    path('search/', views.global_search, name='global_search'),

    path('api/printer/<int:printer_id>/compatible-supplies/', views.api_compatible_supplies, name='api_compatible_supplies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)