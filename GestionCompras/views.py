from django.shortcuts import render
from GestionCompras.models import *
from django.utils.timezone import datetime
from django.http import HttpResponseRedirect
# Create your views here.

def PagoView(request):
    # OBTENER INFORMACION DE LA TRANSACCION DE SESIONES
    # request.session['Monto'] = 1
    idC = request.session.get('idCarrito')
    idM = request.session.get('Monto')
    idU = request.session.get('id')



    # PARA PRUEBA: CERRAR SESIONES
    # del request.session['Monto']
    # del request.session['idCarrito']
    # del request.session['id']
    # del request.session['Pedidos']

    if 'btnCompra' in request.GET:
        if idU is not None and idM is not None and idC is not None:
            idMN = float(idM)
            idCN = int(idC)
            hoyMerito = datetime.today()

            #Guardar en BD
            pagoCarrito = Pago(Pago=idMN, Estado='Pagado', carrito=idCN, IdUser_id=idU, FechaPago=hoyMerito)
            pagoCarrito.save()
            idPago = Pago.objects.only('id').get(id=pagoCarrito.id).id  # id Pago

            EnvioNuevo= Envios(Estado="Pendiente", IdUser_id=idU, idPago_id=idPago)
            EnvioNuevo.save()

            # NECESARIO BORRAR SESIONES
            del request.session['Monto']
            del request.session['idCarrito']
            return HttpResponseRedirect('/Catalogo/')


    return render(request, 'Pago.html', {"Monto": idM})
