# pallet_manager/mysite/dashboard/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from empleados.forms import EmpleadoCreationForm

# estos de abajo ya estaban aca
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random #genera balances mockeados
from empresas.models import Empresa #para obtener la lista real de empresas

# 1. Vista para la página principal (el 'index')
def index(request):
    # Aquí puedes agregar la lógica que tenías en tu vista index original.
    # Por ahora, simplemente renderizamos una plantilla.
    return render(request, 'dashboard/index.html', {'title': 'Página Principal'})

# 2. Vista para el registro de nuevos usuarios (ahora son Empleados)
class SignUpView(CreateView):
    form_class = EmpleadoCreationForm
    success_url = reverse_lazy('login') # Redirige al login después de un registro exitoso
    template_name = 'registration/register.html'

    def form_valid(self, form):
        messages.success(self.request, "¡Registro exitoso! Ya puedes iniciar sesión.")
        return super().form_valid(form)

class RememberMeLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0) # Expira al cerrar el navegador
        else:
            self.request.session.set_expiry(1209600) # 2 semanas de sesión
        return super().form_valid(form)

@login_required #solo usuarios logueados accedan
def home(request):
    """
    Vista principal del Dashboard. 
    Prepara datos mockeados y datos reales para la renderización.
    """
    
    ahora = datetime.now()
    datos_header = {
        'fecha': ahora.strftime("%d/%m/%Y"), 
        'hora': ahora.strftime("%H:%M:%S"), 
        'usuario': request.user.get_username(),
    }
    
    #donut mockeado
    total_pallets = 10000
    balance_stock = {
        'total': total_pallets,
        'disponibles': 4500,
        'en_uso': 3000,
        'danados': 2500,
    }
    
    #balance por empresa
    #obtener empresas
    empresas_reales = Empresa.objects.all().order_by('razon_social')
    
    lista_balance_empresas = []
    
    for empresa in empresas_reales:
        total_in = random.randint(300, 1500)
        total_out = random.randint(300, 1500)
        balance_qty = total_in - total_out
        
        lista_balance_empresas.append({
            'nombre': empresa.razon_social,
            'total_in': total_in,
            'total_out': total_out,
            'balance': balance_qty,
            'es_proveedor': empresa.es_proveedor
        })
        
    es_admin = request.user.is_superuser

    context = {
        'header_title': 'Dashboard', # Título para el encabezado principal
        'title': 'Dashboard', # Título para la página (y como fallback)
        'es_admin': es_admin,
        'header': datos_header,
        'balance_stock': balance_stock,
        'balance_empresas': lista_balance_empresas,
    }

    return render(request, 'dashboard/home.html', context)