#Import Standard
from django import forms
from django.forms import ModelForm
#Import Personales
from .models import Inscriptos

#creamos ModelForm
class InscriptoForm_asistente(ModelForm):
    class Meta:
        model = Inscriptos
        fields = ['nombres', 'apellido', 'num_doc', 'telefono', 'email', 'categoria']
        widgets = {'categoria': forms.HiddenInput()}

class InscriptoForm_expositor(ModelForm):
    class Meta:
        model = Inscriptos
        fields = ['nombres', 'apellido', 'num_doc', 'telefono', 'email', 'foto', 'categoria']
        widgets = {'categoria': forms.HiddenInput()}