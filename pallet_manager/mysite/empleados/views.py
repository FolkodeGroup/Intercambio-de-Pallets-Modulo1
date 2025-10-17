from django.shortcuts import render

# Create your views here.
def vista_empleados(request):
    empleados = []
    context = {
        'empleados': empleados,
        'title': 'Empleados'  # <-- Añadimos el título aquí
    }
    return render(request, 'empleados/vista_empleados.html', context)