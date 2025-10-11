from django.urls import path
from . import views

urlpatterns = [
    path("movimientos/", views.movimientos, name="movimientos"),
    path("registrar_movimiento/", views.registrar_movimiento, name="registrar_movimiento"),
]