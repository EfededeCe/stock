from django.urls import path, include
from rest_framework import routers
from inventory import views

router = routers.DefaultRouter()

router.register(r'plp', views.ProductoLoteProveedorView,
                'productos_lote_proveedor')
router.register(r'productos', views.ProductoView, 'productos')
router.register(r'productos-id-desc',
                views.ProductoIDDescView, 'productosIDDesc')
router.register(r'productos-id-codigo',
                views.ProductoIDCodigoView, 'productosIDCodigo')

router.register(r'proveedores', views.ProveedorView, 'proveedores')
router.register(r'proveedores-id-nombre',
                views.ProveedorIDNombreView, 'proveedoresIDNombre')
router.register(r'proveedores-id-url',
                views.ProveedorIDUrlView, 'proveedoresIDUrl')

router.register(r'lotes', views.LoteView, 'lotes')

router.register(r'ventas', views.VentaView, 'ventas')

router.register(r'vget',
                views.VentaDetalleViewSet, 'get_venta')

# router.register(r'vgp',
#                 views.VentaDetalleGetPostViewSet, 'get_post_venta')

router.register(r'gav',
                views.GetAllVentasViewSet, 'get_all_venta')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/presupuesto',
         views.VentaPostAPIView.as_view(), name='api_view'),
]
