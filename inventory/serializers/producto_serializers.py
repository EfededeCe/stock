from rest_framework import serializers
from ..models import Producto


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'

    def validate(self, data):
        descripcion = data.get('descripcion')
        modelo = data.get('modelo')
        marca = data.get('marca')

        if Producto.objects.filter(descripcion=descripcion, modelo=modelo, marca=marca).exists():
            raise serializers.ValidationError(
                "Un producto con la misma descripción, modelo y marca ya existe.")

        return data


class ProductoIDDescSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ('id', 'descripcion')
        read_only_fields = ('id', 'descripcion')


class ProductoIDCodigoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ('id', 'codigo_del_local')
        read_only_fields = ('id', 'codigo_del_local')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'codigo_local': instance.codigo_del_local
        }
