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
        # fields = ['cantidad', 'producto_id',
        #           'codigo_del_local', 'venta_id', 'lote_id']
        fields = ['cantidad', 'venta_id', 'lote_id']

   


class VentaSerializer(serializers.ModelSerializer):
    
    # TODO: validar que en la venta se traiga al menos un producto con cantidad asociada > 0.

    # TODO: Devolver JSON con los datos de la venta:

    # TODO: Agregar validación antes de guardar, si existe el lote de producto requerido

    # TODO: Hacer el calculo del iva y el precio en backend

    # {
    #   "usuario": "Empleado 1",
    #   "venta": 2,
    #   "fecha": "30/07/2024",
    #   "precio_total": 245000.00,
    #   "productos": [
    #     {
    #       "cantidad": "4",
    #       "codigo_de_barra": "43252",
    #       "descripcion": "Freno de cangoo",
    #       "precio_de_venta": "48000.00"
    #     },
    #     {
    #       "cantidad": "2",
    #       "codigo_de_barra": "542342",
    #       "descripcion": "Freno de citroen 13V 3",
    #       "precio_de_venta": "210000.00"
    #     }
    #   ]
    # }
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

    # def create(self, validated_data):
    #     productos_data = validated_data.pop('productosLote')
    #     venta = Venta.objects.create(**validated_data)
    #     for producto_data in productos_data:
    #         producto_id = producto_data.get('producto_id')
    #         codigo_del_local = producto_data.get('codigo_del_local')
    #         if producto_id:
    #             lote = Lote.objects.get(id=producto_id)
    #         elif codigo_del_local:
    #             lote = Lote.objects.get(codigo_del_local=codigo_del_local)
    #         else:
    #             continue
    #         Tabla_intermedia_venta.objects.create(
    #             venta=venta, producto=lote, cantidad=producto_data['cantidad'])
    #     return venta

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
        return venta

# class ImpresionTalonarioSerializer(serializers.Serializer):
#     email = serializers.EmailField()


#     def validate_name(self, value):
#         # print(self.context)
#         print(value)
#         if 'developer' in value:
#             raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre')
#         return value

#     def validate_email(self, value):
#         print(value)
#         if  value == '':
#             raise serializers.ValidationError('Tiene que indicar un correo')
#         # if self.context['name'] in value:
#         #   raise serializers.ValidationError('No puede el email contener el nombre')
#         return value

#     def validate(self, data):
#         return data

#     def create(self, validated_data):
#         print(validated_data)
#         return User.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         print(f"Instancia => {instance}")
#         print(f"Datos validados => {validated_data}")
#         instance.name = validated_data.get('name', instance.name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#         return instance


class TbSerializer(serializers.ModelSerializer):
    # producto_id = serializers.IntegerField(write_only=True, required=False)
    # codigo_del_local = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Tabla_intermedia_venta
        # fields = ['cantidad', 'producto_id',
        #           'codigo_del_local', 'venta_id', 'lote_id']
        fields = ['cantidad',  'lote']
        # depth = 2


class PostVentaSerializer(serializers.Serializer):

    usuario = serializers.CharField(max_length=40, required=False)
    lote_cantidad = TbSerializer(many=True)

    def validate(self, data):
        return data

    # TODO: Agregar @atomic_attributes
    # TODO: Restar cantidad de lote

    def create(self, validated_data):

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

            precio_total = precio_total + \
                float(lote_cant['lote'].precio_de_venta) * \
                float(lote_cant['cantidad'])
            print('PRECIO TOTAL =====> ', precio_total)
            # talonario['productos'].append(data_producto)

        print(validated_data)
        venta = Venta.objects.create(
            usuario=validated_data['usuario'], precio_de_venta_Total=precio_total)
        print(venta)

        for lote in lotes_cantidades:
            print('venta_id ====> ', venta.id)
            print('lote_id  ====> ', lote['lote'].id)
            print('cantidad ====> ', lote['cantidad'])
            Tabla_intermedia_venta.objects.create(
                venta_id=venta.id, lote_id=lote['lote'].id, cantidad=lote['cantidad'])

        # return User.objects.create(**validated_data)
        return validated_data
