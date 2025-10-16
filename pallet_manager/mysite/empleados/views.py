from django.shortcuts import render

# Create your views here.
def vista_empleados(request):
    empleados = []
    return render(request, 'empleados/vista_empleados.html', {'empleados': empleados})