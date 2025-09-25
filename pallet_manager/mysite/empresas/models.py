from django.db import models

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

    # --- CAMPOS DE IDENTIFICACIÓN ---
    
    # Razón social con restricción de unicidad para evitar duplicados
    razon_social = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Razón Social",
        help_text="Nombre legal o comercial de la empresa."
    )
    
    # CUIT con restricción de unicidad
    cuit = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="CUIT",
        help_text="Número de Identificación Fiscal. Máximo 11 dígitos."
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
        verbose_name="Condición ante el IVA"
    )

    # --- CAMPOS DE CONTACTO Y UBICACIÓN ---
    
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección Principal"
    )

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Correo Electrónico"
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
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

    def __str__(self):
        return f"{self.razon_social} ({self.cuit})"