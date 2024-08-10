# from rest_framework import DjangoFilterBackend, FilterSet
from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Proveedor, Producto, Lote, Venta, Tabla_intermedia_venta

# API views
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

# SERIALIZERS
from .serializers.general_serializer import Tabla_intermedia_ventaSerializer, ProductoLoteProveedorSerializer
from .serializers.lote_serializer import LoteSerializer
from .serializers.producto_serializers import ProductoSerializer, ProductoIDDescSerializer, ProductoIDCodigoSerializer
from .serializers.proveedor_serializer import ProveedorSerializer, ProveedorIDNombreSerializer, ProveedorIDUrlSerializer
from .serializers.venta_serializer import VentaSerializer, VentaDetalleSerializer, TablaIntermediaVentaSerializer, PostVentaSerializer

# Create your views here.

# class ProductoFilter(FilterSet):
#     class Meta:
#         model = Producto
#         fields = {
#             'descripcion': ['icontains'],
#             'codigo_del_local': ['icontains'],
#         }


class ProveedorView(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class ProveedorIDNombreView(viewsets.ModelViewSet):
    serializer_class = ProveedorIDNombreSerializer
    queryset = Proveedor.objects.all()


class ProveedorIDUrlView(viewsets.ModelViewSet):
    serializer_class = ProveedorIDUrlSerializer
    queryset = Proveedor.objects.all()


class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()


class ProductoIDDescView(viewsets.ModelViewSet):
    serializer_class = ProductoIDDescSerializer
    queryset = Producto.objects.all()


class ProductoIDCodigoView(viewsets.ModelViewSet):
    serializer_class = ProductoIDCodigoSerializer
    queryset = Producto.objects.all()


class LoteView(viewsets.ModelViewSet):
    serializer_class = LoteSerializer
    queryset = Lote.objects.all()


class VentaView(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()


class Tabla_intermedia_ventaView(viewsets.ModelViewSet):
    serializer_class = Tabla_intermedia_ventaSerializer
    queryset = Tabla_intermedia_venta.objects.all()


class ProductoLoteProveedorView(viewsets.ModelViewSet):
    serializer_class = ProductoLoteProveedorSerializer
    queryset = Producto.objects.all()


# @api_view(['GET', 'POST'])
# def venta_api_view(request):
    # VentaSerializerPOST

    #   if request.method == 'GET':
    #     users = User.objects.all().values('id', 'username', 'email', 'password')
    #     user_serializer = UserListSerializer(users, many = True)

    #     # test_data = {
    #     #   'name': 'develop',
    #     #   'email': 'test@gmail.com'
    #     # }

    #     # test_user = TestUserSerializer(data = test_data, context = test_data)
    #     # if test_user.is_valid():
    #     #   user_instance = test_user.save()
    #     #   print(user_instance)
    #     # else:
    #     #   print(test_user.errors)

    #     return Response(user_serializer.data, status = status.HTTP_200_OK)

    #   elif request.method == 'POST':

    # if request.method == 'POST':
    #     venta_serializer = VentaSerializerPOST(data=request.data)
    #     if venta_serializer.is_valid():
    #         venta_serializer.save()
    #         return Response({'message': 'Venta creada correctamente', 'venta': VentaSerializerPOST.data}, status=status.HTTP_201_CREATED)
    #     return Response(VentaSerializerPOST.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    # serializer_class = VentaDetalleSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return VentaDetalleSerializer
        return VentaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IntermediaViewSet(viewsets.ModelViewSet):
    queryset = Tabla_intermedia_venta.objects.all()
    serializer_class = TablaIntermediaVentaSerializer
    # serializer_class = VentaDetalleSerializer

    # def get_serializer_class(self):
    #     if self.action in ['retrieve', 'list']:
    #         return VentaDetalleSerializer
    #     return VentaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('=========================')
        print(type(instance))
        print(instance)
        print(instance.id)
        print(instance.venta_id)
        print(instance.lote_id)
        print('=========================')
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TalonarioViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='(?P<venta_id>[^/.]+)')
    def buscar_por_venta(self, request, venta_id=None):
        venta_productos = Tabla_intermedia_venta.objects.filter(
            venta_id=venta_id)
        # serializer = ImpresionTalonarioSerializer(venta_productos, many=True)
        serializer = TablaIntermediaVentaSerializer(venta_productos, many=True)

        precio_total = 0
        talonario = {
            'productos': [],
            'total': 0,
            'fecha': ""
        }

        for prod in serializer.data:
            print('Productos en la venta')
            print('========> ', prod)
            data_producto = {
                'cantidad': prod['cantidad'],
                'descripcion': prod['lote']['producto']['descripcion'],
                'precio': float(prod['lote']['precio_de_venta'])
            }
            precio_total = precio_total + \
                float(prod['lote']['precio_de_venta'])
            print(data_producto)
            talonario['productos'].append(data_producto)

        talonario['total'] = precio_total
        fecha = serializer.data[0]['venta']['fecha']
        talonario['fecha'] = fecha

        return Response(talonario)


# class VentaPostViewSet(viewsets.ViewSet):

#     # Espera ==>
#     # {"usuario": "Pepe",
#     #   "productos"[
#     #       {"lote_id": 2, "cantidad": 4}
#     #       {"lote_id": 3, "cantidad": 1}
#     #   ]}

#     def create(self, request, *args):
#         print(self)
#         print(args)
#         print(request)
#         print(request.data)
#         return Response({"mensaje": "respuesta"})


class VentaPostViewSet(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()

    # Espera ==>
    # {"usuario": "Pepe",
    #   "productos"[
    #       {"lote_id": 2, "cantidad": 4}
    #       {"lote_id": 3, "cantidad": 1}
    #   ]}

    def create(self, request, *args):
        print('================================')
        print(request.data)
        print('================================')
        serializer = self.get_serializer(data=request.data)
        print('================================')
        print(request.data)
        print(serializer)
        print('================================')
        serializer.is_valid()
        print('================================')
        print(request.data)
        print('================================')
        venta = self.perform_create(serializer)

        print(self)
        print(args)
        print(request)
        print(request.data)
        headers = self.get_success_header(serializer.data)
        return Response(serializer.data,  status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        return serializer.save()


class VentaPostAPIView(generics.CreateAPIView):
    serializer_class = PostVentaSerializer

    print('================================')

    print('================================')
    # return Response({"mensaje": "respuesta"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)  # intercepta los datos
        if serializer.is_valid():
            # intercepta los datos
            serializer.save()
            print('serializer.data ======> ', serializer.data)
            return Response({'message': 'Producto creado correctamente!', 'data':  serializer.data}, status=status.HTTP_201_CREATED)
        print('serializer.data no válido ======> ',
              serializer)  # intercepta los datos
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer, status=status.HTTP_400_BAD_REQUEST)
