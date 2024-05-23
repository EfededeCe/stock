from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductoSerializer, ProveedorSerializer, LoteSerializer , VentaSerializer, Tabla_intermedia_ventaSerializer
from .models import Proveedor, Producto, Lote, Venta, Tabla_intermedia_venta
# Create your views here.


class ProveedorView(viewsets.ModelViewSet):
  serializer_class = ProveedorSerializer
  queryset = Proveedor.objects.all()
class ProductoView(viewsets.ModelViewSet):
  serializer_class = ProductoSerializer
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