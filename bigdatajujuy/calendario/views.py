from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
#Import Personales
from .models import Evento

# Create your views here.
def calendario(request):
    eventos = Evento.objects.filter(fecha_inicio__date=date.today()).order_by('fecha_inicio')
    importantes = Evento.objects.filter(importante=True, fecha_inicio__date__gt=date.today()).order_by('fecha_inicio')
    if len(eventos) + len(importantes) == 0:
        importantes = Evento.objects.all().order_by('fecha_inicio')
    return render(request, 'calendario.html', { 'eventos': eventos, 'importantes': importantes, 'hoy' : datetime.now().strftime('%d/%m/%Y')})

def calendario_diario(request, str_fecha):
    fecha = date(int(str_fecha[:4]), int(str_fecha[4:6]), int(str_fecha[6:]))
    eventos = Evento.objects.filter(fecha_inicio__date=fecha).order_by('fecha_inicio')
    return render(request, 'calendario.html', { 'eventos': eventos, 'hoy' : fecha.strftime('%d/%m/%Y')})