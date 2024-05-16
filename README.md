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

# Crear una "Aplicación" dentro del proyecto

Todo lo hecho hasta ahora son configuraciones generales, pera empezar a crear vistas o funciones que operen con la base de datos se pueden ir creando distintas aplicaciones, en este caso la app `inventory`:

```sh
python manage.py startapp inventory
```

Y se agrega a la sección INSTALLED_APPS en `settings.py`

```py
INSTALLED_APPS = [
    # ...
    'rest_framework', # DRF
    "corsheaders", # CORS middleware
    "inventory", # App creada
]
```

# Base de Datos, Modelos y Tablas

[ManyToMany Django models](https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/)

```py
class Proveedor(models.Model):
  nombre = models.CharField(max_length=250)
  url = models.CharField(max_length=250)

  def __str__(self):
      return self.nombre

class Producto(models.Model):
  descripcion = models.CharField(max_length=250)
  nombre = models.CharField(max_length=100)
  modelo = models.CharField(max_length=100)
  marca = models.CharField(max_length=100)

  def __str__(self):
      return "{0} / {1} / {2}".format(self.nombre, self.modelo, self.marca)

class Lote(models.Model):
  codigo_barra = models.CharField(max_length=100)
  fecha = models.DateTimeField(default=timezone.now)
  precio_de_compra = models.DecimalField(max_digits=12, decimal_places=2)
  ultimo_precio = models.DecimalField(max_digits=12, decimal_places=2)
  proveedor  = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
  cantidad  = models.IntegerField()
  precio_de_venta = models.DecimalField(max_digits=12, decimal_places=2)

  def __str__(self):
      return "{0} / cantidad {1} / comprado a: ${2}".format(self.proveedor, self.cantidad, self.precio_de_compra)

```

## Migraciones

Para poblar la base de datos hay que ejecutar los comandos `python manage.py makemigrations` y `python manage.py migrate` ó para espesificar una sóla aplicación para hacer las migraciones `python manage.py makemigrations inventory` y `python manage.py migrate inventory`.
El primer comando genera la carpeta `/migrations` (`/inventory/migrations`) y va a contener las distintas migraciones a lo largo del tiempo, si se realizan cambios en la estructura de la base de datos, ahí se pasa a un código python intermedio al lenguaje de BD. El segundo, crea las tablas de la base de datos en la base que se le indicó en `/settings.py`.

## Crear un super usuario de administración

El comando `python manage.py createsuperuser` crea un super usuario para poder gestioinar la base de datos desde el administrador de django. Después de crear el super usuario, levantar el servidor con `python manage.py runserver` e ir a `http://127.0.0.1:8000/admin` ingresar con el usuario y contraseña dados.

# [Django Rest Framework](https://www.django-rest-framework.org/tutorial/quickstart/)

Con DRF ya instalado e integrado como aplicación en `INSTALLED_APPS`, se pueden enviar `json`s como respuesta a una petición http, que represente los distintos modelos de la BD de forma automática y también da la posibilidad de realizar `CRUD`s.

## [Serializers](https://www.django-rest-framework.org/api-guide/serializers/#serializers)

Los `serializers` se usan para serializar, transformar los objetos que vienen de la petición a la BD (como QuerySets), devolviendo un formato apto para el envío como `JSON`.
Para esto hay que crear un archivo para definir los `serializers` de cada modelo, dentro de la carpeta de la aplicación que tiene estos modelos, en este caso `serializers.py`:

**/inventory/serializers.py**

```py
class ProveedorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Proveedor
    fields = '__all__'  # serializa todos los campos de la tabla
```

## Vistas => datos devueltos por serializers


