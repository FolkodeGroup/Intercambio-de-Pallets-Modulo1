from django.urls import path
from . import views

app_name = 'movimientos'

urlpatterns = [
    path('', views.movimientos, name='movimientos'),
    path('registrar/', views.registrar_movimiento, name='registrar_movimiento'),
    path('gestion-stock/', views.gestion_stock, name='gestion_stock'),
    path('gestion-stock/actualizar/', views.actualizar_stock, name='actualizar_stock'),
    path('stock/', views.gestion_stock, name='stock_alias'),
]
