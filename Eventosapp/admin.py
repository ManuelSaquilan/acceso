
from django.contrib import admin
from .models import Evento, Invitados
from django.utils.html import format_html
# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    search_fields = ['descripcion']
    ordering = ['descripcion']

class InvitadosAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    list_display = ('nombre', 'evento_name','mensaje','ingreso', 'hora_ingreso', 'qr_image')

    def evento_name(self, obj):
        return obj.idEvento.descripcion
        evento_name.short_description = 'Evento'

    def qr_image(self, obj):
        if obj.qr:
            return format_html('<img src="{}" width="100" height="100" />', obj.qr.url)
        else:
            return '-'
    qr_image.short_description = 'QR Code'

admin.site.register(Evento, EventoAdmin)
admin.site.register(Invitados, InvitadosAdmin)