"""PopProps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from GestionInventarios.views import *
from GestionUsuarios.views import *
from GestionCompras.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Catalogo/', Catalogo),
    path("Bienvenido/", Bienvenida),
    path("InicioSesion/", inicio),
    path("Registro/", registro),
    path("Continua/", continuar),
    path("Carrito/<string>", CarritoCompra),
    path('Pago/', PagoView),
]

# handler404 = error_404

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()




