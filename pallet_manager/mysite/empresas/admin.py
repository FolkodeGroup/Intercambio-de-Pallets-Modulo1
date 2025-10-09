# pallet_manager/mysite/empresas/admin.py

from django.contrib import admin
from .models import Empresa

# Configuramos cómo se mostrará el modelo Empresa en el Admin
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "cuit", "es_proveedor", "condicion_iva", "fecha_alta")
    list_filter = ("es_proveedor", "condicion_iva")
    search_fields = ("razon_social", "cuit")
    ordering = ("razon_social",)