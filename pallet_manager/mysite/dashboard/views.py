# pallet_manager/mysite/dashboard/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from empleados.forms import EmpleadoCreationForm

from django.contrib.auth.decorators import login_required
from datetime import datetime
import random #genera balances mockeados
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from empresas.models import Empresa 
from pallets.models import Pallet 
from movimientos.views import _snapshot_stock

def index(request):
    return render(request, 'dashboard/index.html', {'title': 'Página Principal'})

class SignUpView(CreateView):
    form_class = EmpleadoCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'

    def form_valid(self, form):
        messages.success(self.request, "¡Registro exitoso! Ya puedes iniciar sesión.")
        return super().form_valid(form)

class RememberMeLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600) 
        return super().form_valid(form)

@login_required 
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
    
    _, contadores = _snapshot_stock()
    
    balance_stock = {
        'disponibles': contadores.get('disponibles', 0),
        'en_uso': contadores.get('en_uso', 0),
        'danados': contadores.get('danados', 0),
        'total': sum(contadores.values())
    }
    
    # --- CÁLCULO REAL DEL BALANCE POR EMPRESA ---
    # Usamos 'annotate' para agregar los campos calculados a cada empresa.
    balance_empresas = Empresa.objects.annotate(
        total_in=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'IN'), Value(0)),
        total_out=Coalesce(Sum('movimientos__lineas__cantidad', filter=F('movimientos__tipo') == 'OUT'), Value(0))
    ).annotate(
        balance=F('total_in') - F('total_out')
    ).order_by('-balance') # Ordenamos para ver los balances más altos primero
    
        
    es_admin = request.user.is_superuser

    context = {
        'header_title': 'Dashboard', 
        'title': 'Dashboard',
        'es_admin': es_admin,
        'header': datos_header,
        'balance_stock': balance_stock,
        'balance_empresas': balance_empresas,
    }

    return render(request, 'dashboard/home.html', context)