# Validaciones Implementadas

## Validaciones a nivel de modelo (models.py)

### Validaciones de campos:
- **Razón Social**: Campo obligatorio, único, máximo 150 caracteres
- **CUIT**: Campo obligatorio, único, exactamente 11 dígitos numéricos
- **Dirección**: Campo obligatorio, máximo 255 caracteres
- **Email**: Campo opcional, formato de email válido
- **Teléfono**: Campo opcional, formato flexible (7-20 caracteres)
- **Condición IVA**: Campo obligatorio, valores predefinidos

### Validaciones personalizadas (`clean()` method):
- Validación de formato del CUIT (solo dígitos, 11 caracteres)
- Validación para proveedores: deben tener al menos un medio de contacto (teléfono o email)
- Validación de campos obligatorios

### Validadores con Regex:
- **CUIT**: `^\d{11}$` - Asegura 11 dígitos numéricos
- **Teléfono**: `^[\d\-\+\(\)\s]{7,20}$` - Permite dígitos, espacios, guiones, paréntesis y signo más

## Validaciones a nivel de formulario (forms.py)

### Validaciones de formulario:
- Validación de longitud mínima para razón social (3 caracteres)
- Limpieza y validación del CUIT
- Validación de proveedores (deben tener contacto)
- Validación de email (formato correcto, minúsculas)

## Mostrar errores en el frontend

Los errores se muestran en el template con el siguiente patrón:
- Mensajes generales de Django (`messages`)
- Errores específicos de cada campo
- Estilos de Bootstrap para errores visibles
- Validaciones en tiempo real en el formulario

## Criterios de aceptación cumplidos

✅ Las validaciones funcionan y evitan datos inconsistentes  
✅ Los errores se muestran correctamente al usuario  
✅ Validaciones en modelo y formulario  
✅ Documentación de todas las validaciones en este README