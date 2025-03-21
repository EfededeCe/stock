# from rest_framework import DjangoFilterBackend, FilterSet
from .models import Proveedor, Producto, Lote, Venta, Tabla_intermedia_venta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Autenticación
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# API views
from rest_framework import status
from rest_framework.response import Response

from rest_framework import viewsets, generics, views
from rest_framework.decorators import action

# SERIALIZERS
from .serializers.general_serializer import ProductoLoteProveedorSerializer
from .serializers.lote_serializer import LoteSerializer, LoteProductoSerializer
from .serializers.producto_serializers import (
    ProductoSerializer,
    ProductoIDDescSerializer,
    ProductoIDCodigoSerializer,
)
from .serializers.proveedor_serializer import (
    ProveedorSerializer,
    ProveedorIDNombreSerializer,
    ProveedorIDUrlSerializer,
)
from .serializers.venta_serializer import (
    VentaSerializer,
    PostVentaSerializer,
    Venta2Serializer,
    GetAllVentaSerializer,
)


class ProveedorIDUrlView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProveedorIDUrlSerializer
    queryset = Proveedor.objects.all()


class ProductoView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()


class ProductoIDDescView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoIDDescSerializer
    queryset = Producto.objects.all()


class ProductoIDCodigoView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoIDCodigoSerializer
    queryset = Producto.objects.all()


class ProveedorView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class ProveedorIDNombreView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProveedorIDNombreSerializer
    queryset = Proveedor.objects.all()


class LoteView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LoteSerializer
    queryset = Lote.objects.all()

    @action(detail=False, methods=["get"], url_path="detalle-producto")
    def lote_con_producto(self, request, *args, **kwargs):

        lotes = self.get_queryset().exclude(cantidad__lte=0)

        page = self.paginate_queryset(lotes)

        if page is not None:
            serializer = LoteProductoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LoteProductoSerializer(lotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VentaView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()


class ProductoLoteProveedorView(viewsets.ModelViewSet):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    print("Producto - Lote - etc")
    serializer_class = ProductoLoteProveedorSerializer
    queryset = Producto.objects.all()


# /api/v1/presupeusto/
# @csrf_exempt
class VentaPostAPIView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # class VentaPostAPIView(viewsets.GenericViewSet):
    serializer_class = PostVentaSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                venta = serializer.save()
                return Response(
                    {"message": "Venta creada correctamente!", "data": venta},
                    status=status.HTTP_201_CREATED,
                )
            except ValueError as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detalle de una venta => productos, cantidades, precios, fecha, empleado, total
# Sólo GET
# Url => http://localhost:8000/drf-endpoints/api/v1/vget/  2/


class VentaDetalleViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Venta2Serializer
    queryset = Tabla_intermedia_venta.objects.all()

    def retrieve(self, request, *args, **kwargs):
        venta_id = kwargs.get("pk")
        queryset = self.queryset.filter(venta_id=venta_id).select_related("venta")
        if queryset.exists():
            venta = queryset[0].venta
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "venta_id": venta_id,
                    "vendedor": venta.usuario,
                    "fecha": venta.fecha,
                    "venta": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "No se encontraron registros para el venta_id dado."},
            status=status.HTTP_404_NOT_FOUND,
        )


class GetAllVentasViewSet(viewsets.GenericViewSet):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    print("authentication_classes ===> ", authentication_classes)
    print("permission_classes ===> ", permission_classes)

    serializer_class = GetAllVentaSerializer
    queryset = Venta.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetAllVentaSerializer(queryset, many=True)
        return Response(serializer.data)


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(views.APIView):

    def get(self, request, *args, **kwargs):
        # Enviar el token CSRF
        csrf_token = get_token(request)
        return Response(
            {"message": "Token CSRF generado", "csrfToken": csrf_token},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("hay usuairo")
            login(request, user)
            return Response(
                {"message": "Login exitoso", "usuario": request.data["username"]},
                status=status.HTTP_200_OK,
            )
        else:
            print("no hay usuario")
            return Response(
                {"message": "No se pudo realizar el login"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class Logout(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("POST /logout/ - Intentando cerrar sesión")
        print("Cookies:", request.COOKIES)
        print("CSRF Token from Cookie:", request.COOKIES.get("csrftoken"))

        logout(request)
        print("Sesión cerrada.")
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)
