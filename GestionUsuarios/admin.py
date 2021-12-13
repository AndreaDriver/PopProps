from django.contrib import admin
from GestionUsuarios.models import *

class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "idUser")
    list_filter = ("nombres", "idUser")
    list_per_page = 10

class DireccionAdmin(admin.ModelAdmin):
    list_display = ("pais", "estado", "ciudad", "codigoPostal", "direccion", "idUser")
    search_fields = ("pais", "estado", "ciudad")
    list_filter = ("idUser",)
    list_per_page = 10

# Register your models here.
admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(Direccion, DireccionAdmin)
