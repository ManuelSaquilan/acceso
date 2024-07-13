from django.urls import path
from . import views
from .views import      EventoListView\
                    ,   EventoDetailView\
                    ,   EventoCreateView\
                    ,   EventoUpdateView\
                    ,   BuscaInvitado\
                    ,   BuscaEvento\
                    ,   InvitadoUpdate\
                    ,   InvitadosUpdate\
                    ,   InvitadoCreate\
                    ,   exportar_invitados\
                    ,   exportar_qrs\
                    ,   etiquetas\
                    ,   invitado_updaterecord\
                    ,   etiquetas_individuales\
                    ,   lista_pdf\
                    #,   Evento_Update\

app_name = "eventos"

urlpatterns = [
    path("", EventoListView.as_view(), name="evento_all"),
    path("evento_create/", EventoCreateView.as_view(), name="evento_create"),
    path("detail/<int:pk>", EventoDetailView.as_view(), name="evento_detail"),
    path("evento_update/<int:pk>", EventoUpdateView.as_view(), name="evento_update"),
    #path("evento_updaterecord/<int:pk>", Evento_Update, name="evento_updaterecord"),
    path("invitados",BuscaEvento,name="invitados"),
    path("evento",BuscaInvitado,name="invitados_detail"),
    path("invitados_update",InvitadosUpdate,name="invitados_update"),
    path("invitado_update/<int:pk>",InvitadoUpdate,name="invitado_update"),
    path("invitado_create/<int:evento_id>",InvitadoCreate.as_view(),name="invitado_create"),
    path('invitados/exportar/<int:pk>', exportar_invitados, name='exportar_invitados'),
    path('invitados/exportarqr/<int:pk>', exportar_qrs, name='exportar_qrinvitados'),
    path('etiquetas/<int:pk>',etiquetas,name='etiquetas'),
    path('etiquetas_individuales/<int:pk1>/<int:pk2>',etiquetas_individuales,name='etiquetas_individuales'),
    path('invitado_updaterecord/<int:pk>', invitado_updaterecord, name='invitado_updaterecord'),
    path('lista/<int:pk>',lista_pdf,name='lista_pdf'),
]