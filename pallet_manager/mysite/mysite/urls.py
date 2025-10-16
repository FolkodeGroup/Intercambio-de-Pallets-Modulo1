from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from users.views import index, RememberMeLoginView, SignUpView

urlpatterns = [
    path('movimientos/', include('movimientos.urls', namespace='movimientos')),
    path("polls/", include("polls.urls")),
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
    path('empleados/', include('empleados.urls')),
    path('', index, name='index'),
]
