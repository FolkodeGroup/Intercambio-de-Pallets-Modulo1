from django.shortcuts import render
from .models import Empresa
from .forms import EmpresaForm
from django.db.models import Sum, Value, Case, When, F
from django.db.models.functions import Coalesce
import random # Importamos random para generar datos de prueba
from django.shortcuts import render, redirect
from django.contrib import messages  # <-- Importa messages


# empresas/views.py

from django.shortcuts import render, redirect
from django.contrib import messages  # <-- Importa messages
from .models import Empresa
from .forms import EmpresaForm       # <-- ¡Importa tu formulario!
# ... (otros imports)


# --- Tu vista 'lista_empresas' (la dejo como referencia) ---
def lista_empresas(request):
    # ... (tu lógica de lista_empresas)
    
    # --- MODO DATOS REALES (Descomenta esto cuando funcione) ---
    # empresas_con_totales = Empresa.objects.annotate(...)
    
    # --- MODO MOCK (El que estás usando ahora) ---
    empresas_con_totales = []
    for i in range(1, 11): 
        total_in = random.randint(50, 500)
        total_out = random.randint(50, 500)
        empresas_con_totales.append({
            'id': i, 
            'razon_social': f'Empresa de Prueba {i}',
            'cuit': f'30{random.randint(10000000, 99999999)}9',
            'direccion': f'Calle Falsa {random.randint(100, 2000)}, Ciudad Ejemplo',
            'total_in': total_in,
            'total_out': total_out,
            'balance': total_in - total_out,
        })

    context = {
        'title': 'Gestión de Empresas',
        'header_title': 'Empresas', 
        'empresas': empresas_con_totales,
    }
    return render(request, 'empresas/lista_empresas.html', context)


# --- VISTA 'crear_empresa' (¡LA CORRECCIÓN!) ---

def crear_empresa(request):
    """
    Muestra Y PROCESA el formulario para crear una nueva empresa.
    """
    if request.method == 'POST':
        # 1. Rellena el formulario con los datos del POST
        form = EmpresaForm(request.POST)
        
        # 2. Valida el formulario
        if form.is_valid():
            # 3. Guarda la nueva empresa en la BD
            form.save()
            messages.success(request, f"Empresa '{form.cleaned_data['razon_social']}' creada exitosamente.")
            
            # 4. Redirige a la lista
            return redirect('empresas:lista_empresas')
        else:
            # Si hay errores, se los muestra al usuario
            messages.error(request, "Error al crear la empresa. Revisa los campos.")
    else:
        # Si es GET, muestra un formulario vacío
        form = EmpresaForm()

    context = {
        'title': 'Nueva Empresa',
        'header_title': 'Empresas',
        'form': form  # <-- Pasa el formulario al contexto
    }
    return render(request, 'empresas/crear_empresa.html', context)