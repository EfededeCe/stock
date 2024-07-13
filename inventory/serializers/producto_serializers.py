from rest_framework import serializers
from ..models import Producto


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'


class ProductoIDDescSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ('id', 'descripcion')
        read_only_fields = ('id', 'descripcion')
