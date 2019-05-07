from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import *
from django.utils import timezone
from tinymce.models import HTMLField

#Create your models here.
class Evento(models.Model):
    nombre = models.CharField('Titulo', max_length=200)
    portada = models.FileField(upload_to='eventos/portadas/', default='/archivos/defaults/noimage.gif')
    descripcion = HTMLField()
    fecha_inicio = models.DateTimeField('Fecha del Evento', default=datetime.datetime.now)
    fecha_fin = models.DateTimeField('Fecha de fin del Evento', default=datetime.datetime.now)
    models.ForeignKey(User, on_delete=models.CASCADE)
    importante = models.BooleanField(default=False)
    #ubicacion = ciudades? 
    def __str__(self):
        return self.nombre + ' ' + str(self.fecha_inicio)