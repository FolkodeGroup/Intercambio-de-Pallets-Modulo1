from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from users.views import index, RememberMeLoginView, SignUpView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', index, name='index'),
    path('movimientos/', include('movimientos.urls', namespace='movimientos')),
    path("polls/", include("polls.urls")),
    path('empleados/', include('empleados.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),

    # Auth
    path('login/', RememberMeLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Reset de contraseña (opcional)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('empresas/', include('empresas.urls')), 

    # Registro (opcional)
    path('register/', SignUpView.as_view(), name='register'),

    # Home


]
# --- ALIAS DE COMPATIBILIDAD (no tocan el código de tus compañeros) ---
# Hace que {% url 'registrar_movimiento' %} funcione, redirigiendo a la ruta namespaced real.

# --- ALIAS DE COMPATIBILIDAD (no tocan el código de tus compañeros) ---
# Hace que {% url 'registrar_movimiento' %} funcione, redirigiendo a la ruta namespaced real.
urlpatterns += [
    path(
        'compat/registrar/',
        RedirectView.as_view(pattern_name='movimientos:registrar_movimiento', permanent=False),
        name='registrar_movimiento',   # <-- nombre "plano" que necesita la plantilla de tu compañero
    ),
    # Si el sidebar global usa estos nombres "planos", también los resolvemos sin tocar sus archivos:
    path('empresas/', RedirectView.as_view(url='/empresas/', permanent=False), name='empresas'),
    path('empleados/', RedirectView.as_view(url='/empleados/', permanent=False), name='empleados'),
]
