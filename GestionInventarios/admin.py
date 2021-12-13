from django.contrib import admin
from GestionInventarios.models import Franquicia
from GestionInventarios.models import Articulo
from GestionInventarios.models import Carrito
from GestionInventarios.models import Categoria
from GestionInventarios.models import PedidoxArticulo

# Register your models here.
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("Nombre", "Precio", "Imagen", "Descripcion", "Franquicia", "Categoria")
    search_fields = ("Nombre", "Precio", "Descripcion")
    ordering = ("Nombre",)
    list_per_page = 10

class CarritoAdmin(admin.ModelAdmin):
    list_display = ("FechaPedido", "IdUser", "PrecioTotal", "IDs_pedido_x_art")
    list_filter = ("IdUser", "FechaPedido")
    ordering = ("FechaPedido",)
    list_per_page = 10


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id","Cantidad", "Articulo")
    search_fields = ("id",)
    ordering = ("id",)
    list_per_page = 10

# Register your models here.
admin.site.register(Franquicia)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(PedidoxArticulo, PedidoAdmin)
admin.site.register(Categoria)



