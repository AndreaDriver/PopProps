from django.db import models
from GestionInventarios.models import Carrito
from django.contrib.auth.models import User


# Create your models here.
class Pago(models.Model):
    Pago = models.FloatField()
    Estado = models.CharField(max_length=10) #Pagado, devuelto
    carrito = models.IntegerField()
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    FechaPago = models.DateField()



class Envios(models.Model):
    Estado = models.CharField(max_length=10)  #Pendiente de enviar, Entregado
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idPago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    FechaEntrega = models.DateField(null=True, blank=True)
