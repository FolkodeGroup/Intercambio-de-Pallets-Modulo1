from django.contrib import admin
from .models import Pallet

@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    """
    Configuración para mostrar el modelo Pallet en el panel de administración.
    """
    list_display = ('id', 'calidad', 'estado', 'fecha_alta')
    list_filter = ('estado', 'calidad')
    search_fields = ('id',)
    ordering = ('-fecha_alta',)
    readonly_fields = ('fecha_alta',)