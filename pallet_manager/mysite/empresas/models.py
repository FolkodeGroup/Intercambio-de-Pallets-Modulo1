from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Empresa(models.Model):
    """
    Modelo que representa a un cliente, proveedor, o tercero asociado a los movimientos de pallets.
    """

    # Opciones para el campo 'condicion_iva'
    class CondicionIVA(models.TextChoices):
        RI = "RI", "Responsable Inscripto"
        MT = "MT", "Monotributo"
        EX = "EX", "Exento"
        CF = "CF", "Consumidor Final"

    # Validador para CUIT (debe tener 11 dígitos)
    cuit_validator = RegexValidator(
        regex=r'^\d{11}$',
        message="El CUIT debe tener exactamente 11 dígitos numéricos.",
        code='invalid_cuit'
    )

    # Validador para teléfono (puede tener formato flexible)
    telefono_validator = RegexValidator(
        regex=r'^[\d\-\+\(\)\s]{7,20}$',
        message="El teléfono debe tener entre 7 y 20 caracteres y contener solo dígitos, espacios, guiones, paréntesis y signo más.",
        code='invalid_telefono'
    )


    # --- CAMPOS DE IDENTIFICACIÓN ---
    
    # Razón social con validaciones
    razon_social = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Razón Social",
        help_text="Nombre legal o comercial de la empresa.",
        error_messages={
            'unique': "Ya existe una empresa con esta razón social.",
            'blank': "La razón social es obligatoria.",
            'max_length': "La razón social no puede exceder los 150 caracteres."
        }
    )
    
    # CUIT con validaciones
    cuit = models.CharField(
        max_length=11,
        unique=True,
        validators=[cuit_validator],
        verbose_name="CUIT",
        help_text="Número de Identificación Fiscal. Máximo 11 dígitos.",
        error_messages={
            'unique': "Ya existe una empresa con este CUIT.",
            'blank': "El CUIT es obligatorio.",
            'max_length': "El CUIT no puede exceder los 11 caracteres."
        }
    )

    # --- CAMPOS DE ROL Y CLASIFICACIÓN ---
    
    es_proveedor = models.BooleanField(
        default=False,
        verbose_name="¿Es Proveedor?",
        help_text="Marca si esta empresa actúa como proveedor de pallets/servicios."
    )

    condicion_iva = models.CharField(
        max_length=2,
        choices=CondicionIVA.choices,
        default=CondicionIVA.CF,
        verbose_name="Condición ante el IVA",
        error_messages={
            'blank': "La condición de IVA es obligatoria."
        }
    )

    # --- CAMPOS DE CONTACTO Y UBICACIÓN ---
    
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección Principal",
        error_messages={
            'blank': "La dirección es obligatoria.",
            'max_length': "La dirección no puede exceder los 255 caracteres."
        }
    )

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Correo Electrónico",
        error_messages={
            'invalid': "Ingrese un correo electrónico válido.",
            'max_length': "El correo electrónico no puede exceder los 100 caracteres."
        }
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[telefono_validator],
        verbose_name="Teléfono"
    )
    
    # --- METADATOS Y CLASE META ---
    
    fecha_alta = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Alta"
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['razon_social']

    def clean(self):
        """
        Validaciones personalizadas a nivel de modelo
        """
        super().clean()
        
        # Validar que si es proveedor, tenga información de contacto
        if self.es_proveedor:
            if not self.telefono and not self.email:
                raise ValidationError({
                    'telefono': 'Los proveedores deben tener al menos un medio de contacto (teléfono o email).',
                    'email': 'Los proveedores deben tener al menos un medio de contacto (teléfono o email).'
                })
        
        # Validar que no se pueda crear empresa sin razón social o CUIT
        if not self.razon_social:
            raise ValidationError({'razon_social': 'La razón social es obligatoria.'})
        
        if not self.cuit:
            raise ValidationError({'cuit': 'El CUIT es obligatorio.'})
        
        # Validar formato del CUIT (debe tener 11 dígitos)
        if self.cuit and not self.cuit.isdigit():
            raise ValidationError({'cuit': 'El CUIT debe contener solo dígitos numéricos.'})
        
        if self.cuit and len(self.cuit) != 11:
            raise ValidationError({'cuit': 'El CUIT debe tener exactamente 11 dígitos.'})

    def save(self, *args, **kwargs):
        """
        Override del método save para asegurar validaciones antes de guardar
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.razon_social} ({self.cuit})"