from django.urls import path
from . import views

urlpatterns = [
    # URL para la lista de empleados (la que ya tenías)
    path('gestion/', views.vista_empleados, name='vista_empleados'),
    
    # ¡NUEVA URL para el formulario de creación!
    path('crear/', views.crear_empleado, name='crear_empleado'),
]
