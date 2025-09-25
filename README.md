#Pallet Manager
## Version de Django 25.2

### Para poder iniciar el proyecto:


# Intercambio de Pallets – Módulo 1

Plataforma Django para la gestión de intercambio de pallets.  
Este módulo permite administrar movimientos, usuarios y procesos de pallets de forma independiente, pero integrable con los demás módulos del proyecto.

---

## 1️⃣ Requisitos previos

- **Python 3.11 o superior**  
- **Git**  
- (Opcional) **SQLite** (incluido con Python)  
- (Opcional) Editor recomendado: **Visual Studio Code** con la extensión *Python*.

---

## 2️⃣ Clonar el repositorio

```bash
git clone https://github.com/FolkodeGroup/Intercambio-de-Pallets-Modulo1.git
cd Intercambio-de-Pallets-Modulo1/pallet_manager/mysite
💡 Si vas a trabajar en una tarea específica:
git checkout -b nombre-de-tu-rama

3️⃣ Crear y activar el entorno virtual
Windows (PowerShell):

powershell
Copiar código
python -m venv venv
venv\Scripts\activate
Linux / macOS:

bash
Copiar código
python3 -m venv venv
source venv/bin/activate
4️⃣ Instalar dependencias
Con el entorno activado:

bash
Copiar código
pip install -r requirements.txt
5️⃣ Configurar variables de entorno (si aplica)
Si el proyecto utiliza variables de entorno:

bash
Copiar código
cp .env.example .env
Editar .env con las credenciales necesarias.

6️⃣ Migrar la base de datos
bash
Copiar código
python manage.py migrate
Ejecutar solo la primera vez o cuando cambien los modelos.

7️⃣ Crear superusuario (opcional pero recomendado)
Cada integrante puede crear su propio superusuario para acceder al panel de administración:

bash
Copiar código
python manage.py createsuperuser
Completar usuario, correo y contraseña.

Es normal que al escribir la contraseña no se vean los caracteres.

8️⃣ Ejecutar el servidor de desarrollo
bash
Copiar código
python manage.py runserver
Abrir en el navegador:
http://127.0.0.1:8000

Para detener el servidor:
Ctrl + C

9️⃣ Subir cambios al repositorio
bash
Copiar código
git add .
git commit -m "Descripción del cambio"
git push origin nombre-de-tu-rama
⚠️ Errores frecuentes y soluciones
| Problema                                      | Causa probable                      | Solución                                  |
| --------------------------------------------- | ----------------------------------- | ----------------------------------------- |
| `ModuleNotFoundError`                         | Entorno virtual no activado         | Activar venv antes de ejecutar            |
| `django.core.exceptions.ImproperlyConfigured` | Faltan variables en `.env`          | Revisar `.env`                            |
| Puerto 8000 en uso                            | Otro proceso usa el puerto          | `python manage.py runserver 0.0.0.0:8001` |
| `db.sqlite3` o `.pyc` aparecen modificados    | Cambios locales en la base de datos | Agregar a `.gitignore` o evitar su commit |


📂 Estructura principal del proyecto
Copiar código
Intercambio-de-Pallets-Modulo1/
│
├─ pallet_manager/
│   └─ mysite/
│       ├─ manage.py
│       ├─ settings.py
│       └─ ...
├─ requirements.txt
└─ README.md

##documentación de prueba de autenticación
La documentación completa(con caturas y explicación) se encuentra en el siguiente archivo PDF:
[ver documento en Google Drive]
(https://drive.google.com/file/d/1qcSLThX36ie7ZifjgUlU3LJRc73oxeTI/view?usp=drive_link)