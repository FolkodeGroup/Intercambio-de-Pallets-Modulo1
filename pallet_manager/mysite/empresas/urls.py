from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    # Ruta principal para la lista de empresas
    path('', views.lista_empresas, name='lista_empresas'),
]