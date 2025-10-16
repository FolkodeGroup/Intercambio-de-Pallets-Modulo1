from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),

    path('crear/', views.crear_empresa, name='crear_empresa'),

]