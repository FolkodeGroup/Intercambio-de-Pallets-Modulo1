from django.shortcuts import render

# Create your views here.
def listar_empleados(request):
    empleados = []
    return render(request, 'empleados/lista_empleados.html', {'empleados': empleados})