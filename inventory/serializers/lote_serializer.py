from rest_framework import serializers
from ..models import Lote


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
        depth = 1


class LoteProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ('id', 'codigo_barra', 'precio_de_compra', 'cantidad', 'precio_bonificado',
                  'ultimo_precio', 'proveedor', 'cantidad', 'precio_de_venta', 'iva')
        depth = 1


class LoteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ('id', 'codigo_barra', 'precio_de_compra', 'cantidad', 'precio_bonificado',
                  'ultimo_precio', 'cantidad', 'precio_de_venta', 'iva', 'producto')
        depth = 1
