from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empleado

class EmpleadoCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Empleado
        fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar clases de Bootstrap y placeholders a todos los campos
        field_placeholders = {
            'username': 'nombre.apellido',
            'first_name': 'Nombre del empleado',
            'last_name': 'Apellido del empleado',
            'email': 'correo@ejemplo.com',
            'dni': 'Solo números, sin puntos',
            'telefono': '(011) 1234-5678',
            'password1': "Ingrese una contraseña",
            'password2': "Repita la contraseña"
        }

        for field_name, placeholder in field_placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholder
                })
        
        # Ocultar la ayuda de la contraseña, ya que Django la explica bien
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''


    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni and not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        return dni
