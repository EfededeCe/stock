from django.contrib import admin
from .models import Producto, Proveedor, Lote, Venta , Tabla_intermedia_venta

# modelos que se muestran en el gestor online .
admin.site.register(Venta)
admin.site.register(Tabla_intermedia_venta)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Lote)

