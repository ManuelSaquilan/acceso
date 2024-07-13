from django.db import models
import os, qrcode
from django.core.files import File
from django.core.exceptions import ValidationError

def validate_video(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError('Solo se permiten archivos MP4 para video.')
    
def validate_imagen(value):
    if not value.name.endswith('.jpeg'):
        raise ValidationError('Solo se permiten archivos JPEG para imagen.')
    
# Create your models here.
class Evento(models.Model):
    idEvento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, null=False,verbose_name='Nombre')
    fechaInicio = models.DateTimeField(null=False, verbose_name='fecha')
    lugar = models.CharField(max_length=30,null= False,verbose_name='Lugar')
    activo  = models.BooleanField(default=True,verbose_name='Activo')
    video = models.FileField(upload_to='video/',null=True,blank=True, validators=[validate_video], error_messages={'invalid': 'Solo se permiten archivos MP4 para video.'})
    imagen = models.FileField(upload_to='img/',null=True,blank=True, validators=[validate_imagen], error_messages={'invalid': 'Solo se permiten archivos JPEG para imagen.'})

    class Meta:
        db_table = "eventos"

    def __str__(self):
        return f"Evento: {self.descripcion} {self.fechaInicio} lugar {self.lugar}"
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]
    


class Invitados(models.Model):
    idInvitado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70, null=False, verbose_name='Nombre',blank=False)
    idEvento = models.ForeignKey(Evento,on_delete=models.CASCADE,null=False,blank=False)
    ingreso = models.BooleanField(verbose_name='Ingresó', null=False,default=False)
    hora_ingreso = models.TimeField(verbose_name='Hora de Ingreso', null=True,blank=True)
    qr = models.ImageField(upload_to='qr', null=True, blank=True)
    mensaje = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name='invitado'
        verbose_name_plural='invitados'
        db_table = 'invitados'
    
    

    def generate_qr(self):
        # Generar el código QR con los datos del invitado y el evento
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{self.idInvitado}-{self.idEvento}-Invitado: {self.nombre}\nEvento: {self.idEvento.descripcion}\n @2004 SSCOM INFORMATICA - DERECHOS RESERVADOS")
        qr.make(fit=True)

        # Convertir a PIL.Image
        img = qr.make_image(fill_color="black", back_color=(255, 255, 255))

        # Guardar la imagen en un archivo temporal
        filename = f'qr_{self.idInvitado}.jpg'
        img.save(filename, format="JPEG")

        # Guardar la imagen en el campo qr del modelo Invitados
        self.qr.save(filename, File(open(filename, 'rb')))

        # Eliminar el archivo temporal
        os.remove(filename)

    def __str__(self):
        fila = "Invitado: " + str(self.nombre) + " - " + " Evento: " + str(self.idEvento.descripcion) + " - " +" Ingreso: " + str(self.ingreso) +" - " + " Hora: " + str(self.hora_ingreso) + " - " +" IdEvento: " + str(self.idEvento.idEvento)+ " - " + " Mensaje: " + str(self.mensaje)
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]
    

