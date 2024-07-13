from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['descripcion', 'lugar', 'fechaInicio', 'activo']
        widgets = {
            'fechaInicio': forms.DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
        }