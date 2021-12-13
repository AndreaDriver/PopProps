from django.shortcuts import render
from .models import Articulo
from .models import Franquicia
from .models import PedidoxArticulo
from .models import Carrito
from django.http import HttpResponse
from django.db.models import Q
from django.utils.timezone import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages




# Create your views here.
def Catalogo(request):
    idd = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO
    iddPedidoss = request.session.get('Pedidos')
    MontoSesion = request.session.get('Monto')
    CarritoSession = request.session.get('idCarrito')


    #Borrar lista de pedidos anteriores, montos anteriores talvez no concretados, asi como los carritos no pagados.
    if iddPedidoss is not None:
        del request.session['Pedidos']

    if MontoSesion is not None:
        del request.session['Monto']

    if CarritoSession is not None:
        del request.session['idCarrito']
    # del request.session['id']

    #Comprobar inicio de sesion
    if idd is not None:
        print(idd)

        list_articulos = []
        list_franquicias = []
        busqueda = ""
        franquiciaSeleccionada = ""



        list_franquicias = Franquicia.objects.all()
        if request.method == "POST" and "franquicia" in request.POST:


            franquiciaSeleccionada = request.POST['franquicia']
            id = Franquicia.objects.only('id').get(Franquicia=franquiciaSeleccionada).id
            # print(id)
            list_articulos = Articulo.objects.filter(Franquicia=id)

        elif request.method == "GET" and "txtBuscar" in request.GET:
            busqueda = request.GET["txtBuscar"]

            if busqueda:
                list_articulos = Articulo.objects.filter(Nombre__icontains=busqueda)
                print(list_articulos)
        else:
            list_articulos = Articulo.objects.all()
        return render(request, 'Catalogo.html', {"articulos": list_articulos, "franquicias": list_franquicias})
    else:
        return HttpResponseRedirect('/InicioSesion/')


def error_404(request, exception):
    return render(request, '404Error.html')


def CarritoCompra(request, string):
    iddPrebaIngreso = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO
    # Comprobar inicio de sesion
    if iddPrebaIngreso is not None:

        listaA = []
        listaIDPedidos = []
        listaB = []
        botonComprar = ""



        idd = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO
        hoyMerito = datetime.today()


        listaA = [int(x) for x in string.split(',')]

        #Convertirlos a int
        for x in listaA:
            aa = int(x)
            listaB.append(aa)

        # Obtener lista de articulos
        my_filtro = Q()
        for x in listaB:
            my_filtro = my_filtro | Q(id=x)
        list_articulos = Articulo.objects.filter(my_filtro)

        if 'botonB' in request.GET:
            idProductoSeleccionado = request.GET.get('botonB')
            cantidad = request.GET.get('cantidad')

            if cantidad is not "":

                cantidadN = int(cantidad)

                # Verificar no 0
                if cantidadN > 0:


                    # Obtener Id del art.
                    artSeleccionado = Articulo.objects.only('id').get(id=idProductoSeleccionado).id

                    # # Guardar en BD
                    pedidoXart = PedidoxArticulo(Cantidad=cantidadN, Articulo_id = artSeleccionado)
                    pedidoXart.save()
                    id = PedidoxArticulo.objects.only('id').get(id=pedidoXart.id).id #id de pedido de art.

                    #Guardar lista str de id de PedidoxArticulo en sesion
                    idS = str(id)
                    idd = request.session.get('Pedidos')
                    if idd is None:
                        idd = 0;
                    iddS = str(idd)
                    strPedidoList = iddS + ','+idS
                    request.session['Pedidos'] = strPedidoList

                    # Mandar nuevo String
                    list_articulos_Eliminar = Articulo.objects.filter(id=artSeleccionado)

                    idProductoSeleccionadoN = int(idProductoSeleccionado)

                    listaB.remove(idProductoSeleccionadoN)
                    listaA = []

                    for x in listaB:
                        aaa = str(x)
                        listaA.append(aaa)

                    string = listaA
                    list_articulos = list_articulos.filter(~Q(id=artSeleccionado))
                    StrA = ",".join(listaA)
                    link = '/Carrito/'+StrA
                    if link == '/Carrito/':
                        return render(request, 'Carrito.html')
                    else:
                        return HttpResponseRedirect(link)

        if 'btnCompra' in request.GET:
            pedi = request.session.get('Pedidos')

            if pedi is not None:

                listaPedi = [int(x) for x in pedi.split(',')] #obtenemos id de pedidos, en forma de lista

                # Obtener lista de id de pedidos de articulos
                my_filtroZZ = Q()
                for x in listaPedi:
                    if x is not 0:
                        my_filtroZZ = my_filtroZZ | Q(id=x)
                lista_ID_Pedidos_articulos = PedidoxArticulo.objects.filter(my_filtroZZ) #lista de objetos de pedidos
                lista_SOLO_ID_Pedidos_articulos= lista_ID_Pedidos_articulos.values_list('pk') #lista de SOLO LOS ID de objetos de pedidos


               #Ver precio acomulado
                precioAcomulado = 0
                for x in listaPedi:
                    if x is not 0:
                        subtotal = 0
                        pedidoo = PedidoxArticulo.objects.only('Articulo_id').get(id=x).Articulo_id #id del articulo
                        pedidoPrecio = Articulo.objects.only('Precio').get(id=pedidoo).Precio #id precio del art.
                        cantidad = PedidoxArticulo.objects.only('Cantidad').get(id=x).Cantidad #id del articulo
                        subtotal = pedidoPrecio * cantidad
                        precioAcomulado =  precioAcomulado + subtotal
                idUssser = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO

                #ingresar a BD
                carrito = Carrito(FechaPedido=hoyMerito, PrecioTotal=precioAcomulado, IdUser_id = idUssser)
                carrito.save()
                for lista_ID_Pedidos_articulos in lista_ID_Pedidos_articulos:
                    carrito.PedidoxArticulo.add(lista_ID_Pedidos_articulos)
                idCarrito = PedidoxArticulo.objects.only('id').get(id=carrito.id).id  # id de CARRITO

                #Sesiones para el pago y id de carrio (para usarse en GestonComprar: Pago)
                request.session['idCarrito'] = idCarrito
                request.session['Monto'] = precioAcomulado

                #se cierra sesion de lista de pedidos
                del request.session['Pedidos']
                return HttpResponseRedirect('/Pago/')
            else:
                messages.error(request, "Necesitas seleccionar el botón de comprar artículo, antes de ir a pagarlo.")

        return render(request, 'Carrito.html', {"articulos": list_articulos})

    else:
        return HttpResponseRedirect('/InicioSesion/')