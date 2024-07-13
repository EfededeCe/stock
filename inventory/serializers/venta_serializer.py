from rest_framework import serializers
from ..models import Venta


class VentaSerializer(serializers.ModelSerializer):
    # productosLotes = Tabla_intermedia_ventaSerializer(
    #     source='Tabla_intermedia_venta_set', many=True)

    class Meta:
        model = Venta
        fields = '__all__'
