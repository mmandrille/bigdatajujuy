#Import Standard
from django import forms
from django.forms import ModelForm
#import extras:

#Import Personales
from .models import Conferencias

#Definiciones oficiales:

#creamos ModelForm
class ConferenciaForm(ModelForm):
    class Meta:
        model = Conferencias
        fields = ['titulo', 'descripcion', 'archivo',]
    descripcion = forms.CharField(widget=forms.Textarea )