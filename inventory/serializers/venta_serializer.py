from rest_framework import serializers
from ..models import Venta, Lote, Tabla_intermedia_venta
from ..serializers.lote_serializer import LoteProveedorSerializer

class ProductoVentaSerializer(serializers.ModelSerializer):
    codigo_de_barra = serializers.CharField(source='producto.codigo_barra')
    descripcion = serializers.CharField(source='producto.producto.descripcion')
    precio_de_venta = serializers.DecimalField(
        source='producto.precio_de_venta', max_digits=12, decimal_places=2)

    class Meta:
        model = Tabla_intermedia_venta
        fields = ['cantidad', 'codigo_de_barra',
                  'descripcion', 'precio_de_venta']


class VentaDetalleSerializer(serializers.ModelSerializer):
    productos = ProductoVentaSerializer(
        source='tabla_intermedia_venta_set', many=True)
    venta = serializers.IntegerField(source='id')
    fecha = serializers.DateTimeField(format='%d/%m/%Y')
    precio_total = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['usuario', 'venta', 'fecha', 'precio_total', 'productos']

    def get_precio_total(self, obj):
        return sum(item.producto.precio_de_venta * item.cantidad for item in obj.tabla_intermedia_venta_set.all())


class TablaIntermediaVentaSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Tabla_intermedia_venta
        fields = ['cantidad', 'venta_id', 'lote_id']

   


class VentaSerializer(serializers.ModelSerializer):
    
    # TODO: validar que en la venta se traiga al menos un producto con cantidad asociada > 0.

    # TODO: Devolver JSON con los datos de la venta:

    # TODO: Agregar validación antes de guardar, si existe el lote de producto requerido

    # TODO: Hacer el calculo del iva y el precio en backend

    
    lotes = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['usuario', 'fecha',
                  'precio_de_venta_Total', 'lotes']
        # depth = 1

    def get_lotes(self, obj):
        print('obj ====> ', obj)
        print('obj ====> ', obj.usuario)
        # Aquí debes definir cómo obtener el lote para un producto.
        # Este es solo un ejemplo, debes ajustarlo a tu modelo y lógica.
        # Supongo que tienes una relación entre Producto y Lote que debes definir en tu modelo.
        try:
            lotes = Lote.objects.all()
            return LoteProveedorSerializer(lotes, many=True).data
        except Lote.DoesNotExist:
            return None

    def create(self, validated_data):
        productos_data = validated_data.pop('productosLote')
        venta = Venta.objects.create(**validated_data)
        for producto_data in productos_data:
            producto_id = producto_data.get('producto_id')
            codigo_del_local = producto_data.get('codigo_del_local')
            if producto_id:
                lote = Lote.objects.get(id=producto_id)
            elif codigo_del_local:
                lote = Lote.objects.get(codigo_del_local=codigo_del_local)
            else:
                continue
            Tabla_intermedia_venta.objects.create(
                venta=venta, producto=lote, cantidad=producto_data['cantidad'])
        return venta
