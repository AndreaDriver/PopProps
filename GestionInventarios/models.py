from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Franquicia(models.Model):
    Franquicia = models.CharField(max_length=50)

    def __str__(self):
       return self.Franquicia
       # return "Franquicia: %s" %(self.Franquicia)

class Categoria(models.Model):
    Categoria = models.CharField(max_length=50)

    def __str__(self):
       return self.Categoria

class Articulo(models.Model):
    Nombre = models.CharField(max_length=50)
    Precio = models.FloatField()
    Imagen = models.ImageField(upload_to="articulos", null=True)
    Descripcion = models.CharField(max_length=200)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    Franquicia = models.ForeignKey(Franquicia, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class PedidoxArticulo(models.Model):
    Cantidad = models.IntegerField()
    Articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)



class Carrito(models.Model):
    FechaPedido = models.DateField()
    PrecioTotal = models.FloatField()
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE)
    PedidoxArticulo = models.ManyToManyField(PedidoxArticulo)

    def IDs_pedido_x_art(self):
        return "\n".join(str([p.id for p in self.PedidoxArticulo.all()]))



