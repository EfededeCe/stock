from rest_framework import serializers
from ..models import Proveedor, Producto, Lote, Tabla_intermedia_venta, Venta
from .proveedor_serializer import ProveedorSerializer


class Tabla_intermedia_ventaSerializer (serializers.ModelSerializer):
    # producto = ProductoSerializer(many=True, source='lotes')

    class Meta:
        model = Tabla_intermedia_venta
        fields = '__all__'


class LoteProveedorSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()

    class Meta:
        model = Lote
        fields = '__all__'


class ProductoLoteProveedorSerializer(serializers.ModelSerializer):
    # lote = Lote.objects.filter(producto__id=producto.id)
    # LoteProveedorSerializer(many=True)

    class Meta:
        model = Producto
        fields = '__all__'

    def to_representation(self, instance):

        queryset_values = Lote.objects.filter(
            producto__id=instance.id).values()

        return {
            'id': instance.id,
            'descripcion': instance.descripcion,
            'codigo_del_local': instance.codigo_del_local,
            'modelo': instance.modelo,
            'marca': instance.marca,
            'lotes': queryset_values
        }
