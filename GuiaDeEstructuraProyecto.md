
---

### **GUIA_DE_ESTRUCTURA.md**

# 🗺️ Guía de Estructura del Proyecto: Pallet Manager

¡Hola equipo! Esta es nuestra guía de referencia para navegar la arquitectura del proyecto. Entenderla nos ayudará a colaborar mejor y a desarrollar nuevas funcionalidades de manera más rápida y ordenada.

---

## 🌳 Árbol de Carpetas (La vista de pájaro)

Esta es la estructura principal. Los emojis te ayudarán a identificar rápidamente el propósito de cada carpeta y archivo clave.

```
pallet_manager/
└── mysite/                 <-- 🚀 RAÍZ DEL PROYECTO DJANGO (Nuestro centro de operaciones)
    ├── manage.py           <-- 🛠️ La herramienta para todos los comandos de Django.
    |
    ├── mysite/             <-- ⚙️ CONFIGURACIÓN GLOBAL (El cerebro del proyecto)
    │   ├── settings.py     <-- 🔩 Ajustes principales (BBDD, Apps, etc.)
    │   └── urls.py         <-- 🗺️ El mapa de URLs principal.
    |
    ├── templates/          <-- 🎨 PLANTILLAS (Aquí vive el HTML)
    │   ├── base.html       <-- 뼈 El esqueleto de todas nuestras páginas.
    │   └── index.html      <-- 🏠 La página de inicio, por ejemplo.
    |
    ├── static/             <-- 💅 ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes)
    │   ├── css/
    │   └── images/
    |
    └── users/              <-- 📦 APP: Módulo de Usuarios
    │   ├── views.py        <-- 🧠 Lógica (qué mostrar en cada página).
    │   ├── models.py       <-- 📊 Estructura de la BBDD.
    │   └── urls.py         <-- 📍 (Opcional) Rutas específicas de esta app.
    |
    └── empleados/          <-- 📦 APP: Módulo de Empleados
    └── ... (y el resto de nuestras apps)
```

---

## 🔬 Anatomía del Proyecto: ¿Qué hace cada parte?

### 🚀 `mysite/` (La Raíz del Proyecto)

| Característica      | Descripción                                                                                                                                                            |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **¿Qué es?**        | La carpeta principal de trabajo que contiene `manage.py`.                                                                                                              |
| **Contenido Clave** | `manage.py`, las carpetas de las apps (`users`, `empleados`), `static` y `templates`.                                                                                    |
| **¿Cuándo la uso?** | **Siempre abres tu terminal aquí.** Es el punto de partida para todos los comandos. <br> > `python manage.py runserver` <br> > `python manage.py makemigrations`          |

### ⚙️ `mysite/mysite/` (La Carpeta de Configuración)

| Característica      | Descripción                                                                                                                                                                                                                            |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **¿Qué es?**        | El centro de control global. Las decisiones que se toman aquí afectan a todo el proyecto.                                                                                                                                              |
| **Contenido Clave** | `settings.py`, `urls.py`.                                                                                                                                                                                                              |
| **¿Cuándo la uso?** | **Cuando necesitas hacer cambios a nivel de proyecto.** <br> • **En `settings.py`:** Al registrar una nueva app en `INSTALLED_APPS`. <br> • **En `urls.py`:** Al conectar las URLs de una app al sitio principal (ej: `/empleados/`). |

### 🎨 `templates/`

| Característica      | Descripción                                                                                                                                                             |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **¿Qué es?**        | La casa de toda la parte visual (el HTML).                                                                                                                              |
| **Contenido Clave** | `base.html` (la plantilla maestra) y las páginas específicas (`index.html`, `login.html`, etc.).                                                                         |
| **¿Cuándo la uso?** | Para crear o modificar la interfaz que ve el usuario. <br> > **Recuerda:** Siempre empieza una nueva plantilla con `{% extends 'base.html' %}` para mantener el diseño consistente. |

### 💅 `static/`

| Característica      | Descripción                                                                                                                                                                                            |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **¿Qué es?**        | Nuestro almacén de recursos de diseño: CSS, JavaScript, imágenes, fuentes, etc.                                                                                                                        |
| **Contenido Clave** | Subcarpetas `css`, `js`, `images`.                                                                                                                                                                     |
| **¿Cuándo la uso?** | Para añadir estilos o interactividad a las plantillas. Para usar un archivo, cárgalo en el HTML así: <br> ```html {% load static %} <link rel="stylesheet" href="{% static 'css/mi_estilo.css' %}"> ``` |

### 📦 Las Apps (`users/`, `empleados/`, etc.)

| Característica      | Descripción                                                                                                                                                                                                          |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **¿Qué es?**        | Módulos de funcionalidad autocontenidos. `users` se ocupa de todo lo relacionado con usuarios, `empleados` de todo lo de empleados.                                                                                   |
| **Contenido Clave** | `models.py` (los datos), `views.py` (la lógica) y **a veces** un `urls.py` (rutas internas).                                                                                                                           |
| **¿Cuándo la uso?** | **El 90% del tiempo trabajarás aquí.** Cuando desarrollas una nueva funcionalidad, casi siempre implicará tocar los archivos de una de estas carpetas.                                                                 |

> **⚠️ ¡Ojo! ¿Y si mi app no tiene `urls.py`?**
> ¡No pasa nada! Es completamente normal. Significa que sus URLs se gestionan directamente en el archivo principal **`mysite/mysite/urls.py`**. Es una forma más directa de trabajar para apps con pocas rutas.

---

## 💡 Flujo de Trabajo Práctico: "Crear una nueva página"

Este es el ciclo de vida típico para añadir una funcionalidad.

**1️⃣ Modelo (`models.py`)** ➡️ **2️⃣ Vista (`views.py`)** ➡️ **3️⃣ Plantilla (`.html`)** ➡️ **4️⃣ URL (`mysite/urls.py`)**

| Paso                  | Archivo a Modificar            | Acción a Realizar                                                                            |
| :-------------------- | :----------------------------- | :------------------------------------------------------------------------------------------- |
| **1. Definir Datos**  | `pallets/models.py`            | Creas una clase `Pallet` que define los campos de la base de datos (nombre, fecha, etc.).      |
| **2. Crear Lógica**   | `pallets/views.py`             | Creas una función que consulta la base de datos (`Pallet.objects.all()`) y decide qué HTML mostrar. |
| **3. Diseñar Vista**  | `templates/listar_pallets.html`| Creas el archivo HTML que recibe los datos y los muestra en una tabla, lista, etc.            |
| **4. Conectar URL**   | `mysite/mysite/urls.py`        | Importas la vista desde su app (`from pallets.views import ...`) y creas el `path()` que apunta a ella. |

---

Si algo no está claro, ¡pregunta sin dudarlo!

**¡Feliz codificación!** 🚀