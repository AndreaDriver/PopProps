from django.shortcuts import render
from .models import Articulo
from .models import Franquicia
from .models import PedidoxArticulo
from .models import Carrito
from django.http import HttpResponse
from django.db.models import Q
from django.utils.timezone import datetime
from django.http import HttpResponseRedirect




# Create your views here.
def Catalogo(request):
    list_articulos = []
    list_franquicias = []
    # ll=[]
    busqueda = ""
    franquiciaSeleccionada = ""
    # ll = request.POST.get('listaSeleccionada')
    # print(request.session.get('id'))



    list_franquicias = Franquicia.objects.all()
    # print(list_franquicias)
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

# def Catalogo(request):
#     list_articulos = Articulo.objects.all()
#     return render(request, 'Catalogo.html', {"articulos": list_articulos})

def error_404(request, exception):
    return render(request, '404.html')


# w = 0;


def CarritoCompra(request, string):
    listaA = []
    listaIDPedidos = []
    listaB = []
    botonComprar = ""



    # listaA = string.split(',')

    # a =
    idd = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO
    # hoyMerito = datetime.today().strftime('%Y-%m-%d')
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
        cantidadN = int(cantidad)

        # Verificar no 0
        if cantidadN > 0:

            botonComprar = "si"
            # ESTE SI SIRVE
            # # Obtener Id del art.
            artSeleccionado = Articulo.objects.only('id').get(id=idProductoSeleccionado).id
            # print(artSeleccionado)
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


            # print(ddd)


            # Mandar nuevo String
            list_articulos_Eliminar = Articulo.objects.filter(id=artSeleccionado)
            # list_articulos.delete(list_articulos_Eliminar)
            # listaB.pop(idProductoSeleccionado)

            idProductoSeleccionadoN = int(idProductoSeleccionado)
            # print(listaB, idProductoSeleccionadoN)
            listaB.remove(idProductoSeleccionadoN)
            # print(listaB)
            # Convertirlos a str
            listaA = []

            for x in listaB:
                aaa = str(x)
                listaA.append(aaa)
            # print(listaA)
            # print(listaB)
            string = listaA
            list_articulos = list_articulos.filter(~Q(id=artSeleccionado))
            StrA = ",".join(listaA)
            link = '/Carrito/'+StrA
            # print(link)
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
            # pp= PedidoxArticulo.



            # pedidoodfdf = PedidoxArticulo.objects.only('Articulo_id').get(id=x).Articulo_id

            # print(lista_ID_Pedidos_articulos2.values(), pedi)


            precioAcomulado = 0
            for x in listaPedi:
                if x is not 0:
                    subtotal = 0
                    pedidoo = PedidoxArticulo.objects.only('Articulo_id').get(id=x).Articulo_id #id del articulo
                    pedidoPrecio = Articulo.objects.only('Precio').get(id=pedidoo).Precio #id precio del art.
                    cantidad = PedidoxArticulo.objects.only('Cantidad').get(id=x).Cantidad #id del articulo
                    subtotal = pedidoPrecio * cantidad
                    precioAcomulado =  precioAcomulado + subtotal
            # print(hoyMerito)
            idUssser = request.session.get('id')  # SE OBTIENE EL ID DEL USUARIO

            #SI SIRVE
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
            print('sdsdf')







            # list_articulos.filter(id is not artSeleccionado)

            # return render(request, 'Carrito/',string)
            # print(list_articulos.values())
        # print(list_articulos.values())






        #Obtener franquicia
        # my_filtro2 = Q()
        # for x in list_articulos:
        #     my_filtro2 = my_filtro | Q(id=x.Franquicia_id)
        # list_articulos2 = Franquicia.objects.filter(my_filtro2)
        # print(list_articulos2.values())

        # list_articulos.append(list_articulos2)

        # listaF = list_articulos.values('Categoria_id')
        # listaFNombres = Franquicia.objects.filter(id=listaF)
        # print(listaF.values())

        # print(list_articulos.values('Descripcion'))

    return render(request, 'Carrito.html', {"articulos": list_articulos})

