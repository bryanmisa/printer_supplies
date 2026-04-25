import json
from datetime import datetime, timedelta
from decimal import Decimal
from itertools import chain

from django.db import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.html import format_html
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import (
    LoginForm, UserCreationForm, SupplierForm, PrinterModelForm, PrinterForm,
    SupplyForm, DeliveryForm, DeliveryItemForm, InstallationForm, DisposalForm
)
from .models import (
    Supply, Printer, PrinterModel, Supplier, Delivery, DeliveryItem,
    SupplyInstallation, AuditLog, User
)


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


def is_manager(user):
    return user.is_authenticated and user.role in ['admin', 'manager']


def log_audit(user, action, obj, changes=None):
    if obj:
        AuditLog.objects.create(
            user=user,
            action=action,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            object_repr=str(obj),
            changes=changes or {}
        )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or 'dashboard')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_supplies = Supply.objects.filter(is_active=True).count()
    total_printers = Printer.objects.filter(status='active').count()
    installed_supplies = SupplyInstallation.objects.filter(is_active=True).count()
    out_of_stock = Supply.objects.filter(current_stock=0, is_active=True).count()
    low_stock = Supply.objects.filter(
        current_stock__gt=0,
        current_stock__lte=models.F('low_stock_threshold'),
        is_active=True
    ).count()

    out_of_stock_alerts = Supply.objects.filter(current_stock=0, is_active=True)[:5]
    low_stock_alerts = Supply.objects.filter(
        current_stock__gt=0,
        current_stock__lte=models.F('low_stock_threshold'),
        is_active=True
    )[:5]

    last_30_days = timezone.now() - timedelta(days=30)
    consumption_data = SupplyInstallation.objects.filter(
        disposed_at__gte=last_30_days
    ).values('disposed_at__date').annotate(count=Count('id')).order_by('disposed_at__date')

    labels = []
    data = []
    for i in range(30, -1, -1):
        date = (timezone.now() - timedelta(days=i)).date()
        labels.append(date.strftime('%b %d'))
        count = next((item['count'] for item in consumption_data if item['disposed_at__date'] == date), 0)
        data.append(count)

    supply_models = PrinterModel.objects.all()[:10]

    context = {
        'total_supplies': total_supplies,
        'total_printers': total_printers,
        'installed_supplies': installed_supplies,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'out_of_stock_alerts': out_of_stock_alerts,
        'low_stock_alerts': low_stock_alerts,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
        'supply_models': supply_models,
    }
    return render(request, 'inventory/dashboard.html', context)


class SupplyListView(LoginRequiredMixin, ListView):
    model = Supply
    template_name = 'inventory/supply_list.html'
    paginate_by = 20
    context_object_name = 'supplies'

    def get_queryset(self):
        queryset = Supply.objects.filter(is_active=True)
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        printer_model = self.request.GET.get('printer_model')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(sku__icontains=query)
            )
        if status:
            if status == 'out_of_stock':
                queryset = queryset.filter(current_stock=0)
            elif status == 'low_stock':
                queryset = queryset.filter(
                    current_stock__gt=0,
                    current_stock__lte=models.F('low_stock_threshold')
                )
            elif status == 'normal':
                queryset = queryset.filter(
                    current_stock__gt=models.F('low_stock_threshold')
                )
            elif status == 'overstock':
                queryset = queryset.filter(
                    current_stock__gt=models.F('max_stock_threshold')
                )
        if printer_model:
            queryset = queryset.filter(printer_models_id=printer_model)
        if supplier:
            queryset = queryset.filter(suppliers_id=supplier)

        return queryset.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['printer_models'] = PrinterModel.objects.all()
        context['suppliers'] = Supplier.objects.filter(is_active=True)
        return context


class SupplyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supply
    form_class = SupplyForm
    template_name = 'inventory/supply_form.html'
    permission_required = 'inventory.add_supply'
    success_url = reverse_lazy('supply_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Supply created successfully.')
        log_audit(self.request.user, 'create', form.instance, {'action': 'created'})
        return response


class SupplyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Supply
    form_class = SupplyForm
    template_name = 'inventory/supply_form.html'
    permission_required = 'inventory.change_supply'
    success_url = reverse_lazy('supply_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Supply updated successfully.')
        log_audit(self.request.user, 'update', form.instance, {'action': 'updated'})
        return response


class SupplyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supply
    template_name = 'inventory/supply_confirm_delete.html'
    permission_required = 'inventory.delete_supply'
    success_url = reverse_lazy('supply_list')
    context_object_name = 'supply'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(request, 'Supply deleted successfully.')
        log_audit(request.user, 'delete', self.object, {'action': 'deleted'})
        return redirect(self.success_url)


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    paginate_by = 20
    context_object_name = 'suppliers'

    def get_queryset(self):
        queryset = Supplier.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(contact_name__icontains=query)
            )
        return queryset


class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    permission_required = 'inventory.add_supplier'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Supplier created successfully.')
        log_audit(self.request.user, 'create', form.instance, {'action': 'created'})
        return response


class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    permission_required = 'inventory.change_supplier'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Supplier updated successfully.')
        log_audit(self.request.user, 'update', form.instance, {'action': 'updated'})
        return response


class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    permission_required = 'inventory.delete_supplier'
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'supplier'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(request, 'Supplier deleted successfully.')
        log_audit(request.user, 'delete', self.object, {'action': 'deleted'})
        return redirect(self.success_url)


class PrinterListView(LoginRequiredMixin, ListView):
    model = Printer
    template_name = 'inventory/printer_list.html'
    paginate_by = 20
    context_object_name = 'printers'

    def get_queryset(self):
        queryset = Printer.objects.all()
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        custodian = self.request.GET.get('custodian')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(serial_number__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        if custodian:
            queryset = queryset.filter(custodian_id=custodian)

        return queryset.select_related('printer_model', 'custodian')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class PrinterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Printer
    form_class = PrinterForm
    template_name = 'inventory/printer_form.html'
    permission_required = 'inventory.add_printer'
    success_url = reverse_lazy('printer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Printer created successfully.')
        log_audit(self.request.user, 'create', form.instance, {'action': 'created'})
        return response


class PrinterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Printer
    form_class = PrinterForm
    template_name = 'inventory/printer_form.html'
    permission_required = 'inventory.change_printer'
    success_url = reverse_lazy('printer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Printer updated successfully.')
        log_audit(self.request.user, 'update', form.instance, {'action': 'updated'})
        return response


class PrinterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Printer
    template_name = 'inventory/printer_confirm_delete.html'
    permission_required = 'inventory.delete_printer'
    success_url = reverse_lazy('printer_list')
    context_object_name = 'printer'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Printer deleted successfully.')
        log_audit(request.user, 'delete', self.object, {'action': 'deleted'})
        return redirect(self.success_url)


class PrinterDetailView(LoginRequiredMixin, DetailView):
    model = Printer
    template_name = 'inventory/printer_detail.html'
    context_object_name = 'printer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        printer = self.object

        context['installations'] = SupplyInstallation.objects.filter(
            printer=printer
        ).select_related('supply', 'installed_by').order_by('-installed_at')

        context['current_installations'] = SupplyInstallation.objects.filter(
            printer=printer, is_active=True
        ).select_related('supply', 'installed_by')

        context['compatible_supplies'] = Supply.objects.filter(
            printer_models=printer.printer_model,
            is_active=True,
            current_stock__gt=0
        )

        return context


class PrinterModelListView(LoginRequiredMixin, ListView):
    model = PrinterModel
    template_name = 'inventory/printer_model_list.html'
    context_object_name = 'printer_models'


class PrinterModelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PrinterModel
    form_class = PrinterModelForm
    template_name = 'inventory/printer_model_form.html'
    permission_required = 'inventory.add_printermodel'
    success_url = reverse_lazy('printer_model_list')

    def form_valid(self, form):
        messages.success(self.request, 'Printer model created successfully.')
        return super().form_valid(form)


class PrinterModelUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PrinterModel
    form_class = PrinterModelForm
    template_name = 'inventory/printer_model_form.html'
    permission_required = 'inventory.change_printermodel'
    success_url = reverse_lazy('printer_model_list')

    def form_valid(self, form):
        messages.success(self.request, 'Printer model updated successfully.')
        return super().form_valid(form)


class DeliveryListView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = 'inventory/delivery_list.html'
    paginate_by = 20
    context_object_name = 'deliveries'

    def get_queryset(self):
        queryset = Delivery.objects.all()
        query = self.request.GET.get('q')
        supplier = self.request.GET.get('supplier')

        if query:
            queryset = queryset.filter(notes__icontains=query)
        if supplier:
            queryset = queryset.filter(supplier_id=supplier)

        return queryset.select_related('supplier', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.filter(is_active=True)
        return context


class DeliveryCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    form_class = DeliveryForm
    template_name = 'inventory/delivery_form.html'
    permission_required = 'inventory.add_delivery'
    success_url = reverse_lazy('delivery_list')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.created_by = request.user
            delivery.save()

            supply_id = request.POST.get('supply')
            quantity = request.POST.get('quantity')
            if supply_id and quantity:
                supply = Supply.objects.get(pk=supply_id)
                item = DeliveryItem.objects.create(
                    delivery=delivery,
                    supply=supply,
                    quantity=int(quantity)
                )
                supply.current_stock += int(quantity)
                supply.save()

                log_audit(request.user, 'delivery', delivery, {
                    'supply': supply.name,
                    'quantity': quantity
                })

            messages.success(request, 'Delivery created successfully.')
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class DeliveryDetailView(LoginRequiredMixin, DetailView):
    model = Delivery
    template_name = 'inventory/delivery_detail.html'
    context_object_name = 'delivery'


class InstallationListView(LoginRequiredMixin, ListView):
    model = SupplyInstallation
    template_name = 'inventory/installation_list.html'
    paginate_by = 20
    context_object_name = 'installations'

    def get_queryset(self):
        queryset = SupplyInstallation.objects.all()
        printer = self.request.GET.get('printer')
        status = self.request.GET.get('status')

        if printer:
            queryset = queryset.filter(printer_id=printer)
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'disposed':
            queryset = queryset.filter(is_active=False)

        return queryset.select_related('printer', 'printer__printer_model', 'supply', 'installed_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['printers'] = Printer.objects.filter(status='active')
        return context


@login_required
def install_supply(request, pk):
    printer = get_object_or_404(Printer, pk=pk)

    if request.method == 'POST':
        supply_ids = request.POST.getlist('supplies')
        notes = request.POST.get('notes', '')

        if not supply_ids:
            messages.error(request, 'Please select at least one supply to install.')
            return redirect('printer_detail', pk=printer.id)

        installed = []
        errors = []

        for supply_id in supply_ids:
            supply = get_object_or_404(Supply, pk=supply_id)

            if supply.current_stock <= 0:
                errors.append(f'{supply.name} is out of stock.')
                continue

            if not supply.printer_models.filter(pk=printer.printer_model.pk).exists():
                errors.append(f'{supply.name} is not compatible with this printer model.')
                continue

            if SupplyInstallation.objects.filter(printer=printer, supply=supply, is_active=True).exists():
                errors.append(f'{supply.name} is already installed on this printer.')
                continue

            installation = SupplyInstallation.objects.create(
                printer=printer,
                supply=supply,
                installed_by=request.user,
                notes=notes
            )
            supply.current_stock -= 1
            supply.save()

            log_audit(request.user, 'install', installation, {
                'printer': printer.name,
                'supply': supply.name
            })
            installed.append(supply.name)

        if installed:
            messages.success(request, f'Installed: {", ".join(installed)}.')
        if errors:
            messages.error(request, f'Could not install: {", ".join(errors)}')

        return redirect('printer_detail', pk=printer.id)

    return redirect('printer_list')


@login_required
def dispose_supply(request, pk):
    installation = get_object_or_404(SupplyInstallation, pk=pk)
    printer_pk = installation.printer.pk
    
    if not installation.is_active:
        messages.error(request, 'This supply is already disposed.')
        return redirect('printer_detail', pk=printer_pk)

    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        installation.is_active = False
        installation.disposed_at = timezone.now()
        installation.notes = notes
        installation.save()

        log_audit(request.user, 'dispose', installation, {
            'printer': installation.printer.name,
            'supply': installation.supply.name
        })

        messages.success(request, f'{installation.supply.name} disposed from {installation.printer.name}.')
        return redirect('printer_detail', pk=printer_pk)

    return redirect('printer_detail', pk=printer_pk)


@login_required
def inventory_report(request):
    supplies = Supply.objects.filter(is_active=True)
    
    out_of_stock = supplies.filter(current_stock=0)
    low_stock = supplies.filter(
        current_stock__gt=0,
        current_stock__lte=models.F('low_stock_threshold')
    )
    normal = supplies.filter(
        current_stock__gt=models.F('low_stock_threshold'),
        current_stock__lte=models.F('max_stock_threshold')
    )
    overstock = supplies.filter(
        current_stock__gt=models.F('max_stock_threshold')
    )

    context = {
        'total_supplies': supplies.count(),
        'out_of_stock': out_of_stock,
        'out_of_stock_count': out_of_stock.count(),
        'low_stock': low_stock,
        'low_stock_count': low_stock.count(),
        'normal': normal,
        'normal_count': normal.count(),
        'overstock': overstock,
        'overstock_count': overstock.count(),
    }
    return render(request, 'inventory/inventory_report.html', context)


@login_required
def replenishment_report(request):
    supplies = Supply.objects.filter(is_active=True)
    
    out_of_stock = supplies.filter(current_stock=0).order_by('name')
    low_stock = supplies.filter(
        current_stock__gt=0,
        current_stock__lte=models.F('low_stock_threshold')
    ).order_by('name')

    context = {
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
    }
    return render(request, 'inventory/replenishment_report.html', context)


@login_required
def consumption_report(request):
    months = int(request.GET.get('months', 12))
    custodian_id = request.GET.get('custodian')

    start_date = timezone.now() - timedelta(days=months * 30)
    queryset = SupplyInstallation.objects.filter(
        disposed_at__gte=start_date,
        is_active=False
    )

    if custodian_id:
        queryset = queryset.filter(printer__custodian_id=custodian_id)

    data = queryset.values('disposed_at__year', 'disposed_at__month').annotate(
        count=Count('id')
    ).order_by('disposed_at__year', 'disposed_at__month')

    labels = []
    counts = []
    for item in data:
        labels.append(f"{item['disposed_at__year']}-{item['disposed_at__month']:02d}")
        counts.append(item['count'])

    context = {
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(counts),
        'months': months,
        'custodians': User.objects.filter(printers__isnull=False).distinct(),
    }
    return render(request, 'inventory/consumption_report.html', context)


@login_required
def audit_log(request):
    queryset = AuditLog.objects.all()
    query = request.GET.get('q')
    action = request.GET.get('action')
    user = request.GET.get('user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if query:
        queryset = queryset.filter(object_repr__icontains=query)
    if action:
        queryset = queryset.filter(action=action)
    if user:
        queryset = queryset.filter(user_id=user)
    if date_from:
        queryset = queryset.filter(timestamp__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(timestamp__date__lte=date_to)

    paginator = Paginator(queryset, 50)
    page = request.GET.get('page')
    logs = paginator.get_page(page)

    context = {
        'logs': logs,
        'actions': AuditLog.ACTION_CHOICES,
        'users': User.objects.all(),
    }
    return render(request, 'inventory/audit_log.html', context)


@login_required
def api_compatible_supplies(request, printer_id):
    printer = get_object_or_404(Printer, pk=printer_id)
    compatible = Supply.objects.filter(
        printer_models=printer.printer_model,
        is_active=True
    ).values('id', 'name', 'sku', 'current_stock')

    supplies = []
    for s in compatible:
        supplies.append({
            'id': s['id'],
            'name': s['name'],
            'sku': s['sku'],
            'current_stock': s['current_stock']
        })

    return JsonResponse({'supplies': supplies})