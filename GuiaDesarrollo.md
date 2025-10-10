

# Guía de Desarrollo: Creando un Nuevo Módulo (App) en Django

Este documento describe el procedimiento estándar para añadir una nueva funcionalidad (una "app") a nuestro proyecto Django. Seguir estos pasos asegura que el código esté organizado, sea modular y que podamos trabajar en paralelo sin conflictos.

## Resumen del Flujo Básico

El ciclo para mostrar una página en Django es:

**URL del Navegador** → **URLs del Proyecto** → **URLs de la App** → **Vista (View)** → **Plantilla (Template)**

---

### Paso 1: Crear la App

Cada nueva funcionalidad principal debe vivir en su propia "app".

1.  Abre la terminal en el directorio donde está `manage.py`.
2.  Ejecuta el comando `startapp`.

    ```bash
    # Sintaxis: python manage.py startapp <nombre_de_la_app>
    python manage.py startapp tu_app
    ```
    *Reemplaza `tu_app` por el nombre de la funcionalidad que desarrollarás (ej: `proveedores`, `clientes`, etc.)*

### Paso 2: Registrar la App

Django necesita saber que esta nueva app existe.

1.  Abre el archivo de configuración principal: `pallet_manager/mysite/mysite/settings.py`.
2.  Añade el nombre de tu nueva app a la lista `INSTALLED_APPS`.

    ```python
    # pallet_manager/mysite/mysite/settings.py

    INSTALLED_APPS = [
        # ... apps de Django
        'pallet_manager',
        # --- NUESTRAS APPS ---
        'tu_app',  # <-- AÑADIR AQUÍ LA NUEVA APP
    ]
    ```

### Paso 3: Crear una Vista simple (`views.py`)

La vista es una función de Python que recibe una petición y decide qué HTML mostrar. Por ahora, solo haremos que muestre una plantilla vacía.

1.  Abre el archivo `tu_app/views.py`.
2.  Crea una función simple que renderice un archivo HTML.

    ```python
    # tu_app/views.py
    from django.shortcuts import render

    def mi_vista_principal(request):
        # Esta función simplemente le dice a Django que muestre la siguiente plantilla:
        return render(request, 'tu_app/mi_pagina.html')
    ```

### Paso 4: Definir las URLs (`urls.py`)

Conecta una URL (ej: `/mi-modulo/`) a la vista que acabas de crear.

1.  **Crear `urls.py` para la app:**
    *   Crea un **nuevo archivo** llamado `urls.py` dentro de la carpeta de tu app (`tu_app/urls.py`).
    *   Define las rutas específicas para tu app.

        ```python
        # tu_app/urls.py (archivo nuevo)
        from django.urls import path
        from . import views

        urlpatterns = [
            # La URL '' corresponde a la raíz de la app (ej: /mi-modulo/)
            path('', views.mi_vista_principal, name='vista_principal_de_mi_app'),
        ]
        ```

2.  **Incluir las URLs de la app en el proyecto principal:**
    *   Abre el archivo de URLs del proyecto: `pallet_manager/mysite/mysite/urls.py`.
    *   Usa la función `include()` para enlazar a las URLs de tu app.

        ```python
        # pallet_manager/mysite/mysite/urls.py
        from django.contrib import admin
        from django.urls import path, include  # <-- ¡Importar include!

        urlpatterns = [
            path('admin/', admin.site.urls),
            # ... otras urls del proyecto
            path('mi-modulo/', include('tu_app.urls')), # <-- AÑADE ESTA LÍNEA
        ]
        ```
        *Cambia `'mi-modulo/'` por la URL base que quieras para tu sección.*

### Paso 5: Crear la Plantilla (HTML)

Aquí es donde va el código HTML que el usuario verá. La estructura de carpetas es **muy importante** para que Django encuentre el archivo.

1.  Dentro de tu app, crea la siguiente estructura de carpetas: `templates/tu_app/`.

    ```
    tu_app/
    └── templates/
        └── tu_app/  <-- Esta subcarpeta con el nombre de la app es crucial
            └── mi_pagina.html
    ```

2.  Crea un archivo HTML simple dentro de esa carpeta.

    ```html
    <!-- tu_app/templates/tu_app/mi_pagina.html -->

    <h1>¡Hola desde mi App!</h1>
    <p>Si ves esto, tu app está correctamente configurada.</p>

    <!-- Más adelante podrás usar tags de Django como {{ variable }} para mostrar datos. -->
    ```

---

## Solución de Errores Comunes: `TemplateDoesNotExist`

Si ves este error, significa que Django no encuentra tu archivo HTML. Sigue esta lista de verificación:

1.  **✅ ¿La Estructura de Carpetas es Correcta?**
    *   Verifica que la ruta sea exactamente: `tu_app/templates/tu_app/mi_pagina.html`. El error más común es olvidar la segunda carpeta `tu_app`.

2.  **✅ ¿La App está Registrada?**
    *   Revisa que `'tu_app'` esté en `INSTALLED_APPS` en `settings.py`.

3.  **✅ ¿El Nombre del Archivo es Correcto?**
    *   Comprueba que el nombre del archivo en tu vista (`render(request, 'tu_app/mi_pagina.html')`) coincida **exactamente** con el nombre real del archivo.

4.  **✅ ¿Reiniciaste el Servidor?**
    *   Detén el servidor (`Ctrl + C`) y vuelve a iniciarlo (`python manage.py runserver`).