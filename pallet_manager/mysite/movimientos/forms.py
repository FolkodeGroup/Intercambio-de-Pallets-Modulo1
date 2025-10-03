from django import forms
from .models import Movimiento, LineaMovimiento
import re

# Formulario para la cabecera
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

    def clean_empresa(self):
        empresa = self.cleaned_data.get('empresa')
        if not empresa:
            raise forms.ValidationError("Debe seleccionar una empresa.")
        return empresa

    def clean_usuario_creacion(self):
        usuario = self.cleaned_data.get('usuario_creacion')
        if not usuario:
            raise forms.ValidationError("Debe asignar un usuario creador.")
        return usuario

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if tipo not in ['IN', 'OUT']:
            raise forms.ValidationError("Debe seleccionar un tipo de movimiento válido.")
        return tipo

    def clean_ubicacion_origen(self):
        origen = self.cleaned_data.get('ubicacion_origen')
        if not origen or len(origen.strip()) < 3:
            raise forms.ValidationError("La ubicación de origen es obligatoria y debe tener al menos 3 caracteres.")
        return origen

    def clean_ubicacion_destino(self):
        destino = self.cleaned_data.get('ubicacion_destino')
        if not destino or len(destino.strip()) < 3:
            raise forms.ValidationError("La ubicación de destino es obligatoria y debe tener al menos 3 caracteres.")
        return destino

    def clean_doc_referencia(self):
        doc = self.cleaned_data.get('doc_referencia')
        if doc and not re.match(r'^[\w-]{1,50}$', doc):
            raise forms.ValidationError("Número de documento inválido. Máximo 50 caracteres alfanuméricos o guiones.")
        return doc

    def clean_estado_confirmacion(self):
        estado = self.cleaned_data.get('estado_confirmacion')
        if estado not in ['PENDIENTE', 'CONFIRMADO', 'CANCELADO']:
            raise forms.ValidationError("Debe seleccionar un estado de confirmación válido.")
        return estado

    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones')
        if obs and len(obs.strip()) > 500:
            raise forms.ValidationError("Las observaciones no pueden superar los 500 caracteres.")
        return obs

    def clean(self):
        cleaned_data = super().clean()
        origen = cleaned_data.get("ubicacion_origen")
        destino = cleaned_data.get("ubicacion_destino")
        if origen and destino and origen == destino:
            raise forms.ValidationError("La ubicación de origen y destino no pueden ser iguales.")
        return cleaned_data


# Formulario para las líneas (detalle)
class LineaMovimientoForm(forms.ModelForm):
    class Meta:
        model = LineaMovimiento
        fields = ['tipo_pallet', 'cantidad', 'motivo']
    
    def clean_tipo_pallet(self):
        tipo = self.cleaned_data.get('tipo_pallet')
        if tipo not in ['A', 'B', 'C']:
            raise forms.ValidationError("Debe seleccionar un tipo de pallet válido (A, B o C).")
        return tipo

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return cantidad

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if not motivo or len(motivo.strip()) < 3:
            raise forms.ValidationError("El motivo es obligatorio y debe tener al menos 3 caracteres.")
        return motivo
