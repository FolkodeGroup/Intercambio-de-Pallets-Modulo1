from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa
from django.db.models import Sum, Value, Case, When, F, Q
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
    # Obtenemos el término de búsqueda desde la URL (?q=...)
    search_query = request.GET.get('q', '')
    # Nuevos parámetros para saber qué tabla renderizar
    is_partial = request.GET.get('partial', 'false').lower() == 'true'
    view_mode = request.GET.get('view', 'simple')
    
    # Empezamos con el queryset base
    queryset = Empresa.objects.all()

    # Si hay un término de búsqueda, filtramos el queryset
    if search_query:
        queryset = queryset.filter(
            Q(razon_social__icontains=search_query) | 
            Q(cuit__icontains=search_query) |
            Q(direccion__icontains=search_query)
        )

    # Aplicamos los cálculos de balance al queryset (ya sea el original o el filtrado)
    empresas_con_balance = queryset.annotate(
        total_in=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'IN'), Value(0)),
        total_out=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'OUT'), Value(0))
    ).annotate(
        balance=F('total_in') - F('total_out')
    ).order_by('razon_social')

    # Si es una petición AJAX para actualizar la tabla
    if is_partial:
        if view_mode == 'complete':
            template_name = 'empresas/_tabla_empresas_completa.html'
        else:
            template_name = 'empresas/_tabla_empresas.html'
        return render(request, template_name, {'empresas': empresas_con_balance})

    # Si es la carga inicial de la página completa
    else:
        context = {
            'title': 'Gestión de Empresas',
            'empresas': empresas_con_balance,
            'search_query': search_query,
        }
        return render(request, 'empresas/lista_empresas.html', context)

def crear_empresa(request):
    """
    Gestiona la creación de una nueva empresa.
    - Muestra el formulario en una petición GET.
    - Procesa los datos del formulario en una petición POST.
    """
    if request.method == 'POST':
        razon_social = request.POST.get('razon_social')
        cuit = request.POST.get('cuit')
        tipo = request.POST.get('tipo')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        if not all([razon_social, cuit, tipo]):
            messages.error(request, 'Error: Razón Social, CUIT y Tipo son campos obligatorios.')
            context = {
                'form_data': request.POST,
                'header_title': 'Nueva Empresa',
                'title': 'Crear Empresa',
            }
            return render(request, 'empresas/crear_empresa.html', context)

        try:
            Empresa.objects.create(
                razon_social=razon_social,
                cuit=cuit,
                es_proveedor=(tipo == 'PROVEEDOR'), 
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

    context = {
        'header_title': 'Nueva Empresa',
        'title': 'Crear Empresa',
    }
    return render(request, 'empresas/crear_empresa.html', context)

def modificar_empresa(request, empresa_id):
    """
    Gestiona la modificación de una empresa existente.
    Reutiliza la plantilla del formulario de creación.
    """
    empresa = get_object_or_404(Empresa, pk=empresa_id)

    if request.method == 'POST':
        empresa.razon_social = request.POST.get('razon_social')
        empresa.cuit = request.POST.get('cuit')
        empresa.es_proveedor = (request.POST.get('tipo') == 'PROVEEDOR')
        empresa.telefono = request.POST.get('telefono')
        empresa.email = request.POST.get('email')
        empresa.direccion = request.POST.get('direccion')

        try:
            empresa.save()
            messages.success(request, f'¡Empresa "{empresa.razon_social}" actualizada exitosamente!')
            return redirect('empresas:lista_empresas')
        except Exception as e:
            messages.error(request, f'Error al actualizar la empresa: {e}')

    context = {
        'header_title': 'Modificar Empresa',
        'title': 'Modificar Empresa',
        'empresa': empresa, 
    }
    return render(request, 'empresas/crear_empresa.html', context)

def eliminar_empresa(request, empresa_id):
    """
    Elimina una empresa. Por seguridad, solo procesa peticiones POST.
    """
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    
    if request.method == 'POST':
        try:
            nombre_empresa = empresa.razon_social
            empresa.delete()
            messages.success(request, f'Empresa "{nombre_empresa}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la empresa: {e}. Es posible que tenga movimientos asociados.')
        
        return redirect('empresas:lista_empresas')

    return redirect('empresas:lista_empresas')