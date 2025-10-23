from django.urls import path
from . import views

app_name = 'movimientos'

urlpatterns = [
    path('', views.movimientos, name='movimientos'),
    path('exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
    path("remito/<int:movimiento_id>/", views.ver_remito, name="ver_remito"),
    path('ingresar/', views.ingresar_movimiento, name='ingresar_movimiento'),
    path('registrar/', views.registrar_movimiento, name='registrar_movimiento'),
    path('gestion-stock/', views.gestion_stock, name='gestion_stock'),
    path('gestion-stock/actualizar/', views.actualizar_stock, name='actualizar_stock'),
    path('stock/', views.gestion_stock, name='stock_alias'),
    path("registrar-egreso/", views.registrar_egreso, name="registrar_egreso"),
]
