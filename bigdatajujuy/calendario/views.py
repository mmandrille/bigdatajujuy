from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
#Import Personales
from .models import Evento

# Create your views here.
def calendario(request):
    eventos = Evento.objects.filter(fecha_inicio__date=date.today()).order_by('fecha_inicio')
    importantes = Evento.objects.filter(importante=True, fecha_inicio__date__gt=date.today()).order_by('fecha_inicio')
    return render(request, 'calendario.html', { 'eventos': eventos, 'importantes': importantes, 'hoy' : datetime.now().strftime('%d/%m/%Y')})