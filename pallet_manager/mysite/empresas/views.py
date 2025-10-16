from django.shortcuts import render
from .models import Empresa
from django.db.models import Sum, Value, Case, When, F
from django.db.models.functions import Coalesce
import random # Importamos random para generar datos de prueba

# Vista principal para la lista de empresas
def lista_empresas(request):
    """
    Muestra la página de gestión/listado de empresas, calculando los totales
    de movimientos (IN/OUT) y el balance para cada una.
    """
    # --- MODO DATOS REALES (Comentado temporalmente) ---
    # empresas_con_totales = Empresa.objects.annotate(
    #     total_in=Coalesce(Sum(
    #         Case(When(movimientos__tipo='IN', then=F('movimientos__lineas__cantidad')), default=Value(0))
    #     ), Value(0)),
    #     total_out=Coalesce(Sum(
    #         Case(When(movimientos__tipo='OUT', then=F('movimientos__lineas__cantidad')), default=Value(0))
    #     ), Value(0))
    # ).annotate(
    #     balance=F('total_in') - F('total_out')
    # )

    # --- MODO MOCK (Datos de prueba para visualización) ---
    empresas_con_totales = []
    for i in range(1, 11): # Generamos 10 empresas de ejemplo
        total_in = random.randint(50, 500)
        total_out = random.randint(50, 500)
        empresas_con_totales.append({
            'id': i, # Añadimos un ID para los enlaces del menú
            'razon_social': f'Empresa de Prueba {i}',
            'cuit': f'30{random.randint(10000000, 99999999)}9',
            'direccion': f'Calle Falsa {random.randint(100, 2000)}, Ciudad Ejemplo',
            'total_in': total_in,
            'total_out': total_out,
            'balance': total_in - total_out,
        })

    context = {
        'title': 'Gestión de Empresas',
        'empresas': empresas_con_totales,
    }

    return render(request, 'empresas/lista_empresas.html', context)