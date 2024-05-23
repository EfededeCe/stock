from rest_framework import serializers
from .models import Proveedor, Producto, Lote , Tabla_intermedia_venta,Venta
class ProveedorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Proveedor
    fields = '__all__' #(todos los campos)
    # fields = ('id', 'nombre', 'url')

class ProductoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Producto
    fields = '__all__' 
    # fields = ('id', 'nombre', 'modelo', 'marca', 'descripcion')

class LoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lote
    fields = '__all__' 
    # fields = ('id', 'codigo_barra', 'precio_de_compra', 'cantidad')


class Tabla_intermedia_ventaSerializer (serializers.ModelSerializer) :
  class Meta: 
    model=Tabla_intermedia_venta
    fields = '__all__' 

class VentaSerializer(serializers.ModelSerializer): 
  class Meta :
    model:Venta
    fields = '__all__' 