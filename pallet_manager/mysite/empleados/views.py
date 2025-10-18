from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmpleadoCreationForm # Asegúrate de importar el formulario que creamos
from .models import Empleado # Importa el modelo para la vista de listado

# Vista para mostrar la lista de empleados (modificada para mostrar datos reales)
def vista_empleados(request):
    empleados = Empleado.objects.all() # Ahora busca los empleados en la base de datos
    context = {
        'empleados': empleados,
        'title': 'Gestión de Empleados'
    }
    return render(request, 'empleados/vista_empleados.html', context)

# --- ¡NUEVA VISTA PARA CREAR EMPLEADOS! ---
def crear_empleado(request):
    if request.method == 'POST':
        # Si el método es POST, se enviaron datos.
        # Creamos una instancia del formulario con los datos recibidos.
        form = EmpleadoCreationForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guardamos el nuevo empleado.
            form.save()
            # Creamos un mensaje de éxito para mostrar en la siguiente página.
            messages.success(request, '¡El empleado ha sido creado exitosamente!')
            # Redirigimos al usuario a la lista de empleados.
            return redirect('vista_empleados')
    else:
        # Si el método es GET, es la primera vez que se carga la página.
        # Creamos una instancia del formulario vacío.
        form = EmpleadoCreationForm()

    # Preparamos el contexto para pasarlo al template.
    context = {
        'form': form,
        'title': 'Crear Nuevo Empleado'
    }
    # Renderizamos el template con el formulario.
    return render(request, 'empleados/crear_empleado.html', context)
