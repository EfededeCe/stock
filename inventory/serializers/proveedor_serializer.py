from rest_framework import serializers
from ..models import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProveedorIDNombreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ('id', 'nombre')
        read_only_fields = ('id', 'nombre')


class ProveedorIDUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ('id', 'url')
        read_only_fields = ('id', 'url')
