from django.db import models
from django.utils import timezone

# Create your models here.

class Proveedor(models.Model):
  nombre = models.CharField(max_length=250)
  url = models.CharField(max_length=250)
  
  def __str__(self):
      return self.nombre

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
    
class Producto(models.Model):
  descripcion = models.CharField(max_length=250)
  codigo_del_local = models.CharField(max_length=100)
  modelo = models.CharField(max_length=100)
  marca = models.CharField(max_length=100)
  lote= models.ForeignKey(Lote,on_delete=models.CASCADE)
  def __str__(self):
      return "{0} / {1} / {2}".format(self.codigo_del_local, self.modelo, self.marca)

class Venta(models.Model):
         usuario = models.CharField(max_length=40)
         fecha = models.DateTimeField(default=timezone.now)
         precio_de_venta_Total = models.DecimalField(max_digits=12, decimal_places=2)
         productos = models.ManyToManyField(Producto)
         class Meta: 
              ordering=["fecha"]
def _str_(self):
            return "{0}/{1}/{2}/{3}".format(self.usuario,self.fecha, self.productos,self.precio_de_venta_total)