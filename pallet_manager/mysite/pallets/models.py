from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
 

class Pallet(models.Model): 

 
    class Material(models.TextChoices): 

        MADERA = "MADERA", "Madera" 

        PLASTICO = "PLASTICO", "Plástico" 

        METAL = "METAL", "Metal" 

 

    class Estado(models.TextChoices): 

        DISPONIBLE = "DISPONIBLE", "Disponible" 

        EN_USO = "EN_USO", "En uso" 

        EN_REPARACION = "EN_REPARACION", "En reparación" 

        BAJA = "BAJA", "Baja" 

 

    class Calidad(models.TextChoices): 

        A = "A", "A" 

        B = "B", "B" 

        C = "C", "C" 

 

    codigo = models.CharField(
        "Código",
        max_length=50,
        unique=True,
        help_text="Identificador único del pallet (etiqueta/QR).",
        error_messages={
            'unique': "Ya existe un pallet con este código.",
            'blank': "El código es obligatorio.",
        }
    )

    material = models.CharField(
        max_length=10, 
        choices=Material.choices,
        error_messages={
            'blank': "El material es obligatorio.",
        }
    )

    calidad = models.CharField(
        max_length=1, 
        choices=Calidad.choices, 
        default=Calidad.A,
        error_messages={
            'blank': "La calidad es obligatoria.",
        }
    )

    norma_nimf15 = models.BooleanField( 

        "Cumple NIMF-15", 

        default=False, 

        help_text="Tratamiento fitosanitario exigido para exportación.", 

    ) 

 

    peso_max_kg = models.DecimalField(
        "Peso máx. admitido (kg)",
        max_digits=7, 
        decimal_places=2,
        validators=[MinValueValidator(1)],
        error_messages={
            'invalid': "Ingrese un peso válido.",
        }
    )

 

    # Dimensiones estándar en milímetros (mm) 
    largo_mm = models.PositiveIntegerField(
        "Largo (mm)", 
        validators=[MinValueValidator(1)],
        error_messages={
            'invalid': "El largo debe ser un número positivo.",
        }
    )
    
    ancho_mm = models.PositiveIntegerField(
        "Ancho (mm)", 
        validators=[MinValueValidator(1)],
        error_messages={
            'invalid': "El ancho debe ser un número positivo.",
        }
    )
    
    alto_mm = models.PositiveIntegerField(
        "Alto (mm)",  
        validators=[MinValueValidator(1)],
        error_messages={
            'invalid': "El alto debe ser un número positivo.",
        }
    )

    # Vida útil estimada (opcional) 
    vida_util_meses = models.PositiveIntegerField(
        "Vida útil (meses)", 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
 

    estado = models.CharField(
        max_length=15, 
        choices=Estado.choices, 
        default=Estado.DISPONIBLE,
        error_messages={
            'blank': "El estado es obligatorio.",
        }
    )

    activo = models.BooleanField(default=True) 

 

    # Trazas 

    fecha_alta = models.DateField(auto_now_add=True) 

    fecha_baja = models.DateField(null=True, blank=True) 

    ultima_inspeccion = models.DateField(null=True, blank=True) 

 

    created_at = models.DateTimeField(auto_now_add=True, editable=False) 

    updated_at = models.DateTimeField(auto_now=True, editable=False) 

 

    class Meta: 

        ordering = ["-created_at"] 

        indexes = [ 

            models.Index(fields=["codigo"]), 

            models.Index(fields=["estado"]), 

        ] 

        verbose_name = "Pallet" 

        verbose_name_plural = "Pallets" 

 
    def __str__(self):
        return f"{self.codigo} ({self.material}, {self.calidad})"

    def clean(self):
        super().clean()
        
        # Validar dimensiones positivas
        if self.largo_mm <= 0 or self.ancho_mm <= 0 or self.alto_mm <= 0:
            raise ValidationError("Las dimensiones deben ser positivas.")
        
        # Validar que el peso máximo sea positivo
        if self.peso_max_kg <= 0:
            raise ValidationError("El peso máximo debe ser positivo.")
        
        # Validar que si está en baja, debe tener fecha de baja
        if self.estado == self.Estado.BAJA and self.fecha_baja is None:
            raise ValidationError("Los pallets dados de baja deben tener una fecha de baja.")
        
        # Validar que si no está activo, debe tener fecha de baja
        if not self.activo and self.fecha_baja is None:
            raise ValidationError("Los pallets inactivos deben tener una fecha de baja.")
        
        # Validar que si tiene fecha de baja, debe estar en estado BAJA
        if self.fecha_baja and self.estado != self.Estado.BAJA:
            raise ValidationError("Solo los pallets en estado 'Baja' pueden tener una fecha de baja.")
        
        # Validar que la vida útil no sea negativa
        if self.vida_util_meses and self.vida_util_meses <= 0:
            raise ValidationError("La vida útil debe ser positiva o dejarla en blanco.")
        
        # Validar que no se pueda dar de baja un pallet que está en uso
        if self.estado == self.Estado.EN_USO and not self.activo:
            raise ValidationError("No se puede dar de baja un pallet que está en uso.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
