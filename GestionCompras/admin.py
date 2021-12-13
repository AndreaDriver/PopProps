from django.contrib import admin
from GestionCompras.models import *

class PagoAdmin(admin.ModelAdmin):
    list_display = ("IdUser","Pago", "carrito","FechaPago")
    list_filter = ("IdUser", "carrito", "FechaPago")
    search_fields = ("carrito","FechaPago")
    list_per_page = 10

class EnviosAdmin(admin.ModelAdmin):
    list_display = ("IdUser", "Estado", "idPago", "FechaEntrega")
    list_filter = ("IdUser", "FechaEntrega")
    search_fields = ("idPago", "Estado")
    list_per_page = 10

admin.site.register(Pago, PagoAdmin)
admin.site.register(Envios, EnviosAdmin)
