from django.utils import timezone
import pytz

#Import del proyecto
from .models import Evento

#Definimos funciones
def prox_evento():
    try:  evento = Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').first()
    except Evento.DoesNotExist: return "Sin Eventos(Hora Actual)", timezone.now()
    return evento.get_tipo_display(), evento.fecha_inicio

def duracion_congreso():
    try: 
        duracion = Evento.objects.get(tipo=2).fecha_inicio - Evento.objects.get(tipo=1).fecha_inicio 
        if duracion.seconds > 0:
            duracion = duracion.days + 1
        else: duracion = duracion.days
        return duracion
    except Evento.DoesNotExist: 
        duracion = "0"