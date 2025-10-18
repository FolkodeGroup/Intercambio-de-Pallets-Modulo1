from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Empleado(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el User de Django.
    Agrega campos específicos para los empleados de la empresa.
    """
    
    dni_validator = RegexValidator(
        regex=r'^\d{7,8}$',
        message="El DNI debe tener entre 7 y 8 dígitos numéricos.",
        code='invalid_dni'
    )
    
    telefono_validator = RegexValidator(
        regex=r'^[\d\-\+\(\)\s]{7,20}$',
        message="El teléfono debe tener un formato válido.",
        code='invalid_telefono'
    )

    dni = models.CharField(
        max_length=8, 
        unique=True, 
        validators=[dni_validator],
        verbose_name="DNI",
        help_text="DNI del empleado (solo números).",
        error_messages={
            'unique': "Ya existe un empleado con este DNI.",
        }
    )
    
    telefono = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[telefono_validator],
        verbose_name="Teléfono"
    )

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.dni})"
