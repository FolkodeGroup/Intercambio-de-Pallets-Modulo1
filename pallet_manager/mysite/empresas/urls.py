from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),

    path('crear/', views.crear_empresa, name='crear_empresa'), # /empresas/crear/

    path('modificar/<int:empresa_id>/', views.modificar_empresa, name='modificar_empresa'), # /empresas/modificar/1/
    path('eliminar/<int:empresa_id>/', views.eliminar_empresa, name='eliminar_empresa'), # /empresas/eliminar/1/
]