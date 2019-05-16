from django.utils import timezone
import pytz

#Import del proyecto
from .models import Evento

#Definimos funciones
def prox_evento():
    evento = Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').first()
    return evento.get_tipo_display(), evento.fecha_inicio