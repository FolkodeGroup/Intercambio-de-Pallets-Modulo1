from django.db import models
from django.conf import settings # Para acceder a AUTH_USER_MODEL
from django.core.validators import MinValueValidator 

# Importaciones de modelos ya existentes
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
        on_delete=models.PROTECT, # No permite borrar la Empresa si tiene movimientos asociados
        related_name='movimientos',
        verbose_name='Empresa Asociada',
    )
    
    # 2. Relación a Usuario Creador (Empleado/Admin)
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # No permite borrar el usuario si tiene movimientos
        related_name='movimientos_creados',
        verbose_name='Usuario Creador',
        help_text='Usuario que registró el movimiento en el sistema.'
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
    )

    ubicacion_origen = models.CharField(
        max_length=255,
        verbose_name='Ubicación de Origen',
        help_text='Galpón propio o dirección de la empresa de origen.',
    )

    ubicacion_destino = models.CharField(
        max_length=255,
        verbose_name='Ubicación de Destino',
        help_text='Galpón propio o dirección de la empresa a donde llega el pallet.',
    )

    doc_referencia = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Número de Remito / Documento',
    )

    estado_confirmacion = models.CharField(
        max_length=10,
        choices=EstadoConfirmacion.choices,
        default=EstadoConfirmacion.PENDIENTE,
        verbose_name='Estado de Confirmación',
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


# --- 2. Modelo LineaMovimiento (Detalle) ---

class LineaMovimiento(models.Model):
    """
    Representa el detalle de un movimiento, indicando cantidad y tipo de pallet (Calidad).
    """

    # --- RELACIONES ---
    
    # Relación a la Cabecera (Movimiento)
    movimiento = models.ForeignKey(
        Movimiento,
        on_delete=models.CASCADE, # Si se borra el Movimiento, se borran automáticamente todas sus líneas
        related_name='lineas',
        verbose_name='Movimiento Asociado',
    )
    
    # --- CAMPOS DE DATOS ---

    # Reutilizamos las opciones de Calidad del modelo Pallet (A, B, C)
    tipo_pallet = models.CharField(
        max_length=1,
        choices=Pallet.Calidad.choices, # Usamos la clase de Pallet
        verbose_name='Tipo de Pallet (Calidad)',
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], # Asegura que la cantidad sea siempre 1 o mayor
        verbose_name='Cantidad',
        help_text='La cantidad de pallets de este tipo en la transacción.',
    )

    motivo = models.CharField(
        max_length=100,
        verbose_name='Motivo',
        help_text='(Entrega, Devolución, Reparación, etc.)',
    )
    
    # --- METADATOS ---
    class Meta:
        verbose_name = "Línea de Movimiento (Detalle)"
        verbose_name_plural = "Líneas de Movimiento (Detalles)"

    def __str__(self):
        return f"Línea de {self.movimiento.tipo} - {self.cantidad} x {self.tipo_pallet}"