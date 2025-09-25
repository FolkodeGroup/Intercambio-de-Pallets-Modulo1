# pallet_manager/mysite/movimientos/admin.py

from django.contrib import admin
from .models import Movimiento, LineaMovimiento

# 1. Definimos el Inline para LineaMovimiento (permite editar el detalle dentro de la cabecera)
class LineaMovimientoInline(admin.TabularInline):
    model = LineaMovimiento
    extra = 1  # Muestra 1 línea vacía para agregar un nuevo detalle
    # Campos que el usuario puede editar en el inline
    fields = ('tipo_pallet', 'cantidad', 'motivo')


# 2. Registramos el modelo Movimiento e incluimos el Inline
@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "empresa", "estado_confirmacion", "usuario_creacion", "fecha_hora")
    list_filter = ("tipo", "estado_confirmacion", "empresa")
    search_fields = ("doc_referencia", "empresa__razon_social")
    ordering = ("-fecha_hora",)
    inlines = [LineaMovimientoInline] # Agregamos el detalle al formulario de la cabecera
    
    # Campo 'usuario_creacion' se auto-completa al guardar
    def save_model(self, request, obj, form, change):
        if not change: # Solo al crear el objeto por primera vez
            obj.usuario_creacion = request.user
        super().save_model(request, obj, form, change)