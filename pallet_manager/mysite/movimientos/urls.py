from django.urls import path
from . import views

app_name = 'movimientos'

urlpatterns = [
    path('', views.movimientos, name='movimientos'),
    path('registrar/', views.registrar_movimiento, name='registrar_movimiento'),
]