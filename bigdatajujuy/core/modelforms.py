#Import Standard
from django import forms
from django.forms import ModelForm
#import extras:

#Import Personales
from .models import Conferencia

#Definiciones oficiales:

#creamos ModelForm
class ConferenciaForm(ModelForm):
    class Meta:
        model = Conferencia
        fields = ['titulo', 'descripcion', 'archivo',]
    descripcion = forms.CharField(widget=forms.Textarea )