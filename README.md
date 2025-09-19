#Pallet Manager
## Version de Django 25.2

### Para poder iniciar el proyecto:


````markdown
# Instalación y ejecución – Pallet Manager Módulo 1
**Carpeta del proyecto:** `intercambio-de-pallets-modulo1`  
**Framework:** Django 5.2.1 (Python 3.10 o superior)

---

## 1️⃣ Instalación

1. **Clonar el repositorio y entrar a la carpeta del módulo**
   ```bash
   git clone https://github.com/FolkodeGroup/Intercambio-de-Pallets-Modulo1.git
   cd Intercambio-de-Pallets-Modulo1.git
````

2. **Crear y activar un entorno virtual (recomendado)**

   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   Si existe un archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   En caso contrario, al menos instalar Django:

   ```bash
   pip install django==5.2.1
   ```

4. **Aplicar migraciones para crear la base de datos**

   ```bash
   cd pallet_manager
   cd mysite
   python manage.py migrate
   ```

---

## 2️⃣ Ejecución

1. **Iniciar el servidor de desarrollo**

   ```bash
   python manage.py runserver
   ```

2. **Abrir la aplicación en el navegador**

   ```
   http://127.0.0.1:8000/
   ```

---

> La base de datos por defecto es **SQLite**, que se crea automáticamente.
> Para usar otra base (PostgreSQL, MySQL), modificar la configuración en
> `intercambio-de-pallets-modulo1/settings.py` antes de aplicar las migraciones.


