#Import Standard
from django import forms
from django.forms import ModelForm
#import extras:

#Import Personales
from .models import Inscriptos

#Definiciones oficiales:

#creamos ModelForm
class InscriptoForm_asistente(ModelForm):
    class Meta:
        model = Inscriptos
        fields = ['nombres', 'apellido', 'num_doc', 'telefono', 'email', 'categoria']
        widgets = {'categoria': forms.HiddenInput()}

class InscriptoForm_expositor(ModelForm):
    class Meta:
        model = Inscriptos
        fields = ['nombres', 'apellido', 'num_doc', 'telefono', 'email', 'descripcion', 'foto', 'categoria']
        widgets = {'categoria': forms.HiddenInput()}
    descripcion = forms.CharField(label='Acerca de Mi', widget=forms.Textarea )