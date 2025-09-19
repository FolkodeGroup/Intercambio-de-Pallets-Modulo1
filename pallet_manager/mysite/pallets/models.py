from django.db import models 

from django.core.validators import MinValueValidator 

from django.core.exceptions import ValidationError 

 

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

    ) 

    material = models.CharField(max_length=10, choices=Material.choices) 

    calidad = models.CharField(max_length=1, choices=Calidad.choices, default=Calidad.A) 

 

    norma_nimf15 = models.BooleanField( 

        "Cumple NIMF-15", 

        default=False, 

        help_text="Tratamiento fitosanitario exigido para exportación.", 

    ) 

 

    peso_max_kg = models.DecimalField( 

        "Peso máx. admitido (kg)", 

        max_digits=7, decimal_places=2, 

        validators=[MinValueValidator(1)] 

    ) 

 

    # Dimensiones estándar en milímetros (mm) 

    largo_mm = models.PositiveIntegerField("Largo (mm)", validators=[MinValueValidator(1)]) 

    ancho_mm = models.PositiveIntegerField("Ancho (mm)", validators=[MinValueValidator(1)]) 

    alto_mm  = models.PositiveIntegerField("Alto (mm)",  validators=[MinValueValidator(1)]) 

 

    # Vida útil estimada (opcional) 

    vida_util_meses = models.PositiveIntegerField("Vida útil (meses)", null=True, blank=True) 

 

    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.DISPONIBLE) 

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

        if self.largo_mm <= 0 or self.ancho_mm <= 0 or self.alto_mm <= 0: 

            raise ValidationError("Las dimensiones deben ser positivas.") 


