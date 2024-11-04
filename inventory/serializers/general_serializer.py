from rest_framework import serializers
from ..models import Proveedor, Producto, Lote, Tabla_intermedia_venta, Venta
from .proveedor_serializer import ProveedorSerializer
from .lote_serializer import LoteSerializer, LoteProveedorSerializer


class Tabla_intermedia_ventaSerializer (serializers.ModelSerializer):
    # producto = ProductoSerializer(many=True, source='lotes')

    class Meta:
        model = Tabla_intermedia_venta
        # fields = '__all__'
        exclude = ['lote']
        depth = 4


class ProductoLoteProveedorSerializer(serializers.ModelSerializer):

    lote = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ('id', 'descripcion', 'codigo_del_local',
                  'modelo', 'marca', 'lote')
        depth = 2

    def get_lote(self, obj):
        # Aquí debes definir cómo obtener el lote para un producto.
        # Este es solo un ejemplo, debes ajustarlo a tu modelo y lógica.
        # Supongo que tienes una relación entre Producto y Lote que debes definir en tu modelo.
        try:
            lotes = Lote.objects.filter(producto=obj).exclude(cantidad__lte=0)
            return LoteProveedorSerializer(lotes, many=True).data
        except Lote.DoesNotExist:
            return None
