from rest_framework import serializers
from ..models import Venta, Lote, Tabla_intermedia_venta
from ..serializers.lote_serializer import LoteProveedorSerializer
from django.db import transaction


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

    # TODO: validar que en la venta se traiga al menos un producto con cantidad asociada > 0. crear error para no

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
        print('obj ====> ', self)
        print('obj ====> ', obj.usuario)
        print('obj ====> ', obj.tabla_intermedia_venta_set.all())
        # Aquí debes definir cómo obtener el lote para un producto.
        # Este es solo un ejemplo, debes ajustarlo a tu modelo y lógica.
        # Supongo que tienes una relación entre Producto y Lote que debes definir en tu modelo.
        try:
            lotes = Lote.objects.all()
            # lotes = obj.tabla_intermedia_venta_set.all()
            print('Data del serializer', lotes[0])
            return LoteProveedorSerializer(lotes, many=True).data
        except Lote.DoesNotExist:
            return None

    @transaction.atomic
    def create(self, validated_data):
        productos_data = validated_data.pop('productosLote')
        venta = Venta.objects.create(**validated_data)

        for producto_data in productos_data:
            lote_id = producto_data.get('lote_id')
            cantidad = producto_data.get('cantidad')

            if lote_id and cantidad:
                lote = Lote.objects.get(id=lote_id)
                Tabla_intermedia_venta.objects.create(
                    venta=venta, lote=lote, cantidad=cantidad)
                lote.restar_cantidad(cantidad)
        return venta


class TbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tabla_intermedia_venta

        fields = ['cantidad',  'lote']


class PostVentaSerializer(serializers.Serializer):

    """
    Fromato del body de la petición POST

    {
        "usuario": "Fede",
        "fecha": "",
        "precio_de_venta_Total": 0.00,
        "lote_cantidad":[{"lote": 1, "cantidad": 4},
        {"lote": 2, "cantidad": 25}]

    }
    """

    usuario = serializers.CharField(max_length=40, required=False)
    lote_cantidad = TbSerializer(many=True)

    def validate(self, data):
        return data

    # TODO: Agregar @atomic_attributes x test
    # TODO: Restar cantidad de lote x test

    def create(self, validated_data):
        with transaction.atomic():
            lotes_cantidades = validated_data['lote_cantidad']

            print('====================================')
            print('====================================')
            print('PostVentaSerializer create')
            print('====================================')
            print('====================================')

            precio_total = 0

            print(lotes_cantidades)
            print('====================================')
            print('====================================')
            print('PostVentaSerializer, for in ====>')
            print('====================================')
            print('====================================')

            for lote_cant in lotes_cantidades:
                Lote.objects.select_for_update().get(id=lote_cant['lote'].id)
                precio_total = precio_total + \
                    float(lote_cant['lote'].precio_de_venta) * \
                    float(lote_cant['cantidad'])
                print('PRECIO TOTAL =====> ', precio_total)
                # talonario['productos'].append(data_producto)

            print(validated_data)
            venta = Venta.objects.create(
                usuario=validated_data['usuario'], precio_de_venta_Total=precio_total)
            print(venta)

            # print(asd)

            for lote in lotes_cantidades:
                print('venta_id ====> ', venta.id)
                print('lote_id  ====> ', lote['lote'].id)
                print('cantidad ====> ', lote['cantidad'])
                Tabla_intermedia_venta.objects.create(
                    venta_id=venta.id, lote_id=lote['lote'].id, cantidad=lote['cantidad'])
            try:
                Lote.objects.get(id=lote['lote'].id).restar_cantidad(
                    lote['cantidad'])

            except ValueError:
                raise

                # lote.restar_cantidad(lote['cantidad'])

            # return User.objects.create(**validated_data)
        return validated_data
