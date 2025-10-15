from django.urls import path
from . import views

urlpatterns = [
    # La URL '' corresponde a la raíz de la app (ej: /mi-modulo/)
    path('', views.home, name='home'),
]