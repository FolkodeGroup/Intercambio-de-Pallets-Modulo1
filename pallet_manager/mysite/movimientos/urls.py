from django.urls import path
from . import views

urlpatterns = [
    path("lista_movimientos/", views.lista_movimientos, name="lista_movimientos"),
    path("registrar_movimiento/", views.registrar_movimiento, name="registrar_movimiento"),
]