from django.utils import timezone
import pytz

#Import del proyecto
from .models import Evento

#Definimos funciones
def prox_evento():
    #Formato de entrega: "6 13, 2019 11:00:00"
    try: 
        prox_fecha = Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').first().fecha_inicio
    except:
        prox_fecha = timezone.now()
    str_prox_fecha = prox_fecha.strftime("%m %d, %Y %H:%M:%S")
    return str_prox_fecha

def duracion_congreso():
    try: 
        duracion = Evento.objects.get(tipo=2).fecha_inicio - Evento.objects.get(tipo=1).fecha_inicio 
        if duracion.seconds > 0:
            duracion = duracion.days + 1
        else: 
            duracion = duracion.days
    except: 
        duracion = "0"
    return duracion
