# from rest_framework import DjangoFilterBackend, FilterSet
from django.shortcuts import render
from rest_framework import viewsets
from .models import Proveedor, Producto, Lote, Venta, Tabla_intermedia_venta

# API views
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# SERIALIZERS
from .serializers.general_serializer import Tabla_intermedia_ventaSerializer, ProductoLoteProveedorSerializer
from .serializers.lote_serializer import LoteSerializer
from .serializers.producto_serializers import ProductoSerializer, ProductoIDDescSerializer, ProductoIDCodigoSerializer
from .serializers.proveedor_serializer import ProveedorSerializer, ProveedorIDNombreSerializer, ProveedorIDUrlSerializer
from .serializers.venta_serializer import VentaSerializer, VentaDetalleSerializer

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
