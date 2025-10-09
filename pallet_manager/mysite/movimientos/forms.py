from django import forms
from .models import Movimiento, LineaMovimiento

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'empresa',
            'usuario_creacion',
            'tipo',
            'ubicacion_origen',
            'ubicacion_destino',
            'doc_referencia',
            'estado_confirmacion',
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
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return cantidad

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo and len(motivo.strip()) < 3:
            raise forms.ValidationError("El motivo debe tener al menos 3 caracteres.")
        return motivo
