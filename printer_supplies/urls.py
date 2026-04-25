from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from inventory import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),

    path('supplies/', views.SupplyListView.as_view(), name='supply_list'),
    path('supplies/create/', views.SupplyCreateView.as_view(), name='supply_create'),
    path('supplies/<int:pk>/', views.SupplyListView.as_view(), name='supply_detail'),
    path('supplies/<int:pk>/update/', views.SupplyUpdateView.as_view(), name='supply_update'),
    path('supplies/<int:pk>/delete/', views.SupplyDeleteView.as_view(), name='supply_delete'),

    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),

    path('printers/', views.PrinterListView.as_view(), name='printer_list'),
    path('printers/create/', views.PrinterCreateView.as_view(), name='printer_create'),
    path('printers/<int:pk>/', views.PrinterDetailView.as_view(), name='printer_detail'),
    path('printers/<int:pk>/update/', views.PrinterUpdateView.as_view(), name='printer_update'),
    path('printers/<int:pk>/delete/', views.PrinterDeleteView.as_view(), name='printer_delete'),
    path('printers/<int:pk>/install/', views.install_supply, name='printer_install'),

    path('printer-models/', views.PrinterModelListView.as_view(), name='printer_model_list'),
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

    path('api/printer/<int:printer_id>/compatible-supplies/', views.api_compatible_supplies, name='api_compatible_supplies'),
]