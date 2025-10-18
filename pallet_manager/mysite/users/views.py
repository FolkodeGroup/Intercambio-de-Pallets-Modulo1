from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.shortcuts import render

def index(request):
    # 1. Crea un diccionario llamado 'context'
    context = {
        'title': 'Dashboard Principal'  # <-- Aquí defines la variable y su valor
    }
    # 2. Pasa el diccionario como tercer argumento a render()
    return render(request, 'index.html', context)

class RememberMeLoginView(LoginView):
    template_name = "registration/login.html"
    def form_valid(self, form):
        resp = super().form_valid(form)
        remember = self.request.POST.get("remember_me")
        self.request.session.set_expiry(60*60*24*14 if remember else 0)  # 14 días o al cerrar
        return resp

class SignUpView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
