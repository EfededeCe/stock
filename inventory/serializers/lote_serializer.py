from rest_framework import serializers
from ..models import Lote


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = "__all__"


class LoteProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = (
            "id",
            "codigo_barra",
            "precio_de_compra",
            "cantidad",
            "precio_bonificado",
            "ultimo_precio",
            "proveedor",
            "cantidad",
            "precio_de_venta",
            "iva",
        )
        depth = 1


class LoteProductoSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Lote
    #     fields = ('id', 'codigo_barra', 'precio_de_compra', 'cantidad', 'precio_bonificado',
    #               'ultimo_precio', 'cantidad', 'precio_de_venta', 'iva', 'producto')
    #     depth = 1

    # Agregar campos del producto directamente
    descripcion = serializers.CharField(source="producto.descripcion")
    codigo_del_local = serializers.CharField(source="producto.codigo_del_local")
    modelo = serializers.CharField(source="producto.modelo")
    marca = serializers.CharField(source="producto.marca")
    producto_id = serializers.IntegerField(source="producto.id")
    codigo_de_barra = serializers.IntegerField(source="codigo_barra")
    stock = serializers.IntegerField(source="cantidad")
    proveedor = serializers.CharField(source="proveedor.nombre")
    precio_de_lista = serializers.CharField(source="precio_de_compra")

    class Meta:
        model = Lote
        fields = (
            "id",
            "codigo_de_barra",
            "precio_de_lista",
            "stock",
            "precio_bonificado",
            "ultimo_precio",
            "precio_de_venta",
            "iva",
            "producto_id",
            "proveedor",
            "descripcion",
            "codigo_del_local",
            "modelo",
            "marca",
        )
