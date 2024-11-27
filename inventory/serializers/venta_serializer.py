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
                  'precio_de_venta_total', 'lotes']
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


class VntSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venta
        fields = '__all__'


class TbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tabla_intermedia_venta

        fields = ['cantidad', 'lote']


class PostVentaSerializer(serializers.Serializer):

    """
    Formato del body de la petición POST

    {
        "usuario": "Fede",
        "fecha": "",
        "precio_de_venta_total": 0.00,
        "lote_cantidad":[{"lote": 1, "cantidad": 1},
        {"lote": 2, "cantidad": 1}]

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
            array_errores = []

            precio_total = 0

            for lote_cant in lotes_cantidades:
                try:
                    Lote.objects.select_for_update().get(
                        id=lote_cant['lote'].id)

                    if lote_cant['lote'].cantidad < lote_cant['cantidad']:
                        array_errores.append("{}, no hay suficientes en stock para el pedido de {}".format(
                            lote_cant['lote'], lote_cant['cantidad']))

                    precio_total = precio_total + \
                        float(lote_cant['lote'].precio_de_venta) * \
                        float(lote_cant['cantidad'])
                    print('PRECIO TOTAL =====> ', precio_total)
                # talonario['productos'].append(data_producto)
                except Lote.DoesNotExist:
                    raise serializers.ValidationError(
                        "Error al restar cantidad del lote.")

            if len(array_errores) > 0:
                raise ValueError('{}'.format(array_errores))

            print(validated_data)
            venta = Venta.objects.create(
                usuario=validated_data['usuario'], precio_de_venta_total=precio_total)
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

                except ValueError as e:
                    raise ValueError(str(e))

                # lote.restar_cantidad(lote['cantidad'])
        # TODO: devolver con el siguiente formato
        #     "data": {
        #        "id"=1,
        #         "usuario": "Fede",
        #          'fecha': ''
        # !         es un arreglo de objetos
        #         "lote_cantidad": [
        #             {
        #                 "cantidad": 4,
        #                 "lote": 1
        #                  'nombre': '',
        #                  'precio_unitario' : ''
        #             }
        #         ]
        #     }
            # return User.objects.create(**validated_data)

        # return validated_data
        info_lotes_cantidad = []

        for lote_cant in lotes_cantidades:
            info_lotes_cantidad.append({
                'cantidad': lote_cant['cantidad'],
                'lote_id': lote_cant['lote'].id,
                'nombre': lote_cant['lote'].producto.descripcion,
                'precio_unitario': lote_cant['lote'].precio_de_venta
            })

        info_venta = {
            'venta_id': venta.id,
            'usuario': venta.usuario,
            'fecha': venta.fecha,
            'lote_cantidad': info_lotes_cantidad,
            'precio_de_venta_total': precio_total
        }

        return info_venta


# Devolver productos, cantidades, precios, fecha, empleado, total

class Venta2Serializer(serializers.ModelSerializer):

    usuario = serializers.CharField(max_length=40, required=False)
    lote_cantidad = TbSerializer(many=True)

    class Meta:
        model = Tabla_intermedia_venta
        fields = ['cantidad', 'venta', 'lote', 'usuario', 'lote_cantidad']

    def to_representation(self, instance):
        lote = Lote.objects.get(id=instance.lote_id)
        venta = Venta.objects.get(id=instance.venta_id)
        return {
            'tb_inter_id': instance.id,
            'venta_id': venta.id,
            'lote_id': instance.lote_id,
            'descripcion': lote.producto.descripcion,
            'precio_unidad': lote.precio_de_venta,
            'codigo_de_barra': lote.codigo_barra,
            'cantidad_vendida': instance.cantidad
        }


class GetAllVentaSerializer(serializers.ModelSerializer):

    # usuario = serializers.CharField(max_length=40, required=False)
    # lote_cantidad = TbSerializer(many=True)

    class Meta:
        model = Venta
        # fields = ['cantidad', 'venta', 'lote', 'usuario', 'lote_cantidad']
        fields = '__all__'

    def to_representation(self, instance):
        # lote = Lote.objects.get(id=instance.lote_id)
        # venta = Venta.objects.get(id=instance.venta_id)

        # print('=============== Instance ================')
        # print('=============== Instance ================')
        tb_inter = instance.tabla_intermedia_venta_set.all().select_related('lote__producto')
        # print(tb_inter)
        lote_cantidad = []
        for row_tb_inter in tb_inter:
            # print('LOTE     =======> ', row_tb_inter.lote)
            # print('CANTIDAD =======> ', row_tb_inter.cantidad)
            lote_cantidad.append(
                {
                    'lote_id': row_tb_inter.lote.id,
                    'descripcion': row_tb_inter.lote.producto.descripcion,
                    'precio_unitario': row_tb_inter.lote.precio_de_venta,
                    'codigo_de_barra': row_tb_inter.lote.codigo_barra,
                    'codigo_local': row_tb_inter.lote.producto.codigo_del_local,
                    'cantidad': row_tb_inter.cantidad
                })

        # print('=============== Instance ================')
        # print('=============== Instance ================')
        # print('=============== Venta ================')
        # print('=============== Venta ================')
        # print(Venta.objects.get(instance.venta))
        # print('=============== Venta ================')
        # print('=============== Venta ================')

        return {
            'venta_id': instance.id,
            'fecha': instance.fecha,
            'vendedor': instance.usuario,
            'precio_total': instance.precio_de_venta_total,
            'lote_cantidad': lote_cantidad,
        }
