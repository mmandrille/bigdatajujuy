#Modulos Standard
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
#Agregamos modulos personales
from .models import Faq, Conferencias
from .modelforms import ConferenciaForm
from inscripciones.models import Inscriptos

def home(request):
    casistentes = Inscriptos.objects.filter(activo=True, categoria=1).count()
    cexpositores = Inscriptos.objects.filter(autorizado=True, categoria=2).count()
    cconferencias = Conferencias.objects.filter(autorizada=True).count()
    texto_central = Faq.objects.filter().first()
    return render(request, 'home.html', {'casistentes': casistentes, 'cexpositores': cexpositores, 'cconferencias': cconferencias,
                                         'texto_central': texto_central, })

def mostrar_exposiciones(request):
    conferencias = Conferencias.objects.filter(autorizada=True)
    return render(request, 'conferencias.html', {'conferencias': conferencias, })

def cargar_exposicion(request, inscripto_id, inscripto_dni):
    try:
        inscripto = Inscriptos.objects.get(pk=inscripto_id, num_doc=inscripto_dni, autorizado=True, categoria=2) #Chequeamos si no esta inscripto y autorizado
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
    except Inscriptos.DoesNotExist: return render(request, 'resultado.html', {'texto': 'Aun no ha sido autorizado por la administracion para cargar Exposiciones.', })

def mostrar_expositores(request):
    expositores = Inscriptos.objects.filter(categoria=2, autorizado=True)
    return render(request, 'expositores.html', {'expositores': expositores, })

def contacto(request):
    return render(request, 'contacto.html', { })

def faq(request):
    faqs = Faq.objects.all().order_by('orden')
    return render(request, 'faq.html', {'faqs' : faqs })