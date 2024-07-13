from rest_framework import serializers
from ..models import Lote


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
        # fields = ('id', 'codigo_barra', 'precio_de_compra', 'cantidad')
