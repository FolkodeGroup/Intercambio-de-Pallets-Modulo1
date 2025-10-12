from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

def index(request):
    
    from django.shortcuts import render
    return render(request, 'index.html')

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
