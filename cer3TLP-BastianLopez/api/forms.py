from django import forms
from .models import Evento

class FormularioEvento(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'comentarios', 'tipo']
        widgets = {
            'tipo': forms.Select(choices=Evento.TIPO_EVENTO),
        }
