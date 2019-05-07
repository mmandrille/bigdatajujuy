from __future__ import unicode_literals
import datetime
from django.db import models
from tinymce.models import HTMLField
#Agregar Modulos personales
from inscripciones.models import Inscriptos
from calendario.models import Evento
#Elementos del FAQ
class Faq(models.Model):
    orden = models.IntegerField()
    pregunta = models.CharField('Titulo', max_length=200)
    respuesta = HTMLField()
    def __str__(self):
        return self.pregunta

class Conferencias(models.Model):
    expositor = models.ForeignKey(Inscriptos, on_delete=models.CASCADE)
    titulo = models.CharField('Titulo', max_length=200)
    descripcion = HTMLField()
    agenda = models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null=True)
    autorizada = models.BooleanField('Autorizada', default=False)
    def __str__(self):
        return (self.titulo + " por: " + self.expositor.apellido + ', ' + self.expositor.nombres)