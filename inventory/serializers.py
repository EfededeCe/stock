from rest_framework import serializers
from .models import Proveedor, Producto, Lote

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


