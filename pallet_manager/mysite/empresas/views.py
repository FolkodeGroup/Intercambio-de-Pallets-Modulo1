from django.shortcuts import render, redirect
from .models import Empresa
from django.db.models import Sum, Value, Case, When, F
from django.db.models.functions import Coalesce
import random # Importamos random para generar datos de prueba
from django.contrib import messages
from django.urls import reverse

# Vista principal para la lista de empresas
def lista_empresas(request):
    """
    Muestra la página de gestión/listado de empresas, calculando los totales
    de movimientos (IN/OUT) y el balance para cada una.
    """
    # --- MODO DATOS REALES CON CÁLCULOS ---
    # Usamos 'annotate' para agregar campos calculados a cada empresa.
    empresas_con_balance = Empresa.objects.annotate(
        # Suma las cantidades de las líneas de movimiento si el tipo es 'IN'
        total_in=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'IN'), Value(0)),
        # Suma las cantidades de las líneas de movimiento si el tipo es 'OUT'
        total_out=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'OUT'), Value(0))
    ).annotate(
        # Calcula el balance restando las salidas de las entradas
        balance=F('total_in') - F('total_out')
    ).order_by('razon_social')
    
    context = {
        'title': 'Gestión de Empresas',
        'header_title': 'Empresas', # Título para el encabezado principal
        # Pasamos la lista de empresas con los datos calculados a la plantilla
        'empresas': empresas_con_balance,
    }

    return render(request, 'empresas/lista_empresas.html', context)

def crear_empresa(request):
    """
    Gestiona la creación de una nueva empresa.
    - Muestra el formulario en una petición GET.
    - Procesa los datos del formulario en una petición POST.
    """
    if request.method == 'POST':
        # --- PROCESAR EL FORMULARIO ---
        razon_social = request.POST.get('razon_social')
        cuit = request.POST.get('cuit')
        tipo = request.POST.get('tipo') # 'CLIENTE' o 'PROVEEDOR'
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        # Validar que los campos obligatorios no estén vacíos
        if not all([razon_social, cuit, tipo]):
            messages.error(request, 'Error: Razón Social, CUIT y Tipo son campos obligatorios.')
            context = {
                'form_data': request.POST,
                'header_title': 'Nueva Empresa',
                'title': 'Crear Empresa',
            }
            # Devolvemos los datos ingresados para que el usuario no los pierda
            return render(request, 'empresas/crear_empresa.html', context)

        try:
            # Crear la nueva instancia del modelo Empresa
            Empresa.objects.create(
                razon_social=razon_social,
                cuit=cuit,
                es_proveedor=(tipo == 'PROVEEDOR'), # Convertimos el 'tipo' a un booleano
                telefono=telefono,
                email=email,
                direccion=direccion
            )
            messages.success(request, f'¡Empresa "{razon_social}" creada exitosamente!')
            return redirect('empresas:lista_empresas')

        except Exception as e:
            messages.error(request, f'Error al crear la empresa: {e}')
            context = {
                'form_data': request.POST,
                'header_title': 'Nueva Empresa',
                'title': 'Crear Empresa',
            }
            return render(request, 'empresas/crear_empresa.html', context)

    # --- MOSTRAR EL FORMULARIO VACÍO (petición GET) ---
    context = {
        'header_title': 'Nueva Empresa',
        'title': 'Crear Empresa',
    }
    return render(request, 'empresas/crear_empresa.html', context)