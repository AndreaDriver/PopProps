from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib import messages
from .models import DatosPersonales, Direccion #Usuario
from django.http import HttpResponseRedirect

# Create your views here.
def Bienvenida(request):
   iddSesionU = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO

   #Borrar sesion del usuarios
   if iddSesionU is not None:
      del request.session['id']

   return render(request, 'Pagina_Bienvenida.html')


def registro(request):
   model = User
   if request.method == 'POST':
      username = request.POST.get('username')
      if model.objects.filter(username=username).exists():
         messages.error(request, "El correo electrónico ya esta registrado.")
         return render(request, 'Registro.html')
      else:
         if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            o_ref = model(username=username, password=password)
            o_ref.save()
            id = model.objects.only('id').get(username=username).id
            request.session['id'] = id #SE GUARDA EL ID DEL USUARIO
            return HttpResponseRedirect('/Continua/')

   else:
      return render(request, 'Registro.html')


def continuar(request):
   if request.method == 'POST':
      if request.POST.get('nombres') and request.POST.get('apellidos') and request.POST.get(
              'pais') and request.POST.get('estado') and request.POST.get('ciudad') and request.POST.get(
         'codigoPostal') and request.POST.get('direccion'):
         idd = request.session.get('id')
         idUser = User.objects.get(id=idd)
         nombres = request.POST.get('nombres')
         apellidos = request.POST.get('apellidos')
         uNom = DatosPersonales(nombres=nombres, apellidos=apellidos, idUser=idUser)
         uNom.save()

         pais = request.POST.get('pais')
         estado = request.POST.get('estado')
         ciudad = request.POST.get('ciudad')
         codigoPostal = request.POST.get('codigoPostal')
         direccion = request.POST.get('direccion')
         uDir = Direccion(pais=pais, estado=estado, ciudad=ciudad, codigoPostal=codigoPostal, direccion=direccion,
                          idUser=idUser)
         uDir.save()

         # eliminar sesion
         del request.session['id']
      return HttpResponseRedirect('/InicioSesion/')
   else:
      return render(request, 'ContinuarRegistro.html')


def inicio(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      usNameBD=""
      try:
         usNameBD = User.objects.get(username=username).username
         usConBD = User.objects.get(username=username).password
         # print(usNameBD, usConBD)
         if username == usNameBD and password == usConBD:
            id = User.objects.only('id').get(username=username).id
            request.session['id'] = id  # sesion
            return HttpResponseRedirect('/Catalogo/')
         else:
            messages.error(request, "Correo electrónico o contraseña incorrectos")
            return render(request, 'inicioSesion.html')
      except:
         messages.error(request, "Correo electrónico o contraseña incorrectos")
         return render(request, 'inicioSesion.html')
   else:
      return render(request, 'inicioSesion.html')