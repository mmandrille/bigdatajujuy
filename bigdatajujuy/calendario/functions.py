from django.utils import timezone
import pytz

#Import del proyecto
from .models import Evento

#Definimos funciones
def prox_evento():
    try: 
        evento = Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').first()
        return evento.get_tipo_display(), evento.fecha_inicio
    except Evento.DoesNotExist or AttributeError:
        return "Sin Eventos(Hora Actual)", timezone.now()

def duracion_congreso():
    try: 
        duracion = Evento.objects.get(tipo=2).fecha_inicio - Evento.objects.get(tipo=1).fecha_inicio 
        if duracion.seconds > 0:
            duracion = duracion.days + 1
        else: 
            duracion = duracion.days
    except Evento.DoesNotExist or AttributeError: 
        duracion = "0"
    return duracion
