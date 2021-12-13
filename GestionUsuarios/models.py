from django.db import models
from django.contrib.auth.models import User

class DatosPersonales(models.Model):
   nombres=models.CharField(max_length=50)
   apellidos=models.CharField(max_length=50)
   idUser = models.OneToOneField(User, on_delete=models.CASCADE)

#antes en lugar de User, estaba usuario
class Direccion(models.Model):
   pais=models.CharField(max_length=50)
   estado=models.CharField(max_length=50)
   ciudad=models.CharField(max_length=50)
   codigoPostal=models.IntegerField()
   direccion=models.CharField(max_length=200)
   idUser = models.OneToOneField(User, on_delete=models.CASCADE)

