# Parrot Backend POS SYSTEM - README

Este documento proporciona instrucciones detalladas para configurar y ejecutar el proyecto Django utilizando Poetry para la gestión de dependencias.

## Requisitos previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Python 3.9 o superior
- Poetry (para gestionar dependencias y entorno virtual)

## Instalación

### Clonar el repositorio
```bash
git clone git@github.com:josejuniorpg/PosParrotBack.git
cd PosParrotBack
```

### Configurar Poetry

Si aún no tienes Poetry instalado, puedes hacerlo con:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
o 
```pip
pip install poetry
```

Luego, dentro del directorio del proyecto, instala las dependencias:
```bash
poetry install
```

Para activar el entorno virtual de Poetry:
```bash
poetry shell
```

### Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes configuraciones: (Puede guiarte usnando el `.env.example`)
```ini
SECRET_KEY=tu_clave_secreta
```

Asegúrate de modificar los valores según tu configuración.

### Aplicar migraciones

Ejecuta las migraciones de la base de datos:
```bash
python manage.py migrate
```

### Crear un superusuario

Para acceder al panel de administración, crea un superusuario con:
```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para establecer un usuario y contraseña.

## Ejecución del proyecto

Para el modo de pruebas, sera necesario esta key, para confugurar el archivo de desarollo correctamente. Ya que si no se introduce, se ejecutara el modo de produccion por defecto. 
```ini
DJANGO_ENVIRONMENT_FILE=PosBack.settings.local
```
Para iniciar el servidor, ejecuta:
```bash
python manage.py runserver
```

El proyecto estará disponible en `http://127.0.0.1:8000/`.

## Documentacion

`http://localhost:8000/swagger/`

## Pruebas

Para ejecutar las pruebas del proyecto:
```bash
python manage.py test
```

## Carga de datos iniciales (Opcional)
Este link redirijira a un archivo de json que tendra datos para llenar la BD:
```link
https://drive.google.com/file/d/1v8XTHAJ-kA0Xn-RHtuBQjFgak7UiCdtF/view?usp=sharing
```
```bash
python manage.py loaddata data.json
```
### Datos
Estos datos ya tienen creadoa varios Usuarios y restaurantes, junto con sus ordenes y productos.  
Para que funcionen los usuarios posiblemente sera necesaria  poner esta secret key.
```
SECRET_KEY=dj1223ago-insasdecureasd--t454awc%j)n%dbl-5*^j@43y1^$scamb*5(ai6jx@$@q
```
### Users
``` Es un Usuario con varios restaurantes, ordenes, productos, etc. 
username: pepe3
constraseña; admin
```
``` Es un super Usuario
username: admin
constraseña; admin
```

---

Si tienes preguntas o problemas, no dudes en abrir un issue en el repositorio. ¡Gracias por contribuir!
