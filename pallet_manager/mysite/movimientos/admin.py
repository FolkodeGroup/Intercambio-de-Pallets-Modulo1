from django.contrib import admin


# Register your models here.

'''
Esto es solo para que el admin visualice los movimientos
(lo uso para verificar que el formulario permita registrar los movimientos correctamente)
'''
from .models import Movimiento, LineaMovimiento
# Inline para mostrar las líneas de cada movimiento
class LineaMovimientoInline(admin.TabularInline):
    model = LineaMovimiento
    fields = ('tipo_pallet', 'cantidad', 'motivo')
    readonly_fields = ('tipo_pallet', 'cantidad', 'motivo')
    can_delete = False
    extra = 0  # No mostrar filas vacías

# Admin solo de lectura para Movimientos
@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'empresa', 'usuario_creacion', 'fecha_hora', 'estado_confirmacion')
    list_filter = ('tipo', 'estado_confirmacion', 'fecha_hora', 'empresa')
    search_fields = ('empresa__razon_social', 'doc_referencia', 'ubicacion_origen', 'ubicacion_destino')
    ordering = ('-fecha_hora',)
    inlines = [LineaMovimientoInline]
    readonly_fields = (
        'empresa',
        'usuario_creacion',
        'fecha_hora',
        'tipo',
        'ubicacion_origen',
        'ubicacion_destino',
        'doc_referencia',
        'estado_confirmacion',
        'observaciones',
    )

    def has_add_permission(self, request):
        return False  # No permite agregar nuevos movimientos desde el admin

    def has_change_permission(self, request, obj=None):
        return False  # No permite editar movimientos

    def has_delete_permission(self, request, obj=None):
        return False  # No permite borrar movimientos