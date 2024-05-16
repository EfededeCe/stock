from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductoSerializer, ProveedorSerializer, LoteSerializer
from .models import Proveedor, Producto, Lote
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
