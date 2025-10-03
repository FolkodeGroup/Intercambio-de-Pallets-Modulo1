from django import forms
from .models import Movimiento, LineaMovimiento

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'empresa', 
            'tipo', 
            'ubicacion_origen', 
            'ubicacion_destino', 
            'doc_referencia', 
            'observaciones'
        ]
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese ubicación de origen'
            }),
            'ubicacion_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese ubicación de destino'
            }),
            'doc_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de remito'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
        }

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError("El tipo de movimiento es obligatorio.")
        return tipo

    def clean_empresa(self):
        empresa = self.cleaned_data.get('empresa')
        tipo = self.cleaned_data.get('tipo')
        
        if empresa and tipo:
            if tipo == Movimiento.TipoMovimiento.INGRESO and not empresa.es_proveedor:
                raise forms.ValidationError("Para ingresos, la empresa debe ser un proveedor.")
            if tipo == Movimiento.TipoMovimiento.EGRESO and empresa.es_proveedor:
                raise forms.ValidationError("Para egresos, la empresa no puede ser un proveedor.")
        
        return empresa

    def clean(self):
        cleaned_data = super().clean()
        ubicacion_origen = cleaned_data.get('ubicacion_origen')
        ubicacion_destino = cleaned_data.get('ubicacion_destino')

        if ubicacion_origen and ubicacion_destino and ubicacion_origen == ubicacion_destino:
            raise forms.ValidationError("La ubicación de origen y destino no pueden ser iguales.")

        return cleaned_data


class LineaMovimientoForm(forms.ModelForm):
    class Meta:
        model = LineaMovimiento
        fields = ['tipo_pallet', 'cantidad', 'motivo']
        widgets = {
            'tipo_pallet': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Cantidad'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motivo (Entrega, Devolución, etc.)'
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")
        return cantidad

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo:
            motivo = motivo.strip()
            if len(motivo) < 3:
                raise forms.ValidationError("El motivo debe tener al menos 3 caracteres.")
        return motivo