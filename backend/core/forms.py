from django import forms
from .models import Cliente, Sucursal, Area


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre', 'descripcion', 'email', 'telefono',
            'direccion', 'ciudad', 'pais',
            'contacto_nombre', 'contacto_puesto', 'contacto_email', 'contacto_telefono',
            'ruc_nit', 'industria', 'empleados', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
            'contacto_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre contacto'}),
            'contacto_puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Puesto'}),
            'contacto_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email contacto'}),
            'contacto_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono contacto'}),
            'ruc_nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUC/NIT'}),
            'industria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industria'}),
            'empleados': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de empleados'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = [
            'nombre', 'descripcion', 'email', 'telefono',
            'direccion', 'ciudad', 'pais',
            'contacto_nombre', 'contacto_puesto', 'contacto_email', 'contacto_telefono',
            'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sucursal'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
            'contacto_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre contacto'}),
            'contacto_puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Puesto'}),
            'contacto_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email contacto'}),
            'contacto_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono contacto'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
