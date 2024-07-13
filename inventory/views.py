# from rest_framework import DjangoFilterBackend, FilterSet
from django.shortcuts import render
from rest_framework import viewsets
from .models import Proveedor, Producto, Lote, Venta, Tabla_intermedia_venta

## SERIALIZERS ##
from .serializers.general_serializer import Tabla_intermedia_ventaSerializer, ProductoLoteProveedorSerializer
from .serializers.lote_serializer import LoteSerializer
from .serializers.producto_serializers import ProductoSerializer
from .serializers.proveedor_serializer import ProveedorSerializer
from .serializers.venta_serializer import VentaSerializer
from .serializers.producto_serializers import ProductoIDDescSerializer

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


class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = ProductoFilter


class ProductoIDDescView(viewsets.ModelViewSet):
    serializer_class = ProductoIDDescSerializer
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
