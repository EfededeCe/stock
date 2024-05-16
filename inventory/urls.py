from django.urls import path, include
from rest_framework import routers
from inventory import views

router = routers.DefaultRouter()
router.register(r'productos', views.ProductoView, 'productos')
router.register(r'proveedores', views.ProveedorView, 'proveedores')
router.register(r'lotes', views.LoteView, 'lotes')

urlpatterns = [
  path('api/v1/', include(router.urls))
]

