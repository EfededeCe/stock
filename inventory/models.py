from django.db import models
from django.utils import timezone

# Create your models here.

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
  