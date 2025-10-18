"""
URL configuration for mysite project.
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

# --- ¡CAMBIO CLAVE! ---
# Importamos las vistas desde 'dashboard.views' en lugar de la app 'users' que eliminamos.
from dashboard.views import index, RememberMeLoginView, SignUpView

urlpatterns = [
    # --- VISTAS PRINCIPALES Y DE AUTENTICACIÓN ---
    path('', index, name='index'),
    path('login/', RememberMeLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    
    # --- ADMIN Y APPS DEL PROYECTO ---
    path('admin/', admin.site.urls),
    path('empleados/', include('empleados.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('movimientos/', include('movimientos.urls', namespace='movimientos')),
    path('empresas/', include('empresas.urls')),
    # path("polls/", include("polls.urls")), # Si aún usas esta app, descomentala.

    # --- VISTAS PARA RESET DE CONTRASEÑA ---
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# --- ALIAS DE COMPATIBILIDAD (se mantienen como estaban para no romper nada) ---
urlpatterns += [
    path(
        'compat/registrar/',
        RedirectView.as_view(pattern_name='movimientos:registrar_movimiento', permanent=False),
        name='registrar_movimiento',
    ),
    # He corregido los nombres de los alias para evitar conflictos con las rutas reales
    path('compat/empresas/', RedirectView.as_view(url='/empresas/', permanent=False), name='empresas_compat'),
    path('compat/empleados/', RedirectView.as_view(url='/empleados/', permanent=False), name='empleados_compat'),
]

