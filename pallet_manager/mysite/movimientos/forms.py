from django import forms
from django.forms import BaseInlineFormSet
from .models import Movimiento, LineaMovimiento
from empresas.models import Empresa

from .models import Movimiento

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
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            }),
        }

class IngresoMovimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        # Primero: usar los help_text como placeholder
        for field in self.fields.values():
            if field.help_text:
                field.widget.attrs['placeholder'] = field.help_text
                
        self.fields["observaciones"].widget.attrs.update({
            "placeholder": "Escriba aquí las observaciones...",
            "rows": 3,
        })
        # Luego: eliminar los help_text para que no se muestren en el template
        for field in self.fields.values():
            field.help_text = None
        # 1. Filtramos el campo 'empresa' para mostrar solo proveedores
        self.fields['empresa'].queryset = Empresa.objects.filter(es_proveedor=True)
        self.fields['empresa'].label = "Proveedor"
        
        # 2. Ocultamos el campo 'tipo' y le asignamos el valor 'IN' por defecto
        self.fields['tipo'].initial = 'IN'
        self.fields['tipo'].widget = forms.HiddenInput()
        
    class Meta:
        model = Movimiento
        # Excluimos 'usuario_creacion' porque se asigna en la vista
        exclude = ['usuario_creacion', 'fecha_hora', 'estado_confirmacion']

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar los help_text de todos los campos
        for field in self.fields.values():
            field.help_text = None
    
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

class EgresoMovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        # Ajustá si en tu modelo estos nombres cambian
        exclude = ['usuario_creacion', 'fecha_hora', 'estado_confirmacion']
        #👇 Esto elimina cualquier help_text que venga del modelo
        help_texts = {
            "ubicacion_origen": "",
            "ubicacion_destino": "",
            "usuario_creacion": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Quitar cualquier resto de help_text por seguridad
        for field in self.fields.values():
            field.help_text = None
        
        # Aseguramos que exista el campo 'empresa' en el form
        if 'empresa' in self.fields:
            try:
                # Cliente = empresa que NO es proveedora
                self.fields['empresa'].queryset = Empresa.objects.filter(es_proveedor=False)
                self.fields['empresa'].label = "Cliente"
            except Exception:
                # Fallback por si algo raro pasa con el modelo/queryset
                self.fields['empresa'].queryset = Empresa.objects.all()
                self.fields['empresa'].label = "Empresa"

        # Fijar tipo OUT y ocultarlo si el modelo Movimiento tiene ese campo
        if 'tipo' in self.fields:
            self.fields['tipo'].initial = 'OUT'
            self.fields['tipo'].widget = forms.HiddenInput()
            
        # Placeholders y ajustes de estilo
        self.fields["ubicacion_origen"].widget.attrs["placeholder"] = "Galpón o dirección de origen"
        self.fields["ubicacion_destino"].widget.attrs["placeholder"] = "Galpón o dirección de destino"
        self.fields["observaciones"].widget.attrs.update({
            "placeholder": "Escriba aquí las observaciones...",
            "rows": 3,
        })

    