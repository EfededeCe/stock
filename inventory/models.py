from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django_prometheus.models import ExportModelOperationsMixin
# Create your models here.


class Proveedor(ExportModelOperationsMixin('proveedor'), models.Model):
    nombre = models.CharField(max_length=250, unique=True)
    url = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.nombre


class Producto(ExportModelOperationsMixin('producto'), models.Model):
    descripcion = models.CharField(max_length=250)
    codigo_del_local = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return "{0} / {1} / {2}".format(self.codigo_del_local, self.modelo, self.marca)


class Lote(ExportModelOperationsMixin('lote'), models.Model):
    codigo_barra = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    precio_de_compra = models.DecimalField(
        max_digits=12, validators=[MinValueValidator(0)], decimal_places=2)
    precio_bonificado = models.DecimalField(
        max_digits=12, validators=[MinValueValidator(0)], decimal_places=2, null=True)
    ultimo_precio = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], null=False)
    precio_de_venta = models.DecimalField(
        max_digits=12, validators=[MinValueValidator(0)], decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, default='0')

    def restar_cantidad(self, cantidad):
        """Reduce la cantidad disponible del lote."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self.cantidad:
            raise ValueError(
                "La cantidad a restar no puede ser mayor a la cantidad disponible")

        self.cantidad -= cantidad
        self.save()

    def __str__(self):
        return "{0} / cantidad {1} / comprado a: ${2}".format(self.proveedor, self.cantidad, self.precio_de_compra)


class Venta(ExportModelOperationsMixin('venta'), models.Model):
    usuario = models.CharField(max_length=40, default="Empleado 1")
    fecha = models.DateTimeField(default=timezone.now)
    precio_de_venta_total = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    lotes = models.ManyToManyField(
        Lote, through="Tabla_intermedia_venta")

    class Meta:
        ordering = ["fecha"]

    def _str_(self):
        return "{0}/{1}/{2}/{3}".format(self.usuario, self.fecha, self.lotes, self.precio_de_venta_total)


class Tabla_intermedia_venta(ExportModelOperationsMixin('tabla_intermedia_venta'), models.Model):
    cantidad = models.PositiveIntegerField(default=0)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
