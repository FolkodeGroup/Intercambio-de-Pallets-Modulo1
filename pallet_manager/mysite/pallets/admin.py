from django.contrib import admin

# Register your models here.


from .models import Pallet 

 

@admin.register(Pallet) 

class PalletAdmin(admin.ModelAdmin): 

    list_display = ("codigo", "material", "calidad", "estado", "norma_nimf15", "peso_max_kg", "activo", "created_at") 

    list_filter  = ("estado", "material", "calidad", "norma_nimf15", "activo") 

    search_fields = ("codigo",) 

    ordering = ("-created_at",) 

