from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Supply, Printer, PrinterModel, Supplier, Delivery, DeliveryItem, SupplyInstallation, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'email', 'phone', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrinterModelForm(forms.ModelForm):
    class Meta:
        model = PrinterModel
        fields = ['name', 'manufacturer', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'printer_model', 'serial_number', 'custodian', 'status', 'location', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'printer_model': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'custodian': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'sku', 'description', 'printer_models', 'suppliers', 'current_stock', 'low_stock_threshold', 'max_stock_threshold', 'unit_price', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'printer_models': forms.SelectMultiple(attrs={'class': 'form-select', 'required': True}),
            'suppliers': forms.SelectMultiple(attrs={'class': 'form-select', 'required': True}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': '0'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': '0'}),
            'max_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['supplier', 'delivery_date', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['supply', 'quantity']
        widgets = {
            'supply': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


class DeliveryItemFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        supplies = []
        for form in self.forms:
            if form.cleaned_data.get('supply') in supplies:
                raise forms.ValidationError('Duplicate supply items are not allowed.')
            supplies.append(form.cleaned_data.get('supply'))


class InstallationForm(forms.ModelForm):
    class Meta:
        model = SupplyInstallation
        fields = ['printer', 'supply', 'notes']
        widgets = {
            'printer': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'supply': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DisposalForm(forms.ModelForm):
    class Meta:
        model = SupplyInstallation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }