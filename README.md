# Instalación inicial

Para crear un [entorno virtual](https://docs.python.org/es/3/tutorial/venv.html) para las dependencias, se puede usar el comando:

```sh
python -m venv tutorial-env
```

y para activar el entorno virtual en windows usar el comando:

```sh
tutorial-env\Scripts\activate
```

O en linux:

```sh
source tutorial-env/bin/activate
```

Una vez dentro del entorno virtual, instalar Django y las dependencias requeridas, para salir del entorno virtual usar el comando:

```sh
deactivate
```

En este caso la creación del entorno virtual se hizo con el nombre .venvlnx (haciendo referencia a que es un entorno virtual creado en mi SO linux) con el comando `python3 -m venv .venvlnx`.

## Instalación de [Django](https://www.djangoproject.com/download/)

Ya existe un archivo `requirements.txt` donde se encuentran las bibliotecas usadas con sus versiones exactas:

```sh
pip install -r requirements.txt
```

Hay que usar siempre la misma versión tanto de Python como de Django, la última de Django es la `5.0.4` que es compatible sólo con Python `3.10` en adelante.

En windows:

```sh
py -m pip install Django==5.0.4
```

En linux

```sh
python -m pip install Django==5.0.4
```

# [Django Rest Framework - DRF](https://www.django-rest-framework.org/#installation)

Esta librería provee una interfaz para realizar APIs de una manera más simple que con puro Django.

```sh
pip install djangorestframework
```

Luego agregar en el archivo `setings.py`:

```py
INSTALLED_APPS = [
    # ... otras aplicaciones por defecto
    'rest_framework',

]
```

```py
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",    # Va antes de
    "django.middleware.common.CommonMiddleware", # CommonMiddleware
    ...,
]
```

```py
# Agregado para usar con la biblioteca django-cors-headers
CORS_ALLOWED_ORIGINS = [...]
```

## Base de datos [MariaDB >= 10.4 ó MySQL >= 8.0.11](https://docs.djangoproject.com/en/5.0/ref/databases/#mysql-notes)

Ver la versión del motor de base de datos `MySQL` que sea mayor o igual a 8.0.11 y `MariaDB` mayor o igual a 10.4

Hay que instalar un [driver](https://docs.djangoproject.com/en/5.0/topics/install/#get-your-database-running) según la base de datos a usar (a menos que sea Sqlite que la usa por defecto). La recomendada es [mysqlclient](https://pypi.org/project/mysqlclient/)

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # DB a usar (MySQL o MariaDB)
        'NAME': 'stock_manager',
        'USER': 'mi_usuario',
        'PASSWORD': 'mi_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

O bien crear un archivo `.env` donde definir las variables:

```txt
NAME=stock_manager
USER=mi_usuario
PASSWORD=mi_contraseña
HOST=localhost
PORT=3306
```

Para poder conectar el `.env` con `settings.py` y llevar las variables hay que instalar la biblioteca [python-decouple](https://pypi.org/project/python-decouple/) ([ver ejemplo](https://diegoamorin.com/variables-de-entorno-django/)) e importar el método config al principio de `settings.py`

```py
from decouple import config`
# ...
# ...

# Para usar  las variables usar conf
'NAME': config('DB_NAME'),
'USER': config('DB_USER'),
'PASSWORD': config('DB_PASSWORD'),
'HOST': config('DB_HOST'),
'PORT': config('DB_PORT', cast=int),

```

# Configuración de [.gitignore](https://djangowaves.com/tips-tricks/gitignore-for-a-django-project/)

Agregar a la lista del archivo `.gitignore` los archivos que no sean código de la aplicación o cache, como el entorno virtual creado (venv o .venv o .venvlnx etc...)

## Más [configuraciones](https://dev.to/iamjonathanpumares/configura-tu-entorno-de-desarrollo-de-manera-profesional-con-python-y-django-335g) generales
