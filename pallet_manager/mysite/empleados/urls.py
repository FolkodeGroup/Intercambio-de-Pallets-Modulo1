from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_empleados, name='lista_empleados')
]
