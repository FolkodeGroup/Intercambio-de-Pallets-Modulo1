from django.db import models
from django.conf import settings # Para acceder a AUTH_USER_MODEL
from django.core.validators import MinValueValidator 
from django.core.exceptions import ValidationError
from empresas.models import Empresa # Importa el modelo Empresa
from pallets.models import Pallet # Importa el modelo Pallet para reutilizar opciones


# --- 1. Modelo Movimiento (Cabecera) ---

class Movimiento(models.Model):
    """
    Representa la cabecera de una transacción de pallets (remito IN/OUT).
    Contiene la información general de la operación.
    """

    # Opciones de Tipo de Movimiento
    class TipoMovimiento(models.TextChoices):
        INGRESO = "IN", "Ingreso"
        EGRESO = "OUT", "Egreso"

    # Opciones de Estado de Confirmación (Clave para impactar stock)
    class EstadoConfirmacion(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente de Confirmación"
        CONFIRMADO = "CONFIRMADO", "Confirmado"
        CANCELADO = "CANCELADO", "Cancelado"

    # --- RELACIONES (Claves Foráneas) ---

    # 1. Relación a Empresa (Cliente/Proveedor)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Empresa Asociada',
        error_messages={
            'null': "La empresa es obligatoria.",
        }
    )
    
    # 2. Relación a Usuario Creador (Empleado/Admin)
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos_creados',
        verbose_name='Usuario Creador',
        help_text='Usuario que registró el movimiento en el sistema.',
        error_messages={
            'null': "El usuario creador es obligatorio.",
        }
    )
    
    # --- CAMPOS DE DATOS ---

    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora',
    )

    tipo = models.CharField(
        max_length=5,
        choices=TipoMovimiento.choices,
        verbose_name='Tipo de Movimiento',
        error_messages={
            'blank': "El tipo de movimiento es obligatorio.",
        }
    )

    ubicacion_origen = models.CharField(
        max_length=255,
        verbose_name='Ubicación de Origen',
        help_text='Galpón propio o dirección de la empresa de origen.',
        error_messages={
            'blank': "La ubicación de origen es obligatoria.",
            'max_length': "La ubicación de origen no puede exceder los 255 caracteres.",
        }
    )

    ubicacion_destino = models.CharField(
        max_length=255,
        verbose_name='Ubicación de Destino',
        help_text='Galpón propio o dirección de la empresa a donde llega el pallet.',
        error_messages={
            'blank': "La ubicación de destino es obligatoria.",
            'max_length': "La ubicación de destino no puede exceder los 255 caracteres.",
        }
    )


    doc_referencia = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Número de Remito / Documento',
        error_messages={
            'max_length': "El documento de referencia no puede exceder los 50 caracteres.",
        }
    )

    estado_confirmacion = models.CharField(
        max_length=10,
        choices=EstadoConfirmacion.choices,
        default=EstadoConfirmacion.PENDIENTE,
        verbose_name='Estado de Confirmación',
        error_messages={
            'blank': "El estado de confirmación es obligatorio.",
        }
    )
    # Campo Observaciones no está en la lista final, pero es útil para auditoría
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name='Observaciones',
    )


    # --- METADATOS ---
    class Meta:
        verbose_name = "Movimiento (Cabecera)"
        verbose_name_plural = "Movimientos (Cabeceras)"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Mov. N°{self.id} | {self.tipo} ({self.empresa.razon_social})" # Usa la razón social de la FK

    def clean(self):
        super().clean()
        
        # Validar que la ubicación de origen y destino no sean iguales
        if self.ubicacion_origen == self.ubicacion_destino:
            raise ValidationError("La ubicación de origen y destino no pueden ser iguales.")
        
        # Validar que para ingresos, la empresa sea proveedor
        if self.tipo == self.TipoMovimiento.INGRESO:
            if not self.empresa.es_proveedor:
                raise ValidationError("Para ingresos, la empresa debe ser un proveedor.")
        
        # Validar que para egresos, la empresa no sea proveedor
        if self.tipo == self.TipoMovimiento.EGRESO:
            if self.empresa.es_proveedor:
                raise ValidationError("Para egresos, la empresa no puede ser un proveedor.")
        
        # Validar que no se puedan modificar movimientos confirmados
        if self.pk and self.estado_confirmacion == self.EstadoConfirmacion.CONFIRMADO:
            original = Movimiento.objects.get(pk=self.pk)
            if original.estado_confirmacion == self.EstadoConfirmacion.CONFIRMADO:
                raise ValidationError("No se puede modificar un movimiento confirmado.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# --- 2. Modelo LineaMovimiento (Detalle) ---

class LineaMovimiento(models.Model):
    """
    Representa el detalle de un movimiento, indicando cantidad y tipo de pallet (Calidad).
    """

    # --- RELACIONES ---
    
    # Relación a la Cabecera (Movimiento)
    movimiento = models.ForeignKey(
        Movimiento,
        on_delete=models.CASCADE,
        related_name='lineas',
        verbose_name='Movimiento Asociado',
        error_messages={
            'null': "El movimiento asociado es obligatorio.",
        }
    )
    
    # --- CAMPOS DE DATOS ---

    # Reutilizamos las opciones de Calidad del modelo Pallet (A, B, C)
    tipo_pallet = models.CharField(
        max_length=1,
        choices=Pallet.Calidad.choices,
        verbose_name='Tipo de Pallet (Calidad)',
        error_messages={
            'blank': "El tipo de pallet es obligatorio.",
        }
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad',
        help_text='La cantidad de pallets de este tipo en la transacción.',
        error_messages={
            'invalid': "La cantidad debe ser un número positivo.",
        }
    )

    motivo = models.CharField(
        max_length=100,
        verbose_name='Motivo',
        help_text='(Entrega, Devolución, Reparación, etc.)',
        error_messages={
            'blank': "El motivo es obligatorio.",
            'max_length': "El motivo no puede exceder los 100 caracteres.",
        }
    )
    
    # --- METADATOS ---
    class Meta:
        verbose_name = "Línea de Movimiento (Detalle)"
        verbose_name_plural = "Líneas de Movimiento (Detalles)"

    def __str__(self):
        return f"Línea de {self.movimiento.tipo} - {self.cantidad} x {self.tipo_pallet}"
    
    def clean(self):
        super().clean()
        
        # Validar que la cantidad no sea cero o negativa
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)