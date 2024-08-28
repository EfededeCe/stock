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

# SERIALIZERS
from .serializers.general_serializer import ProductoLoteProveedorSerializer
from .serializers.lote_serializer import LoteSerializer
from .serializers.producto_serializers import ProductoSerializer, ProductoIDDescSerializer, ProductoIDCodigoSerializer
from .serializers.proveedor_serializer import ProveedorSerializer, ProveedorIDNombreSerializer, ProveedorIDUrlSerializer
from .serializers.venta_serializer import VentaSerializer, PostVentaSerializer, Venta2Serializer, GetAllVentaSerializer


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


class ProveedorView(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class ProveedorIDNombreView(viewsets.ModelViewSet):
    serializer_class = ProveedorIDNombreSerializer
    queryset = Proveedor.objects.all()


class LoteView(viewsets.ModelViewSet):
    serializer_class = LoteSerializer
    queryset = Lote.objects.all()


class VentaView(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()


class ProductoLoteProveedorView(viewsets.ModelViewSet):
    serializer_class = ProductoLoteProveedorSerializer
    queryset = Producto.objects.all()


class VentaPostAPIView(generics.CreateAPIView):
    # class VentaPostAPIView(viewsets.GenericViewSet):
    serializer_class = PostVentaSerializer

    print('================================')

    print('================================')
    # return Response({"mensaje": "respuesta"})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        # intercepta los datos
        print(request.data)

        if serializer.is_valid():
            try:
                venta = serializer.save()
                # print('serializer.data ======> ', serializer.data)
                print('==========================')
                print('==========================')
                # print('serializer.validated_data ======> ',
                #   serializer.validated_data)
                print('==========================')
                print('==========================')
                # print('VENTA ======> ', Venta.objects.get(id = venta))
                print('VENTA ======> ', venta)
                print('serializer.validated_data ======> ')
                print('serializer.validated_data======> ',
                      venta['lote_cantidad'])
                # print('serializer.data ======> ', serializer.data)
                return Response({'message': 'Producto creado correctamente!', 'data': venta}, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response({'error': 'No son válidas algunas cantidades de productos!'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        print('serializer.data no válido ======> ',
              serializer)  # intercepta los datos
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detalle de una venta => productos, cantidades, precios, fecha, empleado, total
# Sólo GET
# Url => http://localhost:8000/drf-endpoints/api/v1/vget/  2/

class VentaDetalleViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = Venta2Serializer
    # queryset = Venta.objects.all()
    queryset = Tabla_intermedia_venta.objects.all()

    def retrieve(self, request, *args, **kwargs):
        venta_id = kwargs.get('pk')
        queryset = self.queryset.filter(
            venta_id=venta_id).select_related('venta')
        if queryset.exists():
            venta = queryset[0].venta
            serializer = self.get_serializer(queryset, many=True)
            return Response({'venta_id': venta_id, 'vendedor': venta.usuario,
                             'fecha': venta.fecha,
                             'venta': serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"detail": "No se encontraron registros para el venta_id dado."},
                        status=status.HTTP_404_NOT_FOUND)


class GetAllVentasViewSet(viewsets.GenericViewSet):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    print('authentication_classes ===> ', authentication_classes)
    print('permission_classes ===> ', permission_classes)

    serializer_class = GetAllVentaSerializer
    queryset = Venta.objects.all()

    # queryset = Venta.objects.get(id=1).tabla_intermedia_venta_set.all()
    # queryset = Venta.objects.tabla_intermedia_venta_set.all()
    # print('===== View Queryset =====')
    # print('===== View Queryset =====')
    # print(queryset)
    # print('===== View Queryset =====')
    # print('===== View Queryset =====')

    def list(self, request, *args, **kwargs):
        print('list request ===> ')
        print('request.user ===> ', request.user)
        print('request.user ===> ', User.objects.get(
            username=request.user))
        print('request.auth ===> ', request.auth)
        print(request)
        print(request.session)
        print(request.session.get_session_cookie_age())
        queryset = self.get_queryset()
        serializer = GetAllVentaSerializer(queryset, many=True)
        return Response(serializer.data)


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(views.APIView):

    def get(self, request, *args, **kwargs):
        # Enviar el token CSRF
        csrf_token = get_token(request)
        print('Token ===========> ')
        print(csrf_token)
        return Response({'message': 'Token CSRF generado', 'csrfToken': csrf_token}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # token, created = Token.objects.get_or_create(user=user)
        # return Response({'token': token.key})
        print("POST /login/ - Datos recibidos:")
        print("Username:", request.data.get('username'))
        print("Password:", request.data.get('password'))
        print("Cookies:", request.COOKIES)
        print("CSRF Token from Cookie:", request.COOKIES.get('csrftoken'))

        print("request['username'] =======> ")
        print(request.data['username'])
        print(request.data['password'])
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('hay usuairo')
            login(request, user)
            return Response({'message': 'Login exitoso', 'usuario': request.data['username']}, status=status.HTTP_200_OK)
        else:
            print('no hay usuario')
            return Response({'message': 'No se pudo realizar el login'}, status=status.HTTP_401_UNAUTHORIZED)


# def my_view(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# @method_decorator(csrf_exempt, name='dispatch')
class Logout(views.APIView):

    def post(self, request, *args, **kwargs):
        print("POST /logout/ - Intentando cerrar sesión")
        print("Cookies:", request.COOKIES)
        print("CSRF Token from Cookie:", request.COOKIES.get('csrftoken'))

        logout(request)
        print("Sesión cerrada.")
        return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
