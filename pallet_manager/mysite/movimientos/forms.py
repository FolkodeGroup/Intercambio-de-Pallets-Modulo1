from django import forms
from django.forms import BaseInlineFormSet
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


class LineaMovimientoForm(forms.ModelForm):
    class Meta:
        model = LineaMovimiento
        fields = ['tipo_pallet', 'cantidad', 'motivo']
        widgets = {
            'tipo_pallet': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ingrese cantidad de pallets'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Entrega, Devolución, Reparación...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        cantidad = self.cleaned_data.get('cantidad')
        motivo = self.cleaned_data.get('motivo')
        
        #Validar cantidad
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        
        #Validar motivo
        if motivo and len(motivo.strip()) < 3:
            raise forms.ValidationError("El motivo debe tener al menos 3 caracteres.")

        return cleaned_data
    
class LineaMovimientoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # self.instance es el Movimiento padre
        if self.instance and self.instance.estado_confirmacion == Movimiento.EstadoConfirmacion.CONFIRMADO:
            raise forms.ValidationError("No se pueden modificar líneas de un movimiento confirmado.")