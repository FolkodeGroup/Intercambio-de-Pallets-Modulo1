# pallet_manager/mysite/dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random #genera balances mockeados
from empresas.models import Empresa #para obtener la lista real de empresas

@login_required #solo usuarios logueados accedan
def home(request):
    """
    Vista principal del Dashboard. 
    Prepara datos mockeados y datos reales para la renderización.
    """
    
    ahora = datetime.now()
    datos_header = {
        'fecha': ahora.strftime("%d/%m/%Y"), 
        'hora': ahora.strftime("%H:%M:%S"), 
        'usuario': request.user.get_username(),
    }
    
    #donut mockeado
    total_pallets = 10000
    balance_stock = {
        'total': total_pallets,
        'disponibles': 4500,
        'en_uso': 3000,
        'danados': 2500,
    }
    
    #balance por empresa
    #obtener empresas
    empresas_reales = Empresa.objects.all().order_by('razon_social')
    
    lista_balance_empresas = []
    
    for empresa in empresas_reales:
        total_in = random.randint(300, 1500)
        total_out = random.randint(300, 1500)
        balance_qty = total_in - total_out
        
        lista_balance_empresas.append({
            'nombre': empresa.razon_social,
            'total_in': total_in,
            'total_out': total_out,
            'balance': balance_qty,
            'es_proveedor': empresa.es_proveedor
        })
        
    es_admin = request.user.is_superuser

    context = {
        'header_title': 'Dashboard', # Título para el encabezado principal
        'title': 'Dashboard', # Título para la página (y como fallback)
        'es_admin': es_admin,
        'header': datos_header,
        'balance_stock': balance_stock,
        'balance_empresas': lista_balance_empresas,
    }

    return render(request, 'dashboard/home.html', context)