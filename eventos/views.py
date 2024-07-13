from django.http import HttpResponse
from django.views.generic import TemplateView

# Request:para realizar correciones
# HttpResponse: para enviar la respuesta usando el protocolo HTTP

# esto es una vista
def bienvenida(request,tarjeta, ingreso):
    if tarjeta == "1":
        mensaje = "Ud no tiene acceso a este evento"
    else:
        if ingreso == "1":
            mensaje = "Ud. ingreso a las 22 hs"
        else: 
            mensaje = "Bienvenido NN a este evento"
    mostrar = mensaje
    return HttpResponse(mostrar)

class LandingPage(TemplateView):
    template_name = "bloques/index.html"
    extra_context = {
        "titulo_pagina" : "Bienvenida"
    }



        
