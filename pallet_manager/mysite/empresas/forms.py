from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razon_social', 
            'cuit', 
            'es_proveedor', 
            'condicion_iva', 
            'direccion', 
            'email', 
            'telefono'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la razón social'
            }),
            'cuit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese CUIT (11 dígitos)',
                'maxlength': '11'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@empresa.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(011) 1234-5678'
            }),
            'es_proveedor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'condicion_iva': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get('razon_social')
        if razon_social:
            razon_social = razon_social.strip()
            if len(razon_social) < 3:
                raise forms.ValidationError("La razón social debe tener al menos 3 caracteres.")
        return razon_social

    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')
        if cuit:
            # Validar que sea numérico y tenga 11 dígitos
            cuit = cuit.replace('-', '').replace('.', '').replace(' ', '')
            if not cuit.isdigit() or len(cuit) != 11:
                raise forms.ValidationError("El CUIT debe tener exactamente 11 dígitos numéricos.")
        return cuit

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email

    def clean(self):
        cleaned_data = super().clean()
        es_proveedor = cleaned_data.get('es_proveedor')
        email = cleaned_data.get('email')
        telefono = cleaned_data.get('telefono')

        # Validar que los proveedores tengan al menos un medio de contacto
        if es_proveedor and not email and not telefono:
            raise forms.ValidationError(
                "Los proveedores deben tener al menos un medio de contacto (teléfono o email)."
            )

        return cleaned_data