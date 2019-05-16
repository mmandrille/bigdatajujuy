#Modulos Standard
from datetime import date
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
#Agregamos modulos personales
from .models import Faq, Conferencia
from .modelforms import ConferenciaForm
from inscripciones.models import Inscripto

def home(request):
    casistentes = Inscripto.objects.filter(activo=True, categoria=1).count()
    cexpositores = Inscripto.objects.filter(autorizado=True, categoria=2).count()
    cconferencias = Conferencia.objects.filter(autorizada=True).count()
    texto_central = Faq.objects.filter().first()
    return render(request, 'home.html', {'casistentes': casistentes, 'cexpositores': cexpositores, 'cconferencias': cconferencias,
                                         'texto_central': texto_central, })

def mostrar_exposiciones(request):
    conferencias = Conferencia.objects.filter(autorizada=True).order_by('evento__fecha_inicio')
    return render(request, 'conferencias.html', {'conferencias': conferencias, })

def mostrar_exposiciones_diario(request, str_fecha):
    fecha = date(int(str_fecha[:4]), int(str_fecha[4:6]), int(str_fecha[6:]))
    conferencias = Conferencia.objects.filter(autorizada=True, evento__fecha_inicio__date=fecha).order_by('evento__fecha_inicio')
    return render(request, 'conferencias.html', {'conferencias': conferencias, })

def cargar_exposicion(request, inscripto_id, inscripto_dni):
    try:
        inscripto = Inscripto.objects.get(pk=inscripto_id, num_doc=inscripto_dni, categoria=2) #Chequeamos si no esta inscripto y autorizado
        if request.method == 'POST':
            print(inscripto)
            form = ConferenciaForm(request.POST)
            if form.is_valid():#Si el formulario se completo correctamente
                conferencia = form.save(commit=False)
                conferencia.expositor = inscripto
                conferencia.save()
                return render(request, 'resultado.html', {'texto': 'La conferencia fue Agregada, espere a que sea revisada por la administracion.', })
        else:
            form = ConferenciaForm()
            return render(request, 'cargar_exposicion.html', {'inscripto': inscripto, 'form': form, })
    except Inscripto.DoesNotExist: return render(request, 'resultado.html', {'texto': 'Aun no ha sido autorizado por la administracion para cargar Exposiciones.', })

def mostrar_expositores(request):
    expositores = Inscripto.objects.filter(categoria=2, autorizado=True)
    return render(request, 'expositores.html', {'expositores': expositores, })

def mostrar_expositores_diario(request, str_fecha):
    fecha = date(int(str_fecha[:4]), int(str_fecha[4:6]), int(str_fecha[6:]))
    expositores = Inscripto.objects.filter(categoria=2, autorizado=True, conferencias__evento__fecha_inicio__date=fecha)
    return render(request, 'expositores.html', {'expositores': expositores, })

def contacto(request):
    return render(request, 'contacto.html', { })

def faq(request):
    faqs = Faq.objects.all().order_by('orden')
    return render(request, 'faq.html', {'faqs' : faqs })