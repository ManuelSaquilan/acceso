import csv, os
from django.shortcuts               import render,get_object_or_404
from django.urls                    import reverse_lazy
from django.views.generic           import TemplateView
from django.views.generic.list      import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.db                      import models
from django.shortcuts               import render, redirect
from django.views                   import View

from django.db.models import Q

from .models                        import Evento, Invitados

from django.http import HttpResponse, HttpResponseRedirect
import cv2
from pyzbar.pyzbar import decode
from django.core.files.base import ContentFile
from datetime import datetime
from .models import Invitados
import qrcode
from io import BytesIO
import base64
import zipfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.

class EventoBaseView(View):
    """ESTA CLASE NO SE PONE EN LAS URLS"""
    template_name = "evento.html"
    model         = Evento
    fields        = "__all__"
    success_url = reverse_lazy("eventos:evento_all")

class EventoListView(EventoBaseView,ListView):
    context_object_name = 'eventos'
    
class EventoDetailView(EventoBaseView,DetailView):
    template_name = "eventos_detail.html"
    extra_content={"Titulo" : "Detalle del Evento"}

    
class EventoCreateView(EventoBaseView,CreateView):
    template_name = "eventoscreate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = "CREA UN NUEVO EVENTO"
        context['tipo'] = "Crear Evento"
        return context
    
    
class EventoUpdateView(EventoBaseView,UpdateView):
    template_name = "eventoupdate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = "Actualiza el Evento"
        context['tipo'] = "Actualiza Evento"
        return context

#def Evento_Update(request, pk):
#    evento = Evento.objects.get(idEvento=pk)
#    todo = request.POST
#    print(todo)
#    descripcion = request.POST['descripcion']
#    lugar = request.POST['lugar']
#    fechainicio = request.POST['fechaInicio']
#    video = request.POST['video']
#    imagen = request.POST['imagen']
#    evento.descripcion = descripcion
#    evento.lugar = lugar
#    evento.fechaInicio = fechainicio
#    if video:
#        evento.video = video
#    if imagen:
#        evento.imagen = imagen
#    evento.save()
#    return redirect('eventos:evento_all')

                                                     
"""class InvitadosView(ListView):
    
    invitados = Invitados.objects.all()
    eventos = Evento.objects.all()
    template_name = "invitado.html"
    extra_content = {'invitados':invitados,
                     'evento_list':eventos
    }
    success_url   = reverse_lazy('ordenes:invitados')

    def get_queryset(self):
        return Invitados.objects.all()"""
    
def BuscaEvento(request):
    
    if request.method == 'POST':
        buscar_evento = request.POST.get("evento")            
        evento_buscado = Evento.objects.filter(idEvento=buscar_evento)
        return render(request, 'pantalla.html',{'evento_buscado':evento_buscado})
    if request.method == 'GET':         
        evento_list = Evento.objects.filter(activo=True)
        return render(request, 'invitado.html',{'evento_list':evento_list})

    
"*** P A N T A L L A ***"
def BuscaInvitado(request):
    invitados =Invitados.objects.all()
    if request.method == 'POST':
        buscar_invitado = request.POST.get("updateinvitado")
        buscar_evento = request.POST.get("eventoseleccionado")
        qr = buscar_invitado.split('-')
        
        eventoprincipal = Evento.objects.filter(idEvento=buscar_evento)
        
        buscar_invitado=qr[0]
        if buscar_invitado:
            invitadosBuscados = Invitados.objects.filter(idInvitado=buscar_invitado,idEvento=buscar_evento)
            for i in invitadosBuscados:
                ingresodeinvitado = i.ingreso
                horaingreso = i.hora_ingreso
                msj = i.mensaje
            if msj == "None":
                msj = ""
            if invitadosBuscados:
                print(invitadosBuscados)
                if ingresodeinvitado:
                
                    mensaje="Ud . ya ingresó al evento a  las "+str(horaingreso.strftime('%H:%M'))+" hrs."
                    mensajepersonal =""
                else:
                    invitadosBuscados.update(ingreso=True, hora_ingreso=datetime.now())
                    mensaje="Gracias por venir !!"
                    mensajepersonal =msj
                print("coincidencia", mensajepersonal)
                return render(request, 'pantalla.html',{'invitado_buscado':invitadosBuscados,'evento_buscado':eventoprincipal,'mensaje':mensaje,'mensajepersonal':mensajepersonal})
            else:
                print("sin coincidencia")
                mensaje="Ud. no tiene acceso a este evento"
                return render(request, 'pantalla.html',{'invitado':invitados,'evento_buscado':eventoprincipal,'mensaje':mensaje})           
        else:
            return render(request, 'pantalla.html',{'invitado':invitados,'evento_buscado':eventoprincipal})


def InvitadosUpdate(request):
    eventos = Evento.objects.all()
    evento_list = Evento.objects.filter(activo=True)
    if request.method == 'POST':
        buscar_evento = request.POST.get("eventoupdate")
        #obtener el id del evento a partir de su nombre
        if buscar_evento:
            invitados = Invitados.objects.filter(idEvento=buscar_evento)
            evento = Evento.objects.filter(idEvento=buscar_evento)
            print(buscar_evento)
            return render(request, 'invitadosupdate.html',{'evento_list':evento_list,'invitados':invitados,
                                                           'evento_buscado':buscar_evento,"evento":evento})


    if request.method == 'GET':         
        return render(request, 'invitadosupdate.html',{'evento_list':evento_list})


class InvitadoBaseView(View):
    model=Invitados
    fields        = "__all__"
    success_url   = reverse_lazy('eventos:invitados_update')

def InvitadoUpdate(request,pk):
    invitado = get_object_or_404(Invitados, idInvitado=pk)
    return render(request, 'invitadoupdate.html',{"tipo": "Actualizar Invitado","invitado":invitado})
    
def invitado_updaterecord(request, pk):
    invitado = Invitados.objects.get(idInvitado=pk)
    ingreso = request.POST['ingreso']
    mensaje = request.POST['mensaje']
    nombre = request.POST['nombre']
    buscar_evento = request.POST['idEvento']
    invitado.ingreso = ingreso
    invitado.mensaje = mensaje
    invitado.nombre = nombre
    invitado.save()
    evento_list = Evento.objects.filter(activo=True)
    invitados = Invitados.objects.filter(idEvento=buscar_evento)
    evento = Evento.objects.filter(idEvento=buscar_evento)
    return render(request, 'invitadosupdate.html',{'evento_list':evento_list,'invitados':invitados,
                                                'evento_buscado':buscar_evento,"evento":evento})



class InvitadoCreate(InvitadoBaseView,CreateView):
    template_name='invitadocreate.html'
    evento_list = Evento.objects.filter(activo=True)
    extra_context = {"tipo": "Aceptar","evento_list":evento_list}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento_id'] = self.kwargs.get('evento_id',None)
        context['evento'] = Evento.objects.get(idEvento=self.kwargs.get('evento_id')).descripcion
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        invitado = form.save(commit=False)
        invitado.generate_qr()
        invitado.save()
        evento_list = Evento.objects.filter(activo=True)
        buscar_evento = self.kwargs.get('evento_id',None)
        invitados = Invitados.objects.filter(idEvento=buscar_evento)
        evento = Evento.objects.filter(idEvento=buscar_evento)
        return render(self.request, 'invitadosupdate.html', {'evento_list':evento_list,'invitados':invitados,
                                                'evento_buscado':buscar_evento,"evento":evento})
## ///////// NO LO USO  ///////////
def exportar_invitados(request,pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invitados.csv"'

    writer = csv.writer(response)
    writer.writerow(['IdInvito','IdEvento','Nombre', 'Evento','Fecha del Evento','Hora de ingreso', 'Ingresó'])

    invitados = Invitados.objects.filter(idEvento=pk)
    for invitado in invitados:
        writer.writerow([invitado.idInvitado,invitado.idEvento.idEvento,invitado.nombre,invitado.idEvento.descripcion,invitado.idEvento.fechaInicio  ,invitado.hora_ingreso, invitado.ingreso])

    return response


## ///// NO LO USO ///////////
def exportar_qrs(request, pk):
    response = HttpResponse(content_type='application/zip')
    zip_filename = 'qrs.zip'
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    zip = zipfile.ZipFile(response, 'w')

    invitados = Invitados.objects.filter(idEvento=pk)
    for invitado in invitados:
        qr_filename = f'qr_{invitado.idInvitado}.jpg'
        qr_image = generate_qr_image(invitado.idInvitado, pk, qr_filename)
        zip.writestr(qr_filename, qr_image)

    zip.close()
    return response

def generate_qr_image(invitado_id, evento_id, filename):
    invitado = Invitados.objects.get(idInvitado=invitado_id)
    evento = Evento.objects.get(idEvento=evento_id)

    # Generar el código QR con los datos del invitado y el evento
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{invitado.idInvitado}-{evento.idEvento}-Invitado: {invitado.nombre}\nEvento: {evento.descripcion}")
    qr.make(fit=True)

    # Convertir a PIL.Image
    img = qr.make_image(fill_color="black", back_color=(255, 255, 255)) # Cambiar el parámetro 'back_color' a un entero o una tupla de tres elementos

    # Guardar la imagen en un archivo temporal
    img.save(filename, format="JPEG")

    # Abrir el archivo temporal y leer su contenido en memoria
    with open(filename, "rb") as f:
        img_data = f.read()

    # Eliminar el archivo temporal
    os.remove(filename)

    return img_data

from io import BytesIO
import qrcode
from PIL import Image

def generate_qr(self):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{self.idInvitado}-{self.idEvento}-Invitado: {self.nombre}\nEvento: {self.idEvento.descripcion}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color=(255, 255, 255))

    img_io = BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)

    img_data = base64.b64encode(img_io.read()).decode('utf-8')

    return f"data:image/jpeg;base64,{img_data}"


def etiquetas(request, pk):
    invitados = Invitados.objects.filter(idEvento=pk)
    eventos = Evento.objects.filter(idEvento=pk)
    #ruta = "/static/media/img/"+str(pk)+".jpeg"
    for evento in eventos:
        ruta = "/static/media/"+ str(evento.imagen)
    print(ruta)
    return render(request, 'etiquetas.html', {'invitados': invitados,'ruta':ruta})
    
def etiquetas_individuales(request, pk1, pk2):
    invitado = Invitados.objects.filter(idEvento=pk1,idInvitado=pk2)
    eventos = Evento.objects.filter(idEvento=pk1)
    #ruta = "/static/media/img/"+str(pk1)+".jpeg"
    for evento in eventos:
        ruta = "/static/media/"+ str(evento.imagen)
    print(ruta)
    print(pk1)
    print(pk2)
    return render(request, 'etiquetas_individuales.html', {'invitado': invitado,'ruta':ruta})

def lista_pdf(request, pk):
    # Obtener los invitados del evento seleccionado
    invitados = Invitados.objects.filter(idEvento=pk)
    evento = Evento.objects.filter(idEvento=pk)
    print("evento:",evento)
    # Crear un buffer para el PDF
    buffer = BytesIO()

    # Crear un objeto canvas para dibujar el PDF
    c = canvas.Canvas(buffer, pagesize=A4)

    # Configurar la fuente y el tamaño de letra
    c.setFont("Helvetica", 18)
    c.setFillColor(aColor='blue')

    # Coloca el nombre del evento
    x_titulo = 10 * cm
    y_titulo = 28 * cm
    for nombre_evento in evento:
        c.drawCentredString(x_titulo, y_titulo, f"{nombre_evento.descripcion}")

    # Configurar la fuente y el tamaño de letra
    c.setFont("Helvetica", 12)
    c.setFillColor(aColor='black')

    # Iterar sobre los invitados y dibujar la información
    x_nombre = 2.54 * cm
    x_qr = x_nombre + 13 * cm
    y = 23.4 * cm

    for invitado in invitados:
        c.drawString(x_nombre, y + 2 *cm, f"{invitado.nombre}")
        c.drawImage(invitado.qr.path, x_qr, y, width=100, height=100)
        
        # Dibujar una línea
        c.line(x_nombre, y, x_qr + 100, y)

        y -= 4 * cm
        
    # Guardar el PDF
    c.save()

    # Devolver el PDF como respuesta
    buffer.seek(0)
    # Enviar el archivo PDF como respuesta HTTP
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_invitados.pdf"'

    return response 
    #return redirect("eventos:evento_all")

    #return HttpResponse(buffer.getvalue(), content_type='application/pdf')