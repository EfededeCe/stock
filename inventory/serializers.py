from rest_framework import serializers
from .models import Proveedor, Producto, Lote, Tabla_intermedia_venta, Venta


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'  # (todos los campos)
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


class Tabla_intermedia_ventaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Tabla_intermedia_venta
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'


class LoteProveedorSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()

    class Meta:
        model = Lote
        fields = '__all__'


class ProductoLoteProveedorSerializer(serializers.ModelSerializer):
    lote = LoteProveedorSerializer()

    class Meta:
        model = Producto
        fields = '__all__'

    # def to_representation(self, instance):

    #   return {
    #     "id": instance.id,
    #     "descripcion": instance.descripcion,
    #     "codigo_del_local": instance.codigo_del_local,
    #     "modelo": instance.modelo,
    #     "marca": instance.marca,
    #     "lote_cod_barra": instance.lote.fecha if instance.lote != '' else ''
    #   }
